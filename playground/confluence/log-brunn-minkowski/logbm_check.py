"""Independent numeric checks of the log-Brunn-Minkowski inequality as stated in
lean/ComparatorChallenges/LogBrunnMinkowski.lean:

    vol(K)^(1-t) * vol(L)^t <= vol( W[h_K^(1-t) h_L^t] ),
    W[f] = { x : <x,u> <= f(u) for all unit u },  h_K(u) = sup_{x in K} <x,u>.

Part A (plane, bounded): W is approximated from OUTSIDE by N sampled half-planes
(A_N = polar of conv{u_j / f(u_j)}, computed exactly as a polygon), then shrunk by a
proven factor to give a LOWER bound on vol W:
    x in A_N, |u - u_j| <= d  =>  <x,u> <= f(u) + (Lip_f + R_A) d  =: f(u) + eps
    so A_N is inside W[f + eps], inside (1 + eps/m_f) W[f],
    vol W >= vol A_N / (1 + eps/m_f)^2.
Lip_f <= M_f ((1-t) R_K/m_K + t R_L/m_L) (h_K is R_K-Lipschitz, h_K >= m_K = inradius).
Floating point is NOT controlled (doubles, margins reported); bounds are "rigorous modulo
rounding".

Part B (R^3, numeric only): radial-function quadrature on a Fibonacci sphere. Not a bound.

Controls: (1) a NON-symmetric pair (origin in the interior, so every power is defined)
where the inequality must FAIL; (2) a deliberately wrong combination, W[min(h_K, h_L)] =
K cap L, that must fail; (3) equality cases (t=0, t=1, dilates) must come out ~equal.
Pure python + numpy. Run: python3 logbm_check.py
"""
import math
import numpy as np

# numpy 2.0 + macOS Accelerate raises spurious FP flags in matmul (checked against an explicit
# elementwise sum: max diff 4e-16, all finite); real inf/nan in the results are asserted below.
np.seterr(all="ignore")

# ---------------------------------------------------------------- polygons in the plane

def hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def area(poly):
    s = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % len(poly)]
        s += x1*y2 - x2*y1
    return abs(s) / 2


def support(verts, u):
    return max(v[0]*u[0] + v[1]*u[1] for v in verts)


def inradius(verts):
    """distance from the origin to the nearest edge line of conv(verts) (origin inside)."""
    P = hull(verts)
    best = math.inf
    for i in range(len(P)):
        (x1, y1), (x2, y2) = P[i], P[(i+1) % len(P)]
        nx, ny = y2-y1, x1-x2
        nn = math.hypot(nx, ny)
        best = min(best, abs(nx*x1 + ny*y1) / nn)
    return best


def circumradius(verts):
    return max(math.hypot(*v) for v in verts)


def wulff_outer(f, N):
    """A_N = {x : <x,u_j> <= f(u_j), j<N} as a polygon, via polarity."""
    dual = []
    for j in range(N):
        a = 2*math.pi*j/N
        u = (math.cos(a), math.sin(a))
        fu = f(u)
        dual.append((u[0]/fu, u[1]/fu))
    P = hull(dual)
    out = []
    for i in range(len(P)):
        (a1, b1), (a2, b2) = P[i], P[(i+1) % len(P)]
        det = a1*b2 - a2*b1
        out.append(((b2 - b1)/det, (a1 - a2)/det))  # solves v.p=1, v.q=1
    return out


def wulff_lower_bound(Kv, Lv, t, N=20000, comb=None):
    hK = lambda u: support(Kv, u)
    hL = lambda u: support(Lv, u)
    if comb is None:
        f = lambda u: hK(u)**(1-t) * hL(u)**t
        mK, mL, RK, RL = inradius(Kv), inradius(Lv), circumradius(Kv), circumradius(Lv)
        m_f = mK**(1-t) * mL**t
        M_f = RK**(1-t) * RL**t
        lip = M_f * ((1-t)*RK/mK + t*RL/mL)
    else:
        f = comb
        m_f = min(inradius(Kv), inradius(Lv))
        lip = max(circumradius(Kv), circumradius(Lv))
    A = wulff_outer(f, N)
    RA = circumradius(A)
    d = 2*math.sin(math.pi/(2*N))      # chord to the nearest sample
    eps = (lip + RA) * d
    return area(A) / (1 + eps/m_f)**2, area(A)


def poly_area(verts):
    return area(hull(verts))


def rect(a, b, c=(0.0, 0.0)):
    return [(c[0]+sx*a, c[1]+sy*b) for sx in (-1, 1) for sy in (-1, 1)]


def rot(verts, th):
    c, s = math.cos(th), math.sin(th)
    return [(c*x - s*y, s*x + c*y) for x, y in verts]


def regular(k, r=1.0, phase=0.0):
    return [(r*math.cos(phase + 2*math.pi*i/k), r*math.sin(phase + 2*math.pi*i/k)) for i in range(k)]


def random_symmetric(rng, k):
    pts = []
    for _ in range(k):
        a = rng.uniform(0, math.pi)
        r = rng.uniform(0.3, 2.0)
        pts.append((r*math.cos(a), r*math.sin(a)))
    pts += [(-x, -y) for x, y in pts]
    return pts


def check2d(name, Kv, Lv, t, expect="holds", **kw):
    lhs = poly_area(Kv)**(1-t) * poly_area(Lv)**t
    lb, outer = wulff_lower_bound(Kv, Lv, t, **kw)
    if expect == "holds":
        ok = lb >= lhs
        verdict = "PASS (proved lower bound >= LHS)" if ok else (
            "NEAR-EQUALITY (outer >= LHS, bound too loose)" if outer >= lhs*(1-1e-12) else "FAIL")
    else:  # control: must fail, i.e. even the OUTER approximation (>= true W) is below LHS
        ok = outer < lhs
        verdict = "CONTROL FAILS AS REQUIRED" if ok else "CONTROL DID NOT FAIL (instrument suspect)"
    print(f"{name:44s} t={t:.2f} LHS={lhs:.6f} volW in [{lb:.6f}, {outer:.6f}]  "
          f"ratio_lb={lb/lhs:.6f}  {verdict}")
    return verdict


# ---------------------------------------------------------------- R^3 numeric (not a bound)

def fib_sphere(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2*i/n)
    th = math.pi * (1 + 5**0.5) * i
    return np.stack([np.cos(th)*np.sin(phi), np.sin(th)*np.sin(phi), np.cos(phi)], axis=1)


def wulff_volume3(f_vals, U, Theta, chunk=2000):
    """vol of {x : <x,u_j> <= f_j}  ~  (1/3) * mean(rho^3) * 4pi."""
    rho = []
    for s in range(0, len(Theta), chunk):
        c = Theta[s:s+chunk] @ U.T              # (chunk, N)
        with np.errstate(divide="ignore"):
            r = np.where(c > 1e-12, f_vals[None, :] / np.where(c > 1e-12, c, 1), np.inf)
        rho.append(r.min(axis=1))
    rho = np.concatenate(rho)
    return 4*math.pi/3 * np.mean(rho**3)


def h3(V, U):
    return (U @ V.T).max(axis=1)


def check3d(name, KV, LV, t, volK, volL, normals, comb=None, expect="holds", N=6000, M=40000):
    # constraint directions = Fibonacci grid PLUS the facet normals of K and L (without them the
    # outer approximation of a cube is ~4% too big, measured); evaluation grid rotated off it.
    U = np.vstack([fib_sphere(N), normals])
    Th = fib_sphere(M) @ np.array([[1, 0, 0], [0, .8, .6], [0, -.6, .8]])
    hK, hL = h3(KV, U), h3(LV, U)
    f = hK**(1-t) * hL**t if comb is None else comb(hK, hL)
    vw = wulff_volume3(f, U, Th)
    lhs = volK**(1-t) * volL**t
    # quadrature sanity: the same routine on f = h_K should give vol K
    vK = wulff_volume3(hK, U, Th)
    assert np.isfinite(vw) and np.isfinite(vK)
    tag = ("PASS (numeric)" if vw >= lhs*(1-2e-3) else "FAIL") if expect == "holds" else (
        "CONTROL FAILS AS REQUIRED" if vw < lhs*0.98 else "CONTROL DID NOT FAIL")
    print(f"{name:44s} t={t:.2f} LHS={lhs:.5f} volW~{vw:.5f} ratio={vw/lhs:.5f} "
          f"[quadrature on K: {vK:.5f} vs exact {volK:.5f}]  {tag}")
    return tag


def box3(a):
    return np.array([[sx*a[0], sy*a[1], sz*a[2]] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)])


def octa(r):
    I = np.eye(3)*r
    return np.vstack([I, -I])


def rot3(V, ax, th):
    c, s = math.cos(th), math.sin(th)
    if ax == 2:
        R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    else:
        R = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    return V @ R.T


if __name__ == "__main__":
    import random
    rng = random.Random(20261008)
    res = []
    print("== Part A: plane, proved lower bound on vol W (modulo float rounding)")
    sq = rect(1, 1)
    res.append(check2d("square vs rectangle 4x0.25 (common axes)", sq, rect(2, 0.125), 0.5))
    res.append(check2d("rect 2x0.5 vs rect 0.5x2", rect(1, .25), rect(.25, 1), 0.5))
    res.append(check2d("square vs 45deg-rotated square", sq, rot(sq, math.pi/4), 0.5))
    res.append(check2d("rect 3x1 vs rotated 30deg", rect(1.5, .5), rot(rect(1.5, .5), math.pi/6), 0.3))
    res.append(check2d("square vs regular hexagon", sq, regular(6), 0.5))
    res.append(check2d("thin rect vs rotated thin rect (60deg)", rect(2, .1), rot(rect(2, .1), math.pi/3), 0.5,
                       N=400000))
    for i in range(6):
        K, L = random_symmetric(rng, rng.randint(2, 6)), random_symmetric(rng, rng.randint(2, 6))
        res.append(check2d(f"random symmetric polygons #{i}", K, L, rng.uniform(0.05, 0.95)))
    print("-- equality cases (must be ~ratio 1; lower bound may land just under)")
    check2d("t=0 (W[h_K] = K)", sq, rot(sq, .4), 0.0)
    check2d("dilates K, 3K (W = 3^t K)", regular(6), regular(6, 3.0), 0.5)
    print("-- note: boxes with COMMON axes are an equality case: Hoelder gives box(a^(1-t)b^t) inside W and")
    print("   the axis constraints give W inside that box, so W = box(a^(1-t) b^t) exactly (ratio 1).")
    print("-- CONTROLS (must FAIL)")
    # non-symmetric: square vs translated square with origin just inside the edge
    ctrl1 = check2d("NONSYM: square vs square shifted (0.95,0.95)", sq, rect(1, 1, (0.95, 0.95)), 0.5,
                    expect="fails")
    ctrl2 = check2d("WRONG COMB: W[min(h_K,h_L)] = K cap L", rect(1, .25), rect(.25, 1), 0.5,
                    expect="fails",
                    comb=lambda u: min(support(rect(1, .25), u), support(rect(.25, 1), u)))
    print("== Part B: R^3, quadrature only (not a bound)")
    AX = np.vstack([np.eye(3), -np.eye(3)])
    r3 = []
    r3.append(check3d("box(1,1,1) vs box(2,.5,1) common axes", box3((1, 1, 1)), box3((2, .5, 1)), .5, 8, 8, AX))
    r3.append(check3d("cube vs cube rotated 45 about z", box3((1, 1, 1)), rot3(box3((1, 1, 1)), 2, math.pi/4), .5, 8, 8,
                       np.vstack([AX, rot3(AX, 2, math.pi/4)])))
    r3.append(check3d("cube vs octahedron r=1.5", box3((1, 1, 1)), octa(1.5), .5, 8, 4/3*1.5**3,
                       np.vstack([AX, box3((1, 1, 1))/3**.5])))
    r3.append(check3d("box(2,.3,1) vs rotated about x 50deg", box3((2, .3, 1)), rot3(box3((2, .3, 1)), 0, .87), .4, 4.8, 4.8,
                       np.vstack([AX, rot3(AX, 0, .87)])))
    c3 = check3d("NONSYM 3D: cube vs cube shifted .95(1,1,1)", box3((1, 1, 1)), box3((1, 1, 1)) + 0.95, .5, 8, 8, AX,
                 expect="fails")
    print()
    print("Part A results:", {v: res.count(v) for v in set(res)})
    print("Part B results:", {v: r3.count(v) for v in set(r3)})
    print("controls:", ctrl1, "|", ctrl2, "|", c3)
