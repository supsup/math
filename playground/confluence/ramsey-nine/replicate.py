#!/usr/bin/env python3
"""Independent exact replication of the computable parts of
OAI.EuclideanRamsey.NineStatement.nine_circle_configuration.

Exact arithmetic only (fractions.Fraction). No sympy (not installed on this host).
Run: python3 -I replicate.py   (exit 0 = all positive checks pass AND all controls fail as expected)
"""
from fractions import Fraction as F
import random
import sys

FAIL = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))
    if not ok:
        FAIL.append(name)


# ---- the configuration, exactly as literalCircleConfig -------------------------------------
def point(t):
    t = F(t)
    return ((1 - t * t) / (1 + t * t), (2 * t) / (1 + t * t))


# ---- polynomial helpers (coefficient lists, index = power of t) -----------------------------
def pmul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def padd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def det(M):
    """Exact determinant by fraction Gaussian elimination."""
    M = [[F(x) for x in row] for row in M]
    n = len(M)
    d = F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return F(0)
        if p != c:
            M[c], M[p] = M[p], M[c]
            d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f:
                M[r] = [M[r][k] - f * M[c][k] for k in range(n)]
    return d


def rank(M):
    M = [[F(x) for x in row] for row in M]
    rows, cols = len(M), len(M[0])
    rk = 0
    for c in range(cols):
        p = next((r for r in range(rk, rows) if M[r][c] != 0), None)
        if p is None:
            continue
        M[rk], M[p] = M[p], M[rk]
        for r in range(rows):
            if r != rk and M[r][c] != 0:
                f = M[r][c] / M[rk][c]
                M[r] = [M[r][k] - f * M[rk][k] for k in range(cols)]
        rk += 1
    return rk


# Columns: Option(Fin 2) x Option(Fin 2), encoded by finSuccEquiv as (a, b) in Fin 3 x Fin 3,
# 0 = none (constant 1), 1 = x-coordinate, 2 = y-coordinate. Order (a,b) -> 3a+b.
COLS = [(a, b) for a in range(3) for b in range(3)]


def r(z):            # NineRational.r : the augmented coordinate vector [1, x, y]
    x, y = point(z)
    return (F(1), x, y)


def q(z):            # NineGrid.q : denominator-cleared [1+z^2, 1-z^2, 2z]
    z = F(z)
    return (1 + z * z, 1 - z * z, 2 * z)


def generic_matrix(T, U):
    """Row i: r(T_i)[a] * r(U_i)[b]. T = left tensor copy, U = right tensor copy."""
    return [[r(T[i])[a] * r(U[i])[b] for (a, b) in COLS] for i in range(len(T))]


def E_matrix(T, U):
    return [[q(T[i])[a] * q(U[i])[b] for (a, b) in COLS] for i in range(len(T))]


def main():
    rng = random.Random(20261008)
    rnd = lambda: F(rng.randint(-50, 50), rng.randint(1, 50))

    print("== 1. the points lie on the unit circle ==")
    # polynomial identity (1-t^2)^2 + (2t)^2 == (1+t^2)^2
    lhs = padd(pmul([1, 0, -1], [1, 0, -1]), pmul([0, 2], [0, 2]))
    rhs = pmul([1, 0, 1], [1, 0, 1])
    check("identity (1-t^2)^2+(2t)^2 = (1+t^2)^2 as polynomials", lhs == rhs, f"{lhs} vs {rhs}")
    ts = [rnd() for _ in range(200)]
    check("x^2+y^2 = 1 exactly at 200 random rationals",
          all(sum(c * c for c in point(t)) == 1 for t in ts))
    # note 1+t^2 > 0 for real t, so the parametrization is total on R (Lean's x/0 = 0 never bites)
    check("denominator 1+t^2 never 0 on R (min 1 at t=0)", True, "1+t^2 >= 1")

    print("== 2. injectivity: t is recovered as y/(1+x) ==")
    check("y/(1+x) == t exactly at 200 random rationals",
          all((lambda p: p[1] / (1 + p[0]))(point(t)) == F(t) for t in ts))
    # 1+x = 2/(1+t^2) > 0, so the recovery denominator is never 0; point(t) never hits (-1,0)
    check("1+x = 2/(1+t^2) at 200 random rationals",
          all(1 + point(t)[0] == F(2) / (1 + F(t) ** 2) for t in ts))

    print("== 3. affine span is the whole plane (needed by not_ramsey_of_det_ne_zero) ==")
    a, b, c = point(0), point(1), point(-1)
    area = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    check("3 distinct circle points are not collinear (t=0,1,-1)", area != 0, f"2*area = {area}")

    print("== 4. NineGrid: E at T_(a,b)=g[a], U_(a,b)=g[b], g=(0,1,-1) ==")
    g = [F(0), F(1), F(-1)]
    idx = [(a, b) for a in range(3) for b in range(3)]   # finProdFinEquiv row order
    Tg = [g[a] for (a, b) in idx]
    Ug = [g[b] for (a, b) in idx]
    C = [list(q(z)) for z in g]
    check("C = [[1,1,0],[2,0,2],[2,0,-2]]", C == [[1, 1, 0], [2, 0, 2], [2, 0, -2]], str(C))
    check("det C = 8", det(C) == 8, str(det(C)))
    Eg = E_matrix(Tg, Ug)
    kron = [[C[i // 3][j // 3] * C[i % 3][j % 3] for j in range(9)] for i in range(9)]
    check("E(grid) equals the Kronecker square C (x) C entrywise", Eg == kron)
    dE = det(Eg)
    check("det E(grid) = 8^6 = 262144 (built from the definition, not the Kronecker rule)",
          dE == 8 ** 6, str(dE))
    # The paper (sections/07-consequences.tex) uses the UNcleared matrix: C' = rows p(0),p(1),p(-1),
    # det C' = 2, det = 2^6 = 64. Cross-check: 64 * prod of denominators (4^6) = 8^6.
    Cp = [list(r(z)) for z in g]
    dMg = det(generic_matrix(Tg, Ug))
    check("paper's uncleared form: det C' = 2 and det M(grid) = 2^6 = 64",
          det(Cp) == 2 and dMg == 64, f"det C' = {det(Cp)}, det M(grid) = {dMg}")
    check("64 * 4^6 == 8^6 (paper's 64 and Lean's 8^6 agree via the row denominators)",
          dMg * 4 ** 6 == dE)

    print("== 5. the rational matrix at independent random T, U (18 rationals) ==")
    nz = 0
    for trial in range(20):
        T = [rnd() for _ in range(9)]
        U = [rnd() for _ in range(9)]
        dG = det(generic_matrix(T, U))
        dEe = det(E_matrix(T, U))
        den = F(1)
        for i in range(9):
            den *= (1 + T[i] ** 2) * (1 + U[i] ** 2)
        assert dEe == den * dG, "cleared_matrix relation det E = prod(denominators) * det M failed"
        nz += dG != 0
    check("det genericMatrix != 0 at 20/20 random independent rational points", nz == 20, f"{nz}/20")
    check("det E = prod_i (1+T_i^2)(1+U_i^2) * det M at all 20 points (cleared_matrix)", True)

    print("== CONTROLS (each MUST come out singular / failing) ==")
    # C1. No tensor independence: U = T (this is what the multiply map sees, i.e. a configuration
    # whose two tensor factors collapse, as for rational parameters where Q (x) Q = Q).
    T = [rnd() for _ in range(9)]
    M1 = generic_matrix(T, T)
    d1 = det(M1)
    check("CONTROL C1: U = T gives det = 0", d1 == 0, f"det = {d1}, rank = {rank(M1)}")
    # explicit kernel vector = the circle equation x*x + y*y - 1*1: P(none,none) = -1,
    # P(x,x) = P(y,y) = 1, others 0; spatial condition P(some a, some b) = [a = b] holds.
    P = {(0, 0): F(-1), (1, 1): F(1), (2, 2): F(1)}
    v = [P.get(cb, F(0)) for cb in COLS]
    resid = [sum(row[k] * v[k] for k in range(9)) for row in M1]
    check("CONTROL C1: circle equation is a nonzero kernel vector meeting the spatial condition",
          all(x == 0 for x in resid), "so FieldCriterion's witness exists when the factors collapse")
    resid_ind = [sum(row[k] * v[k] for k in range(9))
                 for row in generic_matrix([rnd() for _ in range(9)], [rnd() for _ in range(9)])]
    check("CONTROL C1b: same vector is NOT a kernel vector once T, U independent",
          any(x != 0 for x in resid_ind), f"first residual = {resid_ind[0]}")
    # C2. Not injective (t_0 = t_1): duplicate row -> det 0.
    T = [rnd() for _ in range(9)]
    U = [rnd() for _ in range(9)]
    T[1], U[1] = T[0], U[0]
    d2 = det(generic_matrix(T, U))
    check("CONTROL C2: repeated parameter (t1 = t0) gives det = 0", d2 == 0, f"det = {d2}")
    # C3. Perturbed grid (0,1,1): det C = 0 so the evaluation certificate dies.
    g3 = [F(0), F(1), F(1)]
    C3 = [list(q(z)) for z in g3]
    E3 = E_matrix([g3[a] for (a, b) in idx], [g3[b] for (a, b) in idx])
    check("CONTROL C3: grid (0,1,1) gives det C = 0 and det E = 0",
          det(C3) == 0 and det(E3) == 0, f"det C = {det(C3)}, det E = {det(E3)}")
    # C4. Drop a point: 8 rows, 9 columns -> rank 8 < 9, a kernel always exists; the
    # determinant argument has nothing to say about 8 points.
    T = [rnd() for _ in range(8)]
    U = [rnd() for _ in range(8)]
    rk = rank(generic_matrix(T, U))
    check("CONTROL C4: 8 points give an 8x9 system of rank 8 (nonzero kernel)", rk == 8, f"rank = {rk}")

    print()
    if FAIL:
        print("FAILED:", FAIL)
        sys.exit(1)
    print("ALL CHECKS PASS (positive checks hold, every control came out singular as required)")


if __name__ == "__main__":
    main()
