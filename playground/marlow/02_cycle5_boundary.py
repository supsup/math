"""Enumerate the C5/K3 Ramsey boundary, one vertex at a time.

Red C5 means a five-cycle, not necessarily induced. Blue K3 means three
vertices all of whose edges are blue. Pure standard-library Python.
Run: python3 -I playground/marlow/02_cycle5_boundary.py
"""

from collections import Counter
from itertools import combinations, permutations
from pathlib import Path


HERE = Path(__file__).resolve().parent


def edge_index(n):
    return {edge: i for i, edge in enumerate(combinations(range(n), 2))}


def forbidden(n):
    idx = edge_index(n)
    cycles = set()
    for vertices in combinations(range(n), 5):
        for order in permutations(vertices[1:]):
            walk = (vertices[0],) + order
            cycles.add(sum(1 << idx[tuple(sorted((walk[i], walk[(i + 1) % 5])))]
                           for i in range(5)))
    triangles = {sum(1 << idx[edge] for edge in combinations(vertices, 2))
                 for vertices in combinations(range(n), 3)}
    assert len(cycles) == 12 * len(list(combinations(range(n), 5)))
    return tuple(cycles), tuple(triangles)


def safe(mask, cycles, triangles):
    return not any(mask & cycle == cycle for cycle in cycles) and not any(
        mask & triangle == 0 for triangle in triangles)


def extend(safe_old, n):
    old = edge_index(n - 1)
    new = edge_index(n)
    cycles, triangles = forbidden(n)
    survivors = []
    for mask in safe_old:
        base = sum(1 << new[edge] for edge, bit in old.items() if mask & (1 << bit))
        for attachment in range(1 << (n - 1)):
            candidate = base | sum(1 << new[(v, n - 1)] for v in range(n - 1)
                                   if attachment & (1 << v))
            if safe(candidate, cycles, triangles):
                survivors.append(candidate)
    return survivors


def red_edges(mask, n):
    return {edge for edge, bit in edge_index(n).items() if mask & (1 << bit)}


def classify_eight(mask):
    """Find the two red K4s and return their count of red cross-edges."""
    red = red_edges(mask, 8)
    universe = set(range(8))
    matches = []
    for first in combinations(range(8), 4):
        left = set(first)
        if 0 not in left:  # one representative of each unordered partition
            continue
        right = universe - left
        if not all(edge in red for edge in combinations(sorted(left), 2)):
            continue
        if not all(edge in red for edge in combinations(sorted(right), 2)):
            continue
        bridges = sum(tuple(sorted((a, b))) in red for a in left for b in right)
        matches.append(bridges)
    assert len(matches) == 1, (mask, matches)
    assert matches[0] <= 1, (mask, matches)
    return matches[0]


def independent_check(mask, n):
    """Adjacency-matrix check for survivors, separate from pattern masks."""
    red = red_edges(mask, n)

    def edge(a, b):
        return tuple(sorted((a, b))) in red

    for triangle in combinations(range(n), 3):
        if not any(edge(a, b) for a, b in combinations(triangle, 2)):
            return False
    for vertices in combinations(range(n), 5):
        for order in permutations(vertices[1:]):
            walk = (vertices[0],) + order
            if all(edge(walk[i], walk[(i + 1) % 5]) for i in range(5)):
                return False
    return True


def drawing(path, types, counts):
    """Two isomorphism types; count labels come from the enumeration."""
    ink, red, blue, paper = '#242320', '#ad4d35', '#718aa0', '#f7f4ed'
    parts = [f'<rect width="1000" height="510" fill="{paper}"/>',
             f'<text x="500" y="42" text-anchor="middle" font-size="25" fill="{ink}">The next rung: eight vertices</text>',
             f'<text x="500" y="70" text-anchor="middle" font-size="15" fill="{ink}">No red 5-cycle · No blue triangle</text>']

    def panel(x0, bridge_count):
        # Each K4 is a diamond, so all six red edges are visible.
        centers = ((x0 + 115, 171), (x0 + 355, 171))
        offsets = ((-47, 0), (0, -48), (47, 0), (0, 48))
        points = {4 * side + i: (cx + dx, cy + dy)
                  for side, (cx, cy) in enumerate(centers)
                  for i, (dx, dy) in enumerate(offsets)}
        bridge = (2, 4)
        for a in range(4):
            for b in range(4, 8):
                if bridge_count and (a, b) == bridge:
                    continue
                x1, y1 = points[a]
                x2, y2 = points[b]
                parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{blue}" stroke-width="1.1" opacity="0.36"/>')
        for side in (range(4), range(4, 8)):
            for a, b in combinations(side, 2):
                x1, y1 = points[a]
                x2, y2 = points[b]
                parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{red}" stroke-width="3.6"/>')
        if bridge_count:
            x1, y1 = points[bridge[0]]
            x2, y2 = points[bridge[1]]
            parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{red}" stroke-width="3.6"/>')
        for k, (x, y) in points.items():
            parts.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{paper}" stroke="{ink}" stroke-width="1.5"/>')
            parts.append(f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="11" fill="{ink}">{k + 1}</text>')
        title = 'one red bridge' if bridge_count else 'no red bridge'
        parts.append(f'<text x="{x0 + 235}" y="280" text-anchor="middle" font-size="20" fill="{ink}">{title}</text>')
        parts.append(f'<text x="{x0 + 235}" y="307" text-anchor="middle" font-size="16" fill="{ink}">{types[bridge_count]} labelled colourings</text>')

    panel(15, 0)
    panel(515, 1)
    parts.append(f'<line x1="55" y1="343" x2="945" y2="343" stroke="{blue}" opacity="0.5"/>')
    notes = (
        'Every surviving K8 colouring has this shape. This classification is exhaustive by code,',
        f'not a new general proof: {counts[5]} → {counts[6]} → {counts[7]} → {counts[8]} safe labelled colourings at K5–K8.',
        f'A ninth vertex has no safe attachment among the {counts[8]} × {1 << 8} possibilities.',
        'The two red K4s contain no 5-cycle; one bridge cannot close a cycle across them.'
    )
    for i, line in enumerate(notes):
        parts.append(f'<text x="61" y="{378 + 27 * i}" font-size="16" fill="{ink}">{line}</text>')
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 510" width="1000" height="510" role="img" aria-label="Two surviving types for the C5 K3 Ramsey boundary" font-family="Georgia, serif">' + ''.join(parts) + '</svg>\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)


def main():
    cycles5, triangles5 = forbidden(5)
    survivors = [mask for mask in range(1 << 10) if safe(mask, cycles5, triangles5)]
    counts = {5: len(survivors)}
    for n in (6, 7, 8):
        survivors = extend(survivors, n)
        counts[n] = len(survivors)
    assert counts == {5: 170, 6: 475, 7: 945, 8: 595}, counts
    assert all(independent_check(mask, 8) for mask in survivors)
    types = Counter(classify_eight(mask) for mask in survivors)
    assert types == {0: 35, 1: 560}, types
    assert not extend(survivors, 9)
    drawing(HERE / 'art/cycle5_boundary.svg', types, counts)
    print('safe labelled colorings by order:', counts)
    print('K8 types, red cross-edges:', dict(sorted(types.items())))
    print('K9 extensions surviving: 0 of', len(survivors) * 256)
    print('R(C5,K3)=9 verified in this finite domain; general theorem untested')


if __name__ == '__main__':
    main()
