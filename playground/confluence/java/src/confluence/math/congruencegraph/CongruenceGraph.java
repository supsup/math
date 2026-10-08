package confluence.math.congruencegraph;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/// Exhaustive small-case check of OAI.FiniteCongruence.graph_criterion
/// (lean/ComparatorChallenges/FiniteCongruenceGraph.lean), both sides implemented from the
/// challenge definitions, not from the proof.
///
/// The theorem: a finite lattice `L` is isomorphic to the full congruence lattice of some
/// nonempty finite algebra (finitely many operations, finite arities) if and only if there is a
/// nonempty finite set `Fin n` and a coloring `color : Fin n -> Fin n -> L` that is
///
/// 1. symmetric,
/// 2. `⊥` exactly on the diagonal,
/// 3. a join-triangle inequality: `color(x,y) <= color(x,z) ⊔ color(z,y)`,
/// 4. separating: if `a` is not `<= b`, some edge has color `<= a` and not `<= b`
///    (equivalently: every element is the join of the edge colors below it),
/// 5. generating: for every nonempty seed set `S` of ordered pairs, every pair whose color is
///    `<= ⊔ color(S)` is joined by a path of images of seeds under "admissible" maps, the
///    self-maps `p` with `color(p x, p y) <= color(x, y)`.
///
/// Both sides are existential over `n`, so this class checks the stronger size-matched form:
/// for every lattice with at most [#MAX_LATTICE] elements and every `n <= ` [#MAX_N],
/// `A_n(L)` (some algebra on `Fin n` has congruence lattice `≅ L`) agrees with `B_n(L)` (some
/// coloring on `Fin n` is a witness). The Lean proof is size-preserving in both directions, so
/// the size-matched form is what it actually establishes.
///
/// Side A uses one reduction, checked in the Python companion against random algebras with
/// arities 0..3: compatibility with an operation equals compatibility with its one-variable
/// translations, so the attainable congruence families on `Fin n` are exactly the intersections
/// of the families `Con(f)` for single maps `f : n -> n` (the empty intersection being all
/// equivalences, the algebra with no operations).
///
/// Negative control: dropping conjunct 5 (generation) must make the two sides disagree. It does,
/// at `n = 4` on M4 (bottom, four atoms, top), which has no algebra on four points; the coloring
/// [#M4_COLOR] passes conjuncts 1 to 4 and fails 5 at seed (0,1).
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.congruencegraph.CongruenceGraph
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Testing a lattice of "equivalences that survive the operations".** Any Java system that
///   partitions states and needs the partition respected by its transitions (DFA minimisation,
///   bisimulation in model checkers, cache keys that must be stable under a transformation) is
///   computing congruences of a finite unary algebra. The family enumeration here is a brute-force
///   oracle such code can be compared against on tiny inputs.
/// - **A certificate format smaller than the algebra.** The criterion turns "this lattice is a
///   congruence lattice" into a colored complete graph plus a checkable condition. A tool that
///   searches for representations could emit the coloring as its certificate and a separate,
///   simple checker (like [#isWitness]) could validate it without trusting the search.
/// - **Generation is the load-bearing clause.** The control shows the metric-like conditions
///   (symmetry, triangle, separation) are satisfiable for lattices that are NOT representable at
///   that size. A Java validator that checks only the cheap clauses would accept wrong
///   certificates; the expensive closure check cannot be skipped.
/// - **Minimal-closure trick.** Conjunct 5 quantifies over all 2^(n^2) seed sets, but depends
///   only on the pair (join of seed colors, union of seed images); closing singletons under that
///   pairwise union is exponentially cheaper. The same trick applies to any Java check of the
///   form "for every subset, a monotone join-property holds".
public class CongruenceGraph {

    static final int MAX_LATTICE = 6;
    static final int MAX_N = 4;
    static final int[][] M4_COLOR = {{0, 1, 1, 2}, {1, 0, 1, 3}, {1, 1, 0, 4}, {2, 3, 4, 0}};

    /// A finite lattice given by its order matrix and join table, bottom at index 0.
    record Lattice(boolean[][] leq, int[][] join, String key) {
        int size() { return leq.length; }
    }

    // ------------------------------------------------------------- lattices up to iso

    static int[][] joinTable(boolean[][] leq) {
        int k = leq.length;
        int[][] join = new int[k][k];
        for (int a = 0; a < k; a++)
            for (int b = 0; b < k; b++) {
                int least = -1, count = 0;
                for (int c = 0; c < k; c++) {
                    if (!leq[a][c] || !leq[b][c]) continue;
                    boolean isLeast = true;
                    for (int d = 0; d < k; d++)
                        if (leq[a][d] && leq[b][d] && !leq[c][d]) { isLeast = false; break; }
                    if (isLeast) { least = c; count++; }
                }
                if (count != 1) return null;
                join[a][b] = least;
            }
        return join;
    }

    /// Canonical key: lexicographically least order string over relabelings fixing bottom/top.
    static String canon(boolean[][] leq) {
        int k = leq.length;
        int bot = -1, top = -1;
        for (int i = 0; i < k; i++) {
            boolean b = true, t = true;
            for (int j = 0; j < k; j++) { b &= leq[i][j]; t &= leq[j][i]; }
            if (b) bot = i;
            if (t) top = i;
        }
        List<Integer> interior = new ArrayList<>();
        for (int i = 0; i < k; i++) if (i != bot && i != top) interior.add(i);
        String[] best = {null};
        int[] order = new int[k];
        order[0] = bot;
        if (k > 1) order[k - 1] = top;
        permute(interior, 0, order, leq, best);
        return best[0];
    }

    static void permute(List<Integer> items, int pos, int[] order, boolean[][] leq, String[] best) {
        int k = leq.length;
        if (pos == items.size()) {
            StringBuilder sb = new StringBuilder(k * k);
            for (int i = 0; i < k; i++) for (int j = 0; j < k; j++) sb.append(leq[order[i]][order[j]] ? '1' : '0');
            String s = sb.toString();
            if (best[0] == null || s.compareTo(best[0]) < 0) best[0] = s;
            return;
        }
        for (int i = pos; i < items.size(); i++) {
            java.util.Collections.swap(items, pos, i);
            order[pos + 1] = items.get(pos);
            permute(items, pos + 1, order, leq, best);
            java.util.Collections.swap(items, pos, i);
        }
    }

    /// All lattices of size k up to isomorphism. Elements are labeled along a linear extension,
    /// so only relations i < j between interior elements are enumerated.
    static List<Lattice> lattices(int k) {
        Map<String, Lattice> found = new java.util.LinkedHashMap<>();
        List<int[]> pairs = new ArrayList<>();
        for (int i = 1; i < k - 1; i++) for (int j = i + 1; j < k - 1; j++) pairs.add(new int[] {i, j});
        for (long bits = 0; bits < (1L << pairs.size()); bits++) {
            boolean[][] leq = new boolean[k][k];
            for (int i = 0; i < k; i++) { leq[i][i] = true; leq[0][i] = true; leq[i][k - 1] = true; }
            for (int t = 0; t < pairs.size(); t++)
                if ((bits >> t & 1) == 1) leq[pairs.get(t)[0]][pairs.get(t)[1]] = true;
            boolean transitive = true;
            for (int a = 0; a < k && transitive; a++)
                for (int b = 0; b < k && transitive; b++)
                    for (int c = 0; c < k; c++)
                        if (leq[a][b] && leq[b][c] && !leq[a][c]) { transitive = false; break; }
            if (!transitive) continue;
            int[][] join = joinTable(leq);
            if (join == null) continue;
            String key = canon(leq);
            found.putIfAbsent(key, new Lattice(leq, join, key));
        }
        return new ArrayList<>(found.values());
    }

    // ------------------------------------------------------------- side A: Representable

    static List<int[]> partitions(int n) {
        List<int[]> out = new ArrayList<>();
        partRec(new int[n], 0, 0, out);
        return out;
    }

    static void partRec(int[] cur, int pos, int blocks, List<int[]> out) {
        if (pos == cur.length) { out.add(cur.clone()); return; }
        for (int b = 0; b <= blocks; b++) {
            cur[pos] = b;
            partRec(cur, pos + 1, Math.max(blocks, b + 1), out);
        }
    }

    static int[][] allMaps(int n) {
        int count = 1;
        for (int i = 0; i < n; i++) count *= n;
        int[][] maps = new int[count][n];
        for (int m = 0; m < count; m++) {
            int v = m;
            for (int i = 0; i < n; i++) { maps[m][i] = v % n; v /= n; }
        }
        return maps;
    }

    /// Canonical keys of congruence lattices of algebras on Fin n with at most maxSize elements.
    static Set<String> representable(int n, int maxSize) {
        List<int[]> parts = partitions(n);
        int p = parts.size();   // <= 15 for n <= 4, so a long bitmask suffices
        Set<Long> single = new HashSet<>();
        for (int[] f : allMaps(n)) {
            long mask = 0;
            for (int i = 0; i < p; i++) {
                int[] q = parts.get(i);
                boolean ok = true;
                for (int x = 0; x < n && ok; x++)
                    for (int y = 0; y < n; y++)
                        if (q[x] == q[y] && q[f[x]] != q[f[y]]) { ok = false; break; }
                if (ok) mask |= 1L << i;
            }
            single.add(mask);
        }
        long full = (1L << p) - 1;
        Set<Long> fams = new HashSet<>(List.of(full));
        List<Long> frontier = List.of(full);
        while (!frontier.isEmpty()) {
            List<Long> next = new ArrayList<>();
            for (long a : frontier) for (long s : single) if (fams.add(a & s)) next.add(a & s);
            frontier = next;
        }
        Set<String> keys = new HashSet<>();
        for (long m : fams) {
            int[] idx = java.util.stream.IntStream.range(0, p).filter(i -> (m >> i & 1) == 1).toArray();
            if (idx.length > maxSize) continue;
            boolean[][] leq = new boolean[idx.length][idx.length];
            for (int i = 0; i < idx.length; i++)
                for (int j = 0; j < idx.length; j++)
                    leq[i][j] = refines(parts.get(idx[i]), parts.get(idx[j]));
            keys.add(canon(leq));
        }
        return keys;
    }

    static boolean refines(int[] a, int[] b) {
        for (int x = 0; x < a.length; x++)
            for (int y = 0; y < a.length; y++)
                if (a[x] == a[y] && b[x] != b[y]) return false;
        return true;
    }

    // ------------------------------------------------------------- side B: HasGraphWitness

    static int[] classes(int n, Set<Long> edges) {
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        for (long e : edges) {
            int a = find(parent, (int) (e >> 8)), b = find(parent, (int) (e & 0xff));
            parent[a] = b;
        }
        for (int i = 0; i < n; i++) parent[i] = find(parent, i);
        return parent;
    }

    static int find(int[] parent, int x) {
        while (parent[x] != x) x = parent[x] = parent[parent[x]];
        return x;
    }

    /// IsGraphWitness conjunct by conjunct; `checkGeneration = false` is the negative control.
    static boolean isWitness(int n, Lattice lat, int[][] color, int[][] maps, boolean checkGeneration) {
        boolean[][] leq = lat.leq();
        int[][] join = lat.join();
        for (int x = 0; x < n; x++)
            for (int y = 0; y < n; y++) {
                if (color[x][y] != color[y][x]) return false;
                if ((color[x][y] == 0) != (x == y)) return false;
                for (int z = 0; z < n; z++)
                    if (!leq[color[x][y]][join[color[x][z]][color[z][y]]]) return false;
            }
        for (int lo = 0; lo < lat.size(); lo++)
            for (int up = 0; up < lat.size(); up++) {
                if (leq[lo][up]) continue;
                boolean found = false;
                for (int x = 0; x < n && !found; x++)
                    for (int y = 0; y < n; y++)
                        if (leq[color[x][y]][lo] && !leq[color[x][y]][up]) { found = true; break; }
                if (!found) return false;
            }
        if (!checkGeneration) return true;
        List<int[]> adm = new ArrayList<>();
        for (int[] f : maps) {
            boolean ok = true;
            for (int x = 0; x < n && ok; x++)
                for (int y = 0; y < n; y++)
                    if (!leq[color[f[x]][f[y]]][color[x][y]]) { ok = false; break; }
            if (ok) adm.add(f);
        }
        // conjunct 5 depends on a seed set only via (join of colors, union of seed images)
        record State(int sup, Set<Long> marked) {}
        List<State> start = new ArrayList<>();
        for (int x = 0; x < n; x++)
            for (int y = 0; y < n; y++) {
                Set<Long> img = new HashSet<>();
                for (int[] f : adm) img.add(((long) f[x] << 8) | f[y]);
                start.add(new State(color[x][y], img));
            }
        Set<State> seen = new HashSet<>(start);
        List<State> frontier = new ArrayList<>(seen);
        while (!frontier.isEmpty()) {
            List<State> next = new ArrayList<>();
            for (State a : frontier)
                for (State b : start) {
                    Set<Long> u = new HashSet<>(a.marked());
                    u.addAll(b.marked());
                    State c = new State(join[a.sup()][b.sup()], u);
                    if (seen.add(c)) next.add(c);
                }
            frontier = next;
        }
        for (State s : seen) {
            int[] cls = classes(n, s.marked());
            for (int x = 0; x < n; x++)
                for (int y = 0; y < n; y++)
                    if (leq[color[x][y]][s.sup()] && cls[x] != cls[y]) return false;
        }
        return true;
    }

    /// Exists a witness on Fin n: symmetric colorings, bottom exactly on the diagonal (any
    /// witness has that shape by conjuncts 1 and 2), off-diagonal values from L minus bottom.
    static boolean hasWitness(int n, Lattice lat, boolean checkGeneration) {
        int[][] maps = allMaps(n);
        int pairs = n * (n - 1) / 2, base = lat.size() - 1;
        if (pairs > 0 && base == 0) return false;
        long total = 1;
        for (int i = 0; i < pairs; i++) total *= base;
        int[][] color = new int[n][n];
        for (long code = 0; code < total; code++) {
            long v = code;
            for (int x = 0; x < n; x++)
                for (int y = x + 1; y < n; y++) {
                    color[x][y] = color[y][x] = 1 + (int) (v % base);
                    v /= base;
                }
            if (isWitness(n, lat, color, maps, checkGeneration)) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        List<Lattice> lats = new ArrayList<>();
        for (int k = 1; k <= MAX_LATTICE; k++) {
            List<Lattice> ls = lattices(k);
            System.out.printf("lattices of size %d: %d%n", k, ls.size());
            lats.addAll(ls);
        }
        int instances = 0, aTrue = 0, bTrue = 0, mismatches = 0, controlHits = 0;
        for (int n = 1; n <= MAX_N; n++) {
            Set<String> rep = representable(n, MAX_LATTICE);
            for (Lattice lat : lats) {
                boolean a = rep.contains(lat.key());
                boolean b = hasWitness(n, lat, true);
                instances++;
                if (a) aTrue++;
                if (b) bTrue++;
                if (a != b) { mismatches++; System.out.printf("MISMATCH n=%d lattice %s%n", n, lat.key()); }
                if (!a && hasWitness(n, lat, false)) {
                    controlHits++;
                    System.out.printf("  control (no generation) disagrees: n=%d |L|=%d order %s%n",
                        n, lat.size(), lat.key());
                }
            }
        }
        System.out.printf("instances %d, A true %d, B true %d, mismatches %d%n", instances, aTrue, bTrue, mismatches);
        System.out.printf("control without conjunct 5: %d disagreeing instances%n", controlHits);

        // the explicit control coloring on M4 = bottom, four atoms, top
        boolean[][] m4leq = {
            {true, true, true, true, true, true}, {false, true, false, false, false, true},
            {false, false, true, false, false, true}, {false, false, false, true, false, true},
            {false, false, false, false, true, true}, {false, false, false, false, false, true}};
        Lattice m4raw = new Lattice(m4leq, joinTable(m4leq), canon(m4leq));
        int[][] maps = allMaps(4);
        boolean weak = isWitness(4, m4raw, M4_COLOR, maps, false);
        boolean strong = isWitness(4, m4raw, M4_COLOR, maps, true);
        boolean m4rep = representable(4, MAX_LATTICE).contains(m4raw.key());
        System.out.printf("M4 coloring %s: conjuncts 1-4 %b, all five %b; M4 representable on Fin 4: %b%n",
            Arrays.deepToString(M4_COLOR), weak, strong, m4rep);
        boolean ok = mismatches == 0 && controlHits > 0 && weak && !strong && !m4rep;
        System.out.println(ok ? "OK" : "FAILED");
        if (!ok) System.exit(1);
    }
}
