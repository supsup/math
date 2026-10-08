package confluence.math.midpointlenses;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/// Java replication of one finite instance of OAI.SegmentLenses.midpoint_lens_main
/// (lean/ComparatorChallenges/MidpointLenses.lean), in exact rational arithmetic.
///
/// The space: functions on the vertices of a rooted forest. A *segment* is an interval [a, b] of an
/// ancestor chain; the primal norm of a finitely supported u is
/// rho(u) = max over pairwise-disjoint segment families of sqrt(sum_S u(S)^2), where u(S) is the sum
/// of u over S. The theorem lives in the DUAL: for a finite ancestral ("closed under ancestors") set
/// H, a functional x supported on H, any y, and R with ||x + y|| <= R and ||x - y|| <= R, the part of
/// y outside H has norm at most 2 sqrt(R^2 - ||x||^2).
///
/// On a finite ancestral vertex set the dual norm is computable: the dual unit ball is the convex
/// hull of the atoms sum_{S in P} a_S d_S over partitions P into segments with ||a||_2 <= 1. So every
/// primal test u gives a lower bound f(u)/rho(u) and every atom decomposition gives an upper bound.
/// This class pins four norms EXACTLY (lower bound == upper bound, both rational) on the two-vertex
/// tree root r, child c, with H = {r}:
///
///   x = (9/10, 0), y = (1/10, 3/5):  ||x|| = 9/10, ||x+y|| = ||x-y|| = 1, ||Q_H y|| = 3/5.
///
/// With R = 1 the theorem asks 3/5 <= 2 sqrt(19/100) (i.e. 9/25 <= 19/25): true. Two negative
/// controls must FAIL: (A) the same claim with constant 13/10 instead of 2 (9/25 > 3211/10000), and
/// (B) the claim for the l1-of-segment-sums norm, a one-symbol change of the definition, where
/// x = e_r^*, y = (1/2) e_c^* has R = ||x|| = 1 but ||Q_H y|| = 1/2 > 0.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.midpointlenses.MidpointLenses
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Certified bounds instead of a solver's float.** A dual norm here is a convex optimisation
///   (an SOCP). Rather than trusting a solver's number, the code checks a *certificate pair*: a
///   primal test u (lower bound) and an explicit atom decomposition (upper bound), both in exact
///   rationals. The same pattern fits any Java service that reports an optimum: ship the witness
///   with the number and verify it cheaply on the client side.
/// - **Enumerating path partitions of a tree.** `partitions` lists every way to cut a rooted
///   forest into ancestor chains, by letting each vertex either continue its parent's chain or start
///   a new one (at most one child continues). That is a small reusable routine for tree DP tests,
///   e.g. checking a heavy-path or chain-decomposition implementation against brute force.
/// - **A small exact regression fixture.** The instance above is four rational vectors with known
///   exact norms and a known ratio sqrt(36/19). A numerical library computing this kind of norm
///   (James-tree-style tests, mixed l2/segment norms) could keep it as a unit test, together with
///   control B, which shows that swapping l2 for l1 in the segment sum changes the answer.
/// - **Do not round before comparing.** Every comparison is made on squares of rationals; no
///   `Math.sqrt` is called on a value that decides an outcome. That is the general rule for code whose
///   verdict sits on an inequality between square roots.
public class MidpointLenses {

    // ------------------------------------------------------------------ exact rationals

    record Q(BigInteger n, BigInteger d) implements Comparable<Q> {
        Q {
            if (d.signum() == 0) throw new ArithmeticException("zero denominator");
            if (d.signum() < 0) { n = n.negate(); d = d.negate(); }
            BigInteger g = n.gcd(d);
            if (!g.equals(BigInteger.ONE) && g.signum() != 0) { n = n.divide(g); d = d.divide(g); }
            if (n.signum() == 0) d = BigInteger.ONE;
        }
        static Q of(long n, long d) { return new Q(BigInteger.valueOf(n), BigInteger.valueOf(d)); }
        static Q of(long n) { return of(n, 1); }
        Q add(Q o) { return new Q(n.multiply(o.d).add(o.n.multiply(d)), d.multiply(o.d)); }
        Q sub(Q o) { return add(o.neg()); }
        Q mul(Q o) { return new Q(n.multiply(o.n), d.multiply(o.d)); }
        Q div(Q o) { return new Q(n.multiply(o.d), d.multiply(o.n)); }
        Q neg() { return new Q(n.negate(), d); }
        Q abs() { return n.signum() < 0 ? neg() : this; }
        Q sq() { return mul(this); }
        int signum() { return n.signum(); }
        double toDouble() { return new java.math.BigDecimal(n).divide(new java.math.BigDecimal(d), java.math.MathContext.DECIMAL64).doubleValue(); }
        public int compareTo(Q o) { return n.multiply(o.d).compareTo(o.n.multiply(d)); }
        /// exact square root, or an exception if q is not the square of a rational
        Q sqrtExact() {
            BigInteger a = n.sqrt(), b = d.sqrt();
            if (!a.multiply(a).equals(n) || !b.multiply(b).equals(d))
                throw new ArithmeticException(this + " is not a rational square");
            return new Q(a, b);
        }
        @Override public String toString() { return d.equals(BigInteger.ONE) ? n.toString() : n + "/" + d; }
    }

    // ------------------------------------------------------------------ forests, partitions

    /// parent[i] == -1 for a root, else parent[i] < i
    record Forest(int[] parent) {
        int n() { return parent.length; }

        List<Integer> ancestors(int v) {
            List<Integer> out = new ArrayList<>();
            for (int w = v; w != -1; w = parent[w]) out.add(w);
            return out;
        }

        /// all partitions of the vertex set into segments (ancestor chains)
        List<List<Set<Integer>>> partitions() {
            List<List<Set<Integer>>> out = new ArrayList<>();
            int n = n();
            for (int mask = 0; mask < (1 << n); mask++) {
                boolean ok = true;
                for (int v = 0; v < n && ok; v++) {
                    boolean ext = (mask >> v & 1) == 1;
                    if (ext && parent[v] == -1) ok = false;
                }
                for (int v = 0; v < n && ok; v++) {
                    int cont = 0;
                    for (int c = 0; c < n; c++) if (parent[c] == v && (mask >> c & 1) == 1) cont++;
                    if (cont > 1) ok = false;
                }
                if (!ok) continue;
                int[] top = new int[n];
                for (int v = 0; v < n; v++) top[v] = (mask >> v & 1) == 1 ? top[parent[v]] : v;
                List<Set<Integer>> groups = new ArrayList<>();
                for (int t = 0; t < n; t++) {
                    Set<Integer> g = new HashSet<>();
                    for (int v = 0; v < n; v++) if (top[v] == t) g.add(v);
                    if (!g.isEmpty()) groups.add(g);
                }
                out.add(groups);
            }
            return out;
        }

        /// every segment [a, b]
        List<Set<Integer>> segments() {
            List<Set<Integer>> segs = new ArrayList<>();
            for (int b = 0; b < n(); b++) {
                List<Integer> chain = ancestors(b);
                for (int k = 1; k <= chain.size(); k++) segs.add(new HashSet<>(chain.subList(0, k)));
            }
            return segs;
        }
    }

    static Q sumOn(Set<Integer> s, Q[] u) {
        Q t = Q.of(0);
        for (int v : s) t = t.add(u[v]);
        return t;
    }

    /// rho(u)^2 over partitions (the shortcut)
    static Q rhoSq(Forest f, Q[] u) {
        Q best = Q.of(0);
        for (List<Set<Integer>> p : f.partitions()) {
            Q s = Q.of(0);
            for (Set<Integer> seg : p) s = s.add(sumOn(seg, u).sq());
            if (s.compareTo(best) > 0) best = s;
        }
        return best;
    }

    /// rho(u)^2 over ALL pairwise-disjoint segment families (the definition), to check the shortcut
    static Q rhoSqAllFamilies(Forest f, Q[] u) {
        List<Set<Integer>> segs = f.segments();
        Q best = Q.of(0);
        for (int mask = 0; mask < (1 << segs.size()); mask++) {
            Set<Integer> used = new HashSet<>();
            boolean ok = true;
            Q s = Q.of(0);
            for (int i = 0; i < segs.size() && ok; i++) {
                if ((mask >> i & 1) == 0) continue;
                for (int v : segs.get(i)) if (!used.add(v)) ok = false;
                s = s.add(sumOn(segs.get(i), u).sq());
            }
            if (ok && s.compareTo(best) > 0) best = s;
        }
        return best;
    }

    /// lower bound squared: (f(u))^2 / rho(u)^2, requires f(u) >= 0
    static Q lowerSq(Forest f, Q[] fn, Q[] u) {
        Q fu = Q.of(0);
        for (int v = 0; v < f.n(); v++) fu = fu.add(fn[v].mul(u[v]));
        if (fu.signum() < 0) throw new IllegalArgumentException("f(u) < 0");
        return fu.sq().div(rhoSq(f, u));
    }

    /// one atom: coefficients on the segments of one partition
    record Atom(List<Set<Integer>> segs, Q[] coeff) {}

    /// upper bound: sum of ||coeff||_2 (each must be an exact rational square root) plus the l1 norm
    /// of whatever the atoms leave unpaid (singleton atoms e_v^* have norm <= 1)
    static Q upper(Forest f, Q[] fn, List<Atom> atoms, List<List<Set<Integer>>> parts) {
        Q[] rem = fn.clone();
        Q cost = Q.of(0);
        for (Atom a : atoms) {
            if (!parts.contains(a.segs())) throw new IllegalStateException("not a partition: " + a.segs());
            Q ss = Q.of(0);
            for (int i = 0; i < a.coeff().length; i++) {
                ss = ss.add(a.coeff()[i].sq());
                for (int v : a.segs().get(i)) rem[v] = rem[v].sub(a.coeff()[i]);
            }
            cost = cost.add(ss.sqrtExact());
        }
        for (Q r : rem) cost = cost.add(r.abs());
        return cost;
    }

    static Q exactNorm(String name, Forest f, Q[] fn, Q[] u, List<Atom> atoms, List<List<Set<Integer>>> parts) {
        Q lo2 = lowerSq(f, fn, u);
        Q hi = upper(f, fn, atoms, parts);
        boolean pinned = lo2.compareTo(hi.sq()) == 0;
        System.out.printf("  ||%s||: lower^2 = %s, upper = %s, pinned exactly: %s%n", name, lo2, hi, pinned);
        if (!pinned) throw new AssertionError(name + " not pinned");
        return hi;
    }

    static Set<Integer> s(Integer... v) { return new HashSet<>(List.of(v)); }

    public static void main(String[] args) {
        Forest edge = new Forest(new int[]{-1, 0});
        List<List<Set<Integer>>> parts = edge.partitions();
        System.out.println("== two-vertex tree (r = 0, c = 1), H = {r}; partitions: " + parts);
        if (parts.size() != 2) throw new AssertionError("expected 2 partitions");

        // partition shortcut == definition, on a few rational u (also on a 4-vertex Y tree)
        Forest y4 = new Forest(new int[]{-1, 0, 1, 1});
        Q[][] us = {{Q.of(1), Q.of(0)}, {Q.of(4, 5), Q.of(-3, 5)}, {Q.of(-2), Q.of(7)}};
        for (Q[] u : us) if (rhoSq(edge, u).compareTo(rhoSqAllFamilies(edge, u)) != 0) throw new AssertionError();
        Q[][] us4 = {{Q.of(1), Q.of(-2), Q.of(3), Q.of(1, 2)}, {Q.of(5), Q.of(-1), Q.of(-1), Q.of(-1)},
                     {Q.of(0), Q.of(1), Q.of(1), Q.of(-3, 7)}};
        for (Q[] u : us4) if (rhoSq(y4, u).compareTo(rhoSqAllFamilies(y4, u)) != 0) throw new AssertionError();
        System.out.println("  rho via partitions == rho via all disjoint families (edge, Y tree): true");

        List<Set<Integer>> singles = List.of(s(0), s(1));
        List<Set<Integer>> whole = List.of(s(0, 1));
        // order the partition lists exactly as partitions() produced them
        singles = parts.stream().filter(p -> p.size() == 2).findFirst().orElseThrow();
        whole = parts.stream().filter(p -> p.size() == 1).findFirst().orElseThrow();
        int i0 = singles.get(0).contains(0) ? 0 : 1, i1 = 1 - i0;

        Q[] x = {Q.of(9, 10), Q.of(0)};
        Q[] y = {Q.of(1, 10), Q.of(3, 5)};
        Q[] xp = {x[0].add(y[0]), x[1].add(y[1])};
        Q[] xm = {x[0].sub(y[0]), x[1].sub(y[1])};
        Q[] qy = {Q.of(0), y[1]};

        Q[] c1 = new Q[2]; c1[i0] = Q.of(9, 10); c1[i1] = Q.of(0);
        Q nx = exactNorm("x", edge, x, new Q[]{Q.of(1), Q.of(0)}, List.of(new Atom(singles, c1)), parts);
        Q[] c2 = new Q[2]; c2[i0] = Q.of(2, 5); c2[i1] = Q.of(0);
        Q np = exactNorm("x+y", edge, xp, new Q[]{Q.of(1), Q.of(0)},
            List.of(new Atom(singles, c2), new Atom(whole, new Q[]{Q.of(3, 5)})), parts);
        Q[] c3 = new Q[2]; c3[i0] = Q.of(4, 5); c3[i1] = Q.of(-3, 5);
        Q nm = exactNorm("x-y", edge, xm, new Q[]{Q.of(4, 5), Q.of(-3, 5)}, List.of(new Atom(singles, c3)), parts);
        Q[] c4 = new Q[2]; c4[i0] = Q.of(0); c4[i1] = Q.of(3, 5);
        Q nq = exactNorm("Q_H y", edge, qy, new Q[]{Q.of(0), Q.of(1)}, List.of(new Atom(singles, c4)), parts);

        Q r = np.compareTo(nm) >= 0 ? np : nm;
        Q deficit = r.sq().sub(nx.sq());
        Q lhs2 = nq.sq();
        boolean theorem = lhs2.compareTo(Q.of(4).mul(deficit)) <= 0;
        System.out.printf("  R = %s, deficit R^2-||x||^2 = %s; theorem: %s <= 4*%s : %s%n", r, deficit, lhs2, deficit, theorem);
        System.out.printf("  ratio ||Q_H y||/sqrt(deficit) = sqrt(%s) ~ %.6f (theorem allows 2)%n",
            lhs2.div(deficit), Math.sqrt(lhs2.div(deficit).toDouble()));
        if (!theorem) throw new AssertionError("theorem instance failed");

        // CONTROL A: constant 13/10 instead of 2 must fail on this same instance
        Q c = Q.of(13, 10);
        boolean failsA = lhs2.compareTo(c.sq().mul(deficit)) > 0;
        System.out.printf("  CONTROL A (c = 13/10): %s > %s, claim FAILS: %s%n", lhs2, c.sq().mul(deficit), failsA);
        if (!failsA) throw new AssertionError("control A did not fail");

        // CONTROL B: l1 sum over segments (rho1(u) = max_P sum |u(S)|). Unit ball of the dual is the
        // square [-1,1]^2 here: ||(1,0)|| >= 1 via u = (1,0) (rho1 = 1); (1, +-1/2) = 1/2 (1,+-1) +
        // 1/2 (1,0) with both atoms sign vectors of norm 1, so ||x +- y|| <= 1; ||(0,1/2)|| >= 1/2.
        Q rho1a = rho1(edge, new Q[]{Q.of(1), Q.of(0)}), rho1b = rho1(edge, new Q[]{Q.of(0), Q.of(1)});
        Q[] atomPlus = {Q.of(1), Q.of(1)}, atomMinus = {Q.of(1), Q.of(-1)}, atomE = {Q.of(1), Q.of(0)};
        // here rho1(u) = |u0| + |u1| (the l1 norm), whose unit ball has extreme points +-e0, +-e1 (all
        // included below); a.u <= rho1(u) there proves each atom has dual norm <= 1
        for (Q[] a : List.of(atomPlus, atomMinus, atomE)) {
            for (Q[] u : List.of(new Q[]{Q.of(1), Q.of(0)}, new Q[]{Q.of(0), Q.of(1)}, new Q[]{Q.of(1, 2), Q.of(1, 2)},
                                 new Q[]{Q.of(1), Q.of(-1)}, new Q[]{Q.of(-1), Q.of(0)}, new Q[]{Q.of(0), Q.of(-1)},
                                 new Q[]{Q.of(-1, 2), Q.of(-1, 2)}, new Q[]{Q.of(-1), Q.of(1)})) {
                Q au = a[0].mul(u[0]).add(a[1].mul(u[1]));
                if (au.compareTo(rho1(edge, u)) > 0) throw new AssertionError("atom outside rho1 dual ball");
            }
        }
        boolean failsB = rho1a.equals(Q.of(1)) && rho1b.equals(Q.of(1))
            && Q.of(1, 2).sq().compareTo(Q.of(4).mul(Q.of(1).sub(Q.of(1)))) > 0;
        System.out.println("  CONTROL B (l1 segment sums): R = 1, ||x|| = 1, ||Q_H y|| >= 1/2 > 2*sqrt(0), claim FAILS: " + failsB);
        if (!failsB) throw new AssertionError("control B did not fail");

        // closed form of the two-vertex lens (derived in NOTES.md): max |y_c| = 2 sqrt(r(1-r)) for r >= 1/2;
        // the witness y = (1 - r, 2 sqrt(r(1-r))) at r = 9/10 is exactly the y above.
        Q rr = Q.of(9, 10);
        Q b2 = Q.of(4).mul(rr).mul(Q.of(1).sub(rr));
        System.out.printf("  closed form at r = 9/10: max|y_c|^2 = %s (= (3/5)^2: %s)%n", b2, b2.equals(Q.of(9, 25)));
        if (!b2.equals(Q.of(9, 25))) throw new AssertionError();
        System.out.println("ALL CHECKS PASSED (and both controls failed, as they must)");
    }

    static Q rho1(Forest f, Q[] u) {
        Q best = Q.of(0);
        for (List<Set<Integer>> p : f.partitions()) {
            Q s = Q.of(0);
            for (Set<Integer> seg : p) s = s.add(sumOn(seg, u).abs());
            if (s.compareTo(best) > 0) best = s;
        }
        return best;
    }
}
