"""Check finite K_(m,7) cycle blocks and the odd-p residue argument.

A row (H, L) is H[0], L[0], H[1], L[1], ..., H[-1], L[-1], H[0].
"""

from collections import Counter


SIX = [
    ([2, 4, 5, 1, 3, 0], [2, 6, 3, 5, 1, 4]),
    ([1, 2, 3, 4, 0, 5], [6, 3, 4, 0, 5, 2]),
    ([1, 5, 2, 4, 0, 3], [4, 1, 5, 3, 6, 0]),
]

NINE = [
    ([0, 2, 4, 3, 1, 6, 5], [3, 0, 2, 1, 4, 6, 5]),
    ([0, 8, 7, 4, 5, 6, 1], [4, 5, 6, 1, 0, 3, 2]),
    ([2, 6, 7, 8, 5, 4, 3], [2, 1, 0, 3, 4, 5, 6]),
    ([0, 8, 7, 3, 2, 1], [1, 2, 3, 4, 5, 6]),
]

TEN = [
    ([0, 3, 4, 1, 2, 5], [4, 3, 1, 5, 0, 6]),
    ([1, 9, 8, 6, 5, 4], [6, 1, 0, 5, 4, 2]),
    ([0, 2, 8, 3, 9, 7], [3, 6, 5, 0, 2, 1]),
    ([2, 5, 7, 4, 6, 8], [1, 3, 0, 6, 2, 4]),
    ([0, 1, 7, 9, 6, 3], [0, 4, 5, 3, 1, 2]),
]

ELEVEN = [
    ([8, 10, 3, 4, 9, 5, 0], [2, 1, 0, 5, 3, 6, 4]),
    ([1, 5, 9, 0, 6, 4, 10], [1, 4, 0, 3, 2, 6, 5]),
    ([6, 0, 5, 10, 1, 2, 7], [1, 2, 0, 3, 6, 4, 5]),
    ([3, 6, 1, 2, 8, 7], [6, 4, 0, 1, 3, 2]),
    ([4, 2, 9, 7, 8, 3], [3, 2, 1, 0, 5, 4]),
]


def seven():
    return [
        ([-k % 7 for k in range(7)], [(-k + a) % 7 for k in range(7)])
        for a in (1, 3, 5)
    ]


BLOCKS = {6: SIX, 7: seven(), 9: NINE, 10: TEN, 11: ELEVEN}
EXPECTED_LENGTHS = {
    6: [12, 12, 12],
    7: [14, 14, 14],
    9: [14, 14, 14, 12],
    10: [12, 12, 12, 12, 12],
    11: [14, 14, 14, 12, 12],
}


def edges(hubs, leaves):
    r = len(hubs)
    assert r == len(leaves) and 2 <= r <= 7
    assert len(set(hubs)) == r and len(set(leaves)) == r
    for i, leaf in enumerate(leaves):
        yield hubs[i], leaf
        yield hubs[(i + 1) % r], leaf


def audit_block(m, cycles):
    assert [2 * len(hubs) for hubs, _ in cycles] == EXPECTED_LENGTHS[m]
    universe = {(h, leaf) for h in range(m) for leaf in range(7)}
    used = [edge for hubs, leaves in cycles for edge in edges(hubs, leaves)]
    assert set(used) <= universe
    assert len(used) == len(set(used))
    singleton = universe - set(used)
    assert len(singleton) == m
    assert Counter(h for h, _ in singleton) == Counter(range(m))
    assert len(cycles) == (3 * m + 6) // 7
    return sorted(singleton)


# Each odd residue modulo 14 has one base; its blocks attain the ceiling.
ODD_BASES = {
    7: [7],
    9: [9],
    11: [11],
    13: [6, 7],
    15: [6, 9],
    17: [6, 11],
    19: [6, 6, 7],
}


def decomposition(p):
    assert p >= 7 and p % 2 == 1
    base = next(b for b in ODD_BASES if b % 14 == p % 14)
    assert p >= base
    return ODD_BASES[base] + [7] * (2 * ((p - base) // 14))


def main():
    for m, cycles in BLOCKS.items():
        singleton = audit_block(m, cycles)
        print(f"K_({m},7): {len(cycles)} cycles, {len(singleton)} singleton spokes: PASS")
        if m in (9, 10):
            print(f"  singleton spokes: {singleton}")
    assert {b % 14 for b in ODD_BASES} == set(range(1, 14, 2))
    for base, sizes in ODD_BASES.items():
        assert sum(sizes) == base
        assert sum(len(BLOCKS[m]) for m in sizes) == (3 * base + 6) // 7
    # Adding two K_(7,7) blocks adds 14 hubs, 14 singletons, and 6 cycles;
    # ceil(3(p+14)/7) = ceil(3p/7) + 6.  The finite base check proves all p.
    for p in range(7, 1000, 2):
        sizes = decomposition(p)
        assert sum(sizes) == p
        assert sum(len(BLOCKS[m]) for m in sizes) == (3 * p + 6) // 7
    print("Every odd p >= 7: residue proof and sample decompositions: PASS")


if __name__ == "__main__":
    main()
