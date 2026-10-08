"""Check the five-site Coulomb contact types and regenerate their SVG.

Run: python3 -I playground/marlow/28_finite_coulomb_branches.py
The arbitrary-m, arbitrary-s theorem is proved in the accompanying note.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path


HERE = Path(__file__).resolve().parent
O = (0, 0)
E = (1, 0)
W = (-1, 0)
N = (0, 1)
S = (0, -1)
OUTER = (E, W, N, S)
SITES = (O,) + OUTER


def squared_distance(x, y):
    return sum((a-b)**2 for a, b in zip(x, y))


def check():
    centered = Counter(squared_distance(x, y) for x, y in combinations(OUTER, 2))
    assert centered == {4: 2, 2: 4}
    assert len(list(combinations(SITES, 3))) == 10
    assert len(list(combinations(OUTER, 3))) == 4
    # Centered cost is 2 + 1/sqrt(d2). Since 2 < 4, only d2=4
    # reaches the dual value 5/2; all centerless costs are positive.
    dual = Fraction(5, 2)
    assert Fraction(2) + Fraction(1, 2) == dual

    marginal = [Counter() for _ in range(3)]
    for pair in ((E, W), (N, S)):
        for triple in permutations((O,) + pair):
            for coordinate, site in enumerate(triple):
                marginal[coordinate][site] += Fraction(1, 12)
    expected = {O: Fraction(1, 3),
                E: Fraction(1, 6), W: Fraction(1, 6),
                N: Fraction(1, 6), S: Fraction(1, 6)}
    assert all(dict(m) == expected for m in marginal)
    assert 3*sum((dual if x == O else 0)*mass
                 for x, mass in expected.items()) == dual
    assert expected[O] > max(expected[x] for x in OUTER)
    return centered, expected


def draw(path):
    paper, ink, muted = '#f7f4ed', '#26333d', '#596a72'
    blue, copper = '#527fa9', '#bd7956'
    parts = [f'<rect width="1020" height="445" fill="{paper}"/>',
             f'<text x="38" y="48" font-size="27" fill="{ink}">Five sites, two optimal Coulomb branches</text>',
             f'<text x="38" y="76" font-size="15" fill="{muted}">The central third splits across two antipodal pairs; each outer atom holds only one sixth.</text>',
             '<rect x="35" y="100" width="555" height="300" rx="12" fill="#fffdf9" stroke="#d7d4ca"/>',
             '<rect x="608" y="100" width="376" height="300" rx="12" fill="#fffdf9" stroke="#d7d4ca"/>',
             f'<line x1="130" y1="250" x2="500" y2="250" stroke="{blue}" stroke-width="7" opacity=".55"/>',
             f'<line x1="315" y1="120" x2="315" y2="380" stroke="{copper}" stroke-width="7" opacity=".55"/>']
    nodes = [(130, 250, blue, '−e₁', '1/6'),
             (500, 250, blue, '+e₁', '1/6'),
             (315, 125, copper, '+e₂', '1/6'),
             (315, 375, copper, '−e₂', '1/6'),
             (315, 250, ink, '0', '1/3')]
    for x, y, color, label, mass in nodes:
        parts.extend([f'<circle cx="{x}" cy="{y}" r="27" fill="{color}"/>',
                      f'<text x="{x}" y="{y+6}" text-anchor="middle" font-size="18" fill="#fffdf9">{label}</text>',
                      f'<text x="{x+37}" y="{y-24}" font-size="15" fill="{muted}">{mass}</text>'])
    parts.extend([f'<text x="630" y="145" font-size="20" fill="{ink}">Exact dual certificate</text>',
                  f'<text x="630" y="185" font-size="18" fill="{blue}">u(0) = 5/2</text>',
                  f'<text x="630" y="215" font-size="18" fill="{copper}">u(outer) = 0</text>',
                  f'<text x="630" y="263" font-size="17" fill="{ink}">optimal cost = 5/2</text>',
                  f'<text x="630" y="307" font-size="15" fill="{muted}">2 opposite pairs touch the bound</text>',
                  f'<text x="630" y="333" font-size="15" fill="{muted}">4 cross pairs cost 2 + 1/√2</text>',
                  f'<text x="630" y="370" font-size="14" fill="{muted}">Atomic Monge cost is infinite.</text>',
                  f'<text x="38" y="426" font-size="13" fill="{muted}">Finite mechanism only · the source smooth theorem has equal finite infima without attainment · Marlow</text>'])
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1020 445" width="1020" height="445" role="img" aria-label="Finite five-site Coulomb model with two antipodal optimal branches through a common center" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n')


if __name__ == '__main__':
    centered, expected = check()
    draw(HERE / 'art/finite_coulomb_branches.svg')
    print(f'Centered unordered types: {dict(centered)}; exact marginal: {expected}')
    print('Dual and coupling values both 5/2; SVG written.')
