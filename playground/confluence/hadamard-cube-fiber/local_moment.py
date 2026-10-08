"""Marlow's suggestion (undervoice 15899): the cube-fibre lemma needs only a row-ratio vector v with
|v_k| = 1, sum v = 0 and sum v^2 = 0 (the LOCAL second moment), not H∘H Hadamard. Real Hadamard matrices
outside Tao's class have such row pairs, so the lemma's two-value case occurs on actual matrices.

For F6 and random equivalents of it (row/column permutations, diagonal unimodular phases), list every row
pair, classify it, and check the fibre sums. Negative control: pairs with sum v = 0 but sum v^2 != 0 and
two cube values (F6 rows at distance 3) must give a nonzero fibre sum.
Plain Python, no numpy: run with python3 -I local_moment.py
"""
import cmath, itertools, random

TOL = 1e-8
F6 = [[cmath.exp(2j * cmath.pi * i * k / 6) for k in range(6)] for i in range(6)]


def random_equivalent(H, rng):
    rows, cols = list(range(6)), list(range(6))
    rng.shuffle(rows); rng.shuffle(cols)
    dl = [cmath.exp(1j * rng.uniform(0, 2 * cmath.pi)) for _ in range(6)]
    dr = [cmath.exp(1j * rng.uniform(0, 2 * cmath.pi)) for _ in range(6)]
    return [[dl[i] * H[rows[i]][cols[k]] * dr[k] for k in range(6)] for i in range(6)]


def classify(H):
    out = {"local": [], "control": []}
    for i, j in itertools.permutations(range(6), 2):
        v = [H[i][k] * H[j][k].conjugate() for k in range(6)]
        cubes = []
        for z in v:
            if not any(abs(z ** 3 - c) < TOL for c in cubes):
                cubes.append(z ** 3)
        if len(cubes) != 2 or abs(sum(v)) > TOL:
            continue
        worst = max(abs(sum(z for z in v if abs(z ** 3 - a) < TOL)) for a in cubes)
        key = "local" if abs(sum(z * z for z in v)) < TOL else "control"
        out[key].append(((i, j), worst))
    return out


def main():
    rng = random.Random(20261008)
    mats = [("F6", F6)] + [("F6 equivalent %d" % n, random_equivalent(F6, rng)) for n in range(200)]
    n_local = n_ctrl = 0
    worst_local, min_ctrl = 0.0, float("inf")
    for name, H in mats:
        c = classify(H)
        n_local += len(c["local"]); n_ctrl += len(c["control"])
        worst_local = max([worst_local] + [w for _, w in c["local"]])
        min_ctrl = min([min_ctrl] + [w for _, w in c["control"]])
        if name == "F6":
            print("F6 two-valued pairs with local sum v^2 = 0:", [p for p, _ in c["local"]])
            print("F6 two-valued pairs with sum v^2 != 0 (control):", [p for p, _ in c["control"]])
    print("matrices: %d" % len(mats))
    print("lemma case (sum v = sum v^2 = 0, two cube values): %d pairs, max |fibre sum| %.1e" % (n_local, worst_local))
    print("control (sum v^2 != 0, two cube values): %d pairs, min max|fibre sum| %.3f" % (n_ctrl, min_ctrl))
    ok = n_local > 0 and worst_local < 1e-9 and n_ctrl > 0 and min_ctrl > 1
    print("RESULT:", "lemma holds on every local case, control fires" if ok else "UNEXPECTED")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
