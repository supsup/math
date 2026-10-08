"""Enumerate the ten-edge odd-degree triangle-free K8 leave candidates.

Run: python3 -I playground/marlow/12_triangle_removal_obstructions.py
The self-contained structural proof is in 12_triangle_removal_eight.md.
"""

from collections import defaultdict
from itertools import combinations


CORE_EDGES = tuple(combinations(range(6), 2))
FULL_EDGES = tuple(combinations(range(8), 2))
EDGE_ID = {e: i for i, e in enumerate(FULL_EDGES)}
CORE_ID = {e: i for i, e in enumerate(CORE_EDGES)}
CORE_TRIANGLES = tuple(sum(1 << CORE_ID[e] for e in combinations(triple, 2))
                       for triple in combinations(range(6), 3))
TRIANGLES = tuple(sum(1 << EDGE_ID[e] for e in combinations(triple, 2))
                  for triple in combinations(range(8), 3))
FULL_MASK = (1 << len(FULL_EDGES)) - 1

# Each three-digit word is one removed triangle; each two-digit word an H edge.
WITNESSES = {
    'matching': ('01 23 45 67', '034 027 056 125 246 147 357 136'),
    'star': ('01 02 03 04 05 06 07', '134 245 467 126 237 157 356'),
    'two-center tree': ('01 02 03 04 05 16 17',
                        '067 123 145 246 347 257 356'),
    'three-center tree': ('01 12 03 04 15 26 27',
                          '025 067 234 137 146 457 356'),
}


def core_graphs_by_degrees():
    result = defaultdict(list)
    for mask in range(1 << len(CORE_EDGES)):
        if bin(mask).count('1') not in (8, 9):
            continue
        if any(mask & tri == tri for tri in CORE_TRIANGLES):
            continue
        degrees = [0] * 6
        for i, (u, v) in enumerate(CORE_EDGES):
            if mask >> i & 1:
                degrees[u] += 1
                degrees[v] += 1
        result[tuple(degrees)].append(mask)
    return result


def full_mask(core_mask, extra_edges):
    edges = [e for i, e in enumerate(CORE_EDGES) if core_mask >> i & 1]
    edges.extend(extra_edges)
    assert len(edges) == 10
    return sum(1 << EDGE_ID[tuple(sorted(e))] for e in edges)


def triangle_partition_exists(mask):
    """Exact-cover check for the removed-edge complement, as a cross-check."""
    triangles = [tri for tri in TRIANGLES if tri & mask == tri]
    by_edge = [[] for _ in FULL_EDGES]
    for tri in triangles:
        for i in range(len(FULL_EDGES)):
            if tri >> i & 1:
                by_edge[i].append(tri)

    def search(remaining):
        if remaining == 0:
            return True
        best = None
        for i in range(len(FULL_EDGES)):
            if remaining >> i & 1:
                choices = [tri for tri in by_edge[i] if tri & remaining == tri]
                if best is None or len(choices) < len(best):
                    best = choices
                if not best:
                    return False
        return any(search(remaining ^ tri) for tri in best)

    return search(mask)


def main():
    cores = core_graphs_by_degrees()
    adjacent, pendant = 0, 0
    seen = set()
    # Fix the two degree-one vertices as 6 and 7; multiply by C(8,2) below.
    for core in cores[(3,) * 6]:
        leave = full_mask(core, ((6, 7),))
        seen.add(leave)
        assert not triangle_partition_exists(FULL_MASK ^ leave)
        adjacent += 1
    for a in range(6):
        for b in range(6):
            degrees = [3] * 6
            degrees[a] -= 1
            degrees[b] -= 1
            for core in cores[tuple(degrees)]:
                leave = full_mask(core, ((a, 6), (b, 7)))
                seen.add(leave)
                complement = FULL_MASK ^ leave
                assert a != b and complement >> EDGE_ID[tuple(sorted((a, b)))] & 1
                assert not any(tri & complement == tri and
                               tri >> EDGE_ID[tuple(sorted((a, b)))] & 1
                               for tri in TRIANGLES)
                assert not triangle_partition_exists(complement)
                pendant += 1
    assert adjacent == 10 and pendant == 180
    assert len(seen) == 190
    assert len(seen) * 28 == 5320
    for name, (edge_words, triangle_words) in WITNESSES.items():
        leave = sum(1 << EDGE_ID[tuple(map(int, word))]
                    for word in edge_words.split())
        removed = 0
        for word in triangle_words.split():
            triangle = sum(1 << EDGE_ID[e]
                           for e in combinations(tuple(map(int, word)), 2))
            assert not removed & triangle
            removed |= triangle
        assert leave & removed == 0 and leave | removed == FULL_MASK, name
    print('Fixed degree-one vertices 6,7: 10 adjacent + 180 pendant leaves.')
    print('All 190 complements fail triangle decomposition; 5,320 labelled leaves.')
    print('Four representative reachable terminal shapes have exact triangle covers.')


if __name__ == '__main__':
    main()
