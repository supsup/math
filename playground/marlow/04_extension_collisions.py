"""Count forbidden copies when one vertex joins a cycle/triangle critical coloring.

For m=4,5,6 this enumerates every attachment to each of the two critical
isomorphism types. Red C_m copies are undirected cycle edge sets; blue K3
copies are vertex triples. A conditional count, not the unrestricted
threshold Ramsey multiplicity on all colorings of K_(2m-1).

Run: python3 -I playground/marlow/04_extension_collisions.py
"""

from itertools import combinations, permutations
from math import factorial
from pathlib import Path


HERE = Path(__file__).resolve().parent


def edge_index(n):
    return {edge: bit for bit, edge in enumerate(combinations(range(n), 2))}


def cycle_masks(n, m, index):
    """Each undirected C_m appears once as an edge set."""
    masks = set()
    for vertices in combinations(range(n), m):
        for tail in permutations(vertices[1:]):
            walk = (vertices[0],) + tail
            masks.add(sum(1 << index[tuple(sorted((walk[i], walk[(i + 1) % m])))]
                          for i in range(m)))
    assert len(masks) == len(list(combinations(range(n), m))) * factorial(m - 1) // 2
    return tuple(masks)


def triangle_masks(n, index):
    return tuple(sum(1 << index[edge] for edge in combinations(vertices, 2))
                 for vertices in combinations(range(n), 3))


def critical_base(m, bridge, index):
    k = m - 1
    red = [(a, b) for block in (range(k), range(k, 2 * k))
           for a, b in combinations(block, 2)]
    if bridge:
        red.append((k - 1, k))
    return sum(1 << index[edge] for edge in red)


def extension_stats(m, bridge, index, cycles, triangles):
    k = m - 1
    old_n = 2 * k
    base = critical_base(m, bridge, index)
    minimum = None
    achievers = 0
    witness = None
    zero_red = 0
    zero_blue = 0
    for attachment in range(1 << old_n):
        mask = base | sum(1 << index[(v, old_n)] for v in range(old_n)
                          if attachment & (1 << v))
        red_count = sum(mask & cycle == cycle for cycle in cycles)
        blue_count = sum(mask & triangle == 0 for triangle in triangles)
        total = red_count + blue_count
        zero_red += red_count == 0
        zero_blue += blue_count == 0
        if minimum is None or total < minimum:
            minimum = total
            achievers = 1
            witness = (attachment, red_count, blue_count)
        elif total == minimum:
            achievers += 1
    return {'minimum': minimum, 'achievers': achievers, 'witness': witness,
            'zero_red': zero_red, 'zero_blue': zero_blue,
            'extensions': 1 << old_n}


def drawing(path, results):
    """A compact chart of the exact conditional minima."""
    ink, red, blue, paper = '#242320', '#ad4d35', '#718aa0', '#f7f4ed'
    parts = [f'<rect width="960" height="540" fill="{paper}"/>',
             f'<text x="480" y="43" text-anchor="middle" font-size="25" fill="{ink}">The first unavoidable collisions</text>',
             f'<text x="480" y="70" text-anchor="middle" font-size="15" fill="{ink}">One vertex joins a critical colouring · red Cₘ copies + blue K₃ copies</text>']
    max_count = max(row['minimum'] for row in results.values())
    scale = 510 / max_count
    for row, m in enumerate(sorted({m for m, _ in results})):
        y = 135 + row * 112
        parts.append(f'<text x="83" y="{y + 30}" text-anchor="end" font-size="19" fill="{ink}">m = {m}</text>')
        for offset, bridge in ((0, 0), (33, 1)):
            value = results[(m, bridge)]['minimum']
            width = round(value * scale, 2)
            color = blue if bridge == 0 else red
            parts.append(f'<rect x="120" y="{y + offset}" width="{width}" height="26" rx="3" fill="{color}"/>')
            parts.append(f'<text x="{137 + width}" y="{y + offset + 19}" font-size="17" fill="{ink}">{value}</text>')
    parts.append(f'<rect x="120" y="475" width="15" height="15" fill="{blue}"/>')
    parts.append(f'<text x="143" y="488" font-size="14" fill="{ink}">two cliques, no bridge</text>')
    parts.append(f'<rect x="420" y="475" width="15" height="15" fill="{red}"/>')
    parts.append(f'<text x="443" y="488" font-size="14" fill="{ink}">two cliques, one red bridge</text>')
    parts.append(f'<text x="480" y="524" text-anchor="middle" font-size="12" fill="{blue}">Critical types: Radziszowski &amp; Jin (1994), Thm 3</text>')
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" width="960" height="540" role="img" aria-label="Minimum forbidden copies in one-vertex extensions of critical cycle triangle colorings" font-family="Georgia, serif">' + ''.join(parts) + '</svg>\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)


def main():
    expected = {(4, 0): 3, (4, 1): 2,
                (5, 0): 8, (5, 1): 9,
                (6, 0): 16, (6, 1): 16}
    results = {}
    for m in (4, 5, 6):
        n = 2 * m - 1
        index = edge_index(n)
        cycles = cycle_masks(n, m, index)
        triangles = triangle_masks(n, index)
        for bridge in (0, 1):
            results[(m, bridge)] = extension_stats(m, bridge, index, cycles, triangles)
    assert {key: item['minimum'] for key, item in results.items()} == expected
    drawing(HERE / 'art/extension_collisions.svg', results)
    for key, item in sorted(results.items()):
        print(key, item)
    print('For m>=6 the analytic bound is (m-2)^2; these checks cover m=6 only.')


if __name__ == '__main__':
    main()
