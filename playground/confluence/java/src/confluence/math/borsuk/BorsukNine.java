package confluence.math.borsuk;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/// Java replication of the DEFINITIONS behind OAI.BorsukNine.main_theorem
/// (lean/ComparatorChallenges/BorsukNine.lean).
///
/// The theorem says: the set X of rank-one projectors u u^T (u a unit vector in R^4), with the
/// Frobenius metric, is compact, lies in the trace-one symmetric matrices (a 9-dimensional affine
/// space), has diameter sqrt 2, and cannot be covered by ten sets of diameter strictly less than
/// sqrt 2. So Borsuk's covering assertion fails in dimension nine. The covering obstruction is
/// topological (an odd map, mod-two degree and finite cases, per the preprint), and Java cannot
/// replicate a statement quantified over all ten-set covers of a continuum. What Java CAN check:
///
/// - the distance identity |u u^T - v v^T|_F^2 = 2 - 2 <u,v>^2, so the distance depends only on the
///   angle between the LINES (u and -u give the same projector), and the diameter sqrt 2 is
///   reached exactly at orthogonal lines;
/// - every projector is symmetric with trace 1, and the projectors' affine span is 9-dimensional
///   (rank of differences, by exact elimination on sampled points), so "dimension nine" is right;
/// - for a FINITE set of lines, a piece has diameter below sqrt 2 exactly when it holds no
///   orthogonal pair, so the fewest small pieces is the chromatic number of the orthogonality graph.
///   For Peres' 24 Kochen-Specker rays that number is computed exactly below. It is far below 11,
///   which shows why the theorem needs the full compact set and not a finite configuration of this
///   kind.
///
/// Controls: a wrong identity (2 - 2|<u,v>|) is refuted by the same samples; a non-orthogonal
/// pair never reaches sqrt 2; and the chromatic-number search is checked on K4 (needs 4) and an
/// orthogonal basis plus its negatives (still 4, because -u is the same line).
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.borsuk.BorsukNine
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Compare lines, not vectors, without building matrices.** Whenever direction matters but sign
///   does not (surface normals, principal axes, eigenvectors from a solver that returns either sign,
///   fibre orientations in imaging), the projector distance sqrt(2 - 2<u,v>^2) is a true metric on
///   lines that needs one dot product. It avoids the classic bug of clustering u and -u apart.
/// - **Clustering lines has a hard floor.** Any scheme that splits sign-free directions in R^4 into
///   buckets "smaller than the whole set" (for indexing, quantisation or load balancing) must use at
///   least 11 buckets if every bucket is to have diameter below sqrt 2 in this metric. A design with
///   10 buckets cannot keep orthogonal-ish lines apart everywhere, no matter how clever.
/// - **A finite test is not the continuum.** The Peres computation is the cautionary unit test:
///   a finite sample can make a covering look easy (here 5 or so pieces suffice) while the full set
///   needs at least 11. Property tests over sampled directions can certify an UPPER bound on what a
///   bucketing needs, never this kind of lower bound.
public class BorsukNine {

    static int failures = 0;

    static void check(String name, boolean ok) {
        System.out.println((ok ? "ok   " : "FAIL ") + name);
        if (!ok) failures++;
    }

    // ---- Lean definitions, transcribed ----
    /// projector u = fun (i, j) => u i * u j, the matrix u u^T as a 16-vector.
    static double[] projector(double[] u) {
        double[] m = new double[16];
        for (int i = 0; i < 4; i++)
            for (int j = 0; j < 4; j++) m[4 * i + j] = u[i] * u[j];
        return m;
    }

    static double dist2(double[] a, double[] b) {
        double s = 0;
        for (int k = 0; k < a.length; k++) s += (a[k] - b[k]) * (a[k] - b[k]);
        return s;
    }

    static double dot(double[] u, double[] v) {
        double s = 0;
        for (int k = 0; k < u.length; k++) s += u[k] * v[k];
        return s;
    }

    static double[] unit(double[] u) {
        double n = Math.sqrt(dot(u, u));
        double[] r = new double[u.length];
        for (int k = 0; k < u.length; k++) r[k] = u[k] / n;
        return r;
    }

    static double[] gaussUnit(Random rnd) {
        double[] u = new double[4];
        for (int k = 0; k < 4; k++) u[k] = rnd.nextGaussian();
        return unit(u);
    }

    /// traceOneSymmetric: A (i,j) = A (j,i) and sum_i A (i,i) = 1.
    static boolean traceOneSymmetric(double[] a, double tol) {
        double tr = 0;
        for (int i = 0; i < 4; i++) {
            tr += a[5 * i];
            for (int j = 0; j < 4; j++) if (Math.abs(a[4 * i + j] - a[4 * j + i]) > tol) return false;
        }
        return Math.abs(tr - 1) <= tol;
    }

    /// Rank of a list of vectors by Gaussian elimination with partial pivoting.
    static int rank(List<double[]> rows, double tol) {
        double[][] m = rows.stream().map(double[]::clone).toArray(double[][]::new);
        int r = 0, cols = m.length == 0 ? 0 : m[0].length;
        for (int c = 0; c < cols && r < m.length; c++) {
            int piv = r;
            for (int i = r; i < m.length; i++) if (Math.abs(m[i][c]) > Math.abs(m[piv][c])) piv = i;
            if (Math.abs(m[piv][c]) < tol) continue;
            double[] t = m[r]; m[r] = m[piv]; m[piv] = t;
            for (int i = 0; i < m.length; i++) {
                if (i == r) continue;
                double f = m[i][c] / m[r][c];
                for (int k = c; k < cols; k++) m[i][k] -= f * m[r][k];
            }
            r++;
        }
        return r;
    }

    // ---- finite pieces: chromatic number of the orthogonality graph ----
    static boolean[][] orthogonality(List<double[]> lines) {
        int n = lines.size();
        boolean[][] adj = new boolean[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                adj[i][j] = i != j && Math.abs(dot(lines.get(i), lines.get(j))) < 1e-12;
        return adj;
    }

    static boolean colourable(boolean[][] adj, int k, int[] col, int v) {
        if (v == adj.length) return true;
        for (int c = 0; c < k; c++) {
            boolean okc = true;
            for (int w = 0; w < v && okc; w++) if (adj[v][w] && col[w] == c) okc = false;
            if (!okc) continue;
            col[v] = c;
            if (colourable(adj, k, col, v + 1)) return true;
            if (c > maxUsed(col, v)) break; // symmetry: a fresh colour is as good as any other fresh one
        }
        col[v] = -1;
        return false;
    }

    static int maxUsed(int[] col, int v) {
        int m = -1;
        for (int w = 0; w < v; w++) m = Math.max(m, col[w]);
        return m;
    }

    static int chromatic(boolean[][] adj) {
        for (int k = 1; k <= adj.length; k++) {
            int[] col = new int[adj.length];
            java.util.Arrays.fill(col, -1);
            if (colourable(adj, k, col, 0)) return k;
        }
        return adj.length;
    }

    /// Peres' 24 rays in R^4: the 4 axes, the 12 lines (e_i +- e_j)/sqrt2, and the 8 lines (1,+-1,+-1,+-1)/2.
    static List<double[]> peres24() {
        List<double[]> rays = new ArrayList<>();
        for (int i = 0; i < 4; i++) { double[] u = new double[4]; u[i] = 1; rays.add(u); }
        for (int i = 0; i < 4; i++)
            for (int j = i + 1; j < 4; j++)
                for (int s = -1; s <= 1; s += 2) { double[] u = new double[4]; u[i] = 1; u[j] = s; rays.add(unit(u)); }
        for (int s1 = -1; s1 <= 1; s1 += 2)
            for (int s2 = -1; s2 <= 1; s2 += 2)
                for (int s3 = -1; s3 <= 1; s3 += 2) rays.add(unit(new double[]{1, s1, s2, s3}));
        return rays;
    }

    public static void main(String[] args) {
        Random rnd = new Random(20261009L);

        // 1. distance identity, and the wrong identity as a control
        double worst = 0, worstWrong = 0, maxD2 = 0;
        for (int t = 0; t < 20000; t++) {
            double[] u = gaussUnit(rnd), v = gaussUnit(rnd);
            double d2 = dist2(projector(u), projector(v)), ip = dot(u, v);
            worst = Math.max(worst, Math.abs(d2 - (2 - 2 * ip * ip)));
            worstWrong = Math.max(worstWrong, Math.abs(d2 - (2 - 2 * Math.abs(ip))));
            maxD2 = Math.max(maxD2, d2);
        }
        check("distance identity |uu^T - vv^T|^2 = 2 - 2<u,v>^2 (worst error " + worst + ")", worst < 1e-12);
        check("control: the wrong identity 2 - 2|<u,v>| is refuted (worst gap " + worstWrong + ")", worstWrong > 0.1);
        check("sampled squared distances never exceed 2 (max " + maxD2 + ")", maxD2 <= 2 + 1e-12);

        // 2. the diameter is attained exactly at orthogonal lines; u and -u give the same projector
        double[] e1 = {1, 0, 0, 0}, e2 = {0, 1, 0, 0};
        check("orthogonal lines are at distance sqrt 2", Math.abs(dist2(projector(e1), projector(e2)) - 2) < 1e-15);
        double[] m1 = {-1, 0, 0, 0};
        check("u and -u give the same projector", dist2(projector(e1), projector(m1)) == 0);
        double[] tilt = unit(new double[]{1, 1e-3, 0, 0});
        check("control: a non-orthogonal pair stays below sqrt 2", dist2(projector(tilt), projector(e2)) < 2);

        // 3. trace-one symmetric, and the affine span is 9-dimensional
        List<double[]> diffs = new ArrayList<>();
        double[] p0 = projector(gaussUnit(rnd));
        boolean allIn = traceOneSymmetric(p0, 1e-12);
        for (int t = 0; t < 40; t++) {
            double[] p = projector(gaussUnit(rnd));
            allIn &= traceOneSymmetric(p, 1e-12);
            double[] d = new double[16];
            for (int k = 0; k < 16; k++) d[k] = p[k] - p0[k];
            diffs.add(d);
        }
        check("every sampled projector is symmetric with trace 1", allIn);
        int dim = rank(diffs, 1e-9);
        check("affine span of the projectors has dimension 9 (measured " + dim + ")", dim == 9);

        // 4. finite pieces: chromatic number of orthogonality graphs
        boolean[][] k4 = orthogonality(List.of(e1, e2, new double[]{0, 0, 1, 0}, new double[]{0, 0, 0, 1}));
        check("control: an orthogonal basis needs 4 pieces", chromatic(k4) == 4);
        boolean[][] k4neg = orthogonality(List.of(e1, e2, new double[]{0, 0, 1, 0}, new double[]{0, 0, 0, 1}, m1));
        check("control: adding -e1 (the same line) still needs 4", chromatic(k4neg) == 4);
        List<double[]> peres = peres24();
        boolean[][] pg = orthogonality(peres);
        int chi = chromatic(pg);
        int edges = 0;
        for (boolean[] row : pg) for (boolean b : row) if (b) edges++;
        check("Peres 24 rays: " + peres.size() + " lines, " + edges / 2 + " orthogonal pairs, fewest small pieces = " + chi, chi >= 4);
        check("a finite configuration like Peres' needs far fewer than the theorem's 11 pieces (" + chi + " < 11)", chi < 11);

        System.out.println(failures == 0 ? "ALL CHECKS PASSED" : failures + " CHECK(S) FAILED");
        if (failures != 0) System.exit(1);
    }
}
