"""Newton flow rivers: the continuous Newton flow of p(z) = z^3 - 1, drawn as rivers draining to its roots.

The flow is dz/dt = -p(z)/p'(z). Along it dp/dt = p'(z) dz/dt = -p, so p(z(t)) = p(z0) e^-t: every
trajectory keeps arg p fixed and slides down |p| to a root. Seeds sit on a jittered grid in
|Re z|, |Im z| <= 2; each is integrated with RK4 (step clamped in arc length, which only re-times the
same curve) until it is within TOL of a root or hits the step cap. Trajectories are coloured by the root
they reach, simplified with Douglas-Peucker, and drawn thicker and brighter where many pass through the
same part of a binned plane (log count, interpolated between bins, taken as a running max downstream).

Behind them, faintly: the basin boundaries of the DISCRETE Newton map z -> z - p/p', from sampling which
root each grid point reaches and tracing marching-squares contours between the labels.

The script also checks its own claims: every seed's root is compared with the sector rule (the flow's
separatrices are the rays arg z = 60, 180, 300 degrees, where p is real and below -1, flowing into the
critical point 0); the drift of arg p along each trajectory is measured; and the discrete boundary length
is measured at three grid resolutions (a smooth curve's length converges, a fractal one's keeps growing).

Deterministic, standard library only: python3 -I newton_flow.py  ->  newton_flow.svg
"""
import cmath
import math
import pathlib
import random

W, H = 480, 600
BG, INK, DIM = "#0d1b2a", "#e8eef2", "#7d92a6"
COL = ["#f4d58d", "#6ec4e2", "#e58fb0"]           # root 1, omega, omega^2
ROOTS = [cmath.exp(2j * math.pi * k / 3) for k in range(3)]
R = 2.0                                            # window half-width
BOX_X, BOX_Y, BOX = 18, 56, 444                    # art square in px
SEEDS = 30                                         # SEEDS x SEEDS jittered grid
TOL, CAP = 1e-3, 20000
DT, DS = 0.05, 0.012                               # time step, max arc length per step
CELL = 5.0                                         # px, flow-count bins
LEVELS = 10
DP_TOL = 0.35                                      # px, simplification tolerance
NEWTON_GRID = 200                                  # discrete basin sampling (per side)


def f(z):
    return -(z * z * z - 1) / (3 * z * z)


def px(z):
    return BOX_X + (z.real + R) / (2 * R) * BOX, BOX_Y + (R - z.imag) / (2 * R) * BOX


def near_root(z):
    for k, r in enumerate(ROOTS):
        if abs(z - r) < TOL:
            return k
    return None


def integrate(z):
    pts = [z]
    for _ in range(CAP):
        k = near_root(z)
        if k is not None:
            return k, pts
        if z == 0:
            return None, pts
        s = abs(f(z))
        h = min(DT, DS / s) if s > 0 else DT
        try:
            k1 = f(z)
            k2 = f(z + h / 2 * k1)
            k3 = f(z + h / 2 * k2)
            k4 = f(z + h * k3)
        except ZeroDivisionError:
            return None, pts
        z = z + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        pts.append(z)
    return None, pts


def sector_root(z):
    a = math.degrees(cmath.phase(z))
    if -60 < a < 60:
        return 0
    return 1 if 60 < a < 180 else 2


def newton_label(z):
    for _ in range(80):
        if z == 0:
            return 3
        z = z - (z * z * z - 1) / (3 * z * z)
        for k, r in enumerate(ROOTS):
            if abs(z - r) < 1e-6:
                return k
    return 3


def marching(n, label=newton_label):
    """Basin boundary segments (in z coordinates) of `label` sampled on an n x n grid."""
    step = 2 * R / n
    xs = [-R + (i + 0.5) * step for i in range(n)]
    lab = [[label(complex(x, y)) for x in xs] for y in xs]   # lab[j][i]: y index j
    segs = set()
    for j in range(n - 1):
        for i in range(n - 1):
            c = (lab[j][i], lab[j][i + 1], lab[j + 1][i + 1], lab[j + 1][i])
            if c[0] == c[1] == c[2] == c[3]:
                continue
            x0, y0 = xs[i], xs[j]
            corner = [(x0, y0), (x0 + step, y0), (x0 + step, y0 + step), (x0, y0 + step)]
            mids = [((corner[e][0] + corner[(e + 1) % 4][0]) / 2, (corner[e][1] + corner[(e + 1) % 4][1]) / 2)
                    for e in range(4)]
            for L in set(c):
                inside = [v == L for v in c]
                cut = [e for e in range(4) if inside[e] != inside[(e + 1) % 4]]
                if len(cut) == 2:
                    pairs = [cut]
                elif len(cut) == 4:                      # saddle: keep L's corners separated
                    pairs = [[3, 0], [1, 2]] if inside[0] else [[0, 1], [2, 3]]
                else:
                    continue
                for a, b in pairs:
                    p, q = mids[a], mids[b]
                    key = (min(p, q), max(p, q))
                    segs.add((round(key[0][0], 9), round(key[0][1], 9), round(key[1][0], 9), round(key[1][1], 9)))
    return segs, lab


def chain(segs):
    """Join segments sharing endpoints into polylines."""
    adj = {}
    for s in segs:
        a, b = (s[0], s[1]), (s[2], s[3])
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    used, lines = set(), []
    starts = [v for v in adj if len(adj[v]) != 2] + list(adj)
    for v0 in starts:
        for v1 in adj[v0]:
            if (v0, v1) in used:
                continue
            line = [v0, v1]
            used.add((v0, v1)); used.add((v1, v0))
            while True:
                cur = line[-1]
                nxt = [w for w in adj[cur] if (cur, w) not in used]
                if len(adj[cur]) != 2 or not nxt:
                    break
                w = nxt[0]
                used.add((cur, w)); used.add((w, cur))
                line.append(w)
            lines.append(line)
    return lines


def dp(points, tol):
    if len(points) < 3:
        return points
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        a, b = stack.pop()
        (ax, ay), (bx, by) = points[a], points[b]
        dx, dy = bx - ax, by - ay
        norm = math.hypot(dx, dy)
        best, bi = 0.0, -1
        for i in range(a + 1, b):
            x, y = points[i]
            d = abs(dy * (x - ax) - dx * (y - ay)) / norm if norm > 0 else math.hypot(x - ax, y - ay)
            if d > best:
                best, bi = d, i
        if best > tol:
            keep[bi] = True
            stack.append((a, bi)); stack.append((bi, b))
    return [p for p, k in zip(points, keep) if k]


def num(v):
    t = f"{v:.1f}"
    if t.endswith(".0"):
        t = t[:-2]
    if t == "-0":
        t = "0"
    if t.startswith("0."):
        t = t[1:]
    elif t.startswith("-0."):
        t = "-" + t[2:]
    return t


def path_d(pts):
    """Absolute moveto, then relative lineto deltas computed on the rounded grid (no drift)."""
    q = [(round(x * 10), round(y * 10)) for x, y in pts]
    out = [f"M{num(q[0][0] / 10)} {num(q[0][1] / 10)}l"]
    prev = q[0]
    for a, b in q[1:]:
        dx, dy = (a - prev[0]) / 10, (b - prev[1]) / 10
        if dx == 0 and dy == 0:
            continue
        sx, sy = num(dx), num(dy)
        out.append(("" if len(out) == 1 or sx.startswith("-") else " ") + sx + ("" if sy.startswith("-") else " ") + sy)
        prev = (a, b)
    if len(out) == 1:
        return ""
    return "".join(out)


def main():
    rng = random.Random(20261008)
    g = 2 * R / SEEDS
    seeds = [complex(-R + (i + rng.random()) * g, -R + (j + rng.random()) * g)
             for j in range(SEEDS) for i in range(SEEDS)]

    runs, counts, sector_mismatch, max_drift, max_out, steps_max = [], [0, 0, 0], 0, 0.0, 0.0, 0
    unresolved = 0
    for z0 in seeds:
        k, pts = integrate(z0)
        steps_max = max(steps_max, len(pts) - 1)
        if k is None:
            unresolved += 1
            continue
        counts[k] += 1
        if k != sector_root(z0):
            sector_mismatch += 1
        a0 = cmath.phase(z0 ** 3 - 1)
        for z in pts[:-1]:
            if abs(z ** 3 - 1) > 1e-2:
                d = abs((cmath.phase(z ** 3 - 1) - a0 + math.pi) % (2 * math.pi) - math.pi)
                max_drift = max(max_drift, d)
            max_out = max(max_out, abs(z.real) - R, abs(z.imag) - R)
        runs.append((k, [px(z) for z in pts]))
    n_seeds = len(seeds)
    exact1 = 0.5 - 1 / (4 * math.sqrt(3))                 # area share of the sector |arg z| < 60 in the square
    exact = [exact1, (1 - exact1) / 2, (1 - exact1) / 2]

    # flow count: distinct trajectories through each CELL x CELL bin
    nb = int(BOX / CELL) + 2
    grid = {}
    cell_sets = []
    for k, pts in runs:
        cells = set()
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            m = max(1, int(math.hypot(x2 - x1, y2 - y1) / (CELL / 2)) + 1)
            for t in range(m + 1):
                x, y = x1 + (x2 - x1) * t / m, y1 + (y2 - y1) * t / m
                cells.add((int((x - BOX_X) // CELL), int((y - BOX_Y) // CELL)))
        for c in cells:
            grid[c] = grid.get(c, 0) + 1
        cell_sets.append(cells)
    top = math.log(max(grid.values()))

    def level(x, y):
        # bilinear interpolation of log(count) between cell centres, so width changes fall on smooth
        # contours of the flow field rather than on the cell grid
        u, v = (x - BOX_X) / CELL - 0.5, (y - BOX_Y) / CELL - 0.5
        i, j = math.floor(u), math.floor(v)
        fu, fv = u - i, v - j
        val = 0.0
        for di, dj, wgt in ((0, 0, (1 - fu) * (1 - fv)), (1, 0, fu * (1 - fv)), (0, 1, (1 - fu) * fv), (1, 1, fu * fv)):
            val += wgt * math.log(max(1, grid.get((i + di, j + dj), 0)))
        return min(LEVELS - 1, int(val / top * LEVELS))

    buckets = {}
    for k, pts in runs:
        cur, run, hi = None, [], 0
        for p in pts:
            hi = max(hi, level(*p))      # a river only widens downstream: running max of the flow level
            lv = hi
            if lv != cur and run:
                run.append(p)
                buckets.setdefault((k, cur), []).append(dp(run, DP_TOL))
                run = []
            cur = lv
            run.append(p)
        if len(run) > 1:
            buckets.setdefault((k, cur), []).append(dp(run, DP_TOL))

    # discrete Newton basin boundaries, plus their length at three resolutions
    segs, lab = marching(NEWTON_GRID)
    lengths = {}
    for n in (NEWTON_GRID // 2, NEWTON_GRID, NEWTON_GRID * 2):
        s = segs if n == NEWTON_GRID else marching(n)[0]
        lengths[n] = sum(math.hypot(a - c, b - d) for a, b, c, d in s)
    flow_boundary = R / math.sin(math.radians(60)) * 2 + R
    # control: the same instrument on the flow's own (sector) labels must NOT grow with the grid
    control = {n: sum(math.hypot(a - c, b - d) for a, b, c, d in marching(n, sector_root)[0])
               for n in (NEWTON_GRID // 2, NEWTON_GRID, NEWTON_GRID * 2)}      # the three separatrix rays inside the square
    disc_counts = [sum(row.count(k) for row in lab) for k in range(4)]
    step = 2 * R / NEWTON_GRID
    cs = [-R + (i + 0.5) * step for i in range(NEWTON_GRID)]
    differ = sum(lab[j][i] != sector_root(complex(cs[i], cs[j]))
                 for j in range(NEWTON_GRID) for i in range(NEWTON_GRID)) / NEWTON_GRID ** 2
    # how far do discrete boundary points stray from the flow's separatrix rays?
    rays = [cmath.exp(1j * math.radians(a)) for a in (60, 180, 300)]
    far = 0
    for a, b, c, d in segs:
        z = complex((a + c) / 2, (b + d) / 2)
        dist = min(abs((z * r.conjugate()).imag) if (z * r.conjugate()).real > 0 else abs(z) for r in rays)
        if dist > 0.25:
            far += 1

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect width="{W}" height="{H}" fill="{BG}"/>',
           f'<text x="240" y="38" text-anchor="middle" font-family="serif" font-size="23" fill="{INK}">'
           'Newton flow rivers</text>',
           f'<rect x="{BOX_X}" y="{BOX_Y}" width="{BOX}" height="{BOX}" fill="none" stroke="{DIM}" '
           'stroke-opacity="0.25" stroke-width="0.6"/>']
    lines = chain(segs)
    d = "".join(path_d(dp([px(complex(x, y)) for x, y in ln], 0.3)) for ln in lines)
    out.append(f'<path d="{d}" fill="none" stroke="{DIM}" stroke-opacity="0.55" stroke-width="0.5" '
               'stroke-linejoin="round"/>')
    for lv in range(LEVELS):
        t = (lv + 0.5) / LEVELS
        for k in range(3):
            polys = buckets.get((k, lv))
            if not polys:
                continue
            out.append(f'<path d="{"".join(path_d(p) for p in polys)}" fill="none" stroke="{COL[k]}" '
                       f'stroke-opacity="{0.22 + 0.6 * t:.2f}" stroke-width="{0.45 + 2.6 * t ** 2:.2f}" '
                       'stroke-linecap="butt" stroke-linejoin="round"/>')
    names = ["1", "ω", "ω²"]
    offs = [(10, 15), (-14, -8), (-14, 18)]
    for k, r in enumerate(ROOTS):
        x, y = px(r)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="{BG}" stroke="{COL[k]}" stroke-width="1.6"/>')
        out.append(f'<text x="{x + offs[k][0]:.1f}" y="{y + offs[k][1]:.1f}" font-family="serif" font-style="italic" '
                   f'font-size="15" text-anchor="middle" fill="{COL[k]}">{names[k]}</text>')
    zx, zy = px(0j)
    out.append(f'<circle cx="{zx:.1f}" cy="{zy:.1f}" r="1.8" fill="{INK}"/>')

    pct = [100 * c / n_seeds for c in counts]
    ex = [100 * e for e in exact]
    ln_ = [f"{lengths[n]:.1f}" for n in sorted(lengths)]
    cap = [
        (f"{n_seeds:,} seeds, dz/dt = −p/p′ for p = z³ − 1:  {pct[0]:.1f}% reach 1, {pct[1]:.1f}% ω, {pct[2]:.1f}% ω²", INK, 12),
        ("arg p is constant along every river, so the flow's basins are sectors cut by three", DIM, 10.5),
        (f"straight rays into 0 ({ex[0]:.1f} / {ex[1]:.1f} / {ex[2]:.1f}% of the square). Faint: discrete Newton", DIM, 10.5),
        (f"boundaries, {ln_[0]} → {ln_[1]} → {ln_[2]} long as the grid doubles: fractal, on and off the rays.", DIM, 10.5),
    ]
    y = 522
    for text, colour, size in cap:
        out.append(f'<text x="240" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" '
                   f'fill="{colour}">{text}</text>')
        y += 15
    out.append(f'<text x="240" y="592" text-anchor="middle" font-family="sans-serif" font-size="9.5" '
               f'fill="{DIM}">ideas after Confluence at 1 · Confluence</text>')
    out.append("</svg>")
    p = pathlib.Path(__file__).with_name("newton_flow.svg")
    p.write_text("".join(out), encoding="utf-8")
    print(p.name, p.stat().st_size, "bytes")
    print("seeds", n_seeds, "counts", counts, "unresolved", unresolved, "pct", [f"{v:.2f}" for v in pct],
          "exact", [f"{v:.2f}" for v in ex])
    print("sector-rule mismatches", sector_mismatch, "max arg-p drift (rad)", f"{max_drift:.2e}",
          "max excursion outside window", f"{max_out:.3f}", "max steps", steps_max)
    print("discrete boundary length by grid", {n: round(v, 3) for n, v in lengths.items()},
          "flow boundary", round(flow_boundary, 3),
          "control (sector labels, same instrument)", {n: round(v, 3) for n, v in control.items()})
    print("discrete labels counts (1, w, w2, none)", disc_counts, "boundary segs", len(segs),
          "segs farther than 0.25 from rays", far, f"({100 * far / len(segs):.1f}%)",
          "discrete-vs-flow label disagreement", f"{100 * differ:.2f}%", "max cell count", max(grid.values()))


if __name__ == "__main__":
    main()
