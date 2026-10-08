"""Independent numerical checks for OAI.CrouzeixHilbert.hilbert (finite-dimensional only).

For a matrix A:
  * boundary of W(A) via support functions: for each angle t, the top eigenvector x of
    Re(e^{-it} A) gives the boundary point x*Ax (these points lie ON W, so a max over them is a
    LOWER bound for max_W, and the computed ratio is an UPPER bound for the true ratio:
    conservative in the direction of finding a violation).
  * ratio  ||p(A)|| / max_{bdry W} |p|   (scalar), and the matrix-valued ("complete") version
    ||sum_k A^k (x) B_k|| / max_{bdry W} ||sum_k z^k B_k||_op.
  * rational r(z) = 1/(z-c) with c outside W:  r(A) = (A - c)^{-1}.
  * Dunford/Cauchy: f(A) = (1/2 pi i) \oint f(z) (z - A)^{-1} dz over the boundary of W + delta*D
    (a convex C^1 curve enclosing W, so index 1 on W), compared with f(A) computed directly.
Negative controls (each must FAIL): W replaced by conv(spectrum); constant 2 replaced by 1.9.
Run: python3 crouzeix_check.py   (numpy only)
"""
import numpy as np

rng = np.random.default_rng(20261008)
NT = 4096
FAIL = []


def opnorm(M):
    return np.linalg.norm(M, 2)


def boundary(A, nt=NT):
    ts = np.linspace(0, 2 * np.pi, nt, endpoint=False)
    pts = np.empty(nt, complex)
    for k, t in enumerate(ts):
        Hm = (np.exp(-1j * t) * A + np.exp(1j * t) * A.conj().T) / 2
        w, V = np.linalg.eigh(Hm)
        x = V[:, -1]
        pts[k] = np.vdot(x, A @ x)  # vdot conjugates the first argument: x* A x
    return ts, pts


def peval(A, coeffs):
    """coeffs[k] scalar or matrix B_k; returns sum A^k (x) B_k (kron)."""
    n = A.shape[0]
    P = None
    Ak = np.eye(n, dtype=complex)
    for B in coeffs:
        B = np.atleast_2d(np.asarray(B, complex))
        term = np.kron(Ak, B)
        P = term if P is None else P + term
        Ak = Ak @ A
    return P


def pz(z, coeffs):
    out = None
    for k, B in enumerate(coeffs):
        B = np.atleast_2d(np.asarray(B, complex))
        out = z ** k * B if out is None else out + z ** k * B
    return out


def supW(pts, coeffs):
    return max(opnorm(pz(z, coeffs)) for z in pts)


def jordan(n):
    return np.diag(np.ones(n - 1), 1).astype(complex)


def report(name, ratio, bound=2.0, expect_fail=False):
    ok = ratio <= bound + 1e-9
    status = "ok" if ok else "EXCEEDS"
    print(f"  {name:48s} ratio = {ratio:.12f}  [{status} vs {bound}]")
    if expect_fail:
        if ok:
            FAIL.append(f"control did not fail: {name}")
    elif not ok:
        FAIL.append(name)
    return ratio


# ---------------------------------------------------------------- scalar polynomials
print("== scalar polynomials: ||p(A)|| / max_W |p|")
cases = {
    "J2": jordan(2),
    "J3": jordan(3),
    "J4": jordan(4),
    "J6": jordan(6),
    "[[1,2],[0,i]]": np.array([[1, 2], [0, 1j]], complex),
    "[[0,5],[0,0.3]]": np.array([[0, 5], [0, 0.3]], complex),
    "normal diag(1,i,-1)": np.diag([1, 1j, -1]).astype(complex),
}
for k in range(3):
    cases[f"random 4x4 #{k}"] = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
polys = {
    "z": [0, 1],
    "z^2": [0, 0, 1],
    "z^3": [0, 0, 0, 1],
    "1+2z-z^3": [1, 2, 0, -1],
}
bounds = {}
for an, A in cases.items():
    ts, pts = boundary(A)
    bounds[an] = pts
    for pn, c in polys.items():
        num = opnorm(peval(A, c))
        den = supW(pts, c)
        if den < 1e-12:
            continue
        report(f"{an}, p={pn}", num / den)

# exact J2 / p = z: W(J2) is the disk of radius 1/2
pts = bounds["J2"]
print(f"  J2 boundary radius: min {abs(pts).min():.15f} max {abs(pts).max():.15f} (expect 0.5)")
r = opnorm(jordan(2)) / np.abs(pts).max()
print(f"  J2, p=z exact ratio = {r:.15f} (expect 2)")
if abs(r - 2) > 1e-12:
    FAIL.append("J2 ratio not 2")
# SharpConstant instance: B = (0, 2): supNorm = 1, ||2 J2|| = 2
print(f"  SharpConstant witness p=2z on J2: sup_W = {supW(pts, [0, 2]):.15f}, ||p(A)|| = {opnorm(peval(jordan(2), [0, 2])):.15f}")

# ---------------------------------------------------------------- random search
print("== random search (3x3 matrices, random cubics), max ratio seen")
best = 0
for trial in range(400):
    A = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    if trial % 2:
        A = np.triu(A)  # push toward non-normal
    _, pts = boundary(A, 1024)
    c = list(rng.normal(size=4) + 1j * rng.normal(size=4))
    best = max(best, opnorm(peval(A, c)) / supW(pts, c))
report("max over 400 random (A, cubic)", best)

# ---------------------------------------------------------------- matrix-valued (complete)
print("== matrix-valued polynomials sum A^k (x) B_k, B_k 2x2 (the 'complete' version)")
best = 0
for trial in range(200):
    A = np.triu(rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)))
    _, pts = boundary(A, 1024)
    c = [rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2)) for _ in range(3)]
    best = max(best, opnorm(peval(A, c)) / supW(pts, c))
report("max over 200 random (A, 2x2 matrix quadratic)", best)
# a structured matrix example on J2: B0 = 0, B1 = E_12 (nilpotent) -> J2 (x) E12
c = [np.zeros((2, 2)), np.array([[0, 1], [0, 0]])]
report("J2, B1 = E12", opnorm(peval(jordan(2), c)) / supW(bounds["J2"], c))

# ---------------------------------------------------------------- rational
print("== rational r(z) = 1/(z - c), c outside W:  ||(A - c)^{-1}|| / max_W |r|")
for an in ["J2", "J4", "[[1,2],[0,i]]", "random 4x4 #0"]:
    A = cases[an]
    pts = bounds[an]
    R = np.abs(pts).max()
    for cpole in [1.2 * R, R + 0.05, -1j * (R + 0.3)]:
        dist = np.abs(pts - cpole).min()
        if dist < 1e-3:
            continue
        num = opnorm(np.linalg.inv(A - cpole * np.eye(len(A))))
        den = np.abs(1 / (pts - cpole)).max()
        report(f"{an}, pole {cpole:.3f}", num / den)

# ---------------------------------------------------------------- Dunford integral
print("== Dunford/Cauchy integral over boundary of W + delta D vs direct evaluation")


def contour(A, delta, nt=NT):
    ts, pts = boundary(A, nt)
    return pts + delta * np.exp(1j * ts)  # boundary point in direction t, pushed out along normal


def dunford(A, f, gamma):
    n = len(A)
    I = np.eye(n)
    z = gamma
    zn = np.roll(z, -1)
    mids = (z + zn) / 2
    dz = zn - z
    acc = np.zeros((n, n), complex)
    for m, d in zip(mids, dz):
        acc += f(m) * np.linalg.solve(m * I - A, I) * d
    return acc / (2j * np.pi)


for an in ["J2", "J4", "[[1,2],[0,i]]", "random 4x4 #0"]:
    A = cases[an]
    n = len(A)
    g = contour(A, 0.25, 8192)
    # winding number of the contour about the eigenvalues (must be 1)
    wind = [np.sum(np.diff(np.unwrap(np.angle(np.append(g, g[0]) - ev)))) / (2 * np.pi)
            for ev in np.linalg.eigvals(A)]
    p = lambda z: 1 + 2 * z - z ** 3
    Pd = np.eye(n) + 2 * A - A @ A @ A
    Pc = dunford(A, p, g)
    cpole = 1.5 * np.abs(bounds[an]).max() + 0.6
    Rd = np.linalg.inv(A - cpole * np.eye(n))
    Rc = dunford(A, lambda z: 1 / (z - cpole), g)
    Ed = np.eye(n)
    from_exp = dunford(A, np.exp, g)
    # exp(A) directly via eigen-free power series
    E = np.eye(n, dtype=complex); term = np.eye(n, dtype=complex)
    for k in range(1, 60):
        term = term @ A / k
        E = E + term
    e1 = opnorm(Pc - Pd) / opnorm(Pd)
    e2 = opnorm(Rc - Rd) / opnorm(Rd)
    e3 = opnorm(from_exp - E) / opnorm(E)
    poleinside = np.abs(g - cpole).min()
    print(f"  {an:16s} winding about eigenvalues {np.round(wind, 6)}; rel.err poly {e1:.2e}, "
          f"rational(pole {cpole:.2f}, dist to contour {poleinside:.2f}) {e2:.2e}, exp {e3:.2e}")
    if max(e1, e2, e3) > 1e-5 or any(abs(w - 1) > 1e-6 for w in wind):
        FAIL.append(f"dunford mismatch {an}")
    # Control: a contour that does NOT enclose W (shifted far away) gives f(A) = 0, not p(A)
    gbad = g + 10 * (np.abs(bounds[an]).max() + 1)
    bad = dunford(A, p, gbad)
    print(f"  {'':16s} control: contour shifted off W gives ||integral|| = {opnorm(bad):.2e} vs ||p(A)|| = {opnorm(Pd):.3f} (must differ)")
    if opnorm(bad - Pd) < 1e-3:
        FAIL.append(f"contour control did not fail {an}")

# ---------------------------------------------------------------- negative controls
print("== NEGATIVE CONTROLS (each must exceed its bound)")
for n in [2, 4, 8]:
    J = jordan(n)
    ev = np.linalg.eigvals(J)
    den = np.abs(ev).max()  # conv(spectrum) = {0}: max |z| = 0 (numerically ~1e-8 for J8)
    num = opnorm(J)
    ratio = np.inf if den < 1e-6 else num / den
    report(f"W -> conv(spectrum), J{n}, p=z", ratio, expect_fail=True)
report("constant 2 -> 1.9, J2, p=z", opnorm(jordan(2)) / np.abs(bounds["J2"]).max(), bound=1.9,
       expect_fail=True)
# W computed with x^T A x (conjugate dropped, real-slot mistake) on [[1,2],[0,i]]: a set that is
# not W; with it the ratio is not the Crouzeix ratio. Shown for information only.
A = cases["[[1,2],[0,i]]"]
pts_bad = []
for t in np.linspace(0, 2 * np.pi, NT, endpoint=False):
    x = np.array([np.cos(t), np.sin(t)])
    pts_bad.append(x @ A @ x)
pts_bad = np.array(pts_bad)
print(f"  (info) real-vector 'range' of [[1,2],[0,i]]: max|z| = {np.abs(pts_bad).max():.4f} vs true W max|z| = {np.abs(bounds['[[1,2],[0,i]]']).max():.4f}")

print()
print("OVERALL:", "PASS" if not FAIL else "FAIL " + "; ".join(FAIL))
raise SystemExit(0 if not FAIL else 1)
