"""Explicit permutation-to-e-shape witness for naturally labeled paths.

Run: python3 -I playground/marlow/51_path_binary_witness.py
"""

from collections import Counter
from itertools import permutations, product
from math import comb


def permutation(bits):
    """The unique admissible path permutation with edge-inversion bits."""
    word = [1]
    for vertex, bit in enumerate(bits, start=2):
        if bit:
            word.insert(word.index(vertex - 1), vertex)
        else:
            word.append(vertex)
    return tuple(word)


def admissible(word):
    return all(a < b or a == b + 1 for a, b in zip(word, word[1:]))


def edge_inversion_bits(word):
    positions = {value: index for index, value in enumerate(word)}
    return tuple(int(positions[vertex + 1] < positions[vertex])
                 for vertex in range(1, len(word)))


def shape(bits):
    """Append zero, then take lengths of initial 0-run and 1^+0^+ blocks."""
    padded = tuple(bits) + (0,)
    lengths = []
    cursor = 0
    while cursor < len(padded) and padded[cursor] == 0:
        cursor += 1
    if cursor:
        lengths.append(cursor)
    while cursor < len(padded):
        start = cursor
        assert padded[cursor] == 1
        while cursor < len(padded) and padded[cursor] == 1:
            cursor += 1
        assert cursor < len(padded) and padded[cursor] == 0
        while cursor < len(padded) and padded[cursor] == 0:
            cursor += 1
        lengths.append(cursor - start)
    assert sum(lengths) == len(padded)
    return tuple(sorted(lengths, reverse=True))


def witness_coefficients(n):
    result = Counter()
    for bits in product((0, 1), repeat=n - 1):
        result[shape(bits), sum(bits)] += 1
    return result


def direct_specialization(n, colors):
    """Count actual proper path colorings with colors 0,...,colors-1."""
    result = Counter()
    for coloring in product(range(colors), repeat=n):
        if any(a == b for a, b in zip(coloring, coloring[1:])):
            continue
        ascents = sum(a < b for a, b in zip(coloring, coloring[1:]))
        result[ascents] += 1
    return result


def from_witness(coefficients, colors):
    """Evaluate e_k at an alphabet of `colors` ones."""
    result = Counter()
    for (partition, degree), count in coefficients.items():
        value = count
        for part in partition:
            value *= comb(colors, part) if part <= colors else 0
        result[degree] += value
    return +result


def main():
    for n in range(1, 8):
        observed = {word for word in permutations(range(1, n + 1))
                    if admissible(word)}
        modeled = {permutation(bits) for bits in product((0, 1), repeat=n - 1)}
        assert modeled == observed and len(modeled) == 2 ** (n - 1)
        for word in observed:
            bits = edge_inversion_bits(word)
            assert permutation(bits) == word
        if n <= 6:
            coefficients = witness_coefficients(n)
            for colors in range(1, n + 1):
                assert from_witness(coefficients, colors) == direct_specialization(n, colors)

    n = 6
    coefficients = witness_coefficients(n)
    print('P6 nonzero e-shape coefficients:')
    for partition in sorted({partition for partition, _ in coefficients}, reverse=True):
        row = {degree: count for (shape_, degree), count in coefficients.items()
               if shape_ == partition}
        print(f'  {partition}: {dict(sorted(row.items()))}')
    examples = [(bits, permutation(bits))
                for bits in product((0, 1), repeat=5)
                if shape(bits) == (2, 2, 2)]
    assert examples == [((0, 0, 1, 0, 1), (1, 2, 4, 3, 6, 5)),
                        ((1, 0, 1, 0, 1), (2, 1, 4, 3, 6, 5))]
    print('P6 e_(2,2,2) witnesses:', examples)
    print('Admissible permutations checked to n=7; direct coloring'
          ' specializations checked to n=6.')


if __name__ == '__main__':
    main()
