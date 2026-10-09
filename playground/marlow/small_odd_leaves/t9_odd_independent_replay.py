"""Standalone, standard-library replay of the saved K_(m,9) certificates.

Usage: python3 -I t9_odd_independent_replay.py t9_odd_base_cycles.json
This does not import the author's checker or any search/optimization package.
"""

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


BASES = tuple(range(9, 26, 2))
LEAVES = range(9)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inspect_cycle(row, m, index):
    require(isinstance(row, list) and len(row) == 2, f"m={m} row={index}: shape")
    hubs, leaves = row
    require(isinstance(hubs, list) and isinstance(leaves, list), f"m={m} row={index}: lists")
    n = len(hubs)
    require(n in (8, 9) and len(leaves) == n, f"m={m} row={index}: length")
    require(all(type(h) is int and 0 <= h < m for h in hubs), f"m={m} row={index}: hubs")
    require(all(type(l) is int and l in LEAVES for l in leaves), f"m={m} row={index}: leaves")
    require(len(set(hubs)) == n and len(set(leaves)) == n, f"m={m} row={index}: repeated vertex")
    edges = []
    for i, l in enumerate(leaves):
        edges.extend(((hubs[i], l), (hubs[(i + 1) % n], l)))
    require(len(set(edges)) == 2 * n, f"m={m} row={index}: repeated edge")
    return edges


def inspect_base(m, rows):
    require(isinstance(rows, list), f"m={m}: rows")
    k = (m - 9) // 2
    require(len(rows) == 4 + k, f"m={m}: cycle count")
    lengths = Counter()
    cycle_edges = []
    for i, row in enumerate(rows):
        lengths[len(row[0])] += 1
        cycle_edges.extend(inspect_cycle(row, m, i))
    require(lengths == Counter({9: 4, 8: k}) if k else lengths == Counter({9: 4}),
            f"m={m}: length distribution")
    edge_counts = Counter(cycle_edges)
    require(len(cycle_edges) == 8 * m, f"m={m}: total cycle edges")
    require(all(v == 1 for v in edge_counts.values()), f"m={m}: duplicate spoke")
    universe = {(h, l) for h in range(m) for l in LEAVES}
    require(set(edge_counts) <= universe, f"m={m}: extraneous spoke")
    singletons = universe - set(edge_counts)
    require(len(singletons) == m, f"m={m}: singleton count")
    require(Counter(h for h, _ in singletons) == Counter({h: 1 for h in range(m)}),
            f"m={m}: singleton at each hub")
    expected_leaf_counts = Counter({l: (3 if l < k else 1) for l in LEAVES})
    require(Counter(l for _, l in singletons) == expected_leaf_counts,
            f"m={m}: singleton leaves")
    require(len(rows) == (4 * m + 8) // 9, f"m={m}: optimal count")
    return singletons


def blocks_for(p):
    require(type(p) is int and p >= 9 and p % 2 == 1, "invalid p")
    b = next(m for m in BASES if m % 18 == p % 18)
    r, rem = divmod(p - b, 18)
    require(rem == 0 and r >= 0, f"p={p}: residue decomposition")
    return [b] + [9] * (2 * r)


def inspect_nine_hub_formula(rows):
    expected = []
    for a in (1, 3, 5, 7):
        formula_row = [[(-i) % 9 for i in range(9)], [(a - i) % 9 for i in range(9)]]
        expected.append(set(inspect_cycle(formula_row, 9, a)))
    actual = [set(inspect_cycle(row, 9, i)) for i, row in enumerate(rows)]
    require(actual == expected, "m=9: displayed formula differs from saved rows")


def inspect_lift(p, data, base_singletons):
    all_edges = Counter()
    all_singletons = Counter()
    offset = 0
    cycle_count = 0
    for m in blocks_for(p):
        for i, row in enumerate(data[str(m)]):
            for h, l in inspect_cycle(row, m, i):
                all_edges[(offset + h, l)] += 1
            cycle_count += 1
        for h, l in base_singletons[m]:
            all_singletons[(offset + h, l)] += 1
        offset += m
    universe = {(h, l) for h in range(p) for l in LEAVES}
    require(offset == p, "lift: hub offsets")
    require(all(v == 1 for v in all_edges.values()), "lift: repeated cycle spoke")
    require(all(v == 1 for v in all_singletons.values()), "lift: repeated singleton")
    require(set(all_edges).isdisjoint(all_singletons), "lift: overlap")
    require(set(all_edges) | set(all_singletons) == universe, "lift: incomplete graph")
    require(len(all_edges) == 8 * p and len(all_singletons) == p, "lift: edge counts")
    require(cycle_count == (4 * p + 8) // 9, "lift: cycle count")
    return cycle_count


def main(path):
    payload = Path(path).read_bytes()
    data = json.loads(payload)
    require(isinstance(data, dict) and set(data) == {str(m) for m in BASES}, "base keys")
    print("JSON SHA256", hashlib.sha256(payload).hexdigest())
    singletons = {}
    for m in BASES:
        singletons[m] = inspect_base(m, data[str(m)])
        print(f"m={m}: {m} singletons, {len(data[str(m)])} cycles, 9m edges exactly once")
    inspect_nine_hub_formula(data["9"])
    require({m % 18 for m in BASES} == set(range(1, 18, 2)), "odd residue coverage")
    # One symbolic count identity per residue; r remains an arbitrary nonnegative integer.
    for b in BASES:
        q, rem = divmod(4 * b, 9)
        ceil_base = q + bool(rem)
        require(len(data[str(b)]) == ceil_base, f"b={b}: ceiling")
        require(4 * (b + 18) == 4 * b + 72, f"b={b}: increment")
        require(len(data[str(b)]) + 8 == (4 * (b + 18) + 8) // 9,
                f"b={b}: lift count increment")
    p = 12289
    cycles = inspect_lift(p, data, singletons)
    print(f"p={p}: {p} singletons, {cycles} cycles, {p + cycles} pieces, {9*p} edges exactly once")
    print("PASS")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 -I t9_odd_independent_replay.py t9_odd_base_cycles.json")
    main(sys.argv[1])
