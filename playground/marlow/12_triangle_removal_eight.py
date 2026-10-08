"""Exact terminal graph-shape law for uniform triangle removal on K8.

Run: python3 -I playground/marlow/12_triangle_removal_eight.py
Uses rational recursion over only the labelled graphs reachable from K8.
"""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 8
EDGES = tuple(combinations(range(N), 2))
EDGE_ID = {edge: i for i, edge in enumerate(EDGES)}
TRIANGLES = tuple(sum(1 << EDGE_ID[edge] for edge in combinations(vertices, 2))
                  for vertices in combinations(range(N), 3))
SHAPES = {
    (1,) * 8: 0,                         # perfect matching, F=4
    (1,) * 7 + (7,): 1,                 # star K_(1,7), F=7
    (1,) * 6 + (3, 5): 2,              # joined degree-5 and degree-3 centers
    (1,) * 5 + (3, 3, 3): 3,           # path of three degree-3 centers
}
NAMES = ('perfect matching', 'seven-edge star',
         'two-center tree', 'three-center tree')
EXPECTED_PROBABILITY = (
    Fraction(599217, 3203200),
    Fraction(1359, 553280),
    Fraction(570231, 3477760),
    Fraction(78694289, 121721600),
)
EXPECTED_TERMINAL_COUNTS = (105, 8, 840, 5040)


def terminal_type(mask):
    degrees = [0] * N
    for i, (u, v) in enumerate(EDGES):
        if mask & (1 << i):
            degrees[u] += 1
            degrees[v] += 1
    key = tuple(sorted(degrees))
    assert key in SHAPES, key
    result = SHAPES[key]
    assert bin(mask).count('1') == (4 if result == 0 else 7)
    return result


def exact_law():
    terminal_masks = set()

    @lru_cache(None)
    def law(mask):
        choices = [triangle for triangle in TRIANGLES
                   if mask & triangle == triangle]
        if not choices:
            terminal_masks.add(mask)
            kind = terminal_type(mask)
            return tuple(Fraction(i == kind) for i in range(4))
        totals = [Fraction(0) for _ in range(4)]
        for triangle in choices:
            child = law(mask ^ triangle)
            for i in range(4):
                totals[i] += child[i]
        return tuple(value / len(choices) for value in totals)

    result = law((1 << len(EDGES)) - 1)
    counts = Counter(terminal_type(mask) for mask in terminal_masks)
    assert result == EXPECTED_PROBABILITY
    assert sum(result) == 1
    assert law.cache_info().currsize == 196870
    assert tuple(counts[i] for i in range(4)) == EXPECTED_TERMINAL_COUNTS
    assert len(terminal_masks) == 5993
    return result, counts, law.cache_info().currsize


def draw(path, probabilities):
    ink, muted, paper = '#242320', '#625e57', '#f7f4ed'
    colors = ('#586aa2', '#aa6545', '#3e8b7f', '#8e729e')
    parts = [f'<rect width="980" height="620" fill="{paper}"/>',
             f'<text x="42" y="54" font-size="28" fill="{ink}">Four ways K₈ can finish</text>',
             f'<text x="42" y="82" font-size="16" fill="{muted}">Exact shape probabilities after uniform random triangle removal</text>',
             f'<text x="270" y="126" font-size="14" fill="{muted}">0%</text>',
             f'<text x="900" y="126" font-size="14" fill="{muted}">100%</text>']
    x0, scale = 265, 650
    for i, (name, p, color) in enumerate(zip(NAMES, probabilities, colors)):
        y = 157 + i * 103
        count = 4 if i == 0 else 7
        parts.append(f'<text x="43" y="{y+16}" font-size="17" fill="{ink}">{name}</text>')
        parts.append(f'<text x="43" y="{y+42}" font-size="14" fill="{muted}">F={count} · {EXPECTED_TERMINAL_COUNTS[i]:,} labelled leaves</text>')
        parts.append(f'<rect x="{x0}" y="{y}" width="{scale}" height="32" rx="5" fill="#e8e2d7"/>')
        width = scale * float(p)
        if i == 1:
            # A sub-2px bar is represented as a crisp vertical marker at its true endpoint.
            parts.append(f'<path d="M{x0+width:.3f} {y}V{y+32}" stroke="{color}" stroke-width="2"/>')
        else:
            parts.append(f'<rect x="{x0}" y="{y}" width="{width:.3f}" height="32" rx="5" fill="{color}"/>')
        parts.append(f'<text x="{x0+scale}" y="{y+55}" text-anchor="end" font-size="15" fill="{ink}">{p} · {100*float(p):.3f}%</text>')
    parts.append(f'<text x="42" y="587" font-size="14" fill="{muted}">The three seven-edge outcomes are trees. The star is only 0.246% of runs.</text>')
    parts.append(f'<text x="936" y="587" text-anchor="end" font-size="12" fill="{muted}">Marlow · family 188 · finite exact law</text>')
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 620" width="980" height="620" role="img" aria-label="Exact terminal shape probabilities for triangle removal from K8" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n'
    path.write_text(svg)


def main():
    probabilities, counts, states = exact_law()
    print('reachable labelled states:', states)
    for i, p in enumerate(probabilities):
        print(NAMES[i], 'terminal masks', counts[i], 'probability', p,
              'decimal', f'{float(p):.9f}')
    draw(HERE / 'art/triangle_removal_eight.svg', probabilities)
    print('Generated the K8 terminal-shape diagram.')


if __name__ == '__main__':
    main()
