"""Verify an optimal K_(7,8) cycle/edge partition and its seven-leaf lift.

Run: python3 -I playground/marlow/20_bipartite_seven.py
Regenerates art/bipartite_seven_eight.svg from the checked certificate.
"""

from html import escape
from pathlib import Path


HUBS = tuple(range(7))
LEAF_NAMES = 'ABCDEFGH'
SINGLETONS_8 = ((0, 0), (0, 1), (1, 2), (1, 3),
                (2, 4), (2, 5), (3, 6), (3, 7))
WALKS_8 = (
    (1, 'E', 3, 'D', 4, 'F', 5, 'C', 6, 'G', 2, 'H'),
    (0, 'F', 3, 'A', 2, 'B', 4, 'G', 5, 'E', 6, 'H'),
    (0, 'D', 6, 'A', 5, 'H', 4, 'C', 3, 'B', 1, 'G'),
    (0, 'C', 2, 'D', 5, 'B', 6, 'F', 1, 'A', 4, 'E'),
)


def normalize_vertex(vertex):
    return LEAF_NAMES.index(vertex) if isinstance(vertex, str) else vertex


def cycle_edges(walk):
    assert len(walk) >= 4 and len(walk) % 2 == 0
    assert len(set(walk)) == len(walk), 'cycle repeats a vertex'
    assert all(isinstance(walk[i], int) == (i % 2 == 0)
               for i in range(len(walk))), 'cycle is not bipartite'
    result = []
    for a, b in zip(walk, walk[1:] + walk[:1]):
        hub, leaf = (a, b) if isinstance(a, int) else (b, a)
        assert hub in HUBS
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
            walk.extend((hub, start + (hub + offset) % 7))
        result.append(tuple(walk))
    return result


def edge_list(walk):
    if isinstance(walk[1], str):
        return cycle_edges(walk)
    assert len(walk) == 14 and len(set(walk)) == 14
    edges = []
    for a, b in zip(walk, walk[1:] + walk[:1]):
        hub, leaf = (a, b) if a < 7 else (b, a)
        assert hub in HUBS and leaf >= 8
        edges.append((hub, leaf))
    return edges


def certificate(q):
    assert q >= 0
    t = 8 + 7 * q
    singleton = list(SINGLETONS_8)
    cycles = list(WALKS_8)
    for block in range(q):
        start = 8 + 7 * block
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
    lower = t + (3 * t + 6) // 7
    assert len(singleton) + len(cycles) == lower == 12 + 10 * q
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
    base = certificate(0)
    for q in range(1, 7):
        certificate(q)
    target = Path(__file__).with_name('art') / 'bipartite_seven_eight.svg'
    target.write_text(make_svg(base))
    print('K_(7,8): 56 spokes covered exactly by eight singletons and four simple cycles.')
    print('Seven-leaf extension checked through q=6; all attain t+ceil(3t/7).')
    print(f'Wrote {target}.')


if __name__ == '__main__':
    main()
