"""The complex Collatz fractal as a pure SVG: a contour map instead of pixels.

Same field as complex_variations.smooth_fractal: f(z) = (2 + 7z - (2 + 5z) cos(pi z)) / 4, each point
coloured by a smooth escape count nu. Here nu is sampled on a grid and its level lines are traced by
marching squares (one <path> per level), so every line is vector and scales cleanly; the points that
never escape (the dark sea around the 1-2 cycle and the islands on the real axis) are filled with
row-merged rectangles. No raster, no href.

Standard library only: python3 -I collatz_fractal_svg.py  ->  variations/m_complex_fractal_contours_lite.svg
"""
import cmath
import math
import pathlib

GW, GH = 300, 106                    # coarser grid for a small file
X0, X1, YH = -0.4, 5.6, 1.05
W, H = 1080, 380                      # drawing size
LEVELS = [0.9, 1.5, 2.1, 2.8, 4.0]
MAX_IT, R = 60, 30.0


def f(z):
    return (2 + 7 * z - (2 + 5 * z) * cmath.cos(math.pi * z)) / 4


def nu_at(z):
    n = 0
    try:
        while n < MAX_IT:
            z = f(z)
            n += 1
            if abs(z.imag) > R or abs(z) > 1e10:
                big = abs(z.imag) if abs(z.imag) > R else abs(z)
                return n - math.log(max(math.log(big) / math.log(R), 1.0)) / math.log(math.pi)
    except OverflowError:
        return float(n)
    return None                       # never escaped


def main():
    xs = [X0 + (X1 - X0) * i / (GW - 1) for i in range(GW)]
    ys = [YH - 2 * YH * j / (GH - 1) for j in range(GH)]
    field = [[nu_at(complex(x, y)) for x in xs] for y in ys]
    sea = sum(v is None for row in field for v in row)
    big = 99.0                        # the sea counts as "very slow" for contouring
    val = [[big if v is None else v for v in row] for row in field]
    sx, sy = W / (GW - 1), H / (GH - 1)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H + 46}" viewBox="0 0 {W} {H + 46}">',
           f'<rect width="{W}" height="{H + 46}" fill="#0d1b2a"/>']
    # sea: merge runs of non-escaping samples per row into rectangles
    rects = []
    for j, row in enumerate(field):
        i = 0
        while i < GW:
            if row[i] is None:
                k = i
                while k < GW and row[k] is None:
                    k += 1
                rects.append(f"M{(i - 0.5) * sx:.1f} {(j - 0.5) * sy:.1f}h{(k - i) * sx:.1f}v{sy:.1f}h{-(k - i) * sx:.1f}z")
                i = k
            else:
                i += 1
    out.append(f'<path d="{"".join(rects)}" fill="#050b12"/>')
    total = 0
    for li, lev in enumerate(LEVELS):
        segs = []
        for j in range(GH - 1):
            for i in range(GW - 1):
                c = [(i, j, val[j][i]), (i + 1, j, val[j][i + 1]), (i + 1, j + 1, val[j + 1][i + 1]), (i, j + 1, val[j + 1][i])]
                pts = []
                for k in range(4):
                    (xa, ya, va), (xb, yb, vb) = c[k], c[(k + 1) % 4]
                    if (va - lev) * (vb - lev) < 0:
                        t = (lev - va) / (vb - va)
                        pts.append(((xa + t * (xb - xa)) * sx, (ya + t * (yb - ya)) * sy))
                for a, b in zip(pts[0::2], pts[1::2]):
                    segs.append("M%.1f %.1fL%.1f %.1f" % (*a, *b))
        total += len(segs)
        t = li / (len(LEVELS) - 1)
        colour = f"rgb({int(70 + 180 * t)},{int(90 + 130 * t)},{int(120 + 30 * t)})"
        out.append(f'<path d="{"".join(segs)}" fill="none" stroke="{colour}" stroke-width="{0.5 + 0.7 * t:.2f}" '
                   f'stroke-opacity="{0.55 + 0.45 * t:.2f}"/>')
    out.append(f'<text x="{W / 2}" y="{H + 20}" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#e8eef2">'
               'f(z) = (2 + 7z - (2 + 5z) cos πz) / 4: contours of how slowly each point escapes</text>')
    out.append(f'<text x="{W / 2}" y="{H + 38}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#7d92a6">'
               f'Re z from {X0} to {X1}, Im z within ±{YH}; {len(LEVELS)} levels; dark = never escapes in {MAX_IT} steps '
               f'({sea:,} of {GW * GH:,} samples) · Confluence</text>')
    out.append("</svg>")
    p = pathlib.Path(__file__).with_name("variations") / "m_complex_fractal_contours_lite.svg"
    p.write_text("".join(out), encoding="utf-8")
    print(p.name, p.stat().st_size, "bytes; segments", total, "sea rects", len(rects), "sea samples", sea)


if __name__ == "__main__":
    main()
