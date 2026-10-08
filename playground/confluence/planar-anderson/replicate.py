"""Illustration (NOT a proof) of OAI.PlanarAnderson.anderson_spectrum_ae.

Lean statement, in words: for h > 0 and i.i.d. potentials v(x) ~ Uniform[-h, h] on Z^2, almost
surely the operator (H u)(x) = sum_{|y-x|=1} u(y) + v(x) u(x) on l^2(Z^2) is bounded, self-adjoint,
and spectrum(H) = [-4-h, 4+h] (as a subset of C with im = 0).

Here: finite L x L periodic boxes (a finite-volume stand-in; the theorem is about Z^2, where these
box matrices are NOT the operator). We report
  * hard check: every box eigenvalue lies in [-4-h, 4+h] (true for every box by ||H|| <= 4 + h);
  * fill: the largest gap between consecutive eigenvalues inside [-4-h, 4+h], and the extreme
    eigenvalues, as L grows (edges approach slowly -- Lifshitz tails);
  * Weyl mechanism: a planted constant patch v = w on an n x n block forces eigenvalues near
    e + w for free energies e of the block, which is how the proof reaches the edges;
  * controls that MUST fail: a checkerboard periodic potential (gap (-h, h), edges sqrt(16+h^2)),
    the zero potential (edges 4, not 4+h), and the wrong formula [-2-h, 2+h].
Run: python3 replicate.py   (numpy only; seeds fixed)
"""
import numpy as np


def hopping(L):
    n = L * L
    A = np.zeros((n, n))
    for i in range(L):
        for j in range(L):
            s = i * L + j
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                t = ((i + di) % L) * L + (j + dj) % L
                A[s, t] += 1.0
    return A


def eig(A, v):
    return np.linalg.eigvalsh(A + np.diag(v))


def max_gap_inside(ev, lo, hi):
    pts = np.concatenate(([lo], ev[(ev >= lo) & (ev <= hi)], [hi]))
    return float(np.max(np.diff(pts)))


def interior_gap(ev):
    """Largest gap between consecutive eigenvalues (edges excluded)."""
    return float(np.max(np.diff(ev)))


def main():
    rng = np.random.default_rng(20261008)
    ok = True
    print("== random potential, Uniform[-h,h], periodic L x L ==")
    for h in (1.0, 3.0):
        lo, hi = -4 - h, 4 + h
        for L in (8, 16, 32, 48):
            A = hopping(L)
            mins, maxs, gaps, igaps = [], [], [], []
            for _ in range(4 if L < 48 else 2):
                ev = eig(A, rng.uniform(-h, h, L * L))
                inside = bool(np.all((ev >= lo - 1e-9) & (ev <= hi + 1e-9)))
                ok &= inside
                mins.append(ev[0]); maxs.append(ev[-1]); igaps.append(interior_gap(ev))
            print(f"h={h} L={L:3d}: min={np.mean(mins):+.3f} max={np.mean(maxs):+.3f} "
                  f"(predicted edges {lo:+.1f},{hi:+.1f}) largest interior gap={np.mean(igaps):.4f} "
                  f"all-inside={inside}")
    print("hard check (every eigenvalue in [-4-h,4+h]):", "PASS" if ok else "FAIL")

    print("\n== Weyl mechanism: planted constant n x n patch v=w inside a random L=48 box, h=1 ==")
    h, L = 1.0, 48
    A = hopping(L)
    for n, w in ((8, 0.95), (16, 0.95), (24, 0.99)):
        v = rng.uniform(-h, h, L * L).reshape(L, L)
        v[:n, :n] = w
        ev = eig(A, v.ravel())
        # Rayleigh quotient of the Dirichlet ground state of the n x n patch (supported where v = w)
        # gives the rigorous lower bound max eig >= 4 cos(pi/(n+1)) + w.
        bound = 4 * np.cos(np.pi / (n + 1)) + w
        ok_b = ev[-1] >= bound - 1e-9
        ok &= ok_b
        print(f"patch n={n:2d} w={w}: max eig={ev[-1]:+.4f} >= 4cos(pi/(n+1))+w={bound:+.4f}: {ok_b}"
              f"  (target 4+h={4+h})")

    print("\n== controls (must FAIL the prediction [-4-h,4+h]) ==")
    h, L = 1.0, 48
    A = hopping(L)
    lo, hi = -4 - h, 4 + h
    idx = np.add.outer(np.arange(L), np.arange(L))
    cb = h * np.where(idx % 2 == 0, 1.0, -1.0).ravel()
    ev = eig(A, cb)
    gap_lo, gap_hi = ev[ev < 0].max(), ev[ev > 0].min()
    print(f"checkerboard +-h: edges {ev[0]:+.4f},{ev[-1]:+.4f} (theory +-sqrt(16+h^2)={np.sqrt(16+h*h):.4f}); "
          f"gap ({gap_lo:+.4f},{gap_hi:+.4f}) (theory (-h,h)); largest gap in interval="
          f"{max_gap_inside(ev, lo, hi):.3f}")
    cb_fails = (gap_hi - gap_lo) > 1.9 * h * 0.99 and ev[-1] < hi - 0.8
    print("  checkerboard fails to fill [-4-h,4+h]:", cb_fails)
    ev0 = eig(A, np.zeros(L * L))
    print(f"zero potential: edges {ev0[0]:+.4f},{ev0[-1]:+.4f} -> misses (4,4+h]:", ev0[-1] <= 4 + 1e-9)
    evr = eig(A, rng.uniform(-h, h, L * L))
    out = int(np.sum((evr < -2 - h) | (evr > 2 + h)))
    print(f"wrong formula [-2-h,2+h]: {out}/{L*L} random-box eigenvalues fall outside it -> formula rejected:",
          out > 0)


if __name__ == "__main__":
    main()
