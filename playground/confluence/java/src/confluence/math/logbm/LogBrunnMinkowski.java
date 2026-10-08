package confluence.math.logbm;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.function.ToDoubleFunction;

/// Java check of the inequality stated in OAI.LogBrunnMinkowski.main
/// (lean/ComparatorChallenges/LogBrunnMinkowski.lean), in the plane, definition for definition.
///
/// - `support K u` is `sup { <x,u> : x in K }`; for a polygon that is the max over its vertices.
/// - `wulff f` is `{ x : <x,u> <= f(u) for every unit u }`.
/// - `logCombination K L t` is `wulff (u -> h_K(u)^(1-t) * h_L(u)^t)`.
/// - The theorem: for origin-symmetric convex bodies K, L and 0 <= t <= 1,
///   `vol(K)^(1-t) * vol(L)^t <= vol(logCombination K L t)`. That is the origin-symmetric
///   log-Brunn-Minkowski conjecture of Boroczky, Lutwak, Yang and Zhang (Adv. Math. 231, 2012).
///
/// How the volume is bounded. Keeping only N sampled directions gives a polygon A_N that CONTAINS
/// the Wulff body (fewer constraints), computed exactly as the polar of the hull of the points
/// u_j / f(u_j). Every point of A_N violates the full constraint set by at most
/// eps = (Lip_f + R_A) * chord, and the Wulff body of f + eps is inside (1 + eps/min f) times the
/// Wulff body of f, so `area(A_N) / (1 + eps/min f)^2` is a LOWER bound on the true area. A case
/// passes only if that lower bound reaches the left side. Doubles are not interval-controlled.
///
/// Controls that must fail: a non-symmetric pair (origin still inside, so every power is
/// defined) where even the OUTER area is below the left side, and a deliberately wrong
/// combination, `wulff(min(h_K, h_L)) = K cap L`. Equality cases (common-axis boxes, t = 0,
/// dilates) must NOT come out as a proved pass: the instrument has to be able to say "not proved".
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.logbm.LogBrunnMinkowski
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Interpolating shapes without losing volume.** The log combination is a way to blend two
///   symmetric convex shapes (tolerance zones, collision hulls, confidence ellipsoid-like regions)
///   whose result never has less volume than the geometric mean of the inputs. A geometry or
///   robotics library that morphs symmetric hulls could use it as a lower-bound guarantee, and the
///   Minkowski average as the upper one (Wulff of the geometric mean sits inside the Minkowski mean).
/// - **The symmetry check is load-bearing.** The non-symmetric control loses about 40 percent of the
///   promised area. Code that relies on the inequality must verify `x in K iff -x in K` (or
///   recentre) first; a body that merely contains the origin is not enough.
/// - **Polarity is a cheap Wulff-shape algorithm.** Intersecting N half-planes that all contain a
///   disk is the polar of a convex hull, so it costs one O(N log N) hull instead of N clippings.
///   Any 2D Java code that builds "intersection of support constraints" shapes can use this.
/// - **Certified-by-construction numerics.** Turning an outer approximation into a proven lower
///   bound with an explicit Lipschitz shrink factor is a pattern for any sampled geometric quantity
///   that a test must not over-claim; it is why the equality cases here report "not proved".
public class LogBrunnMinkowski {

    record P(double x, double y) {}

    static double cross(P o, P a, P b) { return (a.x() - o.x()) * (b.y() - o.y()) - (a.y() - o.y()) * (b.x() - o.x()); }

    static List<P> hull(List<P> in) {
        List<P> pts = new ArrayList<>(in);
        pts.sort(Comparator.comparingDouble(P::x).thenComparingDouble(P::y));
        int n = pts.size();
        P[] h = new P[2 * n];
        int k = 0;
        for (int i = 0; i < n; i++) {
            while (k >= 2 && cross(h[k - 2], h[k - 1], pts.get(i)) <= 0) k--;
            h[k++] = pts.get(i);
        }
        for (int i = n - 2, lo = k + 1; i >= 0; i--) {
            while (k >= lo && cross(h[k - 2], h[k - 1], pts.get(i)) <= 0) k--;
            h[k++] = pts.get(i);
        }
        return Arrays.asList(Arrays.copyOf(h, k - 1));
    }

    static double area(List<P> poly) {
        double s = 0;
        for (int i = 0; i < poly.size(); i++) {
            P a = poly.get(i), b = poly.get((i + 1) % poly.size());
            s += a.x() * b.y() - b.x() * a.y();
        }
        return Math.abs(s) / 2;
    }

    static double support(List<P> v, double ux, double uy) {
        double m = Double.NEGATIVE_INFINITY;
        for (P p : v) m = Math.max(m, p.x() * ux + p.y() * uy);
        return m;
    }

    static double inradius(List<P> v) {
        List<P> h = hull(v);
        double best = Double.POSITIVE_INFINITY;
        for (int i = 0; i < h.size(); i++) {
            P a = h.get(i), b = h.get((i + 1) % h.size());
            double nx = b.y() - a.y(), ny = a.x() - b.x();
            best = Math.min(best, Math.abs(nx * a.x() + ny * a.y()) / Math.hypot(nx, ny));
        }
        return best;
    }

    static double circumradius(List<P> v) {
        double m = 0;
        for (P p : v) m = Math.max(m, Math.hypot(p.x(), p.y()));
        return m;
    }

    /// A_N: the polygon cut out by N sampled constraints, via polarity.
    static List<P> wulffOuter(ToDoubleFunction<double[]> f, int n) {
        List<P> dual = new ArrayList<>(n);
        for (int j = 0; j < n; j++) {
            double a = 2 * Math.PI * j / n, ux = Math.cos(a), uy = Math.sin(a);
            double fu = f.applyAsDouble(new double[] {ux, uy});
            dual.add(new P(ux / fu, uy / fu));
        }
        List<P> h = hull(dual);
        List<P> out = new ArrayList<>(h.size());
        for (int i = 0; i < h.size(); i++) {
            P p = h.get(i), q = h.get((i + 1) % h.size());
            double det = p.x() * q.y() - q.x() * p.y();
            out.add(new P((q.y() - p.y()) / det, (p.x() - q.x()) / det));
        }
        return out;
    }

    /// {lowerBound, outerArea} for the Wulff body of f.
    static double[] wulffBounds(ToDoubleFunction<double[]> f, double minF, double lip, int n) {
        List<P> a = wulffOuter(f, n);
        double eps = (lip + circumradius(a)) * 2 * Math.sin(Math.PI / (2 * n));
        double outer = area(a);
        return new double[] {outer / Math.pow(1 + eps / minF, 2), outer};
    }

    static int passes, nearEq, controlsOk, failures;

    static void check(String name, List<P> k, List<P> l, double t, int n) {
        double lhs = Math.pow(area(hull(k)), 1 - t) * Math.pow(area(hull(l)), t);
        double mK = inradius(k), mL = inradius(l), rK = circumradius(k), rL = circumradius(l);
        double minF = Math.pow(mK, 1 - t) * Math.pow(mL, t), maxF = Math.pow(rK, 1 - t) * Math.pow(rL, t);
        double lip = maxF * ((1 - t) * rK / mK + t * rL / mL);
        double[] b = wulffBounds(u -> Math.pow(support(k, u[0], u[1]), 1 - t) * Math.pow(support(l, u[0], u[1]), t),
                minF, lip, n);
        String v;
        if (b[0] >= lhs) { v = "PASS (proved lower bound >= LHS)"; passes++; }
        else if (b[1] >= lhs * (1 - 1e-12)) { v = "NEAR-EQUALITY (not proved)"; nearEq++; }
        else { v = "FAIL"; failures++; }
        System.out.printf("%-44s t=%.2f LHS=%.6f vol in [%.6f, %.6f]  %s%n", name, t, lhs, b[0], b[1], v);
    }

    static void control(String name, List<P> k, List<P> l, double t, ToDoubleFunction<double[]> comb) {
        double lhs = Math.pow(area(hull(k)), 1 - t) * Math.pow(area(hull(l)), t);
        double outer = area(wulffOuter(comb, 20000));   // outer >= true volume
        boolean ok = outer < lhs;
        if (ok) controlsOk++; else failures++;
        System.out.printf("%-44s t=%.2f LHS=%.6f vol <= %.6f  %s%n", name, t, lhs, outer,
                ok ? "CONTROL FAILS AS REQUIRED" : "CONTROL DID NOT FAIL");
    }

    static List<P> rect(double a, double b, double cx, double cy) {
        return List.of(new P(cx - a, cy - b), new P(cx - a, cy + b), new P(cx + a, cy - b), new P(cx + a, cy + b));
    }

    static List<P> rot(List<P> v, double th) {
        double c = Math.cos(th), s = Math.sin(th);
        return v.stream().map(p -> new P(c * p.x() - s * p.y(), s * p.x() + c * p.y())).toList();
    }

    static List<P> regular(int k, double r) {
        List<P> v = new ArrayList<>();
        for (int i = 0; i < k; i++) v.add(new P(r * Math.cos(2 * Math.PI * i / k), r * Math.sin(2 * Math.PI * i / k)));
        return v;
    }

    static List<P> randomSymmetric(Random rng) {
        List<P> v = new ArrayList<>();
        int k = 2 + rng.nextInt(5);
        for (int i = 0; i < k; i++) {
            double a = rng.nextDouble() * Math.PI, r = 0.3 + 1.7 * rng.nextDouble();
            v.add(new P(r * Math.cos(a), r * Math.sin(a)));
            v.add(new P(-r * Math.cos(a), -r * Math.sin(a)));
        }
        return v;
    }

    public static void main(String[] args) {
        List<P> sq = rect(1, 1, 0, 0);
        int n = 20000;
        System.out.println("-- symmetric pairs (theorem's class)");
        check("square vs 45deg-rotated square", sq, rot(sq, Math.PI / 4), 0.5, n);
        check("rect 3x1 vs rotated 30deg", rect(1.5, .5, 0, 0), rot(rect(1.5, .5, 0, 0), Math.PI / 6), 0.3, n);
        check("square vs regular hexagon", sq, regular(6, 1), 0.5, n);
        check("thin rect vs rotated thin rect (60deg)", rect(2, .1, 0, 0), rot(rect(2, .1, 0, 0), Math.PI / 3), 0.5, 400000);
        Random rng = new Random(20261008L);
        for (int i = 0; i < 6; i++) check("random symmetric polygons #" + i, randomSymmetric(rng), randomSymmetric(rng),
                0.05 + 0.9 * rng.nextDouble(), n);
        System.out.println("-- equality cases (must NOT be reported as proved)");
        check("common-axis rects 2x0.5 vs 0.5x2", rect(1, .25, 0, 0), rect(.25, 1, 0, 0), 0.5, n);
        check("t=0", sq, rot(sq, .4), 0.0, n);
        check("dilates hexagon, 3*hexagon", regular(6, 1), regular(6, 3), 0.5, n);
        System.out.println("-- controls (must fail)");
        List<P> shifted = rect(1, 1, .95, .95);
        control("NONSYM: square vs square shifted (.95,.95)", sq, shifted, 0.5,
                u -> Math.sqrt(support(sq, u[0], u[1]) * support(shifted, u[0], u[1])));
        List<P> k = rect(1, .25, 0, 0), l = rect(.25, 1, 0, 0);
        control("WRONG COMB: wulff(min(h_K,h_L)) = K cap L", k, l, 0.5,
                u -> Math.min(support(k, u[0], u[1]), support(l, u[0], u[1])));
        System.out.printf("%nproved passes=%d, near-equality (not proved)=%d, controls failing as required=%d/2, failures=%d%n",
                passes, nearEq, controlsOk, failures);
        if (failures != 0 || controlsOk != 2 || nearEq != 3) throw new AssertionError("unexpected outcome");
    }
}
