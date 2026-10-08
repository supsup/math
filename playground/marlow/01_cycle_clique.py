"""The two extremal K6 colourings for R(C4,K3), checked exactly.

Red has no (not necessarily induced) four-cycle; blue has no triangle.
Run: python3 -I 01_cycle_clique.py -> art/cycle_clique.svg
Pure Python standard library, deterministic and finite. This checks only m=4,n=3
of the collection's cycle-clique Ramsey claim, not the general theorem.
"""

from itertools import combinations, permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent


def edge_index(n):
    return {e: i for i, e in enumerate(combinations(range(n), 2))}


def red_bit(index, a, b):
    return 1 << index[tuple(sorted((a, b)))]


def forbidden_masks(n):
    """Independently generated red C4 and all-blue K3 edge patterns."""
    index = edge_index(n)
    cycles = set()
    for vertices in combinations(range(n), 4):
        a, b, c, d = vertices
        for walk in ((a, b, c, d), (a, b, d, c), (a, c, b, d)):
            cycles.add(sum(red_bit(index, walk[i], walk[(i + 1) % 4]) for i in range(4)))
    triangles = set()
    for tri in combinations(range(n), 3):
        triangles.add(sum(red_bit(index, a, b) for a, b in combinations(tri, 2)))
    return cycles, triangles


def mask_valid(mask, cycles, triangles):
    return not any(mask & c == c for c in cycles) and not any(mask & t == 0 for t in triangles)


def direct_valid(mask, n):
    """Second check via adjacency and ordered walks, not pattern bit masks."""
    index = edge_index(n)
    adj = [[False] * n for _ in range(n)]
    for (a, b), i in index.items():
        adj[a][b] = adj[b][a] = bool(mask & (1 << i))
    for a, b, c in combinations(range(n), 3):
        if not adj[a][b] and not adj[a][c] and not adj[b][c]:
            return False
    for a, b, c, d in permutations(range(n), 4):
        if adj[a][b] and adj[b][c] and adj[c][d] and adj[d][a]:
            return False
    return True


def red_edges(mask, n):
    return {e for e, i in edge_index(n).items() if mask & (1 << i)}


def classify_six(mask):
    """Return number of cross-red edges for a pair of red triangles."""
    red = red_edges(mask, 6)
    vertices = set(range(6))
    for first in combinations(range(6), 3):
        A, B = set(first), vertices - set(first)
        if min(A) > min(B):
            continue
        if not all(e in red for e in combinations(sorted(A), 2)):
            continue
        if not all(e in red for e in combinations(sorted(B), 2)):
            continue
        cross = sum(tuple(sorted((a, b))) in red for a in A for b in B)
        if cross <= 1:
            return cross
    raise AssertionError('unclassified six-vertex counterexample')


def seven_extension_count(six_masks):
    """Every K7 restriction to its first six vertices must be in six_masks."""
    index7 = edge_index(7)
    cycles7, triangles7 = forbidden_masks(7)
    survivors = 0
    for six in six_masks:
        base = sum(red_bit(index7, a, b) for a, b in red_edges(six, 6))
        for extension in range(1 << 6):
            new_edges = sum(red_bit(index7, a, 6) for a in range(6) if extension & (1 << a))
            survivors += mask_valid(base | new_edges, cycles7, triangles7)
    return survivors


def drawing(path, counts):
    ink, red, blue, pale = '#242320', '#ad4d35', '#718aa0', '#f7f4ed'
    elements = [f'<rect width="1000" height="530" fill="{pale}"/>',
                f'<text x="500" y="44" text-anchor="middle" font-size="25" fill="{ink}">Two ways to delay a Ramsey collision</text>',
                f'<text x="500" y="72" text-anchor="middle" font-size="15" fill="{ink}">No red 4-cycle · No blue triangle · Six vertices</text>']

    def panel(x0, one_bridge):
        points = {0: (x0 + 75, 155), 1: (x0 + 155, 115), 2: (x0 + 155, 205),
                  3: (x0 + 285, 155), 4: (x0 + 365, 115), 5: (x0 + 365, 205)}
        left, right = (0, 1, 2), (3, 4, 5)
        bridge = (2, 3)
        for a in left:
            for b in right:
                if one_bridge and (a, b) == bridge:
                    continue
                xa, ya = points[a]
                xb, yb = points[b]
                elements.append(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="{blue}" stroke-width="1.5" opacity="0.43"/>')
        for tri in (left, right):
            for a, b in combinations(tri, 2):
                xa, ya = points[a]
                xb, yb = points[b]
                elements.append(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="{red}" stroke-width="4"/>')
        if one_bridge:
            xa, ya = points[bridge[0]]
            xb, yb = points[bridge[1]]
            elements.append(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="{red}" stroke-width="4"/>')
        for k, (px, py) in points.items():
            elements.append(f'<circle cx="{px}" cy="{py}" r="12" fill="{pale}" stroke="{ink}" stroke-width="1.7"/>')
            elements.append(f'<text x="{px}" y="{py + 5}" text-anchor="middle" font-size="13" fill="{ink}">{k + 1}</text>')
        title = 'one red bridge' if one_bridge else 'no red bridge'
        count = f'{counts[int(one_bridge)]} labelled colourings'
        elements.append(f'<text x="{x0 + 220}" y="258" text-anchor="middle" font-size="20" fill="{ink}">{title}</text>')
        elements.append(f'<text x="{x0 + 220}" y="281" text-anchor="middle" font-size="15" fill="{ink}">{count}</text>')

    panel(35, False)
    panel(525, True)
    elements.append(f'<line x1="55" y1="314" x2="945" y2="314" stroke="{blue}" stroke-width="1" opacity="0.5"/>')
    explanation = [
        'A red triangle must exist. Every outside vertex has at most one red neighbour in it,',
        'or those four vertices make a red 4-cycle. Two outside vertices cannot share a blue edge:',
        'a triangle vertex misses both in red and would close a blue triangle.',
        'So the other three vertices form a red triangle. Two red bridges would close a red 4-cycle.',
        'A seventh vertex makes the outside four a red K4, which already contains a 4-cycle.'
    ]
    for i, line in enumerate(explanation):
        elements.append(f'<text x="65" y="{347 + 28*i}" font-size="16" fill="{ink}">{line}</text>')
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 530" width="1000" height="530" role="img" aria-label="Two extremal cycle clique Ramsey colourings" font-family="Georgia, serif">' + ''.join(elements) + '</svg>\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)


def main():
    cycles6, triangles6 = forbidden_masks(6)
    safe = []
    for mask in range(1 << 15):
        fast = mask_valid(mask, cycles6, triangles6)
        assert fast == direct_valid(mask, 6), ('independent predicate disagreement', mask)
        if fast:
            safe.append(mask)
    counts = {0: 0, 1: 0}
    for mask in safe:
        counts[classify_six(mask)] += 1
    assert counts == {0: 10, 1: 90}
    assert len(safe) == 100
    assert seven_extension_count(safe) == 0
    output = HERE/'art/cycle_clique.svg'
    drawing(output, counts)
    print('K6 safe labelled colourings:', len(safe), 'types:', counts)
    print('K7 extensions of all safe K6 restrictions: 0 of', len(safe) * 64)
    print('R(C4,K3)=7 verified in this finite domain; general m,n theorem untested')
    print('art:', output)


if __name__ == '__main__':
    main()
