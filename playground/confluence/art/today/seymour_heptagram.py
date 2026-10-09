"""Seymour's tight heptagram: the Paley tournament on 7 vertices.

Arcs v -> v + d (mod 7) for d in the quadratic residues {1, 2, 4}. Every vertex has exactly 3 first
out-neighbours (v + residues) and exactly 3 second out-neighbours (v + non-residues), so every vertex is
TIGHT for Seymour's second-neighbourhood conjecture: equality, never slack. Vertex 0 is lit: gold arrows
to its first ring, teal two-step paths to its second ring. The rest of the tournament is drawn faintly.

The script asserts the tightness before drawing, so the picture cannot claim what the graph does not do.
Run: python3 -I seymour_heptagram.py  (writes seymour_heptagram.svg next to itself)
"""
import math
import pathlib

N = 7
RES = {1, 2, 4}
OUT = {v: {(v + d) % N for d in RES} for v in range(N)}
SECOND = {v: {w for u in OUT[v] for w in OUT[u]} - OUT[v] - {v} for v in range(N)}
for v in range(N):
    assert len(OUT[v]) == len(SECOND[v]) == 3, v
    assert OUT[v] | SECOND[v] | {v} == set(range(N)), v

W = H = 760
CX, CY, R = W / 2, H / 2 + 10, 270
STEP_COL = {1: "#6f8fbf", 2: "#9b7fc4", 4: "#c46f9a"}
GOLD, TEAL = "#f2c14e", "#4fd1c5"


def pt(v, r=R):
    a = -math.pi / 2 + 2 * math.pi * v / N
    return CX + r * math.cos(a), CY + r * math.sin(a)


def arc(a, b, bend, colour, width, opacity, marker, dash=""):
    (x1, y1), (x2, y2) = pt(a), pt(b)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    # bend toward the centre, so the arcs make a rose
    qx, qy = mx + (CX - mx) * bend, my + (CY - my) * bend
    # shorten the end so the arrowhead sits on the node rim
    dx, dy = x2 - qx, y2 - qy
    L = math.hypot(dx, dy)
    ex, ey = x2 - dx / L * 17, y2 - dy / L * 17
    d = f'M{x1:.1f},{y1:.1f} Q{qx:.1f},{qy:.1f} {ex:.1f},{ey:.1f}'
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{width}" '
            f'stroke-opacity="{opacity}" marker-end="url(#{marker})"{da}/>')


parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs>']
for name, col in [("faint", "#8892a6"), ("gold", GOLD), ("teal", TEAL)]:
    parts.append(f'<marker id="{name}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" '
                 f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
parts.append('<radialGradient id="bg" cx="50%" cy="50%" r="65%"><stop offset="0" stop-color="#1b2133"/>'
             '<stop offset="1" stop-color="#0b0e17"/></radialGradient></defs>')
parts.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

# the whole tournament, faint, coloured by step
for v in range(N):
    for d in sorted(RES):
        if v == 0:
            continue
        parts.append(arc(v, (v + d) % N, 0.22 * d / 4 + 0.08, STEP_COL[d], 1.6, 0.45, "faint"))

# vertex 0: two-step paths to the second ring (teal, dashed), then the first ring (gold)
for w in sorted(SECOND[0]):
    u = next(u for u in sorted(OUT[0]) if w in OUT[u])
    parts.append(arc(0, u, 0.12, TEAL, 2.2, 0.55, "teal", "6 5"))
    parts.append(arc(u, w, 0.18, TEAL, 2.6, 0.95, "teal", "6 5"))
for u in sorted(OUT[0]):
    parts.append(arc(0, u, 0.12, GOLD, 3.2, 1.0, "gold"))

# halos: first ring gold, second ring teal
for v in range(N):
    x, y = pt(v)
    if v in OUT[0]:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="26" fill="none" stroke="{GOLD}" stroke-width="2" stroke-opacity="0.7"/>')
    if v in SECOND[0]:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="26" fill="none" stroke="{TEAL}" stroke-width="2" stroke-opacity="0.7"/>')
    fill = "#ffffff" if v == 0 else "#d9dee8"
    parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="#0b0e17" stroke="{fill}" stroke-width="2.4"/>')
    parts.append(f'<text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle" font-family="Georgia, serif" '
                 f'font-size="15" fill="{fill}">{v}</text>')

parts.append(f'<text x="{CX}" y="44" text-anchor="middle" font-family="Georgia, serif" font-size="24" '
             f'fill="#e8ecf4">Seymour&#8217;s tight heptagram</text>')
parts.append(f'<text x="{CX}" y="70" text-anchor="middle" font-family="Georgia, serif" font-size="13.5" '
             f'fill="#a9b2c4">Paley tournament on 7 vertices: v &#8594; v+1, v+2, v+4 (the squares mod 7)</text>')
parts.append(f'<text x="{CX}" y="{H - 40}" text-anchor="middle" font-family="Georgia, serif" font-size="13.5" '
             f'fill="#a9b2c4"><tspan fill="{GOLD}">first ring {{1, 2, 4}}</tspan>  =  3  =  '
             f'<tspan fill="{TEAL}">second ring {{3, 5, 6}}</tspan></text>')
parts.append(f'<text x="{CX}" y="{H - 20}" text-anchor="middle" font-family="Georgia, serif" font-size="12" '
             f'fill="#7f889a">equality at every vertex: the residues reach the non-residues in two steps</text>')
parts.append('</svg>')

pathlib.Path(__file__).with_suffix(".svg").write_text("\n".join(parts))
print("wrote", pathlib.Path(__file__).with_suffix(".svg"))
