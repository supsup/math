"""Independent replication of OAI.SegmentLenses.midpoint_lens_main on finite instances.

Written from the Lean challenge's definitions (lean/ComparatorChallenges/MidpointLenses.lean), not from
the paper's proof.

Model. For a finite ANCESTRAL set T of vertices (a finite rooted forest), every functional that is a
finite combination of coordinates e_v^* (v in T) has the same norm in X = J^* (and in B_inf) as in the
finite-dimensional space R^T with the norm dual to

    rho(u) = max over families of pairwise-disjoint segments S of  sqrt( sum_S u(S)^2 ).

Reason (argued in NOTES.md): restricting a primal test u to an ancestral set T never increases rho,
because a segment meets an ancestral set in a segment or in nothing. Adding a segment to a family only
adds a square, so the max may be taken over PARTITIONS of T into segments.

The dual unit ball is the convex hull of the atoms  sum_{S in P} a_S d_S  (P a partition, ||a||_2 <= 1,
d_S the indicator of S). Hence
  * LOWER bound: any u gives ||f|| >= f(u) / rho(u)          (exact rational: compare squares)
  * UPPER bound: any decomposition f = sum_P A_P^T z_P + r gives ||f|| <= sum_P ||z_P||_2 + ||r||_1
    (the residual r is paid with singleton atoms e_v^*, each of norm <= 1).

Parts:
  1. exact 2-vertex instance (Fractions only), true statement holds, two negative controls fail;
  2. exact closed form for the 2-vertex lens, compared with brute force;
  3. numeric (numpy) adversarial search on small trees for the largest ratio
     ||Q_H y|| / sqrt(R^2 - ||x||^2), with the best instance re-certified in exact arithmetic.

Run from this folder:  python3 replicate.py      (numpy from user site is needed for part 3 only)
"""
from fractions import Fraction as F
from math import isqrt
import itertools
import random
import sys

# ---------------------------------------------------------------- trees, segments, partitions


class Forest:
    """parent[i] = -1 for a root; nodes are numbered so that parent[i] < i."""

    def __init__(self, parent, name):
        self.parent = parent
        self.n = len(parent)
        self.name = name
        for i, p in enumerate(parent):
            assert p < i
        self.children = [[j for j in range(self.n) if parent[j] == i] for i in range(self.n)]
        self.partitions = self._partitions()

    def ancestors(self, v):
        out = []
        while v != -1:
            out.append(v)
            v = self.parent[v]
        return out  # v, parent(v), ..., root

    def is_ancestral(self, H):
        return all(a in H for v in H for a in self.ancestors(v))

    def segments(self):
        """every interval [a,b] with a an ancestor of b (same component)."""
        segs = []
        for b in range(self.n):
            chain = self.ancestors(b)
            for k in range(len(chain)):
                segs.append(frozenset(chain[: k + 1]))
        return segs

    def _partitions(self):
        """all partitions of the vertex set into segments: each non-root vertex either continues its
        parent's segment downward or starts a new one; at most one child continues a given vertex."""
        nonroots = [v for v in range(self.n) if self.parent[v] != -1]
        parts = []
        for choice in itertools.product([False, True], repeat=len(nonroots)):
            ext = dict(zip(nonroots, choice))
            ok = all(sum(1 for c in self.children[v] if ext.get(c)) <= 1 for v in range(self.n))
            if not ok:
                continue
            top = {}
            for v in range(self.n):
                top[v] = top[self.parent[v]] if ext.get(v) else v
            groups = {}
            for v in range(self.n):
                groups.setdefault(top[v], set()).add(v)
            parts.append([frozenset(g) for g in groups.values()])
        return parts


def rho_sq(T, u):
    """rho(u)^2 exactly (works for Fractions or floats)."""
    best = 0
    for P in T.partitions:
        s = sum(sum(u[v] for v in S) ** 2 for S in P)
        if s > best:
            best = s
    return best


def rho_sq_bruteforce_families(T, u):
    """rho(u)^2 over ALL disjoint families of segments (not just partitions): used to check the
    partition shortcut on small trees."""
    segs = list(set(T.segments()))
    best = 0
    for r in range(len(segs) + 1):
        for fam in itertools.combinations(segs, r):
            used = set()
            ok = True
            for S in fam:
                if used & S:
                    ok = False
                    break
                used |= S
            if ok:
                best = max(best, sum(sum(u[v] for v in S) ** 2 for S in fam))
    return best


# ---------------------------------------------------------------- exact rational sqrt bounds

SCALE = 10 ** 15


def sqrt_up(q):
    q = F(q)
    assert q >= 0
    r = isqrt(q.numerator * SCALE * SCALE // q.denominator) + 1
    return F(r, SCALE)


def sqrt_down(q):
    q = F(q)
    assert q >= 0
    r = isqrt(q.numerator * SCALE * SCALE // q.denominator)
    return F(r, SCALE)


def lower_bound(T, f, u):
    """certified rational lower bound for ||f||, from the primal test u."""
    fu = sum(F(f[v]) * F(u[v]) for v in range(T.n))
    rs = rho_sq(T, [F(x) for x in u])
    if fu <= 0 or rs == 0:
        return F(0)
    return sqrt_down(fu * fu / rs)


def upper_bound(T, f, decomposition):
    """decomposition: list of (partition index, {segment: coefficient}). Returns certified rational
    upper bound sum ||z_P||_2 + ||residual||_1."""
    rem = [F(f[v]) for v in range(T.n)]
    cost = F(0)
    for pi, coeffs in decomposition:
        P = T.partitions[pi]
        assert set(coeffs) <= set(P)
        cost += sqrt_up(sum(F(a) ** 2 for a in coeffs.values()))
        for S, a in coeffs.items():
            for v in S:
                rem[v] -= F(a)
    return cost + sum(abs(r) for r in rem)


def partition_index(T, segs):
    target = set(frozenset(s) for s in segs)
    for i, P in enumerate(T.partitions):
        if set(P) == target:
            return i
    raise KeyError(segs)


# ---------------------------------------------------------------- part 1: exact 2-vertex instance


def part1():
    print("== Part 1: exact 2-vertex instance (root r = 0, child c = 1, H = {r}) ==")
    T = Forest([-1, 0], "edge")
    # check the partition shortcut against all disjoint families on a few rational u
    for u in ([F(1), F(0)], [F(4, 5), F(-3, 5)], [F(1, 2), F(1, 3)], [F(-2), F(7)]):
        assert rho_sq(T, u) == rho_sq_bruteforce_families(T, u)
    singles = partition_index(T, [{0}, {1}])
    whole = partition_index(T, [{0, 1}])
    S0, S1, S01 = frozenset({0}), frozenset({1}), frozenset({0, 1})
    x = [F(9, 10), F(0)]
    y = [F(1, 10), F(3, 5)]
    xp = [x[i] + y[i] for i in range(2)]   # (1, 3/5)
    xm = [x[i] - y[i] for i in range(2)]   # (4/5, -3/5)
    Qy = [F(0), y[1]]                      # tail outside H = {r}
    # norms, each pinned by a matching lower and upper certificate
    cert = {
        "x": (x, [1, 0], [(singles, {S0: F(9, 10)})]),
        "x+y": (xp, [1, 0], [(singles, {S0: F(2, 5)}), (whole, {S01: F(3, 5)})]),
        "x-y": (xm, [F(4, 5), F(-3, 5)], [(singles, {S0: F(4, 5), S1: F(-3, 5)})]),
        "Q_H y": (Qy, [0, 1], [(singles, {S1: F(3, 5)})]),
    }
    vals = {}
    for k, (f, u, dec) in cert.items():
        lo, hi = lower_bound(T, f, u), upper_bound(T, f, dec)
        vals[k] = (lo, hi)
        print(f"  ||{k}|| in [{float(lo):.15f}, {float(hi):.15f}]")
        assert hi - lo < F(1, 10 ** 13)
    # these are 9/10, 1, 1, 3/5 up to the 1e-15 rounding of sqrt_up/sqrt_down
    R = F(1)
    assert vals["x+y"][1] <= R + F(1, 10 ** 14) and vals["x-y"][1] <= R + F(1, 10 ** 14)
    # with exact values: LHS^2 = 9/25, deficit = R^2 - ||x||^2 = 19/100
    lhs2, deficit = F(9, 25), R * R - F(81, 100)
    print(f"  exact: R = 1, ||x|| = 9/10, ||Q_H y|| = 3/5, deficit R^2-||x||^2 = {deficit}")
    print(f"  theorem (c = 2):   LHS^2 = {lhs2} <= 4*deficit = {4 * deficit} : {lhs2 <= 4 * deficit}")
    assert lhs2 <= 4 * deficit
    ratio = (lhs2 / deficit)
    print(f"  ratio ||Q_H y|| / sqrt(deficit) = sqrt({ratio}) = {float(ratio) ** 0.5:.6f}")
    # NEGATIVE CONTROL A: same statement with constant 1.3 in place of 2 must FAIL here
    c = F(13, 10)
    fails = lhs2 > c * c * deficit
    print(f"  CONTROL A (c = 13/10): LHS^2 = {lhs2} > c^2*deficit = {c * c * deficit} -> claim FAILS: {fails}")
    assert fails
    # NEGATIVE CONTROL B: change the definition, l1 sum over segments instead of l2
    # (dual atoms become sign vectors with l_inf coefficients). x = e_r^*, y = t e_c^*.
    # rho_1(u) = max over partitions of sum |u(S)|; for (1,0) it is 1, so ||e_r^*|| >= 1;
    # x +- y = (1, +-t) = sum of singleton atoms (1, +-1) and (1, 0) mix: (1,+-t) = t(1,+-1) + (1-t)(1,0)
    t = F(1, 2)
    def rho1(u):
        return max(sum(abs(sum(u[v] for v in S)) for S in P) for P in T.partitions)
    # dual norm of (1, s) under rho1 is max(|1|,|s|) = 1 for |s| <= 1 (unit ball = square): check
    # the lower bound with u=(1,0) and the upper bound by the convex combination above
    assert rho1([1, 0]) == 1
    xn, R1 = F(1), F(1)          # ||x|| >= 1 from u=(1,0); ||x +- y|| <= t + (1-t) = 1
    lhsB = t                     # ||(0,t)|| >= t from u = (0,1), rho1 = 1
    assert rho1([0, 1]) == 1
    failsB = lhsB * lhsB > 4 * (R1 * R1 - xn * xn)
    print(f"  CONTROL B (l1 segment sums): R = 1, ||x|| = 1, ||Q_H y|| >= {t} > 2*sqrt(0) -> claim FAILS: {failsB}")
    assert failsB
    return T


# ---------------------------------------------------------------- part 2: closed form of the 2-vertex lens


def part2():
    print("== Part 2: 2-vertex lens, closed form vs brute force ==")
    # unit ball B = conv(unit disk, +-(1,1)); horizontal slice at height b in [0,1] is
    # [-sqrt(1-b^2), 1]. Lens at x = (r,0), R = 1: max |y_c| = 1 if r <= 1/2 else 2 sqrt(r(1-r)).
    # Brute force: membership f in B  <=>  f(u) <= rho(u) for all u (support function), sampled
    # over 3600 directions; then maximize b over a grid of a.
    import math
    dirs = [(math.cos(2 * math.pi * k / 3600), math.sin(2 * math.pi * k / 3600)) for k in range(3600)]
    T = Forest([-1, 0], "edge")
    rhos = [math.sqrt(rho_sq(T, list(d))) for d in dirs]

    def in_ball(p):
        return all(p[0] * d[0] + p[1] * d[1] <= r + 1e-12 for d, r in zip(dirs, rhos))

    worst = 0.0
    for r in (0.3, 0.5, 0.6, 0.75, 0.9, 0.97):
        closed = 1.0 if r <= 0.5 else 2 * math.sqrt(r * (1 - r))
        best = 0.0
        for ia in range(-200, 201):
            a = ia / 200
            lo, hi = 0.0, 1.2
            if not (in_ball((r + a, 0.0)) and in_ball((r - a, -0.0))):
                continue
            for _ in range(40):
                mid = (lo + hi) / 2
                if in_ball((r + a, mid)) and in_ball((r - a, -mid)):
                    lo = mid
                else:
                    hi = mid
            best = max(best, lo)
        bound = 2 * math.sqrt(1 - r * r)
        worst = max(worst, abs(best - closed))
        print(f"  r = {r:4}: max|y_c| brute {best:.5f}  closed {closed:.5f}  bound 2sqrt(1-r^2) {bound:.5f}"
              f"  ratio to sqrt(1-r^2): {best / math.sqrt(1 - r * r):.4f}")
    assert worst < 5e-3
    print("  sup of ratio as r -> 1 is 2*sqrt(r/(1+r)) -> sqrt(2) = 1.41421 (theorem allows 2)")


# ---------------------------------------------------------------- part 3: numeric search, small trees


def part3():
    try:
        import numpy as np
    except ImportError:
        print("== Part 3 skipped: numpy not importable (run without -I) ==")
        return
    print("== Part 3: adversarial search on small trees (numeric, best instance re-certified exactly) ==")
    rng = np.random.default_rng(20261008)
    random.seed(20261008)

    trees = [
        (Forest([-1, 0], "edge"), [{0}]),
        (Forest([-1, 0, 1], "chain3"), [{0}, {0, 1}]),
        (Forest([-1, 0, 0], "cherry"), [{0}]),
        (Forest([-1, 0, 1, 2], "chain4"), [{0}, {0, 1}, {0, 1, 2}]),
        (Forest([-1, 0, 1, 1], "Y"), [{0}, {0, 1}]),
        (Forest([-1, 0, 0, 0], "star3"), [{0}]),
        (Forest([-1, 0, 1, 1, 0], "Y+leaf"), [{0}, {0, 1}, {0, 4}]),
        (Forest([-1, 0, -1, 2], "two edges"), [{0}, {0, 2}]),
    ]

    def mats(T):
        Gs = []
        for P in T.partitions:
            A = np.zeros((len(P), T.n))
            for i, S in enumerate(P):
                for v in S:
                    A[i, v] = 1.0
            Gs.append(A.T @ A)
        return np.array(Gs)

    def dual_norm(Ms, f, iters=200):
        """IRLS for min sum_P ||z_P|| s.t. sum A_P^T z_P = f. Returns (approx value, lambda, weights).
        Ms is the stack G_P = A_P^T A_P, so ||A_P lam||^2 = lam^T G_P lam."""
        n = len(f)
        eps = np.ones(Ms.shape[0])
        lam = np.zeros(n)
        I = 1e-14 * np.eye(n)
        for _ in range(iters):
            M = np.tensordot(eps, Ms, axes=1) + I
            lam = np.linalg.solve(M, f)
            nrm = np.sqrt(np.maximum(np.einsum("i,kij,j->k", lam, Ms, lam), 0.0))
            used = eps                      # z_P = used_P * A_P lam satisfies sum A_P^T z_P = f
            eps = np.maximum(eps * nrm, 1e-13)
        return float(eps.sum()), lam, used

    def norm_est(Ms, f, iters=200):
        if not np.any(f):
            return 0.0, np.zeros(len(f))
        up, lam, _ = dual_norm(Ms, f, iters)
        rho = float(np.sqrt(np.max(np.einsum("i,kij,j->k", lam, Ms, lam))))
        lo = float(f @ lam) / rho if rho > 0 else 0.0
        return 0.5 * (up + lo), lam

    def ratio(T, Ms, H, x, y, iters=200):
        Hmask = np.array([1.0 if v in H else 0.0 for v in range(T.n)])
        x = x * Hmask
        nx, _ = norm_est(Ms, x, iters)
        R = max(norm_est(Ms, x + y, iters)[0], norm_est(Ms, x - y, iters)[0])
        q, _ = norm_est(Ms, y * (1 - Hmask), iters)
        d = R * R - nx * nx
        if d < 1e-6 * R * R:
            return -1.0
        return q / np.sqrt(d)

    # instrument check on the 2-vertex ball, where the exact norms are known (Part 1/2)
    G2 = mats(Forest([-1, 0], "edge"))
    for f, want in (((1, 0.6), 1.0), ((1, -0.5), 1.25 ** 0.5), ((0.8, -0.6), 1.0), ((0, 1), 1.0)):
        got = norm_est(G2, np.array(f, dtype=float))[0]
        assert abs(got - want) < 1e-6, (f, got, want)
    print("  IRLS instrument matches exact 2-vertex norms to 1e-6", flush=True)
    def certify(T, Ms, f):
        fr = [F(float(c)).limit_denominator(10 ** 9) for c in f]
        up, lam, eps = dual_norm(Ms, np.array([float(c) for c in fr]), iters=4000)
        lo = lower_bound(T, fr, [F(float(c)).limit_denominator(10 ** 12) for c in lam])
        # decomposition z_P = eps_P A_P lam, rebuilt in exact arithmetic; residual paid in l1
        dec = []
        for pi, P in enumerate(T.partitions):
            if eps[pi] <= 1e-12:
                continue
            dec.append((pi, {S: F(float(eps[pi] * sum(lam[v] for v in S))).limit_denominator(10 ** 12)
                             for S in P}))
        hi = upper_bound(T, fr, dec)
        return fr, lo, hi

    def certify_instance(T, Ms, H, x, y):
        """exact rational x (on H), y; certified intervals; returns (holds, ratio_lo, ratio_hi)."""
        xr = [F(float(x[v])).limit_denominator(10 ** 9) if v in H else F(0) for v in range(T.n)]
        yr = [F(float(c)).limit_denominator(10 ** 9) for c in y]
        _, xlo, xhi = certify(T, Ms, xr)
        _, plo, phi = certify(T, Ms, [xr[i] + yr[i] for i in range(T.n)])
        _, mlo, mhi = certify(T, Ms, [xr[i] - yr[i] for i in range(T.n)])
        _, qlo, qhi = certify(T, Ms, [F(0) if v in H else yr[v] for v in range(T.n)])
        Rup = max(phi, mhi)          # a valid R for the theorem's hypotheses
        holds = qhi * qhi <= 4 * (Rup * Rup - xhi * xhi)
        Rlo = max(plo, mlo)          # the true max(||x+y||,||x-y||) lies in [Rlo, Rup]
        # ratio at the true R = max(||x+y||, ||x-y||):  q / sqrt(R^2 - ||x||^2)
        rlo = float(qlo) / max(float(Rup * Rup - xlo * xlo), 1e-300) ** 0.5
        d_lo = float(Rlo * Rlo - xhi * xhi)
        rhi = float(qhi) / d_lo ** 0.5 if d_lo > 0 else float("inf")
        return holds, rlo, rhi, (xlo, xhi, plo, phi, mlo, mhi, qlo, qhi, Rup)

    overall = []
    for T, Hs in trees:
        Ms = mats(T)
        # sanity: the partition shortcut agrees with all disjoint families (small trees)
        if T.n <= 4:
            for _ in range(5):
                u = [F(random.randint(-5, 5), random.randint(1, 4)) for _ in range(T.n)]
                assert rho_sq(T, u) == rho_sq_bruteforce_families(T, u)
        for H in Hs:
            assert T.is_ancestral(H)
            best = (-1, None, None)
            for restart in range(4):
                x = rng.normal(size=T.n)
                y = rng.normal(size=T.n) * 0.3
                cur = ratio(T, Ms, H, x, y, 150)
                step = 0.3
                for it in range(150):
                    x2 = x + step * rng.normal(size=T.n)
                    y2 = y + step * rng.normal(size=T.n)
                    r2 = ratio(T, Ms, H, x2, y2, 150)
                    if r2 > cur:
                        x, y, cur = x2, y2, r2
                    else:
                        step *= 0.98
                if cur > best[0]:
                    best = (cur, x.copy(), y.copy())
            coarse, x, y = best
            # refine with an accurate instrument (2000 IRLS steps) so the optimizer cannot farm error
            cur = ratio(T, Ms, H, x, y, 2000)
            step = 0.02
            for it in range(60):
                x2 = x + step * rng.normal(size=T.n)
                y2 = y + step * rng.normal(size=T.n)
                r2 = ratio(T, Ms, H, x2, y2, 2000)
                if r2 > cur:
                    x, y, cur = x2, y2, r2
                else:
                    step *= 0.97
            holds, rlo, rhi, _ = certify_instance(T, Ms, H, x, y)
            overall.append((rlo, T.name, sorted(H)))
            print(f"  {T.name:9} H={str(sorted(H)):9}: coarse {coarse:.4f} refined {cur:.4f} | certified ratio in "
                  f"[{rlo:.4f}, {rhi:.4f}], theorem instance certified: {holds}", flush=True)
            assert holds
    top = max(overall)
    print(f"  largest certified ratio LOWER bound: {top[0]:.5f} ({top[1]}, H={top[2]}); theorem constant 2; "
          f"sqrt(2) = {2 ** 0.5:.5f}")

if __name__ == "__main__":
    part1()
    part2()
    part3()
    print("ALL CHECKS DONE")
