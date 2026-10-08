package confluence.math.crouzeixhilbert;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/// Java illustration of OAI.CrouzeixHilbert.hilbert (lean/ComparatorChallenges/CrouzeixHilbert.lean)
/// on 2x2 complex matrices, where everything has a closed form.
///
/// The theorem's headline clause is the (complete) Crouzeix inequality with constant 2:
/// for a bounded operator A on a complex Hilbert space and a polynomial p,
/// ||p(A)|| <= 2 * sup over W(A) of |p|, where W(A) = { x*Ax : ||x|| = 1 } is the numerical range.
/// Its `SharpConstant` clause says 2 cannot be lowered, witnessed by the 2x2 Jordan block J2 with
/// p(z) = 2z: W(J2) is the disk of radius 1/2, so sup_W |p| = 1, while ||2 J2|| = 2.
///
/// For a 2x2 matrix, W(A) is a closed elliptical disk (the elliptic range theorem): foci at the
/// eigenvalues l1, l2, minor axis sqrt(||A||_F^2 - |l1|^2 - |l2|^2). This file builds that ellipse
/// in closed form, checks it against x*Ax for random unit vectors x, computes ||p(A)|| with the
/// closed-form 2x2 spectral norm, and reports ||p(A)|| / max over the ellipse of |p|.
/// Controls that must FAIL: replacing W by the convex hull of the spectrum (ratio infinite for
/// J2), and replacing the constant 2 by 1.9 (fails at J2).
///
/// This checks a handful of 2x2 cases. It is not evidence for the theorem in general: Crouzeix's
/// inequality is already known to hold with constant 2 for 2x2 matrices (Crouzeix 2004).
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.crouzeixhilbert.CrouzeixHilbert
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **A transient-growth bound for linear iterations.** Code that iterates x_{k+1} = A x_k
///   (Markov chains, linear recurrences, explicit time-steppers, IIR filters) can see ||A^k||
///   grow transiently even when every eigenvalue is inside the unit disk. If the inequality holds,
///   ||p(A)|| <= 2 max_W |p| bounds that growth using W(A), which is computable from Hermitian
///   eigenproblems. A Java numerics library could expose `numericalRadius` and use 2 * r(A)^k as a
///   certified bound on ||A^k||. (The bound ||A^k|| <= 2 r(A)^k is in fact already classical, via
///   Berger's power inequality; Crouzeix's inequality extends it to every polynomial.)
/// - **A guard for eigenvalue-only stability checks.** The control in this file shows the
///   spectrum alone says nothing: J2 has spectrum {0} but norm 1. A stability check in Java code
///   that looks only at eigenvalues should be suspected; the numerical range is the safe input.
/// - **A regression fixture for norm and numerical-range code.** J2 with p(z) = 2z gives exactly
///   ratio 2 (sup 1, norm 2), and J3 with p(z) = z^2 does too; these make cheap exact unit tests
///   for a spectral-norm or numerical-range routine.
public class CrouzeixHilbert {

    // ------------------------------------------------------------------ complex numbers
    record C(double re, double im) {
        static final C ZERO = new C(0, 0), ONE = new C(1, 0), I = new C(0, 1);
        C add(C o) { return new C(re + o.re, im + o.im); }
        C sub(C o) { return new C(re - o.re, im - o.im); }
        C mul(C o) { return new C(re * o.re - im * o.im, re * o.im + im * o.re); }
        C scale(double s) { return new C(re * s, im * s); }
        C conj() { return new C(re, -im); }
        double abs() { return Math.hypot(re, im); }
        double abs2() { return re * re + im * im; }
        C sqrt() {
            double r = abs();
            double a = Math.sqrt((r + re) / 2), b = Math.copySign(Math.sqrt((r - re) / 2), im);
            return new C(a, b);
        }
        static C polar(double r, double t) { return new C(r * Math.cos(t), r * Math.sin(t)); }
        double arg() { return Math.atan2(im, re); }
    }

    // ------------------------------------------------------------------ 2x2 matrices
    record M(C a, C b, C c, C d) {
        static final M ID = new M(C.ONE, C.ZERO, C.ZERO, C.ONE);
        M add(M o) { return new M(a.add(o.a), b.add(o.b), c.add(o.c), d.add(o.d)); }
        M scale(C s) { return new M(a.mul(s), b.mul(s), c.mul(s), d.mul(s)); }
        M mul(M o) {
            return new M(a.mul(o.a).add(b.mul(o.c)), a.mul(o.b).add(b.mul(o.d)),
                         c.mul(o.a).add(d.mul(o.c)), c.mul(o.b).add(d.mul(o.d)));
        }
        C trace() { return a.add(d); }
        C det() { return a.mul(d).sub(b.mul(c)); }
        double frob2() { return a.abs2() + b.abs2() + c.abs2() + d.abs2(); }
        /// Closed-form largest singular value of a 2x2 matrix:
        /// sigma_max^2 = (F^2 + sqrt(F^4 - 4|det|^2)) / 2.
        double opNorm() {
            double f = frob2(), dd = det().abs2();
            return Math.sqrt((f + Math.sqrt(Math.max(0, f * f - 4 * dd))) / 2);
        }
        /// x* A x, with the conjugate on the FIRST slot (Mathlib's inner product convention).
        C quad(C x0, C x1) {
            C y0 = a.mul(x0).add(b.mul(x1)), y1 = c.mul(x0).add(d.mul(x1));
            return x0.conj().mul(y0).add(x1.conj().mul(y1));
        }
        C[] eigenvalues() {
            C half = trace().scale(0.5);
            C disc = half.mul(half).sub(det()).sqrt();
            return new C[] {half.add(disc), half.sub(disc)};
        }
    }

    /// The numerical range of a 2x2 matrix: an ellipse with foci at the eigenvalues.
    record Ellipse(C center, double semiMajor, double semiMinor, double angle) {
        static Ellipse of(M m) {
            C[] l = m.eigenvalues();
            double minor2 = Math.max(0, m.frob2() - l[0].abs2() - l[1].abs2());
            double b = Math.sqrt(minor2) / 2;
            double halfFocal = l[0].sub(l[1]).abs() / 2;
            double a = Math.sqrt(b * b + halfFocal * halfFocal);
            double ang = halfFocal > 0 ? l[0].sub(l[1]).arg() : 0;
            return new Ellipse(l[0].add(l[1]).scale(0.5), a, b, ang);
        }
        C point(double t) {
            C local = new C(semiMajor * Math.cos(t), semiMinor * Math.sin(t));
            return center.add(local.mul(C.polar(1, angle)));
        }
        /// (u/a)^2 + (v/b)^2 in the ellipse frame; <= 1 means inside (degenerate b = 0 handled by caller).
        double level(C z) {
            C local = z.sub(center).mul(C.polar(1, -angle));
            double u = local.re() / semiMajor, v = semiMinor > 1e-15 ? local.im() / semiMinor : 0;
            return u * u + v * v;
        }
    }

    static M poly(M a, C[] coeffs) {
        M acc = new M(C.ZERO, C.ZERO, C.ZERO, C.ZERO), pow = M.ID;
        for (C k : coeffs) { acc = acc.add(pow.scale(k)); pow = pow.mul(a); }
        return acc;
    }

    static C poly(C z, C[] coeffs) {
        C acc = C.ZERO, pow = C.ONE;
        for (C k : coeffs) { acc = acc.add(pow.mul(k)); pow = pow.mul(z); }
        return acc;
    }

    /// max over the ellipse boundary of |p| (max modulus principle: the max over the closed disk
    /// is on the boundary). Sampled, so this is a lower bound and the ratio an upper bound.
    static double supOnW(Ellipse e, C[] coeffs) {
        double best = 0;
        int n = 20000;
        for (int k = 0; k < n; k++) best = Math.max(best, poly(e.point(2 * Math.PI * k / n), coeffs).abs());
        return best;
    }

    static final List<String> FAILURES = new ArrayList<>();

    static double ratio(String name, M a, C[] coeffs, double bound, boolean expectFail) {
        Ellipse e = Ellipse.of(a);
        double num = poly(a, coeffs).opNorm(), den = supOnW(e, coeffs);
        double r = den < 1e-14 ? Double.POSITIVE_INFINITY : num / den;
        boolean ok = r <= bound + 1e-9;
        System.out.printf("  %-44s ||p(A)|| = %.9f  sup_W|p| = %.9f  ratio = %.9f  %s (bound %.1f)%s%n",
            name, num, den, r, ok ? "ok" : "EXCEEDS", bound, expectFail ? "  [control: must exceed]" : "");
        if (ok == expectFail) FAILURES.add(name);
        return r;
    }

    static C c(double re, double im) { return new C(re, im); }
    static C r(double re) { return new C(re, 0); }

    public static void main(String[] args) {
        M j2 = new M(C.ZERO, C.ONE, C.ZERO, C.ZERO);
        M ell = new M(C.ONE, r(2), C.ZERO, C.I);
        M skew = new M(r(0), r(5), C.ZERO, r(0.3));
        M normal = new M(C.ONE, C.ZERO, C.ZERO, C.I);
        M generic = new M(c(0.3, -1), c(1.7, 0.4), c(-0.2, 0.9), c(-1.1, 0.5));
        M[] mats = {j2, ell, skew, normal, generic};
        String[] names = {"J2", "[[1,2],[0,i]]", "[[0,5],[0,0.3]]", "diag(1,i)", "generic"};

        System.out.println("== closed-form W(A) vs x*Ax for 200000 random unit vectors");
        Random rnd = new Random(20261008);
        for (int i = 0; i < mats.length; i++) {
            Ellipse e = Ellipse.of(mats[i]);
            double worst = 0;
            for (int k = 0; k < 200000; k++) {
                C x0 = new C(rnd.nextGaussian(), rnd.nextGaussian()), x1 = new C(rnd.nextGaussian(), rnd.nextGaussian());
                double n = Math.sqrt(x0.abs2() + x1.abs2());
                C z = mats[i].quad(x0.scale(1 / n), x1.scale(1 / n));
                worst = Math.max(worst, e.semiMinor() > 1e-12 ? e.level(z) : 0);
            }
            boolean ok = worst <= 1 + 1e-9;
            System.out.printf("  %-16s center %s, semi-axes %.9f / %.9f, max level of samples %.9f %s%n",
                names[i], fmt(e.center()), e.semiMajor(), e.semiMinor(), worst, ok ? "ok" : "OUTSIDE");
            if (!ok) FAILURES.add("ellipse " + names[i]);
        }

        System.out.println("== ratios ||p(A)|| / sup_W |p| (must be <= 2)");
        C[][] polys = {{C.ZERO, r(2)}, {C.ZERO, C.ZERO, C.ONE}, {C.ONE, r(2), C.ZERO, r(-1)}, {c(0.5, 1), C.I, r(-3)}};
        String[] pnames = {"2z", "z^2", "1+2z-z^3", "(0.5+i)+iz-3z^2"};
        for (int i = 0; i < mats.length; i++)
            for (int k = 0; k < polys.length; k++)
                ratio(names[i] + ", p=" + pnames[k], mats[i], polys[k], 2, false);

        double sharp = ratio("SharpConstant witness: J2, p=2z", j2, polys[0], 2, false);
        if (Math.abs(sharp - 2) > 1e-9) FAILURES.add("J2 ratio is not exactly 2");

        System.out.println("== NEGATIVE CONTROLS");
        // W replaced by conv(spectrum) = {0} for J2: sup over {0} of |2z| is 0, so the ratio is infinite.
        double convSpec = Math.max(poly(j2.eigenvalues()[0], polys[0]).abs(), poly(j2.eigenvalues()[1], polys[0]).abs());
        boolean convFails = poly(j2, polys[0]).opNorm() > 2 * convSpec;
        System.out.printf("  W -> conv(spectrum), J2, p=2z: sup = %.3g, ||p(A)|| = %.3f -> bound %s%n",
            convSpec, poly(j2, polys[0]).opNorm(), convFails ? "FAILS (as it must)" : "holds (control broken)");
        if (!convFails) FAILURES.add("conv(spectrum) control did not fail");
        ratio("constant 1.9, J2, p=2z", j2, polys[0], 1.9, true);

        System.out.println();
        System.out.println("OVERALL: " + (FAILURES.isEmpty() ? "PASS" : "FAIL " + FAILURES));
        if (!FAILURES.isEmpty()) System.exit(1);
    }

    static String fmt(C z) { return String.format("%.6f%+.6fi", z.re(), z.im()); }
}
