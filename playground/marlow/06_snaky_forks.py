"""Enumerate the three-blocker exception in Snaky's four-in-a-row lemma.

Run: python3 -I playground/marlow/06_snaky_forks.py
This checks a local proof case split, not the paper's 21-move strategy.
"""

from collections import Counter
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
SNAKY = frozenset({(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)})
ROW = frozenset((x, 0) for x in range(4))
Q = tuple((x, y) for x in range(-3, 7) for y in range(-4, 5))
BREAKER_CELLS = tuple(cell for cell in Q if cell not in ROW)


def transformed(shape, swap, flip_x, flip_y):
    points = []
    for x, y in shape:
        if swap:
            x, y = y, x
        points.append(((-x if flip_x else x), (-y if flip_y else y)))
    return frozenset(points)


def contains_snaky(points):
    """Check copies using all eight signed coordinate permutations."""
    for swap in (0, 1):
        for flip_x in (0, 1):
            for flip_y in (0, 1):
                shape = transformed(SNAKY, swap, flip_x, flip_y)
                for x, y in points:
                    for u, v in shape:
                        copy = {(a + x - u, b + y - v) for a, b in shape}
                        if copy <= points:
                            return True
    return False


def triple(endpoint, side):
    return frozenset((x, side) for x in (endpoint - 1, endpoint, endpoint + 1))


def fork_geometry():
    five = frozenset((x, 0) for x in range(5))
    for endpoint in (0, 4):
        for side in (-1, 1):
            center = (endpoint, side)
            assert not contains_snaky(five | {center})
            for outer in ((endpoint - 1, side), (endpoint + 1, side)):
                assert contains_snaky(five | {center, outer})


def reflected(blockers, horizontal, vertical):
    return frozenset((3 - x if horizontal else x, -y if vertical else y)
                     for x, y in blockers)


def classify():
    left = tuple(triple(endpoint, side) for endpoint in (-1, 3) for side in (-1, 1))
    right = tuple(triple(endpoint, side) for endpoint in (0, 4) for side in (-1, 1))
    zones = (frozenset((x, y) for x in (-1, 0, 1) for y in range(-4, 5) if y),
             frozenset((x, y) for x in (2, 3, 4) for y in range(-4, 5) if y))
    counts = Counter()
    exceptional = set()
    for size in range(4):
        for choice in combinations(BREAKER_CELLS, size):
            blockers = frozenset(choice)
            extensions = (int((-1, 0) in blockers), int((4, 0) in blockers))
            if extensions == (1, 1):
                assert any(not blockers & zone for zone in zones)
                counts['both extensions blocked'] += 1
            elif sum(extensions) == 1:
                available = right if extensions[0] else left
                assert sum(not blockers & t for t in available) >= 2
                counts['one extension blocked'] += 1
            else:
                clean_left = sum(not blockers & t for t in left)
                clean_right = sum(not blockers & t for t in right)
                if max(clean_left, clean_right) >= 2:
                    counts['easy fork'] += 1
                else:
                    assert size == 3 and clean_left == clean_right == 1
                    assert all(x in (-1, 0, 3, 4) and y in (-1, 1)
                               for x, y in blockers)
                    exceptional.add(blockers)
                    counts['three-blocker exception'] += 1
    assert sum(counts.values()) == 1 + 86 + 3655 + 102340 == 106082
    assert counts == {'both extensions blocked': 85,
                      'one extension blocked': 7142,
                      'easy fork': 98823,
                      'three-blocker exception': 32}
    orbits = []
    while exceptional:
        seed = min(exceptional, key=lambda b: tuple(sorted(b)))
        orbit = {reflected(seed, h, v) for h in (0, 1) for v in (0, 1)}
        assert len(orbit) == 4 and orbit <= exceptional
        exceptional -= orbit
        orbits.append(min(orbit, key=lambda b: tuple(sorted(b))))
    assert len(orbits) == 8
    return counts, orbits


def drawing(path, orbits):
    """One representative of each reflection orbit."""
    ink, blocker, paper = '#242320', '#bc6d3a', '#f7f4ed'
    parts = [f'<rect width="1000" height="570" fill="{paper}"/>',
             f'<text x="500" y="42" text-anchor="middle" font-size="27" fill="{ink}">When both easy forks fail</text>',
             f'<text x="500" y="69" text-anchor="middle" font-size="16" fill="{ink}">32 three-cell Breaker placements · eight reflection orbits</text>']
    for index, blockers in enumerate(orbits):
        col, row = index % 4, index // 4
        ox, oy = 30 + col * 242, 100 + row * 220
        parts.append(f'<rect x="{ox}" y="{oy}" width="220" height="198" rx="8" fill="#ebe6d8"/>')
        parts.append(f'<text x="{ox+16}" y="{oy+26}" font-size="16" fill="{ink}">orbit {index+1} · 4</text>')
        for y in (-1, 0, 1):
            for x in range(-1, 5):
                cx, cy = ox + 27 + (x + 1) * 31, oy + 73 + (1 - y) * 35
                parts.append(f'<rect x="{cx-12}" y="{cy-12}" width="24" height="24" rx="3" fill="#fffdf8" stroke="#cfc8b9"/>')
                if (x, y) in ROW:
                    parts.append(f'<circle cx="{cx}" cy="{cy}" r="8" fill="{ink}"/>')
                if (x, y) in blockers:
                    parts.append(f'<path d="M{cx-7} {cy-7}L{cx+7} {cy+7} M{cx+7} {cy-7}L{cx-7} {cy+7}" stroke="{blocker}" stroke-width="4" stroke-linecap="round"/>')
    parts.extend([
        f'<circle cx="65" cy="551" r="6" fill="{ink}"/>',
        f'<text x="80" y="556" font-size="14" fill="{ink}">Maker four-cell row</text>',
        f'<path d="M315 545L327 557 M327 545L315 557" stroke="{blocker}" stroke-width="3"/>',
        f'<text x="339" y="556" font-size="14" fill="{ink}">Breaker cell</text>',
        f'<text x="950" y="556" text-anchor="end" font-size="12" fill="{ink}">Fork tactic: Snaky paper, §5</text>',
    ])
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 570" width="1000" height="570" role="img" aria-label="Eight reflection orbits of three-cell Breaker patterns obstructing both immediate Snaky forks" font-family="Georgia, serif">' + ''.join(parts) + '</svg>\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)


def main():
    fork_geometry()
    counts, orbits = classify()
    drawing(HERE / 'art/snaky_four_row.svg', orbits)
    print('All local fork target pairs are Snaky copies.')
    print(dict(counts))
    print('Exceptional orbits:', len(orbits), 'each of size 4')


if __name__ == '__main__':
    main()
