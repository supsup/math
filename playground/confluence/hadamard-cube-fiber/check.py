"""Numerical replication of OAI.HadamardSix.rowRatio_cubeFiber_sum_zero
(lean/ComparatorChallenges/HadamardCubeFiber.lean).

Statement, definition for definition:
  H : 6x6 complex.  Unimodular H := all |H_ik| = 1.
  IsComplexHadamard H := Unimodular H and H^* H = 6 I.
  entrywiseSquare H := (H_ik^2).
  rowRatio H i j k := H_ik * conj(H_jk).
  cubeFiber v z := { k : v_k^3 = z }.
  Hypotheses: hH: H Hadamard; hs: entrywiseSquare H Hadamard; i != j; a != b;
              hab: every rowRatio_k^3 is a or b.
  Conclusion: sum_{k in cubeFiber(rowRatio H i j, a)} H_ik conj(H_jk) = 0.

Exact equalities (v_k^3 = a) are tested with tolerance TOL. Run: python3 check.py (numpy needed).
"""
import itertools
import numpy as np

TOL = 1e-8
rng = np.random.default_rng(20261008)
W3 = np.exp(2j * np.pi / 3)


# ---------------------------------------------------------------- the definitions
def unimodular_res(H):
    return np.max(np.abs(np.abs(H) - 1))


def hadamard_res(H):
    n = H.shape[0]
    return max(unimodular_res(H), np.max(np.abs(H.conj().T @ H - n * np.eye(n))))


def square(H):
    return H ** 2


def row_ratio(H, i, j):
    return H[i] * H[j].conj()


def cube_classes(v):
    """Distinct values of v_k^3, clustered with tolerance TOL."""
    reps = []
    for c in v ** 3:
        if not any(abs(c - r) < TOL for r in reps):
            reps.append(c)
    return reps


def fiber_sum(H, i, j, a):
    v = row_ratio(H, i, j)
    return sum(H[i, k] * H[j, k].conj() for k in range(len(v)) if abs(v[k] ** 3 - a) < TOL)


def admissible_ab(v):
    """All (a, b) choices that satisfy hne and hab, up to the irrelevant spare value.

    Two cube values {c1, c2}: (a, b) = (c1, c2) or (c2, c1).
    One cube value c: (a, b) = (c, other) [fiber = everything] or (other, c) [fiber empty].
    Three or more: hab is unsatisfiable, the theorem says nothing.
    """
    cl = cube_classes(v)
    if len(cl) == 2:
        return [(cl[0], cl[1]), (cl[1], cl[0])]
    if len(cl) == 1:
        other = cl[0] + 1.0  # any value != cl[0]
        return [(cl[0], other), (other, cl[0])]
    return []


def theorem_quantity(H):
    """Max |fiber sum| over all ordered pairs i != j and all admissible (a, b); plus bookkeeping."""
    worst, n_inst, n_nontriv, n_pairs_no_hab = 0.0, 0, 0, 0
    for i, j in itertools.permutations(range(H.shape[0]), 2):
        v = row_ratio(H, i, j)
        abs_ = admissible_ab(v)
        if not abs_:
            n_pairs_no_hab += 1
        if len(cube_classes(v)) == 2:
            n_nontriv += 1
        for a, _b in abs_:
            n_inst += 1
            worst = max(worst, abs(fiber_sum(H, i, j, a)))
    return worst, n_inst, n_nontriv, n_pairs_no_hab


# ---------------------------------------------------------------- families
def fourier6():
    return np.exp(2j * np.pi * np.outer(range(6), range(6)) / 6)


def fourier_affine(a, b):
    """F6^(2)(a,b) = F6 o EXP(i R(a,b)), Tadej-Zyczkowski catalogue form (verified numerically below)."""
    R = np.zeros((6, 6))
    for r in (1, 3, 5):
        R[r] = [0, a, b, 0, a, b]
    return fourier6() * np.exp(1j * R)


def dita_product(d1, d2):
    """[[F3, D F3], [F3, -D F3]], D = diag(1, e^{i d1}, e^{i d2}): rows orthogonal since F3 F3^* = 3I."""
    F3 = np.exp(2j * np.pi * np.outer(range(3), range(3)) / 3)
    D = np.diag([1, np.exp(1j * d1), np.exp(1j * d2)])
    return np.block([[F3, F3 @ D], [F3, -F3 @ D]])


def dita_D6(c):
    """Dita's one-parameter family D6^(1)(c) (catalogue form; verified numerically below)."""
    I, e, f = 1j, np.exp(1j * c), np.exp(-1j * c)
    return np.array([
        [1, 1, 1, 1, 1, 1],
        [1, -1, I, -I, -I, I],
        [1, I, -1, I * e, -I * e, -I],
        [1, -I, I * f, -1, I, -I * f],
        [1, -I, -I * f, I, -1, I * f],
        [1, I, -I, -I * e, I * e, -1]])


def tao_lean():
    """taoMatrix from lean/OAI/LinearAlgebra/Hadamard/Basic.lean, exponent rule copied exactly."""
    def ex(i, j):
        if i == 0 or j == 0 or i == j:
            return 0
        d = (i - j) % 5  # Lean Int.emod: result in [0,5), same as Python % for positive modulus
        return 1 if d in (1, 4) else -1
    return np.array([[W3 ** ex(i, j) for j in range(6)] for i in range(6)])


def random_equivalent(H):
    """u_i * H[r(i), c(j)] * v_j with random permutations and random unit phases."""
    r, c = rng.permutation(6), rng.permutation(6)
    u, v = np.exp(2j * np.pi * rng.random(6)), np.exp(2j * np.pi * rng.random(6))
    return u[:, None] * H[np.ix_(r, c)] * v[None, :]


# ---------------------------------------------------------------- search for S-Hadamard matrices
def lm_search(start, iters=300):
    """Levenberg-Marquardt on phases theta (H = e^{i theta}) for H^*H = 6I and (H^2)^*(H^2) = 6I."""
    th = start.ravel().copy()

    def resid(th):
        H = np.exp(1j * th.reshape(6, 6))
        S = H ** 2
        E1 = H.conj().T @ H - 6 * np.eye(6)
        E2 = S.conj().T @ S - 6 * np.eye(6)
        return H, S, np.concatenate([E1.real.ravel(), E1.imag.ravel(), E2.real.ravel(), E2.imag.ravel()])

    lam = 1e-2
    H, S, r = resid(th)
    for _ in range(iters):
        J = np.empty((r.size, 36))
        for p in range(36):
            jj, kk = divmod(p, 6)
            dH = np.zeros((6, 6), complex); dH[jj, kk] = 1j * H[jj, kk]
            dS = np.zeros((6, 6), complex); dS[jj, kk] = 2j * S[jj, kk]
            d1 = dH.conj().T @ H + H.conj().T @ dH
            d2 = dS.conj().T @ S + S.conj().T @ dS
            J[:, p] = np.concatenate([d1.real.ravel(), d1.imag.ravel(), d2.real.ravel(), d2.imag.ravel()])
        g = J.T @ r
        step = np.linalg.solve(J.T @ J + lam * np.eye(36), -g)
        H2, S2, r2 = resid(th + step)
        if r2 @ r2 < r @ r:
            th, H, S, r, lam = th + step, H2, S2, r2, max(lam / 3, 1e-12)
        else:
            lam *= 4
        if r @ r < 1e-26:
            break
    return np.exp(1j * th.reshape(6, 6)), np.sqrt(r @ r)


def dephase(H):
    H = H / H[0][None, :]          # first row -> 1
    return H / H[:, [0]]           # first column -> 1


def is_cube_root_matrix(H):
    return np.max(np.abs(H ** 3 - 1))


# ---------------------------------------------------------------- vector-level lemma (the real content)
def vector_lemma_trials(n=2000):
    """ratio_cubeFiber_sum_zero at vector level: |v_k|=1, sum v = 0, sum v^2 = 0, cubes in {a,b}.
    Population 1: constructed v = perm(u*(1,w,w^2), x*(1,w,w^2)).  Population 2: LM-found solutions of
    sum v = sum v^2 = 0 from random phases (not constructed to be two-triples)."""
    worst_c, worst_s, found, two_valued = 0.0, 0.0, 0, 0
    for _ in range(n):
        u, x = np.exp(2j * np.pi * rng.random(2))
        v = rng.permutation(np.concatenate([u * W3 ** np.arange(3), x * W3 ** np.arange(3)]))
        assert abs(v.sum()) < 1e-12 and abs((v ** 2).sum()) < 1e-12
        for a, _ in admissible_ab(v):
            worst_c = max(worst_c, abs(sum(v[k] for k in range(6) if abs(v[k] ** 3 - a) < TOL)))
    for _ in range(n // 4):
        th = 2 * np.pi * rng.random(6)
        for _ in range(200):  # Gauss-Newton on 4 real equations, 6 unknowns (min-norm step)
            v = np.exp(1j * th)
            r = np.array([v.sum().real, v.sum().imag, (v ** 2).sum().real, (v ** 2).sum().imag])
            if r @ r < 1e-28:
                break
            J = np.array([(1j * v).real, (1j * v).imag, (2j * v ** 2).real, (2j * v ** 2).imag])
            th = th - np.linalg.pinv(J) @ r
        v = np.exp(1j * th)
        if abs(v.sum()) < 1e-12 and abs((v ** 2).sum()) < 1e-12:
            found += 1
            cl = cube_classes(v)
            two_valued += len(cl) <= 2
            for a, _ in admissible_ab(v):
                worst_s = max(worst_s, abs(sum(v[k] for k in range(6) if abs(v[k] ** 3 - a) < TOL)))
    return worst_c, worst_s, found, two_valued


# ---------------------------------------------------------------- report
def report(name, H):
    hh, hs = hadamard_res(H), hadamard_res(square(H))
    q, n_inst, n_nt, n_nohab = theorem_quantity(H)
    hyp = hh < TOL and hs < TOL
    print(f"  {name:38s} Hadamard res {hh:8.1e}  square res {hs:8.1e}  "
          f"{'HYPOTHESES HOLD' if hyp else 'hs FAILS      ' if hh < TOL else 'hH FAILS      '}  "
          f"max|Q| {q:8.2e}  instances {n_inst:3d}  two-valued pairs {n_nt:2d}  pairs w/o hab {n_nohab:2d}")
    return hh, hs, q, hyp


def main():
    print("== 1. Known Hadamard families (hypothesis hH and hs checked separately)")
    report("F6", fourier6())
    fam = {
        "F6^(2)(a,b) affine": lambda: fourier_affine(*(2 * np.pi * rng.random(2))),
        "Dita product [[F3,F3D],[F3,-F3D]]": lambda: dita_product(*(2 * np.pi * rng.random(2))),
        "Dita D6(c)": lambda: dita_D6(2 * np.pi * rng.random()),
        "random equivalent of F6": lambda: random_equivalent(fourier6()),
    }
    for name, mk in fam.items():
        hh_max, hs_min = 0.0, np.inf
        qmax, any_hyp = 0.0, False
        for _ in range(200):
            H = mk()
            hh, hs, q = hadamard_res(H), hadamard_res(square(H)), theorem_quantity(H)[0]
            hh_max, hs_min, qmax = max(hh_max, hh), min(hs_min, hs), max(qmax, q)
            any_hyp |= hh < TOL and hs < TOL
        print(f"  {name:38s} 200 random params: max Hadamard res {hh_max:8.1e}  MIN square res {hs_min:6.3f}  "
              f"hs ever holds: {any_hyp}  (max|Q| where hab held, hypotheses NOT all met: {qmax:.3f})")

    print("\n== 2. Tao's cubic matrix (the Lean taoMatrix) and random members of its equivalence class")
    report("taoMatrix (Lean exponents)", tao_lean())
    worst = (0.0, 0.0, 0.0)
    nt_total = 0
    for _ in range(500):
        H = random_equivalent(tao_lean())
        hh, hs = hadamard_res(H), hadamard_res(square(H))
        q, _, nt, _ = theorem_quantity(H)
        nt_total += nt
        worst = (max(worst[0], hh), max(worst[1], hs), max(worst[2], q))
    print(f"  500 random equivalents: max Hadamard res {worst[0]:.1e}  max square res {worst[1]:.1e}  "
          f"max|Q| {worst[2]:.1e}  pairs with TWO distinct cube values: {nt_total}")

    print("\n== 3. Unbiased search for H with H and H^2 both Hadamard (LM from random phases)")
    conv, cube_ok, qmax, nt_total, worst_res = 0, 0, 0.0, 0, 0.0
    for _ in range(300):
        H, res = lm_search(2 * np.pi * rng.random((6, 6)))
        if res < 1e-10 and hadamard_res(H) < 1e-9 and hadamard_res(square(H)) < 1e-9:
            conv += 1
            worst_res = max(worst_res, hadamard_res(H), hadamard_res(square(H)))
            cube_ok += is_cube_root_matrix(dephase(H)) < 1e-7
            q, _, nt, _ = theorem_quantity(H)
            qmax, nt_total = max(qmax, q), nt_total + nt
    print(f"  300 starts: {conv} converged (worst residual {worst_res:.1e}); dephased entries all cube roots "
          f"of unity in {cube_ok}/{conv}; max|Q| {qmax:.1e}; pairs with TWO distinct cube values: {nt_total}")

    print("\n== 4. Vector-level lemma ratio_cubeFiber_sum_zero (where the a != b, both-fibres-nonempty case lives)")
    wc, ws, found, tv = vector_lemma_trials()
    print(f"  constructed two-triple vectors: max|fibre sum| {wc:.1e}")
    print(f"  LM-found v with sum v = sum v^2 = 0: {found} found, cubes two-valued in {tv}/{found}, "
          f"max|fibre sum| {ws:.1e}")

    print("\n== 5. Negative controls (the instrument must be able to report non-zero)")
    F = fourier6()
    v = row_ratio(F, 0, 3)
    print(f"  F6 rows (0,3): Hadamard res {hadamard_res(F):.1e}, square res {hadamard_res(square(F)):.1f} (hs fails); "
          f"cube values {np.round(cube_classes(v), 6)}; sum v^2 = {abs((v**2).sum()):.1f}; "
          f"Q(a=1) = {fiber_sum(F, 0, 3, 1.0):.6f}, Q(a=-1) = {fiber_sum(F, 0, 3, -1.0):.6f}")
    v = row_ratio(F, 0, 1)
    print(f"  F6 rows (0,1) for contrast (hs fails globally, but this pair has sum v^2 = {abs((v**2).sum()):.1e}): "
          f"Q(a=1) = {abs(fiber_sum(F, 0, 1, 1.0)):.1e}")
    J = np.ones((6, 6), complex)
    print(f"  all-ones (unimodular, NOT Hadamard, res {hadamard_res(J):.0f}): Q(i=0,j=1,a=1) = {fiber_sum(J, 0, 1, 1.0):.1f}")
    P = tao_lean() * np.exp(1j * 0.05 * rng.standard_normal((6, 6)))
    q, n_inst, nt, nohab = theorem_quantity(P)
    print(f"  Tao with 0.05-rad phase noise: Hadamard res {hadamard_res(P):.2f}; pairs where hab is "
          f"unsatisfiable {nohab}/30 (so the theorem is silent there)")
    # vector-level: drop sum v^2 = 0, keep sum v = 0 and two-valued cubes
    v = np.array([1, 1, 1, -1, -1, -1], complex)
    print(f"  vector (1,1,1,-1,-1,-1): sum v = {abs(v.sum()):.0f}, sum v^2 = {abs((v**2).sum()):.0f}, "
          f"fibre(a=1) sum = {abs(v[:3].sum()):.0f}")


if __name__ == "__main__":
    main()
