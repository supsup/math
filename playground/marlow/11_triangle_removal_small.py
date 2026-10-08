"""Exact terminal laws of uniform random triangle removal on K_3..K_7.

Run: python3 -I playground/marlow/11_triangle_removal_small.py
Each step chooses uniformly among triangles present in the current graph.
"""

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED = {
    3: {0: Fraction(1)},
    4: {3: Fraction(1)},
    5: {4: Fraction(1)},
    6: {3: Fraction(9, 10), 9: Fraction(1, 10)},
    7: {0: Fraction(1125, 4004), 6: Fraction(2879, 4004)},
}
EXPECTED_STATES = {3: 2, 4: 5, 5: 26, 6: 256, 7: 4972}
EXPECTED_TERMINAL_MASKS = {3: 1, 4: 4, 5: 15, 6: 25, 7: 421}


def shape_check(n, mask, edges):
    degrees = [0] * n
    for i, (u, v) in enumerate(edges):
        if mask & (1 << i):
            degrees[u] += 1
            degrees[v] += 1
    degrees.sort()
    count = bin(mask).count('1')
    expected_degrees = {
        (3, 0): [0, 0, 0],
        (4, 3): [1, 1, 1, 3],
        (5, 4): [0, 2, 2, 2, 2],
        (6, 3): [1] * 6,
        (6, 9): [3] * 6,
        (7, 0): [0] * 7,
        (7, 6): [0] + [2] * 6,
    }
    assert degrees == expected_degrees[(n, count)]


def exact_law(n):
    edges = list(combinations(range(n), 2))
    edge_id = {e: i for i, e in enumerate(edges)}
    triangles = [sum(1 << edge_id[e] for e in combinations(vertices, 2))
                 for vertices in combinations(range(n), 3)]
    terminal_masks = set()

    @lru_cache(None)
    def law(mask):
        available = [triangle for triangle in triangles
                     if mask & triangle == triangle]
        if not available:
            terminal_masks.add(mask)
            shape_check(n, mask, edges)
            return ((bin(mask).count('1'), Fraction(1)),)
        answer = defaultdict(Fraction)
        weight = Fraction(1, len(available))
        for triangle in available:
            for final_edges, chance in law(mask ^ triangle):
                answer[final_edges] += weight * chance
        return tuple(sorted(answer.items()))

    result = dict(law((1 << len(edges)) - 1))
    assert result == EXPECTED[n]
    assert sum(result.values()) == 1
    assert law.cache_info().currsize == EXPECTED_STATES[n]
    assert len(terminal_masks) == EXPECTED_TERMINAL_MASKS[n]
    return result, law.cache_info().currsize, len(terminal_masks)


def draw(path, laws):
    ink, muted, paper = '#242320', '#625e57', '#f7f4ed'
    blue, copper = '#586aa2', '#ba7550'
    parts = [f'<rect width="980" height="500" fill="{paper}"/>',
             f'<text x="42" y="55" font-size="28" fill="{ink}">Where the last edges land</text>',
             f'<text x="42" y="85" font-size="16" fill="{muted}">Exact terminal laws for uniform triangle removal on two complete graphs</text>']
    rows = [
        (6, 155, [(3, 'perfect matching', blue), (9, 'K₃,₃', copper)]),
        (7, 330, [(0, 'empty leave', blue), (6, 'six-cycle + isolated vertex', copper)]),
    ]
    for n, top, outcomes in rows:
        parts.append(f'<text x="43" y="{top}" font-size="23" fill="{ink}">K{n}</text>')
        parts.append(f'<text x="105" y="{top}" font-size="15" fill="{muted}">start: {n*(n-1)//2} edges</text>')
        cursor = 42
        for count, label, color in outcomes:
            p = laws[n][count]
            width = 875 * float(p)
            parts.append(f'<rect x="{cursor:.2f}" y="{top+25}" width="{width:.2f}" height="40" rx="5" fill="{color}"/>')
            cursor += width
        for j, (count, label, color) in enumerate(outcomes):
            x = 44 + j * 445
            p = laws[n][count]
            parts.append(f'<circle cx="{x+8}" cy="{top+97}" r="6" fill="{color}"/>')
            parts.append(f'<text x="{x+23}" y="{top+103}" font-size="17" fill="{ink}">{label}</text>')
            parts.append(f'<text x="{x+23}" y="{top+127}" font-size="15" fill="{muted}">F={count} · {p} · {100*float(p):.1f}%</text>')
    parts.append(f'<text x="43" y="471" font-size="14" fill="{muted}">A finite exact computation. The paper’s 1/(2√2) constant is an n→∞ statement.</text>')
    parts.append(f'<text x="936" y="471" text-anchor="end" font-size="12" fill="{muted}">Marlow · family 188</text>')
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 500" width="980" height="500" role="img" aria-label="Exact terminal probabilities for triangle removal from K6 and K7" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n'
    path.write_text(svg)


def main():
    laws = {}
    for n in range(3, 8):
        result, states, terminal = exact_law(n)
        laws[n] = result
        print(f'n={n}: {result}; reachable states={states}; terminal labelled graphs={terminal}')
    draw(HERE / 'art/triangle_removal_small.svg', laws)
    print('Generated the exact terminal-law diagram.')


if __name__ == '__main__':
    main()
