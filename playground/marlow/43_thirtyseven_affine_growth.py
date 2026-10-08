"""Verify a 16-translate plus one bespoke affine growth family at p=37.

Run: python3 -I playground/marlow/43_thirtyseven_affine_growth.py
"""

from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
P, K = 37, 18
Q = (1, 30, 13, 20, 28, 4, 14, 15, 36, 10, 32, 27, 33, 6, 2, 17, 8, 12,
     5, 25, 11, 29, 34, 18, 16, 19, 22, 31, 7, 21, 3, 9, 35, 23, 24, 26)
R = (1, 3, 16, 28, 23, 19, 29, 11, 5, 26, 9, 20, 35, 15, 18, 27, 36, 31,
     30, 22, 14, 8, 12, 34, 13, 10, 17, 4, 2, 32, 6, 33, 21, 7, 25, 24)
OLD_CENTERS = (36, 35, 34, 30, 29, 25, 24, 23, 19, 18, 14, 13, 9, 8, 4, 3)


def edge(a, b):
    return tuple(sorted((a, b)))


def page(step):
    return [(OLD_CENTERS[step] + a) % P for a in Q] if step < 16 else list(R)


def page_edge_sets(hs):
    edges = [edge(hs[i], hs[(i + 1) % (P - 1)]) for i in range(P - 1)]
    return set(edges), set(edges[::2]), set(edges[1::2])


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
    assert 0 <= j <= 17
    singles, cycles = square()
    slots = {}
    for color, cycle in enumerate(cycles):
        hs = cycle['hubs']
        for i, a in enumerate(hs):
            slots[edge(a, hs[(i + 1) % P])] = (color, i)
    assert len(slots) == P * K
    for step in range(j):
        hs = page(step)
        selected = [slots[edge(hs[i], hs[(i + 1) % (P - 1)])]
                    for i in range(P - 1)]
        assert {color for color, _ in selected[::2]} == set(range(K))
        assert {color for color, _ in selected[1::2]} == set(range(K))
        displaced = [cycles[color]['leaves'][position]
                     for color, position in selected]
        assert len(set(displaced)) == P - 1
        for i, (color, position) in enumerate(selected):
            cycles[color]['leaves'][position] = P + 2 * step + i % 2
        center = OLD_CENTERS[step] if step < 16 else 0
        singles.extend(((center, P + 2 * step),
                        (center, P + 2 * step + 1)))
        cycles.append({'hubs': hs, 'leaves': displaced})
    verify(P + 2 * j, singles, cycles)


def draw(path, overlaps):
    ink, muted, teal, copper = '#25313a', '#5c6970', '#3b927e', '#b47751'
    parts = ['<rect width="980" height="780" fill="#f7f4ed"/>',
             f'<text x="32" y="45" font-size="27" fill="{ink}">The seventeenth page at thirty-seven hubs</text>',
             f'<text x="32" y="76" font-size="15" fill="{muted}">One shared edge per earlier matching keeps displaced leaves distinct.</text>',
             f'<text x="55" y="127" font-size="17" fill="{ink}">earlier center</text>',
             f'<text x="296" y="127" font-size="17" fill="{teal}">even overlap</text>',
             f'<text x="540" y="127" font-size="17" fill="{copper}">odd overlap</text>',
             f'<text x="781" y="127" font-size="17" fill="{ink}">total</text>']
    for i, (center, even, odd) in enumerate(overlaps):
        y = 163 + 36 * i
        if i % 2:
            parts.append(f'<rect x="32" y="{y-25}" width="910" height="32" rx="5" fill="#ebe8df"/>')
        parts.extend([f'<text x="101" y="{y}" text-anchor="middle" font-size="16" fill="{ink}">{center}</text>',
                      f'<text x="346" y="{y}" text-anchor="middle" font-size="18" fill="{teal}">{even}</text>',
                      f'<text x="591" y="{y}" text-anchor="middle" font-size="18" fill="{copper}">{odd}</text>',
                      f'<text x="817" y="{y}" text-anchor="middle" font-size="18" fill="{ink}">{even+odd}</text>'])
    parts.extend([f'<text x="32" y="759" font-size="13" fill="{muted}">Nine totals equal two, always split 1+1 · sixteen translated pages + one bespoke page · Marlow</text>'])
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 780" width="980" height="780" role="img" aria-label="The last thirty-seven-hub page shares at most one edge per earlier alternating matching" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n')


def main():
    assert len(set(OLD_CENTERS)) == 16 and 0 not in OLD_CENTERS
    inv2 = pow(2, -1, P)
    for step in range(17):
        hs = page(step)
        assert len(hs) == P - 1 and len(set(hs)) == P - 1
        assert (OLD_CENTERS[step] if step < 16 else 0) not in hs
        diffs = [min((hs[(i + 1) % (P - 1)] - hs[i]) % P,
                     (hs[i] - hs[(i + 1) % (P - 1)]) % P)
                 for i in range(P - 1)]
        assert set(diffs[::2]) == set(diffs[1::2]) == set(range(1, K + 1))
        mids = [((hs[i] + hs[(i + 1) % (P - 1)]) * inv2) % P
                for i in range(P - 1)]
        center = OLD_CENTERS[step] if step < 16 else 0
        assert set(mids) == set(range(P)) - {center}
    sets = [page_edge_sets(page(step)) for step in range(17)]
    old_pair_counts = Counter(len(sets[i][0] & sets[j][0])
                              for i in range(16) for j in range(i + 1, 16))
    assert old_pair_counts == {0: 58, 1: 62}
    final_edges = sets[16][0]
    overlaps = [(OLD_CENTERS[i], len(final_edges & sets[i][1]),
                 len(final_edges & sets[i][2])) for i in range(16)]
    assert all(even <= 1 and odd <= 1 for _, even, odd in overlaps)
    assert Counter(even + odd for _, even, odd in overlaps) == {0: 2, 1: 5, 2: 9}
    for j in range(18):
        grow(j)
    draw(HERE / 'art/thirtyseven_last_page.svg', overlaps)
    print('Verified 16 translated pages, one final parity-split page, and all 17 growth moves.')


if __name__ == '__main__':
    main()
