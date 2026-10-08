package confluence.math.sidorenko;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.TreeMap;

/// The pattern graph H from "A counterexample to Sidorenko's conjecture" (OpenAI, 2026-09-23),
/// and a small experiment with it.
///
/// Sidorenko's conjecture: for every bipartite H with at least one edge and every graph (or
/// nonnegative kernel) W, t(H, W) >= (E W)^|E(H)|. The paper's H is the incidence graph of 22
/// triples on 13 points; it has 66 edges, so the bound is (E W)^66.
///
/// Part 1 checks H's stated structure from the paper's own table (including the table's
/// "opposite face" columns, which state each pair's partner face independently of the triples).
/// Part 2 computes t(H, W) / (E W)^66 EXACTLY for tiny bipartite kernels and searches for the
/// minimum. The paper's violation needs a large construction, so this is expected to stay >= 1.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.sidorenko.SidorenkoPattern
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper. Everything rests on the
/// paper's theorem, which I have NOT verified: I checked H's structure, not the inequality.
///
/// - **"A random graph has the fewest copies" stops being a safe default.** Sidorenko's
///   conjecture was the intuition that, at a fixed edge density, a random graph minimizes the
///   count of every bipartite pattern. Java code for graph anomaly detection, property testing
///   or synthetic graph generation sometimes leans on that intuition, for example by treating
///   "fewer pattern copies than random" as impossible. If the paper is right, that is false for
///   at least one 66-edge pattern, so such a rule needs to be checked per pattern, not assumed.
/// - **Homomorphism counting is cheap when the pattern has structure.** `logRatio` counts all
///   maps of a 35-vertex pattern into a kernel by fixing the 13 point labels first, which makes
///   the 22 faces independent. The cost is a^13 instead of a^35. The same trick (condition on
///   a vertex cover, then the rest factor) is how a Java graph library could count pattern
///   occurrences in a weighted graph without enumerating everything.
/// - **Work in logs for tiny probabilities.** The bound (E W)^66 underflows a `double` long
///   before anything interesting happens. Summing `exp(t - max)` and adding back `max` (the
///   log-sum-exp trick) keeps the ratio exact enough to compare with 1.
/// - **A structured test fixture.** The 13-point, 22-triple table, where every covered pair lies
///   in exactly two faces, is a small, fully specified hypergraph. It's a good input for testing
///   Java hypergraph or incidence-graph code, and `checkStructure` already states its invariants.
public class SidorenkoPattern {

    /// {i1, i2, i3, j12, j13, j23}: the three points of face j, then the other face containing
    /// each pair {i1,i2}, {i1,i3}, {i2,i3}. Transcribed from the paper's Table tab:complex.
    static final int[][] TABLE = {
        {0, 1, 3, 1, 2, 4}, {0, 1, 9, 0, 3, 7}, {0, 2, 3, 3, 0, 8}, {0, 2, 9, 2, 1, 9},
        {1, 3, 10, 0, 5, 11}, {1, 7, 10, 6, 4, 16}, {1, 7, 12, 5, 7, 18}, {1, 9, 12, 1, 6, 21},
        {2, 3, 4, 2, 9, 10}, {2, 4, 9, 8, 3, 12}, {3, 4, 11, 8, 11, 13}, {3, 10, 11, 4, 10, 17},
        {4, 8, 9, 13, 9, 21}, {4, 8, 11, 12, 10, 19}, {5, 6, 7, 15, 16, 18}, {5, 6, 11, 14, 17, 19},
        {5, 7, 10, 14, 17, 5}, {5, 10, 11, 16, 15, 11}, {6, 7, 12, 14, 20, 6}, {6, 8, 11, 20, 15, 13},
        {6, 8, 12, 19, 18, 21}, {8, 9, 12, 12, 20, 7},
    };

    static final int POINTS = 13;
    static final int FACES = TABLE.length;
    static final int EDGES = 66;

    // ---------------------------------------------------------------- part 1: structure

    static void checkStructure() {
        Set<Integer> points = new HashSet<>();
        Map<Integer, List<Integer>> adj = new HashMap<>(); // vertices: points 0..12, faces 100..121
        int edges = 0;
        for (int j = 0; j < FACES; j++) {
            for (int a = 0; a < 3; a++) {
                int p = TABLE[j][a];
                points.add(p);
                adj.computeIfAbsent(p, k -> new ArrayList<>()).add(100 + j);
                adj.computeIfAbsent(100 + j, k -> new ArrayList<>()).add(p);
                edges++;
            }
        }
        System.out.printf("points %d (claim 13), faces %d (claim 22), H vertices %d (claim 35), edges %d (claim 66)%n",
            points.size(), FACES, adj.size(), edges);

        Set<Integer> seen = new HashSet<>();
        ArrayDeque<Integer> stack = new ArrayDeque<>(List.of(0));
        while (!stack.isEmpty()) {
            int v = stack.pop();
            if (seen.add(v)) stack.addAll(adj.get(v));
        }
        System.out.println("connected: " + (seen.size() == adj.size()));

        Map<Long, List<Integer>> pairFaces = new HashMap<>();
        for (int j = 0; j < FACES; j++) {
            int[] t = TABLE[j];
            for (int[] pr : new int[][] {{t[0], t[1]}, {t[0], t[2]}, {t[1], t[2]}}) {
                pairFaces.computeIfAbsent(key(pr[0], pr[1]), k -> new ArrayList<>()).add(j);
            }
        }
        Map<Integer, Integer> histogram = new TreeMap<>();
        pairFaces.values().forEach(fs -> histogram.merge(fs.size(), 1, Integer::sum));
        System.out.printf("distinct pairs %d (claim 33), multiplicity histogram %s (claim: every pair twice)%n",
            pairFaces.size(), histogram);

        int mismatches = 0;
        for (int j = 0; j < FACES; j++) {
            int[] t = TABLE[j];
            int[][] pairs = {{t[0], t[1], t[3]}, {t[0], t[2], t[4]}, {t[1], t[2], t[5]}};
            for (int[] pc : pairs) {
                List<Integer> others = new ArrayList<>(pairFaces.get(key(pc[0], pc[1])));
                others.remove(Integer.valueOf(j));
                if (!(others.size() == 1 && others.get(0) == pc[2])) mismatches++;
            }
        }
        System.out.println("opposite-face column mismatches: " + mismatches + " of 66");
    }

    static long key(int a, int b) { return (long) Math.min(a, b) * 1000 + Math.max(a, b); }

    // ---------------------------------------------------------------- part 2: tiny kernels

    /// log( t(H,W) / (E W)^66 ) for kernel W (a x b), point weights mu, face weights nu.
    /// With the 13 point labels fixed, the 22 faces are independent, so
    /// t(H,W) = sum_x prod_i mu[x_i] * prod_faces g[x_p][x_q][x_r],
    /// g[u][v][w] = sum_y nu[y] W[u][y] W[v][y] W[w][y]. Computed in logs (the bound is tiny).
    static double logRatio(double[][] w, double[] mu, double[] nu) {
        int a = w.length, b = w[0].length;
        double[][][] logG = new double[a][a][a];
        for (int u = 0; u < a; u++) for (int v = 0; v < a; v++) for (int x = 0; x < a; x++) {
            double s = 0;
            for (int y = 0; y < b; y++) s += nu[y] * w[u][y] * w[v][y] * w[x][y];
            logG[u][v][x] = Math.log(s);
        }
        double mean = 0;
        for (int u = 0; u < a; u++) for (int y = 0; y < b; y++) mean += mu[u] * w[u][y] * nu[y];

        int total = (int) Math.pow(a, POINTS);
        int[] label = new int[POINTS];
        double max = Double.NEGATIVE_INFINITY;
        double[] terms = new double[total];
        for (int n = 0; n < total; n++) {
            int m = n;
            double t = 0;
            for (int i = 0; i < POINTS; i++) { label[i] = m % a; m /= a; t += Math.log(mu[label[i]]); }
            for (int[] face : TABLE) t += logG[label[face[0]]][label[face[1]]][label[face[2]]];
            terms[n] = t;
            if (t > max) max = t;
        }
        double sum = 0;
        for (double t : terms) sum += Math.exp(t - max);
        return max + Math.log(sum) - EDGES * Math.log(mean);
    }

    static double[] normalized(Random rng, int n) {
        double[] p = new double[n];
        double s = 0;
        for (int i = 0; i < n; i++) { p[i] = rng.nextDouble() + 1e-3; s += p[i]; }
        for (int i = 0; i < n; i++) p[i] /= s;
        return p;
    }

    static void searchTinyKernels(int a, int b, int trials, int steps, long seed) {
        Random rng = new Random(seed);
        double best = Double.POSITIVE_INFINITY;
        double[][] bw = null;
        double[] bmu = null, bnu = null;
        for (int t = 0; t < trials; t++) {
            double[][] w = new double[a][b];
            for (double[] row : w) for (int y = 0; y < b; y++) row[y] = rng.nextDouble();
            double[] mu = normalized(rng, a), nu = normalized(rng, b);
            double r = logRatio(w, mu, nu);
            if (r < best) { best = r; bw = w; bmu = mu; bnu = nu; }
        }
        for (int s = 0; s < steps; s++) {
            double[][] w = new double[a][b];
            for (int u = 0; u < a; u++) for (int y = 0; y < b; y++)
                w[u][y] = Math.min(1.0, Math.max(1e-6, bw[u][y] + 0.05 * rng.nextGaussian()));
            double[] mu = perturb(rng, bmu), nu = perturb(rng, bnu);
            double r = logRatio(w, mu, nu);
            if (r < best) { best = r; bw = w; bmu = mu; bnu = nu; }
        }
        System.out.printf("a=%d b=%d: min ratio t(H,W)/(EW)^66 found = %.6f%n", a, b, Math.exp(best));
    }

    static double[] perturb(Random rng, double[] p) {
        double[] q = new double[p.length];
        double s = 0;
        for (int i = 0; i < p.length; i++) { q[i] = Math.max(1e-4, p[i] + 0.05 * rng.nextGaussian()); s += q[i]; }
        for (int i = 0; i < p.length; i++) q[i] /= s;
        return q;
    }

    public static void main(String[] args) {
        checkStructure();
        double[] half = {0.5, 0.5};
        System.out.printf("control: constant kernel log-ratio (expect 0): %+.2e%n",
            logRatio(new double[][] {{0.37, 0.37}, {0.37, 0.37}}, half, half));
        searchTinyKernels(2, 2, 400, 3000, 22);
        searchTinyKernels(2, 3, 300, 3000, 23);
        searchTinyKernels(2, 4, 200, 2000, 24);
    }
}
