package confluence.math.artin;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/// Java replication of the DEFINITIONS behind OAI.ArtinCAT0.main
/// (lean/ComparatorChallenges/ArtinCAT0.lean), definition for definition.
///
/// The theorem says: one explicit Artin group on 116 generators admits no proper, cocompact,
/// isometric action on any nonempty proper CAT(0) space. The group is three braid groups B_40
/// (each a 39-letter path with label 3, label 2 between non-neighbours) glued cyclically on the
/// letters 0,1,2 (which form a (3,3,3) triangle), plus two "sentinel" letters 3,4 that commute
/// with 0,1,2 and are free otherwise. The non-existence proof itself is in the Lean; Java cannot
/// replicate a statement quantified over all metric spaces. What Java CAN check is that the
/// objects are what they claim to be:
///
/// - the Coxeter matrix satisfies the three decidable conjuncts of `main` (symmetric, diagonal 1,
///   off-diagonal in {2, 3, infinity});
/// - the relator for label n is an alternating word of length n against its partner, and maps to
///   the identity in S_40 (block letter i -> transposition (i i+1)), while a relator of the WRONG
///   length does not (negative control);
/// - the Lean CAT0 inequality is exactly the Euclidean law-of-cosines comparison, holds in a
///   metric tree, and fails on the round sphere (negative control).
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.artin.ArtinCAT0
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Group presentations as test oracles.** The S_40 check is the cheap half of any presentation:
///   map generators to concrete permutations and confirm every relator dies. A Java library that
///   builds braid or Artin-group words (knot software, puzzle solvers, scrambling of permutations)
///   can keep exactly this check as a unit test, and the wrong-length relator as its negative case.
/// - **"Nonpositively curved" is not a free assumption.** Algorithms that assume unique geodesics and
///   convex distance functions (CAT(0) spaces: trees, Euclidean space, cube complexes used for
///   phylogenetic tree spaces) get midpoints, barycentres and convergent averaging for free. This
///   result says some well-defined groups cannot be modelled that way at all, so a Java design that
///   picks a CAT(0) model for a group's elements (for geometric hashing or averaging) needs to know
///   the group admits one.
/// - **A ready comparison-inequality checker.** `comparisonGap` is a four-line test of the
///   CAT(0) inequality for one sampled triangle; it can be dropped into property tests of any metric
///   (an edit distance, a graph metric) to detect positive curvature, as the sphere control does.
public class ArtinCAT0 {

    static final int N = 116;
    static final int TOP = Integer.MAX_VALUE; // WithTop ℕ's ⊤
    static int failures = 0;

    static void check(String name, boolean ok) {
        System.out.println((ok ? "ok   " : "FAIL ") + name);
        if (!ok) failures++;
    }

    // ---- Lean definitions, transcribed ----
    static int blockLetter(int b, int i) {
        if (i == 0) return b;
        if (i == 1) return (b + 1) % 3;
        return 5 + 37 * b + (i - 2);
    }

    /// Exists a block b and indices i, j with s = blockLetter b i, t = blockLetter b j and the given gap test.
    static boolean sameBlock(int s, int t, boolean adjacent) {
        for (int b = 0; b < 3; b++)
            for (int i = 0; i < 39; i++)
                for (int j = 0; j < 39; j++)
                    if (s == blockLetter(b, i) && t == blockLetter(b, j)
                            && (adjacent ? Math.abs(i - j) == 1 : Math.abs(i - j) >= 2)) return true;
        return false;
    }

    static boolean sentinel(int s, int t) {
        return ((s == 3 || s == 4) && t < 3) || ((t == 3 || t == 4) && s < 3);
    }

    static int explicitMatrix(int s, int t) {
        if (s == t) return 1;
        if (sameBlock(s, t, true)) return 3;
        if (sameBlock(s, t, false) || sentinel(s, t)) return 2;
        return TOP;
    }

    /// alternating s t 0 = 1, alternating s t (n+1) = of s * alternating t s n; letters as +-(x+1).
    static List<Integer> alternating(int s, int t, int n) {
        List<Integer> w = new ArrayList<>();
        for (int k = 0; k < n; k++) w.add((k % 2 == 0 ? s : t) + 1);
        return w;
    }

    static List<Integer> relator(int s, int t, int n) {
        List<Integer> w = new ArrayList<>(alternating(s, t, n));
        List<Integer> v = alternating(t, s, n);
        for (int k = v.size() - 1; k >= 0; k--) w.add(-v.get(k));
        return w;
    }

    /// Does word w map to the identity of S_40 when block b's letter i goes to transposition (i i+1)?
    static boolean diesInS40(int b, List<Integer> w) {
        int[] index = new int[N];
        java.util.Arrays.fill(index, -1);
        for (int i = 0; i < 39; i++) index[blockLetter(b, i)] = i;
        int[] p = new int[40];
        for (int k = 0; k < 40; k++) p[k] = k;
        for (int x : w) {
            int i = index[Math.abs(x) - 1];
            if (i < 0) throw new IllegalArgumentException("letter outside block");
            for (int k = 0; k < 40; k++) p[k] = p[k] == i ? i + 1 : p[k] == i + 1 ? i : p[k];
        }
        for (int k = 0; k < 40; k++) if (p[k] != k) return false;
        return true;
    }

    /// Lean RHS of CAT0: (t^2 - tu) d(x,y)^2 + (u^2 - tu) d(x,z)^2 + tu d(y,z)^2.
    static double comparisonRhs(double t, double u, double a, double b, double c) {
        return (t * t - t * u) * a * a + (u * u - t * u) * b * b + t * u * c * c;
    }

    /// lhs^2 - rhs: positive means the CAT(0) inequality is violated.
    static double comparisonGap(double d, double t, double u, double a, double b, double c) {
        return d * d - comparisonRhs(t, u, a, b, c);
    }

    public static void main(String[] args) {
        int[][] m = new int[N][N];
        for (int s = 0; s < N; s++) for (int t = 0; t < N; t++) m[s][t] = explicitMatrix(s, t);

        boolean sym = true, diag = true, vals = true;
        int threes = 0, twos = 0, tops = 0;
        for (int s = 0; s < N; s++) {
            diag &= m[s][s] == 1;
            for (int t = 0; t < N; t++) {
                sym &= m[s][t] == m[t][s];
                if (s != t) vals &= m[s][t] == 2 || m[s][t] == 3 || m[s][t] == TOP;
                if (s < t) { if (m[s][t] == 3) threes++; else if (m[s][t] == 2) twos++; else tops++; }
            }
        }
        check("conjunct 1: explicitMatrix symmetric", sym);
        check("conjunct 2: diagonal = 1", diag);
        check("conjunct 3: off-diagonal in {2,3,TOP}", vals);
        check("label census {3:114, 2:2115, TOP:4441} (matches replicate.py)",
              threes == 114 && twos == 2115 && tops == 4441);

        boolean lengths = true, expSum = true, inS40 = true;
        int intra = 0;
        for (int s = 0; s < N; s++)
            for (int t = 0; t < N; t++) {
                if (m[s][t] == TOP) continue;
                List<Integer> w = relator(s, t, m[s][t]);
                lengths &= w.size() == 2 * m[s][t];
                int sum = 0;
                for (int x : w) sum += Integer.signum(x);
                expSum &= sum == 0;
                if (s == t) continue;
                for (int b = 0; b < 3; b++) {
                    boolean sIn = false, tIn = false;
                    for (int i = 0; i < 39; i++) { sIn |= blockLetter(b, i) == s; tIn |= blockLetter(b, i) == t; }
                    if (sIn && tIn) { intra++; inS40 &= diesInS40(b, relator(s, t, m[s][t])); }
                }
            }
        check("relator for label n has length 2n", lengths);
        check("every relator has exponent sum 0 (s -> 1 onto Z: the group is infinite)", expSum);
        check("all " + intra + " intra-block relators die in S_40", intra == 4446 && inS40);

        int s = blockLetter(1, 4), t = blockLetter(1, 5), u = blockLetter(1, 9);
        check("CONTROL: length-2 relator on an adjacent pair survives in S_40", !diesInS40(1, relator(s, t, 2)));
        check("CONTROL: length-3 relator on a commuting pair survives in S_40", !diesInS40(1, relator(s, u, 3)));

        // Euclidean identity, exact in long arithmetic: scale t = T/D, u = U/D, multiply through by D^2.
        Random rnd = new Random(254);
        boolean exact = true;
        long D = 20;
        for (int k = 0; k < 2000; k++) {
            long[] x = {rnd.nextInt(101) - 50, rnd.nextInt(101) - 50};
            long[] y = {rnd.nextInt(101) - 50, rnd.nextInt(101) - 50};
            long[] z = {rnd.nextInt(101) - 50, rnd.nextInt(101) - 50};
            long T = rnd.nextInt(21), U = rnd.nextInt(21);
            long px0 = D * x[0] + T * (y[0] - x[0]), px1 = D * x[1] + T * (y[1] - x[1]);
            long qx0 = D * x[0] + U * (z[0] - x[0]), qx1 = D * x[1] + U * (z[1] - x[1]);
            long lhs = (px0 - qx0) * (px0 - qx0) + (px1 - qx1) * (px1 - qx1); // = D^2 |p-q|^2
            long a2 = sq(y[0] - x[0]) + sq(y[1] - x[1]), b2 = sq(z[0] - x[0]) + sq(z[1] - x[1]);
            long c2 = sq(z[0] - y[0]) + sq(z[1] - y[1]);
            long rhs = (T * T - T * U) * a2 + (U * U - T * U) * b2 + T * U * c2; // = D^2 * Lean RHS
            exact &= lhs == rhs;
        }
        check("R^2: Lean CAT0 RHS equals the squared comparison distance exactly (2000 samples)", exact);

        // Tripod with legs A, B, C: x, y, z at the leg ends.
        boolean tree = true;
        for (int k = 0; k < 2000; k++) {
            double A = 1 + rnd.nextInt(30), B = 1 + rnd.nextInt(30), C = 1 + rnd.nextInt(30);
            double tt = rnd.nextInt(41) / 40.0, uu = rnd.nextInt(41) / 40.0;
            double dp = tt * (A + B), dq = uu * (A + C);
            double d = (dp <= A && dq <= A) ? Math.abs(dp - dq) : (Math.abs(A - dp) + Math.abs(A - dq));
            tree &= comparisonGap(d, tt, uu, A + B, A + C, B + C) <= 1e-9;
        }
        check("tripod tree satisfies the CAT0 inequality (2000 samples)", tree);

        // Sphere octant triangle, midpoints of xy and xz: d = pi/3, sides pi/2.
        double side = Math.PI / 2, mid = Math.PI / 3;
        double gap = comparisonGap(mid, 0.5, 0.5, side, side, side);
        System.out.printf("     sphere octant: d^2 - rhs = %.6f%n", gap);
        check("CONTROL: round sphere violates the CAT0 inequality (gap > 0.05)", gap > 0.05);

        System.out.println();
        System.out.println(failures == 0 ? "ALL CHECKS AND CONTROLS BEHAVE" : failures + " FAILURE(S)");
        if (failures != 0) System.exit(1);
    }

    static long sq(long v) { return v * v; }
}
