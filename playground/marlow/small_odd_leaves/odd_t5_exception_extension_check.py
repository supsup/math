"""Verify the K_(4,5), K_(11,5), and K_(13,5) certificates independently."""

from collections import Counter

FOUR = (
    (4, 4, 4, 4),
    (
        ((0, 1, 2, 3), (0, 1, 2, 3)),
        ((2, 3, 0, 1), (0, 1, 2, 3)),
    ),
)
SEVEN = (
    (0, 1, 2, 3, 4, 0, 0),
    (
        ((0, 1, 3, 2, 4), (4, 2, 6, 3, 1)),
        ((1, 0, 4, 2, 3), (3, 2, 0, 1, 5)),
        ((1, 3, 2, 4), (0, 4, 5, 6)),
    ),
)
NINE = (
    (0, 1, 2, 3, 4, 3, 3, 4, 4),
    (
        ((2, 1, 4, 3, 0), (3, 6, 0, 4, 1)),
        ((4, 0, 2, 1, 3), (3, 8, 4, 7, 1)),
        ((0, 4, 1, 2), (5, 2, 0, 6)),
        ((0, 3, 1, 2), (2, 8, 5, 7)),
    ),
)


def verify(blocks):
    missing = []
    cycles = []
    for block_missing, block_cycles in blocks:
        offset = len(missing)
        missing.extend(block_missing)
        cycles.extend((leaves, tuple(h + offset for h in hubs))
                      for leaves, hubs in block_cycles)

    p = len(missing)
    assert all(0 <= leaf < 5 for leaf in missing)
    edge_counts = Counter((hub, leaf) for hub, leaf in enumerate(missing))
    for leaves, hubs in cycles:
        r = len(leaves)
        assert 2 <= r <= 5 and r == len(hubs)
        assert len(set(leaves)) == r and len(set(hubs)) == r
        assert all(0 <= leaf < 5 for leaf in leaves)
        assert all(0 <= hub < p for hub in hubs)
        for j, hub in enumerate(hubs):
            edge_counts[hub, leaves[j]] += 1
            edge_counts[hub, leaves[(j + 1) % r]] += 1

    expected = {(hub, leaf) for hub in range(p) for leaf in range(5)}
    assert set(edge_counts) == expected
    assert all(edge_counts[edge] == 1 for edge in expected)
    assert len(missing) == p
    assert len(cycles) == (2 * p + 4) // 5
    print(f"p={p}: {p} singletons, {len(cycles)} cycles, "
          f"all {5 * p} edges covered exactly once")


if __name__ == "__main__":
    verify((FOUR,))
    verify((SEVEN, FOUR))
    verify((NINE, FOUR))
