package confluence.math.triangularcovering;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

/// Java replication of OAI.TriangularCovering.main
/// (lean/ComparatorChallenges/TriangularCovering.lean), definition for definition.
///
/// K is the closed regular tetrahedron of edge 2 with vertices (+-1,0,0) and (0,+-1,sqrt 2),
/// written `point x y t = (x, y, H t)` with H = sqrt 2. The theorem has three parts:
///
/// 1. `A_min = H`: the smallest orthogonal shadow of K has area sqrt 2 (looking along an edge).
/// 2. `MainAsymptotic`: for every eps in (0, 1/2000) an explicit family of 2*ceil(2/eps^2)
///    infinite triangular cylinders covers K, with total base area / H =
///    1/2 - (13/6000) eps^2 + O(eps^4), hence strictly below A_min / 2.
/// 3. `NormalizedCounterexample`: some finite cylinder cover has sum of base area / shadow area
///    along its own axis below 1/2.
///
/// Everything is done in (x, y, t) coordinates, where the inner product is
/// x x' + y y' + 2 t t'. Then squared lengths, squared areas and cylinder membership are all
/// rational, so this class checks them with exact BigInteger fractions ([Q]). Doubles are used
/// only for the area sum (8 million terms, with expm1/log1p and compensated summation), for
/// the sphere search, and to choose candidates before an exact check.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.triangularcovering.TriangularCovering
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Covering problems hide a 1/1000 margin.** At eps = 1/2001 the cover only works because of
///   a slack of about eps^2/500, roughly 5e-10. The same cylinders with that slack removed leave a
///   point of K uncovered, and this class finds it. A Java collision, visibility or coverage
///   check (beam or sensor sweeps, for example) that decides "covered" in `double` can be wrong
///   by more than that. The right tool there is exact rationals (as here) or interval
///   arithmetic, not an epsilon picked by feel.
/// - **Membership in a prism with a slanted axis is a 3x3 Cramer solve.** "Is P in triangle +
///   R*axis" reduces to two barycentric coordinates. The code below does it exactly in about ten
///   lines and can be reused in any geometry kernel that tests points against extruded triangles.
/// - **Do a big sum as a correction.** The area is 1/2 plus a correction of about 1e-9. Summing
///   the correction directly (with `Math.expm1`/`Math.log1p` and Neumaier summation) gives about
///   20 correct digits of it from 8 million `double` terms. Summing the raw areas would lose
///   most of them. This applies to any Java numeric code that sums values close to a known total.
/// - **A ready-made regression fixture.** `CONTROL D` gives an explicit rational point that a
///   cover with cutoff 1/2 misses and the real cover hits. A geometry library could keep it as a
///   unit test that fails if a refactor loosens exact predicates into tolerant ones.
public class TriangularCovering {

    // ------------------------------------------------------------------ exact rationals
    record Q(BigInteger n, BigInteger d) implements Comparable<Q> {
        static Q of(long a) { return new Q(BigInteger.valueOf(a), BigInteger.ONE); }
        static Q of(long a, long b) { return make(BigInteger.valueOf(a), BigInteger.valueOf(b)); }
        static Q of(double v) { // exact value of the double
            BigDecimal b = new BigDecimal(v);
            return b.scale() > 0 ? make(b.unscaledValue(), BigInteger.TEN.pow(b.scale()))
                                 : new Q(b.toBigIntegerExact(), BigInteger.ONE);
        }
        static Q make(BigInteger n, BigInteger d) {
            if (d.signum() < 0) { n = n.negate(); d = d.negate(); }
            BigInteger g = n.gcd(d);
            return g.equals(BigInteger.ONE) || g.signum() == 0 ? new Q(n, d) : new Q(n.divide(g), d.divide(g));
        }
        Q add(Q o) { return make(n.multiply(o.d).add(o.n.multiply(d)), d.multiply(o.d)); }
        Q sub(Q o) { return make(n.multiply(o.d).subtract(o.n.multiply(d)), d.multiply(o.d)); }
        Q mul(Q o) { return make(n.multiply(o.n), d.multiply(o.d)); }
        Q div(Q o) { return make(n.multiply(o.d), d.multiply(o.n)); }
        Q neg() { return new Q(n.negate(), d); }
        int signum() { return n.signum(); }
        public int compareTo(Q o) { return n.multiply(o.d).compareTo(o.n.multiply(d)); }
        Q max(Q o) { return compareTo(o) >= 0 ? this : o; }
        double dbl() { return new BigDecimal(n).divide(new BigDecimal(d), java.math.MathContext.DECIMAL64).doubleValue(); }
        @Override public String toString() { return d.equals(BigInteger.ONE) ? n.toString() : n + "/" + d; }
    }
    static final Q ZERO = Q.of(0), ONE = Q.of(1), HALF = Q.of(1, 2);

    record V(Q x, Q y, Q t) {
        V sub(V o) { return new V(x.sub(o.x), y.sub(o.y), t.sub(o.t)); }
    }
    /// Euclidean inner product of the physical vectors (x, y, H t), (x', y', H t').
    static Q ip(V u, V v) { return u.x.mul(v.x).add(u.y.mul(v.y)).add(Q.of(2).mul(u.t.mul(v.t))); }
    static Q det3(V a, V b, V c) {
        return a.x.mul(b.y.mul(c.t).sub(b.t.mul(c.y)))
            .sub(b.x.mul(a.y.mul(c.t).sub(a.t.mul(c.y))))
            .add(c.x.mul(a.y.mul(b.t).sub(a.t.mul(b.y))));
    }

    // ------------------------------------------------------------------ the Lean definitions
    static final Q ETA = Q.of(1, 1000);
    static Q alpha(Q a, Q b) { return ONE.add(a.mul(b)).div(Q.of(4)); }
    static Q beta(Q a, Q b) { return a.add(b).div(Q.of(4)); }
    static Q dq(Q q) { Q q2 = q.mul(q); return q2.mul(ONE.add(q2)).div(Q.of(16)); }

    enum Cut { REAL, HALF_ONLY, ETA_ZERO }

    record Cyl(V v0, V v1, V v2, V axis) {}

    static final class Family {
        final Q eps; final long n; final Cut cut;
        Family(Q eps, Cut cut) {
            this.eps = eps; this.cut = cut;
            Q q = Q.of(2).div(eps.mul(eps));                    // n eps = Nat.ceil (2 / eps^2)
            BigInteger[] qr = q.n().divideAndRemainder(q.d());
            this.n = qr[0].longValueExact() + (qr[1].signum() > 0 ? 1 : 0);
        }
        Q mesh(long i) { return Q.of(-1).add(Q.of(2 * i, n)); }
        Q cutoff(Q a, Q b) {
            return switch (cut) {
                case REAL -> HALF.add(eps.mul(eps).mul(ETA.add(dq(a).max(dq(b)))));
                case ETA_ZERO -> HALF.add(eps.mul(eps).mul(dq(a).max(dq(b))));
                case HALF_ONLY -> HALF;
            };
        }
        double cutoffD(double a, double b) {
            double e2 = eps.dbl() * eps.dbl(), m = Math.max(a * a * (1 + a * a), b * b * (1 + b * b)) / 16;
            return switch (cut) { case REAL -> 0.5 + e2 * (ETA.dbl() + m); case ETA_ZERO -> 0.5 + e2 * m; case HALF_ONLY -> 0.5; };
        }
        /// lowerCylinder: triangle point(0,0,0), point(0,aT,T), point(0,bT,T); axis tiltV = (1, eps A, H eps B).
        Cyl lower(long j) {
            Q a = mesh(j), b = mesh(j + 1), A = alpha(a, b), B = beta(a, b), T = cutoff(a, b);
            return new Cyl(new V(ZERO, ZERO, ZERO), new V(ZERO, a.mul(T), T), new V(ZERO, b.mul(T), T),
                new V(ONE, eps.mul(A), eps.mul(B)));
        }
        /// upperCylinder: triangle point(0,0,1), point(aT,0,1-T), point(bT,0,1-T); axis tiltW = (-eps A, 1, H eps B).
        Cyl upper(long j) {
            Q a = mesh(j), b = mesh(j + 1), A = alpha(a, b), B = beta(a, b), T = cutoff(a, b);
            return new Cyl(new V(ZERO, ZERO, ONE), new V(a.mul(T), ZERO, ONE.sub(T)), new V(b.mul(T), ZERO, ONE.sub(T)),
                new V(eps.mul(A).neg(), ONE, eps.mul(B)));
        }
    }

    /// Exact: P in conv(v0,v1,v2) + R*axis. Solve P - v0 = s1 e1 + s2 e2 + lam axis by Cramer.
    static boolean inCarrier(Cyl c, V p) {
        V e1 = c.v1.sub(c.v0), e2 = c.v2.sub(c.v0), r = p.sub(c.v0);
        Q dt = det3(e1, e2, c.axis);
        Q s1 = det3(r, e2, c.axis).div(dt), s2 = det3(e1, r, c.axis).div(dt);
        return s1.signum() >= 0 && s2.signum() >= 0 && s1.add(s2).compareTo(ONE) <= 0;
    }

    /// Exact squared area of the triangle projected onto the plane normal to the axis.
    static Q baseAreaSq(Cyl c) {
        V e1 = c.v1.sub(c.v0), e2 = c.v2.sub(c.v0), u = c.axis;
        Q dd = ip(u, u);
        Q g11 = ip(e1, e1).sub(ip(e1, u).mul(ip(e1, u)).div(dd));
        Q g22 = ip(e2, e2).sub(ip(e2, u).mul(ip(e2, u)).div(dd));
        Q g12 = ip(e1, e2).sub(ip(e1, u).mul(ip(e2, u)).div(dd));
        return g11.mul(g22).sub(g12.mul(g12)).div(Q.of(4));
    }

    // ------------------------------------------------------------------ search helpers
    /// Float fixed-point guess for the sector index, then an exact check of a +-4 window.
    static long findWitness(Family f, V p, boolean upper) {
        double x = p.x.dbl(), y = p.y.dbl(), t = p.t.dbl(), e = f.eps.dbl(); long n = f.n, j = 0;
        for (int it = 0; it < 30; it++) {
            double a = -1 + 2.0 * j / n, b = a + 2.0 / n, A = (1 + a * b) / 4, B = (a + b) / 4;
            double r = upper ? 1 - t + e * y * B : t - e * x * B, z = upper ? x + e * y * A : y - e * x * A;
            double q = r > 0 ? z / r : 0;
            long jn = Math.min(n - 1, Math.max(0, (long) Math.floor((q + 1) * n / 2)));
            if (jn == j) break;
            j = jn;
        }
        for (long k = Math.max(0, j - 4); k <= Math.min(n - 1, j + 4); k++)
            if (inCarrier(upper ? f.upper(k) : f.lower(k), p)) return k;
        return -1;
    }

    /// All indices (0..2n-1) whose cylinder contains p: float margins pre-filter at -1e-9, then exact.
    /// The margins are the coordinate form of membership (a lower carrier point has lam = x because
    /// the triangle lies in the plane x = 0 and the axis has x-component 1; upper: lam = y).
    static List<Long> exhaustive(Family f, V p) {
        double x = p.x.dbl(), y = p.y.dbl(), t = p.t.dbl(), e = f.eps.dbl(); long n = f.n;
        List<Long> hits = new ArrayList<>(); long cands = 0; double best = -1e300;
        for (int up = 0; up < 2; up++) for (long j = 0; j < n; j++) {
            double a = -1 + 2.0 * j / n, b = -1 + 2.0 * (j + 1) / n, A = (1 + a * b) / 4, B = (a + b) / 4, T = f.cutoffD(a, b);
            double r = up == 1 ? 1 - t + e * y * B : t - e * x * B, z = up == 1 ? x + e * y * A : y - e * x * A;
            double m = Math.min(Math.min(r, T - r), Math.min(z - a * r, b * r - z));
            best = Math.max(best, m);
            if (m > -1e-9) { cands++; if (inCarrier(up == 1 ? f.upper(j) : f.lower(j), p)) hits.add(up * n + j); }
        }
        System.out.printf("    exhaustive over %d cylinders: %d float candidates, max float margin %.3e%n", 2 * n, cands, best);
        return hits;
    }

    /// Sum of the two cutoff slacks at t = 1/2, and the t-shift that splits it evenly.
    static double[] slackG(Family f, double x, double y) {
        double e = f.eps.dbl(); long n = f.n;
        double[] res = new double[2], m = new double[2];
        for (int up = 0; up < 2; up++) {
            long j = 0; double a = 0, b = 0, B = 0;
            for (int it = 0; it < 30; it++) {
                a = -1 + 2.0 * j / n; b = a + 2.0 / n; double A = (1 + a * b) / 4; B = (a + b) / 4;
                double r = up == 1 ? 0.5 + e * y * B : 0.5 - e * x * B, z = up == 1 ? x + e * y * A : y - e * x * A;
                long jn = Math.min(n - 1, Math.max(0, (long) Math.floor((z / r + 1) * n / 2)));
                if (jn == j) break;
                j = jn;
            }
            a = -1 + 2.0 * j / n; b = a + 2.0 / n; B = (a + b) / 4;
            double T = f.cutoff(f.mesh(j), f.mesh(j + 1)).dbl();
            m[up] = T - (up == 1 ? 0.5 + e * y * B : 0.5 - e * x * B);
        }
        res[0] = m[0] + m[1]; res[1] = (m[0] - m[1]) / 2;
        return res;
    }

    static V adversarialPoint(double x, double y, double dt) {
        return new V(Q.of(Math.round(x * 1e9), 1_000_000_000L), Q.of(Math.round(y * 1e9), 1_000_000_000L),
            HALF.add(Q.of(dt)));
    }

    /// Returns {min G/eps^2, x, y, dt} over a grid.
    static double[] worstSlack(Family f, int grid) {
        double e2 = f.eps.dbl() * f.eps.dbl(); double[] w = {Double.MAX_VALUE, 0, 0, 0};
        for (int i = 0; i < grid; i++) for (int k = 0; k < grid; k++) {
            double x = -0.4999 + 0.9998 * i / (grid - 1), y = -0.4999 + 0.9998 * k / (grid - 1);
            double[] g = slackG(f, x, y);
            if (g[0] / e2 < w[0]) w = new double[] {g[0] / e2, x, y, g[1]};
        }
        return w;
    }

    // ------------------------------------------------------------------ area sum
    /// totalArea/H - 1/2 = sum_j D [e2 M + e2^2 M^2 + (1/4 + e2 M + e2^2 M^2)(g - 1)], g = (1+e2 S)^(-1/2).
    static double residual(Family f) {
        long n = f.n; double e2 = f.eps.dbl() * f.eps.dbl(), D = 2.0 / n, s = 0, c = 0;
        for (long j = 0; j < n; j++) {
            double a = -1 + j * D, b = -1 + (j + 1) * D, A = (1 + a * b) / 4, B = (a + b) / 4, S = A * A + 2 * B * B;
            double M = f.cutoffD(a, b) - 0.5; // = e2 * cutoffCoeff
            double gm1 = Math.expm1(-0.5 * Math.log1p(e2 * S));
            double term = D * (M + M * M + (0.25 + M + M * M) * gm1);
            double tt = s + term;                                            // Neumaier summation
            c += Math.abs(s) >= Math.abs(term) ? (s - tt) + term : (term - tt) + s;
            s = tt;
        }
        return s + c;
    }

    static double shadowClosedForm(double u0, double u1, double u2) {
        double h = Math.sqrt(2);
        return Math.max(h * Math.abs(u0), Math.abs(u2)) + Math.max(h * Math.abs(u1), Math.abs(u2));
    }

    static double shadowHull(double[] u) {
        double nu = Math.sqrt(u[0] * u[0] + u[1] * u[1] + u[2] * u[2]);
        double[] w = {u[0] / nu, u[1] / nu, u[2] / nu};
        double[] ref = Math.abs(w[0]) < 0.9 ? new double[] {1, 0, 0} : new double[] {0, 1, 0};
        double[] a = cross(w, ref); double na = Math.sqrt(dot(a, a)); for (int i = 0; i < 3; i++) a[i] /= na;
        double[] b = cross(w, a);
        double[][] P = {{-1, 0, 0}, {1, 0, 0}, {0, -1, Math.sqrt(2)}, {0, 1, Math.sqrt(2)}};
        double[][] pts = new double[4][];
        for (int i = 0; i < 4; i++) pts[i] = new double[] {dot(P[i], a), dot(P[i], b)};
        Arrays.sort(pts, (p, q) -> p[0] != q[0] ? Double.compare(p[0], q[0]) : Double.compare(p[1], q[1]));
        double[][] h = new double[8][]; int k = 0;
        for (int pass = 0; pass < 2; pass++) {
            int start = k;
            for (int ii = 0; ii < 4; ii++) {
                double[] p = pass == 0 ? pts[ii] : pts[3 - ii];
                while (k >= start + 2 && crossZ(h[k - 2], h[k - 1], p) <= 1e-15) k--;
                h[k++] = p;
            }
            k--;
        }
        double area = 0;
        for (int i = 0; i < k; i++) { double[] p = h[i], q = h[(i + 1) % k]; area += p[0] * q[1] - q[0] * p[1]; }
        return Math.abs(area) / 2;
    }
    static double[] cross(double[] a, double[] b) { return new double[] {a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]}; }
    static double dot(double[] a, double[] b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
    static double crossZ(double[] o, double[] p, double[] q) { return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0]); }

    // ------------------------------------------------------------------ main
    public static void main(String[] args) {
        Map<String, Boolean> ok = new LinkedHashMap<>();
        Random rnd = new Random(20261008);

        // A. tetrahedron and A_min
        V[] verts = {new V(Q.of(-1), ZERO, ZERO), new V(ONE, ZERO, ZERO), new V(ZERO, Q.of(-1), ONE), new V(ZERO, ONE, ONE)};
        boolean regular = true;
        for (int i = 0; i < 4; i++) for (int k = i + 1; k < 4; k++) { V d = verts[i].sub(verts[k]); regular &= ip(d, d).equals(Q.of(4)); }
        ok.put("K is a regular tetrahedron of edge 2 (exact squared edges = 4)", regular);
        V e1 = new V(ZERO, ONE, ONE), e2 = new V(ZERO, Q.of(-1), ONE);
        Q sh2 = ip(e1, e1).mul(ip(e2, e2)).sub(ip(e1, e2).mul(ip(e1, e2))).div(Q.of(4));
        ok.put("shadow along the x-axis has area^2 = 2 exactly (area H)", sh2.equals(Q.of(2)));
        double maxDiff = 0;
        for (int i = 0; i < 2000; i++) {
            double[] u = {rnd.nextGaussian(), rnd.nextGaussian(), rnd.nextGaussian()};
            double nu = Math.sqrt(dot(u, u));
            maxDiff = Math.max(maxDiff, Math.abs(shadowHull(u) - shadowClosedForm(u[0] / nu, u[1] / nu, u[2] / nu)));
        }
        ok.put(String.format("closed-form shadow = convex-hull shadow (max diff %.1e, 2000 directions)", maxDiff), maxDiff < 1e-12);
        int M = 400000; double best = 9; double gold = Math.PI * (3 - Math.sqrt(5));
        for (int i = 0; i < M; i++) {
            double z = 1 - 2 * (i + 0.5) / M, r = Math.sqrt(1 - z * z);
            best = Math.min(best, shadowClosedForm(r * Math.cos(gold * i), r * Math.sin(gold * i), z));
        }
        System.out.printf("min shadow over %d sphere points: %.12f (H = %.12f)%n", M, best, Math.sqrt(2));
        ok.put("no sampled shadow below H", best >= Math.sqrt(2) - 1e-12);

        // B. exact base areas at eps = 1/2001
        Family fam = new Family(Q.of(1, 2001), Cut.REAL);
        System.out.printf("eps = 1/2001, n(eps) = %d, cylinders = %d%n", fam.n, 2 * fam.n);
        ok.put("n(1/2001) = ceil(2*2001^2) = 8008002", fam.n == 8008002L);
        boolean areas = true;
        long[] js = {0, 1, fam.n / 3, fam.n / 2, fam.n - 1, 12345, 7000000};
        for (long j : js) {
            Q a = fam.mesh(j), b = fam.mesh(j + 1), A = alpha(a, b), B = beta(a, b), T = fam.cutoff(a, b);
            Q closed = Q.of(2).mul(b.sub(a).mul(b.sub(a))).mul(T.mul(T).mul(T.mul(T)))
                .div(Q.of(4).mul(ONE.add(fam.eps.mul(fam.eps).mul(A.mul(A).add(Q.of(2).mul(B.mul(B)))))));
            areas &= baseAreaSq(fam.lower(j)).equals(closed) && baseAreaSq(fam.upper(j)).equals(closed);
        }
        ok.put("base area^2 = (H (b-a) T^2 / (2 sqrt(1+eps^2(A^2+2B^2))))^2 exactly (14 cylinders)", areas);

        // C. area expansion
        double e = fam.eps.dbl(), r = residual(fam), R = r + 13.0 / 6000 * e * e;
        System.out.printf("totalArea/H - 1/2 = %.12e ; R = that + (13/6000) eps^2 = %.6e ; R/eps^4 = %.4f%n", r, R, R / Math.pow(e, 4));
        ok.put("|R| <= 14 eps^4 (Lean's constant)", Math.abs(R) <= 14 * Math.pow(e, 4));
        ok.put("totalArea < A_min/2 (i.e. totalArea/H < 1/2)", r < 0);

        // D. covering
        double[] w = worstSlack(fam, 81);
        System.out.printf("min over 81x81 grid of the slack G/eps^2 at t=1/2: %.6f at (%.4f, %.4f)%n", w[0], w[1], w[2]);
        ok.put("slack G > 0 on the grid", w[0] > 0);
        List<V> pts = new ArrayList<>();
        pts.add(adversarialPoint(w[1], w[2], w[3]));
        for (int i = 0; i < 60; i++) { double x = rnd.nextDouble() - 0.5, y = rnd.nextDouble() - 0.5; pts.add(adversarialPoint(x * 0.999, y * 0.999, slackG(fam, x * 0.999, y * 0.999)[1])); }
        for (V v : verts) pts.add(v);
        for (int i = 0; i < 1500; i++) {
            Q t = Q.of(rnd.nextInt(1_000_001), 1_000_000);
            Q fx = Q.of(rnd.nextInt(2_000_001) - 1_000_000, 1_000_000), fy = Q.of(rnd.nextInt(2_000_001) - 1_000_000, 1_000_000);
            pts.add(new V(fx.mul(ONE.sub(t)), fy.mul(t), t));                                   // interior
            pts.add(new V(fx.signum() >= 0 ? ONE.sub(t) : ONE.sub(t).neg(), fy.mul(t), t));     // face |x| = 1-t
            pts.add(new V(fx, ZERO, ZERO));                                                      // bottom edge
            Q ts = HALF.add(Q.of(rnd.nextInt(600_001) - 300_000, 1_000_000_000_000L));
            pts.add(new V(fx.mul(ONE.sub(ts)), fy.mul(ts), ts));                                 // critical slab
        }
        int uncovered = 0;
        for (V p : pts) if (findWitness(fam, p, false) < 0 && findWitness(fam, p, true) < 0) {
            uncovered++;
            System.out.println("  window search missed " + p);
            if (exhaustive(fam, p).isEmpty()) System.out.println("  REALLY UNCOVERED " + p);
        }
        ok.put("every one of " + pts.size() + " test points has an exact covering cylinder", uncovered == 0);

        ok.forEach((k, v) -> System.out.printf("  [%s] %s%n", v ? "OK " : "NO ", k));
        System.out.println(ok.values().stream().allMatch(b -> b) ? "ALL CHECKS HOLD" : "SOME CHECK FAILS");

        // negative controls: the replication must be able to say NO
        System.out.printf("control A: 'A_min = sqrt3' (face shadow) refuted, since a shadow %.6f < %.6f exists: %s%n",
            best, Math.sqrt(3), best < Math.sqrt(3) - 1e-3);
        double Rw = r + 12.0 / 6000 * e * e;
        System.out.printf("control C: with 12/6000 instead of 13/6000, |R'|/eps^4 = %.1f; within 14? %s%n",
            Math.abs(Rw) / Math.pow(e, 4), Math.abs(Rw) <= 14 * Math.pow(e, 4));
        Family half = new Family(Q.of(1, 2001), Cut.HALF_ONLY);
        double[] wh = worstSlack(half, 81);
        V hole = adversarialPoint(wh[1], wh[2], wh[3]);
        System.out.printf("control D: cutoff T = 1/2. min G/eps^2 = %.6f at (%.4f, %.4f); test point %s%n", wh[0], wh[1], wh[2], hole);
        List<Long> hh = exhaustive(half, hole);
        System.out.println("control D: cylinders containing it (exact): " + hh + (hh.isEmpty() ? "  -> UNCOVERED (control fails, as required)" : "  -> covered (control did NOT fail)"));
        System.out.println("control D: same point, real family: lower witness " + findWitness(fam, hole, false) + ", upper witness " + findWitness(fam, hole, true));
    }
}
