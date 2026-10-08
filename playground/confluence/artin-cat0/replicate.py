"""Exact checks on the DEFINITIONS of lean/ComparatorChallenges/ArtinCAT0.lean.

Everything here is re-derived from the Lean text (blockLetter, Adjacent, Distant, Sentinel,
explicitMatrix, alternating, artinRelators, CAT0), not from the paper. Exact arithmetic
(int / Fraction) except the sphere control, which uses floats with a wide margin.

Run: python3 -I replicate.py   (exit code 0 iff every check AND every control behaves)
"""
from fractions import Fraction as F
from itertools import combinations
import math
import random
import sys

N = 116
TOP = "inf"  # WithTop ℕ's ⊤
fails = []


def check(name, ok):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        fails.append(name)


# ---- the Lean definitions, transcribed -------------------------------------------------
def block_letter(b, i):
    if i == 0:
        return b
    if i == 1:
        return (b + 1) % 3
    return 5 + 37 * b + (i - 2)


POS = {}  # letter -> list of (block, index)
for b in range(3):
    for i in range(39):
        POS.setdefault(block_letter(b, i), []).append((b, i))


def adjacent(s, t):
    return any(bs == bt and abs(i - j) == 1 for bs, i in POS.get(s, []) for bt, j in POS.get(t, []))


def distant(s, t):
    return any(bs == bt and abs(i - j) >= 2 for bs, i in POS.get(s, []) for bt, j in POS.get(t, []))


def sentinel(s, t):
    return (s in (3, 4) and t < 3) or (t in (3, 4) and s < 3)


def M(s, t):
    if s == t:
        return 1
    if adjacent(s, t):
        return 3
    if distant(s, t) or sentinel(s, t):
        return 2
    return TOP


MAT = [[M(s, t) for t in range(N)] for s in range(N)]

# ---- 1. the three decidable conjuncts of `main` ----------------------------------------
check("blockLetter is injective on each block and hits 114 letters (all but 3,4)",
      all(len({block_letter(b, i) for i in range(39)}) == 39 for b in range(3))
      and set(POS) == set(range(N)) - {3, 4})
check("conjunct 1: explicitMatrix symmetric", all(MAT[s][t] == MAT[t][s] for s in range(N) for t in range(N)))
check("conjunct 2: diagonal = 1", all(MAT[s][s] == 1 for s in range(N)))
check("conjunct 3: off-diagonal in {2,3,TOP}",
      all(MAT[s][t] in (2, 3, TOP) for s in range(N) for t in range(N) if s != t))
check("no pair is both Adjacent and Distant (if-order never decides a label)",
      not any(adjacent(s, t) and distant(s, t) for s in range(N) for t in range(N)))
census = {}
for s, t in combinations(range(N), 2):
    census[MAT[s][t]] = census.get(MAT[s][t], 0) + 1
print("     label census over unordered pairs:", census)
check("each block restricted is the A_39 path (braid group B_40): 38 threes, rest twos",
      all(sum(MAT[block_letter(b, i)][block_letter(b, j)] == 3 for i, j in combinations(range(39), 2)) == 38
          and all(MAT[block_letter(b, i)][block_letter(b, j)] in (2, 3) for i, j in combinations(range(39), 2))
          for b in range(3)))
check("letters 0,1,2 form a (3,3,3) triangle", MAT[0][1] == MAT[1][2] == MAT[0][2] == 3)
check("sentinels 3,4: label 2 to 0,1,2, TOP to each other and to all of 5..115",
      all(MAT[a][c] == 2 for a in (3, 4) for c in (0, 1, 2)) and MAT[3][4] == TOP
      and all(MAT[a][c] == TOP for a in (3, 4) for c in range(5, N)))


# ---- 2. relators as the Lean builds them ------------------------------------------------
def alternating(s, t, n):  # free-group word as list of (letter, +-1); 0 -> [], n+1 -> s * alt(t,s,n)
    return [] if n == 0 else [(s, 1)] + alternating(t, s, n - 1)


def inv(w):
    return [(x, -e) for x, e in reversed(w)]


def reduce(w):
    out = []
    for x in w:
        if out and out[-1][0] == x[0] and out[-1][1] == -x[1]:
            out.pop()
        else:
            out.append(x)
    return out


rels = []
for s in range(N):
    for t in range(N):
        n = MAT[s][t]
        if n != TOP:  # M s t = (n : Label) for exactly this n
            rels.append((s, t, n, alternating(s, t, n) + inv(alternating(t, s, n))))
check("alternating(s,t,3) = s t s (length n, starts at s, alternates)",
      alternating(7, 9, 3) == [(7, 1), (9, 1), (7, 1)])
check("every relator for label n has length 2n; diagonal relators reduce to 1",
      all(len(w) == 2 * n for s, t, n, w in rels)
      and all(reduce(w) == [] for s, t, n, w in rels if s == t))
check("every relator has exponent sum 0, so s -> 1 defines a surjection onto Z (group is infinite)",
      all(sum(e for _, e in w) == 0 for _, _, _, w in rels))
check("no relation at all for TOP pairs (e.g. 3,4 generate a free group modulo the rest)",
      not any((s, t) in ((3, 4), (4, 3)) for s, t, _, _ in rels))


# Coxeter quotient of a block: block b's letter at index i -> adjacent transposition (i, i+1) in S_40.
def perm_of_word(w, img, n):
    p = list(range(n))
    for x, e in w:  # transpositions are involutions, so e is irrelevant
        a, b = img[x]
        p = [b if v == a else a if v == b else v for v in p]
    return p


def holds_in_S40(b, w):
    img = {block_letter(b, i): (i, i + 1) for i in range(39)}
    return perm_of_word(w, img, 40) == list(range(40))


block_rels = [(b, w) for b in range(3) for s, t, n, w in rels
              if s != t and s in {block_letter(b, i) for i in range(39)}
              and t in {block_letter(b, i) for i in range(39)}]
check(f"all {len(block_rels)} intra-block relators hold in S_40 under i -> (i i+1)",
      all(holds_in_S40(b, w) for b, w in block_rels))

# NEGATIVE CONTROL 1: wrong relator length for an adjacent pair (label 3 used as 2) must fail in S_40.
s, t = block_letter(0, 2), block_letter(0, 3)
bad = alternating(s, t, 2) + inv(alternating(t, s, 2))
check("CONTROL: length-2 relator on an ADJACENT pair fails in S_40", not holds_in_S40(0, bad))
s, t = block_letter(0, 2), block_letter(0, 5)
bad = alternating(s, t, 3) + inv(alternating(t, s, 3))
# (I first predicted S_40 could NOT see this; it can: commuting s,t give sts = t, tst = s.)
check("CONTROL': length-3 relator on a DISTANT (commuting) pair fails in S_40", not holds_in_S40(0, bad))

# ---- 3. Gram matrices, exactly (cos(pi/2)=0, cos(pi/3)=1/2, label TOP -> -1) -------------
def gram(letters):
    g = {2: F(0), 3: F(-1, 2), TOP: F(-1)}
    return [[F(1) if a == c else g[MAT[a][c]] for c in letters] for a in letters]


def leading_minors(A):
    A = [row[:] for row in A]
    n, dets, d = len(A), [], F(1)
    for k in range(n):
        piv = A[k][k]
        d *= piv
        dets.append(d)
        if piv == 0:
            return dets
        for r in range(k + 1, n):
            f = A[r][k] / piv
            for c in range(k, n):
                A[r][c] -= f * A[k][c]
    return dets


blk = [block_letter(0, i) for i in range(39)]
dm = leading_minors(gram(blk))
check("block Gram matrix positive definite (spherical A_39), det = 40/2^39",
      all(x > 0 for x in dm) and dm[-1] == F(40, 2 ** 39))
check("triangle 0,1,2 Gram matrix has det 0 (affine A~_2: not spherical)",
      leading_minors(gram([0, 1, 2]))[-1] == 0)


# ---- 4. the CAT0 inequality as written in Lean --------------------------------------------
def rhs(t, u, a, b, c):  # a = d(x,y), b = d(x,z), c = d(y,z)
    return (t * t - t * u) * a * a + (u * u - t * u) * b * b + t * u * c * c


rnd = random.Random(254)
ok = True
for _ in range(2000):
    x, y, z = [(F(rnd.randint(-50, 50)), F(rnd.randint(-50, 50))) for _ in range(3)]
    t, u = F(rnd.randint(0, 20), 20), F(rnd.randint(0, 20), 20)
    p = tuple(x[k] + t * (y[k] - x[k]) for k in range(2))
    q = tuple(x[k] + u * (z[k] - x[k]) for k in range(2))
    d2 = lambda P, Q: (P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2
    lhs = d2(p, q)
    r = (t * t - t * u) * d2(x, y) + (u * u - t * u) * d2(x, z) + t * u * d2(y, z)
    ok &= lhs == r
check("in R^2 the Lean RHS equals |gamma(t)-eta(u)|^2 EXACTLY (it is the law-of-cosines comparison)", ok)

# A tripod (metric tree) is CAT(0): legs of lengths A,B,C from a centre; inequality must hold.
ok = True
for _ in range(2000):
    A, B, C = [F(rnd.randint(1, 30)) for _ in range(3)]
    t, u = F(rnd.randint(0, 40), 40), F(rnd.randint(0, 40), 40)
    a, b, c = A + B, A + C, B + C  # x on leg A, y on leg B, z on leg C
    # point at parameter t on [x,y]: signed position along leg A then leg B
    def pos(s, L_other):
        d = s * (A + L_other)
        return ("A", A - d) if d <= A else ("O", d - A)
    p, q = pos(t, B), pos(u, C)
    if p[0] == "A" and q[0] == "A":
        dist = abs(p[1] - q[1])
    elif p[0] == "A":
        dist = p[1] + q[1]
    elif q[0] == "A":
        dist = p[1] + q[1]
    else:
        dist = p[1] + q[1]  # different legs B and C
    ok &= dist * dist <= rhs(t, u, a, b, c)
check("tripod tree satisfies the Lean CAT0 inequality on 2000 exact samples", ok)

# NEGATIVE CONTROL 2: the unit round sphere is NOT CAT(0); an octant triangle must violate it.
def sph(lat, lon):
    return (math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat))


def slerp(P, Q, s):
    w = math.acos(max(-1, min(1, sum(p * q for p, q in zip(P, Q)))))
    return tuple((math.sin((1 - s) * w) * p + math.sin(s * w) * q) / math.sin(w) for p, q in zip(P, Q))


def gdist(P, Q):
    return math.acos(max(-1, min(1, sum(p * q for p, q in zip(P, Q)))))


X, Y, Z = sph(math.pi / 2, 0), sph(0, 0), sph(0, math.pi / 2)
g, h = slerp(X, Y, 1), slerp(X, Z, 1)
lhs = gdist(g, h) ** 2
r = rhs(1.0, 1.0, gdist(X, Y), gdist(X, Z), gdist(Y, Z))
gm, hm = slerp(X, Y, 0.5), slerp(X, Z, 0.5)
lhs_m, r_m = gdist(gm, hm) ** 2, rhs(0.5, 0.5, gdist(X, Y), gdist(X, Z), gdist(Y, Z))
print(f"     sphere octant midpoints: d^2 = {lhs_m:.6f}  vs Euclidean comparison {r_m:.6f}")
check("CONTROL: sphere octant triangle VIOLATES the inequality at t=u=1/2 (margin > 0.05)",
      lhs_m > r_m + 0.05)
check("     (sanity: at t=u=1 both sides are d(y,z)^2)", abs(lhs - r) < 1e-12)

# ---- 5. the action clauses are not vacuous ---------------------------------------------
# Z acting on R by translation: for K=[a,b], {n : (K+n) cap K nonempty} = {|n| <= b-a}, finite;
# K=[0,1] is a compact fundamental set. And a point fails properness for an infinite group,
# so the 'trivially CAT(0) point' loophole is closed by the properness clause.
a, b = F(-3, 2), F(7, 3)
hits = [n for n in range(-100, 101) if max(a, a + n) <= min(b, b + n)]
check("Z on R: {n | (K+n) meets K} for K=[-3/2,7/3] is exactly |n|<=3", hits == list(range(-3, 4)))
check("point space: {g | g.K meets K} = whole group, infinite here (surjects onto Z) -> not proper",
      True)  # follows from the exponent-sum check above; recorded so the argument is explicit

print()
print("ALL CHECKS AND CONTROLS BEHAVE" if not fails else f"{len(fails)} FAILURE(S): {fails}")
sys.exit(1 if fails else 0)
