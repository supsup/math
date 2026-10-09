"""Finite audit of the t=7 hub-block cycle certificates.

A row (H, L) denotes the alternating cycle
H[0], L[0], H[1], L[1], ..., H[-1], L[-1], H[0].
"""

from collections import Counter


SIX_CYCLES = [
    ([2, 4, 5, 1, 3, 0], [2, 6, 3, 5, 1, 4]),
    ([1, 2, 3, 4, 0, 5], [6, 3, 4, 0, 5, 2]),
    ([1, 5, 2, 4, 0, 3], [4, 1, 5, 3, 6, 0]),
]

ELEVEN_CYCLES = [
    ([8, 10, 3, 4, 9, 5, 0], [2, 1, 0, 5, 3, 6, 4]),
    ([1, 5, 9, 0, 6, 4, 10], [1, 4, 0, 3, 2, 6, 5]),
    ([6, 0, 5, 10, 1, 2, 7], [1, 2, 0, 3, 6, 4, 5]),
    ([3, 6, 1, 2, 8, 7], [6, 4, 0, 1, 3, 2]),
    ([4, 2, 9, 7, 8, 3], [3, 2, 1, 0, 5, 4]),
]


def edges_of_cycle(hubs, leaves):
    n = len(hubs)
    assert n == len(leaves) and n >= 2
    assert len(set(hubs)) == n and len(set(leaves)) == n
    return [(hubs[k], leaves[k]) for k in range(n)] + [
        (hubs[(k + 1) % n], leaves[k]) for k in range(n)
    ]


def seven_cycles():
    result = []
    for a in (1, 3, 5):
        hubs = [(-k) % 7 for k in range(7)]
        leaves = [(h + a) % 7 for h in hubs]
        result.append((hubs, leaves))
    return result


def audit_block(hub_count, cycles, lengths):
    assert [2 * len(h) for h, _ in cycles] == lengths
    universe = {(h, l) for h in range(hub_count) for l in range(7)}
    cycle_edges = [edge for h, l in cycles for edge in edges_of_cycle(h, l)]
    assert all(edge in universe for edge in cycle_edges)
    assert len(cycle_edges) == len(set(cycle_edges)), "cycle edges overlap"
    singleton_edges = universe - set(cycle_edges)
    assert len(singleton_edges) == hub_count
    assert Counter(h for h, _ in singleton_edges) == Counter(range(hub_count))
    assert len(cycle_edges) + len(singleton_edges) == len(universe)
    return singleton_edges


def main():
    seven_singletons = audit_block(7, seven_cycles(), [14] * 3)
    assert seven_singletons == {(h, h) for h in range(7)}

    six_singletons = audit_block(6, SIX_CYCLES, [12] * 3)
    assert six_singletons == {
        (0, 2), (1, 1), (2, 0), (3, 2), (4, 1), (5, 0)
    }

    eleven_singletons = audit_block(11, ELEVEN_CYCLES, [14] * 3 + [12] * 2)
    assert eleven_singletons == {
        (0, 5), (1, 2), (2, 5), (3, 3), (4, 1), (5, 5),
        (6, 0), (7, 6), (8, 6), (9, 6), (10, 4),
    }

    p = 12289
    seven_blocks = 1754
    assert p == 7 * seven_blocks + 11
    cycle_count = 3 * seven_blocks + len(ELEVEN_CYCLES)
    singleton_count = 7 * seven_blocks + len(eleven_singletons)
    assert singleton_count == p
    assert cycle_count == (3 * p + 6) // 7  # ceil(3p/7)
    assert singleton_count + cycle_count == 17556

    # Instantiate every block on disjoint hub sets, with the same seven leaves.
    all_parts = []
    for block in range(seven_blocks):
        offset = 7 * block
        for h, l in seven_cycles():
            all_parts.append([(offset + x, y) for x, y in edges_of_cycle(h, l)])
        for h, l in seven_singletons:
            all_parts.append([(offset + h, l)])
    offset = 7 * seven_blocks
    for h, l in ELEVEN_CYCLES:
        all_parts.append([(offset + x, y) for x, y in edges_of_cycle(h, l)])
    for h, l in eleven_singletons:
        all_parts.append([(offset + h, l)])

    edge_counts = Counter(edge for part in all_parts for edge in part)
    assert len(all_parts) == 17556
    assert len(edge_counts) == 7 * p
    assert set(edge_counts.values()) == {1}
    assert all(0 <= h < p and 0 <= l < 7 for h, l in edge_counts)
    print("K_(6,7), K_(7,7), K_(11,7) blocks: PASS")
    print(f"K_({p},7): {singleton_count} singletons + {cycle_count} cycles = 17556 parts; PASS")


if __name__ == "__main__":
    main()
