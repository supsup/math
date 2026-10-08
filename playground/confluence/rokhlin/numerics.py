"""Illustrations of the DEFINITIONS in lean/ComparatorChallenges/Rokhlin.lean.

NOT evidence for the theorem: Rokhlin's problem is about every mixing system, and every system
below is either Bernoulli (where mixing of all orders is classical) or a negative control.

Run: python3 -I numerics.py   (stdlib only; seeded, deterministic)

Quantity measured, for k = 3 sets and gaps (g1, g2) as in Lean's layoutTime (times 0, g1, g1+g2):
    corr = mu(A  ∩  T^{-g1} B  ∩  T^{-(g1+g2)} C)      vs     mu(A) mu(B) mu(C)
"""
import math
import random
from fractions import Fraction

random.seed(20261008)


# ---- Lean's layoutTime, transcribed --------------------------------------------------------
def layout_time(gaps, i):
    """layoutTime gaps i = sum_{j < i} gaps j   (gaps : Fin (k-1) -> PNat, i : Fin k)."""
    return sum(g for j, g in enumerate(gaps) if j < i)


def check_layout():
    gaps = (5, 7, 11)  # k = 4
    times = [layout_time(gaps, i) for i in range(4)]
    assert times == [0, 5, 12, 23], times
    print(f"layoutTime (5,7,11) -> times {times}  (successive differences are exactly the gaps)")


# ---- 1. Bernoulli(p) two-sided shift, cylinder sets: EXACT --------------------------------
# A cylinder set fixes coordinates in a window; T^{-t} of it fixes the window shifted by t.
# mu(intersection) = product over coordinates of the constraint probability (0 if two
# constraints on one coordinate conflict). Exact rational arithmetic.
P = Fraction(3, 10)


def cyl_measure(constraints):
    """constraints: list of dict coord->symbol. Returns exact measure of the intersection."""
    merged = {}
    for c in constraints:
        for pos, s in c.items():
            if merged.get(pos, s) != s:
                return Fraction(0)
            merged[pos] = s
    m = Fraction(1)
    for s in merged.values():
        m *= P if s == 1 else 1 - P
    return m


def shift(c, t):
    return {pos + t: s for pos, s in c.items()}


def bernoulli():
    A = {0: 1, 1: 0, 2: 1}
    B = {0: 1, 1: 1}
    C = {0: 0, 2: 0, 3: 1}
    target = cyl_measure([A]) * cyl_measure([B]) * cyl_measure([C])
    print(f"\n[Bernoulli(3/10) shift, exact] mu(A)mu(B)mu(C) = {target} = {float(target):.6f}")
    for g in [1, 2, 3, 4, 10, 100]:
        v = cyl_measure([A, shift(B, g), shift(C, 2 * g)])
        print(f"  gaps ({g},{g}): {float(v):.6f}   exact equal to product: {v == target}")
    # unequal gaps: only min gap matters
    v = cyl_measure([A, shift(B, 50), shift(C, 50 + 1)])
    print(f"  gaps (50,1):  {float(v):.6f}   (second gap small -> not the product: {v != target})")


# ---- 2. Doubling map x -> 2x mod 1 (non-invertible; Lean's T must be invertible) ----------
# x is a random BITS-bit dyadic, so T^n x = (x << n) mod 2^BITS is exact while n << BITS.
BITS = 400
N_MC = 200_000


def doubling():
    A, B, C = (0.0, 0.3), (0.2, 0.7), (0.5, 0.9)
    target = 0.3 * 0.5 * 0.4
    mask = (1 << BITS) - 1
    xs = [random.getrandbits(BITS) for _ in range(N_MC)]
    se = math.sqrt(target * (1 - target) / N_MC)
    print(f"\n[doubling map, Monte Carlo n={N_MC}, exact {BITS}-bit orbits] product = {target:.4f}, "
          f"1-sigma = {se:.4f}")

    def inside(xint, iv):
        u = xint / (1 << BITS)
        return iv[0] <= u < iv[1]
    for g1, g2 in [(1, 1), (2, 3), (5, 5), (20, 20), (60, 90)]:
        cnt = 0
        for x in xs:
            if inside(x, A) and inside((x << g1) & mask, B) and inside((x << (g1 + g2)) & mask, C):
                cnt += 1
        print(f"  gaps ({g1},{g2}): {cnt / N_MC:.4f}   deviation {cnt / N_MC - target:+.4f}")


# ---- 3. Arnold cat map on the torus (invertible, mixing; in the class Lean quantifies over) -
# (x, y) -> (2x + y, x + y) mod 1. Points are random Q-adic lattice points with Q = 2^BITS;
# the integer map mod Q is exact. Expansion is phi^2 ~ 2.618/step, so 400 bits keeps the
# sample faithful to Lebesgue for n << 400 / log2(2.618) ~ 288 steps.
def cat():
    Q = 1 << BITS
    A, B, C = ((0.0, 0.5), (0.0, 0.6)), ((0.3, 0.8), (0.1, 0.5)), ((0.1, 0.4), (0.0, 1.0))
    mA, mB, mC = 0.5 * 0.6, 0.5 * 0.4, 0.3 * 1.0
    target = mA * mB * mC
    pts = [(random.getrandbits(BITS), random.getrandbits(BITS)) for _ in range(N_MC // 2)]
    se = math.sqrt(target * (1 - target) / len(pts))
    print(f"\n[Arnold cat map, Monte Carlo n={len(pts)}] product = {target:.4f}, 1-sigma = {se:.4f}")

    def inside(p, R):
        x, y = p[0] / Q, p[1] / Q
        return R[0][0] <= x < R[0][1] and R[1][0] <= y < R[1][1]

    def it(p, n):
        x, y = p
        for _ in range(n):
            x, y = (2 * x + y) % Q, (x + y) % Q
        return x, y
    for g1, g2 in [(1, 1), (2, 2), (4, 4), (10, 10), (30, 50)]:
        cnt = 0
        for p in pts:
            if not inside(p, A):
                continue
            q = it(p, g1)
            if not inside(q, B):
                continue
            if inside(it(q, g2), C):
                cnt += 1
        print(f"  gaps ({g1},{g2}): {cnt / len(pts):.4f}   deviation {cnt / len(pts) - target:+.4f}")


# ---- 4. NEGATIVE CONTROL: irrational rotation x -> x + alpha (invertible, NOT mixing) ------
# Exact interval arithmetic (floats only in the endpoints; no Monte Carlo).
ALPHA = (math.sqrt(5) - 1) / 2


def circ_pieces(a, b):
    a, b = a % 1.0, (a % 1.0) + (b - a)
    return [(a, b)] if b <= 1.0 else [(a, 1.0), (0.0, b - 1.0)]


def inter_len(sets):
    """sets: list of (a, b) arcs (length < 1). Lebesgue measure of the intersection."""
    cur = circ_pieces(*sets[0])
    for s in sets[1:]:
        nxt = []
        for (a, b) in cur:
            for (c, d) in circ_pieces(*s):
                lo, hi = max(a, c), min(b, d)
                if hi > lo:
                    nxt.append((lo, hi))
        cur = nxt
    return sum(b - a for a, b in cur)


def rotation():
    A = (0.0, 0.4)
    m = 0.4
    print(f"\n[NEGATIVE CONTROL: rotation by golden alpha, exact] mu(A)^2 = {m * m:.4f}, mu(A)^3 = {m ** 3:.4f}")
    # T^{-n} A = A - n alpha. Fibonacci n: ||n alpha|| -> 0, so the 2-correlation -> mu(A).
    fib = [1, 2]
    while fib[-1] < 10 ** 6:
        fib.append(fib[-1] + fib[-2])
    print("  2-fold, n = Fibonacci (mixing would need -> 0.16):")
    for n in fib[-6:]:
        v = inter_len([A, (A[0] - n * ALPHA, A[1] - n * ALPHA)])
        print(f"    n={n:>7}: mu(A ∩ T^-n A) = {v:.4f}")
    print("  3-fold, gaps (F, F') consecutive Fibonacci (3-mixing would need -> 0.064):")
    for g1, g2 in zip(fib[-7:-1], fib[-6:]):
        t1, t2 = g1, g1 + g2
        v = inter_len([A, (A[0] - t1 * ALPHA, A[1] - t1 * ALPHA), (A[0] - t2 * ALPHA, A[1] - t2 * ALPHA)])
        print(f"    gaps ({g1},{g2}): {v:.4f}")
    # and generic large n wander rather than converge:
    vals = [inter_len([A, (A[0] - n * ALPHA, A[1] - n * ALPHA)]) for n in range(10 ** 5, 10 ** 5 + 2000)]
    print(f"  2-fold over n in [1e5, 1e5+2000): min {min(vals):.4f} max {max(vals):.4f} "
          f"(Cesaro mean {sum(vals) / len(vals):.4f}: ergodic, so the AVERAGE -> 0.16, the sequence does not)")


if __name__ == "__main__":
    check_layout()
    bernoulli()
    doubling()
    cat()
    rotation()
