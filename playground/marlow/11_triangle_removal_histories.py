"""A second exact computation of the empty-leave probability on K7.

Run: python3 -I playground/marlow/11_triangle_removal_histories.py
Enumerate exact covers by seven triangles, then weight every removal order.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from math import prod


N = 7
EDGES = tuple(combinations(range(N), 2))
EDGE_ID = {edge: i for i, edge in enumerate(EDGES)}
TRIANGLES = tuple((vertices,
                   sum(1 << EDGE_ID[edge] for edge in combinations(vertices, 2)))
                  for vertices in combinations(range(N), 3))
BY_EDGE = [tuple(j for j, (_, mask) in enumerate(TRIANGLES)
                 if mask & (1 << i)) for i in range(len(EDGES))]
FULL = (1 << len(EDGES)) - 1


def exact_covers():
    covers = []

    def search(remaining, selected):
        if not remaining:
            assert len(selected) == 7
            covers.append(tuple(selected))
            return
        least_edge = (remaining & -remaining).bit_length() - 1
        for index in BY_EDGE[least_edge]:
            triangle_mask = TRIANGLES[index][1]
            if remaining & triangle_mask == triangle_mask:
                search(remaining ^ triangle_mask, selected + [index])

    search(FULL, [])
    assert len(covers) == len({frozenset(cover) for cover in covers}) == 30
    return covers


def count_histories(covers):
    patterns = Counter()
    geometric = Counter()
    for cover in covers:
        for order in permutations(cover):
            remaining = FULL
            available_counts = []
            for index in order:
                available_counts.append(sum(
                    triangle & remaining == triangle
                    for _, triangle in TRIANGLES))
                triangle = TRIANGLES[index][1]
                assert remaining & triangle == triangle
                remaining ^= triangle
            assert remaining == 0
            pattern = tuple(available_counts)
            patterns[pattern] += 1
            first_three = set.intersection(
                *(set(TRIANGLES[index][0]) for index in order[:3]))
            last_three = set.intersection(
                *(set(TRIANGLES[index][0]) for index in order[4:]))
            assert not (first_three and last_three)
            kind = ('first three concurrent' if first_three else
                    'last three concurrent' if last_three else 'generic')
            geometric[(kind, pattern)] += 1
    assert sum(patterns.values()) == 30 * 5040 == 151200
    assert patterns == {
        (35, 22, 13, 7, 4, 2, 1): 90720,
        (35, 22, 13, 8, 4, 2, 1): 30240,
        (35, 22, 13, 7, 3, 2, 1): 30240,
    }
    assert geometric == {
        ('generic', (35, 22, 13, 7, 4, 2, 1)): 90720,
        ('first three concurrent', (35, 22, 13, 8, 4, 2, 1)): 30240,
        ('last three concurrent', (35, 22, 13, 7, 3, 2, 1)): 30240,
    }
    chance = sum((Fraction(count, prod(pattern))
                  for pattern, count in patterns.items()), Fraction(0))
    assert chance == Fraction(1125, 4004)
    return patterns, chance


def main():
    covers = exact_covers()
    patterns, chance = count_histories(covers)
    print('labelled Steiner completions:', len(covers))
    print('ordered full-removal histories:', sum(patterns.values()))
    for pattern, count in sorted(patterns.items()):
        print(count, pattern, 'weight contribution', Fraction(count, prod(pattern)))
    print('P(empty terminal leave on K7) =', chance)


if __name__ == '__main__':
    main()
