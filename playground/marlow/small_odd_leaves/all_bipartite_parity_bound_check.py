"""Bounded full-edge audit of the all-parity K_(p,t) formula."""

from collections import Counter, defaultdict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from odd_hubs_large_leaves_uniform_check import (
    even_weave,
    odd_small_leaf_partition,
    partition,
)


def odd_hub_partition(p, t):
    assert p % 2 == 1
    if p == 1 or t == 1:
        return {(h, leaf) for h in range(p) for leaf in range(t)}, []
    if t >= p - 1:
        return partition(p, t)
    if t % 2:
        return odd_small_leaf_partition(p, t)
    return {(p - 1, leaf) for leaf in range(t)}, even_weave(p - 1, t)


def construct(p, t):
    if p % 2:
        return odd_hub_partition(p, t)
    if t % 2:
        singles, cycles = odd_hub_partition(t, p)
        return {(leaf, hub) for hub, leaf in singles}, [
            {(leaf, hub) for hub, leaf in cycle} for cycle in cycles
        ]
    q, m = max(p, t), min(p, t)
    cycles = even_weave(q, m)
    if p == q:
        return set(), cycles
    return set(), [{(leaf, hub) for hub, leaf in cycle} for cycle in cycles]


def assert_simple_cycle(edges):
    assert len(edges) >= 4 and len(edges) % 2 == 0
    adj = defaultdict(set)
    for hub, leaf in edges:
        h, l = (0, hub), (1, leaf)
        adj[h].add(l)
        adj[l].add(h)
    assert len(adj) == len(edges)
    assert all(len(neighbors) == 2 for neighbors in adj.values())
    seen = set()
    stack = [next(iter(adj))]
    while stack:
        vertex = stack.pop()
        if vertex not in seen:
            seen.add(vertex)
            stack.extend(adj[vertex] - seen)
    assert len(seen) == len(adj)


def check(p, t):
    singles, cycles = construct(p, t)
    required_singles = max(p if t % 2 else 0, t if p % 2 else 0)
    m = min(p, t)
    minimum = required_singles + (p * t - required_singles + 2 * m - 1) // (2 * m)
    assert len(singles) == required_singles
    assert len(singles) + len(cycles) == minimum
    used = Counter(singles)
    for cycle in cycles:
        assert_simple_cycle(cycle)
        used.update(cycle)
    assert used == Counter((hub, leaf) for hub in range(p) for leaf in range(t))


if __name__ == "__main__":
    for p in range(1, 42):
        for t in range(1, 42):
            check(p, t)
    print("GENERAL_ALL_PARITIES_PASS 1,681 full K_(p,t) partitions, p,t=1..41")
