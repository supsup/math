package confluence.math.permanent;

import java.util.Random;

/// A numerical look at `OAI.FourRow.robust_permanent`
/// (lean/ComparatorChallenges/FourRowPermanent.lean; the Lean proof checks, see
/// playground/confluence/lean-docker/).
///
/// The theorem: there are p₀ with 4/3 < p₀ < 2 and ε > 0 such that for every probability law ν on
/// the 24 permutations of 4 sites that is ε-close to uniform in total variation and has uniform
/// marginals (each site goes to each site with probability 1/4), and every nonnegative f,
///
///     E_ν [ ∏ᵢ fᵢ(π(i)) ]  ≤  ∏ᵢ ‖fᵢ‖_{p₀},     ‖g‖_p = ( (1/4) Σⱼ g(j)^p )^{1/p}.
///
/// At ν = uniform the left side is perm(F)/24 with F[i][j] = fᵢ(j). Both sides are homogeneous of
/// degree 1 in each row, and the all-ones matrix gives equality for every p. This program asks: for a
/// given p, how large can perm(F)/24 / ∏ᵢ‖Fᵢ‖_p get? If the sup is above 1, the inequality fails at
/// that p even for the uniform law; the theorem says some p₀ in (4/3, 2) is safe even with a
/// robustness margin.
///
/// It is a random search plus multiplicative hill-climbing, so it gives LOWER bounds on the sup: a
/// value above 1 is a real counterexample matrix (printed), while "about 1" means the search found
/// nothing, not that nothing exists.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.permanent.FourRowPermanent
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Bounding an expensive quantity by cheap ones.** The permanent is #P-hard to compute in
///   general, but the right side is just a product of per-row norms. An inequality like this lets
///   Java code bound the expected product over random assignments (the "matching" weight of a
///   random bijection) without enumerating permutations. That only holds for n = 4 and laws with
///   uniform marginals; nothing here extends it.
/// - **Robustness is the useful part.** The theorem holds for every law ε-close to uniform, not
///   only the uniform one. A shuffler or load balancer whose permutation distribution is only
///   APPROXIMATELY uniform, but has exactly uniform marginals, would still get the bound. ε itself
///   isn't given explicitly in the statement, so a program can't use it as a number.
/// - **Search as a falsifier for claimed constants.** The method here (homogeneous ratio, random
///   start, multiplicative steps that keep entries nonnegative) is a cheap way for a Java test to
///   probe an inequality at a candidate exponent before trusting it: a found violation is
///   conclusive, a clean search is only evidence.
public class FourRowPermanent {

    static final int N = 4;

    /// perm(F) by expansion over all 24 permutations.
    static double permanent(double[][] f) {
        return permRec(f, 0, new boolean[N]);
    }

    private static double permRec(double[][] f, int row, boolean[] used) {
        if (row == N) return 1.0;
        double s = 0;
        for (int j = 0; j < N; j++) {
            if (used[j] || f[row][j] == 0) continue;
            used[j] = true;
            s += f[row][j] * permRec(f, row + 1, used);
            used[j] = false;
        }
        return s;
    }

    static double norm(double[] g, double p) {
        double s = 0;
        for (double x : g) s += Math.pow(x, p);
        return Math.pow(s / N, 1 / p);
    }

    static double ratio(double[][] f, double p) {
        double prod = 1;
        for (double[] row : f) prod *= norm(row, p);
        return permanent(f) / 24.0 / prod;
    }

    static double[][] copy(double[][] f) {
        double[][] g = new double[N][];
        for (int i = 0; i < N; i++) g[i] = f[i].clone();
        return g;
    }

    /// Best ratio found for exponent p: random starts, then multiplicative perturbations.
    static double[][] search(double p, Random rng, double[] bestOut) {
        double best = -1;
        double[][] bestF = null;
        for (int start = 0; start < 300; start++) {
            double[][] f = new double[N][N];
            for (double[] row : f) for (int j = 0; j < N; j++) row[j] = rng.nextDouble() < 0.3 ? 0 : rng.nextDouble();
            double r = ratio(f, p);
            if (Double.isNaN(r)) continue;
            for (int step = 0; step < 4000; step++) {
                double[][] g = copy(f);
                int i = rng.nextInt(N), j = rng.nextInt(N);
                g[i][j] = rng.nextDouble() < 0.05 ? 0 : g[i][j] * Math.exp(0.3 * rng.nextGaussian()) + 1e-12;
                double rg = ratio(g, p);
                if (!Double.isNaN(rg) && rg > r) { f = g; r = rg; }
            }
            if (r > best) { best = r; bestF = f; }
        }
        bestOut[0] = best;
        return bestF;
    }

    static String show(double[][] f) {
        double max = 0;
        for (double[] row : f) for (double x : row) max = Math.max(max, x);
        StringBuilder sb = new StringBuilder();
        for (double[] row : f) {
            sb.append("      [");
            for (double x : row) sb.append(String.format(" %9.2e", x / max));
            sb.append(" ]\n");
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        double[][] ones = new double[N][N];
        for (double[] row : ones) java.util.Arrays.fill(row, 1.0);
        double[][] identity = new double[N][N];
        for (int i = 0; i < N; i++) identity[i][i] = 1.0;
        System.out.printf("control: all-ones matrix ratio at p=1.5 (expect exactly 1): %.12f%n", ratio(ones, 1.5));
        System.out.printf("control: identity (a single permutation) at p=1: %.6f, p=2: %.6f  (perm/24 = 1/24, norms = 4^{-1/p})%n",
            ratio(identity, 1.0), ratio(identity, 2.0));

        Random rng = new Random(2026_10_08L);
        double crit = 4 * Math.log(4) / Math.log(24);
        System.out.printf("closed form: a permutation matrix gives perm/24 / prod ||f_i||_p = 4^(4/p)/24, which is 1 at p* = 4 ln4/ln24 = %.6f%n", crit);
        double[] ps = {1.0, 1.2, 4.0 / 3, 1.4, 1.5, 1.6, 1.7, crit - 0.01, crit + 0.01, 1.8, 2.0, 2.5};
        System.out.println("\n  p        best perm/24 / prod ||f_i||_p found (lower bound on the sup)");
        for (double p : ps) {
            double[] best = new double[1];
            double[][] f = search(p, rng, best);
            System.out.printf("  %.4f   %.6f   (permutation matrix: %.6f)%s%n", p, best[0], Math.pow(4, 4 / p) / 24,
                best[0] > 1 + 1e-9 ? "  <- VIOLATES at uniform law" : "");
            if (best[0] > 1 + 1e-9 && (p == 1.0 || Math.abs(p - 4.0 / 3) < 1e-9)) System.out.print(show(f));
        }
    }
}
