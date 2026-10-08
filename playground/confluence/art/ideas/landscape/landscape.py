"""The stopping-time landscape: Collatz total stopping time s(n) drawn as a contour map.

s(n) = number of steps of n -> n/2 (even) or n -> 3n+1 (odd) needed to reach 1, for every n < 2^20.

THE MAP (landscape.svg). x = the residue class r = n mod 64; y = log2 n, from 2^14 (bottom) to 2^20
(top), 8 rows per octave. Each grid node is the mean of s over the n in one class and one 1/8-octave.
Columns are ordered by a(r) = the number of odd steps among the first 6 steps of the shortcut map
T(n) = n/2 or (3n+1)/2 (the parity pattern of those steps is fixed by n mod 64, Terras), ties broken
by bit-reversed r. Rows get a light 1-2-1 smoothing ALONG y only, twice; x is never smoothed, so no
two residue classes are ever mixed. Contours (marching squares, one <path> per level) every 5 steps.

WHY THIS LAYOUT. Every layout below is measured and printed. The plain grids n = x + W*y (W = 1024,
natural or bit-reversed columns) do show the 2-adic structure but as dense vertical stripes; an Ulam
spiral and a 2-adic square (low bits of n -> coarse position) are rough at every scale. Putting log2 n
on y turns the growth of s into level contours, and ordering the classes by a(r) turns the column
effect into terraces, one per value of a. The control (landscape_control.svg) is the same picture
with r = n mod 81 = 3^4 in natural order.

THE FACT, measured: least squares over all 2^14 <= n < 2^20 of s(n) on a(n mod 2^k) and log2 n.
Heuristic: k shortcut steps are k + a ordinary steps and take n to about n 3^a / 2^k, so if s(m) is
about c log2 m then s(n) ~ k + a + c (log2 n + a log2 3 - k): the slope in a should be 1 + c log2 3.
The script compares the fitted a-slope with that prediction from the fitted c.

HONESTY: everything is for n < 2^20 only; the fit is a summary of these numbers, not a theorem.

Deterministic, standard library only: python3 -I landscape.py -> landscape.svg, landscape_control.svg
"""
import math
import pathlib

K = 20
N = 1 << K                      # s(n) for 1 <= n < N
BG, INK, DIM, GOLD = "#0d1b2a", "#e8eef2", "#7d92a6", "#f4d58d"
HERE = pathlib.Path(__file__).parent
BX, BY, BW, BH = 40, 74, 418, 356       # plot box
KT, Y0, PER, STEP = 6, 14, 8, 5         # terrace modulus 2^KT, first octave, rows/octave, contour step


def stopping_times():
    s = [0] * N
    for n in range(2, N):
        m, k = n, 0
        while m >= n:                     # walk until we fall below n (already known)
            m = m // 2 if m % 2 == 0 else 3 * m + 1
            k += 1
        s[n] = k + s[m]
    return s


def bitrev(p, bits):
    r = 0
    for _ in range(bits):
        r = (r << 1) | (p & 1)
        p >>= 1
    return r


def odd_steps(r, k):
    a = 0
    for _ in range(k):
        if r % 2:
            r, a = (3 * r + 1) // 2, a + 1
        else:
            r //= 2
    return a


def eta2(s, key, lo=1):
    """Fraction of the variance of s(n), lo <= n < N, explained by the group key(n)."""
    tot, cnt = {}, {}
    sq = sm = 0
    for n in range(lo, N):
        g, v = key(n), s[n]
        tot[g] = tot.get(g, 0) + v
        cnt[g] = cnt.get(g, 0) + 1
        sm += v
        sq += v * v
    m = sm / (N - lo)
    sst = sq - (N - lo) * m * m
    return sum(cnt[g] * (tot[g] / cnt[g] - m) ** 2 for g in tot) / sst, len(tot)


def structure(cells, within, size):
    flat = [v for row in cells for v in row]
    m = sum(flat) / len(flat)
    var = sum((v - m) ** 2 for v in flat) / (len(flat) - 1)
    return var / (sum(within) / len(within) / size)


def column_structure(s, W, order, g=8):
    """Layout n = r + W*y (y >= 1), column p holds residue order[p]; g x g block means.
    Returns Var(block means) / (mean within-block variance / g^2): about 1 if cells were random."""
    rows = (N - 1) // W
    cells, within = [], []
    for i in range((rows - 1) // g):
        row = []
        for j in range(W // g):
            vals = [s[W * (1 + i * g + a) + order[j * g + b]] for a in range(g) for b in range(g)]
            m = sum(vals) / len(vals)
            row.append(m)
            within.append(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))
        cells.append(row)
    return structure(cells, within, g * g)


def spiral_structure(s, side=1000, g=8):
    grid = [[0] * side for _ in range(side)]
    x = y = side // 2 - 1
    n, step, d = 1, 1, 0
    dirs = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    grid[y][x] = 1
    while n < side * side:
        for _ in range(2):
            dx, dy = dirs[d % 4]
            for _ in range(step):
                if n >= side * side:
                    break
                x, y, n = x + dx, y + dy, n + 1
                if 0 <= x < side and 0 <= y < side:
                    grid[y][x] = n
            d += 1
        step += 1
    cells, within = [], []
    for i in range(side // g):
        row = []
        for j in range(side // g):
            vals = [s[grid[i * g + a][j * g + b]] for a in range(g) for b in range(g)]
            m = sum(vals) / len(vals)
            row.append(m)
            within.append(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))
        cells.append(row)
    return structure(cells, within, g * g)


def twoadic_structure(s, bits=12):
    """Residue c = n mod 2^bits -> cell; even bits of c (bit-reversed) give x, odd bits give y."""
    half = bits // 2
    side = 1 << half
    tot = [[0] * side for _ in range(side)]
    cnt = [[0] * side for _ in range(side)]
    sq = [[0] * side for _ in range(side)]
    pos = []
    for c in range(1 << bits):
        x = y = 0
        for i in range(half):
            x |= ((c >> (2 * i)) & 1) << (half - 1 - i)
            y |= ((c >> (2 * i + 1)) & 1) << (half - 1 - i)
        pos.append((x, y))
    mask = (1 << bits) - 1
    for n in range(1, N):
        x, y = pos[n & mask]
        tot[y][x] += s[n]
        sq[y][x] += s[n] * s[n]
        cnt[y][x] += 1
    cells = [[tot[i][j] / cnt[i][j] for j in range(side)] for i in range(side)]
    within = [(sq[i][j] - cnt[i][j] * cells[i][j] ** 2) / (cnt[i][j] - 1)
              for i in range(side) for j in range(side)]
    rough = sum(abs(cells[i][j + 1] - cells[i][j]) for i in range(side) for j in range(side - 1))
    return structure(cells, within, (N - 1) / side / side), rough / (side * (side - 1))


def smooth_rows(cells):
    """1-2-1 smoothing ALONG y only (neighbouring n ranges within one residue class)."""
    h = len(cells)
    out = []
    for i in range(h):
        a, b = cells[max(0, i - 1)], cells[min(h - 1, i + 1)]
        out.append([(a[j] + 2 * cells[i][j] + b[j]) / 4 for j in range(len(cells[i]))])
    return out


def log_grid(s, M, order):
    """Node (row i, column p) = mean s over n in [2^(Y0 + i/PER), 2^(Y0 + (i+1)/PER)) with
    n mod M = order[p]. Returned with large n first (top of the picture)."""
    rows = (K - Y0) * PER
    col = [0] * M
    for p, r in enumerate(order):
        col[r] = p
    tot = [[0] * M for _ in range(rows)]
    cnt = [[0] * M for _ in range(rows)]
    for n in range(1 << Y0, N):
        i = int((math.log2(n) - Y0) * PER)
        tot[i][col[n % M]] += s[n]
        cnt[i][col[n % M]] += 1
    cells = [[tot[i][j] / cnt[i][j] for j in range(M)] for i in range(rows)]
    fewest = min(min(r) for r in cnt)
    for _ in range(2):
        cells = smooth_rows(cells)
    return cells[::-1], fewest


def fit(s, k):
    """Least squares s(n) = b0 + b1 a(n mod 2^k) + b2 log2 n over 2^Y0 <= n < N."""
    A = [odd_steps(r, k) for r in range(1 << k)]
    S = [[0.0] * 3 for _ in range(3)]
    T = [0.0] * 3
    yy = ys = 0
    cnt = N - (1 << Y0)
    mask = (1 << k) - 1
    for n in range(1 << Y0, N):
        v = (1.0, A[n & mask], math.log2(n))
        y = s[n]
        for i in range(3):
            T[i] += v[i] * y
            for j in range(3):
                S[i][j] += v[i] * v[j]
        yy += y * y
        ys += y
    M = [S[i][:] + [T[i]] for i in range(3)]
    for c in range(3):
        p = max(range(c, 3), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(3):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * z for x, z in zip(M[r], M[c])]
    b = [M[i][3] / M[i][i] for i in range(3)]
    sse = yy - 2 * sum(b[i] * T[i] for i in range(3)) + sum(b[i] * b[j] * S[i][j]
                                                           for i in range(3) for j in range(3))
    return b, 1 - sse / (yy - ys * ys / cnt)


def contours(cells, level):
    """Marching squares on node values; polylines in grid coordinates (col, row)."""
    h, w = len(cells), len(cells[0])
    segs = []
    table = {1: [("L", "T")], 2: [("T", "R")], 3: [("L", "R")], 4: [("R", "B")], 6: [("T", "B")],
             7: [("L", "B")], 8: [("B", "L")], 9: [("B", "T")], 11: [("B", "R")], 12: [("R", "L")],
             13: [("R", "T")], 14: [("T", "L")]}
    for i in range(h - 1):
        for j in range(w - 1):
            a, b, c, d = cells[i][j], cells[i][j + 1], cells[i + 1][j + 1], cells[i + 1][j]
            idx = (a > level) | (b > level) << 1 | (c > level) << 2 | (d > level) << 3
            if idx in (0, 15):
                continue
            edge = {"T": ("h", i, j), "R": ("v", i, j + 1), "B": ("h", i + 1, j), "L": ("v", i, j)}
            if idx in (5, 10):
                centre = (a + b + c + d) / 4 > level
                if centre:
                    pairs = [("L", "B"), ("T", "R")] if idx == 5 else [("T", "L"), ("B", "R")]
                else:
                    pairs = [("L", "T"), ("R", "B")] if idx == 5 else [("T", "R"), ("B", "L")]
            else:
                pairs = table[idx]
            segs.extend((edge[p], edge[q]) for p, q in pairs)

    def coord(e):
        kind, i, j = e
        i2, j2 = (i, j + 1) if kind == "h" else (i + 1, j)
        v1, v2 = cells[i][j], cells[i2][j2]
        t = (level - v1) / (v2 - v1)
        return (j + t * (j2 - j), i + t * (i2 - i))

    adj = {}
    for k, (e1, e2) in enumerate(segs):
        adj.setdefault(e1, []).append(k)
        adj.setdefault(e2, []).append(k)
    used = [False] * len(segs)
    lines = []
    for k0 in range(len(segs)):
        if used[k0]:
            continue
        used[k0] = True
        chain = [segs[k0][0], segs[k0][1]]
        for forward in (True, False):
            while True:
                end = chain[-1] if forward else chain[0]
                nxt = next((k for k in adj[end] if not used[k]), None)
                if nxt is None:
                    break
                used[nxt] = True
                e1, e2 = segs[nxt]
                other = e2 if e1 == end else e1
                if forward:
                    chain.append(other)
                else:
                    chain.insert(0, other)
        lines.append([coord(e) for e in chain])
    return lines


def sup(k):
    return "2" + str(k).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))


def colour(t):
    return f"rgb({int(60 + 190 * t)},{int(140 + 90 * t - 50 * t * t)},{int(210 - 125 * t)})"


def draw(cells, levels, head, labels_top, labels_left, notes, path, bands=None):
    h, w = len(cells), len(cells[0])
    sx, sy = BW / (w - 1), BH / (h - 1)
    lo, hi = levels[0], levels[-1]
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="480" height="600" viewBox="0 0 480 600">',
           f'<rect width="480" height="600" fill="{BG}"/>',
           f'<text x="240" y="31" text-anchor="middle" font-family="serif" font-size="22" fill="{INK}">'
           f'{head[0]}</text>',
           f'<text x="240" y="49" text-anchor="middle" font-family="sans-serif" font-size="10.5" '
           f'fill="{DIM}">{head[1]}</text>']
    # filled bands: run-length rects per row, colour of the band each node falls in
    fills = {}
    for i in range(h):
        y1 = BY + max(0.0, (i - 0.5) * sy)
        y2 = BY + min(BH, (i + 0.5) * sy)
        j = 0
        while j < w:
            band = max(0, min(len(levels) - 2, int((cells[i][j] - lo) // STEP)))
            j2 = j
            while j2 + 1 < w and max(0, min(len(levels) - 2, int((cells[i][j2 + 1] - lo) // STEP))) == band:
                j2 += 1
            x1 = BX + max(0.0, (j - 0.5) * sx)
            x2 = BX + min(BW, (j2 + 0.5) * sx)
            fills.setdefault(band, []).append(f"M{x1:.1f} {y1:.1f}H{x2:.1f}V{y2:.1f}H{x1:.1f}z")
            j = j2 + 1
    for band, d in sorted(fills.items()):
        t = (band + 0.5) / (len(levels) - 1)
        out.append(f'<path d="{"".join(d)}" fill="{colour(t)}" fill-opacity="{0.13 + 0.27 * t:.2f}"/>')
    if bands:
        for x in bands:
            out.append(f'<line x1="{BX + x * sx:.1f}" y1="{BY}" x2="{BX + x * sx:.1f}" y2="{BY + BH}" '
                       f'stroke="{DIM}" stroke-opacity="0.35" stroke-width="0.5" stroke-dasharray="2 3"/>')
    total = 0
    for k, lev in enumerate(levels):
        t = (lev - lo) / (hi - lo)
        d = []
        for pl in contours(cells, lev):
            if len(pl) < 4:
                continue
            pts = [(BX + x * sx, BY + y * sy) for x, y in pl]
            d.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts))
        total += len(d)
        index = lev % 20 == 0
        out.append(f'<path d="{"".join(d)}" fill="none" stroke="{colour(t)}" '
                   f'stroke-width="{1.2 if index else 0.55}" stroke-opacity="{1 if index else 0.75}" '
                   f'stroke-linejoin="round"/>')
    out.append(f'<rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" fill="none" stroke="{DIM}" '
               f'stroke-opacity="0.5" stroke-width="0.6"/>')
    for x, text, size, col in labels_top:
        out.append(f'<text x="{BX + x * sx:.1f}" y="{BY - 5}" text-anchor="middle" font-family="sans-serif" '
                   f'font-size="{size}" fill="{col}">{text}</text>')
    for y, text in labels_left:
        out.append(f'<text x="{BX - 5}" y="{BY + y * sy + 3:.1f}" text-anchor="end" font-family="sans-serif" '
                   f'font-size="11" fill="{DIM}">{text}</text>')
    kx, ky = BX, BY + BH + 15
    keys = [lev for lev in levels if lev % 20 == 0]
    for k, lev in enumerate(keys):
        t = (lev - lo) / (hi - lo)
        x = kx + (BW - 30) * k / max(1, len(keys) - 1)
        out.append(f'<line x1="{x:.1f}" y1="{ky}" x2="{x + 16:.1f}" y2="{ky}" stroke="{colour(t)}" '
                   f'stroke-width="2"/>')
        out.append(f'<text x="{x + 19:.1f}" y="{ky + 3.5}" font-family="sans-serif" font-size="9" '
                   f'fill="{INK}">{lev}</text>')
    y = ky + 21
    for text, col, size in notes:
        out.append(f'<text x="240" y="{y:.1f}" text-anchor="middle" font-family="sans-serif" '
                   f'font-size="{size}" fill="{col}">{text}</text>')
        y += 15
    out.append(f'<text x="240" y="590" text-anchor="middle" font-family="sans-serif" font-size="9.5" '
               f'fill="{DIM}">ideas after Confluence at 1 · Confluence</text>')
    out.append("</svg>")
    path.write_text("".join(out), encoding="utf-8")
    return path.stat().st_size, total


def main():
    s = stopping_times()
    top = max(range(N), key=lambda n: (s[n], -n))
    print(f"s(n) for 1 <= n < {N}: mean {sum(s) / (N - 1):.2f}, max s({top}) = {s[top]}")

    # --- layouts tried, measured ---------------------------------------------------------------
    print("STRUCTURE = Var(8x8 block means) / (within-block variance / 64); random placement ~ 1")
    for name, val in (("A  n = r + 1024 y, bit-reversed r", column_structure(s, 1024, [bitrev(p, 10) for p in range(1024)])),
                      ("B  n = r + 1024 y, natural r", column_structure(s, 1024, list(range(1024)))),
                      ("C  n = r + 729 y (control)", column_structure(s, 729, list(range(729)))),
                      ("D  n = r + 1000 y (control)", column_structure(s, 1000, list(range(1000)))),
                      ("E  Ulam spiral to 1000^2", spiral_structure(s))):
        print(f"  {name:36s} {val:6.2f}")
    st2, rough2 = twoadic_structure(s)
    print(f"  F  2-adic square, n mod 2^12        {st2:6.2f}  (mean |neighbour diff| {rough2:.1f})")
    print("ETA2 = share of the variance of s(n), 1 <= n < 2^20, explained by the residue class")
    etas = {}
    for M in (8, 16, 64, 81, 125, 729, 1000, 1024):
        e, groups = eta2(s, lambda n, M=M: n % M)
        etas[M] = e
        print(f"  n mod {M:5d}: {100 * e:6.2f}%   (null for random groups ~ {100 * (groups - 1) / (N - 2):.3f}%)")

    m16 = [sum(s[16 + r:N:16]) / len(s[16 + r:N:16]) for r in range(16)]
    a16 = [odd_steps(r, 4) for r in range(16)]
    print("mean s by n mod 16 (a = odd steps in first 4):",
          " ".join(f"{r}:{m:.1f}(a{a16[r]})" for r, m in enumerate(m16)))
    rmin, rmax = min(range(16), key=lambda r: m16[r]), max(range(16), key=lambda r: m16[r])
    print(f"  min r={rmin} {m16[rmin]:.1f}, max r={rmax} {m16[rmax]:.1f}, ratio {m16[rmax] / m16[rmin]:.3f}")

    fits = {}
    for k in (4, KT, 10):
        b, r2 = fit(s, k)
        fits[k] = (b, r2)
        print(f"fit k={k:2d}: s = {b[0]:.2f} + {b[1]:.3f} a + {b[2]:.3f} log2 n  (R2 {r2:.4f}); "
              f"heuristic a-slope 1 + c log2 3 = {1 + b[2] * math.log2(3):.3f}, intercept k(1-c) = {k * (1 - b[2]):.2f}")

    # --- the map ---------------------------------------------------------------------------------
    M = 1 << KT
    av = [odd_steps(r, KT) for r in range(M)]
    order = sorted(range(M), key=lambda r: (av[r], bitrev(r, KT)))
    cells, fewest = log_grid(s, M, order)
    terr = {}
    for r in range(M):
        vals = s[(1 << Y0) + ((r - (1 << Y0)) % M):N:M]
        terr.setdefault(av[r], []).extend(vals)
    terr_mean = {a: sum(v) / len(v) for a, v in sorted(terr.items())}
    print("terrace mean s (2^14 <= n < 2^20) by a:", " ".join(f"{a}:{m:.1f}" for a, m in terr_mean.items()))
    steps = [terr_mean[a + 1] - terr_mean[a] for a in range(KT)]
    print("  rise per terrace:", " ".join(f"{d:.1f}" for d in steps))
    flat = sorted(v for row in cells for v in row)
    lo = STEP * math.floor(flat[0] / STEP)
    hi = STEP * math.ceil(flat[-1] / STEP)
    levels = list(range(lo, hi + 1, STEP))
    print(f"map grid {len(cells)} rows x {len(cells[0])} cols, fewest n per node {fewest}, "
          f"node range {flat[0]:.1f}..{flat[-1]:.1f}, levels {lo}..{hi} step {STEP}")

    edges, labels = [], []
    p = 0
    for a in range(KT + 1):
        wdt = sum(1 for r in range(M) if av[r] == a)
        if a:
            edges.append(p - 0.5)
        labels.append((p + (wdt - 1) / 2, str(a), 10, INK))
        p += wdt
    labels.append((-3.2, "a =", 9, DIM))
    rows = len(cells)
    left = [(rows - 1 - PER * o, sup(Y0 + o)) for o in range(0, K - Y0 + 1, 2) if PER * o <= rows - 1]
    left[0] = (rows - 1, sup(Y0))
    b, r2 = fits[KT]
    tm = list(terr_mean.values())
    notes = [
        (f"x: the {M} classes n mod {M}, sorted by a = odd steps among the first {KT} steps of", DIM, 10),
        (f"n → n/2 or (3n+1)/2. y: log₂ n. Contours every {STEP} of mean s; terraces = values of a.", DIM, 10),
        (f"Fit over all n in [{sup(Y0)}, {sup(K)}): s ≈ {b[1]:.2f} a + {b[2]:.2f} log₂ n − {-b[0]:.1f}; the heuristic", INK, 10.5),
        (f"1 + {b[2]:.2f}·log₂ 3 predicts an a-slope of {1 + b[2] * math.log2(3):.2f}. Terrace means rise "
         f"{tm[0]:.1f} → {tm[-1]:.1f}.", INK, 10.5),
        (f"Mean s by n mod 16 spans {m16[rmin]:.1f} (r = {rmin}) to {m16[rmax]:.1f} (r = {rmax}), ×{m16[rmax] / m16[rmin]:.2f}.", DIM, 10),
        (f"n mod 64 explains {100 * etas[64]:.1f}% of the variance of s; control n mod 81: {100 * etas[81]:.2f}%,"
         f" n mod 1000: {100 * etas[1000]:.1f}%.", DIM, 10),
    ]
    sz, nl = draw(cells, levels, ("The stopping-time landscape",
                                  f"Collatz total stopping time s(n) for {sup(Y0)} ≤ n &lt; {sup(K)}, as a contour map"),
                  labels, left, notes, HERE / "landscape.svg", edges)
    print(f"landscape.svg {sz} bytes, {nl} contour polylines")

    cc, fewest_c = log_grid(s, 81, list(range(81)))
    notes_c = [
        ("Control: x = n mod 81 = 3⁴ in natural order; same rows, smoothing and levels.", DIM, 10),
        (f"n mod 81 explains {100 * etas[81]:.2f}% of the variance of s (n mod 64: {100 * etas[64]:.1f}%).", INK, 10.5),
        (f"n mod 1000 explains {100 * etas[1000]:.1f}%, almost all of it from n mod 8 ({100 * etas[8]:.1f}%): 1000 = 8·125.", DIM, 10),
        (f"n mod 125 alone: {100 * etas[125]:.2f}%. The contours here only climb with log2 n.", DIM, 10),
    ]
    sz_c, nl_c = draw(cc, levels, ("Control: n mod 81", "the same map with a modulus coprime to 2"),
                      [(0, "r = 0", 9, DIM), (80, "80", 9, DIM)], left, notes_c,
                      HERE / "landscape_control.svg")
    print(f"landscape_control.svg {sz_c} bytes, {nl_c} contour polylines, fewest n per node {fewest_c}")


if __name__ == "__main__":
    main()
