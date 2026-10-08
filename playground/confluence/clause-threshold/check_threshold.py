#!/usr/bin/env python3
"""Independent finite checks for OAI.FixedClauseThreshold.main (random proper k-SAT).

Model (from the challenge, read literally):
  ProperClause n k = maps Fin n -> Option Bool with exactly k `some` entries
                   = k distinct variables with a sign each; N(n,k) = C(n,k) * 2^k of them.
  Formula n k m    = m-tuples of proper clauses (ordered, with replacement), N^m of them.
  properSATProbability n k m = #satisfiable tuples / N^m  (real division; x/0 = 0).

Part A: exact integer DP over the set of surviving assignments (bitmask of 2^n bits).
Part B: the solution's `center n k` = E[sum_{j=1}^{2^(k+1) n} alive_j] / n, exact for tiny n.
Part C: seeded Monte Carlo with a small DPLL solver, densities well below / above 4.27.
Controls: a deliberately wrong first-moment bound (k=2 kill fraction 1/4 in place of 1/8)
must be violated by the exact numbers; a deliberately wrong Monte Carlo expectation must fail.
"""
import itertools, math, random, sys
from fractions import Fraction

def clauses(n, k):
    """All proper clauses as satisfying-set bitmasks over assignments a in [0, 2^n)."""
    out = []
    for vs in itertools.combinations(range(n), k):
        for signs in itertools.product((False, True), repeat=k):
            mask = 0
            for a in range(1 << n):
                if any(((a >> v) & 1) == int(s) for v, s in zip(vs, signs)):
                    mask |= 1 << a
            out.append(mask)
    return out

def sat_counts(n, k, mmax):
    """sat[m] = number of satisfiable m-tuples, exact integers, m = 0..mmax."""
    cl = clauses(n, k)
    full = (1 << (1 << n)) - 1
    state = {full: 1}
    sat = [1]  # m = 0: the empty tuple is satisfiable (any n, including n < k)
    for m in range(1, mmax + 1):
        nxt = {}
        for S, c in state.items():
            for C in cl:
                T = S & C
                if T:
                    nxt[T] = nxt.get(T, 0) + c
        state = nxt
        sat.append(sum(state.values()))
    return sat, len(cl)

def prob(n, k, m, cache={}):
    key = (n, k)
    if key not in cache or len(cache[key][0]) <= m:
        cache[key] = sat_counts(n, k, max(m, 2))
    sat, N = cache[key]
    total = N ** m
    return Fraction(sat[m], total) if total else Fraction(0)  # Lean: x / 0 = 0

# ---------------- Part C: DPLL ----------------
def random_formula(rng, n, k, m):
    F = []
    for _ in range(m):
        vs = rng.sample(range(n), k)
        F.append([v + 1 if rng.random() < 0.5 else -(v + 1) for v in vs])
    return F

def dpll(F, n):
    sys.setrecursionlimit(10000)
    assign = {}
    def solve(clauses):
        # unit propagation
        clauses = [c[:] for c in clauses]
        local = []
        while True:
            unit = None
            for c in clauses:
                if len(c) == 0:
                    for v in local: assign.pop(v, None)
                    return False
                if len(c) == 1:
                    unit = c[0]; break
            if unit is None: break
            assign[abs(unit)] = unit > 0; local.append(abs(unit))
            clauses = [[l for l in c if l != -unit] for c in clauses if unit not in c]
        if not clauses: return True
        # branch on most frequent variable
        cnt = {}
        for c in clauses:
            for l in c: cnt[l] = cnt.get(l, 0) + 1
        lit = max(cnt, key=lambda l: (cnt[l] + cnt.get(-l, 0), cnt[l]))
        for choice in (lit, -lit):
            assign[abs(choice)] = choice > 0
            reduced = [[l for l in c if l != -choice] for c in clauses if choice not in c]
            if solve(reduced): return True
            assign.pop(abs(choice), None)
        for v in local: assign.pop(v, None)
        return False
    ok = solve(F)
    return ok

def wilson(s, t, z=1.96):
    p = s / t; d = 1 + z*z/t
    c = (p + z*z/(2*t)) / d; h = z*math.sqrt(p*(1-p)/t + z*z/(4*t*t)) / d
    return c - h, c + h

def main():
    fails = 0
    def check(name, ok, detail=""):
        nonlocal fails
        print(("PASS " if ok else "FAIL ") + name + (": " + detail if detail else ""))
        if not ok: fails += 1

    k = 3
    # A0: clause counts C(n,k) 2^k
    for n in range(0, 7):
        check(f"A0 card ProperClause n={n} k=3", len(clauses(n, 3)) == math.comb(n, 3) * 8,
              str(len(clauses(n, 3))))
    # A1: degenerate conventions
    check("A1 n=2<k=3, m=0 -> 1", prob(2, 3, 0) == 1)
    check("A1 n=2<k=3, m=1 -> 0 (x/0 = 0)", prob(2, 3, 1) == 0)
    # A2: exact probabilities, monotone in m, first-moment bound P <= 2^n (7/8)^m
    print("exact properSATProbability n k=3 m (first unsat-possible m is 2^n / ... )")
    violations_wrong = []
    for n, mmax in ((3, 20), (4, 64)):
        sat, N = sat_counts(n, k, mmax)
        P = [Fraction(sat[m], N ** m) for m in range(mmax + 1)]
        check(f"A2 n={n} monotone nonincreasing in m", all(P[i+1] <= P[i] for i in range(mmax)))
        check(f"A2 n={n} first moment P <= 2^n (7/8)^m",
              all(P[m] <= Fraction(2**n) * Fraction(7, 8)**m for m in range(mmax + 1)))
        # Smallest unsatisfiable proper 3-CNF needs 2^3 = 8 clauses (on one variable triple)
        firstunsat = next(m for m in range(mmax + 1) if P[m] < 1)
        check(f"A2 n={n} P=1 exactly for m<8 and P<1 at m=8", firstunsat == 8, f"first m with P<1: {firstunsat}")
        for m in (8, 10, 16, 3*n, 4*n, 5*n, 8*n):
            if m <= mmax:
                print(f"   n={n} m={m:3d} P={float(P[m]):.6f}  ({sat[m]} / {N}^{m})")
        # center n k with cap 2^(k+1) n = 16 n
        cap = 2 ** (k + 1) * n
        if cap <= mmax:
            center = sum(P[1:cap + 1]) / n
            lb = math.exp(-2) / 16
            print(f"   center({n},3) = {float(center):.6f}  (solution's eventual bounds: {lb:.5f} <= center <= 9)")
            check(f"B center({n},3) within [e^-2/16, 9]", lb <= center <= 9)
        # NEGATIVE CONTROL: wrong bound with kill fraction 1/4 (2-SAT's) instead of 1/8
        for m in range(mmax + 1):
            if P[m] > Fraction(2**n) * Fraction(3, 4)**m:
                violations_wrong.append((n, m, float(P[m]), float(Fraction(2**n) * Fraction(3, 4)**m)))
    ctrl = bool(violations_wrong)
    print(f"CONTROL wrong bound 2^n(3/4)^m: {len(violations_wrong)} violations, e.g. {violations_wrong[:2]}")
    check("CONTROL-A wrong first-moment bound is refuted by exact numbers", ctrl)

    # Part C: Monte Carlo
    rng = random.Random(20261008)
    T = 200
    print(f"Monte Carlo k=3, seed 20261008, {T} formulas per cell, DPLL")
    res = {}
    for c in (2.0, 3.0, 4.27, 6.0, 8.0):
        for n in (20, 40, 80):
            m = math.floor(c * n)
            s = sum(dpll(random_formula(rng, n, 3, m), n) for _ in range(T))
            lo, hi = wilson(s, T)
            res[(c, n)] = s / T
            print(f"   c={c:4.2f} n={n:3d} m={m:4d}  P^={s/T:.3f}  95% CI [{lo:.3f},{hi:.3f}]")
    check("C c=2.0 n=80 P^ >= 0.95", res[(2.0, 80)] >= 0.95)
    check("C c=6.0 n=80 P^ <= 0.05", res[(6.0, 80)] <= 0.05)
    check("C c=3.0 trend nondecreasing in n (20 -> 80)", res[(3.0, 80)] >= res[(3.0, 20)])
    check("C c=6.0 trend nonincreasing in n (20 -> 80)", res[(6.0, 80)] <= res[(6.0, 20)])
    # first-moment sanity: above ln2 / -ln(7/8) = 5.19 the expectation 2^n (7/8)^m -> 0
    alpha1 = math.log(2) / -math.log(7 / 8)
    print(f"   first-moment upper bound on any threshold for k=3: {alpha1:.4f}")
    # NEGATIVE CONTROL: claim the wrong side (c=6 behaves subcritically) must fail
    wrong = res[(6.0, 80)] >= 0.95
    check("CONTROL-C wrong-side claim 'P(c=6,n=80) >= 0.95' is false", not wrong,
          f"observed {res[(6.0,80)]:.3f}")
    print("RESULT", "ALL PASS" if fails == 0 else f"{fails} FAIL")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
