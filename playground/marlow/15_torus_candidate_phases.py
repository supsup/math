"""Compare the three canonical cubic-torus isoperimetric candidates.

Run: python3 -I playground/marlow/15_torus_candidate_phases.py
This does not check the source paper's global-minimality theorem.
"""

from math import pi, sqrt, isclose
from pathlib import Path


HERE = Path(__file__).resolve().parent
V1 = 4 * pi / 81
V2 = 1 / pi
HIDDEN_CROSSING = sqrt(2 / (9 * pi))


def ball_area(v):
    return (36 * pi) ** (1 / 3) * v ** (2 / 3)


def tube_area(v):
    return 2 * sqrt(pi * v)


def slab_area(_v):
    return 2.0


def check():
    assert 0 < V1 < V2 < 0.5
    assert V1 < HIDDEN_CROSSING < V2
    assert isclose(ball_area(V1), tube_area(V1), rel_tol=1e-14)
    assert isclose(ball_area(V1), 4 * pi / 9, rel_tol=1e-14)
    assert isclose(tube_area(V2), slab_area(V2), rel_tol=1e-14)
    assert isclose(ball_area(HIDDEN_CROSSING), slab_area(HIDDEN_CROSSING), rel_tol=1e-14)
    assert tube_area(HIDDEN_CROSSING) < slab_area(HIDDEN_CROSSING)
    for v in (0.01, V1 / 2):
        assert ball_area(v) < tube_area(v) < slab_area(v)
    for v in ((V1 + V2) / 2,):
        assert tube_area(v) < min(ball_area(v), slab_area(v))
    for v in ((V2 + 0.5) / 2, 0.5):
        assert slab_area(v) < min(ball_area(v), tube_area(v))


def draw(path):
    ink, muted, paper = '#252420', '#68635c', '#f7f4ed'
    blue, copper, teal = '#586aa2', '#ba7550', '#2d8c82'
    parts = [f'<rect width="1020" height="710" fill="{paper}"/>',
             f'<text x="40" y="50" font-size="29" fill="{ink}">A growing bubble in a periodic cube</text>',
             f'<text x="40" y="79" font-size="16" fill="{muted}">Three candidate shapes; opposite cube faces are identified. Schematics above, exact areas below.</text>']

    panels = ((42, '1 · BALL', blue), (360, '2 · WRAPPING TUBE', copper),
              (678, '3 · SLAB', teal))
    for x, label, color in panels:
        parts.append(f'<rect x="{x}" y="105" width="298" height="193" rx="12" fill="#fffdf8" stroke="#ded7ca"/>')
        parts.append(f'<text x="{x+18}" y="132" font-size="16" fill="{color}">{label}</text>')
        # One transparent periodic cell in an orthographic schematic.
        a, b, w, h, dx, dy = x+61, 159, 135, 106, 27, -17
        parts.append(f'<path d="M{a+dx} {b+dy}h{w}v{h}h-{w}z M{a} {b}h{w}v{h}h-{w}z M{a} {b}l{dx} {dy} M{a+w} {b}l{dx} {dy} M{a} {b+h}l{dx} {dy} M{a+w} {b+h}l{dx} {dy}" fill="none" stroke="#a9a297" stroke-width="1.5"/>')
    # Shapes deliberately schematic, not volume-matched renderings.
    parts.append(f'<circle cx="170" cy="211" r="32" fill="{blue}" fill-opacity=".70" stroke="{blue}" stroke-width="2"/>')
    parts.append(f'<path d="M416 192h138a18 18 0 0 1 0 36H416a18 18 0 0 1 0-36z" fill="{copper}" fill-opacity=".72" stroke="{copper}" stroke-width="2"/>')
    parts.append(f'<path d="M734 195h135v43H734z" fill="{teal}" fill-opacity=".65" stroke="{teal}" stroke-width="2"/>')
    parts.append(f'<text x="190" y="283" text-anchor="middle" font-size="13" fill="{muted}">local, round boundary</text>')
    parts.append(f'<text x="508" y="283" text-anchor="middle" font-size="13" fill="{muted}">one direction closes on itself</text>')
    parts.append(f'<text x="826" y="283" text-anchor="middle" font-size="13" fill="{muted}">two flat boundaries</text>')

    x0, y0, width, height = 75, 635, 875, 286
    def xy(v, area):
        return x0 + 2 * width * v, y0 - height * area / 3.2

    parts.append(f'<text x="42" y="337" font-size="18" fill="{ink}">Boundary area versus enclosed volume V (0 &lt; V ≤ 1/2)</text>')
    for area in (0, 1, 2, 3):
        y = xy(0, area)[1]
        parts.append(f'<path d="M{x0} {y:.2f}H{x0+width}" stroke="#ded8cb" stroke-width="1"/>')
        parts.append(f'<text x="{x0-12}" y="{y+5:.2f}" text-anchor="end" font-size="13" fill="{muted}">{area}</text>')
    for v, label in ((0, '0'), (V1, '4π/81'), (V2, '1/π'), (0.5, '1/2')):
        x = xy(v, 0)[0]
        parts.append(f'<path d="M{x:.2f} {y0}v6" stroke="{ink}"/>')
        parts.append(f'<text x="{x:.2f}" y="{y0+24}" text-anchor="middle" font-size="13" fill="{muted}">{label}</text>')
    for v in (V1, V2):
        x = xy(v, 0)[0]
        parts.append(f'<path d="M{x:.2f} {y0-height}V{y0}" stroke="#b9b0a0" stroke-dasharray="5 5"/>')
    for fn, color in ((ball_area, blue), (tube_area, copper), (slab_area, teal)):
        coords = [xy(i / 1000, fn(i / 1000)) for i in range(1, 501)]
        points = ' '.join(f'{x:.2f},{y:.2f}' for x, y in coords)
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.3" stroke-opacity=".55"/>')
    coords = [xy(i / 1000, min(ball_area(i / 1000),
                                   tube_area(i / 1000), slab_area(i / 1000)))
              for i in range(1, 501)]
    points = ' '.join(f'{x:.2f},{y:.2f}' for x, y in coords)
    parts.append(f'<polyline points="{points}" fill="none" stroke="{ink}" stroke-width="3.6"/>')
    for v, area in ((V1, 4*pi/9), (V2, 2)):
        x, y = xy(v, area)
        parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="{ink}"/>')
    parts.append(f'<text x="75" y="686" font-size="13" fill="{muted}">Dark line = least area among these three candidates. Global minimality is the paper’s separate claim.</text>')
    parts.append(f'<text x="966" y="686" text-anchor="end" font-size="12" fill="{muted}">Marlow · family 354 candidate geometry</text>')
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1020 710" width="1020" height="710" role="img" aria-label="Three schematic periodic-cube shapes and their exact candidate boundary-area curves" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n'
    path.write_text(svg)


def main():
    check()
    draw(HERE / 'art/torus_candidate_phases.svg')
    print(f'ball/tube crossing: V=4π/81={V1:.9f}, area=4π/9={4*pi/9:.9f}')
    print(f'tube/slab crossing: V=1/π={V2:.9f}, area=2')
    print(f'ball/slab crossing is hidden above the tube: V={HIDDEN_CROSSING:.9f}')
    print('Generated candidate-only torus diagram.')


if __name__ == '__main__':
    main()
