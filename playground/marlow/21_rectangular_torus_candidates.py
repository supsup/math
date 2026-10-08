"""Check and draw the three standard candidates in unit-volume rectangular tori.

Run: python3 -I playground/marlow/21_rectangular_torus_candidates.py
Only compares candidate regions; does not claim global isoperimetric minimality.
"""

from math import isclose, pi, sqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent


def phases(a, b, c):
    assert 0 < a <= b <= c and isclose(a * b * c, 1.0)
    return 4 * pi * a**3 / 81, b / (pi * c)


def areas(v, a, c):
    return ((36 * pi) ** (1 / 3) * v ** (2 / 3),
            2 * sqrt(pi * a * v), 2 / c)


def hidden_crossing(c):
    return sqrt(2 / (9 * pi)) / c ** (3 / 2)


def check(a, b, c):
    v1, v2 = phases(a, b, c)
    v0 = hidden_crossing(c)
    assert 0 < v1 < v0 < v2 < 0.5
    assert isclose(v1 / v2, (4 * pi**2 / 81) * (a / b)**2)
    assert isclose(v2 / v1, (81 / (4 * pi**2)) * (b / a)**2)
    ball1, tube1, slab1 = areas(v1, a, c)
    ball2, tube2, slab2 = areas(v2, a, c)
    ball0, tube0, slab0 = areas(v0, a, c)
    assert isclose(ball1, tube1) and isclose(ball1, 4 * pi * a*a / 9)
    assert ball1 < slab1
    assert isclose(tube2, slab2) and isclose(slab2, 2 / c)
    assert tube2 < ball2
    assert isclose(ball0, slab0) and tube0 < ball0
    assert a / 3 < a / 2  # ball radius at first switch
    assert b / pi < b / 2  # transverse tube radius at second switch
    assert isclose(sqrt(v2 / (pi * a)), b / pi)
    assert isclose(sqrt(pi * a / v2), pi / b)
    assert isclose(sqrt(pi * a / v1), 9 / (2 * a))
    assert isclose(2 / (a / 3), 6 / a)
    for v, winner in ((v1 / 2, 0), ((v1 + v2) / 2, 1),
                      ((v2 + 0.5) / 2, 2)):
        vals = areas(v, a, c)
        assert vals[winner] == min(vals)
    return v1, v2


def draw(path):
    paper, ink, faint = '#f8f5ee', '#222633', '#d7d4ca'
    muted, ball_color, tube_color, slab_color = '#59606d', '#576cad', '#ba754c', '#389487'
    curves = ((1.0, 1.0, 1.0, 'Cube  1 : 1 : 1'),
              (0.5, 1.0, 2.0, 'Rectangular  1/2 : 1 : 2'))
    parts = [f'<rect width="1120" height="670" fill="{paper}"/>',
             f'<text x="48" y="53" font-size="29" fill="{ink}">Stretching a periodic box moves the shape switches</text>',
             f'<text x="48" y="82" font-size="16" fill="{muted}">Least boundary area among a ball, a shortest wrapping tube, and a two-wall slab · unit volume</text>']
    for index, (a, b, c, title) in enumerate(curves):
        left = 62 + index * 535
        top, width, height = 175, 455, 362
        v1, v2 = phases(a, b, c)

        def xy(v, area):
            return left + width * sqrt(v / 0.5), top + height * (1 - area / 2.45)

        parts += [f'<rect x="{left-17}" y="106" width="{width+34}" height="486" rx="15" fill="#fffdf9" stroke="{faint}"/>',
                  f'<text x="{left}" y="139" font-size="19" fill="{ink}">{title}</text>',
                  f'<text x="{left}" y="160" font-size="13" fill="{muted}">ball→tube: {v1:.4f}     tube→slab: {v2:.4f}</text>']
        for area in (0, 0.5, 1, 1.5, 2):
            y = xy(0, area)[1]
            parts.append(f'<path d="M{left} {y:.2f}h{width}" stroke="{faint}" stroke-width="1"/>')
            parts.append(f'<text x="{left-5}" y="{y+4:.2f}" text-anchor="end" font-size="11" fill="{muted}">{area:g}</text>')
        for v, label in ((0, '0'), (v1, 'v₁'), (v2, 'v₂'), (0.5, '1/2')):
            x = xy(v, 0)[0]
            if v in (v1, v2):
                parts.append(f'<path d="M{x:.2f} {top}v{height}" stroke="{faint}" stroke-dasharray="4 5"/>')
            parts.append(f'<text x="{x:.2f}" y="{top+height+25}" text-anchor="middle" font-size="13" fill="{muted}">{label}</text>')
        for start, end, shape, color in ((0, v1, 0, ball_color),
                                         (v1, v2, 1, tube_color),
                                         (v2, 0.5, 2, slab_color)):
            coords = [xy(start + (end-start)*j/90, areas(start + (end-start)*j/90, a, c)[shape])
                      for j in range(91)]
            points = ' '.join(f'{x:.2f},{y:.2f}' for x, y in coords)
            parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>')
        for v, color in ((v1, ball_color), (v2, slab_color)):
            x, y = xy(v, min(areas(v, a, c)))
            parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5.5" fill="{color}" stroke="#fffdf9" stroke-width="2"/>')
        parts.append(f'<text x="{left+width/2:.1f}" y="{top+height+49}" text-anchor="middle" font-size="13" fill="{muted}">√(v / 1/2)  ·  v = smaller enclosed volume</text>')
    parts.append(f'<text x="49" y="632" font-size="14" fill="{muted}">Candidate comparison only. Other regions may have less area; no rectangular global-minimality claim is made.</text>')
    parts.append(f'<text x="1072" y="632" text-anchor="end" font-size="12" fill="{muted}">Marlow · family 354 geometry</text>')
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 670" width="1120" height="670" role="img" aria-label="Two candidate boundary-area envelopes for cubic and rectangular flat three-tori" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n'
    path.write_text(svg)


def main():
    for a, b, c in ((1, 1, 1), (0.5, 1, 2), (0.25, 1, 4),
                    (0.5, 0.5, 4), (0.4, 1.25, 2)):
        v1, v2 = check(a, b, c)
        print(f'{a:g}:{b:g}:{c:g}: v1={v1:.9f}, v2={v2:.9f}')
    draw(HERE / 'art/rectangular_torus_candidates.svg')
    print('Wrote candidate-only rectangular-torus diagram.')


if __name__ == '__main__':
    main()
