#!/usr/bin/env python3
"""Independent checks around OAI.common_bases_fpras (CommonBasesFPRAS challenge).

Run: python3 -I common_bases.py            (exit 0 iff every check and every control behaves)

What this does NOT do: it does not run the Lean program `fprasBlock.code`. That program is
compiled inside Lean from an expression language and is not extracted here. The estimator
below is MY reconstruction of the annealing/telescoping layer of the paper's reduction, with an
EXACT sampler over transversals; it tests the reduction and the telescoping arithmetic, not the
paper's Markov chain or its mixing proof.

Matroids are given as a set of bases (bitmasks over n elements), which is the Mathlib
`Matroid.IsBase` view; independence = subset of some basis.
"""
import itertools
import math
import random
import sys
from fractions import Fraction

# ---------------------------------------------------------------- matroid constructions

def popcount(x):
    return bin(x).count("1")


def is_matroid(n, bases):
    """Basis exchange axiom, brute force; plus nonempty."""
    if not bases:
        return False
    bs = set(bases)
    for a in bs:
        for b in bs:
            for e in range(n):
                if (a >> e) & 1 and not (b >> e) & 1:
                    if not any((b >> f) & 1 and not (a >> f) & 1 and ((a & ~(1 << e)) | (1 << f)) in bs
                               for f in range(n)):
                        return False
    return True


def bases_from_indep(n, indep):
    """indep: predicate on bitmasks. Bases = maximal independent sets."""
    ind = [m for m in range(1 << n) if indep(m)]
    r = max(popcount(m) for m in ind)
    return frozenset(m for m in ind if popcount(m) == r)


def uniform(r, n):
    return frozenset(m for m in range(1 << n) if popcount(m) == r)


def partition(blocks, n):
    """blocks: list of element lists, capacity 1 each; elements outside every block are loops."""
    def indep(m):
        if any((m >> e) & 1 for e in range(n) if not any(e in b for b in blocks)):
            return False
        return all(sum((m >> e) & 1 for e in b) <= 1 for b in blocks)
    return bases_from_indep(n, indep)


def graphic(edges, nv):
    n = len(edges)

    def indep(m):
        parent = list(range(nv))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for i, (u, v) in enumerate(edges):
            if (m >> i) & 1:
                a, b = find(u), find(v)
                if a == b:
                    return False
                parent[a] = b
        return True
    return bases_from_indep(n, indep)


def gf2_rank(vectors):
    basis = []
    for v in vectors:
        for b in basis:
            v = min(v, v ^ b)
        if v:
            basis.append(v)
    return len(basis)


def linear_gf2(cols):
    n = len(cols)
    return bases_from_indep(n, lambda m: gf2_rank([cols[i] for i in range(n) if (m >> i) & 1])
                            == popcount(m))


def rank_fn(bases):
    return lambda A: max(popcount(A & b) for b in bases)

# ---------------------------------------------------------------- counting channels

def count_direct(bases1, bases2):
    """Channel 1: literal Lean definition, #{A : A is a base of M1 and of M2}."""
    return len(set(bases1) & set(bases2))


def count_via_paired_reduction(n, bases1, bases2, use_dual=True):
    """Channel 2: paired reduction of the paper (Sec. 2). Build K = M1 (+) M2* on 2n elements
    EXPLICITLY as a basis family (dual bases = complements; direct-sum bases = unions), then count
    transversals S(A) = {x_i : i in A} u {y_i : i not in A} that are bases of K.
    use_dual=False is the NEGATIVE CONTROL (K = M1 (+) M2, which is wrong)."""
    full = (1 << n) - 1
    b2 = [full & ~b for b in bases2] if use_dual else list(bases2)
    K = {b1 | (c << n) for b1 in bases1 for c in b2}
    return sum(1 for A in range(1 << n) if (A | ((full & ~A) << n)) in K)


def defect(n, r, rk1, rk2, A):
    """d(S(A)) = n - rank_K(S(A)) = (|A| - r1(A)) + (r - r2(A))  (derived from the dual-rank formula)."""
    return (popcount(A) - rk1(A)) + (r - rk2(A))


def defect_via_K(n, bases1, bases2, A):
    full = (1 << n) - 1
    K = [b1 | ((full & ~b2) << n) for b1 in bases1 for b2 in bases2]
    S = A | ((full & ~A) << n)
    return n - max(popcount(S & k) for k in K)


def permanent_ryser(M):
    n = len(M)
    tot = 0
    for sub in range(1, 1 << n):
        cols = [j for j in range(n) if (sub >> j) & 1]
        p = 1
        for i in range(n):
            p *= sum(M[i][j] for j in cols)
        tot += (-1) ** len(cols) * p
    return (-1) ** n * tot

# ---------------------------------------------------------------- my reconstruction of the annealing layer

def anneal_estimate(n, r, rk1, rk2, eps, samples, rng, q_final=None):
    """c0(q) = sum over the 2^n transversals of q^d.  c0(1) = 2^n, c0(q) -> Z as q -> 0, and
    Z <= c0(q) <= Z + 2^n q.  Telescoping: Z ~= 2^n * prod_i E_{pi_{q_i}}[(q_{i+1}/q_i)^d].
    Sampler is EXACT (enumerate 2^n), so this tests the reduction + telescoping, not mixing."""
    ds = [defect(n, r, rk1, rk2, A) for A in range(1 << n)]
    if 0 not in ds:
        return Fraction(0)                    # the Lean statement demands output 0 when Z = 0
    if q_final is None:
        q_final = eps / (2 ** (n + 2))        # => c0(q_final) <= Z (1 + eps/4) since Z >= 1
    step = 1.0 / (1.0 + 1.0 / max(n, 1))      # ratio >= (1+1/n)^{-n} >= 1/e per stage
    q, est = 1.0, float(2 ** n)
    while q > q_final:
        q2 = max(q * step, q_final)
        w = [q ** d for d in ds]
        draws = rng.choices(range(1 << n), weights=w, k=samples)
        est *= sum((q2 / q) ** ds[s] for s in draws) / samples
        q = q2
    return est


def metropolis_single_flip_stuck(n, r, rk1, rk2, q, steps, rng):
    """Observation only: single-pair-flip Metropolis on transversals at small q. Returns the number
    of distinct common bases visited from a start at one common basis."""
    ds = [defect(n, r, rk1, rk2, A) for A in range(1 << n)]
    cur = ds.index(0)
    seen = {cur}
    for _ in range(steps):
        nxt = cur ^ (1 << rng.randrange(n))
        if rng.random() < min(1.0, q ** (ds[nxt] - ds[cur])):
            cur = nxt
        if ds[cur] == 0:
            seen.add(cur)
    return len(seen), ds.count(0)

# ---------------------------------------------------------------- instances

def instances(rng):
    out = []
    K4 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    gK4 = graphic(K4, 4)
    out.append(("graphic K4 vs itself", 6, gK4, gK4, 16))                     # Cayley: 4^2
    # K_{3,3}: edges (i,j) indexed 3i+j; M1 = one edge per left vertex, M2 = per right vertex
    left = [[3 * i + j for j in range(3)] for i in range(3)]
    right = [[3 * i + j for i in range(3)] for j in range(3)]
    out.append(("partition x partition = perfect matchings of K33", 9,
                partition(left, 9), partition(right, 9), 6))
    out.append(("U(3,6) vs U(3,6)", 6, uniform(3, 6), uniform(3, 6), 20))
    # C4 with a chord vs a differently labelled C4 with a chord (common spanning trees)
    g1 = graphic([(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)], 4)
    g2 = graphic([(0, 1), (1, 2), (2, 3), (0, 2), (3, 0)][::-1], 4)
    out.append(("two graphic matroids, permuted labels", 5, g1, g2, None))
    # rank mismatch -> Z = 0 (Lean requires equal rank; brute force confirms 0 anyway)
    out.append(("U(2,5) vs U(3,5) (no common base)", 5, uniform(2, 5), uniform(3, 5), 0))
    # disjoint supports: Z = 0 with equal rank
    out.append(("partition {0,1},{2} vs {3,4},{2}", 5, partition([[0, 1], [2]], 5),
                partition([[3, 4], [2]], 5), 0))
    # random bipartite graphs -> permanent (Ryser) as a third, independent oracle
    for t in range(4):
        k = 3 + (t % 2)
        while True:  # no isolated vertex: else partition ranks drop below k and bases != matchings
            M = [[1 if rng.random() < 0.65 else 0 for _ in range(k)] for _ in range(k)]
            if all(any(row) for row in M) and all(any(M[i][j] for i in range(k)) for j in range(k)):
                break
        edges = [(i, j) for i in range(k) for j in range(k) if M[i][j]]
        n = len(edges)
        if n > 12:
            continue
        L = [[e for e, (i, j) in enumerate(edges) if i == a] for a in range(k)]
        R = [[e for e, (i, j) in enumerate(edges) if j == b] for b in range(k)]
        out.append((f"random bipartite {k}x{k} ({n} edges) vs Ryser permanent", n,
                    partition(L, n), partition(R, n), permanent_ryser(M)))
    # random GF(2) linear matroids of equal rank
    for t in range(6):
        n, r = 6, 3
        while True:
            c1 = [rng.randrange(1, 8) for _ in range(n)]
            c2 = [rng.randrange(1, 8) for _ in range(n)]
            if gf2_rank(c1) == r and gf2_rank(c2) == r:
                break
        out.append((f"random binary rank-3 pair #{t}", n, linear_gf2(c1), linear_gf2(c2), None))
    return out

# ---------------------------------------------------------------- main

def main():
    rng = random.Random(20261008)
    fails = []

    def check(ok, msg):
        print(("PASS " if ok else "FAIL ") + msg)
        if not ok:
            fails.append(msg)

    insts = instances(rng)
    control_reduction_caught = False
    for name, n, b1, b2, known in insts:
        check(is_matroid(n, b1) and is_matroid(n, b2), f"[{name}] both families satisfy basis exchange")
        z1 = count_direct(b1, b2)
        z2 = count_via_paired_reduction(n, b1, b2)
        zbad = count_via_paired_reduction(n, b1, b2, use_dual=False)
        if zbad != z1:
            control_reduction_caught = True
        check(z1 == z2, f"[{name}] direct count {z1} == paired-reduction count {z2}")
        if known is not None:
            check(z1 == known, f"[{name}] count {z1} == independently known value {known}")
        r1 = popcount(next(iter(b1)))
        r2 = popcount(next(iter(b2)))
        if r1 == r2:
            rk1, rk2 = rank_fn(b1), rank_fn(b2)
            ok = all(defect(n, r1, rk1, rk2, A) == defect_via_K(n, b1, b2, A) for A in range(1 << n))
            check(ok, f"[{name}] defect formula (|A|-r1(A))+(r-r2(A)) == n - rank_K(S(A)) for all A")
    check(control_reduction_caught,
          "NEGATIVE CONTROL: reduction with M2 instead of M2* disagrees with brute force on >=1 instance")

    # wrong-count control: the comparator must reject an off-by-one claim
    name, n, b1, b2, known = insts[0]
    check(count_direct(b1, b2) + 1 != known, "NEGATIVE CONTROL: claimed count 17 for K4 is rejected")

    # estimator: Lean-shaped guarantee  P[(1-eps)Z <= z <= (1+eps)Z] >= 1 - delta, and Z=0 -> z=0
    eps, delta, runs, samples = 0.25, 0.25, 40, 1500
    ctrl_caught = False
    for name, n, b1, b2, known in insts:
        r1 = popcount(next(iter(b1)))
        if r1 != popcount(next(iter(b2))) or n > 9:
            continue
        rk1, rk2 = rank_fn(b1), rank_fn(b2)
        Z = count_direct(b1, b2)
        good = sum(1 for _ in range(runs)
                   if (1 - eps) * Z <= anneal_estimate(n, r1, rk1, rk2, eps, samples, rng) <= (1 + eps) * Z)
        check(good >= (1 - delta) * runs, f"[{name}] estimator within (1+-{eps})Z in {good}/{runs} runs, Z={Z}")
        if Z > 0:
            bad = sum(1 for _ in range(runs // 4)
                      if (1 - eps) * Z <= anneal_estimate(n, r1, rk1, rk2, eps, samples, rng, q_final=0.5)
                      <= (1 + eps) * Z)
            if bad < (1 - delta) * (runs // 4):
                ctrl_caught = True
    check(ctrl_caught, "NEGATIVE CONTROL: estimator stopped at q=1/2 (too early) fails the accuracy test")

    # observation: single-flip chain at small q, i.e. why the paper adds defect states
    name, n, b1, b2, known = insts[2]  # U(3,6) pair, 20 common bases
    r = 3
    seen, total = metropolis_single_flip_stuck(n, r, rank_fn(b1), rank_fn(b2), 1e-6, 20000, rng)
    print(f"OBSERVATION [{name}] single-flip Metropolis at q=1e-6: visited {seen}/{total} common bases in 20000 steps")

    print("ALL OK" if not fails else f"{len(fails)} FAILURE(S)")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
