package confluence.math.commonbases;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.function.IntPredicate;

/// Brute-force companion to OAI.common_bases_fpras
/// (lean/ComparatorChallenges/CommonBasesFPRAS.lean).
///
/// The Lean theorem asserts a single randomized oracle program that approximates
/// `commonBaseCount M₁ M₂`, the number of sets that are bases of both matroids. This class does
/// not implement that program. It computes the quantity the program approximates, exactly, two
/// independent ways, on small instances whose answers are also known from elsewhere:
///
/// - **direct**: enumerate subsets, keep those that are bases of both (the Lean definition);
/// - **paired reduction** (paper, Section 2): build K = M₁ ⊕ M₂* on 2n elements as an explicit basis
///   family (dual bases are complements), and count the transversals
///   S(A) = {xᵢ : i ∈ A} ∪ {yᵢ : i ∉ A} that are bases of K.
///
/// Known values used as a third channel: K4 has 4² = 16 spanning trees (Cayley); the two partition
/// matroids of K3,3 have 3! = 6 common bases (its perfect matchings); U(3,6) with itself has C(6,3) = 20.
///
/// The NEGATIVE CONTROL builds K with M₂ instead of M₂* and must disagree with the direct count on at
/// least one instance; a claimed count of 17 for K4 must also be rejected. Exit status is non-zero if
/// any check or control misbehaves.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.commonbases.CommonBases
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Common bases are a real query shape.** "Pick a set that is simultaneously a spanning tree of
///   network A and of network B", or "assign one task per worker that is also one worker per shift"
///   (two partition matroids, i.e. bipartite perfect matchings) are both common-base problems. A Java
///   planner that wants to know HOW MANY such choices exist, for example to report slack or to
///   sample one uniformly, is asking the question the theorem addresses.
/// - **An oracle interface is enough.** The theorem's algorithm sees each matroid only through a
///   yes/no `isIndependent(subset)` call. In Java that is an `IntPredicate` or `Predicate<BitSet>`,
///   so a library could accept graphic, linear or custom constraints behind one interface.
///   `fromIndependence` below is that shape, in miniature.
/// - **A brute-force oracle for tests.** Any approximate counter or sampler written in Java (MCMC,
///   annealing) needs ground truth on small inputs. `countDirect` plus `countPaired` is a two-channel
///   reference that a property-based test could compare against, with the dual-swap mutant as a
///   ready-made check that the test can fail.
/// - **Exponential, deliberately.** Everything here is O(2ⁿ) or worse and is only for n of about a
///   dozen. Nothing in this file is evidence that the theorem's polynomial algorithm is practical; the
///   Lean proof's polynomial has an unstated, possibly very large, degree.
public class CommonBases {

    record Matroid(int n, Set<Integer> bases) {
        int rank() { return Integer.bitCount(bases.iterator().next()); }
    }

    static Matroid fromIndependence(int n, IntPredicate indep) {
        int r = 0;
        List<Integer> ind = new ArrayList<>();
        for (int m = 0; m < (1 << n); m++) if (indep.test(m)) { ind.add(m); r = Math.max(r, Integer.bitCount(m)); }
        Set<Integer> bases = new HashSet<>();
        for (int m : ind) if (Integer.bitCount(m) == r) bases.add(m);
        return new Matroid(n, bases);
    }

    static boolean basisExchange(Matroid M) {
        for (int a : M.bases()) for (int b : M.bases()) for (int e = 0; e < M.n(); e++) {
            if (((a >> e) & 1) == 0 || ((b >> e) & 1) == 1) continue;
            boolean found = false;
            for (int f = 0; f < M.n() && !found; f++)
                if (((b >> f) & 1) == 1 && ((a >> f) & 1) == 0 && M.bases().contains((a & ~(1 << e)) | (1 << f)))
                    found = true;
            if (!found) return false;
        }
        return !M.bases().isEmpty();
    }

    static Matroid uniform(int r, int n) { return fromIndependence(n, m -> Integer.bitCount(m) <= r); }

    /// One element per block, capacity one; elements in no block are loops.
    static Matroid partition(int n, int[][] blocks) {
        return fromIndependence(n, m -> {
            int covered = 0;
            for (int[] b : blocks) {
                int c = 0;
                for (int e : b) { covered |= 1 << e; c += (m >> e) & 1; }
                if (c > 1) return false;
            }
            return (m & ~covered) == 0;
        });
    }

    static Matroid graphic(int nv, int[][] edges) {
        return fromIndependence(edges.length, m -> {
            int[] parent = new int[nv];
            for (int i = 0; i < nv; i++) parent[i] = i;
            for (int i = 0; i < edges.length; i++) {
                if (((m >> i) & 1) == 0) continue;
                int a = find(parent, edges[i][0]), b = find(parent, edges[i][1]);
                if (a == b) return false;
                parent[a] = b;
            }
            return true;
        });
    }

    static int find(int[] p, int x) { while (p[x] != x) x = p[x] = p[p[x]]; return x; }

    static long countDirect(Matroid M1, Matroid M2) {
        return M1.bases().stream().filter(M2.bases()::contains).count();
    }

    static long countPaired(Matroid M1, Matroid M2, boolean useDual) {
        int n = M1.n(), full = (1 << n) - 1;
        Set<Long> K = new HashSet<>();
        for (int b1 : M1.bases()) for (int b2 : M2.bases())
            K.add((long) b1 | ((long) (useDual ? full & ~b2 : b2) << n));
        long c = 0;
        for (int A = 0; A <= full; A++) if (K.contains((long) A | ((long) (full & ~A) << n))) c++;
        return c;
    }

    record Case(String name, Matroid m1, Matroid m2, long known) {}

    public static void main(String[] args) {
        int[][] k4 = {{0, 1}, {0, 2}, {0, 3}, {1, 2}, {1, 3}, {2, 3}};
        int[][] left = {{0, 1, 2}, {3, 4, 5}, {6, 7, 8}}, right = {{0, 3, 6}, {1, 4, 7}, {2, 5, 8}};
        List<Case> cases = List.of(
            new Case("graphic K4 vs itself", graphic(4, k4), graphic(4, k4), 16),
            new Case("K3,3 partition pair (perfect matchings)", partition(9, left), partition(9, right), 6),
            new Case("U(3,6) vs U(3,6)", uniform(3, 6), uniform(3, 6), 20),
            new Case("partition {0,1},{2} vs {3,4},{2}", partition(5, new int[][]{{0, 1}, {2}}),
                     partition(5, new int[][]{{3, 4}, {2}}), 0),
            new Case("C4+chord vs relabelled C4+chord", graphic(4, new int[][]{{0, 1}, {1, 2}, {2, 3}, {3, 0}, {0, 2}}),
                     graphic(4, new int[][]{{3, 0}, {0, 2}, {2, 3}, {1, 2}, {0, 1}}), -1));
        int failures = 0;
        boolean controlCaught = false;
        for (Case c : cases) {
            boolean ok = basisExchange(c.m1()) && basisExchange(c.m2()) && c.m1().rank() == c.m2().rank();
            long d = countDirect(c.m1(), c.m2()), p = countPaired(c.m1(), c.m2(), true);
            long bad = countPaired(c.m1(), c.m2(), false);
            ok &= d == p && (c.known() < 0 || d == c.known());
            if (bad != d) controlCaught = true;
            System.out.printf("%s %-42s direct=%d paired=%d known=%s (dual-swap mutant=%d)%n",
                ok ? "PASS" : "FAIL", c.name(), d, p, c.known() < 0 ? "-" : c.known(), bad);
            if (!ok) failures++;
        }
        System.out.println((controlCaught ? "PASS" : "FAIL") + " NEGATIVE CONTROL: dual-swap mutant disagrees on >=1 case");
        if (!controlCaught) failures++;
        boolean rejects17 = countDirect(cases.get(0).m1(), cases.get(0).m2()) != 17;
        System.out.println((rejects17 ? "PASS" : "FAIL") + " NEGATIVE CONTROL: claimed count 17 for K4 is rejected");
        if (!rejects17) failures++;
        System.out.println(failures == 0 ? "ALL OK" : failures + " FAILURE(S)");
        if (failures != 0) System.exit(1);
    }
}
