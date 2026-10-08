"""Draw the two-vertex picture: the dual unit ball B and the lens L(x,1) for x = (9/10, 0), H = {root}.

B = conv(unit disk, (1,1), (-1,-1)) in coordinates (f(root), f(child)).
L(x,1) = {y : x+y in B, x-y in B} = (B - x) cap (B + x)   (B is symmetric).
The theorem bounds |y_child| (the tail outside H) by 2 sqrt(1 - |x|^2) = 0.8718; the lens reaches 0.6.
Pure python, writes lens.svg next to this file.
"""
import math
import pathlib


def ball(k=240):
    pts = [(1.0, 1.0)]
    # arc from (0,1) counterclockwise to (-1,0)
    for i in range(k + 1):
        t = math.pi / 2 + (math.pi / 2) * i / k
        pts.append((math.cos(t), math.sin(t)))
    pts.append((-1.0, -1.0))
    for i in range(k + 1):
        t = 3 * math.pi / 2 + (math.pi / 2) * i / k
        pts.append((math.cos(t), math.sin(t)))
    return pts  # counterclockwise, convex


def clip(subject, clipper):
    """Sutherland-Hodgman: subject polygon clipped by convex counterclockwise clipper."""
    def inside(p, a, b):
        return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= -1e-12

    def inter(p, q, a, b):
        x1, y1, x2, y2 = p[0], p[1], q[0], q[1]
        x3, y3, x4, y4 = a[0], a[1], b[0], b[1]
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))

    out = subject
    for i in range(len(clipper)):
        a, b = clipper[i], clipper[(i + 1) % len(clipper)]
        inp, out = out, []
        if not inp:
            break
        s = inp[-1]
        for e in inp:
            if inside(e, a, b):
                if not inside(s, a, b):
                    out.append(inter(s, e, a, b))
                out.append(e)
            elif inside(s, a, b):
                out.append(inter(s, e, a, b))
            s = e
    return out


r = 0.9
B = ball()
Bm = [(p[0] - r, p[1]) for p in B]
Bp = [(p[0] + r, p[1]) for p in B]
lens = clip(Bm, Bp)
ymax = max(p[1] for p in lens)
bound = 2 * math.sqrt(1 - r * r)
assert abs(ymax - 0.6) < 2e-3, ymax

W, Hh = 1000, 400
S = 105  # pixels per unit


def panel(ox, oy):
    def tr(p):
        return (ox + S * p[0], oy - S * p[1])
    return tr


def poly(pts, tr, **kw):
    d = " ".join(f"{tr(p)[0]:.2f},{tr(p)[1]:.2f}" for p in pts)
    attrs = " ".join(f'{k.rstrip("_")}="{v}"' for k, v in kw.items())
    return f'<polygon points="{d}" {attrs}/>'


def dot(p, tr, cls, label, dx=8, dy=-8):
    x, y = tr(p)
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4.5" class="{cls}"/>'
            f'<text x="{x + dx:.2f}" y="{y + dy:.2f}" class="lbl">{label}</text>')


def axes(tr, xr, yr):
    (x0, y0), (x1, y1) = tr((xr[0], 0)), tr((xr[1], 0))
    (a0, b0), (a1, b1) = tr((0, yr[0])), tr((0, yr[1]))
    return (f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" class="axis"/>'
            f'<line x1="{a0}" y1="{b0}" x2="{a1}" y2="{b1}" class="axis"/>')


L = panel(215, 195)
R = panel(700, 195)
parts = []
parts.append(axes(L, (-1.35, 1.45), (-1.3, 1.3)))
parts.append(poly(B, L, class_="ball"))
parts.append(dot((r, 0), L, "x", "x = (0.9, 0)", 6, 18))
parts.append(dot((1.0, 0.6), L, "p", "x+y = (1, 0.6)"))
parts.append(dot((0.8, -0.6), L, "p", "x−y = (0.8, −0.6)", 8, 18))
parts.append(f'<text x="{L((-1.3, 1.45))[0]}" y="{L((-1.3, 1.45))[1]}" class="ttl">dual unit ball B (two vertices)</text>')

parts.append(axes(R, (-2.0, 2.0), (-1.3, 1.3)))
parts.append(poly(Bm, R, class_="shift"))
parts.append(poly(Bp, R, class_="shift"))
parts.append(poly(lens, R, class_="lens"))
for yy, cls, txt in ((bound, "bnd", "theorem bound 2√(1−‖x‖²) = 0.872"),
                     (ymax, "act", "lens reaches 0.6 = 2√(r(1−r))")):
    for sgn in (1, -1):
        (x0, y0), (x1, y1) = R((-2.0, sgn * yy)), R((2.0, sgn * yy))
        parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" class="{cls}"/>')
    tx, ty = R((0.95, yy + 0.05)) if cls == "bnd" else R((0.95, yy - 0.17))
    parts.append(f'<text x="{tx}" y="{ty}" class="lbl {cls}t">{txt}</text>')
parts.append(dot((0.1, 0.6), R, "p", "y = (0.1, 0.6)", 8, 18))
parts.append(dot((-0.1, -0.6), R, "p", "−y", 8, 18))
parts.append(f'<text x="{R((-1.9, 1.45))[0]}" y="{R((-1.9, 1.45))[1]}" class="ttl">lens (B−x) ∩ (B+x), x = (0.9, 0)</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hh}" viewBox="0 0 {W} {Hh}" font-family="Helvetica, Arial, sans-serif">
<title>Midpoint lens, two-vertex case</title>
<style>
  .bg {{ fill: #ffffff; }}
  .axis {{ stroke: #8a8a8e; stroke-width: 1; }}
  .ball {{ fill: #d9e6f5; stroke: #3a6ea5; stroke-width: 1.6; }}
  .shift {{ fill: none; stroke: #3a6ea5; stroke-width: 1.2; stroke-dasharray: 5 4; }}
  .lens {{ fill: #f2b84b; fill-opacity: 0.8; stroke: #1d1d1f; stroke-width: 1.2; }}
  .bnd {{ stroke: #c0392b; stroke-width: 1.4; stroke-dasharray: 7 4; }}
  .act {{ stroke: #2e7d32; stroke-width: 1.4; }}
  .bndt {{ fill: #c0392b; }} .actt {{ fill: #2e7d32; }}
  .x {{ fill: #1d1d1f; }} .p {{ fill: #c0392b; }}
  .lbl {{ fill: #1d1d1f; font-size: 12px; }} .ttl {{ fill: #1d1d1f; font-size: 14px; font-weight: 600; }}
  .cap {{ fill: #6a6a6e; font-size: 12px; }}
</style>
<rect class="bg" width="{W}" height="{Hh}"/>
{"".join(parts)}
<text x="20" y="{Hh - 16}" class="cap">horizontal axis: coefficient on the root (inside H); vertical axis: coefficient on the child (the tail Q_H). Ball = conv(unit disk, ±(1,1)).</text>
</svg>
'''
STY = {
    "bg": 'fill="#ffffff"', "axis": 'stroke="#8a8a8e" stroke-width="1"',
    "ball": 'fill="#d9e6f5" stroke="#3a6ea5" stroke-width="1.6"',
    "shift": 'fill="none" stroke="#3a6ea5" stroke-width="1.2" stroke-dasharray="5 4"',
    "lens": 'fill="#f2b84b" fill-opacity="0.8" stroke="#1d1d1f" stroke-width="1.2"',
    "bnd": 'stroke="#c0392b" stroke-width="1.4" stroke-dasharray="7 4"',
    "act": 'stroke="#2e7d32" stroke-width="1.4"', "x": 'fill="#1d1d1f"', "p": 'fill="#c0392b"',
    "lbl": 'fill="#1d1d1f" font-size="12"', "lbl bndt": 'fill="#c0392b" font-size="12"',
    "lbl actt": 'fill="#2e7d32" font-size="12"', "ttl": 'fill="#1d1d1f" font-size="14" font-weight="600"',
    "cap": 'fill="#6a6a6e" font-size="12"',
}
import re as _re
svg = _re.sub(r'<style>.*?</style>\n', '', svg, flags=_re.S)
svg = _re.sub(r'class="([^"]+)"', lambda m: STY[m.group(1)], svg)
pathlib.Path(__file__).with_name("lens.svg").write_text(svg)
print(f"lens max |y_child| = {ymax:.5f}, bound = {bound:.5f}; wrote lens.svg")
