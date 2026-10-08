package confluence.math.truffet;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Map;

/// Java replication of OAI.TruffetV4Counterexample.finite_execution_not_optimal
/// (lean/ComparatorChallenges/TruffetCounterexample.lean), definition for definition.
///
/// The setting is a max-plus ("tropical") linear program: a form f assigns a coefficient to
/// each of three columns (two variables and a constant), and f evaluated at w is
/// max_k (f[k] + w[k]). Coefficients live in R plus a bottom element (Lean: WithBot R); here
/// bottom is Double.NEGATIVE_INFINITY, which already absorbs addition the way WithBot does.
///
/// The theorem says: from `initial`, the algorithm is FORCED through two singleton steps to
/// `finalState` and stops, and reading its answer back gives `output` with cost 1, while the
/// feasible point `better` costs 0. So the algorithm's finite execution is not optimal.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.truffet.Truffet
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Max-plus linear programs show up in ordinary systems code.** The max-plus algebra used
///   here is the arithmetic of earliest-start times in schedules, critical paths in build or
///   task graphs, and timing analysis of pipelines: "start = max over predecessors of (their
///   start + delay)". A Java scheduler or build planner that optimizes in that algebra is solving
///   problems of this shape.
/// - **An elimination algorithm's answer is not proof of optimality.** This instance shows a
///   forced, legal run of a published elimination procedure stopping at cost 1 while a feasible
///   point costs 0. A Java implementation of a Truffet-style method should therefore not report
///   "optimal" from the procedure alone. It should carry an independent check, such as comparing
///   against a brute-force or exact solver on small instances.
/// - **A ready-made regression fixture.** `INITIAL`, `OUTPUT` and `BETTER` are a complete,
///   two-variable test case with a known right answer (cost 0) and a known wrong one (cost 1). A
///   max-plus solver library could keep it as a unit test that fails if the solver ever reproduces
///   the non-optimal answer.
/// - **Modelling bottom.** `Double.NEGATIVE_INFINITY` reproduces Lean's `WithBot ℝ` addition
///   (bottom absorbs) and order for free. That only holds while no `+∞` ever appears, since
///   `-∞ + +∞` is `NaN` in Java; a production version would want a small value type that makes
///   bottom explicit.
public class Truffet {

    static final double BOT = Double.NEGATIVE_INFINITY;
    static final int[] VARS = {0, 1};
    static final int[] ROWS = {0, 1};
    static final double[] NULL_FORM = {BOT, BOT, BOT};

    record Row(double[] lhs, double[] rhs) {
        @Override public boolean equals(Object o) {
            return o instanceof Row r && Arrays.equals(lhs, r.lhs) && Arrays.equals(rhs, r.rhs);
        }
        @Override public int hashCode() { return Arrays.hashCode(lhs) * 31 + Arrays.hashCode(rhs); }
    }

    record State(Row[] rows, double[] cost, boolean[] remaining) {
        @Override public boolean equals(Object o) {
            return o instanceof State s && Arrays.equals(rows, s.rows)
                && Arrays.equals(cost, s.cost) && Arrays.equals(remaining, s.remaining);
        }
        @Override public int hashCode() { return Arrays.hashCode(cost); }
    }

    static int column(int j) { return j; }

    static double eval(double[] f, double[] w) {
        double best = BOT;
        for (int k = 0; k < 3; k++) best = Math.max(best, f[k] + w[k]); // -inf + x = -inf
        return best;
    }

    static boolean wellFormed(State s) {
        for (int j : VARS) {
            if (s.remaining()[j]) continue;
            if (s.cost()[column(j)] != BOT) return false;
            for (int i : ROWS) {
                Row r = s.rows()[i];
                if (r.lhs()[column(j)] != BOT || r.rhs()[column(j)] != BOT) return false;
            }
        }
        return true;
    }

    static boolean feasible(State s, double[] w) {
        for (int i : ROWS) if (!(eval(s.rows()[i].rhs(), w) <= eval(s.rows()[i].lhs(), w))) return false;
        return true;
    }

    static boolean lower(State s, int i, int j) {
        Row r = s.rows()[i];
        return r.lhs()[column(j)] != BOT && r.rhs()[column(j)] < r.lhs()[column(j)];
    }

    static boolean upper(State s, int i, int j) {
        Row r = s.rows()[i];
        return r.rhs()[column(j)] != BOT && r.lhs()[column(j)] < r.rhs()[column(j)];
    }

    static boolean anyLower(State s, int j) { for (int i : ROWS) if (lower(s, i, j)) return true; return false; }
    static boolean anyUpper(State s, int j) { for (int i : ROWS) if (upper(s, i, j)) return true; return false; }

    static boolean dominating(State s, int j) { return s.remaining()[j] && anyLower(s, j) && anyUpper(s, j); }

    static boolean anyDominating(State s) { for (int k : VARS) if (dominating(s, k)) return true; return false; }

    static boolean eligible(State s, int i, int j) {
        return s.remaining()[j] && lower(s, i, j) && (!anyDominating(s) || dominating(s, j));
    }

    static boolean bounded(State s) {
        for (int j : VARS) if (s.remaining()[j] && !anyLower(s, j) && !anyUpper(s, j)) return false;
        return true;
    }

    static boolean stop(State s) {
        for (int i : ROWS) if (!(s.rows()[i].rhs()[2] <= s.rows()[i].lhs()[2])) return false;
        return true;
    }

    static boolean anyRemaining(State s) { for (int j : VARS) if (s.remaining()[j]) return true; return false; }

    static boolean anyRemainingLower(State s) {
        for (int i : ROWS) for (int j : VARS) if (s.remaining()[j] && lower(s, i, j)) return true;
        return false;
    }

    static boolean anyRemainingUpper(State s) {
        for (int i : ROWS) for (int j : VARS) if (s.remaining()[j] && upper(s, i, j)) return true;
        return false;
    }

    static boolean switchCond(State s) {
        for (int j : VARS) if (s.remaining()[j] && s.cost()[column(j)] != BOT) return false;
        return !stop(s) && anyRemaining(s) && !anyRemainingLower(s) && anyRemainingUpper(s);
    }

    static boolean failure(State s) {
        return !stop(s) && (!anyRemaining(s) || (!anyRemainingLower(s) && !anyRemainingUpper(s)));
    }

    static double unbotD(double dflt, double x) { return x == BOT ? dflt : x; }

    static double[] lowerForm(State s, int i, int j) {
        Row r = s.rows()[i];
        double shift = -unbotD(0.0, r.lhs()[column(j)]);
        double[] g = new double[3];
        for (int k = 0; k < 3; k++) g[k] = k == column(j) ? BOT : r.rhs()[k] + shift;
        return g;
    }

    static double[] substitute(double[] f, int j, double[] g) {
        double[] out = new double[3];
        for (int k = 0; k < 3; k++) out[k] = k == column(j) ? BOT : Math.max(f[k], f[column(j)] + g[k]);
        return out;
    }

    static Row cleanup(Row r) {
        for (int k = 0; k < 3; k++) if (!(r.rhs()[k] <= r.lhs()[k])) return r;
        return new Row(NULL_FORM.clone(), NULL_FORM.clone());
    }

    static State advance(State s, int i, int j) {
        double[] g = lowerForm(s, i, j);
        Row[] rows = new Row[2];
        for (int r : ROWS) rows[r] = cleanup(new Row(substitute(s.rows()[r].lhs(), j, g), substitute(s.rows()[r].rhs(), j, g)));
        boolean[] rem = new boolean[2];
        for (int k : VARS) rem[k] = s.remaining()[k] && k != j;
        return new State(rows, substitute(s.cost(), j, g), rem);
    }

    static Map<String, Boolean> forcedSingletonStep(State s, State s2, int i, int j) {
        Map<String, Boolean> parts = new LinkedHashMap<>();
        parts.put("wellFormed s", wellFormed(s));
        parts.put("wellFormed s'", wellFormed(s2));
        parts.put("bounded s", bounded(s));
        parts.put("not stop s", !stop(s));
        parts.put("not switch s", !switchCond(s));
        parts.put("not failure s", !failure(s));
        boolean exactlyOne = true;
        for (int r : ROWS) for (int k : VARS) exactlyOne &= eligible(s, r, k) == (r == i && k == j);
        parts.put("eligible exactly (i,j)", exactlyOne);
        boolean someNonBot = false;
        for (double x : substitute(s.cost(), j, lowerForm(s, i, j))) someNonBot |= x != BOT;
        parts.put("substituted cost not all bottom", someNonBot);
        parts.put("s' = advance s i j", s2.equals(advance(s, i, j)));
        return parts;
    }

    static boolean all(Map<String, Boolean> parts) { return parts.values().stream().allMatch(b -> b); }

    static Row row(double[] lhs, double[] rhs) { return new Row(lhs, rhs); }
    static double[] f(double a, double b, double c) { return new double[] {a, b, c}; }

    static final State INITIAL = new State(
        new Row[] {row(f(0, 0, BOT), f(BOT, BOT, 0)), row(f(0, BOT, BOT), f(BOT, 1, -2))},
        f(0, BOT, BOT), new boolean[] {true, true});

    static final State MIDDLE = new State(
        new Row[] {row(NULL_FORM.clone(), NULL_FORM.clone()), row(f(0, BOT, BOT), f(BOT, BOT, 1))},
        f(0, BOT, BOT), new boolean[] {true, false});

    static final State FINAL = new State(
        new Row[] {row(NULL_FORM.clone(), NULL_FORM.clone()), row(NULL_FORM.clone(), NULL_FORM.clone())},
        f(BOT, BOT, 1), new boolean[] {false, false});

    static final double[] OUTPUT = {1, 0, 0};
    static final double[] BETTER = {0, -1, 0};

    /// crossRowRestriction is "for all alpha, exists w"; this samples alpha and searches w,
    /// which is evidence for the statement, not a proof of it (Lean's proof is the proof).
    static boolean crossRowRestrictionEvidence(State s) {
        double[] alphas = {-1e6, -1e3, -50, -5, -1, 0, 1, 5, 50, 1e3, 1e6};
        double[] scales = {1, 10, 1e3, 1e6, 1e9};
        for (int i : ROWS) for (int r : ROWS) {
            if (i == r) continue;
            for (double a : alphas) {
                boolean found = false;
                search:
                for (double sc : scales) {
                    double[] vals = {-sc, 0, sc};
                    for (double x : vals) for (double y : vals) for (double z : vals) {
                        double[] w = {x, y, z};
                        if (eval(s.rows()[i].lhs(), w) < a + eval(s.rows()[r].rhs(), w)) { found = true; break search; }
                    }
                }
                if (!found) return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        var step1 = forcedSingletonStep(INITIAL, MIDDLE, 0, 1);
        var step2 = forcedSingletonStep(MIDDLE, FINAL, 1, 0);
        Map<String, Boolean> conj = new LinkedHashMap<>();
        conj.put("crossRowRestriction initial (sampled evidence)", crossRowRestrictionEvidence(INITIAL));
        conj.put("ForcedSingletonStep initial middle 0 1", all(step1));
        conj.put("ForcedSingletonStep middle finalState 1 0", all(step2));
        conj.put("no remaining var in finalState", !anyRemaining(FINAL));
        conj.put("stop finalState", stop(FINAL));
        conj.put("feasible initial output", feasible(INITIAL, OUTPUT));
        conj.put("feasible initial better", feasible(INITIAL, BETTER));
        conj.put("output 2 = 0", OUTPUT[2] == 0);
        conj.put("better 2 = 0", BETTER[2] == 0);
        conj.put("output 1 = eval (lowerForm initial 0 1) output", OUTPUT[1] == eval(lowerForm(INITIAL, 0, 1), OUTPUT));
        conj.put("output 0 = eval (lowerForm middle 1 0) output", OUTPUT[0] == eval(lowerForm(MIDDLE, 1, 0), OUTPUT));
        conj.put("eval initial.cost output = eval final.cost output", eval(INITIAL.cost(), OUTPUT) == eval(FINAL.cost(), OUTPUT));
        conj.put("eval initial.cost better < eval final.cost output", eval(INITIAL.cost(), BETTER) < eval(FINAL.cost(), OUTPUT));

        conj.forEach((k, v) -> System.out.printf("  [%s] %s%n", v ? "OK " : "NO ", k));
        System.out.printf("costs: the algorithm's output costs %.1f, 'better' costs %.1f%n",
            eval(FINAL.cost(), OUTPUT), eval(INITIAL.cost(), BETTER));
        System.out.println(all(conj) ? "ALL 13 CONJUNCTS HOLD" : "SOME CONJUNCT FAILS");

        // negative controls: the replication must be able to say NO
        System.out.println("control: forced step with the WRONG pivot (1,1): " + all(forcedSingletonStep(INITIAL, MIDDLE, 1, 1)));
        System.out.println("control: feasible initial (5,5,0): " + feasible(INITIAL, f(5, 5, 0)));
        System.out.println("control: 'better' strictly cheaper if we PRETEND its cost is 2: " + (2.0 < eval(FINAL.cost(), OUTPUT)));
    }
}
