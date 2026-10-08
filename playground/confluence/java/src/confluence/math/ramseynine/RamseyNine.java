package confluence.math.ramseynine;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/// Java replication of the computable parts of
/// OAI.EuclideanRamsey.NineStatement.nine_circle_configuration
/// (lean/ComparatorChallenges/EuclideanRamseyNine.lean), in exact rational arithmetic.
///
/// The theorem: take nine real numbers t_0..t_8 that are algebraically independent over Q and put
/// point i at ((1 - t_i^2)/(1 + t_i^2), 2 t_i/(1 + t_i^2)). Then the nine points are distinct, all
/// lie on the unit circle, and the configuration is NOT Euclidean-Ramsey: for some number of
/// colours r, every dimension D has an r-colouring of R^D with no monochromatic congruent copy.
///
/// Nobody can write down nine provably independent reals, so the configuration itself is not
/// computable. What IS computable is the linear-algebra certificate the Lean proof rests on:
/// a 9x9 matrix whose row i is the tensor (1, x(T_i), y(T_i)) (x) (1, x(U_i), y(U_i)), where T and
/// U are the two independent copies of the parameters that the tensor square Q(t) (x) Q(t) provides.
/// The proof shows its determinant is a nonzero rational function, by evaluating the
/// denominator-cleared version at the grid T_(a,b) = g[a], U_(a,b) = g[b], g = (0, 1, -1), where it
/// becomes the Kronecker square of a 3x3 matrix of determinant 8, so 8^6. A nonzero determinant
/// kills every candidate "field criterion" witness, and the deep (Lean-only) step says a Ramsey
/// configuration spanning the plane must have one.
///
/// This class rebuilds that certificate from the definitions, checks circle membership and
/// injectivity, and runs controls that MUST come out singular: U = T (no tensor independence, the
/// circle equation itself is then a kernel vector), a repeated parameter, a degenerate grid, and
/// eight points instead of nine.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.ramseynine.RamseyNine
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Polynomial identity testing by one good evaluation.** The proof never expands a 9x9
///   determinant of rational functions; it evaluates at one point and gets 8^6 != 0. Java code that
///   must decide "is this symbolic expression identically zero?" (a rules engine simplifying
///   formulas, a CAS-lite in a spreadsheet engine) can use the same move: one nonzero exact
///   evaluation proves nonzero; a zero proves nothing, which is why a randomized
///   Schwartz-Zippel test uses several random points.
/// - **Rational parametrizations give exact geometry without square roots.** The map
///   t -> ((1-t^2)/(1+t^2), 2t/(1+t^2)) puts rational t on the unit circle exactly. A Java geometry
///   or CAD library that needs exact on-circle points (tests for intersection code, robust
///   predicates) can generate them from BigInteger fractions with no floating-point drift.
/// - **Exact determinant as a rank oracle in tests.** `det` and `rank` here are fraction-based
///   Gaussian elimination; the controls show the same code reporting 0 when it must. That is a
///   reusable pattern for checking linear-algebra code (a float solver) against an exact reference
///   on small matrices.
/// - **A caution about genericity.** The positive result needs the left and right parameters to be
///   independent; with U = T the same matrix is singular (rank 5). Code that tests a "generic"
///   property on special inputs (all-rational, repeated, symmetric) can see failures that the
///   generic case does not have, and vice versa.
public class RamseyNine {

    /// Exact rational, always normalized with positive denominator.
    record Q(BigInteger n, BigInteger d) {
        Q {
            if (d.signum() == 0) throw new ArithmeticException("zero denominator");
            if (d.signum() < 0) { n = n.negate(); d = d.negate(); }
            BigInteger g = n.gcd(d);
            if (!g.equals(BigInteger.ONE) && g.signum() != 0) { n = n.divide(g); d = d.divide(g); }
            if (n.signum() == 0) d = BigInteger.ONE;
        }
        static Q of(long a) { return new Q(BigInteger.valueOf(a), BigInteger.ONE); }
        static Q of(long a, long b) { return new Q(BigInteger.valueOf(a), BigInteger.valueOf(b)); }
        Q add(Q o) { return new Q(n.multiply(o.d).add(o.n.multiply(d)), d.multiply(o.d)); }
        Q sub(Q o) { return add(o.neg()); }
        Q neg() { return new Q(n.negate(), d); }
        Q mul(Q o) { return new Q(n.multiply(o.n), d.multiply(o.d)); }
        Q div(Q o) { return new Q(n.multiply(o.d), d.multiply(o.n)); }
        boolean isZero() { return n.signum() == 0; }
        @Override public String toString() { return d.equals(BigInteger.ONE) ? n.toString() : n + "/" + d; }
    }

    static final Q ONE = Q.of(1), TWO = Q.of(2);
    static final List<String> FAILED = new ArrayList<>();

    static void check(String name, boolean ok, String detail) {
        System.out.println("[" + (ok ? "PASS" : "FAIL") + "] " + name + (detail.isEmpty() ? "" : "  -- " + detail));
        if (!ok) FAILED.add(name);
    }

    /// literalCircleConfig: point(t) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2)).
    static Q[] point(Q t) {
        Q den = ONE.add(t.mul(t));
        return new Q[] {ONE.sub(t.mul(t)).div(den), TWO.mul(t).div(den)};
    }

    /// NineRational.r: augmented vector (1, x, y).
    static Q[] r(Q z) { Q[] p = point(z); return new Q[] {ONE, p[0], p[1]}; }

    /// NineGrid.q: denominator-cleared (1 + z^2, 1 - z^2, 2z).
    static Q[] q(Q z) { Q z2 = z.mul(z); return new Q[] {ONE.add(z2), ONE.sub(z2), TWO.mul(z)}; }

    /// Column (a, b), a, b in {0 = constant, 1 = x, 2 = y}, at index 3a + b.
    static Q[][] tensorRows(Q[] T, Q[] U, boolean cleared) {
        Q[][] m = new Q[T.length][9];
        for (int i = 0; i < T.length; i++) {
            Q[] l = cleared ? q(T[i]) : r(T[i]);
            Q[] rr = cleared ? q(U[i]) : r(U[i]);
            for (int a = 0; a < 3; a++) for (int b = 0; b < 3; b++) m[i][3 * a + b] = l[a].mul(rr[b]);
        }
        return m;
    }

    static Q[][] copy(Q[][] m) {
        Q[][] c = new Q[m.length][];
        for (int i = 0; i < m.length; i++) c[i] = m[i].clone();
        return c;
    }

    static Q det(Q[][] in) {
        Q[][] m = copy(in);
        int n = m.length;
        Q d = ONE;
        for (int c = 0; c < n; c++) {
            int p = -1;
            for (int r = c; r < n; r++) if (!m[r][c].isZero()) { p = r; break; }
            if (p < 0) return Q.of(0);
            if (p != c) { Q[] t = m[c]; m[c] = m[p]; m[p] = t; d = d.neg(); }
            d = d.mul(m[c][c]);
            for (int r = c + 1; r < n; r++) {
                Q f = m[r][c].div(m[c][c]);
                if (f.isZero()) continue;
                for (int k = 0; k < n; k++) m[r][k] = m[r][k].sub(f.mul(m[c][k]));
            }
        }
        return d;
    }

    static int rank(Q[][] in) {
        Q[][] m = copy(in);
        int rows = m.length, cols = m[0].length, rk = 0;
        for (int c = 0; c < cols && rk < rows; c++) {
            int p = -1;
            for (int r = rk; r < rows; r++) if (!m[r][c].isZero()) { p = r; break; }
            if (p < 0) continue;
            Q[] t = m[rk]; m[rk] = m[p]; m[p] = t;
            for (int r = 0; r < rows; r++) {
                if (r == rk || m[r][c].isZero()) continue;
                Q f = m[r][c].div(m[rk][c]);
                for (int k = 0; k < cols; k++) m[r][k] = m[r][k].sub(f.mul(m[rk][k]));
            }
            rk++;
        }
        return rk;
    }

    static Q rnd(Random g) { return Q.of(g.nextInt(101) - 50, g.nextInt(50) + 1); }

    static Q[] rnds(Random g, int n) { Q[] a = new Q[n]; for (int i = 0; i < n; i++) a[i] = rnd(g); return a; }

    public static void main(String[] args) {
        Random g = new Random(20261008L);

        System.out.println("== 1-2. circle membership and injectivity ==");
        boolean onCircle = true, recovered = true;
        for (int k = 0; k < 200; k++) {
            Q t = rnd(g);
            Q[] p = point(t);
            onCircle &= p[0].mul(p[0]).add(p[1].mul(p[1])).equals(ONE);
            recovered &= p[1].div(ONE.add(p[0])).equals(t);   // 1 + x = 2/(1+t^2) > 0
        }
        check("x^2 + y^2 = 1 exactly at 200 random rationals", onCircle, "");
        check("t = y/(1 + x) recovered exactly at 200 random rationals (injectivity)", recovered, "");

        System.out.println("== 3. affine span ==");
        Q[] a = point(Q.of(0)), b = point(ONE), c = point(Q.of(-1));
        Q area2 = b[0].sub(a[0]).mul(c[1].sub(a[1])).sub(b[1].sub(a[1]).mul(c[0].sub(a[0])));
        check("points at t = 0, 1, -1 are not collinear", !area2.isZero(), "2*area = " + area2);

        System.out.println("== 4. grid certificate ==");
        Q[] grid = {Q.of(0), ONE, Q.of(-1)};
        Q[][] C = new Q[3][];
        for (int i = 0; i < 3; i++) C[i] = q(grid[i]);
        check("det C = 8", det(C).equals(Q.of(8)), "det C = " + det(C));
        Q[] Tg = new Q[9], Ug = new Q[9];
        for (int i = 0; i < 9; i++) { Tg[i] = grid[i / 3]; Ug[i] = grid[i % 3]; }
        Q[][] Eg = tensorRows(Tg, Ug, true);
        boolean kron = true;
        for (int i = 0; i < 9; i++) for (int j = 0; j < 9; j++)
            kron &= Eg[i][j].equals(C[i / 3][j / 3].mul(C[i % 3][j % 3]));
        check("E(grid) equals C (x) C entrywise", kron, "");
        Q dE = det(Eg);
        check("det E(grid) = 8^6 = 262144", dE.equals(Q.of(262144)), "det = " + dE);

        System.out.println("== 5. rational matrix at independent random T, U ==");
        int nonzero = 0;
        boolean cleared = true;
        for (int trial = 0; trial < 20; trial++) {
            Q[] T = rnds(g, 9), U = rnds(g, 9);
            Q dM = det(tensorRows(T, U, false));
            Q den = ONE;
            for (int i = 0; i < 9; i++) den = den.mul(ONE.add(T[i].mul(T[i]))).mul(ONE.add(U[i].mul(U[i])));
            cleared &= det(tensorRows(T, U, true)).equals(den.mul(dM));
            if (!dM.isZero()) nonzero++;
        }
        check("det M != 0 at 20/20 random independent points", nonzero == 20, nonzero + "/20");
        check("det E = prod (1+T_i^2)(1+U_i^2) * det M (cleared_matrix)", cleared, "");

        System.out.println("== CONTROLS (each MUST come out singular) ==");
        Q[] T = rnds(g, 9);
        Q[][] M1 = tensorRows(T, T, false);
        Q d1 = det(M1);
        check("CONTROL C1: U = T gives det 0", d1.isZero(), "det = " + d1 + ", rank = " + rank(M1));
        Q[] circle = new Q[9];
        for (int k = 0; k < 9; k++) circle[k] = Q.of(0);
        circle[0] = Q.of(-1); circle[4] = ONE; circle[8] = ONE;   // -1*1 + x*x + y*y
        boolean kernel = true;
        for (Q[] row : M1) {
            Q s = Q.of(0);
            for (int k = 0; k < 9; k++) s = s.add(row[k].mul(circle[k]));
            kernel &= s.isZero();
        }
        check("CONTROL C1: circle equation is a kernel vector when U = T", kernel, "");
        Q[][] Mi = tensorRows(rnds(g, 9), rnds(g, 9), false);
        Q s0 = Q.of(0);
        for (int k = 0; k < 9; k++) s0 = s0.add(Mi[0][k].mul(circle[k]));
        check("CONTROL C1b: circle vector is NOT in the kernel once T, U independent", !s0.isZero(), "row-0 residual = " + s0);
        Q[] T2 = rnds(g, 9), U2 = rnds(g, 9);
        T2[1] = T2[0]; U2[1] = U2[0];
        Q d2 = det(tensorRows(T2, U2, false));
        check("CONTROL C2: repeated parameter gives det 0", d2.isZero(), "det = " + d2);
        Q[] bad = {Q.of(0), ONE, ONE};
        Q[][] C3 = new Q[3][];
        for (int i = 0; i < 3; i++) C3[i] = q(bad[i]);
        Q[] T3 = new Q[9], U3 = new Q[9];
        for (int i = 0; i < 9; i++) { T3[i] = bad[i / 3]; U3[i] = bad[i % 3]; }
        Q dC3 = det(C3), dE3 = det(tensorRows(T3, U3, true));
        check("CONTROL C3: grid (0,1,1) gives det C = 0 and det E = 0", dC3.isZero() && dE3.isZero(),
              "det C = " + dC3 + ", det E = " + dE3);
        int rk8 = rank(tensorRows(rnds(g, 8), rnds(g, 8), false));
        check("CONTROL C4: 8 points give an 8x9 system of rank 8 (kernel nonzero)", rk8 == 8, "rank = " + rk8);

        System.out.println();
        if (!FAILED.isEmpty()) {
            System.out.println("FAILED: " + FAILED);
            System.exit(1);
        }
        System.out.println("ALL CHECKS PASS (positive checks hold, every control came out singular as required)");
    }
}
