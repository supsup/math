"""Finite cross-check of the prime-center inverse statement in note 50.

Run: python3 -I playground/marlow/50_fortyone_center_inverse.py
"""

from collections import Counter
from itertools import combinations_with_replacement


P = 41
SIZE = 19


def anchored_sets_avoiding_one():
    """All 19-sets containing zero and avoiding differences ±1.

    The 19 cyclic gaps each have length at least two and their total
    surplus beyond 38 is three.  A multiset of three gap indices records
    exactly one weak composition of that surplus into 19 positions.
    """
    for indices in combinations_with_replacement(range(SIZE), 3):
        extra = Counter(indices)
        centers = [0]
        for j in range(SIZE - 1):
            centers.append(centers[-1] + 2 + extra[j])
        assert centers[-1] + 2 + extra[SIZE - 1] == P
        yield tuple(centers)


def absent_magnitudes(centers):
    differences = {(a - b) % P for a in centers for b in centers}
    return tuple(d for d in range(1, (P - 1) // 2 + 1)
                 if d not in differences)


def main():
    for prime in (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47):
        k = (prime - 1) // 2
        size = k - 1
        for c in range(1, prime):
            centers = {(-2 * c * j) % prime for j in range(size)}
            assert len(centers) == size
            differences = {(a - b) % prime for a in centers for b in centers}
            absent = set(range(1, prime)) - differences
            assert absent == {c, -c % prime, 3 * c % prime, -3 * c % prime}

    counts = Counter()
    by_second = Counter()
    for centers in anchored_sets_avoiding_one():
        absent = absent_magnitudes(centers)
        assert 1 in absent
        assert len(absent) <= 2
        counts[len(absent)] += 1
        if len(absent) == 2:
            by_second[absent[1]] += 1
            # Equality in Cauchy-Davenport; the set must be an AP.
            assert any({(a + j * step) % P for j in range(SIZE)}
                       == set(centers)
                       for a in centers for step in range(1, P))
    assert counts == {1: 1292, 2: 38}
    assert by_second == {3: 19, 14: 19}

    witness = tuple(range(1, 20, 2)) + tuple(range(24, 41, 2))
    assert len(witness) == SIZE and len(set(witness)) == SIZE
    assert all((a - b) % P not in (1, 3, P - 1, P - 3)
               for a in witness for b in witness if a != b)
    print('Explicit progression checked at odd primes 7..47; 1330 normalized'
          ' 41-point 19-center sets checked. The two-class forbidden pairs'
          ' are {1,3} and {1,14}, equivalent by scaling.')


if __name__ == '__main__':
    main()
