package confluence.math.barnette;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/// Java replication of the DEFINITIONS behind OAI.Barnette.main
/// (lean/ComparatorChallenges/BarnetteHamiltonian.lean).
///
/// The theorem says: every finite simple graph that is cubic (3-regular), bipartite, planar and
/// 3-vertex-connected has a Hamiltonian cycle, a single cycle through every vertex. That is
/// Barnette's conjecture (1969). Java cannot replicate a statement over all such graphs, and it
/// does not decide planarity. What it CAN do is check the other definitions exactly on graphs that
/// are planar by construction (convex polyhedra), and search for the cycle:
///
/// - `cubic`: every vertex has degree 3;
/// - `bipartite`: a BFS 2-colouring succeeds;
/// - `threeConnected`: the Lean definition word for word, at least 4 vertices, and deleting ANY
///   set of at most two vertices leaves the rest connected (checked over every such set);
/// - `hamiltonianCycle`: a backtracking search for one spanning cycle, returned and re-verified.
///
/// Graphs (all convex polyhedra, hence planar): even prisms C_2k x K_2 for k = 2..8 (the 3-cube is
/// k = 2) and the permutohedron of S_4 (the truncated octahedron), built as the Cayley graph of S_4
/// on the three adjacent transpositions, which is bipartite by the sign of a permutation.
///
/// Controls: the Petersen graph is cubic and 3-connected but not bipartite (and not planar), and the
/// search must find NO Hamiltonian cycle in it; an odd prism C_5 x K_2 is cubic, planar and
/// 3-connected but not bipartite (it is Hamiltonian, so it shows bipartite is checked, not assumed);
/// and a graph with a cut pair (two cubes joined by a 2-edge bridge, made cubic) must fail
/// `threeConnected`.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.barnette.Barnette
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **A guaranteed tour on a common class of meshes.** Polyhedral meshes whose vertices all have
///   degree 3 and whose faces all have an even number of sides (hexagon-and-square cages,
///   truncated-octahedron cells, many CAD and chemistry graphs) are exactly Barnette graphs when
///   3-connected. If the theorem holds, a tour visiting every vertex once always exists there, so a
///   Java route planner, a toolpath generator or a mesh-strip encoder can treat "no tour found" as
///   a bug in the search, never as a property of the input.
/// - **Search should be complete, not hopeful.** Hamiltonian-cycle search is NP-hard in general,
///   and the Petersen control is the reminder that "cubic and 3-connected" is not enough. A Java
///   library should guard its fast path with the full hypothesis (cubic, bipartite, planar,
///   3-connected) and fall back to exhaustive search, or report "unknown", outside it.
/// - **Check the hypothesis you rely on.** The 3-connectivity check here is the literal Lean
///   definition (delete any two vertices, stay connected), which is quadratic in vertices times a
///   BFS. That is cheap enough to run as a precondition assert before trusting the guarantee.
public class Barnette {

    static int failures = 0;

    static void check(String name, boolean ok) {
        System.out.println((ok ? "ok   " : "FAIL ") + name);
        if (!ok) failures++;
    }

    // ---- graph helpers ----
    record Graph(String name, List<int[]> adj) {
        int n() { return adj.size(); }
    }

    static Graph fromEdges(String name, int n, int[][] edges) {
        List<List<Integer>> a = new ArrayList<>();
        for (int i = 0; i < n; i++) a.add(new ArrayList<>());
        for (int[] e : edges) { a.get(e[0]).add(e[1]); a.get(e[1]).add(e[0]); }
        List<int[]> adj = new ArrayList<>();
        for (List<Integer> l : a) adj.add(l.stream().mapToInt(Integer::intValue).toArray());
        return new Graph(name, adj);
    }

    static Graph prism(int m) {
        List<int[]> e = new ArrayList<>();
        for (int i = 0; i < m; i++) {
            e.add(new int[]{i, (i + 1) % m});
            e.add(new int[]{m + i, m + (i + 1) % m});
            e.add(new int[]{i, m + i});
        }
        return fromEdges("prism C" + m + " x K2", 2 * m, e.toArray(new int[0][]));
    }

    /// Cayley graph of S_4 on the adjacent transpositions (01), (12), (23): the truncated octahedron.
    static Graph permutohedron4() {
        List<int[]> perms = new ArrayList<>();
        permute(new int[]{0, 1, 2, 3}, 0, perms);
        List<int[]> e = new ArrayList<>();
        for (int i = 0; i < perms.size(); i++)
            for (int s = 0; s < 3; s++) {
                int[] q = perms.get(i).clone();
                int t = q[s]; q[s] = q[s + 1]; q[s + 1] = t;
                int j = indexOf(perms, q);
                if (i < j) e.add(new int[]{i, j});
            }
        return fromEdges("permutohedron of S4 (truncated octahedron)", perms.size(), e.toArray(new int[0][]));
    }

    static void permute(int[] a, int k, List<int[]> out) {
        if (k == a.length) { out.add(a.clone()); return; }
        for (int i = k; i < a.length; i++) {
            int t = a[k]; a[k] = a[i]; a[i] = t;
            permute(a, k + 1, out);
            t = a[k]; a[k] = a[i]; a[i] = t;
        }
    }

    static int indexOf(List<int[]> l, int[] q) {
        for (int i = 0; i < l.size(); i++) if (Arrays.equals(l.get(i), q)) return i;
        return -1;
    }

    static Graph petersen() {
        int[][] e = {{0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 0}, {5, 7}, {7, 9}, {9, 6}, {6, 8}, {8, 5},
                     {0, 5}, {1, 6}, {2, 7}, {3, 8}, {4, 9}};
        return fromEdges("Petersen", 10, e);
    }

    /// Two 3-cubes, each with one edge removed, joined across by two edges: cubic, but {u, v} is a cut pair.
    static Graph cubesWithCutPair() {
        List<int[]> e = new ArrayList<>();
        for (int c = 0; c < 2; c++) {
            int o = 8 * c;
            for (int a = 0; a < 8; a++)
                for (int b = a + 1; b < 8; b++)
                    if (Integer.bitCount(a ^ b) == 1 && !(a == 0 && b == 1)) e.add(new int[]{o + a, o + b});
        }
        e.add(new int[]{0, 8});
        e.add(new int[]{1, 9});
        return fromEdges("two cubes joined by a 2-edge bridge", 16, e.toArray(new int[0][]));
    }

    // ---- the Lean definitions ----
    static boolean cubic(Graph g) {
        for (int[] a : g.adj()) if (a.length != 3) return false;
        return true;
    }

    static boolean bipartite(Graph g) {
        int[] col = new int[g.n()];
        Arrays.fill(col, -1);
        for (int s = 0; s < g.n(); s++) {
            if (col[s] != -1) continue;
            col[s] = 0;
            int[] q = new int[g.n()];
            int h = 0, t = 0;
            q[t++] = s;
            while (h < t) {
                int v = q[h++];
                for (int w : g.adj().get(v)) {
                    if (col[w] == -1) { col[w] = 1 - col[v]; q[t++] = w; }
                    else if (col[w] == col[v]) return false;
                }
            }
        }
        return true;
    }

    static boolean connectedWithout(Graph g, boolean[] removed) {
        int start = -1, alive = 0;
        for (int v = 0; v < g.n(); v++) if (!removed[v]) { alive++; if (start < 0) start = v; }
        if (alive == 0) return false; // Mathlib: the empty graph is not Connected
        boolean[] seen = new boolean[g.n()];
        int[] stack = new int[g.n()];
        int sp = 0, count = 0;
        stack[sp++] = start; seen[start] = true;
        while (sp > 0) {
            int v = stack[--sp]; count++;
            for (int w : g.adj().get(v)) if (!removed[w] && !seen[w]) { seen[w] = true; stack[sp++] = w; }
        }
        return count == alive;
    }

    /// ThreeVertexConnected: 4 <= |V| and for every S with |S| <= 2, G - S is connected.
    static boolean threeConnected(Graph g) {
        int n = g.n();
        if (n < 4) return false;
        boolean[] rem = new boolean[n];
        if (!connectedWithout(g, rem)) return false;
        for (int a = 0; a < n; a++) {
            rem[a] = true;
            if (!connectedWithout(g, rem)) return false;
            for (int b = a + 1; b < n; b++) {
                rem[b] = true;
                if (!connectedWithout(g, rem)) return false;
                rem[b] = false;
            }
            rem[a] = false;
        }
        return true;
    }

    static int[] hamiltonianCycle(Graph g) {
        int n = g.n();
        int[] path = new int[n];
        boolean[] used = new boolean[n];
        path[0] = 0; used[0] = true;
        return extend(g, path, used, 1) ? path : null;
    }

    static boolean extend(Graph g, int[] path, boolean[] used, int k) {
        int n = g.n(), last = path[k - 1];
        if (k == n) {
            for (int w : g.adj().get(last)) if (w == path[0]) return true;
            return false;
        }
        for (int w : g.adj().get(last)) {
            if (used[w]) continue;
            used[w] = true; path[k] = w;
            if (extend(g, path, used, k + 1)) return true;
            used[w] = false;
        }
        return false;
    }

    static boolean isHamiltonianCycle(Graph g, int[] cyc) {
        if (cyc == null || cyc.length != g.n()) return false;
        boolean[] seen = new boolean[g.n()];
        for (int v : cyc) { if (seen[v]) return false; seen[v] = true; }
        for (int i = 0; i < cyc.length; i++) {
            int a = cyc[i], b = cyc[(i + 1) % cyc.length];
            boolean adj = false;
            for (int w : g.adj().get(a)) if (w == b) adj = true;
            if (!adj) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        List<Graph> barnette = new ArrayList<>();
        for (int k = 2; k <= 8; k++) barnette.add(prism(2 * k));
        barnette.add(permutohedron4());
        for (Graph g : barnette) {
            boolean hyp = cubic(g) && bipartite(g) && threeConnected(g);
            int[] cyc = hamiltonianCycle(g);
            check(g.name() + " (" + g.n() + " vertices): cubic, bipartite, 3-connected, and a verified Hamiltonian cycle",
                hyp && isHamiltonianCycle(g, cyc));
        }

        Graph p = petersen();
        check("control: Petersen is cubic and 3-connected", cubic(p) && threeConnected(p));
        check("control: Petersen is not bipartite", !bipartite(p));
        check("control: the search finds NO Hamiltonian cycle in Petersen", hamiltonianCycle(p) == null);

        Graph odd = prism(5);
        check("control: odd prism C5 x K2 is cubic and 3-connected but not bipartite",
            cubic(odd) && threeConnected(odd) && !bipartite(odd));

        Graph cut = cubesWithCutPair();
        check("control: two cubes on a 2-edge bridge are cubic and bipartite but NOT 3-connected",
            cubic(cut) && bipartite(cut) && !threeConnected(cut));

        System.out.println(failures == 0 ? "ALL CHECKS PASSED" : failures + " CHECK(S) FAILED");
        if (failures != 0) System.exit(1);
    }
}
