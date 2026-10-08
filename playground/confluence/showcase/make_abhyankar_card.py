"""Showcase card for family 049 (Abhyankar-Sathaye counterexample): the cusp inside the fibre F = -1.

F is the paper's polynomial (paper.tex:87-99, Identities.lean S, P, F). At its critical point
P = (2, 0, -1/2, 1/2) (paper.tex:113) the value is -1 and every first partial is 0. This script
computes, exactly, the order to which F + 1 vanishes along two directions through P: along
d1 = (0, 0, 9, 4) it vanishes to order 3, and along d2 = (7, 0, -16, 36) (the one direction where the
rank-1 Hessian is nonzero) to order 2. So on the plane P + s*d1 + t*d2 the level F = -1 is a cusp,
and nearby levels are smooth curves. It then draws the level curves by marching squares.

Every number written into the SVG comes from this script. Deterministic, standard library only:
python3 -I make_abhyankar_card.py  ->  abhyankar-049.svg
"""
import math
import pathlib
from fractions import Fraction as Q

P = (Q(2), Q(0), Q(-1, 2), Q(1, 2))
D1 = (0, 0, 9, 4)
D2 = (7, 0, -16, 36)


def F(h, u, v, w):
    x = u**3 + h * v
    y = -u**2 + h * w
    s = 2 * u**3 * v + 3 * u**4 * w + h * (v * v - 3 * u * u * w * w) + h * h * w**3
    p = -2 * s * s * x + 3 * s * y * y - 3 * s**3 * y
    return h - p - 1


class Poly:
    """Univariate polynomial in t with Fraction coefficients, just enough arithmetic for F."""
    def __init__(self, c):
        self.c = list(c) if isinstance(c, (list, tuple)) else [Q(c)]

    def _co(self, o):
        return o if isinstance(o, Poly) else Poly(o)

    def __add__(self, o):
        o = self._co(o)
        n = max(len(self.c), len(o.c))
        return Poly([(self.c[i] if i < len(self.c) else 0) + (o.c[i] if i < len(o.c) else 0) for i in range(n)])
    __radd__ = __add__

    def __neg__(self):
        return Poly([-x for x in self.c])

    def __sub__(self, o):
        return self + (-self._co(o))

    def __rsub__(self, o):
        return self._co(o) - self

    def __mul__(self, o):
        o = self._co(o)
        r = [Q(0)] * (len(self.c) + len(o.c) - 1)
        for i, a in enumerate(self.c):
            for j, b in enumerate(o.c):
                r[i + j] += a * b
        return Poly(r)
    __rmul__ = __mul__

    def __pow__(self, n):
        r = Poly(1)
        for _ in range(n):
            r = r * self
        return r


def order_along(d):
    g = F(*[Poly([P[i], Q(d[i])]) for i in range(4)]) + 1
    k = next(i for i, x in enumerate(g.c) if x != 0)
    return k, g.c[k]


def g(s, t):
    return F(*[float(P[i]) + s * D1[i] + t * D2[i] for i in range(4)]) + 1.0


def contour(level, xs, ys, vals):
    """Marching squares: list of segments ((x1,y1),(x2,y2)) where vals crosses level."""
    segs = []
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            corners = [(xs[i], ys[j], vals[i][j]), (xs[i + 1], ys[j], vals[i + 1][j]),
                       (xs[i + 1], ys[j + 1], vals[i + 1][j + 1]), (xs[i], ys[j + 1], vals[i][j + 1])]
            pts = []
            for k in range(4):
                (xa, ya, va), (xb, yb, vb) = corners[k], corners[(k + 1) % 4]
                if (va - level) * (vb - level) < 0:
                    f = (level - va) / (vb - va)
                    pts.append((xa + f * (xb - xa), ya + f * (yb - ya)))
            if len(pts) == 2:
                segs.append((pts[0], pts[1]))
            elif len(pts) == 4:
                segs += [(pts[0], pts[1]), (pts[2], pts[3])]
    return segs


def main():
    assert F(*P) == -1
    k1, c1 = order_along(D1)
    k2, c2 = order_along(D2)
    # window: |s| <= S, and t scaled to the cusp, t^2 ~ s^3 * c1 / c2
    S = 0.02
    T = math.sqrt(float(abs(c1)) * S**3 / float(abs(c2))) * 1.6
    N = 260
    xs = [-S + 2 * S * i / N for i in range(N + 1)]
    ys = [-T + 2 * T * j / N for j in range(N + 1)]
    vals = [[g(x, y) for y in ys] for x in xs]
    scale = float(abs(c1)) * S**3
    levels = [(-0.35 * scale, "#4c78a8"), (-0.12 * scale, "#4c78a8"), (0.0, "#e45756"),
              (0.12 * scale, "#54a24b"), (0.35 * scale, "#54a24b")]

    W, H = 480, 600
    BG, INK, DIM = "#fbfaf6", "#1f2430", "#7a7f8c"
    ox, oy, pw, ph = 40, 110, 400, 330

    def px(x, y):
        return ox + (x + S) / (2 * S) * pw, oy + ph - (y + T) / (2 * T) * ph

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect width="{W}" height="{H}" fill="{BG}"/>',
           f'<text x="240" y="44" text-anchor="middle" font-family="serif" font-size="23" fill="{INK}">'
           'The cusp inside the fibre</text>',
           f'<text x="240" y="70" text-anchor="middle" font-family="serif" font-style="italic" font-size="14" '
           f'fill="{DIM}">level curves of F near its critical point P</text>',
           f'<rect x="{ox}" y="{oy}" width="{pw}" height="{ph}" fill="none" stroke="{DIM}" stroke-width="0.8"/>']
    for level, colour in levels:
        width = 2.6 if level == 0.0 else 1.2
        for (a, b) in contour(level, xs, ys, vals):
            (x1, y1), (x2, y2) = px(*a), px(*b)
            out.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{colour}" '
                       f'stroke-width="{width}" stroke-linecap="round"/>')
    cx, cy = px(0, 0)
    out.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="4" fill="{INK}"/>')
    out.append(f'<text x="{cx + 8:.2f}" y="{cy - 8:.2f}" font-family="serif" font-style="italic" font-size="15" '
               f'fill="{INK}">P</text>')
    lines = [
        ("F = -1 (red) pinches to a cusp at P; nearby levels stay smooth", INK, 13),
        (f"F+1 vanishes to order {k1} along (0,0,9,4) (coefficient {c1}),", DIM, 12),
        (f"to order {k2} along (7,0,-16,36) (coefficient {c2}), and grad F(P) = 0", DIM, 12),
        ("A coordinate has no critical point, so F is not one;", DIM, 12),
        ("yet F = 0 is a copy of affine 3-space. Family 049.", DIM, 12),
    ]
    y = 474
    for text, colour, size in lines:
        out.append(f'<text x="240" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" '
                   f'fill="{colour}">{text}</text>')
        y += 22
    out.append(f'<text x="240" y="584" text-anchor="middle" font-family="sans-serif" font-size="10" fill="{DIM}">'
               f'plane P + s(0,0,9,4) + t(7,0,-16,36), |s| &#8804; {S}, coordinates (h,u,v,w) · Confluence</text>')
    out.append("</svg>")
    path = pathlib.Path(__file__).with_name("abhyankar-049.svg")
    path.write_text("".join(out), encoding="utf-8")
    print(path, path.stat().st_size, "bytes; orders", (k1, c1), (k2, c2), "window S", S, "T", round(T, 6))


if __name__ == "__main__":
    main()
