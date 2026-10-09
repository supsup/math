"""Independent replay of the literal rows in odd_t5_exact_blocks.md.

This deliberately does not import odd_t5_edge_check.py. Run it beside the
Markdown file with: python3 odd_t5_skeptical_replay.py
"""

from collections import Counter
from pathlib import Path
import re


NOTE = Path(__file__).with_name("odd_t5_exact_blocks.md")


def displayed_block(markdown, name, hubs):
    section = markdown.split(f"**{name} hubs.**", 1)[1].split("**", 1)[0]
    if name == "Four":
        match = re.search(r"make `\(j,(\d+)\)` singleton for each `j`", section)
        assert match, "missing four-hub singleton rule"
        missing = (int(match.group(1)),) * hubs
    else:
        match = re.search(r"\(m_0,\.\.\.,m_\d+\)=\(([^)]+)\)", section)
        assert match, f"missing singleton list in {name}-hub section"
        missing = tuple(map(int, match.group(1).split(",")))
    assert len(missing) == hubs

    cycles = []
    for line in section.splitlines():
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3 or not cells[0].isdigit():
            continue
        length = int(cells[0])
        leaves = tuple(map(int, cells[1].split(",")))
        cycle_hubs = tuple(map(int, cells[2].split(",")))
        assert length == 2 * len(leaves), (name, line)
        cycles.append((leaves, cycle_hubs))
    assert cycles, f"missing displayed cycles in {name}-hub section"
    return missing, tuple(cycles)


def five_block_from_formula():
    singletons = tuple(range(5))
    cycles = []
    for k in (1, 2):
        hubs = tuple(-2 * k * j % 5 for j in range(5))
        leaves = tuple((hub + k) % 5 for hub in hubs)
        cycles.append((leaves, hubs))
    return singletons, tuple(cycles)


def block_edges(singletons, cycles):
    p = len(singletons)
    counts = Counter((hub, leaf) for hub, leaf in enumerate(singletons))
    assert all(0 <= leaf < 5 for leaf in singletons)
    for leaves, hubs in cycles:
        assert 2 <= len(leaves) == len(hubs) <= 5
        assert len(set(leaves)) == len(leaves)
        assert len(set(hubs)) == len(hubs)
        assert all(0 <= leaf < 5 for leaf in leaves)
        assert all(0 <= hub < p for hub in hubs)
        walk = [("leaf", leaves[i // 2]) if i % 2 == 0 else
                ("hub", hubs[i // 2]) for i in range(2 * len(leaves))]
        assert len(set(walk)) == len(walk), "cycle repeats a vertex"
        for left, right in zip(walk, walk[1:] + walk[:1]):
            assert left[0] != right[0]
            hub = left[1] if left[0] == "hub" else right[1]
            leaf = left[1] if left[0] == "leaf" else right[1]
            counts[hub, leaf] += 1
    expected = {(hub, leaf) for hub in range(p) for leaf in range(5)}
    assert set(counts) == expected
    assert set(counts.values()) == {1}, "overlapping or missing edges"
    assert len(cycles) == (2 * p + 4) // 5
    return counts


def replay_partition(blocks, sizes):
    edge_counts = Counter()
    offset = 0
    singleton_count = cycle_count = 0
    for size in sizes:
        singletons, cycles = blocks[size]
        for hub, leaf in block_edges(singletons, cycles):
            edge_counts[offset + hub, leaf] += 1
        offset += size
        singleton_count += len(singletons)
        cycle_count += len(cycles)
    assert set(edge_counts) == {(hub, leaf) for hub in range(offset) for leaf in range(5)}
    assert set(edge_counts.values()) == {1}
    assert singleton_count == offset
    assert cycle_count == (2 * offset + 4) // 5
    return offset, singleton_count, cycle_count


def sizes_from_residue(p):
    assert p >= 15 and p % 2 == 1
    if p == 23:
        return [9, 7, 7]
    b = next(b for b in range(5) if (p - 7 * b) % 5 == 0)
    a = (p - 7 * b) // 5
    assert a >= 0, (p, a, b)
    assert 2 * a + 3 * b == (2 * p + 4) // 5
    return [5] * a + [7] * b


def sizes_for_odd_p(p):
    assert p >= 5 and p % 2 == 1
    if p in (5, 7, 9):
        return [p]
    if p == 11:
        return [7, 4]
    if p == 13:
        return [9, 4]
    return sizes_from_residue(p)


def main():
    markdown = NOTE.read_text()
    blocks = {
        4: displayed_block(markdown, "Four", 4),
        5: five_block_from_formula(),
        7: displayed_block(markdown, "Seven", 7),
        9: displayed_block(markdown, "Nine", 9),
    }
    for size, block in blocks.items():
        block_edges(*block)
        assert replay_partition(blocks, [size]) == (size, size, (2 * size + 4) // 5)

    # Check the small exceptions and every later residue-class representative.
    for p in range(5, 104, 2):
        sizes = sizes_for_odd_p(p)
        assert sum(sizes) == p
        assert sum(len(blocks[size][1]) for size in sizes) == (2 * p + 4) // 5
        assert replay_partition(blocks, sizes) == (p, p, (2 * p + 4) // 5)

    expected = (12289, 12289, 4916)
    assert replay_partition(blocks, [9] + [5] * 2456) == expected
    assert replay_partition(blocks, sizes_from_residue(12289)) == expected
    print("Literal 4/5/7/9 blocks, odd p=5..103, and both p=12289 partitions verified")


if __name__ == "__main__":
    main()
