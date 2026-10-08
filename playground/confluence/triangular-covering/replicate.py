#!/usr/bin/env python3
"""Independent replication of OAI.TriangularCovering.main (lean/ComparatorChallenges/TriangularCovering.lean).

Standard library + numpy only. Run from this folder:  python3 replicate.py   (no -I: numpy is a user-site package; a few minutes)

Coordinates: a point of Space is written (x, y, t) with physical coordinates (x, y, H*t), H = sqrt 2,
exactly as `point x y t` in the challenge. In (x,y,t) coordinates the Euclidean inner product is
x*x' + y*y' + 2*t*t', so every inner product / squared length / squared area below is RATIONAL
when the inputs are rational, and is computed with fractions.Fraction (exact).
Membership in a cylinder carrier (triangle + R*axis) is affine-invariant, so it is also exact.

Sections:
  A. tetrahedron K, shadow areas, A_min = sqrt 2           (+ control: A_min = sqrt 3 is refuted)
  B. the finite family of 2*n(eps) cylinders: base areas    (exact squared areas vs the closed form)
  C. area expansion totalArea/H = 1/2 - 13/6000 eps^2 + O(eps^4), strict < A_min/2
                                                           (+ control: wrong coefficient fails)
  D. covering of K, exact witnesses at adversarial and random points
                                                           (+ control: cutoff 1/2 leaves a hole)
"""
import math, random, sys, time
from fractions import Fraction as F
import numpy as np

random.seed(20261008)
OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s); sys.stdout.flush()

def ip(u, v):  # Euclidean inner product in (x,y,t) coordinates
    return u[0]*v[0] + u[1]*v[1] + 2*u[2]*v[2]
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def add(u, v): return tuple(a + b for a, b in zip(u, v))
def scl(c, u): return tuple(c*a for a in u)

# ---------------------------------------------------------------- A. tetrahedron and shadows
say("== A. tetrahedron K and A_min")
VERTS = [(F(-1), F(0), F(0)), (F(1), F(0), F(0)), (F(0), F(-1), F(1)), (F(0), F(1), F(1))]
d2 = sorted({ip(sub(p, q), sub(p, q)) for i, p in enumerate(VERTS) for q in VERTS[i+1:]})
say("squared edge lengths (exact):", d2, "-> regular tetrahedron of edge 2" if d2 == [4] else "-> NOT regular")
# K's slice at height t is [-(1-t),1-t] x [-t,t] = (1-t)*bottom edge + t*top edge, i.e. the slice of conv(VERTS).

def shadow_float(u):
    """Area of the orthogonal projection of K (= conv VERTS) on the plane normal to unit u (physical coords)."""
    P = np.array([[v[0], v[1], math.sqrt(2)*v[2]] for v in map(lambda w: tuple(float(c) for c in w), VERTS)])
    u = np.asarray(u, float); u = u/np.linalg.norm(u)
    a = np.cross(u, [1.0, 0, 0] if abs(u[0]) < 0.9 else [0, 1.0, 0]); a /= np.linalg.norm(a)
    b = np.cross(u, a)
    pts = sorted(set((round(float(p@a), 15), round(float(p@b), 15)) for p in P))
    if len(pts) < 3: return 0.0
    def cr(o, p, q): return (p[0]-o[0])*(q[1]-o[1]) - (p[1]-o[1])*(q[0]-o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cr(hi[-2], hi[-1], p) <= 0: hi.pop()
        hi.append(p)
    hull = lo[:-1] + hi[:-1]
    return abs(sum(hull[i][0]*hull[i-1][1] - hull[i-1][0]*hull[i][1] for i in range(len(hull))))/2

# exact shadow along the x-axis (parallel to the bottom edge): projected vertices (0,0,0) twice, (0,-1,1), (0,1,1)
e1, e2 = (F(0), F(1), F(1)), (F(0), F(-1), F(1))
area_sq = (ip(e1, e1)*ip(e2, e2) - ip(e1, e2)**2)/4
say("shadow along x-axis: triangle, area^2 =", area_sq, "(exact) -> area = sqrt 2 = H" if area_sq == 2 else "")
say("shadow along z-axis (float):", shadow_float([0, 0, 1]), " face normal (H,0,1) (float):", shadow_float([math.sqrt(2), 0, 1]),
    " (sqrt3 =", math.sqrt(3), ")")

# dense search over the sphere (Fibonacci points + local refinement)
M = 200000
best = (9.0, None)
gold = math.pi*(3 - math.sqrt(5))
for i in range(M):
    z = 1 - 2*(i + 0.5)/M; r = math.sqrt(1 - z*z); th = gold*i
    u = (r*math.cos(th), r*math.sin(th), z)
    # closed form of the shadow (from the 4 faces, each face area sqrt3, normals (+-H,0,1),(0,+-H,-1)):
    # shadow(u) = (1/2) * sum_i |u . N_i| = max(H|u1|,|u3|) + max(H|u2|,|u3|)
    v = max(math.sqrt(2)*abs(u[0]), abs(u[2])) + max(math.sqrt(2)*abs(u[1]), abs(u[2]))
    if v < best[0]: best = (v, u)
# check closed form against hull computation on a random sample
mx = 0.0
for _ in range(2000):
    u = np.random.default_rng(_).normal(size=3); u /= np.linalg.norm(u)
    cf = max(math.sqrt(2)*abs(u[0]), abs(u[2])) + max(math.sqrt(2)*abs(u[1]), abs(u[2]))
    mx = max(mx, abs(cf - shadow_float(u)))
say("closed form vs convex-hull area, max |diff| over 2000 random directions:", f"{mx:.2e}")
# local refinement from the best grid point
u = np.array(best[1]); step = 1e-3; val = best[0]
f = lambda w: max(math.sqrt(2)*abs(w[0]), abs(w[2])) + max(math.sqrt(2)*abs(w[1]), abs(w[2]))
rng = np.random.default_rng(1)
while step > 1e-12:
    improved = False
    for _ in range(60):
        w = u + step*rng.normal(size=3); w /= np.linalg.norm(w)
        if f(w) < val: u, val, improved = w, f(w), True
    if not improved: step /= 2
say(f"min shadow over {M} sphere points + refinement: {val:.15f} at u={np.round(u, 6)}; H = {math.sqrt(2):.15f}")
say("min - H =", f"{val - math.sqrt(2):.3e}", "(>= 0 expected; Lean proves the lower bound)")
say("CONTROL A: is A_min = sqrt3 (face shadow)?  found shadow", f"{val:.6f}", "< sqrt3 =", f"{math.sqrt(3):.6f}",
    "-> the alternative value is REFUTED" if val < math.sqrt(3) - 1e-3 else "-> NOT refuted (control failed)")

# ---------------------------------------------------------------- construction (transcribed from the Lean defs)
ETA = F(1, 1000)
def alpha(a, b): return (1 + a*b)/4
def beta(a, b): return (a + b)/4
def dq(q): return q**2*(1 + q**2)/16
def cutoffCoeff(a, b, eta=ETA): return eta + max(dq(a), dq(b))
def cutoff(eps, a, b, eta=ETA): return F(1, 2) + eps**2*cutoffCoeff(a, b, eta)
def n_of(eps):  # Nat.ceil (2/eps^2), eps rational
    q = 2/eps**2; return -((-q.numerator)//q.denominator)
def mesh(N, i): return -1 + F(i)*F(2, N)

class Family:
    """The 2N cylinders of finiteFamily eps, with an optional modified cutoff (for controls)."""
    def __init__(self, eps, cut=None):
        self.eps = eps; self.N = n_of(eps)
        self.cut = cut if cut is not None else (lambda a, b: cutoff(eps, a, b))
    def params(self, j):
        a, b = mesh(self.N, j), mesh(self.N, j + 1)
        return a, b, alpha(a, b), beta(a, b), self.cut(a, b)
    def lower(self, j):   # vertices point(0,0,0), point(0,aT,T), point(0,bT,T); axis direction tiltV = (1, eps A, H eps B)
        a, b, A, B, T = self.params(j); e = self.eps
        return [(F(0), F(0), F(0)), (F(0), a*T, T), (F(0), b*T, T)], (F(1), e*A, e*B)
    def upper(self, j):   # vertices point(0,0,1), point(aT,0,1-T), point(bT,0,1-T); axis tiltW = (-eps A, 1, H eps B)
        a, b, A, B, T = self.params(j); e = self.eps
        return [(F(0), F(0), F(1)), (a*T, F(0), 1 - T), (b*T, F(0), 1 - T)], (-e*A, F(1), e*B)
    def cyl(self, i):  # index in Fin (2N): first N lower, then N upper (Fin.append order)
        return self.lower(i) if i < self.N else self.upper(i - self.N)

def det3(c0, c1, c2):
    return (c0[0]*(c1[1]*c2[2] - c1[2]*c2[1]) - c1[0]*(c0[1]*c2[2] - c0[2]*c2[1]) + c2[0]*(c0[1]*c1[2] - c0[2]*c1[1]))

def in_carrier(cyl, P):
    """Exact test: P in conv(V0,V1,V2) + R*D.  Solve P-V0 = s1 E1 + s2 E2 + lam D (Cramer)."""
    (V0, V1, V2), D = cyl
    E1, E2, R = sub(V1, V0), sub(V2, V0), sub(P, V0)
    dt = det3(E1, E2, D)
    assert dt != 0
    s1, s2 = det3(R, E2, D)/dt, det3(E1, R, D)/dt
    return s1 >= 0 and s2 >= 0 and s1 + s2 <= 1

# ---------------------------------------------------------------- B. base areas, exact
say("\n== B. base areas of the cylinders (exact squared areas)")
def base_area_sq(cyl):
    """Squared area of the projection of the triangle on the plane normal to D (exact rational)."""
    (V0, V1, V2), D = cyl
    E1, E2 = sub(V1, V0), sub(V2, V0)
    dd = ip(D, D)
    g = lambda u, v: ip(u, v) - ip(u, D)*ip(v, D)/dd       # inner product of projected vectors
    return (g(E1, E1)*g(E2, E2) - g(E1, E2)**2)/4

eps0 = F(1, 2001)
fam = Family(eps0)
say("eps =", eps0, " n(eps) = ceil(2/eps^2) =", fam.N, " (2/eps^2 =", 2/eps0**2, ") -> 2n =", 2*fam.N, "cylinders")
bad = 0; checked = 0
for j in [0, 1, 2, fam.N//3, fam.N//2, fam.N//2 + 1, fam.N - 2, fam.N - 1] + random.sample(range(fam.N), 40):
    a, b, A, B, T = fam.params(j)
    closed = 2*(b - a)**2*T**4/(4*(1 + eps0**2*(A**2 + 2*B**2)))   # (H (b-a) T^2 / (2 sqrt(1+eps^2(A^2+2B^2))))^2
    for c in (fam.lower(j), fam.upper(j)):
        checked += 1
        if base_area_sq(c) != closed: bad += 1
        assert ip(c[1], c[1]) == 1 + eps0**2*(A**2 + 2*B**2)
say(f"exact squared-area identity checked on {checked} cylinders: {bad} mismatches")

# ---------------------------------------------------------------- C. area expansion
say("\n== C. area expansion  totalArea/H = sum_j (b-a) T_j^2 / sqrt(1+eps^2 S_j)")
def residual(eps_f, N, eta=float(ETA), chunk=4_000_000):
    """sum_j normalizedTerm - 1/2, computed as sum_j D*[eps^2 Mc + eps^4 Mc^2 + (1/4+eps^2 Mc+eps^4 Mc^2)(g-1)],
    g = (1+eps^2 S)^(-1/2), g-1 via expm1/log1p (sum_j D/4 = 1/2 exactly, D = 2/N)."""
    e2 = eps_f*eps_f; tot = []
    for s in range(0, N, chunk):
        j = np.arange(s, min(N, s + chunk), dtype=np.float64)
        a = -1 + j*(2.0/N); b = -1 + (j + 1)*(2.0/N); D = 2.0/N
        A = (1 + a*b)/4; B = (a + b)/4; S = A*A + 2*B*B
        Mc = eta + np.maximum(a*a*(1 + a*a), b*b*(1 + b*b))/16
        gm1 = np.expm1(-0.5*np.log1p(e2*S))
        term = D*(e2*Mc + e2*e2*Mc*Mc + (0.25 + e2*Mc + e2*e2*Mc*Mc)*gm1)
        tot.append(math.fsum(term.tolist()))
    return math.fsum(tot)

# pipeline cross-check with Decimal at a large eps (direct sum of the unexpanded terms, 60 digits)
from decimal import Decimal, getcontext
getcontext().prec = 60
for ec in (F(1, 20), F(1, 50)):
    N = n_of(ec); E = Decimal(ec.numerator)/Decimal(ec.denominator); s = Decimal(0)
    for j in range(N):
        a, b = mesh(N, j), mesh(N, j + 1); A, B = alpha(a, b), beta(a, b)
        T = cutoff(ec, a, b); S = A*A + 2*B*B
        num = (b - a)*T*T
        s += (Decimal(num.numerator)/Decimal(num.denominator))/(1 + E*E*Decimal(S.numerator)/Decimal(S.denominator)).sqrt()
    r_dec = s - Decimal(1)/2
    r_np = residual(float(ec), N)
    say(f"pipeline check eps={ec}: N={N}, Decimal direct sum-1/2 = {float(r_dec):.15e}, numpy residual = {r_np:.15e}, diff = {float(r_dec) - r_np:.2e}")

say("eps          N=n(eps)     R = total/H-(1/2-13/6000 eps^2)   R/eps^4    total/H < 1/2 ?   control R'/eps^4 (12/6000)")
rows = []
for ec in (F(1, 2001), F(1, 2500), F(1, 3000), F(1, 4000), F(1, 5000)):
    N = n_of(ec); e = float(ec)
    r = residual(e, N)                       # total/H - 1/2
    R = r + 13/6000*e*e
    Rc = r + 12/6000*e*e                     # wrong coefficient (control)
    rows.append((ec, N, R/e**4))
    say(f"{str(ec):10s} {N:11d}   {R: .6e}                  {R/e**4: .4f}    {r < 0}            {Rc/e**4: .4e}")
say("Lean constant C = 14; delta = eta/2 = 1/2000.  max |R/eps^4| above =", f"{max(abs(x[2]) for x in rows):.4f}")
say("CONTROL C: replacing 13/6000 by 12/6000 gives |R'|/eps^4 ~ 1/(6000 eps^2) >> 14 -> must FAIL the C*eps^4 bound")

# ---------------------------------------------------------------- D. covering
say("\n== D. covering K at eps = 1/2001 (exact rational membership)")
def find_j(fam, P, upper, tries=4):
    """Float fixed-point guess of the sector index, then an exact window check. Returns witness index or None."""
    x, y, t = map(float, P); e = float(fam.eps); N = fam.N
    j = 0
    for _ in range(30):
        a = -1 + j*2/N; b = a + 2/N; A = (1 + a*b)/4; B = (a + b)/4
        if not upper: r = t - e*x*B; z = y - e*x*A
        else: r = 1 - t + e*y*B; z = x + e*y*A
        q = z/r if r > 0 else 0.0
        jn = min(N - 1, max(0, int(math.floor((q + 1)*N/2))))
        if jn == j: break
        j = jn
    for k in range(max(0, j - tries), min(N, j + tries + 1)):
        c = fam.upper(k) if upper else fam.lower(k)
        if in_carrier(c, P): return k
    return None

def exhaustive(fam, P, cut_float):
    """Return list of ALL cylinder indices that contain P: float prefilter (tolerance 1e-9) + exact check."""
    x, y, t = map(float, P); e = float(fam.eps); N = fam.N
    j = np.arange(N, dtype=np.float64); a = -1 + j*(2.0/N); b = -1 + (j + 1)*(2.0/N)
    A = (1 + a*b)/4; B = (a + b)/4; T = cut_float(a, b)
    hits = []
    for upper in (False, True):
        if not upper: r = t - e*x*B; z = y - e*x*A
        else: r = 1 - t + e*y*B; z = x + e*y*A
        m = np.minimum.reduce([r, T - r, z - a*r, b*r - z])
        cand = np.nonzero(m > -1e-9)[0]
        for k in cand.tolist():
            c = fam.upper(k) if upper else fam.lower(k)
            if in_carrier(c, P): hits.append(N*upper + k)
        say(f"    exhaustive {'upper' if upper else 'lower'}: {len(cand)} float candidates (margin > -1e-9), "
            f"max float margin {m.max():.3e}")
    return hits

def G_float(fam, x, y):
    """Sum of the two cutoff slacks at t=1/2 (float): G = (T_j - r) + (T_k - s), j,k the sector indices.
    If G > 0 every t near 1/2 is covered by one of the two families; the worst t splits G evenly."""
    e = float(fam.eps); N = fam.N
    def idx(upper, t):
        j = 0
        for _ in range(30):
            a = -1 + j*2/N; b = a + 2/N; A = (1 + a*b)/4; B = (a + b)/4
            r, z = ((1 - t + e*y*B), (x + e*y*A)) if upper else ((t - e*x*B), (y - e*x*A))
            jn = min(N - 1, max(0, int(math.floor((z/r + 1)*N/2))))
            if jn == j: break
            j = jn
        a = -1 + j*2/N; b = a + 2/N
        return j, a, b, (1 + a*b)/4, (a + b)/4
    j, a, b, A, B = idx(False, 0.5); k, c, d_, Ac, Bc = idx(True, 0.5)
    Tj = float(fam.cut(F(j*2 - N, N), F((j + 1)*2 - N, N))); Tk = float(fam.cut(F(k*2 - N, N), F((k + 1)*2 - N, N)))
    mL = Tj - (0.5 - e*x*B); mU = Tk - (0.5 + e*y*Bc)
    return mL + mU, (mL - mU)/2

def adversarial(fam, label, grid=161, exact_worst=150):
    e2 = float(fam.eps)**2
    g = np.linspace(-0.4999, 0.4999, grid)
    vals = []
    for x in g:
        for y in g:
            G, dt = G_float(fam, float(x), float(y)); vals.append((G, float(x), float(y), dt))
    vals.sort()
    say(f"  [{label}] grid {grid}x{grid} of (x,y), t=1/2: min G/eps^2 = {vals[0][0]/e2:.6f} at (x,y)=({vals[0][1]:.4f},{vals[0][2]:.4f}); "
        f"max G/eps^2 = {vals[-1][0]/e2:.6f}; #G<0: {sum(1 for v in vals if v[0] < 0)}")
    return vals[:exact_worst]

def rat(v, den=10**9): return F(round(v*den), den)

def check_points(fam, pts, label):
    unc = []
    for P in pts:
        if find_j(fam, P, False) is None and find_j(fam, P, True) is None: unc.append(P)
    say(f"  [{label}] {len(pts)} points, uncovered by window search: {len(unc)}")
    return unc

# --- real family
t0 = time.time()
worst = adversarial(fam, "real family")
pts = []
for G, x, y, dt in worst:
    pts.append((rat(x), rat(y), F(1, 2) + rat(dt, 10**18)))   # t* = 1/2 + (mL - mU)/2 : both slacks ~ G/2
# exact boundary points, vertices, edges, and boundary corners near t = 1/2
for (x, y, t) in [(-1, 0, 0), (1, 0, 0), (0, -1, 1), (0, 1, 1), (0, 0, 0), (0, 0, 1), (F(1, 2), F(1, 2), F(1, 2)),
                  (-F(1, 2), F(1, 2), F(1, 2)), (F(1, 2), -F(1, 2), F(1, 2)), (-F(1, 2), -F(1, 2), F(1, 2))]:
    pts.append((F(x), F(y), F(t)))
for _ in range(300):
    x = rat(random.uniform(-1, 1)); pts.append((x, F(0), F(0)))             # bottom edge
    y = rat(random.uniform(-1, 1)); pts.append((F(0), y, F(1)))             # top edge
    t = rat(random.random()); sx, sy = random.choice((-1, 1)), random.choice((-1, 1))
    pts.append((sx*(1 - t), sy*t, t))                                       # lateral edges
    t = F(1, 2) + rat(random.uniform(-1e-6, 1e-6), 10**15)
    pts.append((sx*(1 - t), rat(random.uniform(-1, 1))*t, t))              # faces near t = 1/2
    pts.append((rat(random.uniform(-1, 1))*(1 - t), sy*t, t))
for _ in range(6000):                                                       # random interior points
    t = rat(random.random()); pts.append((rat(random.uniform(-1, 1))*(1 - t), rat(random.uniform(-1, 1))*t, t))
for _ in range(3000):                                                       # random points in the critical slab
    t = F(1, 2) + rat(random.uniform(-3e-7, 3e-7), 10**15)
    pts.append((rat(random.uniform(-1, 1))*(1 - t), rat(random.uniform(-1, 1))*t, t))
for P in pts: assert 0 <= P[2] <= 1 and abs(P[0]) <= 1 - P[2] and abs(P[1]) <= P[2]
unc = check_points(fam, pts, "real family")
for P in unc[:20]:
    say("  window search missed", P, "-> exhaustive:")
    h = exhaustive(fam, P, lambda a, b: 0.5 + float(eps0)**2*(float(ETA) + np.maximum(a*a*(1 + a*a), b*b*(1 + b*b))/16))
    say("    covering cylinders:", h[:10])
say(f"  (section D real family: {time.time() - t0:.0f}s)")

# --- CONTROL D: cutoff exactly 1/2 (drop the eps^2 * cutoffCoeff term)
say("\n  CONTROL D: same cylinders but cutoff T = 1/2 (eps^2 term removed). Must leave part of K uncovered.")
famc = Family(eps0, cut=lambda a, b: F(1, 2))
worstc = adversarial(famc, "cutoff 1/2", grid=81, exact_worst=5)
found = None
for G, x, y, dt in worstc:
    P = (rat(x), rat(y), F(1, 2) + rat(dt, 10**18))
    if find_j(famc, P, False) is None and find_j(famc, P, True) is None:
        found = P; break
if found is None:
    say("  CONTROL D: no uncovered point found by window search -> control did NOT fail")
else:
    say("  candidate hole:", found, "=", tuple(float(c) for c in found))
    hits = exhaustive(famc, found, lambda a, b: 0.5 + 0*a)
    say("  CONTROL D result: cylinders (of all", 2*famc.N, ") containing it exactly:", hits,
        "-> UNCOVERED, control fails as required" if not hits else "-> covered, control did not fail")
    # and the same point is covered by the real family:
    say("  the same point under the real family: lower witness", find_j(fam, found, False), " upper witness", find_j(fam, found, True))

# --- eta = 0 variant (informational: is the 1/1000 slack necessary at this eps?)
fam0 = Family(eps0, cut=lambda a, b: cutoff(eps0, a, b, eta=F(0)))
worst0 = adversarial(fam0, "eta = 0 (informational)", grid=161, exact_worst=20)
hole0 = None
for G, x, y, dt in worst0:
    if G >= 0: break
    P = (rat(x), rat(y), F(1, 2) + rat(dt, 10**18))
    if find_j(fam0, P, False) is None and find_j(fam0, P, True) is None: hole0 = P; break
if hole0 is None:
    say("  eta = 0: no exact hole found among the negative-G grid points")
else:
    say("  eta = 0 candidate hole:", hole0, "=", tuple(float(c) for c in hole0))
    h0 = exhaustive(fam0, hole0, lambda a, b: 0.5 + float(eps0)**2*(np.maximum(a*a*(1 + a*a), b*b*(1 + b*b))/16))
    say("  eta = 0 result: cylinders containing it exactly:", h0, "-> UNCOVERED: the 1/1000 slack is load-bearing at this eps" if not h0 else "-> covered")
    say("  the same point under the real family: lower witness", find_j(fam, hole0, False), " upper witness", find_j(fam, hole0, True))

open(__file__.replace("replicate.py", "replicate-output.txt"), "w").write("\n".join(OUT) + "\n")
