"""Exhaustively check the explicit K_(p,5) edge partitions in the companion note.

Run: python3 odd_t5_edge_check.py
No external packages are required.
"""

from collections import Counter


SEVEN_MISSING = (0, 1, 2, 3, 4, 0, 0)
SEVEN_CYCLES = (
    ((0, 1, 3, 2, 4), (4, 2, 6, 3, 1)),
    ((1, 0, 4, 2, 3), (3, 2, 0, 1, 5)),
    ((1, 3, 2, 4), (0, 4, 5, 6)),
)
NINE_MISSING = (0, 1, 2, 3, 4, 3, 3, 4, 4)
NINE_CYCLES = (
    ((2, 1, 4, 3, 0), (3, 6, 0, 4, 1)),
    ((4, 0, 2, 1, 3), (3, 8, 4, 7, 1)),
    ((0, 4, 1, 2), (5, 2, 0, 6)),
    ((0, 3, 1, 2), (2, 8, 5, 7)),
)

FOUR_MISSING = (4, 4, 4, 4)
FOUR_CYCLES = (
    ((0, 1, 2, 3), (0, 1, 2, 3)),
    ((2, 3, 0, 1), (0, 1, 2, 3)),
)


def five_block():
    missing = tuple(range(5))
    cycles = []
    for k in (1, 2):
        hubs = tuple((-2 * k * j) % 5 for j in range(5))
        leaves = tuple((h + k) % 5 for h in hubs)
        cycles.append((leaves, hubs))
    return missing, tuple(cycles)


def check_block(missing, cycles):
    """Check syntax, simple cycles, and every edge exactly once."""
    p = len(missing)
    assert all(0 <= leaf < 5 for leaf in missing)
    counts = Counter((hub, leaf) for hub, leaf in enumerate(missing))
    for leaves, hubs in cycles:
        r = len(leaves)
        assert r == len(hubs) and 2 <= r <= 5
        assert len(set(leaves)) == r and len(set(hubs)) == r
        assert all(0 <= leaf < 5 for leaf in leaves)
        assert all(0 <= hub < p for hub in hubs)
        for j, hub in enumerate(hubs):
            counts[(hub, leaves[j])] += 1
            counts[(hub, leaves[(j + 1) % r])] += 1
    expected = {(hub, leaf) for hub in range(p) for leaf in range(5)}
    assert set(counts) == expected
    assert all(counts[edge] == 1 for edge in expected)
    assert len(missing) + len(cycles) == p + (2 * p + 4) // 5
    return p, len(missing), len(cycles)


def assemble(sizes):
    """Translate block-local hub labels and recheck the entire partition."""
    missing = []
    cycles = []
    for size in sizes:
        if size == 4:
            block_missing, block_cycles = FOUR_MISSING, FOUR_CYCLES
        elif size == 5:
            block_missing, block_cycles = five_block()
        elif size == 7:
            block_missing, block_cycles = SEVEN_MISSING, SEVEN_CYCLES
        elif size == 9:
            block_missing, block_cycles = NINE_MISSING, NINE_CYCLES
        else:
            raise ValueError(size)
        offset = len(missing)
        missing.extend(block_missing)
        cycles.extend((leaves, tuple(offset + hub for hub in hubs))
                      for leaves, hubs in block_cycles)
    return check_block(tuple(missing), tuple(cycles))


def general_sizes(p):
    if p == 9:
        return [9]
    if p == 11:
        return [7, 4]
    if p == 13:
        return [9, 4]
    if p == 23:
        return [9, 7, 7]
    for b in range(5):
        if (p - 7 * b) % 5 == 0:
            a = (p - 7 * b) // 5
            if a >= 0:
                return [5] * a + [7] * b
    raise ValueError(f"No stated construction for p={p}")


def main():
    for size, block in ((4, (FOUR_MISSING, FOUR_CYCLES)),
                        (5, five_block()),
                        (7, (SEVEN_MISSING, SEVEN_CYCLES)),
                        (9, (NINE_MISSING, NINE_CYCLES))):
        assert check_block(*block)[0] == size
    for p in range(5, 100, 2):
        assert assemble(general_sizes(p))[0] == p
    assert assemble([9] + [5] * 2456) == (12289, 12289, 4916)
    assert assemble(general_sizes(12289)) == (12289, 12289, 4916)
    print("Verified blocks 4,5,7,9; odd p=5..99; both p=12289 partitions.")


if __name__ == "__main__":
    main()
