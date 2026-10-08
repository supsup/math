"""Replicate OAI.Problem160.properColoring_seven (lean/ComparatorChallenges/PlaneColoring.lean).

Statement: there is c : Plane -> Fin 7 with dist x y = 1 -> c x != c y (distance EXACTLY 1).

What the Lean solution builds (lean/OAI/Geometry/PlaneColoring/{Seven,Metric,Lattice,Covering,Assembly}.lean):
  centers  triangularLattice a b = (4/5) * (a + b/2, (sqrt3/2) * b)      (a, b integers; spacing 4/5)
  colours  colorFin a b         = (a + 3b) mod 7
  cell(x)  = SOME (a, b) with dist(x, center(a, b)) <= r = 7/15, picked by `choose` (Classical.choice).
The proof does NOT fix which admissible centre a point gets; it proves EVERY such choice is proper.
So the strongest replication tests the admissible colour SETS: for |x - y| = 1, no colour may be
admissible at both x and y. That covers every possible selector at once, including Lean's opaque one.

We also run concrete selectors: the floor-based witness from the PROOF of triangular_lattice_cover
(which turns out to be the hexagonal Voronoi tiling with a specific tie-break), nearest-centre, and an
adversarial selector that tries to give y the same colour as x.

Run: python3 replicate.py   (needs numpy from the user site, so not -I; ~10-60 s)
"""
from fractions import Fraction as F
import math
import sys

import numpy as np

S3 = math.sqrt(3.0)
R = 7.0 / 15.0
SEED = 20261008
rng = np.random.default_rng(SEED)


# ---------------------------------------------------------------- the colouring family
class Scheme:
    """A lattice colouring: spacing d, colour rule (a,b) -> int mod k, admissible radius r."""

    def __init__(self, name, d, rule, k, r):
        self.name, self.d, self.rule, self.k, self.r = name, d, rule, k, r

    def center(self, a, b):
        return self.d * (a + b / 2.0), self.d * (S3 / 2.0) * b

    def candidates(self, x, y):
        """Lattice coords near (x,y): a 5x5 block around the rounded inverse. Arrays (N,25)."""
        b0 = np.round(y / (self.d * S3 / 2.0))
        a0 = np.round(x / self.d - b0 / 2.0)
        off = np.arange(-2, 3)
        da, db = np.meshgrid(off, off, indexing="ij")
        a = a0[:, None] + da.ravel()[None, :]
        b = b0[:, None] + db.ravel()[None, :]
        cx, cy = self.center(a, b)
        dist = np.hypot(x[:, None] - cx, y[:, None] - cy)
        return a.astype(np.int64), b.astype(np.int64), dist

    def admissible_mask(self, x, y):
        """Bitmask of colours whose centre lies within r of the point (Lean's admissible set)."""
        a, b, dist = self.candidates(x, y)
        col = self.rule(a, b) % self.k
        ok = dist <= self.r
        assert ok.any(axis=1).all(), f"{self.name}: some point has NO centre within r (cover fails)"
        return np.bitwise_or.reduce(np.where(ok, 1 << col, 0), axis=1), ok.sum(axis=1)

    def nearest(self, x, y):
        a, b, dist = self.candidates(x, y)
        i = np.argmin(dist, axis=1)
        idx = np.arange(len(x))
        return self.rule(a[idx, i], b[idx, i]) % self.k, dist[idx, i]


LEAN = Scheme("lean (d=4/5, a+3b mod 7, r=7/15)", 0.8, lambda a, b: a + 3 * b, 7, R)


def lean_floor_witness(px, py):
    """The witness in the PROOF of Covering.triangular_lattice_cover, on the scaled point (5/4)x.

    Seven.lean feeds hcover ((5/4) x0) ((5/4) x1). Returns (m, n). Boundary ties follow the proof's
    `<=` comparisons and floors. NB: properColoring_seven goes through `choose` on an existential, so
    Lean's actual colouring is NOT pinned to this witness; this is one valid selector."""
    x, y = 1.25 * px, 1.25 * py
    n = math.floor(2 * y / S3)
    m = math.floor(x - n / 2)
    u = x - (m + n / 2)
    v = y - S3 * n / 2
    if u <= 0.5:
        if S3 * v <= 1 - u:
            return m, n
        return m, n + 1
    if S3 * v <= u:
        return m + 1, n
    return m, n + 1


# ---------------------------------------------------------------- exact side conditions
def exact_conditions():
    """The three numeric hypotheses of exists_unit_distance_coloring_of_center_cover, in exact
    arithmetic, plus the lattice lemma (a+3b = 0 mod 7, (a,b) != 0  =>  a^2+ab+b^2 >= 7)."""
    out = {}
    # cover: normalized squared radius 1/3 scales by (4/5)^2 -> 16/75 <= (7/15)^2 = 49/225
    out["cover 16/75 <= (7/15)^2"] = F(16, 75) <= F(7, 15) ** 2
    out["hdiam 2r < 1"] = 2 * F(7, 15) < 1
    # hsep via normSq >= 7: (4/5)^2 * 7 > (1 + 2r)^2, i.e. dist > 2 > 1 + 2r
    out["sep (16/25)*7 > (1+2r)^2"] = F(16, 25) * 7 > (1 + 2 * F(7, 15)) ** 2
    out["Lean's route: (1+2r) < 2 and 4 < (16/25)*7"] = (1 + 2 * F(7, 15) < 2) and (4 < F(16, 25) * 7)
    minimum = min(a * a + a * b + b * b for a in range(-30, 31) for b in range(-30, 31)
                  if (a, b) != (0, 0) and (a + 3 * b) % 7 == 0)
    out[f"min normSq over same-colour offsets |a|,|b|<=30 = {minimum} (>= 7)"] = minimum >= 7
    # 1/3 is TIGHT: the Voronoi vertex (1/2, 1/(2 sqrt3)) is at squared distance 1/4 + 1/12 from all of
    # (0,0), (1,0), (1/2, sqrt3/2); the last one: (0)^2 + (sqrt3/2 - 1/(2sqrt3))^2 = (1/sqrt3)^2 = 1/3.
    out["normalized cover bound 1/3 is attained (Voronoi vertex: 1/4 + 1/12 == 1/3)"] = F(1, 4) + F(1, 12) == F(1, 3)
    return out


# ---------------------------------------------------------------- pair tests
def unit_pairs(n, box=50.0):
    px = rng.uniform(-box, box, n)
    py = rng.uniform(-box, box, n)
    t = rng.uniform(0, 2 * math.pi, n)
    return px, py, px + np.cos(t), py + np.sin(t)


def count_admissible_conflicts(s, px, py, qx, qy):
    mp, cp = s.admissible_mask(px, py)
    mq, cq = s.admissible_mask(qx, qy)
    bad = (mp & mq) != 0
    return bad, cp, cq


def count_nearest_conflicts(s, px, py, qx, qy):
    cp, _ = s.nearest(px, py)
    cq, _ = s.nearest(qx, qy)
    return cp == cq


def boundary_points(n):
    """Points within 1e-9 of hexagon edges/vertices and of the r=7/15 circles, in real coordinates."""
    d = 0.8
    a = rng.integers(-40, 40, n)
    b = rng.integers(-40, 40, n)
    cx, cy = LEAN.center(a, b)
    kind = rng.integers(0, 3, n)
    ang_v = (np.pi / 6) + (np.pi / 3) * rng.integers(0, 6, n)        # Voronoi vertex directions
    ang_e = (np.pi / 3) * rng.integers(0, 6, n)                        # edge midpoint directions
    t = rng.uniform(0, 2 * np.pi, n)
    jitter = rng.uniform(-1e-9, 1e-9, n)
    rad = np.where(kind == 0, d / S3, np.where(kind == 1, d / 2, R)) + jitter
    ang = np.where(kind == 0, ang_v, np.where(kind == 1, ang_e, t))
    # kind 1 also slides along the edge
    slide = np.where(kind == 1, rng.uniform(-1, 1, n) * d / (2 * S3), 0.0)
    px = cx + rad * np.cos(ang) - slide * np.sin(ang)
    py = cy + rad * np.sin(ang) + slide * np.cos(ang)
    return px, py, kind


def boundary_pairs(n):
    """Both ends on boundaries: p on a boundary; direction chosen so q also lands near a vertex
    (aim at a random nearby Voronoi vertex, rescaled to length 1), plus random directions."""
    px, py, _ = boundary_points(n)
    vx, vy, _ = boundary_points(n)
    half = n // 2
    t = rng.uniform(0, 2 * math.pi, n)
    ux, uy = np.cos(t), np.sin(t)
    dx, dy = vx - px, vy - py
    nn = np.hypot(dx, dy)
    nn[nn == 0] = 1.0
    ux[:half], uy[:half] = (dx / nn)[:half], (dy / nn)[:half]
    # exact lattice directions too (0, 30, 60, ... degrees), where edges are parallel to u
    k = rng.integers(0, 12, n)
    lat = np.arange(n) % 4 == 0
    ux[lat], uy[lat] = np.cos(k[lat] * np.pi / 6), np.sin(k[lat] * np.pi / 6)
    return px, py, px + ux, py + uy


def floor_witness_checks(n):
    px = rng.uniform(-50, 50, n)
    py = rng.uniform(-50, 50, n)
    bx, by, _ = boundary_points(n)
    px = np.concatenate([px, bx])
    py = np.concatenate([py, by])
    worst = 0.0
    disagree_nearest_far = 0
    ncol, ndist = LEAN.nearest(px, py)
    for i in range(len(px)):
        m, k = lean_floor_witness(px[i], py[i])
        cx, cy = LEAN.center(m, k)
        dd = math.hypot(px[i] - cx, py[i] - cy)
        worst = max(worst, dd)
        if abs(dd - ndist[i]) > 1e-9:
            disagree_nearest_far += 1
    return len(px), worst, disagree_nearest_far


def hexagon_scale_window():
    """For the hexagonal (nearest-centre) tiling with a+3b mod 7, find the spacings d that work:
    hexagon diameter 2d/sqrt3 < 1 and min distance between same-coloured hexagons > 1.
    Closed form: same-colour centres are d*sqrt7 apart along a direction; the gap between two
    regular hexagons of circumradius d/sqrt3 there is computed numerically below."""
    def hexagon(cx, cy, d):
        rr = d / S3
        return [(cx + rr * math.cos(math.pi / 6 + j * math.pi / 3),
                 cy + rr * math.sin(math.pi / 6 + j * math.pi / 3)) for j in range(6)]

    def seg_dist(p, q, a, b):
        def pt_seg(p, a, b):
            ax, ay = a; bx, by = b; px, py = p
            vx, vy = bx - ax, by - ay
            t = max(0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / (vx * vx + vy * vy)))
            return math.hypot(px - ax - t * vx, py - ay - t * vy)
        return min(pt_seg(p, a, b), pt_seg(q, a, b), pt_seg(a, p, q), pt_seg(b, p, q))

    def poly_dist(P, Q):
        return min(seg_dist(P[i], P[(i + 1) % 6], Q[j], Q[(j + 1) % 6]) for i in range(6) for j in range(6))

    H0 = hexagon(0, 0, 1.0)
    gaps = []
    for a in range(-4, 5):
        for b in range(-4, 5):
            if (a, b) != (0, 0) and (a + 3 * b) % 7 == 0:
                cx, cy = (a + b / 2.0), (S3 / 2.0) * b
                gaps.append(poly_dist(H0, hexagon(cx, cy, 1.0)))
    g = min(gaps)  # for spacing 1; scales linearly
    return 1.0 / g, S3 / 2.0, g


# ---------------------------------------------------------------- negative controls
CONTROLS = [
    Scheme("CONTROL spacing 1.0 (hexagon diameter 1.155 > 1)", 1.0, lambda a, b: a + 3 * b, 7, 0.0),
    Scheme("CONTROL spacing 0.6 (same-colour hexagons too close)", 0.6, lambda a, b: a + 3 * b, 7, 0.0),
    Scheme("CONTROL wrong rule a+b mod 7 (neighbours share colours)", 0.8, lambda a, b: a + b, 7, 0.0),
    Scheme("CONTROL 6 colours a+3b mod 6", 0.8, lambda a, b: a + 3 * b, 6, 0.0),
]


def show_violation(s, px, py, qx, qy, bad):
    i = int(np.flatnonzero(bad)[0])
    cp, dp = s.nearest(px[i:i + 1], py[i:i + 1])
    cq, dq = s.nearest(qx[i:i + 1], qy[i:i + 1])
    # margin: how far each endpoint is from being tied with its second-nearest centre
    def margin(x, y):
        _, _, dist = s.candidates(np.array([x]), np.array([y]))
        srt = np.sort(dist[0])
        return srt[1] - srt[0]
    return (f"p=({px[i]:.12f}, {py[i]:.12f}) q=({qx[i]:.12f}, {qy[i]:.12f}) |p-q|={math.hypot(qx[i]-px[i], qy[i]-py[i]):.15f} "
            f"colour {int(cp[0])} == {int(cq[0])}; tie margins {margin(px[i], py[i]):.3e}, {margin(qx[i], qy[i]):.3e}")


def main():
    ok = True
    print("== exact side conditions (fractions / integers)")
    for k, v in exact_conditions().items():
        print(f"  {'OK ' if v else 'BAD'} {k}")
        ok &= v

    N = 1_000_000
    print(f"\n== (a) dense random test, {N:,} pairs, box [-50,50]^2, seed {SEED}")
    total_bad_adm = total_bad_near = 0
    multi = 0
    for _ in range(4):
        px, py, qx, qy = unit_pairs(N // 4)
        bad, cp, cq = count_admissible_conflicts(LEAN, px, py, qx, qy)
        total_bad_adm += int(bad.sum())
        multi += int((cp > 1).sum() + (cq > 1).sum())
        total_bad_near += int(count_nearest_conflicts(LEAN, px, py, qx, qy).sum())
    print(f"  admissible-set conflicts (ANY choice of cell): {total_bad_adm}")
    print(f"  nearest-centre (hexagon) conflicts:            {total_bad_near}")
    print(f"  endpoints with >1 admissible centre (overlap zones of the r=7/15 disks): {multi:,} of {2*N:,}")
    ok &= total_bad_adm == 0 and total_bad_near == 0

    NB = 400_000
    print(f"\n== (b) boundary-targeted test, {NB:,} pairs (endpoints within 1e-9 of hexagon edges/vertices or r-circles)")
    px, py, qx, qy = boundary_pairs(NB)
    bad, cp, cq = count_admissible_conflicts(LEAN, px, py, qx, qy)
    near = count_nearest_conflicts(LEAN, px, py, qx, qy)
    print(f"  admissible-set conflicts: {int(bad.sum())}; nearest-centre conflicts: {int(near.sum())}")
    print(f"  endpoints with >1 admissible centre: {int((cp > 1).sum() + (cq > 1).sum()):,} of {2*NB:,}")
    ok &= int(bad.sum()) == 0 and int(near.sum()) == 0

    # adversarial selector: give q the colour of p whenever any admissible centre of q allows it
    mp, _ = LEAN.admissible_mask(px, py)
    mq, _ = LEAN.admissible_mask(qx, qy)
    print(f"  adversarial selector (match q's colour to any of p's): {int(((mp & mq) != 0).sum())} successes")

    nf = 100_000
    cnt, worst, disagree = floor_witness_checks(nf)
    print(f"\n== Lean floor-witness selector (proof of triangular_lattice_cover) on {cnt:,} points")
    print(f"  max distance to chosen centre {worst:.15f}; bound 7/15 = {R:.15f}; hexagon circumradius 0.8/sqrt3 = {0.8/S3:.15f}")
    print(f"  points where the witness is NOT a nearest centre (beyond 1e-9): {disagree}")
    ok &= worst <= R and disagree == 0
    px, py, qx, qy = unit_pairs(200_000)
    cols_p = np.array([int(LEAN.rule(*lean_floor_witness(a, b)) % 7) for a, b in zip(px, py)])
    cols_q = np.array([int(LEAN.rule(*lean_floor_witness(a, b)) % 7) for a, b in zip(qx, qy)])
    print(f"  floor-witness colouring conflicts on 200,000 random unit pairs: {int((cols_p == cols_q).sum())}")
    ok &= int((cols_p == cols_q).sum()) == 0

    lo, hi, g = hexagon_scale_window()
    print(f"\n== hexagon scale window for a+3b mod 7 (nearest-centre cells)")
    print(f"  min gap between same-colour hexagons at spacing 1: {g:.6f}")
    print(f"  tiling is proper for spacing d in ({lo:.6f}, {hi:.6f}); Lean uses d = 0.8"
          f" -> {'inside' if lo < 0.8 < hi else 'OUTSIDE'}")
    print(f"  Lean's disk argument (r=7/15) needs only d*sqrt7 > 1+2r: d > {(1 + 2*R)/math.sqrt(7):.6f},"
          f" and cover d/sqrt3 <= 7/15: d <= {7/15*S3:.6f}")

    print("\n== (c) negative controls (nearest-centre colouring, must be CAUGHT)")
    for s in CONTROLS:
        px, py, qx, qy = unit_pairs(200_000)
        bad = count_nearest_conflicts(s, px, py, qx, qy)
        n_bad = int(bad.sum())
        print(f"  {s.name}: {n_bad:,} violating pairs of 200,000")
        if n_bad == 0:
            ok = False
            print("    CONTROL FAILED TO FIRE")
        else:
            print(f"    e.g. {show_violation(s, px, py, qx, qy, bad)}")

    print("\n== (c') negative controls on the ADMISSIBLE-SET instrument (must be CAUGHT)")
    for s in [Scheme("CONTROL r = 0.55 (2r > 1: a cell can contain a unit pair)", 0.8, lambda a, b: a + 3 * b, 7, 0.55),
              Scheme("CONTROL r = 7/15 but rule a+b mod 7", 0.8, lambda a, b: a + b, 7, R)]:
        px, py, qx, qy = unit_pairs(200_000)
        bad, _, _ = count_admissible_conflicts(s, px, py, qx, qy)
        n_bad = int(bad.sum())
        print(f"  {s.name}: {n_bad:,} pairs with a shared admissible colour of 200,000")
        if n_bad == 0:
            ok = False
            print("    CONTROL FAILED TO FIRE")
        else:
            i = int(np.flatnonzero(bad)[0])
            print(f"    e.g. p=({px[i]:.12f}, {py[i]:.12f}) q=({qx[i]:.12f}, {qy[i]:.12f})")

    print("\nRESULT:", "ALL CHECKS PASSED, ALL CONTROLS FIRED" if ok else "SOMETHING FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
