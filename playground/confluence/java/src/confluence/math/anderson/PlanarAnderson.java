package confluence.math.anderson;

import java.util.Arrays;
import java.util.Random;

/// Finite-box illustration of OAI.PlanarAnderson.anderson_spectrum_ae
/// (lean/ComparatorChallenges/PlanarAndersonSpectrum.lean). It is an illustration, not a proof.
///
/// The Lean theorem is about the infinite lattice Z^2. For h > 0, draw v(x) independently and
/// uniformly from [-h, h] at every site. Then almost surely the operator
/// (H u)(x) = u(x+e1) + u(x-e1) + u(x+e2) + u(x-e2) + v(x) u(x) on l^2(Z^2) is bounded and
/// self-adjoint, and its spectrum is exactly the real interval [-4-h, 4+h]. The theorem says
/// nothing about spectral type, so it is not a localization result.
///
/// Here the same operator lives on an L x L torus, which makes it a symmetric (L^2 x L^2) matrix.
/// A cyclic Jacobi eigen-solver diagonalizes it, and the program checks four things:
///
/// - every eigenvalue lies in [-4-h, 4+h], which holds for every box because ||H|| <= 4 + h;
/// - a planted constant n x n patch v = w pushes the top eigenvalue above 4 cos(pi/(n+1)) + w
///   (a Rayleigh-quotient bound). This is how the proof reaches the edges;
/// - CONTROL: a checkerboard potential +-h has a gap (-h, h) and edges +-sqrt(16 + h^2), so it
///   does not fill [-4-h, 4+h]. The prediction must fail for it, and it does;
/// - CONTROL: with zero potential the top eigenvalue is 4, not 4 + h.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.anderson.PlanarAnderson
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend. They are not claims from the paper.
///
/// - **A spectral-bound assertion for graph code.** For any graph Laplacian or adjacency
///   matrix with a bounded diagonal, every eigenvalue lies within max degree + max |diagonal|. That
///   is the `||H|| <= 4 + h` step here, and it is a cheap invariant that a Java numerical or
///   graph-analytics library can assert in tests of its eigen-solver.
/// - **Random data fills the whole interval, periodic data does not.** A simulation on a grid,
///   such as a lattice model or an image filter built on the 4-neighbour stencil, sees energies
///   right up to 4 + h only if large patches are nearly constant. Typical boxes stop well short
///   of the edges (about 4.2 at L = 48 for h = 1 in replicate.py). A test that expects "the
///   extreme eigenvalue equals 4 + h" on a finite random sample is therefore wrong.
/// - **A small reusable Jacobi solver.** `jacobi` is about 30 lines and accurate for small
///   dense symmetric matrices, which is enough for unit tests of larger solvers. It is far too
///   slow for production sizes (it is O(n^3) per sweep).
public class PlanarAnderson {

    /// Adjacency (hopping) matrix of the L x L torus: H[s][t] += 1 for each nearest neighbour.
    static double[][] hopping(int l) {
        int n = l * l;
        double[][] a = new double[n][n];
        int[][] d = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        for (int i = 0; i < l; i++)
            for (int j = 0; j < l; j++)
                for (int[] e : d) {
                    int t = Math.floorMod(i + e[0], l) * l + Math.floorMod(j + e[1], l);
                    a[i * l + j][t] += 1.0;
                }
        return a;
    }

    static double[][] withPotential(double[][] a, double[] v) {
        double[][] m = new double[a.length][];
        for (int i = 0; i < a.length; i++) {
            m[i] = a[i].clone();
            m[i][i] += v[i];
        }
        return m;
    }

    /// Cyclic Jacobi rotations until the off-diagonal mass is negligible; returns sorted eigenvalues.
    static double[] jacobi(double[][] in) {
        int n = in.length;
        double[][] a = new double[n][];
        for (int i = 0; i < n; i++) a[i] = in[i].clone();
        for (int sweep = 0; sweep < 100; sweep++) {
            double off = 0;
            for (int p = 0; p < n; p++) for (int q = p + 1; q < n; q++) off += a[p][q] * a[p][q];
            if (off < 1e-22) break;
            for (int p = 0; p < n; p++)
                for (int q = p + 1; q < n; q++) {
                    if (Math.abs(a[p][q]) < 1e-300) continue;
                    double theta = (a[q][q] - a[p][p]) / (2 * a[p][q]);
                    double t = Math.signum(theta == 0 ? 1 : theta)
                        / (Math.abs(theta) + Math.sqrt(theta * theta + 1));
                    double c = 1 / Math.sqrt(t * t + 1), s = t * c;
                    for (int k = 0; k < n; k++) { // columns p, q
                        double akp = a[k][p], akq = a[k][q];
                        a[k][p] = c * akp - s * akq;
                        a[k][q] = s * akp + c * akq;
                    }
                    for (int k = 0; k < n; k++) { // rows p, q
                        double apk = a[p][k], aqk = a[q][k];
                        a[p][k] = c * apk - s * aqk;
                        a[q][k] = s * apk + c * aqk;
                    }
                }
        }
        double[] ev = new double[n];
        for (int i = 0; i < n; i++) ev[i] = a[i][i];
        Arrays.sort(ev);
        return ev;
    }

    static boolean allIn(double[] ev, double lo, double hi) {
        for (double e : ev) if (e < lo - 1e-9 || e > hi + 1e-9) return false;
        return true;
    }

    public static void main(String[] args) {
        int l = 10;
        double h = 1.0, lo = -4 - h, hi = 4 + h;
        double[][] a = hopping(l);
        Random rng = new Random(20261008L);
        boolean ok = true;

        // Solver self-check: the free torus spectrum is {2cos(2 pi j/L) + 2cos(2 pi k/L)}.
        double[] free = jacobi(a);
        double[] exact = new double[l * l];
        for (int j = 0; j < l; j++) for (int k = 0; k < l; k++)
            exact[j * l + k] = 2 * Math.cos(2 * Math.PI * j / l) + 2 * Math.cos(2 * Math.PI * k / l);
        Arrays.sort(exact);
        double err = 0;
        for (int i = 0; i < exact.length; i++) err = Math.max(err, Math.abs(free[i] - exact[i]));
        System.out.printf("solver check vs exact torus spectrum: max error %.2e%n", err);
        ok &= err < 1e-9;

        double[] v = new double[l * l];
        for (int i = 0; i < v.length; i++) v[i] = -h + 2 * h * rng.nextDouble();
        double[] ev = jacobi(withPotential(a, v));
        boolean inside = allIn(ev, lo, hi);
        System.out.printf("random box L=%d h=%.1f: eigenvalues in [%.4f, %.4f], predicted Z^2 spectrum [%.1f, %.1f]; all inside: %b%n",
            l, h, ev[0], ev[ev.length - 1], lo, hi, inside);
        ok &= inside;

        int n = 8;
        double w = 0.95;
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) v[i * l + j] = w;
        double[] evp = jacobi(withPotential(a, v));
        double bound = 4 * Math.cos(Math.PI / (n + 1)) + w;
        boolean patch = evp[evp.length - 1] >= bound - 1e-9 && allIn(evp, lo, hi);
        System.out.printf("planted %dx%d patch v=%.2f: top eigenvalue %.4f >= Rayleigh bound %.4f: %b (edge 4+h=%.1f)%n",
            n, n, w, evp[evp.length - 1], bound, patch, hi);
        ok &= patch;

        // CONTROL 1: checkerboard. Prediction "fills [-4-h,4+h]" must fail.
        double[] cb = new double[l * l];
        for (int i = 0; i < l; i++) for (int j = 0; j < l; j++) cb[i * l + j] = ((i + j) % 2 == 0) ? h : -h;
        double[] evc = jacobi(withPotential(a, cb));
        double gapLo = -1e9, gapHi = 1e9;
        for (double e : evc) { if (e < 0) gapLo = Math.max(gapLo, e); else gapHi = Math.min(gapHi, e); }
        boolean cbFails = gapHi - gapLo > 2 * h - 1e-9 && evc[evc.length - 1] < hi - 0.5;
        System.out.printf("CONTROL checkerboard: edges +-%.4f (theory sqrt(16+h^2)=%.4f), gap (%.4f, %.4f); fails to fill: %b%n",
            evc[evc.length - 1], Math.sqrt(16 + h * h), gapLo, gapHi, cbFails);
        ok &= cbFails;

        // CONTROL 2: zero potential tops out at 4, not 4 + h.
        boolean zeroFails = free[free.length - 1] < hi - 0.5;
        System.out.printf("CONTROL zero potential: top eigenvalue %.4f, misses (4, 4+h]: %b%n", free[free.length - 1], zeroFails);
        ok &= zeroFails;

        System.out.println(ok ? "ALL CHECKS AS EXPECTED" : "SOME CHECK FAILED");
        if (!ok) System.exit(1);
    }
}
