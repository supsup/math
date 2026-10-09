"""Replay literal seven-leaf blocks and the all-odd residue bases from Markdown.

This script does not import either certificate checker.
"""

from collections import Counter
from pathlib import Path
import re


HERE = Path(__file__).parent
OLD = (HERE / "p12289_t7_odd_block_certificate.md").read_text()
NEW = (HERE / "t7_all_odd_exact.md").read_text()


def cycle_rows(document, begin, end):
    section = document.split(begin, 1)[1].split(end, 1)[0]
    result = []
    for line in section.splitlines():
        cells = re.findall(r"`([0-9]+(?: [0-9]+)+)`", line)
        if len(cells) == 2:
            result.append(tuple(tuple(map(int, cell.split())) for cell in cells))
    return result


def walk_edges(m, cycles):
    counts = Counter()
    for hubs, leaves in cycles:
        assert 2 <= len(hubs) == len(leaves) <= 7
        assert len(set(hubs)) == len(hubs), "cycle repeats a hub"
        assert len(set(leaves)) == len(leaves), "cycle repeats a leaf"
        vertices = [vertex for pair in zip(
            (("H", h) for h in hubs), (("L", l) for l in leaves)
        ) for vertex in pair]
        for u, v in zip(vertices, vertices[1:] + vertices[:1]):
            assert u[0] != v[0]
            h, l = (u[1], v[1]) if u[0] == "H" else (v[1], u[1])
            assert 0 <= h < m and 0 <= l < 7
            counts[(h, l)] += 1
    assert set(counts.values()) == {1}, "cycle edges overlap"
    return counts


def audit_block(m, cycles, claimed_singletons, lengths):
    assert [2 * len(hubs) for hubs, _ in cycles] == lengths
    cycle_edges = walk_edges(m, cycles)
    all_edges = {(h, l) for h in range(m) for l in range(7)}
    singletons = all_edges - set(cycle_edges)
    assert singletons == claimed_singletons, "claimed singleton complement differs"
    assert Counter(h for h, _ in singletons) == Counter(range(m))
    assert len(cycle_edges) + len(singletons) == 7 * m
    return cycle_edges, singletons


def translate(edges, offset):
    return Counter({(offset + h, l): 1 for h, l in edges})


def audit_composition(sizes, blocks):
    partition = Counter()
    offset = 0
    cycles = 0
    singletons = 0
    for m in sizes:
        cycle_edges, residual, cycle_count = blocks[m]
        partition.update(translate(cycle_edges, offset))
        partition.update(translate(residual, offset))
        cycles += cycle_count
        singletons += len(residual)
        offset += m
    assert partition == Counter({(h, l): 1 for h in range(offset) for l in range(7)})
    assert singletons == offset
    assert cycles == (3 * offset + 6) // 7
    return offset, cycles


def main():
    rows = {
        6: cycle_rows(OLD, "An auxiliary `K_(6,7)`", "The needed `K_(11,7)`"),
        9: cycle_rows(NEW, "A new `K_(9,7)`", "Its nine uncovered edges"),
        10: cycle_rows(NEW, "The search also found a `K_(10,7)`", "Its singleton complement"),
        11: cycle_rows(OLD, "The needed `K_(11,7)`", "Partition the 12,289 hubs"),
    }
    rows[7] = [
        (tuple(-k % 7 for k in range(7)),
         tuple((-k + a) % 7 for k in range(7)))
        for a in (1, 3, 5)
    ]
    claimed = {
        6: {(0, 2), (1, 1), (2, 0), (3, 2), (4, 1), (5, 0)},
        7: {(h, h) for h in range(7)},
        9: {(0, 0), (1, 0), (2, 1), (3, 0), (4, 3),
            (5, 2), (6, 5), (7, 4), (8, 6)},
        10: {(0, 5), (1, 3), (2, 2), (3, 6), (4, 5),
             (5, 2), (6, 4), (7, 6), (8, 3), (9, 4)},
        11: {(0, 5), (1, 2), (2, 5), (3, 3), (4, 1), (5, 5),
             (6, 0), (7, 6), (8, 6), (9, 6), (10, 4)},
    }
    lengths = {
        6: [12] * 3,
        7: [14] * 3,
        9: [14] * 3 + [12],
        10: [12] * 5,
        11: [14] * 3 + [12] * 2,
    }
    blocks = {}
    for m in (6, 7, 9, 10, 11):
        edges, residual = audit_block(m, rows[m], claimed[m], lengths[m])
        blocks[m] = edges, residual, len(rows[m])
        print(f"K_({m},7): {len(rows[m])} simple cycles, {len(edges)} unique cycle edges, {m} claimed singletons: PASS")

    base_section = NEW.split("These seven odd bases", 1)[1].split("For any odd", 1)[0]
    bases = {}
    for line in base_section.splitlines():
        match = re.fullmatch(r"\| (\d+) \| `([0-9+]+)` \| (\d+) \|", line)
        if match:
            b, sizes, count = match.groups()
            bases[int(b)] = ([int(x) for x in sizes.split("+")], int(count))
    assert set(bases) == {7, 9, 11, 13, 15, 17, 19}
    assert {b % 14 for b in bases} == set(range(1, 14, 2))
    for b, (sizes, claimed_cycles) in bases.items():
        assert sum(sizes) == b
        assert audit_composition(sizes, blocks) == (b, claimed_cycles)
        assert claimed_cycles == (3 * b + 6) // 7
        assert audit_composition(sizes + [7, 7], blocks) == (b + 14, claimed_cycles + 6)
        print(f"base {b}, residue {b % 14}: {claimed_cycles} cycles; +14 step: PASS")
    # The identities above apply at every step because translated hub intervals
    # never overlap, and ceil(3(p+14)/7) = ceil(3p/7)+6 for every integer p.
    print("All seven odd residues and add-14 induction: PASS")


if __name__ == "__main__":
    main()
