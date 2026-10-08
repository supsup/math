#!/usr/bin/env python3
"""Independent exact-arithmetic checks for OAI.GrahamSpherical.full_main.

Stdlib only (fractions.Fraction); sympy is not installed. Run: python3 -I replicate.py
Every positive check has a negative control that must FAIL; the script exits 1 if any
positive check fails or any control unexpectedly passes.
"""
from fractions import Fraction as Fr
from itertools import combinations, product
import math
import random
import sys

FAIL = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    if not ok:
        FAIL.append(name)


def control(name, failed_as_expected, detail=""):
    print(("CONTROL-OK " if failed_as_expected else "CONTROL-BROKEN ") + name
          + (f"  [{detail}]" if detail else ""))
    if not failed_as_expected:
        FAIL.append("control " + name)


# ---------------------------------------------------------------- 1. the parameter
# Lean: parameter = sum_{m>=0} 1/10^((m+1)!) = sum_{k>=1} 10^(-k!)  (Liouville's constant
# without Mathlib's extra k=0 term; Lean proves parameter = liouvilleNumber 10 - 1/10).
def partial(K):
    return sum(Fr(1, 10 ** math.factorial(k)) for k in range(1, K + 1))


t3 = partial(3)                      # 0.1 + 0.01 + 10^-6
tail_bound = Fr(2, 10 ** 24)         # sum_{k>=4} 10^-k! < 2 * 10^-24
check("parameter partial sum t_3 = 0.110001", t3 == Fr(110001, 10 ** 6))
check("11/100 < t < 12/100 (t in (t_3, t_3 + 2e-24))",
      Fr(11, 100) < t3 and t3 + tail_bound < Fr(12, 100))
print("     t = 0.110001000000000000000001000... (1s at decimal places k! = 1,2,6,24,120,...)")
# Note: Lean's tsum would be 0 if the series were not summable; parameter_bounds rules that out.

# ---------------------------------------------------------------- 2. the twelve points
SQUARE = [(1, 0), (-1, 0), (0, 1), (0, -1)]   # squareCoordinate 0,1,2,3


def uv(t):
    return (1 - t * t) / (1 + t * t), (2 * t) / (1 + t * t)


def coordinates(t, a, q):
    """Lean `coordinates (a, q)`: a=0 rotate by +theta, a=1 by -theta, a=2 identity."""
    u, v = uv(t)
    x, y = SQUARE[q]
    if a == 0:
        return (u * x - v * y, v * x + u * y)
    if a == 1:
        return (u * x + v * y, -v * x + u * y)
    return (Fr(x), Fr(y))


LABELS = [(a, q) for a in range(3) for q in range(4)]
WEIGHT = {lab: (-2 if lab[0] == 2 else 1) for lab in LABELS}

# exact rational stand-ins for t (u, v are rational in t, so every circle fact is exact)
for tt in [t3, Fr(1, 10), Fr(11, 100), Fr(3, 25)]:
    pts = [coordinates(tt, a, q) for (a, q) in LABELS]
    check(f"t={tt}: 12 distinct points", len(set(pts)) == 12)
    check(f"t={tt}: all x^2+y^2 = 1 exactly", all(x * x + y * y == 1 for x, y in pts))


def concyclic_det(p1, p2, p3, p4):
    rows = [[x * x + y * y, x, y, Fr(1)] for (x, y) in (p1, p2, p3, p4)]
    def det(m):
        if len(m) == 1:
            return m[0][0]
        return sum((-1) ** j * m[0][j] * det([r[:j] + r[j + 1:] for r in m[1:]])
                   for j in range(len(m)))
    return det(rows)


pts = [coordinates(t3, a, q) for (a, q) in LABELS]
dets = [concyclic_det(*s) for s in combinations(pts, 4)]
check("all 495 four-point concyclicity determinants vanish (one common circle)",
      all(d == 0 for d in dets), f"{len(dets)} subsets")
bad = list(pts)
bad[0] = (Fr(11, 10) * bad[0][0], Fr(11, 10) * bad[0][1])   # push one point off the circle
bdets = [concyclic_det(*s) for s in combinations(bad, 4)]
control("perturbed set (one point scaled by 11/10) is not concyclic",
        any(d != 0 for d in bdets),
        f"{sum(d != 0 for d in bdets)} nonzero of {len(bdets)}")

d2 = sorted({(p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for p, q in combinations(pts, 2)})
print(f"     t=t_3: {len(d2)} distinct squared distances among the 66 pairs; "
      f"min ~ {float(d2[0]):.6f}, max = {d2[-1]}")
check("min pairwise distance is positive", d2[0] > 0)

# ---------------------------------------------------------------- 3. dual numbers = a derivation
class Dual:
    """a + b*eps with eps^2 = 0. Evaluating a rational function on Duals computes its value and
    its image under any derivation D, given D of the inputs: exactly the Leibniz/quotient rules the
    Lean proof uses on a Derivation Z R R (no continuity needed)."""
    __slots__ = ("a", "b")

    def __init__(self, a, b=Fr(0)):
        self.a, self.b = Fr(a), Fr(b)

    @staticmethod
    def lift(x):
        return x if isinstance(x, Dual) else Dual(x)

    def __add__(s, o): o = Dual.lift(o); return Dual(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __neg__(s): return Dual(-s.a, -s.b)
    def __sub__(s, o): return s + (-Dual.lift(o))
    def __rsub__(s, o): return Dual.lift(o) - s
    def __mul__(s, o): o = Dual.lift(o); return Dual(s.a * o.a, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def __truediv__(s, o):
        o = Dual.lift(o)
        return Dual(s.a / o.a, (s.b * o.a - s.a * o.b) / (o.a * o.a))
    def __rtruediv__(s, o): return Dual.lift(o) / s
    def __eq__(s, o): o = Dual.lift(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))


rng = random.Random(20261008)
def rq(lo=-5, hi=5, den=7):
    return Fr(rng.randint(lo * den, hi * den), rng.randint(1, den))

ok = True
for _ in range(50):
    tv = rq()
    T = Dual(tv, (1 + tv * tv) / 2)          # D t = (1 + t^2)/2
    U, V = uv(T)
    ok &= (U.b == -V.a) and (V.b == U.a)
check("D t = (1+t^2)/2 gives D u = -v and D v = u (50 rational t)", ok)
T = Dual(t3, 1)                               # control: plain d/dt
U, V = uv(T)
control("with D t = 1 instead, D u != -v", U.b != -V.a, f"D u = {float(U.b):.4f}, -v = {float(-V.a):.4f}")

# ---------------------------------------------------------------- 4. the moment identity as a polynomial identity
# Lean `weighted_coordinate_square`, first calc step: with Du=-v, Dv=u (and D of +-1, 0 being 0),
#   sum_i w_i (p + a x_i + b y_i + c Dx_i + d Dy_i)^2
#     = 4(u^2+v^2)(c^2+d^2) + 4(u^2+v^2-1)(a^2+b^2)       as polynomials in u,v,p,a,b,c,d.
VARS = ["u", "v", "p", "a", "b", "c", "d"]
def mono(**e): return tuple(e.get(k, 0) for k in VARS)
def P(d): return {k: Fr(c) for k, c in d.items() if c != 0}
def padd(x, y):
    r = dict(x)
    for k, c in y.items():
        r[k] = r.get(k, 0) + c
    return {k: c for k, c in r.items() if c != 0}
def pmul(x, y):
    r = {}
    for k1, c1 in x.items():
        for k2, c2 in y.items():
            k = tuple(i + j for i, j in zip(k1, k2))
            r[k] = r.get(k, 0) + c1 * c2
    return {k: c for k, c in r.items() if c != 0}
def pscale(x, s): return {k: c * s for k, c in x.items() if c * s != 0}
def var(n): return P({mono(**{n: 1}): 1})
def const(c): return P({mono(): c})
u_, v_, p_, a_, b_, c_, d_ = (var(n) for n in VARS)
ZERO = {}


def sym_point(a, q, signs=(1, -1)):
    """Symbolic (x, y, Dx, Dy) of label (a, q). signs = rotation sense of squares 0 and 1."""
    x, y = SQUARE[q]
    X, Y = const(x), const(y)
    if a == 2:
        return X, Y, ZERO, ZERO
    s = signs[a]
    # R(s*theta) q = (u x - s v y, s v x + u y); D of it with Du=-v, Dv=u
    px = padd(pmul(u_, X), pscale(pmul(v_, Y), -s))
    py = padd(pscale(pmul(v_, X), s), pmul(u_, Y))
    dpx = padd(pscale(pmul(v_, X), -1), pscale(pmul(u_, Y), -s))
    dpy = padd(pscale(pmul(u_, X), s), pscale(pmul(v_, Y), -1))
    return px, py, dpx, dpy


def weighted_sum(signs=(1, -1), weights=WEIGHT):
    tot = {}
    for lab in LABELS:
        px, py, dpx, dpy = sym_point(*lab, signs=signs)
        lin = padd(padd(padd(padd(p_, pmul(a_, px)), pmul(b_, py)), pmul(c_, dpx)), pmul(d_, dpy))
        tot = padd(tot, pscale(pmul(lin, lin), weights[lab]))
    return tot


n2 = padd(pmul(u_, u_), pmul(v_, v_))
rhs = padd(pscale(pmul(n2, padd(pmul(c_, c_), pmul(d_, d_))), 4),
           pscale(pmul(padd(n2, const(-1)), padd(pmul(a_, a_), pmul(b_, b_))), 4))
lhs = weighted_sum()
check("weighted moment identity holds as an exact polynomial identity", lhs == rhs,
      f"{len(lhs)} monomials")
diff1 = padd(weighted_sum(signs=(1, 1)), pscale(rhs, -1))
control("both rotated squares turned the SAME way (+theta,+theta): identity fails",
        diff1 != {}, f"residual has {len(diff1)} monomials (the mixed a*d, b*c terms)")
diff2 = padd(weighted_sum(weights={lab: 1 for lab in LABELS}), pscale(rhs, -1))
control("all weights 1 (no -2 on the fixed square): identity fails", diff2 != {},
        f"residual has {len(diff2)} monomials")

# ---------------------------------------------------------------- 5. the copy invariant in R^n
# For an isometric copy y_i = z + x_i A + y_i B (A, B orthonormal), energy E(y) = sum_j D(y_j)^2.
# Lean `weighted_copy_derivation_energy`: sum_i w_i E(y_i) = 8 for every copy, in every n.
def energy(Y):
    return sum(c.b * c.b for c in Y)


def cayley_orthonormal_pair(n):
    """Exact rational orthonormal A, B in Q^n: first two columns of the Cayley transform
    (I - S)^{-1}(I + S) of a random rational skew matrix S."""
    S = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            S[i][j] = rq(-2, 2, 3); S[j][i] = -S[i][j]
    M = [[(Fr(1) if i == j else Fr(0)) - S[i][j] for j in range(n)] for i in range(n)]
    N = [[(Fr(1) if i == j else Fr(0)) + S[i][j] for j in range(n)] for i in range(n)]
    # solve M X = N by Gauss-Jordan
    aug = [M[i] + N[i] for i in range(n)]
    for col in range(n):
        piv = next(r for r in range(col, n) if aug[r][col] != 0)
        aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        aug[col] = [x / pv for x in aug[col]]
        for r in range(n):
            if r != col and aug[r][col] != 0:
                f = aug[r][col]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[col])]
    Q = [row[n:] for row in aug]
    return [Q[i][0] for i in range(n)], [Q[i][1] for i in range(n)]


def copy_energy(n, Dt_rule=lambda t: (1 + t * t) / 2, scaleA=Fr(1), signs=(1, -1)):
    T = Dual(t3, Dt_rule(t3))
    A, B = cayley_orthonormal_pair(n)
    A = [Dual(scaleA * x, rq()) for x in A]       # arbitrary D(A_j): mixed orthogonality NOT used
    B = [Dual(x, rq()) for x in B]
    z = [Dual(rq(), rq()) for _ in range(n)]
    U, V = uv(T)
    def coord(a, q):
        x, y = SQUARE[q]
        if a == 2:
            return Dual(x), Dual(y)
        s = signs[a]
        return U * x - s * V * y, s * V * x + U * y
    total, ys = Fr(0), {}
    for lab in LABELS:
        cx, cy = coord(*lab)
        Y = [z[j] + cx * A[j] + cy * B[j] for j in range(n)]
        ys[lab] = Y
        total += WEIGHT[lab] * energy(Y)
    return total, ys


ok, iso = True, True
for n in [2, 3, 5, 8]:
    for _ in range(5):
        tot, ys = copy_energy(n)
        ok &= tot == 8
        for l1, l2 in combinations(LABELS, 2):
            dy = sum((p.a - q.a) ** 2 for p, q in zip(ys[l1], ys[l2]))
            p1, p2 = coordinates(t3, *l1), coordinates(t3, *l2)
            iso &= dy == (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
check("weighted energy of 20 random isometric copies (n = 2,3,5,8) is exactly 8", ok)
check("those copies are exact isometric images (all 66 squared distances preserved)", iso)
tot, _ = copy_energy(4, Dt_rule=lambda t: Fr(1))
control("D t = 1 (wrong derivation value): weighted energy != 8", tot != 8, f"{float(tot):.4f}")
tot, _ = copy_energy(4, scaleA=Fr(2))
control("non-isometric copy (A scaled by 2): weighted energy != 8", tot != 8, f"{float(tot):.4f}")
tot, _ = copy_energy(4, signs=(1, 1))
control("set with both squares rotated +theta: energy not invariant", tot != 8, f"{float(tot):.4f}")

# ---------------------------------------------------------------- 6. the fifty-colour rounding step
# colour(y) = floor(3 E(y)) mod 50. If 12 energies e_i with sum w_i e_i = 8 all get one colour,
# S = sum w_i floor(3 e_i) is = 0 mod 50 (weights sum to 0) yet 16 < S < 32.
check("weights sum to 0", sum(WEIGHT.values()) == 0)


def m_works(m):
    """The rounding argument rules out monochromatic copies iff no multiple of m lies in (16, 32)."""
    return not any(S % m == 0 for S in range(17, 32))


good = [m for m in range(1, 61) if m_works(m)]
check("m = 50 colours: no multiple of 50 in (16, 32)", m_works(50))
print(f"     moduli m <= 60 for which this floor(3E) mod m argument works: {good}")


def realize(m):
    """For a modulus that fails, build exact energies with sum w_i e_i = 8 and one colour."""
    S = next(S for S in range(17, 32) if S % m == 0)
    k = S // m
    f = {lab: 0 for lab in LABELS}
    f[(0, 0)] = k * m                  # one +1-weight floor raised by k*m; S = k*m
    # choose 3e_i in [f_i, f_i+1) hitting sum w_i 3e_i = 24 exactly
    e = {lab: Fr(f[lab]) for lab in LABELS}
    need = Fr(24 - S)                  # in (-8, 8)
    pos = [lab for lab in LABELS if WEIGHT[lab] == 1]
    neg = [lab for lab in LABELS if WEIGHT[lab] == -2]
    if need > 0:
        for lab in pos:
            step = min(need, Fr(99, 100)); e[lab] += step; need -= step
    else:
        for lab in neg:
            step = min(-need / 2, Fr(99, 100)); e[lab] += step; need += 2 * step
    assert need == 0
    e = {lab: x / 3 for lab, x in e.items()}
    s = sum(WEIGHT[lab] * e[lab] for lab in LABELS)
    cols = {math.floor(3 * e[lab]) % m for lab in LABELS}
    return s, cols


for m in [15, 17, 31]:
    s, cols = realize(m)
    control(f"m = {m}: the rounding argument does NOT exclude a monochromatic copy",
            s == 8 and len(cols) == 1, f"sum w e = {s}, colours used = {cols}")

print()
if FAIL:
    print("FAILURES:", FAIL)
    sys.exit(1)
print("all checks passed, all controls failed as required")
