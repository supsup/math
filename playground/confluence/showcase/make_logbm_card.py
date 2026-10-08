"""Showcase card: the log-Brunn-Minkowski inequality in one picture.

K = the square [-1,1]^2, L = K turned 45 degrees, t = 1/2. Their L_0 (log) combination is the Wulff body
W = { x : <x,u> <= h_K(u)^(1/2) h_L(u)^(1/2) for every unit u }, computed here by clipping a big square
against N half-planes. The inequality says |W| >= |K|^(1/2) |L|^(1/2) = 4. Every number on the card is
computed below. Standard library only: python3 -I make_logbm_card.py  ->  logbm-wulff.svg
"""
import math
import pathlib

N = 4096
ROT = math.pi / 4
T = 0.5


def h_square(u, rot):
    c, s = math.cos(-rot), math.sin(-rot)
    x, y = c * u[0] - s * u[1], s * u[0] + c * u[1]
    return abs(x) + abs(y)


def clip(poly, a, b, c):
    out = []
    for i in range(len(poly)):
        p, q = poly[i], poly[(i + 1) % len(poly)]
        fp, fq = a * p[0] + b * p[1] - c, a * q[0] + b * q[1] - c
        if fp <= 0:
            out.append(p)
        if fp * fq < 0:
            s = fp / (fp - fq)
            out.append((p[0] + s * (q[0] - p[0]), p[1] + s * (q[1] - p[1])))
    return out


def area(p):
    return abs(sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))) / 2


def wulff(t):
    w = [(-3, -3), (3, -3), (3, 3), (-3, 3)]
    for k in range(N):
        a = 2 * math.pi * k / N
        u = (math.cos(a), math.sin(a))
        w = clip(w, u[0], u[1], h_square(u, 0) ** (1 - t) * h_square(u, ROT) ** t)
    return w


def main():
    W = wulff(T)
    assert abs(area(W) - (16 - 8 * math.sqrt(2))) < 1e-9, area(W)  # the exact octagon
    aw, gm = area(W), 4.0 ** (1 - T) * 4.0 ** T
    curve = [(t / 10, area(wulff(t / 10)) / 4.0) for t in range(11)]
    K = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
    L = [(math.sqrt(2), 0), (0, math.sqrt(2)), (-math.sqrt(2), 0), (0, -math.sqrt(2))]
    BG, INK, DIM, GOLD, AQUA, ROSE = "#0d1b2a", "#e8eef2", "#7d92a6", "#f4d58d", "#8fd3ff", "#ff8fa3"
    cx, cy, sc = 240, 236, 108

    def pts(poly):
        return " ".join(f"{cx + sc * x:.2f},{cy - sc * y:.2f}" for x, y in poly)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="600" viewBox="0 0 480 600">',
         f'<rect width="480" height="600" fill="{BG}"/>',
         f'<text x="240" y="38" text-anchor="middle" font-family="serif" font-size="21" fill="{INK}">Bigger than the geometric mean</text>',
         f'<text x="240" y="60" text-anchor="middle" font-family="serif" font-style="italic" font-size="13" fill="{DIM}">the log-Brunn-Minkowski inequality for two squares</text>',
         f'<polygon points="{pts(W)}" fill="{GOLD}" fill-opacity="0.22" stroke="{GOLD}" stroke-width="2.2"/>',
         f'<polygon points="{pts(K)}" fill="none" stroke="{AQUA}" stroke-width="1.6"/>',
         f'<polygon points="{pts(L)}" fill="none" stroke="{ROSE}" stroke-width="1.6"/>',
         f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="{INK}"/>',
         f'<text x="{cx + sc + 6}" y="{cy - sc - 6}" font-family="sans-serif" font-size="12" fill="{AQUA}">K</text>',
         f'<text x="{cx + sc * 1.414 + 6}" y="{cy + 4}" font-family="sans-serif" font-size="12" fill="{ROSE}">L</text>',
         f'<text x="{cx + 30}" y="{cy - sc * 1.22}" font-family="sans-serif" font-size="12" fill="{GOLD}">W</text>']
    # inset: |W_t| / 4 against t
    ix, iy, iw, ih = 150, 392, 180, 60
    top = max(r for _, r in curve)
    o.append(f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" fill="none" stroke="{DIM}" stroke-width="0.6"/>')
    ypos = lambda r: iy + ih - (r - 1) / (top - 1) * (ih - 8) - 4
    o.append(f'<line x1="{ix}" y1="{ypos(1):.1f}" x2="{ix + iw}" y2="{ypos(1):.1f}" stroke="{DIM}" stroke-dasharray="3 3"/>')
    o.append('<polyline points="' + " ".join(f"{ix + t * iw:.1f},{ypos(r):.1f}" for t, r in curve) + f'" fill="none" stroke="{GOLD}" stroke-width="1.8"/>')
    o.append(f'<text x="{ix - 6}" y="{ypos(1) + 4:.1f}" text-anchor="end" font-family="sans-serif" font-size="10" fill="{DIM}">1</text>')
    o.append(f'<text x="{ix - 6}" y="{ypos(top) + 4:.1f}" text-anchor="end" font-family="sans-serif" font-size="10" fill="{DIM}">{top:.3f}</text>')
    o.append(f'<text x="{ix + iw / 2}" y="{iy + ih + 14}" text-anchor="middle" font-family="sans-serif" font-size="10" fill="{DIM}">|W_t| / |K|^(1-t)|L|^t  for t from 0 to 1</text>')
    lines = [(f"W = log-combination at t = 1/2: support at most √(h_K h_L) in every direction", INK, 12),
             (f"|W| = {aw:.4f} against |K|^(1/2) |L|^(1/2) = {gm:.0f}: ratio {aw / gm:.4f}", INK, 12),
             (f"W is the regular octagon of inradius 2^(1/4), area 16 - 8\u221a2 = {16 - 8 * math.sqrt(2):.4f}", GOLD, 11),
             ("The conjecture (BLYZ 2012), which the collection's family 091 claims to prove:", DIM, 11),
             ("|W| ≥ the geometric mean for origin-symmetric convex bodies, every dimension.", DIM, 11),
             ("The collection's Lean artifact kernel-checks that formal statement.", DIM, 11)]
    y = 490
    for text, col, size in lines:
        o.append(f'<text x="240" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" fill="{col}">{text}</text>')
        y += 16
    o.append(f'<text x="240" y="592" text-anchor="middle" font-family="sans-serif" font-size="9" fill="{DIM}">{N:,} directions clipped; family 091 · Confluence</text>')
    o.append("</svg>")
    p = pathlib.Path(__file__).with_name("logbm-wulff.svg")
    p.write_text("".join(o), encoding="utf-8")
    print(p.name, p.stat().st_size, "bytes; |W| =", round(aw, 6), "ratio", round(aw / gm, 6), "curve", [round(r, 4) for _, r in curve])


if __name__ == "__main__":
    main()
