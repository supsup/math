"""Confluence's card for Fixpoint's 'The Reviewers' showcase (undervoice 15917).

The math: a row-ratio vector of the Fourier matrix F6 (rows one apart) is v_k = z^k with z = e^(i pi/3).
Its cubes are +1 and -1, splitting the six unit vectors into two cube fibres, {z^0, z^2, z^4} and
{z^1, z^3, z^5}. The proved lemma (ratio_cubeFiber_sum_zero, HadamardCubeFiber) says each fibre sums to
zero: drawn head to tail, each one closes into a triangle. Rows three apart (sum v^2 != 0) are the
control: their +1 fibre is three copies of 1, and the path runs off and does not close.

Deterministic, no dependencies: python3 -I make_confluence_card.py  ->  confluence.svg
"""
import cmath
import math
import pathlib

W, H = 480, 600
BG, INK, DIM = "#0f1420", "#e8e6df", "#5d6475"
A, B, GREY = "#2ec4b6", "#f4a259", "#7a8090"
z = cmath.exp(1j * math.pi / 3)


def pt(c, cx, cy, r):
    # y axis up in the math, down in SVG
    return cx + r * c.real, cy - r * c.imag


def arrow(x1, y1, x2, y2, colour, width=3.0, head=9.0):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx = x2 - head * math.cos(ang)
    hy = y2 - head * math.sin(ang)
    left = (hx + head * 0.5 * math.sin(ang), hy - head * 0.5 * math.cos(ang))
    right = (hx - head * 0.5 * math.sin(ang), hy + head * 0.5 * math.cos(ang))
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{hx:.2f}" y2="{hy:.2f}" stroke="{colour}" '
            f'stroke-width="{width}" stroke-linecap="round"/>'
            f'<polygon points="{x2:.2f},{y2:.2f} {left[0]:.2f},{left[1]:.2f} {right[0]:.2f},{right[1]:.2f}" '
            f'fill="{colour}"/>')


def chain(vectors, x0, y0, r, colour):
    out, x, y = [], x0, y0
    for v in vectors:
        nx, ny = x + r * v.real, y - r * v.imag
        out.append(arrow(x, y, nx, ny, colour))
        x, y = nx, ny
    out.append(f'<circle cx="{x0:.2f}" cy="{y0:.2f}" r="4" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    return "".join(out), (x, y)


def main():
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    s.append(f'<text x="240" y="44" text-anchor="middle" font-family="serif" font-size="24" fill="{INK}">'
             'Two fibres, both closed</text>')
    # Top: the six row-ratio entries on the unit circle, coloured by cube value
    cx, cy, r = 240, 205, 120
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{DIM}" stroke-width="1"/>')
    for k in range(6):
        x, y = pt(z ** k, cx, cy, r)
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.2f}" y2="{y:.2f}" stroke="{DIM}" stroke-width="0.8" '
                 'stroke-dasharray="3 4"/>')
    for fibre, colour in (((0, 2, 4), A), ((1, 3, 5), B)):
        pts = " ".join("%.2f,%.2f" % pt(z ** k, cx, cy, r) for k in fibre)
        s.append(f'<polygon points="{pts}" fill="{colour}" fill-opacity="0.12" stroke="{colour}" '
                 'stroke-width="2"/>')
    for k in range(6):
        colour = A if k % 2 == 0 else B
        x, y = pt(z ** k, cx, cy, r)
        s.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="7" fill="{colour}"/>')
        lx, ly = pt(z ** k, cx, cy, r + 24)
        s.append(f'<text x="{lx:.2f}" y="{ly + 5:.2f}" text-anchor="middle" font-family="serif" '
                 f'font-style="italic" font-size="16" fill="{INK}">ζ<tspan font-size="11" dy="-7">{k}</tspan></text>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{INK}"/>')
    # Middle: each fibre head to tail, closing
    t1, _ = chain([z ** 0, z ** 2, z ** 4], 72, 435, 78, A)
    t2, _ = chain([z ** 1, z ** 3, z ** 5], 369, 435, 78, B)
    s += [t1, t2]
    s.append(f'<text x="111" y="470" text-anchor="middle" font-family="monospace" font-size="13" fill="{A}">'
             'ζ⁰+ζ²+ζ⁴ = 0</text>')
    s.append(f'<text x="369" y="470" text-anchor="middle" font-family="monospace" font-size="13" fill="{B}">'
             'ζ¹+ζ³+ζ⁵ = 0</text>')
    # Bottom: the control, rows three apart, does not close
    t3, end = chain([1, 1, 1], 150, 520, 52, GREY)
    s.append(t3)
    s.append(f'<text x="{end[0] + 14:.2f}" y="525" font-family="monospace" font-size="13" fill="{GREY}">'
             '1+1+1 = 3</text>')
    s.append(f'<text x="240" y="560" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{DIM}">'
             'rows one apart close · rows three apart run off</text>')
    s.append(f'<text x="240" y="580" text-anchor="middle" font-family="sans-serif" font-size="11" fill="{DIM}">'
             'F6 row ratios split by cube value · Confluence</text>')
    s.append("</svg>")
    out = pathlib.Path(__file__).with_name("confluence.svg")
    out.write_text("".join(s), encoding="utf-8")
    print(out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
