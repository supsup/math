"""Check a non-primitive affine growth page at p=17 and a p=13 boundary.

Run: python3 -I playground/marlow/41_seventeen_affine_pages.py
"""

from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
P = 17
K = 8
Q = (1, 2, 9, 14, 8, 16, 13, 6, 7, 11, 15, 12, 4, 10, 5, 3)
CENTERS = (0, 1, 2, 3, 8, 9, 10, 11)


def edge(u, v):
    return tuple(sorted((u, v)))


def page(center):
    return tuple((center + u) % P for u in Q)


def page_edges(center):
    hs = page(center)
    return {edge(hs[i], hs[(i + 1) % (P - 1)]) for i in range(P - 1)}


def affine_square():
    singles = [(a, a) for a in range(P)]
    cycles = []
    inv2 = pow(2, -1, P)
    for d in range(1, K + 1):
        hs = [(i * d) % P for i in range(P)]
        ls = [((hs[i] + hs[(i + 1) % P]) * inv2) % P for i in range(P)]
        cycles.append({'hubs': hs, 'leaves': ls})
    return singles, cycles


def verify(t, singles, cycles):
    seen = set()
    for a, v in singles:
        assert 0 <= a < P and 0 <= v < t and (a, v) not in seen
        seen.add((a, v))
    for c in cycles:
        hs, ls = c['hubs'], c['leaves']
        assert len(hs) == len(ls) and len(set(hs)) == len(hs)
        assert len(set(ls)) == len(ls)
        for i, a in enumerate(hs):
            for v in (ls[i], ls[i - 1]):
                assert 0 <= v < t and (a, v) not in seen
                seen.add((a, v))
    assert seen == {(a, v) for a in range(P) for v in range(t)}
    assert len(singles) + len(cycles) == t + (K * t + P - 1) // P


def growth(j):
    singles, cycles = affine_square()
    slot = {}
    for color, c in enumerate(cycles):
        hs = c['hubs']
        for i, a in enumerate(hs):
            slot[edge(a, hs[(i + 1) % P])] = (color, i)
    assert len(slot) == P * K
    for step, center in enumerate(CENTERS[:j]):
        hs = page(center)
        selected = [slot[edge(hs[i], hs[(i + 1) % (P - 1)])]
                    for i in range(P - 1)]
        assert [color for color, _ in selected[::2]] and set(color for color, _ in selected[::2]) == set(range(K))
        assert set(color for color, _ in selected[1::2]) == set(range(K))
        displaced = [cycles[color]['leaves'][pos] for color, pos in selected]
        assert len(set(displaced)) == P - 1
        for i, (color, pos) in enumerate(selected):
            cycles[color]['leaves'][pos] = P + 2 * step + i % 2
        singles.extend(((center, P + 2 * step), (center, P + 2 * step + 1)))
        cycles.append({'hubs': hs, 'leaves': displaced})
    verify(P + 2 * j, singles, cycles)


def strong_matchings(p):
    """Enumerate unordered matchings with rainbow differences and midpoints."""
    vertices = set(range(1, p))
    inv2 = pow(2, -1, p)
    options = {a: [] for a in vertices}
    for a in vertices:
        for b in vertices:
            if a >= b:
                continue
            d = min(b - a, p - (b - a))
            m = ((a + b) * inv2) % p
            options[a].append((b, d, m))
            options[b].append((a, d, m))
    out = []

    def visit(unused, diffs, mids, chosen):
        if not unused:
            out.append(tuple(chosen))
            return
        a = min(unused)
        for b, d, m in options[a]:
            if b in unused and d not in diffs and m not in mids:
                visit(unused - {a, b}, diffs | {d}, mids | {m},
                      chosen + (edge(a, b),))

    visit(vertices, set(), set(), ())
    return out


def components(vertices, edges):
    adj = {v: [] for v in vertices}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    unseen = set(vertices)
    sizes = []
    while unseen:
        start = min(unseen)
        seen, todo = {start}, [start]
        while todo:
            for v in adj[todo.pop()]:
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
        sizes.append(len(seen))
        unseen -= seen
    return tuple(sorted(sizes))


def thirteen_boundary():
    p = 13
    matchings = strong_matchings(p)
    assert len(matchings) == 8
    inv2 = pow(2, -1, p)
    pairs = Counter()
    for i, a in enumerate(matchings):
        ma = {(u + v) * inv2 % p for u, v in a}
        for b in matchings[i + 1:]:
            if set(a) & set(b) or ma & {(u + v) * inv2 % p for u, v in b}:
                continue
            pairs[components(range(1, p), a + b)] += 1
    assert pairs == {(6, 6): 4, (4, 4, 4): 4}
    return len(matchings), pairs


def draw(path):
    ink, muted, teal, copper = '#25313a', '#5c6970', '#3b927e', '#b47751'
    parts = ['<rect width="1120" height="520" fill="#f7f4ed"/>',
             f'<text x="32" y="45" font-size="27" fill="{ink}">A different growth page at seventeen hubs</text>',
             f'<text x="32" y="75" font-size="15" fill="{muted}">Each column samples all eight affine difference colors; sixteen midpoints are distinct.</text>',
             f'<text x="45" y="120" font-size="18" fill="{ink}">difference</text>',
             f'<text x="220" y="120" font-size="18" fill="{teal}">even edge · midpoint</text>',
             f'<text x="600" y="120" font-size="18" fill="{copper}">odd edge · midpoint</text>']
    inv2 = pow(2, -1, P)
    rows = {d: [None, None] for d in range(1, K + 1)}
    for i, a in enumerate(Q):
        b = Q[(i + 1) % (P - 1)]
        d = min((b - a) % P, (a - b) % P)
        rows[d][i % 2] = (a, b, ((a + b) * inv2) % P)
    for d in range(1, K + 1):
        y = 155 + 38 * (d - 1)
        if d % 2 == 0:
            parts.append(f'<rect x="32" y="{y-24}" width="1040" height="34" rx="5" fill="#ebe8df"/>')
        even, odd = rows[d]
        parts.extend([f'<text x="87" y="{y}" text-anchor="middle" font-size="16" fill="{ink}">d{d}</text>',
                      f'<text x="220" y="{y}" font-size="16" fill="{teal}">{even[0]}–{even[1]} · ℓ{even[2]}</text>',
                      f'<text x="600" y="{y}" font-size="16" fill="{copper}">{odd[0]}–{odd[1]} · ℓ{odd[2]}</text>'])
    parts.append(f'<text x="32" y="492" font-size="14" fill="{muted}">Compatible translated centers: 0, 1, 2, 3, 8, 9, 10, 11 · seven suffice for every odd base · Marlow</text>')
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 520" width="1120" height="520" role="img" aria-label="Eight affine difference classes, their even and odd selected edges and midpoints at seventeen hubs" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n')


def main():
    assert len(Q) == P - 1 and set(Q) == set(range(1, P))
    inv2 = pow(2, -1, P)
    diffs = [[min((Q[(i + 1) % (P - 1)] - Q[i]) % P,
                  (Q[i] - Q[(i + 1) % (P - 1)]) % P)
              for i in range(parity, P - 1, 2)] for parity in (0, 1)]
    assert set(diffs[0]) == set(diffs[1]) == set(range(1, K + 1))
    mids = [((Q[i] + Q[(i + 1) % (P - 1)]) * inv2) % P
            for i in range(P - 1)]
    assert len(set(mids)) == P - 1
    pages = {a: page_edges(a) for a in CENTERS}
    assert all(len(pages[a] & pages[b]) <= 1
               for i, a in enumerate(CENTERS) for b in CENTERS[i + 1:])
    for j in range(len(CENTERS) + 1):
        growth(j)
    n, pairs = thirteen_boundary()
    draw(HERE / 'art/seventeen_affine_pages.svg')
    print('p=17: eight compatible translated pages; checked growth j=0..8.')
    print(f'p=13 affine seed: {n} strong rainbow matchings; '
          f'eligible pairs have component counts {dict(pairs)}, no Hamilton page.')


if __name__ == '__main__':
    main()
