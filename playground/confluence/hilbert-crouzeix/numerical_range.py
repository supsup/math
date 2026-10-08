"""Independent numerical checks for OAI.HilbertCrouzeix.numericalClosure_geometry (finite matrices).

The theorem: closure(W(A)) is compact, convex, and contains spectrum(A), where
W(A) = { <x, A x> : ||x|| = 1 } (Mathlib inner product: conjugate-linear in the FIRST slot, so
<x, A x> = x^* A x).  In finite dimension W(A) is already compact, so closure is a no-op there.

Checks per matrix:
  K  compactness proxy : every sampled |x^*Ax| <= ||A||_2.
  C1 convexity (support): every sampled x^*Ax and every eigenvalue lies in the intersection of the
     half-planes Re(e^{-it} z) <= lambda_max(Re(e^{-it} A))  (this intersection IS conv W, so this
     checks containment, not convexity by itself).
  C2 convexity (constructive, Toeplitz-Hausdorff): for random unit x, y, the midpoint of x^*Ax and
     y^*Ay is ATTAINED by an explicit unit vector v in span{x, y}; we search for v and report the
     residual |v^*Av - midpoint|.
  S  spectrum inclusion: eigenvalues satisfy the half-plane inequalities (inside conv W = W).
Controls (must FAIL):
  N1 real-vector variant {x^T A x : x real unit} of a 2x2 complex matrix: midpoint NOT attained
     (the set is a closed curve, not convex).
  N2 'spectrum in the interior of W' for a normal matrix: eigenvalues are vertices, on the boundary.
  N3 'W = conv(spectrum)' for the 2x2 Jordan block: W is the disk of radius 1/2, spectrum is {0}.
Context (not a check of this theorem): Crouzeix ratios ||p(A)|| / max_{W} |p|.
"""
import numpy as np

rng = np.random.default_rng(20261008)
TS = np.linspace(0, 2 * np.pi, 2048, endpoint=False)


def support(A, t):
    H = (np.exp(-1j * t) * A + np.conj(np.exp(-1j * t) * A).T) / 2
    w, V = np.linalg.eigh(H)
    return w[-1], V[:, -1]


def boundary(A):
    pts = []
    for t in TS:
        _, v = support(A, t)
        pts.append(np.vdot(v, A @ v))
    pts = np.array(pts)
    # numpy 2.x on macOS/Accelerate can emit spurious matmul RuntimeWarnings; prove the values are finite
    assert np.all(np.isfinite(pts)), "non-finite boundary point"
    return pts


def in_conv_W(A, z, tol=1e-9):
    worst = -np.inf
    for t in TS[::8]:
        lam, _ = support(A, t)
        worst = max(worst, (np.exp(-1j * t) * z).real - lam)
    return worst <= tol, worst


def rand_unit(n, real=False):
    x = rng.standard_normal(n) + (0 if real else 1j * rng.standard_normal(n))
    return x / np.linalg.norm(x)


def attain(A, target, x, y):
    """min over unit v in span{x,y} of |v^*Av - target|; grid then local refinement."""
    q, _ = np.linalg.qr(np.stack([x, y], axis=1))
    B = np.conj(q).T @ A @ q
    best = (np.inf, None)
    def val(th, ph):
        v = np.array([np.cos(th), np.exp(1j * ph) * np.sin(th)])
        return abs(np.vdot(v, B @ v) - target)
    phs = np.linspace(0, 2 * np.pi, 181)
    for th in np.linspace(0, np.pi, 181):
        for ph in phs:
            r = val(th, ph)
            if r < best[0]:
                best = (r, (th, ph))
    th, ph = best[1]
    step = np.pi / 180
    while step > 1e-13:
        improved = False
        for dth, dph in ((step, 0), (-step, 0), (0, step), (0, -step)):
            r = val(th + dth, ph + dph)
            if r < best[0]:
                best, th, ph, improved = (r, (th + dth, ph + dph)), th + dth, ph + dph, True
        if not improved:
            step /= 2
    return best[0]


def real_attain(A, target):
    """Real-vector variant on R^2 directly: min over real unit v of |v^T A v - target|."""
    th = np.linspace(0, np.pi, 200001)
    v = np.stack([np.cos(th), np.sin(th)])
    vals = np.einsum('it,ij,jt->t', v, A, v)
    return np.min(np.abs(vals - target))


def jordan(n, lam=0.0):
    return lam * np.eye(n) + np.diag(np.ones(n - 1), 1)


def main():
    examples = {
        "normal diag(1, i, -1+0.5i)": np.diag([1, 1j, -1 + 0.5j]).astype(complex),
        "Jordan J2 (disk r=1/2)": jordan(2).astype(complex),
        "Jordan J4 (disk r=cos(pi/5))": jordan(4).astype(complex),
        "2x2 [[1,2],[0,i]] (ellipse)": np.array([[1, 2], [0, 1j]], dtype=complex),
    }
    for k in range(3):
        n = 3 + k
        examples[f"random complex {n}x{n} #{k}"] = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))

    all_ok = True
    print("== checks (must PASS) ==")
    for name, A in examples.items():
        n = A.shape[0]
        nrm = np.linalg.norm(A, 2)
        samples = []
        for _ in range(400):
            x = rand_unit(n)
            samples.append(np.vdot(x, A @ x))
        K = max(abs(z) for z in samples) <= nrm + 1e-12
        C1 = all(in_conv_W(A, z)[0] for z in samples[:60])
        eig = np.linalg.eigvals(A)
        S_res = [in_conv_W(A, l) for l in eig]
        S = all(ok for ok, _ in S_res)
        c2 = []
        for _ in range(8):
            x, y = rand_unit(n), rand_unit(n)
            mid = (np.vdot(x, A @ x) + np.vdot(y, A @ y)) / 2
            c2.append(attain(A, mid, x, y))
        C2 = max(c2) < 1e-9
        ok = K and C1 and C2 and S
        all_ok &= ok
        print(f"{name:32s} K={K} C1={C1} C2={C2}(max resid {max(c2):.1e}) S={S} "
              f"(max eig excess {max(w for _, w in S_res):.1e})  {'PASS' if ok else 'FAIL'}")

    # Jordan disk radius check: W(J_n) is the disk of radius cos(pi/(n+1))
    for n in (2, 4):
        b = boundary(jordan(n).astype(complex))
        r = np.abs(b)
        print(f"J{n}: boundary |z| in [{r.min():.12f}, {r.max():.12f}], expected cos(pi/{n+1}) = {np.cos(np.pi/(n+1)):.12f}")
        all_ok &= abs(r.min() - np.cos(np.pi / (n + 1))) < 1e-9 and abs(r.max() - np.cos(np.pi / (n + 1))) < 1e-9

    # Infinite-dimensional motivation for the closure: diag(1/k) truncated; W_N = [1/N, 1], 0 not in W_N
    print("diag(1/k), k=1..N: min Re W =", [round(float(np.min(boundary(np.diag(1 / np.arange(1, N + 1)).astype(complex)).real)), 6) for N in (5, 50, 500)],
          "-> 0 (spectrum point of the l^2 operator, in closure(W) but not in W)")

    print("\n== negative controls (must FAIL the property) ==")
    A2 = np.array([[1, 2], [0, 1j]], dtype=complex)
    worst = 0.0
    for _ in range(20):
        x, y = rand_unit(2, real=True), rand_unit(2, real=True)
        mid = (x @ A2 @ x + y @ A2 @ y) / 2
        worst = max(worst, real_attain(A2, mid))
    N1 = worst > 1e-3
    print(f"N1 real-vector range of [[1,2],[0,i]]: worst midpoint miss {worst:.4f} -> property fails: {N1}")
    D = examples["normal diag(1, i, -1+0.5i)"]
    exc = [in_conv_W(D, l)[1] for l in np.linalg.eigvals(D)]
    N2 = all(abs(e) < 1e-9 for e in exc)
    print(f"N2 normal matrix eigenvalue excess {['%.1e' % e for e in exc]} (all on boundary) -> 'spectrum in interior' fails: {N2}")
    N3 = in_conv_W(jordan(2).astype(complex), 0.45)[0] and abs(0.45) > 0
    print(f"N3 J2: 0.45 in W but conv(spectrum)={{0}} -> 'W = conv spectrum' fails: {N3}")
    all_ok &= N1 and N2 and N3

    print("\n== context only: Crouzeix ratios ||p(A)|| / max_W |p|  (<= 1+sqrt2 = 2.414 known; conjecture 2) ==")
    def ratio(A, coeffs):
        P = sum(c * np.linalg.matrix_power(A, k) for k, c in enumerate(coeffs))
        b = boundary(A)
        pv = np.abs(sum(c * b ** k for k, c in enumerate(coeffs)))
        return np.linalg.norm(P, 2) / pv.max()
    best = 0
    for name, A in examples.items():
        rs = [ratio(A, [0, 1])] + [ratio(A, rng.standard_normal(4) + 1j * rng.standard_normal(4)) for _ in range(5)]
        best = max(best, max(rs))
        print(f"{name:32s} p=z: {rs[0]:.4f}   random cubics max: {max(rs[1:]):.4f}")
    print(f"J4 with p=z^3: {ratio(jordan(4).astype(complex), [0,0,0,1]):.4f} (= 1/cos(pi/5)^3)")
    print(f"max ratio seen {best:.4f} (J2, p=z gives exactly 2: the known extremal case)")

    print("\nOVERALL", "PASS" if all_ok else "FAIL")


if __name__ == "__main__":
    main()
