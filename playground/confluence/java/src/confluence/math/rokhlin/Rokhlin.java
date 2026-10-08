package confluence.math.rokhlin;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.SplittableRandom;

/// Java illustration of the DEFINITIONS in OAI.Rokhlin.mixing_all_finite_orders
/// (lean/ComparatorChallenges/Rokhlin.lean). Not evidence for the theorem.
///
/// The Lean statement: for any probability space and any invertible, bimeasurable,
/// measure-preserving `T`, if `T` is mixing (`mu(A ∩ T^-n B) -> mu(A) mu(B)` as `|n| -> ∞`,
/// for all measurable `A`, `B`), then for every `k >= 3` and measurable `A_0..A_{k-1}`,
/// `mu(⋂ T^-t_i A_i) -> ∏ mu(A_i)` as ALL successive gaps `t_{i+1} - t_i` tend to infinity
/// (`layoutTime`: `t_0 = 0`, `t_i = g_0 + ... + g_{i-1}`, each `g_j >= 1`, filter `atTop` on
/// the product order of gap vectors). That is Rokhlin's 1949 multiple-mixing problem, stated
/// in full.
///
/// This class checks three things that ARE computable:
/// - `layoutTime` turns gaps into times exactly as the Lean definition does;
/// - a Bernoulli shift (where all-orders mixing is classical) hits the product EXACTLY once
///   the minimum gap exceeds the cylinder window, and Arnold's cat map approaches it (Monte Carlo);
/// - NEGATIVE CONTROL: an irrational rotation (invertible, measure preserving, ergodic, not
///   mixing) does NOT approach the product: along Fibonacci gaps the 3-fold correlation stays
///   near `mu(A)`, not `mu(A)^3`.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.rokhlin.Rokhlin
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Testing pseudo-random generators and hash mixers.** "Mixing" is the ergodic-theory
///   ancestor of the avalanche/independence properties asked of a PRNG or a hash finalizer. A
///   pairwise test (correlation of outputs `n` steps apart) is a 2-fold test; this check is the
///   3-fold version (`A`, then `B` after gap `g1`, then `C` after `g2`). Rokhlin's question is
///   exactly whether passing every 2-fold test forces passing every k-fold one. Whatever the
///   status of the proof, a Java test suite for a generator should run the k-fold check
///   directly rather than infer it from pairwise statistics: the implication is a theorem about
///   ideal measure-preserving maps, not about finite-state generators, which are periodic.
/// - **A negative control that every correlation test should include.** The rotation
///   `x -> x + alpha` is a classic "looks uniform, is not random" sequence (Weyl/low-discrepancy
///   sequences are used deliberately in quasi-Monte Carlo). A correlation test harness that
///   cannot flag it as non-mixing is not testing mixing. The `rotation()` method here is a
///   ready-made fixture for that.
/// - **Exact fixtures beat Monte Carlo when they exist.** For cylinder sets of a Bernoulli
///   shift the k-fold measure is a finite product, computed here in exact `long` arithmetic, so
///   a test can assert equality instead of a tolerance. That pattern (find the exactly
///   solvable sub-case, assert it exactly, and only use sampling elsewhere) carries over to any
///   probabilistic Java code.
/// - **Overflow-safe torus arithmetic.** The cat-map sampler runs on the lattice `(Z / 2^60)^2`
///   so `2x + y` never overflows a `long`; that is a small, reusable trick for exact
///   reversible-map simulation in Java without `BigInteger`.
public class Rokhlin {

    // ---- Lean's layoutTime ----------------------------------------------------------------
    /// `layoutTime gaps i = sum_{j < i} gaps j`.
    static long layoutTime(long[] gaps, int i) {
        long t = 0;
        for (int j = 0; j < gaps.length; j++) if (j < i) t += gaps[j];
        return t;
    }

    // ---- Bernoulli(3/10) two-sided shift, cylinder sets, exact ------------------------------
    /// A cylinder is a map coordinate -> symbol. Measure of an intersection of shifted cylinders,
    /// returned as a numerator over 10^(number of constrained coordinates); -1 numerator = empty.
    record Exact(long num, int tenPower) {
        boolean sameValue(Exact o) {
            // a/10^p == b/10^q  <=>  a*10^q == b*10^p (small powers, no overflow here)
            return num * pow10(o.tenPower) == o.num * pow10(tenPower);
        }
        double value() { return num / (double) pow10(tenPower); }
    }

    static long pow10(int p) { long r = 1; for (int i = 0; i < p; i++) r *= 10; return r; }

    static Exact cylinderMeasure(List<Map<Long, Integer>> constraints) {
        Map<Long, Integer> merged = new HashMap<>();
        for (Map<Long, Integer> c : constraints)
            for (var e : c.entrySet()) {
                Integer prev = merged.putIfAbsent(e.getKey(), e.getValue());
                if (prev != null && !prev.equals(e.getValue())) return new Exact(0, 0);
            }
        long num = 1;
        for (int s : merged.values()) num *= (s == 1 ? 3 : 7);
        return new Exact(num, merged.size());
    }

    static Map<Long, Integer> shift(Map<Long, Integer> c, long t) {
        Map<Long, Integer> out = new HashMap<>();
        c.forEach((pos, s) -> out.put(pos + t, s));
        return out;
    }

    static boolean bernoulli() {
        Map<Long, Integer> a = Map.of(0L, 1, 1L, 0, 2L, 1);
        Map<Long, Integer> b = Map.of(0L, 1, 1L, 1);
        Map<Long, Integer> c = Map.of(0L, 0, 2L, 0, 3L, 1);
        Exact pa = cylinderMeasure(List.of(a)), pb = cylinderMeasure(List.of(b)), pc = cylinderMeasure(List.of(c));
        Exact product = new Exact(pa.num() * pb.num() * pc.num(), pa.tenPower() + pb.tenPower() + pc.tenPower());
        System.out.printf("[Bernoulli(3/10), exact] product = %.6f%n", product.value());
        boolean ok = true;
        for (long g : new long[]{1, 2, 3, 4, 10, 1000}) {
            long[] gaps = {g, g};
            Exact v = cylinderMeasure(List.of(a, shift(b, layoutTime(gaps, 1)), shift(c, layoutTime(gaps, 2))));
            boolean eq = v.sameValue(product);
            System.out.printf("  gaps (%d,%d): %.6f  exact product: %b%n", g, g, v.value(), eq);
            // window length is 4, so every gap >= 4 must give the product exactly
            if (g >= 4 && !eq) ok = false;
        }
        return ok;
    }

    // ---- Arnold cat map on (Z/2^60)^2, Monte Carlo ------------------------------------------
    static final long Q = 1L << 60, MASK = Q - 1;

    static boolean inRect(long x, long y, double x0, double x1, double y0, double y1) {
        double u = x / (double) Q, v = y / (double) Q;
        return u >= x0 && u < x1 && v >= y0 && v < y1;
    }

    static double catTriple(int g1, int g2, int samples, long seed) {
        SplittableRandom rnd = new SplittableRandom(seed);
        int hits = 0;
        for (int s = 0; s < samples; s++) {
            long x = rnd.nextLong() & MASK, y = rnd.nextLong() & MASK;
            if (!inRect(x, y, 0.0, 0.5, 0.0, 0.6)) continue;           // A, mu = 0.30
            for (int i = 0; i < g1; i++) { long nx = (2 * x + y) & MASK; y = (x + y) & MASK; x = nx; }
            if (!inRect(x, y, 0.3, 0.8, 0.1, 0.5)) continue;           // B, mu = 0.20
            for (int i = 0; i < g2; i++) { long nx = (2 * x + y) & MASK; y = (x + y) & MASK; x = nx; }
            if (inRect(x, y, 0.1, 0.4, 0.0, 1.0)) hits++;              // C, mu = 0.30
        }
        return hits / (double) samples;
    }

    static boolean cat() {
        double product = 0.30 * 0.20 * 0.30;
        int n = 400_000;
        double sigma = Math.sqrt(product * (1 - product) / n);
        System.out.printf("[cat map, Monte Carlo n=%d] product = %.4f, 1-sigma = %.4f%n", n, product, sigma);
        double last = 0;
        for (int[] g : new int[][]{{1, 1}, {2, 2}, {5, 5}, {10, 10}, {15, 20}}) {
            last = catTriple(g[0], g[1], n, 7L);
            System.out.printf("  gaps (%d,%d): %.4f  deviation %+.4f%n", g[0], g[1], last, last - product);
        }
        return Math.abs(last - product) < 5 * sigma;
    }

    // ---- NEGATIVE CONTROL: rotation by the golden mean, exact interval arithmetic -----------
    static final double ALPHA = (Math.sqrt(5) - 1) / 2;

    static List<double[]> arc(double a, double len) {
        double s = a - Math.floor(a);
        List<double[]> out = new ArrayList<>();
        if (s + len <= 1) out.add(new double[]{s, s + len});
        else { out.add(new double[]{s, 1}); out.add(new double[]{0, s + len - 1}); }
        return out;
    }

    /// Lebesgue measure of the intersection of arcs [start_i, start_i + len).
    static double arcIntersection(double len, double... starts) {
        List<double[]> cur = arc(starts[0], len);
        for (int k = 1; k < starts.length; k++) {
            List<double[]> nxt = new ArrayList<>();
            for (double[] p : cur)
                for (double[] q : arc(starts[k], len)) {
                    double lo = Math.max(p[0], q[0]), hi = Math.min(p[1], q[1]);
                    if (hi > lo) nxt.add(new double[]{lo, hi});
                }
            cur = nxt;
        }
        double m = 0;
        for (double[] p : cur) m += p[1] - p[0];
        return m;
    }

    static boolean rotation() {
        double len = 0.4, cube = len * len * len;
        System.out.printf("[CONTROL: rotation, exact] mu(A)^3 = %.4f; a mixing system would approach it%n", cube);
        long f1 = 75025, f2 = 121393;
        boolean staysFar = true;
        for (int r = 0; r < 6; r++) {
            long[] gaps = {f1, f2};
            double v = arcIntersection(len, 0.0,
                -layoutTime(gaps, 1) * ALPHA, -layoutTime(gaps, 2) * ALPHA); // T^-t A = A - t alpha
            System.out.printf("  gaps (%d,%d): %.4f%n", f1, f2, v);
            if (Math.abs(v - cube) < 0.2) staysFar = false;
            long f3 = f1 + f2; f1 = f2; f2 = f3;
        }
        return staysFar;
    }

    public static void main(String[] args) {
        long[] gaps = {5, 7, 11};
        long[] times = {layoutTime(gaps, 0), layoutTime(gaps, 1), layoutTime(gaps, 2), layoutTime(gaps, 3)};
        boolean layoutOk = times[0] == 0 && times[1] == 5 && times[2] == 12 && times[3] == 23;
        System.out.printf("layoutTime (5,7,11) -> [%d, %d, %d, %d] ok=%b%n", times[0], times[1], times[2], times[3], layoutOk);
        boolean b = bernoulli(), c = cat(), r = rotation();
        System.out.printf("%nlayout=%b bernoulliExact=%b catNearProduct=%b rotationControlFails=%b%n", layoutOk, b, c, r);
        if (!(layoutOk && b && c && r)) { System.out.println("CHECK FAILED"); System.exit(1); }
        System.out.println("ALL CHECKS PASSED (illustration of the definitions, not evidence for the theorem)");
    }
}
