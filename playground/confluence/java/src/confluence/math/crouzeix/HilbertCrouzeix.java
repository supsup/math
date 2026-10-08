package confluence.math.crouzeix;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/// Java check of OAI.HilbertCrouzeix.numericalClosure_geometry
/// (lean/ComparatorChallenges/HilbertCrouzeix.lean) on explicit 2x2 complex matrices.
///
/// The theorem: for a bounded operator A on a complex Hilbert space, the closure of the numerical
/// range W(A) = { <x, A x> : ||x|| = 1 } is compact, convex, and contains the spectrum. This is the
/// classical Toeplitz-Hausdorff theorem plus the standard inclusion sigma(A) in closure W(A); it is a
/// support lemma for the collection's Crouzeix results, not Crouzeix's conjecture itself.
///
/// In dimension 2 everything has a closed form, so this file needs no eigen-solver:
///
/// - `lambdaMax(Re(e^{-it} A))` for a 2x2 Hermitian matrix is `(a+d)/2 + sqrt(((a-d)/2)^2 + |c|^2)`,
///   and W(A) is exactly the set of z with `Re(e^{-it} z) <= lambdaMax` for every t (W is convex).
/// - eigenvalues come from the quadratic formula.
///
/// Checks: sampled points of W lie within ||A|| (compact) and inside every support half-plane;
/// eigenvalues lie inside every support half-plane (spectrum inclusion); and the MIDPOINT of two
/// sampled points is attained by an explicit unit vector found by search (convexity, constructively).
/// Control (must fail): the real-vector variant { x^T A x : x real unit } of the same matrix does not
/// attain such midpoints; it is a closed curve, not a convex set.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.crouzeix.HilbertCrouzeix
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **A cheap, certified enclosure of eigenvalues.** The spectrum of any matrix sits inside its
///   numerical range, and the range is cut out by the support half-planes computed here from the
///   top eigenvalue of a Hermitian matrix. A Java numerics library could use a few half-planes as a
///   fast, always-valid eigenvalue bound for non-normal matrices (stability checks in simulation or
///   control code), where plain eigenvalues are ill-conditioned but W is not.
/// - **Transient-growth checks.** ||e^{tA}|| is bounded via W(A) (if W lies in Re z <= w then
///   ||e^{tA}|| <= e^{tw}), so a Java ODE or control loop could use lambdaMax(Re A) as a guaranteed
///   growth rate instead of the spectral abscissa, which can badly underestimate short-term growth.
/// - **A test oracle with a real/complex trap built in.** The control shows that switching to real
///   vectors silently breaks convexity. A Java implementation that computes W by sampling unit
///   vectors must sample COMPLEX vectors; this pair (complex passes, real fails) is a ready unit test
///   for that mistake.
/// - **Polynomial-of-matrix bounds (Crouzeix context).** ||p(A)|| <= (1+sqrt 2) max over W of |p| is
///   a proven bound; a library evaluating matrix polynomials could use it as an a-priori norm bound.
///   The constant 2 (Crouzeix's conjecture) is NOT checked here; the Jordan block below only shows a
///   case where the ratio is exactly 2.
public class HilbertCrouzeix {

    record C(double re, double im) {
        C plus(C o) { return new C(re + o.re, im + o.im); }
        C minus(C o) { return new C(re - o.re, im - o.im); }
        C times(C o) { return new C(re * o.re - im * o.im, re * o.im + im * o.re); }
        C scale(double s) { return new C(re * s, im * s); }
        C conj() { return new C(re, -im); }
        double abs() { return Math.hypot(re, im); }
        static C polar(double r, double t) { return new C(r * Math.cos(t), r * Math.sin(t)); }
        C sqrt() { double r = Math.sqrt(abs()); double t = Math.atan2(im, re) / 2; return polar(r, t); }
        @Override public String toString() { return String.format("%.4f%+.4fi", re, im); }
    }

    /// 2x2 matrix [[a, b], [c, d]].
    record M(C a, C b, C c, C d) {
        /// <x, A x> = conj(x) . (A x), conjugate-linear in the first slot as in Mathlib.
        C quad(C x0, C x1) {
            C y0 = a.times(x0).plus(b.times(x1));
            C y1 = c.times(x0).plus(d.times(x1));
            return x0.conj().times(y0).plus(x1.conj().times(y1));
        }
        C[] eig() {
            C tr = a.plus(d), det = a.times(d).minus(b.times(c));
            C disc = tr.times(tr).minus(det.scale(4)).sqrt();
            return new C[] {tr.plus(disc).scale(0.5), tr.minus(disc).scale(0.5)};
        }
        /// lambda_max of Re(e^{-it} A) = (B + B^*)/2 with B = e^{-it} A.
        double support(double t) {
            C r = C.polar(1, -t);
            C ba = r.times(a), bb = r.times(b), bc = r.times(c), bd = r.times(d);
            double h11 = ba.re, h22 = bd.re;
            C h12 = bb.plus(bc.conj()).scale(0.5);
            return (h11 + h22) / 2 + Math.sqrt((h11 - h22) * (h11 - h22) / 4 + h12.abs() * h12.abs());
        }
        /// Operator 2-norm: sqrt of lambda_max(A^* A).
        double norm() {
            double p = a.abs() * a.abs() + c.abs() * c.abs(), q = b.abs() * b.abs() + d.abs() * d.abs();
            C r = a.conj().times(b).plus(c.conj().times(d));
            return Math.sqrt((p + q) / 2 + Math.sqrt((p - q) * (p - q) / 4 + r.abs() * r.abs()));
        }
    }

    static final int DIRS = 4096;

    /// Largest violation of Re(e^{-it} z) <= support(t) over sampled t; <= ~0 means z is in W.
    static double excess(M m, C z) {
        double worst = Double.NEGATIVE_INFINITY;
        for (int k = 0; k < DIRS; k++) {
            double t = 2 * Math.PI * k / DIRS;
            worst = Math.max(worst, C.polar(1, -t).times(z).re - m.support(t));
        }
        return worst;
    }

    static C[] randomUnit(Random rnd) {
        C x0 = new C(rnd.nextGaussian(), rnd.nextGaussian()), x1 = new C(rnd.nextGaussian(), rnd.nextGaussian());
        double n = Math.hypot(x0.abs(), x1.abs());
        return new C[] {x0.scale(1 / n), x1.scale(1 / n)};
    }

    /// min over complex unit v = (cos th, e^{i ph} sin th) of |v^* A v - target| (global phase is irrelevant).
    static double attainComplex(M m, C target) {
        double bestR = Double.POSITIVE_INFINITY, th = 0, ph = 0;
        for (int i = 0; i <= 180; i++) for (int j = 0; j < 360; j++) {
            double t = Math.PI * i / 180, p = 2 * Math.PI * j / 360;
            double r = m.quad(new C(Math.cos(t), 0), C.polar(Math.sin(t), p)).minus(target).abs();
            if (r < bestR) { bestR = r; th = t; ph = p; }
        }
        for (double step = Math.PI / 180; step > 1e-14; ) {
            boolean improved = false;
            double[][] moves = {{step, 0}, {-step, 0}, {0, step}, {0, -step}};
            for (double[] mv : moves) {
                double t = th + mv[0], p = ph + mv[1];
                double r = m.quad(new C(Math.cos(t), 0), C.polar(Math.sin(t), p)).minus(target).abs();
                if (r < bestR) { bestR = r; th = t; ph = p; improved = true; }
            }
            if (!improved) step /= 2;
        }
        return bestR;
    }

    /// min over REAL unit v = (cos th, sin th) of |v^T A v - target| (the wrong variant).
    static double attainReal(M m, C target) {
        double best = Double.POSITIVE_INFINITY;
        for (int i = 0; i <= 400000; i++) {
            double t = Math.PI * i / 400000;
            best = Math.min(best, m.quad(new C(Math.cos(t), 0), new C(Math.sin(t), 0)).minus(target).abs());
        }
        return best;
    }

    static boolean checkMatrix(String name, M m, Random rnd) {
        double norm = m.norm(), maxAbs = 0, maxExcess = Double.NEGATIVE_INFINITY, maxMid = 0;
        List<C> pts = new ArrayList<>();
        for (int s = 0; s < 200; s++) {
            C[] x = randomUnit(rnd);
            C z = m.quad(x[0], x[1]);
            pts.add(z);
            maxAbs = Math.max(maxAbs, z.abs());
        }
        for (int s = 0; s < 40; s++) maxExcess = Math.max(maxExcess, excess(m, pts.get(s)));
        double eigExcess = Double.NEGATIVE_INFINITY;
        for (C l : m.eig()) eigExcess = Math.max(eigExcess, excess(m, l));
        for (int s = 0; s < 6; s++) maxMid = Math.max(maxMid, attainComplex(m, pts.get(2 * s).plus(pts.get(2 * s + 1)).scale(0.5)));
        boolean compact = maxAbs <= norm + 1e-12, inside = maxExcess <= 1e-9, spec = eigExcess <= 1e-9, convex = maxMid < 1e-9;
        boolean ok = compact && inside && spec && convex;
        System.out.printf("%-26s |z|max %.4f <= ||A|| %.4f: %b | samples in half-planes: %b | eig excess %.1e: %b | midpoint resid %.1e: %b  %s%n",
            name, maxAbs, norm, compact, inside, eigExcess, spec, maxMid, convex, ok ? "PASS" : "FAIL");
        return ok;
    }

    public static void main(String[] args) {
        Random rnd = new Random(20261008);
        C z0 = new C(0, 0), one = new C(1, 0), i = new C(0, 1);
        boolean ok = true;
        ok &= checkMatrix("normal diag(1, i)", new M(one, z0, z0, i), rnd);
        M j2 = new M(z0, one, z0, z0);
        ok &= checkMatrix("Jordan J2", j2, rnd);
        M ell = new M(one, new C(2, 0), z0, i);
        ok &= checkMatrix("ellipse [[1,2],[0,i]]", ell, rnd);
        M rand = new M(new C(rnd.nextGaussian(), rnd.nextGaussian()), new C(rnd.nextGaussian(), rnd.nextGaussian()),
            new C(rnd.nextGaussian(), rnd.nextGaussian()), new C(rnd.nextGaussian(), rnd.nextGaussian()));
        ok &= checkMatrix("random complex 2x2", rand, rnd);

        // W(J2) is the disk of radius 1/2: support(t) must be 1/2 in every direction.
        double lo = Double.POSITIVE_INFINITY, hi = 0;
        for (int k = 0; k < DIRS; k++) { double s = j2.support(2 * Math.PI * k / DIRS); lo = Math.min(lo, s); hi = Math.max(hi, s); }
        boolean disk = Math.abs(lo - 0.5) < 1e-12 && Math.abs(hi - 0.5) < 1e-12;
        System.out.printf("J2 support function in [%.12f, %.12f], expected 0.5: %b%n", lo, hi, disk);
        ok &= disk;

        // Control: real-vector variant of the ellipse matrix must NOT attain midpoints.
        double worst = 0;
        for (int s = 0; s < 10; s++) {
            double t1 = rnd.nextDouble() * Math.PI, t2 = rnd.nextDouble() * Math.PI;
            C a = ell.quad(new C(Math.cos(t1), 0), new C(Math.sin(t1), 0));
            C b = ell.quad(new C(Math.cos(t2), 0), new C(Math.sin(t2), 0));
            worst = Math.max(worst, attainReal(ell, a.plus(b).scale(0.5)));
        }
        boolean controlFails = worst > 1e-3;
        System.out.printf("CONTROL real-vector range of [[1,2],[0,i]]: worst midpoint miss %.4f -> convexity fails as expected: %b%n",
            worst, controlFails);
        ok &= controlFails;

        // Context only (not this theorem): Crouzeix ratio for J2 and p(z) = z is ||J2|| / max_{|z|<=1/2} |z| = 2.
        System.out.printf("context: Crouzeix ratio J2, p=z: %.6f (the known extremal value 2)%n", j2.norm() / 0.5);

        System.out.println(ok ? "OVERALL PASS" : "OVERALL FAIL");
        if (!ok) System.exit(1);
    }
}
