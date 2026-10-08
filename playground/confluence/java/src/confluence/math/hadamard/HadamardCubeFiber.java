package confluence.math.hadamard;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/// Java replication of OAI.HadamardSix.rowRatio_cubeFiber_sum_zero
/// (lean/ComparatorChallenges/HadamardCubeFiber.lean), definition for definition.
///
/// A 6x6 complex matrix H is Hadamard when every entry has modulus 1 and H^* H = 6 I. The row ratio
/// of rows i and j is the vector v_k = H[i][k] * conj(H[j][k]); its "cube fibre" at a value a is the
/// set of positions k with v_k^3 = a. The theorem: if H AND its entrywise square H o H are both
/// Hadamard, i != j, a != b, and every v_k^3 is a or b, then the sum of v_k over the fibre at a is 0.
///
/// The hypothesis "H o H is Hadamard" is strong. The paper behind this lemma (Exact Fourier
/// certificates..., Prop. "Classification of the cubic alternative") proves every such H is
/// equivalent to Tao's cubic matrix, whose row ratios all have the SAME cube. So on matrices the
/// theorem's conclusion is always a whole-row inner product (0 by orthogonality) or an empty sum. The
/// case with two genuinely different cube values lives at VECTOR level (unit v with sum v = sum v^2 = 0),
/// which is what the Lean proof actually uses; this class checks both levels.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.hadamard.HadamardCubeFiber
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Check every hypothesis, not just the conclusion.** The Fourier matrix F6 is a perfectly good
///   Hadamard matrix and some of its row pairs even have two-valued cubes, yet the fibre sum there is 3,
///   not 0, because F6 o F6 is not Hadamard. A Java test that only asserted "fibre sum is ~0" on a
///   hand-picked Hadamard matrix could pass or fail for reasons unrelated to the claim; tests of a
///   conditional statement should assert the precondition explicitly and keep a case where it fails.
/// - **Exact equality on doubles needs a declared tolerance.** The fibre is defined by v_k^3 == a, an
///   exact equality in Lean. In Java the cube of e^{2 pi i/3} is 1 only to about 1e-15, so `==` would put
///   every position in the wrong fibre. The tolerance here (`TOL`) is a modelling choice and is printed.
/// - **A small, self-checking fixture for complex linear algebra.** Tao's matrix has entries in
///   {1, w, w^2} (w a cube root of unity) and both it and its entrywise square are unitary up to
///   sqrt 6. A Java complex-matrix or quantum-circuit library could keep it as a unit test: it exercises
///   conjugate-transpose, entrywise powers and products, and the expected answers are exact integers.
/// - **Cancellation of roots of unity as a design check.** The vector-level fact (if unit numbers have
///   zero first and second power sums then each cube class sums to zero) is a cheap invariant a signal
///   or DFT routine could assert on its own output when inputs are known to have that structure.
public class HadamardCubeFiber {

    static final double TOL = 1e-8;
    static final int N = 6;

    record C(double re, double im) {
        static C of(double re, double im) { return new C(re, im); }
        static C polar(double theta) { return new C(Math.cos(theta), Math.sin(theta)); }
        static final C ZERO = new C(0, 0), ONE = new C(1, 0);
        C plus(C o) { return new C(re + o.re, im + o.im); }
        C minus(C o) { return new C(re - o.re, im - o.im); }
        C times(C o) { return new C(re * o.re - im * o.im, re * o.im + im * o.re); }
        C conj() { return new C(re, -im); }
        C cube() { return times(this).times(this); }
        double abs() { return Math.hypot(re, im); }
        boolean near(C o) { return minus(o).abs() < TOL; }
        @Override public String toString() { return String.format("%.6f%+.6fi", re, im); }
    }

    // ------------------------------------------------------------ the challenge's definitions
    static double unimodularResidual(C[][] h) {
        double r = 0;
        for (C[] row : h) for (C z : row) r = Math.max(r, Math.abs(z.abs() - 1));
        return r;
    }

    /// max over entries of |H^* H - 6 I| together with the unimodular residual (IsComplexHadamard)
    static double hadamardResidual(C[][] h) {
        double r = unimodularResidual(h);
        for (int p = 0; p < N; p++) for (int q = 0; q < N; q++) {
            C s = C.ZERO;
            for (int k = 0; k < N; k++) s = s.plus(h[k][p].conj().times(h[k][q]));
            r = Math.max(r, s.minus(p == q ? C.of(N, 0) : C.ZERO).abs());
        }
        return r;
    }

    static C[][] entrywiseSquare(C[][] h) {
        C[][] s = new C[N][N];
        for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) s[i][j] = h[i][j].times(h[i][j]);
        return s;
    }

    static C[] rowRatio(C[][] h, int i, int j) {
        C[] v = new C[N];
        for (int k = 0; k < N; k++) v[k] = h[i][k].times(h[j][k].conj());
        return v;
    }

    static List<C> cubeValues(C[] v) {
        List<C> reps = new ArrayList<>();
        for (C x : v) { C c = x.cube(); if (reps.stream().noneMatch(c::near)) reps.add(c); }
        return reps;
    }

    /// sum over k in cubeFiber(v, a) of v_k (the theorem's sum: H i k * star (H j k) = v_k)
    static C fiberSum(C[] v, C a) {
        C s = C.ZERO;
        for (C x : v) if (x.cube().near(a)) s = s.plus(x);
        return s;
    }

    /// Admissible a for the hypotheses hne + hab: both cube values if there are two; if one value c,
    /// a = c (fibre = all) or a = anything else (fibre empty). None if three or more (theorem silent).
    static List<C> admissibleA(C[] v) {
        List<C> cl = cubeValues(v);
        if (cl.size() == 2) return cl;
        if (cl.size() == 1) return List.of(cl.get(0), cl.get(0).plus(C.ONE));
        return List.of();
    }

    record Verdict(double hadamardRes, double squareRes, double maxQ, int twoValuedPairs) {
        boolean hypotheses() { return hadamardRes < TOL && squareRes < TOL; }
    }

    static Verdict verdict(C[][] h) {
        double q = 0; int twoValued = 0;
        for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) {
            if (i == j) continue;
            C[] v = rowRatio(h, i, j);
            if (cubeValues(v).size() == 2) twoValued++;
            for (C a : admissibleA(v)) q = Math.max(q, fiberSum(v, a).abs());
        }
        return new Verdict(hadamardResidual(h), hadamardResidual(entrywiseSquare(h)), q, twoValued);
    }

    // ------------------------------------------------------------ matrices
    static C[][] fourier6() {
        C[][] f = new C[N][N];
        for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) f[i][j] = C.polar(2 * Math.PI * i * j / 6);
        return f;
    }

    /// taoMatrix from lean/OAI/LinearAlgebra/Hadamard/Basic.lean, exponent rule copied exactly
    static C[][] tao() {
        C[][] t = new C[N][N];
        for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) {
            int e;
            if (i == 0 || j == 0 || i == j) e = 0;
            else { int d = Math.floorMod(i - j, 5); e = (d == 1 || d == 4) ? 1 : -1; }
            t[i][j] = C.polar(2 * Math.PI * e / 3);
        }
        return t;
    }

    /// u_i * H[r(i)][c(j)] * v_j : random permutations and unit phases (Hadamard equivalence)
    static C[][] randomEquivalent(C[][] h, Random rnd) {
        int[] r = perm(rnd), c = perm(rnd);
        C[] u = new C[N], w = new C[N];
        for (int k = 0; k < N; k++) { u[k] = C.polar(2 * Math.PI * rnd.nextDouble()); w[k] = C.polar(2 * Math.PI * rnd.nextDouble()); }
        C[][] out = new C[N][N];
        for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) out[i][j] = u[i].times(h[r[i]][c[j]]).times(w[j]);
        return out;
    }

    /// Dita's one-parameter family D6(c) (catalogue form; Hadamard verified below)
    static C[][] dita(double c) {
        C I = C.of(0, 1), mI = C.of(0, -1), m1 = C.of(-1, 0), e = C.polar(c), f = C.polar(-c);
        C[][] d = {
            {C.ONE, C.ONE, C.ONE, C.ONE, C.ONE, C.ONE},
            {C.ONE, m1, I, mI, mI, I},
            {C.ONE, I, m1, I.times(e), mI.times(e), mI},
            {C.ONE, mI, I.times(f), m1, I, mI.times(f)},
            {C.ONE, mI, mI.times(f), I, m1, I.times(f)},
            {C.ONE, I, mI, mI.times(e), I.times(e), m1}};
        return d;
    }

    static int[] perm(Random rnd) {
        int[] p = {0, 1, 2, 3, 4, 5};
        for (int k = N - 1; k > 0; k--) { int m = rnd.nextInt(k + 1); int t = p[k]; p[k] = p[m]; p[m] = t; }
        return p;
    }

    static boolean expect(String what, boolean ok) {
        System.out.printf("  [%s] %s%n", ok ? "OK " : "NO ", what);
        return ok;
    }

    public static void main(String[] args) {
        Random rnd = new Random(20261008);
        boolean all = true;

        System.out.println("== Matrices satisfying ALL hypotheses (Tao's matrix and its equivalence class)");
        Verdict t = verdict(tao());
        System.out.printf("  Tao: Hadamard res %.1e, square res %.1e, max|Q| %.1e, two-valued pairs %d%n",
            t.hadamardRes(), t.squareRes(), t.maxQ(), t.twoValuedPairs());
        all &= expect("Tao satisfies hH and hs, and every fibre sum is 0", t.hypotheses() && t.maxQ() < TOL);
        double worstQ = 0, worstRes = 0; int twoValued = 0;
        for (int n = 0; n < 500; n++) {
            Verdict v = verdict(randomEquivalent(tao(), rnd));
            worstQ = Math.max(worstQ, v.maxQ());
            worstRes = Math.max(worstRes, Math.max(v.hadamardRes(), v.squareRes()));
            twoValued += v.twoValuedPairs();
        }
        System.out.printf("  500 random equivalents: worst residual %.1e, max|Q| %.1e, two-valued pairs %d%n",
            worstRes, worstQ, twoValued);
        all &= expect("random Tao-equivalents: hypotheses hold, fibre sums 0", worstRes < TOL && worstQ < TOL);

        System.out.println("== Hadamard matrices where hs FAILS (theorem says nothing)");
        Verdict f = verdict(fourier6());
        System.out.printf("  F6: Hadamard res %.1e, square res %.1f, max|Q| over hab-pairs %.3f%n",
            f.hadamardRes(), f.squareRes(), f.maxQ());
        all &= expect("F6 is Hadamard but F6 o F6 is not", f.hadamardRes() < TOL && f.squareRes() > 1);
        double minSq = Double.MAX_VALUE, maxH = 0;
        for (int n = 0; n < 200; n++) {
            C[][] d = dita(2 * Math.PI * rnd.nextDouble());
            maxH = Math.max(maxH, hadamardResidual(d));
            minSq = Math.min(minSq, hadamardResidual(entrywiseSquare(d)));
        }
        System.out.printf("  Dita D6(c), 200 random c: max Hadamard res %.1e, MIN square res %.3f%n", maxH, minSq);
        all &= expect("Dita family is Hadamard and never satisfies hs", maxH < TOL && minSq > 1);

        System.out.println("== Vector level (the a != b case the Lean proof needs): v = perm(u(1,w,w^2), x(1,w,w^2))");
        double worstVec = 0; C w = C.polar(2 * Math.PI / 3);
        for (int n = 0; n < 2000; n++) {
            C u = C.polar(2 * Math.PI * rnd.nextDouble()), x = C.polar(2 * Math.PI * rnd.nextDouble());
            C[] base = {u, u.times(w), u.times(w).times(w), x, x.times(w), x.times(w).times(w)};
            int[] p = perm(rnd);
            C[] v = new C[N];
            for (int k = 0; k < N; k++) v[k] = base[p[k]];
            for (C a : admissibleA(v)) worstVec = Math.max(worstVec, fiberSum(v, a).abs());
        }
        System.out.printf("  2000 random (u, x, permutation): max|fibre sum| %.1e%n", worstVec);
        all &= expect("two-triple vectors: each cube fibre sums to 0", worstVec < TOL);

        System.out.println("== Negative controls (the check must be able to say NO)");
        C[] v03 = rowRatio(fourier6(), 0, 3);
        C q03 = fiberSum(v03, C.ONE);
        System.out.printf("  F6 rows (0,3): cube values %s, fibre(a=1) sum = %s%n", cubeValues(v03), q03);
        all &= expect("F6 rows (0,3) fibre sum is 3, not 0 (hs dropped)", q03.minus(C.of(3, 0)).abs() < TOL);
        C[][] ones = new C[N][N];
        for (C[] row : ones) java.util.Arrays.fill(row, C.ONE);
        C q1 = fiberSum(rowRatio(ones, 0, 1), C.ONE);
        System.out.printf("  all-ones (unimodular, Hadamard res %.0f): fibre(a=1) sum = %s%n", hadamardResidual(ones), q1);
        all &= expect("all-ones fibre sum is 6 (hH dropped)", q1.minus(C.of(6, 0)).abs() < TOL);

        System.out.println(all ? "ALL CHECKS AS EXPECTED" : "SOME CHECK FAILED");
        if (!all) System.exit(1);
    }
}
