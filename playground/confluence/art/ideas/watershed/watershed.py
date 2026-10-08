"""Watershed map of Gaussian-integer Collatz: every a + bi in a box, at its TRUE position in the plane,
coloured by which cycle (sea) its trajectory reaches; dark if it passes a cap first (it 'runs off').

Rule: z is even iff (1 + i) | z iff a + b is even; then z -> z / (1 + i); else z -> m z + 1.
Two panels: m = 2 - i and m = 3. Cells are drawn as row-merged rectangles (pure vector, no raster).
Standard library only: python3 -I watershed.py  ->  watershed.svg
"""
import pathlib

R = 40
CAP_NORM, CAP_STEPS = 10**24, 4000
BG, INK, DIM = "#0d1b2a", "#e8eef2", "#7d92a6"
SEA_COLOURS = ["#f4d58d", "#ff8fa3", "#8fd3ff", "#b8f28f", "#d7a6ff", "#ffc078", "#9fe3d9", "#e599f7"]
RUNOFF = "#060d15"


def step(z, m):
    a, b = z
    if (a + b) % 2 == 0:
        return ((a + b) // 2, (b - a) // 2)
    return (m[0] * a - m[1] * b + 1, m[0] * b + m[1] * a)


def classify(m):
    fate = {}            # value -> cycle representative, or None for run-off
    reps = {}
    for a in range(-R, R + 1):
        for b in range(-R, R + 1):
            z = (a, b)
            if z in fate:
                continue
            path, seen = [], {}
            while z not in fate and z not in seen:
                if z[0] * z[0] + z[1] * z[1] > CAP_NORM or len(path) > CAP_STEPS:
                    z = None
                    break
                seen[z] = len(path)
                path.append(z)
                z = step(z, m)
            if z is None:
                res = None
            elif z in fate:
                res = fate[z]
            else:
                cyc = path[seen[z]:]
                res = min(cyc, key=lambda w: (w[0] ** 2 + w[1] ** 2, w))
                reps[res] = cyc
            for v in path:
                fate[v] = res
    grid = {(a, b): fate[(a, b)] for a in range(-R, R + 1) for b in range(-R, R + 1)}
    return grid, reps


def label(z):
    a, b = z
    if b == 0:
        return str(a)
    bi = ("" if abs(b) == 1 else str(abs(b))) + "i"
    if a == 0:
        return ("-" if b < 0 else "") + bi
    return f"{a}{'-' if b < 0 else '+'}{bi}"


def panel(m, name, x0, y0, size):
    grid, reps = classify(m)
    counts = {}
    for v in grid.values():
        counts[v] = counts.get(v, 0) + 1
    seas = sorted((k for k in counts if k is not None), key=lambda k: -counts[k])
    colour = {k: SEA_COLOURS[i % len(SEA_COLOURS)] for i, k in enumerate(seas)}
    cell = size / (2 * R + 1)
    out = []
    by_colour = {}
    for b in range(R, -R - 1, -1):           # rows top (b = R) to bottom
        row_y = y0 + (R - b) * cell
        a = -R
        while a <= R:
            f = grid[(a, b)]
            k = a
            while k <= R and grid[(k, b)] == f:
                k += 1
            col = RUNOFF if f is None else colour[f]
            by_colour.setdefault(col, []).append(f"M{x0 + (a + R) * cell:.2f} {row_y:.2f}h{(k - a) * cell:.2f}v{cell:.2f}h{-(k - a) * cell:.2f}z")
            a = k
    for col, d in by_colour.items():
        out.append(f'<path d="{"".join(d)}" fill="{col}"/>')
    # axes and the cycles' positions (only the members that fall inside the box)
    cx, cy = x0 + R * cell + cell / 2, y0 + R * cell + cell / 2
    out.append(f'<line x1="{x0}" y1="{cy:.1f}" x2="{x0 + size}" y2="{cy:.1f}" stroke="{INK}" stroke-opacity="0.25" stroke-width="0.6"/>')
    out.append(f'<line x1="{cx:.1f}" y1="{y0}" x2="{cx:.1f}" y2="{y0 + size}" stroke="{INK}" stroke-opacity="0.25" stroke-width="0.6"/>')
    for k in seas:
        for (a, b) in reps.get(k, []):
            if -R <= a <= R and -R <= b <= R:
                px, py = x0 + (a + R) * cell + cell / 2, y0 + (R - b) * cell + cell / 2
                out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{max(1.2, cell * 0.45):.2f}" fill="none" stroke="{BG}" stroke-width="1"/>')
    total = len(grid)
    run = counts.get(None, 0)
    legend = [(colour[k], f"{label(k)}: {counts[k]:,}" + (" (0 is even, so 0 -> 0)" if k == (0, 0) else "")) for k in seas[:5]]
    def frac(lo, hi):
        ring = [v for (a, b), v in grid.items() if lo <= max(abs(a), abs(b)) <= hi]
        return sum(v is not None for v in ring) / len(ring)
    legend.append((None, f"caught: {100 * frac(0, 10):.0f}% within |a|,|b| \u2264 10, {100 * frac(31, R):.0f}% in 31..{R}"))
    return out, total, run, legend, seas, counts


def main():
    W, H = 480, 600
    size = 216
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect width="{W}" height="{H}" fill="{BG}"/>',
           f'<text x="240" y="36" text-anchor="middle" font-family="serif" font-size="21" fill="{INK}">'
           'Where the Gaussian rivers go</text>',
           f'<text x="240" y="58" text-anchor="middle" font-family="serif" font-style="italic" font-size="13" fill="{DIM}">'
           f'every a + bi with |a|, |b| ≤ {R}, at its true place, coloured by the sea it reaches</text>']
    summary = []
    for m, name, x0 in (((2, -1), "z -> (2-i)z + 1", 16), ((3, 0), "z -> 3z + 1", 248)):
        parts, total, run, legend, seas, counts = panel(m, name, x0, 92, size)
        out += parts
        out.append(f'<text x="{x0 + size / 2}" y="84" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{INK}">{name}</text>')
        y = 92 + size + 20
        caught = total - run
        out.append(f'<text x="{x0 + size / 2}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="{INK}">'
                   f'{caught:,} of {total:,} reach a sea ({100 * caught / total:.1f}%)</text>')
        y += 16
        out.append(f'<text x="{x0 + size / 2}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="10.5" fill="{DIM}">'
                   f'{len(seas)} seas; the largest:</text>')
        for col, text in legend:
            y += 15
            if col is None:
                out.append(f'<text x="{x0 + size / 2}" y="{y + 4}" text-anchor="middle" font-family="sans-serif" font-size="10" fill="{DIM}">{text}</text>')
                continue
            out.append(f'<rect x="{x0 + 22}" y="{y - 9}" width="10" height="10" fill="{col}"/>')
            out.append(f'<text x="{x0 + 38}" y="{y}" font-family="monospace" font-size="10" fill="{INK}">{text}</text>')
        summary.append((name, total, caught, len(seas), [(label(k), counts[k]) for k in seas[:5]]))
    notes = ["No watershed territories, unlike Newton's method: the basins are speckle,",
             "neighbours rarely share a sea. Catching thins out away from 0.",
             "'Even' = divisible by 1+i (a + b even), then z -> z/(1+i). Dark = passes",
             "norm 10^24 first (runs off). Circles: cycle members inside the box."]
    y = 500
    for t in notes:
        out.append(f'<text x="240" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="10.5" fill="{DIM}">{t}</text>')
        y += 16
    out.append(f'<text x="240" y="592" text-anchor="middle" font-family="sans-serif" font-size="9" fill="{DIM}">ideas after Confluence at 1 · Confluence</text>')
    out.append("</svg>")
    p = pathlib.Path(__file__).with_name("watershed.svg")
    p.write_text("".join(out), encoding="utf-8")
    print(p.name, p.stat().st_size, "bytes")
    for s in summary:
        print(*s)


if __name__ == "__main__":
    main()
