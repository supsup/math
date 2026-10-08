package confluence.math.planecoloring;

import java.util.SplittableRandom;
import java.util.function.IntBinaryOperator;

/// Java replication of OAI.Problem160.properColoring_seven
/// (lean/ComparatorChallenges/PlaneColoring.lean): there is a colouring c of the plane with 7
/// colours such that any two points at distance EXACTLY 1 get different colours.
///
/// The Lean solution (lean/OAI/Geometry/PlaneColoring/Seven.lean and its imports) builds it from:
///
/// - centres `triangularLattice a b = (4/5) * (a + b/2, (sqrt3/2) * b)`, a triangular lattice with
///   nearest-neighbour spacing 4/5;
/// - colours `colorFin a b = (a + 3b) mod 7`;
/// - each point x takes the colour of SOME centre within r = 7/15 of it, chosen with `choose`
///   (Classical.choice). Lean never says which one. The proof shows every such choice works:
///   one cell has diameter at most 2r = 14/15 < 1, and two distinct same-coloured centres are
///   at least (4/5)*sqrt7 = 2.117 apart, more than 1 + 2r = 1.933.
///
/// So this class tests the ADMISSIBLE COLOUR SETS: for a unit pair (p, q), no colour may be
/// admissible at both ends. That covers every possible selector, including Lean's opaque one. It
/// also runs the hexagonal (nearest-centre) tiling, which is what the floor-based witness in the
/// proof of `triangular_lattice_cover` produces, and negative controls that must be caught.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.planecoloring.PlaneColoring
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper or the Lean proof.
///
/// - **"Any choice works" is a testable contract.** The Lean colouring is defined through an
///   arbitrary choice, and the proof is valid for every choice. A Java method that resolves ties
///   (a point on a cell boundary, a key hashing to a bucket edge) can be tested the same way: test
///   the SET of allowed answers, not the one your implementation happens to return, so the test
///   survives a change of tie-break rule.
/// - **Slack turns floating-point boundary bugs into non-issues.** The construction has a margin of
///   about 0.18 on both sides (cells of diameter 0.924 against 1; same-colour cells at least 1.18
///   apart). Code that assigns a point to a nearby cell with `double` arithmetic can never be wrong
///   by more than rounding error, so no unit pair can be misjudged. When designing a spatial
///   partition in Java, choosing parameters with such a margin is cheaper than exact arithmetic.
/// - **Frequency or channel assignment on a hexagonal grid.** The rule (a + 3b) mod 7 is the
///   classic 7-cell reuse pattern: any two cells sharing a colour are at least sqrt7 lattice steps
///   apart. A Java planner that hands out 7 channels, locks or shard IDs to hexagonal tiles so that
///   neighbours never collide can use this rule and check it the way `main` does.
/// - **A negative control belongs next to every randomized property test.** The 1,000,000-pair
///   test here would also print zero violations if the checker were broken. The four wrong
///   colourings below exist to prove the checker can fail; a jqwik or JUnit property test should
///   carry such a deliberately broken input too.
public class PlaneColoring {

    static final double S3 = Math.sqrt(3.0);
    static final double R = 7.0 / 15.0;
    static final long SEED = 20261008L;

    /// A lattice colouring: spacing d, colour rule (a, b) -> int mod k, admissible radius r.
    record Scheme(String name, double d, IntBinaryOperator rule, int k, double r) {
        double cx(long a, long b) { return d * (a + b / 2.0); }
        double cy(long b) { return d * (S3 / 2.0) * b; }
        int colour(long a, long b) { return Math.floorMod(rule.applyAsInt((int) a, (int) b), k); }

        /// Bitmask of colours whose centre is within r of (x, y); -1 if NO centre is (cover fails).
        int admissible(double x, double y) {
            long b0 = Math.round(y / (d * S3 / 2.0));
            long a0 = Math.round(x / d - b0 / 2.0);
            int mask = 0;
            for (long a = a0 - 2; a <= a0 + 2; a++)
                for (long b = b0 - 2; b <= b0 + 2; b++)
                    if (Math.hypot(x - cx(a, b), y - cy(b)) <= r) mask |= 1 << colour(a, b);
            return mask == 0 ? -1 : mask;
        }

        /// Colour of the nearest centre (the hexagonal tiling); ties go to the first found.
        int nearest(double x, double y) {
            long b0 = Math.round(y / (d * S3 / 2.0));
            long a0 = Math.round(x / d - b0 / 2.0);
            double best = Double.MAX_VALUE;
            int col = -1;
            for (long a = a0 - 2; a <= a0 + 2; a++)
                for (long b = b0 - 2; b <= b0 + 2; b++) {
                    double dd = Math.hypot(x - cx(a, b), y - cy(b));
                    if (dd < best) { best = dd; col = colour(a, b); }
                }
            return col;
        }
    }

    static final Scheme LEAN = new Scheme("lean (d=4/5, a+3b mod 7, r=7/15)", 0.8, (a, b) -> a + 3 * b, 7, R);

    /// The witness in the proof of Covering.triangular_lattice_cover, applied to (5/4) x as Seven.lean
    /// does. Lean's `choose` is NOT pinned to this witness; it is one valid selector. Returns {m, n}.
    static long[] floorWitness(double px, double py) {
        double x = 1.25 * px, y = 1.25 * py;
        long n = (long) Math.floor(2 * y / S3);
        long m = (long) Math.floor(x - n / 2.0);
        double u = x - (m + n / 2.0), v = y - S3 * n / 2.0;
        if (u <= 0.5) return S3 * v <= 1 - u ? new long[] {m, n} : new long[] {m, n + 1};
        return S3 * v <= u ? new long[] {m + 1, n} : new long[] {m, n + 1};
    }

    // ------------------------------------------------------------- exact side conditions
    /// a/b <= c/d for positive denominators, in exact long arithmetic.
    static boolean le(long a, long b, long c, long d) { return a * d <= c * b; }

    static boolean exactConditions() {
        boolean ok = true;
        // cover: (4/5)^2 * (1/3) = 16/75 <= (7/15)^2 = 49/225
        ok &= report("cover 16/75 <= 49/225", le(16, 75, 49, 225));
        // diameter: 2r = 14/15 < 1
        ok &= report("hdiam 14/15 < 1", 14 < 15);
        // separation: (16/25)*7 = 112/25 > (29/15)^2 = 841/225
        ok &= report("sep 112/25 > 841/225", !le(112, 25, 841, 225));
        int min = Integer.MAX_VALUE;
        for (int a = -30; a <= 30; a++)
            for (int b = -30; b <= 30; b++)
                if ((a != 0 || b != 0) && Math.floorMod(a + 3 * b, 7) == 0) min = Math.min(min, a * a + a * b + b * b);
        ok &= report("min a^2+ab+b^2 over same-colour offsets (|a|,|b|<=30) = " + min + " >= 7", min >= 7);
        return ok;
    }

    static boolean report(String what, boolean v) {
        System.out.println("  " + (v ? "OK  " : "BAD ") + what);
        return v;
    }

    // ------------------------------------------------------------- point generators
    static double[] unitPair(SplittableRandom rnd) {
        double px = rnd.nextDouble(-50, 50), py = rnd.nextDouble(-50, 50), t = rnd.nextDouble(0, 2 * Math.PI);
        return new double[] {px, py, px + Math.cos(t), py + Math.sin(t)};
    }

    /// A point within 1e-9 of a hexagon vertex, a hexagon edge, or a circle of radius 7/15.
    static double[] boundaryPoint(SplittableRandom rnd) {
        double d = 0.8;
        long a = rnd.nextInt(-40, 40), b = rnd.nextInt(-40, 40);
        double cx = LEAN.cx(a, b), cy = LEAN.cy(b), j = rnd.nextDouble(-1e-9, 1e-9);
        int kind = rnd.nextInt(3);
        double rad, ang, slide = 0;
        if (kind == 0) { rad = d / S3; ang = Math.PI / 6 + Math.PI / 3 * rnd.nextInt(6); }
        else if (kind == 1) { rad = d / 2; ang = Math.PI / 3 * rnd.nextInt(6); slide = rnd.nextDouble(-1, 1) * d / (2 * S3); }
        else { rad = R; ang = rnd.nextDouble(0, 2 * Math.PI); }
        rad += j;
        return new double[] {cx + rad * Math.cos(ang) - slide * Math.sin(ang), cy + rad * Math.sin(ang) + slide * Math.cos(ang)};
    }

    static double[] boundaryPair(SplittableRandom rnd, int i) {
        double[] p = boundaryPoint(rnd);
        double ux, uy;
        if (i % 4 == 0) { double t = rnd.nextInt(12) * Math.PI / 6; ux = Math.cos(t); uy = Math.sin(t); }
        else if (i % 2 == 0) { double t = rnd.nextDouble(0, 2 * Math.PI); ux = Math.cos(t); uy = Math.sin(t); }
        else {   // aim at another boundary point, so both ends sit on boundaries more often
            double[] v = boundaryPoint(rnd);
            double nx = v[0] - p[0], ny = v[1] - p[1], nn = Math.hypot(nx, ny);
            if (nn == 0) { nx = 1; ny = 0; nn = 1; }
            ux = nx / nn; uy = ny / nn;
        }
        return new double[] {p[0], p[1], p[0] + ux, p[1] + uy};
    }

    // ------------------------------------------------------------- main
    public static void main(String[] args) {
        boolean ok = true;
        System.out.println("== exact side conditions (long arithmetic)");
        ok &= exactConditions();

        SplittableRandom rnd = new SplittableRandom(SEED);
        int n = 1_000_000, admBad = 0, nearBad = 0, multi = 0;
        for (int i = 0; i < n; i++) {
            double[] pq = unitPair(rnd);
            int mp = LEAN.admissible(pq[0], pq[1]), mq = LEAN.admissible(pq[2], pq[3]);
            if (mp < 0 || mq < 0) throw new AssertionError("cover failed at " + pq[0] + "," + pq[1]);
            if ((mp & mq) != 0) admBad++;
            if (Integer.bitCount(mp) > 1) multi++;
            if (Integer.bitCount(mq) > 1) multi++;
            if (LEAN.nearest(pq[0], pq[1]) == LEAN.nearest(pq[2], pq[3])) nearBad++;
        }
        System.out.printf("%n== (a) dense random test, %,d unit pairs in [-50,50]^2, seed %d%n", n, SEED);
        System.out.printf("  admissible-set conflicts (ANY choice of cell): %d%n", admBad);
        System.out.printf("  nearest-centre (hexagon) conflicts:            %d%n", nearBad);
        System.out.printf("  endpoints with >1 admissible colour: %,d of %,d%n", multi, 2 * n);
        ok &= admBad == 0 && nearBad == 0;

        int nb = 400_000, bAdm = 0, bNear = 0, bMulti = 0;
        for (int i = 0; i < nb; i++) {
            double[] pq = boundaryPair(rnd, i);
            int mp = LEAN.admissible(pq[0], pq[1]), mq = LEAN.admissible(pq[2], pq[3]);
            if ((mp & mq) != 0) bAdm++;
            if (Integer.bitCount(mp) > 1) bMulti++;
            if (Integer.bitCount(mq) > 1) bMulti++;
            if (LEAN.nearest(pq[0], pq[1]) == LEAN.nearest(pq[2], pq[3])) bNear++;
        }
        System.out.printf("%n== (b) boundary-targeted test, %,d pairs (an endpoint within 1e-9 of an edge, vertex or r-circle)%n", nb);
        System.out.printf("  admissible-set conflicts: %d; nearest-centre conflicts: %d%n", bAdm, bNear);
        System.out.printf("  endpoints with >1 admissible colour: %,d of %,d%n", bMulti, 2 * nb);
        ok &= bAdm == 0 && bNear == 0;

        int nf = 200_000, fBad = 0;
        double worst = 0;
        for (int i = 0; i < nf; i++) {
            double[] pq = i % 2 == 0 ? unitPair(rnd) : boundaryPair(rnd, i);
            long[] w1 = floorWitness(pq[0], pq[1]), w2 = floorWitness(pq[2], pq[3]);
            worst = Math.max(worst, Math.hypot(pq[0] - LEAN.cx(w1[0], w1[1]), pq[1] - LEAN.cy(w1[1])));
            worst = Math.max(worst, Math.hypot(pq[2] - LEAN.cx(w2[0], w2[1]), pq[3] - LEAN.cy(w2[1])));
            if (LEAN.colour(w1[0], w1[1]) == LEAN.colour(w2[0], w2[1])) fBad++;
        }
        System.out.printf("%n== floor-witness selector (proof of triangular_lattice_cover), %,d pairs (half boundary)%n", nf);
        System.out.printf("  conflicts: %d; max distance to chosen centre %.15f (bound 7/15 = %.15f)%n", fBad, worst, R);
        ok &= fBad == 0 && worst <= R;

        System.out.println("\n== (c) negative controls: wrong colourings that MUST be caught");
        Scheme[] nearestControls = {
            new Scheme("spacing 1.0 (hexagon diameter 1.155 > 1)", 1.0, (a, b) -> a + 3 * b, 7, 0),
            new Scheme("spacing 0.6 (same-colour hexagons too close)", 0.6, (a, b) -> a + 3 * b, 7, 0),
            new Scheme("rule a+b mod 7 (neighbours share colours)", 0.8, (a, b) -> a + b, 7, 0),
            new Scheme("6 colours a+3b mod 6", 0.8, (a, b) -> a + 3 * b, 6, 0),
        };
        for (Scheme s : nearestControls) ok &= control(s, false, rnd);
        ok &= control(new Scheme("admissible r = 0.55 (2r > 1)", 0.8, (a, b) -> a + 3 * b, 7, 0.55), true, rnd);
        ok &= control(new Scheme("admissible r = 7/15, rule a+b mod 7", 0.8, (a, b) -> a + b, 7, R), true, rnd);

        System.out.println("\nRESULT: " + (ok ? "ALL CHECKS PASSED, ALL CONTROLS FIRED" : "SOMETHING FAILED"));
        if (!ok) System.exit(1);
    }

    static boolean control(Scheme s, boolean admissible, SplittableRandom rnd) {
        int bad = 0;
        double[] first = null;
        for (int i = 0; i < 200_000; i++) {
            double[] pq = unitPair(rnd);
            boolean clash = admissible
                ? (s.admissible(pq[0], pq[1]) & s.admissible(pq[2], pq[3])) > 0
                : s.nearest(pq[0], pq[1]) == s.nearest(pq[2], pq[3]);
            if (clash) { bad++; if (first == null) first = pq; }
        }
        System.out.printf("  CONTROL %s [%s]: %,d violating pairs of 200,000%n", s.name(), admissible ? "admissible" : "nearest", bad);
        if (first == null) { System.out.println("    CONTROL FAILED TO FIRE"); return false; }
        System.out.printf("    e.g. p=(%.12f, %.12f) q=(%.12f, %.12f) |p-q|=%.15f%s%n", first[0], first[1], first[2], first[3],
            Math.hypot(first[2] - first[0], first[3] - first[1]),
            admissible ? "" : "  colour " + s.nearest(first[0], first[1]) + " == " + s.nearest(first[2], first[3]));
        return true;
    }
}
