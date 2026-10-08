package confluence.math.clausethreshold;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

/// Java replication of the finite content around OAI.FixedClauseThreshold.main
/// (lean/ComparatorChallenges/FixedClauseThreshold.lean, solution OAI.Probability.RandomSAT.Main).
///
/// The model, read literally from the challenge:
///
/// - a **proper clause** on n variables of size k is a map `Fin n -> Option Bool` with exactly k
///   `some` entries, i.e. k distinct variables each with a sign; there are C(n,k) * 2^k of them;
/// - a **formula** of length m is an ordered m-tuple of proper clauses (with replacement);
/// - `properSATProbability n k m` = (#satisfiable tuples) / (C(n,k) 2^k)^m, with x/0 = 0.
///
/// The theorem says: for every k >= 3 there is one real alpha > 0 such that at every fixed
/// density 0 <= c < alpha the probability at m = floor(c n) tends to 1, and at every c > alpha it
/// tends to 0. That is the satisfiability threshold conjecture in its usual form; nothing is said
/// at c = alpha and no value of alpha is given.
///
/// No finite computation can check a limit. What this class checks:
///
/// 1. exact (BigInteger) satisfiable-tuple counts for n = 3, 4 via a DP over the set of surviving
///    assignments: monotone in m, P = 1 for m < 8, the closed form P(3,3,8) = 1 - 8!/8^8, the
///    first-moment bound P <= 2^n (7/8)^m, and the solution's `center 4 3` inside its bounds;
/// 2. a seeded Monte Carlo with a DPLL solver at densities well below and above 4.27;
/// 3. negative controls: a wrong first-moment bound (kill fraction 1/4, which is 2-SAT's) must be
///    violated by the exact counts, and a wrong-side claim (c = 6 is satisfiable w.h.p.) must fail.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.clausethreshold.FixedClauseThreshold
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Benchmark generation for SAT-backed tools.** Java code that drives a SAT or constraint
///   solver (Sat4j, package-dependency resolvers, configuration checkers, test-case generators)
///   is commonly benchmarked on random 3-SAT. The theorem says there is one fixed density for
///   each k that separates "almost always satisfiable" from "almost never"; generators that want
///   hard instances sit near it (empirically about 4.27 for k = 3), and ones that want easy
///   satisfiable or easy unsatisfiable inputs sit clearly below or above it. The Lean result only
///   guarantees the threshold exists; the number itself is empirical here.
/// - **A known-answer oracle for small instances.** The exact counts below (for example
///   P(n=3, m=8) = 1 - 8!/8^8) are cheap fixtures: a randomized SAT-instance generator in Java can
///   be unit-tested by comparing its empirical satisfiable fraction at tiny n with these exact
///   fractions, which catches bugs such as repeating a variable inside a clause or biased signs.
/// - **Timeouts and capacity planning.** Code that solves many generated constraint problems can
///   use the density of a problem (constraints per variable) as a cheap predictor of whether it is
///   likely satisfiable, but should not trust it near the critical density, where the theorem
///   asserts nothing and the Monte Carlo below shows probabilities near 1/2.
public class FixedClauseThreshold {

    /// Satisfying-set bitmask (over assignments a in [0, 2^n)) of every proper clause.
    static List<Long> clauses(int n, int k) {
        List<Long> out = new ArrayList<>();
        int[] vs = new int[k];
        combos(n, k, 0, 0, vs, out);
        return out;
    }

    static void combos(int n, int k, int start, int depth, int[] vs, List<Long> out) {
        if (depth == k) {
            for (int signs = 0; signs < (1 << k); signs++) {
                long mask = 0;
                for (int a = 0; a < (1 << n); a++) {
                    boolean sat = false;
                    for (int t = 0; t < k; t++)
                        if (((a >> vs[t]) & 1) == ((signs >> t) & 1)) sat = true;
                    if (sat) mask |= 1L << a;
                }
                out.add(mask);
            }
            return;
        }
        for (int v = start; v < n; v++) { vs[depth] = v; combos(n, k, v + 1, depth + 1, vs, out); }
    }

    static long choose(int n, int k) {
        if (k < 0 || k > n) return 0;
        long r = 1;
        for (int i = 0; i < k; i++) r = r * (n - i) / (i + 1);
        return r;
    }

    /// sat[m] = number of satisfiable m-tuples, m = 0..mmax (n <= 6 so masks fit a long).
    static BigInteger[] satCounts(int n, int k, int mmax) {
        List<Long> cl = clauses(n, k);
        long full = (n == 6) ? -1L : (1L << (1 << n)) - 1;
        Map<Long, BigInteger> state = new HashMap<>();
        state.put(full, BigInteger.ONE);
        BigInteger[] sat = new BigInteger[mmax + 1];
        sat[0] = BigInteger.ONE;
        for (int m = 1; m <= mmax; m++) {
            Map<Long, BigInteger> next = new HashMap<>();
            for (var e : state.entrySet())
                for (long c : cl) {
                    long t = e.getKey() & c;
                    if (t != 0) next.merge(t, e.getValue(), BigInteger::add);
                }
            state = next;
            BigInteger s = BigInteger.ZERO;
            for (BigInteger v : state.values()) s = s.add(v);
            sat[m] = s;
        }
        return sat;
    }

    // ---------------- DPLL ----------------
    static int[][] randomFormula(Random rng, int n, int k, int m) {
        int[][] f = new int[m][k];
        for (int j = 0; j < m; j++) {
            int[] vs = new int[k];
            for (int t = 0; t < k; t++) {
                int v;
                do { v = rng.nextInt(n); } while (contains(vs, t, v));
                vs[t] = v;
                f[j][t] = rng.nextBoolean() ? v + 1 : -(v + 1);
            }
        }
        return f;
    }

    static boolean contains(int[] a, int len, int v) {
        for (int i = 0; i < len; i++) if (a[i] == v) return true;
        return false;
    }

    /// val[v] in {0 unassigned, 1 true, -1 false}.
    static boolean dpll(int[][] f, int n, int[] val) {
        List<Integer> trail = new ArrayList<>();
        // unit propagation to fixpoint
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] c : f) {
                int unassigned = 0, last = 0; boolean sat = false;
                for (int l : c) {
                    int x = val[Math.abs(l)];
                    if (x == 0) { unassigned++; last = l; }
                    else if ((x > 0) == (l > 0)) { sat = true; break; }
                }
                if (sat) continue;
                if (unassigned == 0) { undo(val, trail); return false; }
                if (unassigned == 1) { val[Math.abs(last)] = last > 0 ? 1 : -1; trail.add(Math.abs(last)); changed = true; }
            }
        }
        // choose the variable occurring most often in unsatisfied clauses
        int[] cnt = new int[n + 1];
        boolean anyOpen = false;
        for (int[] c : f) {
            boolean sat = false;
            for (int l : c) { int x = val[Math.abs(l)]; if (x != 0 && (x > 0) == (l > 0)) { sat = true; break; } }
            if (sat) continue;
            anyOpen = true;
            for (int l : c) if (val[Math.abs(l)] == 0) cnt[Math.abs(l)]++;
        }
        if (!anyOpen) return true;
        int best = 1;
        for (int v = 1; v <= n; v++) if (cnt[v] > cnt[best]) best = v;
        for (int s : new int[]{1, -1}) {
            val[best] = s;
            if (dpll(f, n, val)) return true;
            val[best] = 0;
        }
        undo(val, trail);
        return false;
    }

    static void undo(int[] val, List<Integer> trail) { for (int v : trail) val[v] = 0; }

    static double[] wilson(int s, int t) {
        double z = 1.96, p = (double) s / t, d = 1 + z * z / t;
        double c = (p + z * z / (2 * t)) / d, h = z * Math.sqrt(p * (1 - p) / t + z * z / (4.0 * t * t)) / d;
        return new double[]{c - h, c + h};
    }

    static int fails = 0;

    static void check(String name, boolean ok, String detail) {
        System.out.printf("  [%s] %s%s%n", ok ? "OK " : "NO ", name, detail.isEmpty() ? "" : ": " + detail);
        if (!ok) fails++;
    }

    static boolean le(BigInteger num, BigInteger den, BigInteger bnum, BigInteger bden) {
        return num.multiply(bden).compareTo(bnum.multiply(den)) <= 0;
    }

    public static void main(String[] args) {
        int k = 3;
        System.out.println("A. exact counts");
        for (int n = 0; n <= 6; n++)
            check("card ProperClause n=" + n + " k=3 = C(n,3)*8", clauses(n, 3).size() == choose(n, 3) * 8, "" + clauses(n, 3).size());
        // n < k: zero clauses; m = 0 gives 1/1, m = 1 gives 0/0 = 0 in Lean
        check("n=2<k: m=0 -> 1/1, m=1 -> 0/0 (Lean 0)", choose(2, 3) == 0, "");
        int violationsWrong = 0; String firstViolation = "";
        for (int[] nm : new int[][]{{3, 20}, {4, 64}}) {
            int n = nm[0], mmax = nm[1];
            BigInteger[] sat = satCounts(n, k, mmax);
            BigInteger N = BigInteger.valueOf(choose(n, k) * 8);
            boolean mono = true, fm = true; int firstUnsat = -1;
            for (int m = 0; m <= mmax; m++) {
                BigInteger tot = N.pow(m);
                if (m > 0 && sat[m].compareTo(sat[m - 1].multiply(N)) > 0) mono = false; // P_m <= P_{m-1}
                if (firstUnsat < 0 && sat[m].compareTo(tot) < 0) firstUnsat = m;
                // P <= 2^n (7/8)^m  <=>  sat * 8^m <= 2^n 7^m tot
                BigInteger bnum = BigInteger.TWO.pow(n).multiply(BigInteger.valueOf(7).pow(m));
                BigInteger bden = BigInteger.valueOf(8).pow(m);
                if (!le(sat[m], tot, bnum, bden)) fm = false;
                BigInteger wnum = BigInteger.TWO.pow(n).multiply(BigInteger.valueOf(3).pow(m));
                BigInteger wden = BigInteger.valueOf(4).pow(m);
                if (!le(sat[m], tot, wnum, wden)) {
                    if (violationsWrong++ == 0) firstViolation = "n=" + n + " m=" + m;
                }
            }
            check("n=" + n + " monotone nonincreasing in m", mono, "");
            check("n=" + n + " first moment P <= 2^n (7/8)^m", fm, "");
            check("n=" + n + " first m with P<1 is 8", firstUnsat == 8, "" + firstUnsat);
            for (int m : new int[]{8, 12, 16, 20, 32})
                if (m <= mmax)
                    System.out.printf("     n=%d m=%2d P=%.6f%n", n, m, new java.math.BigDecimal(sat[m]).divide(new java.math.BigDecimal(N.pow(m)), java.math.MathContext.DECIMAL64).doubleValue());
            if (n == 3) {
                // unsat at m=8 iff the 8 clauses are the 8 distinct sign patterns: 8! of 8^8 tuples
                BigInteger unsat = BigInteger.valueOf(8).pow(8).subtract(sat[8]);
                check("closed form: unsat 8-tuples at n=3 = 8! = 40320", unsat.equals(BigInteger.valueOf(40320)), unsat.toString());
            }
            int cap = (1 << (k + 1)) * n;
            if (cap <= mmax) {
                double center = 0;
                for (int m = 1; m <= cap; m++)
                    center += new java.math.BigDecimal(sat[m]).divide(new java.math.BigDecimal(N.pow(m)), java.math.MathContext.DECIMAL64).doubleValue();
                center /= n;
                double lb = Math.exp(-2) / 16;
                check(String.format("center(%d,3) = %.6f within [e^-2/16, 2^3+1]", n, center), lb <= center && center <= 9, "");
            }
        }
        check("CONTROL wrong bound 2^n (3/4)^m is violated by exact counts", violationsWrong > 0,
            violationsWrong + " violations, first at " + firstViolation);

        System.out.println("B. Monte Carlo, seed 20261008, 400 formulas per cell");
        Random rng = new Random(20261008L);
        int T = 400;
        double[] cs = {2.0, 3.0, 4.27, 6.0};
        int[] ns = {40, 80, 120};
        double[][] ph = new double[cs.length][ns.length];
        for (int i = 0; i < cs.length; i++)
            for (int j = 0; j < ns.length; j++) {
                int n = ns[j], m = (int) Math.floor(cs[i] * n), s = 0;
                for (int t = 0; t < T; t++) if (dpll(randomFormula(rng, n, 3, m), n, new int[n + 1])) s++;
                double[] ci = wilson(s, T);
                ph[i][j] = (double) s / T;
                System.out.printf("     c=%4.2f n=%3d m=%4d P^=%.3f 95%% CI [%.3f,%.3f]%n", cs[i], n, m, ph[i][j], ci[0], ci[1]);
            }
        check("c=2.0 n=120 P^ >= 0.95", ph[0][2] >= 0.95, "");
        check("c=3.0 n=120 P^ >= 0.95", ph[1][2] >= 0.95, "");
        check("c=6.0 n=120 P^ <= 0.05", ph[3][2] <= 0.05, "");
        check("c=6.0 nonincreasing in n (40 -> 120)", ph[3][2] <= ph[3][0], "");
        check("first-moment bound ln2/-ln(7/8) = " + String.format("%.4f", Math.log(2) / -Math.log(7.0 / 8)) + " > 4.27", Math.log(2) / -Math.log(7.0 / 8) > 4.27, "");
        boolean wrongSide = ph[3][2] >= 0.95;
        check("CONTROL wrong-side claim 'P(c=6, n=120) >= 0.95' is FALSE", !wrongSide, String.format("observed %.3f", ph[3][2]));
        System.out.println(fails == 0 ? "ALL CHECKS HOLD" : fails + " CHECK(S) FAIL");
    }
}
