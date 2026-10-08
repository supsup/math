"""Verify an explicit affine two-leaf growth family at prime 29.

Run: python3 -I playground/marlow/42_twentynine_affine_growth.py
"""

from pathlib import Path


HERE = Path(__file__).resolve().parent
P, K = 29, 14
Q = (1, 2, 13, 15, 6, 20, 19, 12, 18, 27, 10, 4, 9, 25,
     11, 8, 16, 24, 28, 23, 26, 7, 5, 22, 3, 14, 21, 17)
CENTERS = (2, 5, 8, 11, 12, 14, 15, 18, 21, 24, 25, 27, 28)


def edge(a, b):
    return tuple(sorted((a, b)))


def page(center):
    return [(center + v) % P for v in Q]


def page_edges(center):
    hs = page(center)
    return {edge(hs[i], hs[(i + 1) % (P - 1)]) for i in range(P - 1)}


def square():
    singles = [(a, a) for a in range(P)]
    cycles = []
    inv2 = pow(2, -1, P)
    for d in range(1, K + 1):
        hs = [(d * i) % P for i in range(P)]
        ls = [((hs[i] + hs[(i + 1) % P]) * inv2) % P for i in range(P)]
        cycles.append({'hubs': hs, 'leaves': ls})
    return singles, cycles


def verify(t, singles, cycles):
    seen = set()
    for a, v in singles:
        assert 0 <= a < P and 0 <= v < t and (a, v) not in seen
        seen.add((a, v))
    for cycle in cycles:
        hs, ls = cycle['hubs'], cycle['leaves']
        assert 2 <= len(hs) == len(ls) <= P
        assert len(set(hs)) == len(hs) and len(set(ls)) == len(ls)
        for i, a in enumerate(hs):
            for v in (ls[i], ls[i - 1]):
                assert 0 <= a < P and 0 <= v < t and (a, v) not in seen
                seen.add((a, v))
    assert seen == {(a, v) for a in range(P) for v in range(t)}
    assert len(singles) == t
    assert len(cycles) == (K * t + P - 1) // P


def grow(j):
    assert 0 <= j <= len(CENTERS)
    singles, cycles = square()
    slots = {}
    for color, cycle in enumerate(cycles):
        hs = cycle['hubs']
        for i, a in enumerate(hs):
            slots[edge(a, hs[(i + 1) % P])] = (color, i)
    assert len(slots) == P * K
    for step, center in enumerate(CENTERS[:j]):
        hs = page(center)
        selected = [slots[edge(hs[i], hs[(i + 1) % (P - 1)])]
                    for i in range(P - 1)]
        assert {color for color, _ in selected[::2]} == set(range(K))
        assert {color for color, _ in selected[1::2]} == set(range(K))
        displaced = [cycles[color]['leaves'][position]
                     for color, position in selected]
        assert len(set(displaced)) == P - 1
        for i, (color, position) in enumerate(selected):
            cycles[color]['leaves'][position] = P + 2 * step + i % 2
        singles.extend(((center, P + 2 * step),
                        (center, P + 2 * step + 1)))
        cycles.append({'hubs': hs, 'leaves': displaced})
    t = P + 2 * j
    verify(t, singles, cycles)
    return singles, cycles


def draw(path):
    ink, muted, teal, copper = '#25313a', '#5c6970', '#3b927e', '#b47751'
    width, height = 1120, 750
    inv2 = pow(2, -1, P)
    rows = {d: [None, None] for d in range(1, K + 1)}
    for i, a in enumerate(Q):
        b = Q[(i + 1) % (P - 1)]
        d = min((b - a) % P, (a - b) % P)
        rows[d][i % 2] = (a, b, ((a + b) * inv2) % P)
    parts = [f'<rect width="{width}" height="{height}" fill="#f7f4ed"/>',
             f'<text x="32" y="45" font-size="27" fill="{ink}">Thirteen growth steps at twenty-nine hubs</text>',
             f'<text x="32" y="75" font-size="15" fill="{muted}">The base page has one even and one odd edge of every affine difference color.</text>',
             f'<text x="46" y="122" font-size="18" fill="{ink}">difference</text>',
             f'<text x="218" y="122" font-size="18" fill="{teal}">even edge · midpoint</text>',
             f'<text x="604" y="122" font-size="18" fill="{copper}">odd edge · midpoint</text>']
    for d in range(1, K + 1):
        y = 159 + 38 * (d - 1)
        if d % 2 == 0:
            parts.append(f'<rect x="32" y="{y-25}" width="1044" height="34" rx="5" fill="#ebe8df"/>')
        even, odd = rows[d]
        parts.extend([f'<text x="88" y="{y}" text-anchor="middle" font-size="16" fill="{ink}">d{d}</text>',
                      f'<text x="218" y="{y}" font-size="16" fill="{teal}">{even[0]}–{even[1]} · ℓ{even[2]}</text>',
                      f'<text x="604" y="{y}" font-size="16" fill="{copper}">{odd[0]}–{odd[1]} · ℓ{odd[2]}</text>'])
    parts.extend([f'<text x="32" y="700" font-size="15" fill="{ink}">13 selected translates: 39 page pairs disjoint, 39 share one edge.</text>',
                  f'<text x="32" y="724" font-size="13" fill="{muted}">Each midpoint from 1 to 28 occurs once. Even weave + offset lift complete all leaf counts · Marlow</text>'])
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="Affine difference table for a twenty-nine-hub compatible growth page" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n')


def main():
    assert len(Q) == P - 1 and set(Q) == set(range(1, P))
    inv2 = pow(2, -1, P)
    diffs = [min((Q[(i + 1) % (P - 1)] - Q[i]) % P,
                 (Q[i] - Q[(i + 1) % (P - 1)]) % P)
             for i in range(P - 1)]
    assert set(diffs[::2]) == set(diffs[1::2]) == set(range(1, K + 1))
    mids = [((Q[i] + Q[(i + 1) % (P - 1)]) * inv2) % P
            for i in range(P - 1)]
    assert set(mids) == set(range(1, P))
    pages = [page_edges(center) for center in CENTERS]
    intersections = [len(pages[i] & pages[j])
                     for i in range(len(pages)) for j in range(i + 1, len(pages))]
    assert intersections.count(0) == intersections.count(1) == 39
    assert len(intersections) == 78
    for j in range(K):
        grow(j)
    draw(HERE / 'art/twentynine_affine_growth.svg')
    print('Verified 13 compatible translated pages, all 13 odd bases, and exact spoke coverage.')


if __name__ == '__main__':
    main()
