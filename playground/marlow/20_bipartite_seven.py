"""Verify exact cycle/edge partitions for every K_(7,t).

Run: python3 -I playground/marlow/20_bipartite_seven.py
Regenerates art/bipartite_seven_eight.svg from the checked certificate.
"""

from html import escape
from pathlib import Path


HUBS = tuple(range(7))
LEAF_NAMES = 'ABCDEFGHIJKL'
SINGLETONS_8 = ((0, 0), (0, 1), (1, 2), (1, 3),
                (2, 4), (2, 5), (3, 6), (3, 7))
WALKS_8 = (
    (1, 'E', 3, 'D', 4, 'F', 5, 'C', 6, 'G', 2, 'H'),
    (0, 'F', 3, 'A', 2, 'B', 4, 'G', 5, 'E', 6, 'H'),
    (0, 'D', 6, 'A', 5, 'H', 4, 'C', 3, 'B', 1, 'G'),
    (0, 'C', 2, 'D', 5, 'B', 6, 'F', 1, 'A', 4, 'E'),
)

SEED_DATA = {
    2: ("6A 6B", """0,A,1,B
2,A,3,B
4,A,5,B"""),
    3: ("0B 1C 2A 3C 4C 5B 6B", """0,A,1,B,2,C
3,A,4,B
5,A,6,C"""),
    4: ("0A 0B 1C 1D", """0,C,6,A,5,B,4,D
1,A,3,C,2,D,6,B
2,A,4,C,5,D,3,B"""),
    5: ("0A 1A 2A 3B 4C 5D 6E", """2,C,6,A,3,D,4,B,5,E
0,B,6,D,1,C,5,A,4,E
0,C,3,E,1,B,2,D"""),
    6: ("0A 0B 1C 1D 2E 2F", """1,A,2,D,4,E,5,C,6,F,3,B
0,C,2,B,5,F,4,A,6,D,3,E
0,D,5,A,3,C,4,B,6,E,1,F"""),
    9: ("0A 0B 0C 1D 2E 3F 4G 5H 6I", """0,G,1,A,5,F,2,I,3,B,4,C,6,H
0,E,1,H,2,C,3,A,6,B,5,D,4,I
0,D,3,E,6,G,5,C,1,B,2,A,4,F
1,F,6,D,2,G,3,H,4,E,5,I"""),
    10: ("0A 0B 1C 1D 2E 2F 3G 3H 4I 4J", """1,F,5,C,2,G,4,D,3,E,6,H
0,E,4,F,3,J,5,G,6,I,2,H
0,G,1,I,3,A,4,H,5,B,6,J
0,D,2,J,1,B,4,C,6,A,5,I
0,C,3,B,2,A,1,E,5,D,6,F"""),
    11: ("0A 0B 0C 0D 0E 1F 2G 3H 4I 5J 6K", """0,F,5,E,6,B,3,D,1,A,4,C,2,I
0,G,1,B,2,A,5,C,3,E,4,D,6,J
0,H,4,B,5,D,2,E,1,C,6,A,3,K
1,I,5,G,3,J,4,F,6,H,2,K
1,H,5,K,4,G,6,I,3,F,2,J"""),
}


def normalize_vertex(vertex):
    if isinstance(vertex, str):
        return LEAF_NAMES.index(vertex)
    assert vertex >= 1000
    return vertex - 1000


def edge_list(walk):
    assert len(walk) >= 4 and len(walk) % 2 == 0
    assert len(set(walk)) == len(walk), 'cycle repeats a vertex'
    assert all(walk[i] in HUBS for i in range(0, len(walk), 2))
    assert all(isinstance(walk[i], str) or walk[i] >= 1000
               for i in range(1, len(walk), 2))
    leaf_ids = [normalize_vertex(walk[i]) for i in range(1, len(walk), 2)]
    assert len(set(leaf_ids)) == len(leaf_ids), 'cycle repeats a leaf'
    result = []
    for i, (a, b) in enumerate(zip(walk, walk[1:] + walk[:1])):
        hub, leaf = (a, b) if i % 2 == 0 else (b, a)
        result.append((hub, normalize_vertex(leaf)))
    assert len(set(result)) == len(result)
    return result


def block_cycles(start):
    """Three Hamilton cycles on seven fresh leaves from paired offsets."""
    result = []
    for offset in (1, 3, 5):
        walk = []
        for j in range(7):
            hub = (-j) % 7
            walk.extend((hub, 1000 + start + (hub + offset) % 7))
        result.append(tuple(walk))
    return result


def parsed_seed(t):
    if t == 0:
        return [], []
    if t == 1:
        return [(hub, 0) for hub in HUBS], []
    if t == 7:
        return [(hub, hub) for hub in HUBS], block_cycles(0)
    if t == 8:
        return list(SINGLETONS_8), list(WALKS_8)
    if t == 12:
        singleton, cycles = parsed_seed(6)
        more_singleton = [(hub, leaf + 6) for hub, leaf in singleton]
        more_cycles = [tuple(vertex if i % 2 == 0 else
                             1000 + LEAF_NAMES.index(vertex) + 6
                             for i, vertex in enumerate(walk))
                       for walk in cycles]
        return singleton + more_singleton, cycles + more_cycles
    singles_text, walks_text = SEED_DATA[t]
    singleton = [(int(token[0]), LEAF_NAMES.index(token[1:]))
                 for token in singles_text.split()]
    cycles = [tuple(int(token) if i % 2 == 0 else token
                    for i, token in enumerate(line.split(',')))
              for line in walks_text.splitlines()]
    return singleton, cycles


def certificate(t):
    assert t >= 0
    if t >= 6:
        base = 6 + (t - 6) % 7
        q = (t - base) // 7
    else:
        base, q = t, 0
    singleton, cycles = parsed_seed(base)
    for block in range(q):
        start = base + 7 * block
        singleton.extend((i, start + i) for i in HUBS)
        cycles.extend(block_cycles(start))
    seen = {}
    for index, edge in enumerate(singleton):
        assert edge not in seen
        seen[edge] = ('singleton', index)
    for index, walk in enumerate(cycles):
        for edge in edge_list(walk):
            assert edge not in seen, (q, index, edge, seen.get(edge))
            seen[edge] = ('cycle', index)
    expected = {(hub, leaf) for hub in HUBS for leaf in range(t)}
    assert set(seen) == expected, (q, sorted(expected - set(seen)))
    expected_parts = (0, 7, 5, 10, 7, 10)[t] if t <= 5 else t + (3 * t + 6) // 7
    assert len(singleton) + len(cycles) == expected_parts
    return seen


def make_svg(seen):
    colors = ('#ea8a6a', '#5eaab6', '#b590d1', '#96b96d')
    x0, y0, cell = 106, 115, 61
    pieces = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 690 630" '
        'role="img" aria-label="Seven by eight spoke matrix partitioned into four cycles and eight singleton spokes">',
        '<rect width="690" height="630" fill="#f7f5ef"/>',
        '<text x="34" y="43" fill="#21313d" font-family="sans-serif" font-size="24" font-weight="700">Seven hubs, eight leaves, twelve parts</text>',
        '<text x="34" y="67" fill="#4c5962" font-family="sans-serif" font-size="13">Each colored cell is one spoke. Four cycles cover the colors; eight dark cells stand alone.</text>',
    ]
    for leaf in range(8):
        x = x0 + leaf * cell + cell / 2
        pieces.append(f'<text x="{x:.1f}" y="101" text-anchor="middle" fill="#233847" font-family="sans-serif" font-size="15" font-weight="700">{LEAF_NAMES[leaf]}</text>')
    for hub in HUBS:
        y = y0 + hub * cell + cell / 2
        pieces.append(f'<text x="75" y="{y + 5:.1f}" text-anchor="middle" fill="#233847" font-family="sans-serif" font-size="15" font-weight="700">{hub}</text>')
        for leaf in range(8):
            kind, index = seen[(hub, leaf)]
            fill = '#263e50' if kind == 'singleton' else colors[index]
            x = x0 + leaf * cell + 3
            yy = y0 + hub * cell + 3
            label = '•' if kind == 'singleton' else str(index + 1)
            pieces.append(f'<rect x="{x}" y="{yy}" width="55" height="55" rx="9" fill="{fill}"/>')
            pieces.append(f'<text x="{x + 27.5:.1f}" y="{yy + 35}" text-anchor="middle" fill="white" font-family="sans-serif" font-size="18" font-weight="700">{escape(label)}</text>')
    pieces.extend([
        '<text x="34" y="579" fill="#4c5962" font-family="sans-serif" font-size="13">Cycle labels 1–4 are complete simple 12-cycles. The dark singleton pattern is 2+2+2+2 across four hubs.</text>',
        '<text x="34" y="602" fill="#21313d" font-family="sans-serif" font-size="14" font-weight="700">8 singletons + 4 cycles = 12, meeting the parity/capacity lower bound.</text>',
        '</svg>',
    ])
    return '\n'.join(pieces) + '\n'


def main():
    base = certificate(8)
    for t in range(0, 100):
        certificate(t)
    target = Path(__file__).with_name('art') / 'bipartite_seven_eight.svg'
    target.write_text(make_svg(base))
    print('All K_(7,t) seed partitions and lifts checked through t=99.')
    print('For t>=6, every certificate attains t+ceil(3t/7).')
    print(f'Wrote {target}.')


if __name__ == '__main__':
    main()
