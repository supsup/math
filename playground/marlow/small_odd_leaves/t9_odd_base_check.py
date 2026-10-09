"""Independent audit of the literal K_(m,9) certificates in JSON.

A row [H, L] encodes H[0], L[0], H[1], L[1], ..., H[-1], L[-1], H[0].
This checker uses no optimization package and does not import the search code.
"""

from collections import Counter
import json
from pathlib import Path


BASES = tuple(range(9, 26, 2))
DATA = Path(__file__).with_name("t9_odd_base_cycles.json")


def cycle_edges(hubs, leaves, m):
    n = len(hubs)
    assert n == len(leaves) and 2 <= n <= 9
    assert len(set(hubs)) == n and len(set(leaves)) == n
    assert all(isinstance(h, int) and 0 <= h < m for h in hubs)
    assert all(isinstance(l, int) and 0 <= l < 9 for l in leaves)
    for i, leaf in enumerate(leaves):
        yield hubs[i], leaf
        yield hubs[(i + 1) % n], leaf


def audit_block(m, rows):
    k = (m - 9) // 2
    assert len(rows) == 4 + k == (4 * m + 8) // 9
    lengths = Counter(len(hubs) for hubs, _ in rows)
    assert lengths == Counter([9] * 4 + [8] * k)
    edges = [edge for hubs, leaves in rows for edge in cycle_edges(hubs, leaves, m)]
    assert len(edges) == len(set(edges)) == 8 * m
    universe = {(h, l) for h in range(m) for l in range(9)}
    remaining = universe.difference(edges)
    assert len(remaining) == m
    assert Counter(h for h, _ in remaining) == Counter(range(m))
    assert Counter(l for _, l in remaining) == Counter(
        {l: 3 if l < k else 1 for l in range(9)}
    )
    assert set(edges).isdisjoint(remaining)
    assert set(edges) | remaining == universe
    return remaining


def decomposition(p):
    assert p >= 9 and p % 2 == 1
    b = next(b for b in BASES if b % 18 == p % 18)
    assert p >= b
    return [b] + [9] * ((p - b) // 9)


def audit_assembly(p, blocks):
    seen = set()
    singletons = set()
    offset = 0
    cycle_count = 0
    for m in decomposition(p):
        rows = blocks[m]
        local_singletons = audit_block(m, rows)
        for hubs, leaves in rows:
            for h, l in cycle_edges(hubs, leaves, m):
                edge = (offset + h, l)
                assert edge not in seen
                seen.add(edge)
        singletons.update((offset + h, l) for h, l in local_singletons)
        cycle_count += len(rows)
        offset += m
    assert offset == p and len(singletons) == p
    assert cycle_count == (4 * p + 8) // 9
    assert len(seen) == 8 * p and seen.isdisjoint(singletons)
    assert seen | singletons == {(h, l) for h in range(p) for l in range(9)}


def main():
    raw = json.loads(DATA.read_text())
    assert set(raw) == {str(m) for m in BASES}
    blocks = {int(m): rows for m, rows in raw.items()}
    assert {b % 18 for b in BASES} == set(range(1, 18, 2))
    for m in BASES:
        audit_block(m, blocks[m])
        print(f"K_({m},9): {m} singleton spokes, {len(blocks[m])} cycles: PASS")
    for p in range(9, 1000, 2):
        sizes = decomposition(p)
        assert sum(sizes) == p
        assert sum(len(blocks[m]) for m in sizes) == (4 * p + 8) // 9
    audit_assembly(12289, blocks)
    print("All odd residues modulo 18 and full p=12289 assembly: PASS")


if __name__ == "__main__":
    main()
