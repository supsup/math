package confluence.math.grahamspherical;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/// Java replication of the computable core of OAI.GrahamSpherical.full_main
/// (lean/ComparatorChallenges/GrahamSpherical.lean): an explicit twelve-point subset of the unit
/// circle that is NOT Euclidean Ramsey, i.e. a counterexample to Graham's conjecture that every
/// finite spherical set is Ramsey.
///
/// The set is three squares inscribed in the unit circle: the coordinate square Q0 = {(+-1,0),
/// (0,+-1)}, and Q0 rotated by +theta and by -theta, where tan(theta/2) = t = sum_{k>=1} 10^(-k!)
/// (Liouville's constant, transcendental). Weights: +1 on the two rotated squares, -2 on Q0.
///
/// The Lean proof picks a derivation D of the reals (additive, Leibniz rule, wildly
/// discontinuous; exists by choice because t is transcendental) with D t = (1 + t^2)/2, so
/// D u = -v and D v = u for (u, v) = (cos theta, sin theta). It colours y in R^n by
/// floor(3 E(y)) mod 50, E(y) = sum_j D(y_j)^2. For EVERY isometric copy y_i of the twelve points
/// the weighted energy sum_i w_i E(y_i) is exactly 8, and that is incompatible with all twelve
/// colours agreeing.
///
/// A derivation of R cannot be computed, but its restriction to a finitely generated field can:
/// dual numbers a + b*eps (eps^2 = 0) evaluate any rational expression together with its image
/// under D, given D of the inputs. This program uses exact BigInteger rationals throughout and
/// checks, each with a control that must fail:
///
/// 1. the twelve points (t replaced by the rational partial sum t_3 = 0.110001, which keeps every
///    circle fact exact because u, v are rational in t) are distinct and on the unit circle, and
///    all 495 concyclicity determinants vanish; control: push one point off the circle;
/// 2. D u = -v, D v = u; control: D t = 1;
/// 3. the weighted energy of random exact isometric copies in R^2..R^8 is exactly 8; controls:
///    wrong D t, a non-isometric copy, and a set with both squares rotated the same way;
/// 4. the floor(3E) mod m step excludes a monochromatic copy for m = 50 (in fact exactly for
///    m = 16 or m >= 32); control: for m = 15, 17, 31 explicit energies with weighted sum 8 and a
///    single colour exist, so the step really depends on the modulus.
///
/// It does NOT check that the derivation exists on R, the transcendence of t, or that the
/// argument covers every colouring; those are the Lean proof's job.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.grahamspherical.GrahamSpherical
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Dual numbers are a cheap, exact derivative engine.** The `Dual` record below is forward-mode
///   automatic differentiation over exact rationals. A Java code base that needs exact sensitivities
///   of rational formulas (pricing formulas, geometry kernels, unit tests for a numeric AD library)
///   can use the same thirty lines as an oracle: no floating-point tolerance, so a mismatch is a
///   real bug.
/// - **Rational orthogonal matrices for exact geometry tests.** `cayleyPair` builds exactly
///   orthonormal vectors in Q^n from a skew matrix. Tests of collision, rendering or GIS code that
///   want "a random rotation, but checkable with ==" can generate them this way instead of
///   comparing doubles with an epsilon.
/// - **An invariant can defeat a colouring/hashing scheme.** The obstruction is a weighted sum of
///   per-point values that is the same for every placement of the pattern, combined with a
///   bucketing (floor mod m) whose bucket sums cannot hit that invariant. The same shape of argument
///   is how one would prove that a bucketing scheme in a spatial index or a sharding function never
///   puts all members of some rigid pattern in one bucket. The modulus table (16 and >= 32 work,
///   17..31 do not) is a reminder that such guarantees can hinge on the exact constant.
/// - **"Cannot be computed" is not "cannot be tested".** The colouring in the theorem is
///   non-constructive, yet every identity it depends on is checkable on a finitely generated
///   piece. Java tests for code built on non-constructive specs can often test the identities on
///   such a piece instead of the object itself.
public class GrahamSpherical {

    // ------------------------------------------------------------------ exact rationals
    record Q(BigInteger n, BigInteger d) {
        Q {
            if (d.signum() == 0) throw new ArithmeticException("x/0 (Lean would silently give 0)");
            if (d.signum() < 0) { n = n.negate(); d = d.negate(); }
            BigInteger g = n.gcd(d);
            if (!g.equals(BigInteger.ONE) && g.signum() != 0) { n = n.divide(g); d = d.divide(g); }
        }
        static Q of(long a) { return new Q(BigInteger.valueOf(a), BigInteger.ONE); }
        static Q of(long a, long b) { return new Q(BigInteger.valueOf(a), BigInteger.valueOf(b)); }
        static final Q ZERO = of(0), ONE = of(1);
        Q add(Q o) { return new Q(n.multiply(o.d).add(o.n.multiply(d)), d.multiply(o.d)); }
        Q sub(Q o) { return add(o.neg()); }
        Q neg() { return new Q(n.negate(), d); }
        Q mul(Q o) { return new Q(n.multiply(o.n), d.multiply(o.d)); }
        Q div(Q o) { return new Q(n.multiply(o.d), d.multiply(o.n)); }
        boolean isZero() { return n.signum() == 0; }
        BigInteger floor() { BigInteger[] qr = n.divideAndRemainder(d); return qr[1].signum() < 0 ? qr[0].subtract(BigInteger.ONE) : qr[0]; }
        double dbl() { return n.doubleValue() / d.doubleValue(); }
        @Override public String toString() { return d.equals(BigInteger.ONE) ? n.toString() : n + "/" + d; }
    }

    // ------------------------------------------------------------------ dual numbers = a derivation
    record Dual(Q a, Q b) {
        static Dual c(Q x) { return new Dual(x, Q.ZERO); }
        Dual add(Dual o) { return new Dual(a.add(o.a), b.add(o.b)); }
        Dual sub(Dual o) { return new Dual(a.sub(o.a), b.sub(o.b)); }
        Dual mul(Dual o) { return new Dual(a.mul(o.a), a.mul(o.b).add(b.mul(o.a))); }
        Dual scale(Q s) { return new Dual(a.mul(s), b.mul(s)); }
        Dual div(Dual o) { return new Dual(a.div(o.a), b.mul(o.a).sub(a.mul(o.b)).div(o.a.mul(o.a))); }
    }

    static final int[][] SQUARE = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};   // squareCoordinate 0..3
    static final int[][] LABELS = new int[12][];
    static { int k = 0; for (int a = 0; a < 3; a++) for (int q = 0; q < 4; q++) LABELS[k++] = new int[]{a, q}; }
    static int weight(int[] lab) { return lab[0] == 2 ? -2 : 1; }

    /// u = (1-t^2)/(1+t^2), v = 2t/(1+t^2), carried with their D-images.
    static Dual[] uv(Dual t) {
        Dual one = Dual.c(Q.ONE), t2 = t.mul(t), den = one.add(t2);
        return new Dual[]{one.sub(t2).div(den), t.scale(Q.of(2)).div(den)};
    }

    /// Lean `coordinates (a, q)`: a = 0 rotates by +theta, a = 1 by -theta (or +theta when
    /// sameSense, for the control), a = 2 is the coordinate square.
    static Dual[] coord(Dual[] uv, int a, int q, boolean sameSense) {
        Q x = Q.of(SQUARE[q][0]), y = Q.of(SQUARE[q][1]);
        if (a == 2) return new Dual[]{Dual.c(x), Dual.c(y)};
        Dual u = uv[0], v = uv[1];
        Q s = (a == 0 || sameSense) ? Q.ONE : Q.of(-1);
        return new Dual[]{u.scale(x).sub(v.scale(s.mul(y))), v.scale(s.mul(x)).add(u.scale(y))};
    }

    static Q liouvillePartial(int k) {
        Q s = Q.ZERO; long f = 1;
        for (int i = 1; i <= k; i++) { f *= i; s = s.add(new Q(BigInteger.ONE, BigInteger.TEN.pow((int) f))); }
        return s;
    }

    static final Q T3 = liouvillePartial(3);
    static final Random RNG = new Random(20261008L);
    static Q rq() { return Q.of(RNG.nextInt(71) - 35, RNG.nextInt(7) + 1); }

    static int failures = 0;
    static void check(String name, boolean ok, String detail) {
        System.out.println((ok ? "PASS " : "FAIL ") + name + (detail.isEmpty() ? "" : "  [" + detail + "]"));
        if (!ok) failures++;
    }
    static void control(String name, boolean failedAsExpected, String detail) {
        System.out.println((failedAsExpected ? "CONTROL-OK " : "CONTROL-BROKEN ") + name + (detail.isEmpty() ? "" : "  [" + detail + "]"));
        if (!failedAsExpected) failures++;
    }

    static Q det(Q[][] m) {
        int n = m.length;
        if (n == 1) return m[0][0];
        Q s = Q.ZERO;
        for (int j = 0; j < n; j++) {
            Q[][] minor = new Q[n - 1][n - 1];
            for (int r = 1; r < n; r++) for (int c = 0, cc = 0; c < n; c++) if (c != j) minor[r - 1][cc++] = m[r][c];
            Q term = m[0][j].mul(det(minor));
            s = (j % 2 == 0) ? s.add(term) : s.sub(term);
        }
        return s;
    }

    static int nonzeroConcyclic(Q[][] pts) {
        int nz = 0;
        for (int i = 0; i < 12; i++) for (int j = i + 1; j < 12; j++) for (int k = j + 1; k < 12; k++) for (int l = k + 1; l < 12; l++) {
            Q[][] m = new Q[4][];
            int[] idx = {i, j, k, l};
            for (int r = 0; r < 4; r++) { Q x = pts[idx[r]][0], y = pts[idx[r]][1]; m[r] = new Q[]{x.mul(x).add(y.mul(y)), x, y, Q.ONE}; }
            if (!det(m).isZero()) nz++;
        }
        return nz;
    }

    /// Exact rational orthonormal pair: first two columns of (I - S)^{-1}(I + S), S skew.
    static Q[][] cayleyPair(int n) {
        Q[][] s = new Q[n][n];
        for (int i = 0; i < n; i++) { s[i][i] = Q.ZERO; for (int j = i + 1; j < n; j++) { s[i][j] = Q.of(RNG.nextInt(13) - 6, RNG.nextInt(3) + 1); s[j][i] = s[i][j].neg(); } }
        Q[][] aug = new Q[n][2 * n];
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) {
            Q id = i == j ? Q.ONE : Q.ZERO;
            aug[i][j] = id.sub(s[i][j]); aug[i][n + j] = id.add(s[i][j]);
        }
        for (int col = 0; col < n; col++) {
            int piv = col; while (aug[piv][col].isZero()) piv++;
            Q[] tmp = aug[col]; aug[col] = aug[piv]; aug[piv] = tmp;
            Q pv = aug[col][col];
            for (int c = 0; c < 2 * n; c++) aug[col][c] = aug[col][c].div(pv);
            for (int r = 0; r < n; r++) if (r != col && !aug[r][col].isZero()) {
                Q f = aug[r][col];
                for (int c = 0; c < 2 * n; c++) aug[r][c] = aug[r][c].sub(f.mul(aug[col][c]));
            }
        }
        Q[] a = new Q[n], b = new Q[n];
        for (int i = 0; i < n; i++) { a[i] = aug[i][n]; b[i] = aug[i][n + 1]; }
        return new Q[][]{a, b};
    }

    /// Weighted energy sum_i w_i sum_j D(y_ij)^2 of a random copy y_i = z + x_i A + y_i B in R^n.
    /// D(A_j), D(B_j), D(z_j) are arbitrary: the Lean proof does not need mixed orthogonality.
    /// Also returns whether the real parts are an exact isometric image of the twelve points.
    static Object[] copyEnergy(int n, Q dt, Q scaleA, boolean sameSense) {
        Dual[] uvT = uv(new Dual(T3, dt));
        Q[][] ab = cayleyPair(n);
        Dual[] A = new Dual[n], B = new Dual[n], z = new Dual[n];
        for (int j = 0; j < n; j++) { A[j] = new Dual(ab[0][j].mul(scaleA), rq()); B[j] = new Dual(ab[1][j], rq()); z[j] = new Dual(rq(), rq()); }
        Q total = Q.ZERO;
        List<Q[]> real = new ArrayList<>();
        for (int[] lab : LABELS) {
            Dual[] c = coord(uvT, lab[0], lab[1], sameSense);
            Q e = Q.ZERO; Q[] y = new Q[n];
            for (int j = 0; j < n; j++) {
                Dual yj = z[j].add(c[0].mul(A[j])).add(c[1].mul(B[j]));
                e = e.add(yj.b().mul(yj.b())); y[j] = yj.a();
            }
            total = total.add(e.mul(Q.of(weight(lab))));
            real.add(y);
        }
        Dual[] uvR = uv(Dual.c(T3));
        boolean iso = true;
        for (int i = 0; i < 12; i++) for (int k = i + 1; k < 12; k++) {
            Q dy = Q.ZERO;
            for (int j = 0; j < n; j++) { Q d = real.get(i)[j].sub(real.get(k)[j]); dy = dy.add(d.mul(d)); }
            Dual[] p = coord(uvR, LABELS[i][0], LABELS[i][1], false), q = coord(uvR, LABELS[k][0], LABELS[k][1], false);
            Q dx = p[0].a().sub(q[0].a()), dyy = p[1].a().sub(q[1].a());
            iso &= dy.equals(dx.mul(dx).add(dyy.mul(dyy)));
        }
        return new Object[]{total, iso};
    }

    static boolean moduloWorks(int m) { for (int s = 17; s <= 31; s++) if (s % m == 0) return false; return true; }

    public static void main(String[] args) {
        Q dtTrue = Q.ONE.add(T3.mul(T3)).div(Q.of(2));

        // 1. the twelve points
        check("t_3 = 0.110001 and 11/100 < t_3 < t_3 + 2e-24 < 12/100",
            T3.equals(Q.of(110001, 1000000)) && T3.sub(Q.of(11, 100)).n().signum() > 0
                && Q.of(12, 100).sub(T3.add(new Q(BigInteger.TWO, BigInteger.TEN.pow(24)))).n().signum() > 0, "");
        Dual[] uvR = uv(Dual.c(T3));
        Q[][] pts = new Q[12][];
        boolean onCircle = true;
        java.util.Set<String> distinct = new java.util.HashSet<>();
        for (int i = 0; i < 12; i++) {
            Dual[] c = coord(uvR, LABELS[i][0], LABELS[i][1], false);
            pts[i] = new Q[]{c[0].a(), c[1].a()};
            onCircle &= pts[i][0].mul(pts[i][0]).add(pts[i][1].mul(pts[i][1])).equals(Q.ONE);
            distinct.add(pts[i][0] + "," + pts[i][1]);
        }
        check("12 distinct points, all with x^2 + y^2 = 1 exactly", onCircle && distinct.size() == 12, distinct.size() + " distinct");
        check("all 495 concyclicity determinants vanish", nonzeroConcyclic(pts) == 0, "");
        Q[][] bad = pts.clone();
        bad[0] = new Q[]{pts[0][0].mul(Q.of(11, 10)), pts[0][1].mul(Q.of(11, 10))};
        int nz = nonzeroConcyclic(bad);
        control("one point scaled by 11/10: not concyclic", nz > 0, nz + " nonzero of 495");

        // 2. derivation values
        Dual[] d = uv(new Dual(T3, dtTrue));
        check("D t = (1+t^2)/2 gives D u = -v, D v = u", d[0].b().equals(d[1].a().neg()) && d[1].b().equals(d[0].a()), "");
        Dual[] d1 = uv(new Dual(T3, Q.ONE));
        control("D t = 1: D u != -v", !d1[0].b().equals(d1[1].a().neg()), String.format("D u = %.4f", d1[0].b().dbl()));

        // 3. copy invariant
        boolean all8 = true, allIso = true;
        for (int n : new int[]{2, 3, 5, 8}) for (int r = 0; r < 5; r++) {
            Object[] res = copyEnergy(n, dtTrue, Q.ONE, false);
            all8 &= res[0].equals(Q.of(8)); allIso &= (Boolean) res[1];
        }
        check("weighted energy of 20 random isometric copies (n = 2,3,5,8) is exactly 8", all8, "");
        check("those copies preserve all 66 squared distances exactly", allIso, "");
        Q e1 = (Q) copyEnergy(4, Q.ONE, Q.ONE, false)[0];
        control("D t = 1: weighted energy != 8", !e1.equals(Q.of(8)), String.format("%.4f", e1.dbl()));
        Q e2 = (Q) copyEnergy(4, dtTrue, Q.of(2), false)[0];
        control("non-isometric copy (A scaled by 2): weighted energy != 8", !e2.equals(Q.of(8)), String.format("%.4f", e2.dbl()));
        Q e3 = (Q) copyEnergy(4, dtTrue, Q.ONE, true)[0];
        control("both squares rotated +theta: energy not invariant", !e3.equals(Q.of(8)), String.format("%.4f", e3.dbl()));

        // 4. rounding step
        StringBuilder good = new StringBuilder();
        for (int m = 1; m <= 60; m++) if (moduloWorks(m)) good.append(m).append(' ');
        check("floor(3E) mod 50 excludes a monochromatic copy (no multiple of 50 in (16,32))", moduloWorks(50), "working m <= 60: " + good.toString().trim());
        for (int m : new int[]{15, 17, 31}) {
            int s = 17; while (s % m != 0) s++;
            // one +1-weight point at floor s, the rest at floor 0; then top up to sum w * 3e = 24
            Q[] threeE = new Q[12];
            for (int i = 0; i < 12; i++) threeE[i] = Q.ZERO;
            threeE[0] = Q.of(s);
            Q need = Q.of(24 - s);
            for (int i = 0; i < 12 && !need.isZero(); i++) {
                int w = weight(LABELS[i]);
                if (need.n().signum() > 0 && w == 1) { Q st = need.sub(Q.of(99, 100)).n().signum() > 0 ? Q.of(99, 100) : need; threeE[i] = threeE[i].add(st); need = need.sub(st); }
                if (need.n().signum() < 0 && w == -2) { Q half = need.neg().div(Q.of(2)); Q st = half.sub(Q.of(99, 100)).n().signum() > 0 ? Q.of(99, 100) : half; threeE[i] = threeE[i].add(st); need = need.add(st.mul(Q.of(2))); }
            }
            Q sum = Q.ZERO; java.util.Set<BigInteger> colours = new java.util.HashSet<>();
            for (int i = 0; i < 12; i++) {
                sum = sum.add(threeE[i].div(Q.of(3)).mul(Q.of(weight(LABELS[i]))));
                colours.add(threeE[i].floor().mod(BigInteger.valueOf(m)));
            }
            control("m = " + m + ": energies with weighted sum 8 and ONE colour exist", sum.equals(Q.of(8)) && colours.size() == 1, "sum = " + sum + ", colours " + colours);
        }

        System.out.println();
        System.out.println(failures == 0 ? "all checks passed, all controls failed as required" : failures + " FAILURE(S)");
        if (failures != 0) System.exit(1);
    }
}
