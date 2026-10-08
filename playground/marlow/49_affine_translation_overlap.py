"""Check the difference-pair overlap identity and a 41-center witness.

Run: python3 -I playground/marlow/49_affine_translation_overlap.py
"""

from collections import Counter, defaultdict
from math import cos, pi, sin
from pathlib import Path
from runpy import run_path


HERE = Path(__file__).resolve().parent
CENTERS_41 = tuple(range(1, 20, 2)) + tuple(range(24, 41, 2))


def edge(a, b):
    return tuple(sorted((a, b)))


def profile(p, page):
    k = (p-1)//2
    assert len(page) == p-1 and set(page) == set(range(1, p))
    inv2 = pow(2, -1, p)
    colors = defaultdict(list)
    edges = set()
    for i, a in enumerate(page):
        b = page[(i+1) % (p-1)]
        d = min((b-a) % p, (a-b) % p)
        midpoint = ((a+b)*inv2) % p
        colors[d].append(midpoint)
        edges.add(edge(a, b))
    assert set(colors) == set(range(1, k+1))
    assert all(len(ms) == 2 for ms in colors.values())
    assert len(edges) == p-1
    multiplicity = Counter()
    for ms in colors.values():
        delta = (ms[1]-ms[0]) % p
        assert delta != 0
        multiplicity[min(delta, p-delta)] += 1
    for c in range(1, p):
        shifted = {edge((a+c) % p, (b+c) % p) for a, b in edges}
        assert len(edges & shifted) == multiplicity[min(c, p-c)]
    return multiplicity


def draw(path):
    ink, muted, teal, pale = '#25313a', '#5e6d76', '#2c8b7f', '#d6d4ca'
    chosen = set(CENTERS_41)
    parts = ['<rect width="1000" height="720" fill="#f7f4ed"/>',
             f'<text x="38" y="49" font-size="28" fill="{ink}">Nineteen compatible centers at forty-one hubs</text>',
             f'<text x="39" y="81" font-size="16" fill="{muted}">Conditional on one growth page whose repeated edge displacements lie only at c and 3c</text>',
             '<circle cx="500" cy="354" r="230" fill="#fffdf9" stroke="#d5d1c7" stroke-width="2"/>']
    for n in range(41):
        angle = -pi/2 + 2*pi*n/41
        x, y = 500+230*cos(angle), 354+230*sin(angle)
        if n in chosen:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="{teal}"/>')
            parts.append(f'<text x="{x:.1f}" y="{y+4:.1f}" text-anchor="middle" font-size="11" fill="#fffdf9">{n}</text>')
        else:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{pale}"/>')
    parts.extend([f'<text x="500" y="336" text-anchor="middle" font-size="24" fill="{ink}">19 centers</text>',
                  f'<text x="500" y="368" text-anchor="middle" font-size="16" fill="{muted}">no pair differs by ±1 or ±3</text>',
                  f'<text x="40" y="654" font-size="17" fill="{ink}">Choose 1,3,…,19 and 24,26,…,40 modulo 41; scale by c for forbidden shifts ±c, ±3c.</text>',
                  f'<text x="40" y="685" font-size="14" fill="{muted}">The center set is explicit. Existence of the required growth page at p=41 remains open here. · Marlow</text>'])
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 720" width="1000" height="720" role="img" aria-label="Nineteen residues on a forty-one-point circle whose pairwise differences avoid one and three">' + ''.join(parts) + '</svg>\n')


def main():
    for name in ('41_seventeen_affine_pages.py',
                 '42_twentynine_affine_growth.py',
                 '43_thirtyseven_affine_growth.py'):
        data = run_path(str(HERE / name))
        hist = profile(data['P'], data['Q'])
        print(f"p={data['P']}: repeated-displacement multiplicities {dict(sorted(hist.items()))}")
    chosen = set(CENTERS_41)
    assert len(chosen) == 19
    assert all((a-b) % 41 not in (1, 3, 38, 40)
               for a in chosen for b in chosen if a != b)
    draw(HERE / 'art/fortyone_compatible_centers.svg')
    print('Verified a 19-center independent set for forbidden shifts ±1, ±3.')


if __name__ == '__main__':
    main()
