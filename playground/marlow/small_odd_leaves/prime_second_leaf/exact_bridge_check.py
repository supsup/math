"""Exact-edge controls for a second-leaf bridge from prime shift pairs.

Finite certificates only. The structural criterion is proved in bridge.md.
"""

from collections import Counter, defaultdict
from itertools import permutations


# Each walk starts at a leaf and alternates leaf/hub; the final vertex
# connects back to the first. Row selections follow s=a^j, j=0..(p-3)/2.
CASES = {
    5: {
        "a": 4, "b": 2, "selected_second": (0, 3),
        "walk": ((1, 0), (0, 0), (1, 3), (0, 3), (1, 4), (0, 4),
                 (1, 1), (0, 1)),
    },
    7: {
        "a": 4, "b": 5, "selected_second": (6, 3, 5),
        "walk": ((1, 1), (0, 1), (1, 2), (0, 2), (1, 4), (0, 4),
                 (1, 5), (0, 6), (1, 6), (0, 3), (1, 3), (0, 5)),
    },
    11: {
        "a": 3, "b": 2, "selected_second": (7, 10, 8, 2, 6),
        "walk": ((1, 1), (0, 1), (1, 4), (0, 4), (1, 5), (0, 5),
                 (1, 9), (0, 9), (1, 3), (0, 6), (1, 8), (0, 8),
                 (1, 7), (0, 7), (1, 2), (0, 2), (1, 10), (0, 10),
                 (1, 6), (0, 3)),
    },
    13: {
        "a": 4, "b": 6, "selected_second": (5, 7, 2, 8, 6, 11),
        "walk": ((1, 1), (0, 1), (1, 10), (0, 10), (1, 9), (0, 9),
                 (1, 12), (0, 7), (1, 7), (0, 6), (1, 6), (0, 12),
                 (1, 3), (0, 5), (1, 5), (0, 8), (1, 8), (0, 3),
                 (1, 4), (0, 11), (1, 11), (0, 2), (1, 2), (0, 4)),
    },
}


def is_cycle(edges):
    graph = defaultdict(set)
    for h, leaf in edges:
        graph[(0, h)].add((1, leaf))
        graph[(1, leaf)].add((0, h))
    assert len(graph) == len(edges)
    assert all(len(neighbors) == 2 for neighbors in graph.values())
    seen, todo = set(), [next(iter(graph))]
    while todo:
        v = todo.pop()
        if v in seen:
            continue
        seen.add(v)
        todo.extend(graph[v] - seen)
    assert len(seen) == len(graph)


def edges_from_walk(walk):
    assert len(set(walk)) == len(walk)
    assert all(walk[j][0] != walk[(j + 1) % len(walk)][0]
               for j in range(len(walk)))
    edges = set()
    for j, vertex in enumerate(walk):
        nxt = walk[(j + 1) % len(walk)]
        h, leaf = (vertex[1], nxt[1]) if vertex[0] == 0 else (nxt[1], vertex[1])
        edges.add((h, leaf))
    assert len(edges) == len(walk)
    is_cycle(edges)
    return edges


def check_case(p, case):
    n = (p - 1) // 2
    a, b = case["a"], case["b"]
    order = [pow(a, j, p) for j in range(n)]
    Q = set(order)
    assert len(Q) == n
    assert Q == {x * x % p for x in range(1, p)}
    assert b not in Q and b != 0
    chi = lambda x: 0 if x % p == 0 else (1 if x % p in Q else -1)
    assert chi(1 - b) == -chi(1 - a)
    assert sorted(k for s in order for k in ((1 - a) * s % p,
                                             (1 - b) * s % p)) == list(range(1, p))
    selected = case["selected_second"]
    assert len(selected) == n == len(set(selected))
    assert set(selected).isdisjoint(Q)
    assert len(case["walk"]) == 4 * n
    z, w = p, p + 1
    full = []
    w_hubs = []
    for s, t in zip(order, selected):
        d, e = (1 - a) * s % p, (1 - b) * s % p
        color = {(h, (h + k) % p) for h in range(p) for k in (d, e)}
        removed_s = {(a * s % p, s), (b * s % p, s)}
        removed_t = {((t - d) % p, t), ((t - e) % p, t)}
        assert removed_s | removed_t <= color
        assert len(removed_s | removed_t) == 4
        color.difference_update(removed_s | removed_t)
        color.update({(h, z) for h, _ in removed_s})
        color.update({(h, w) for h, _ in removed_t})
        w_hubs.extend(h for h, _ in removed_t)
        assert len(color) == 2 * p
        is_cycle(color)
        full.append(color)
    assert len(set(w_hubs)) == p - 1
    assert len({h for part in full for h, leaf in part if leaf == z}) == p - 1
    short = edges_from_walk(case["walk"])
    assert len(short) == 2 * (p - 1)
    assert {leaf for _, leaf in short} == Q | set(selected)
    used = Counter(e for part in full for e in part)
    assert all(multiplicity == 1 for multiplicity in used.values())
    universe = {(h, leaf) for h in range(p) for leaf in range(p + 2)}
    pool = universe - set(used)
    assert short <= pool
    singles = pool - short
    assert len(singles) == p + 2
    assert Counter(leaf for _, leaf in singles) == Counter(range(p + 2))
    assert Counter(e for part in [*full, short, *({edge} for edge in singles)]
                   for e in part) == Counter(universe)
    assert len(full) + 1 + len(singles) == (p + 2) + n + 1
    old_short = {(s, s) for s in Q} | {(a * s % p, s) for s in Q}
    demoted = len(old_short - short)
    cross = sum((h in Q) != (leaf in Q) for h, leaf in short)
    assert cross == 2 * demoted
    return (sorted(set(range(p)) - set(w_hubs)),
            sorted(set(range(p)) - {h for h, _ in short}), demoted, cross)


def check_fixed_base_seven_failure():
    # The author's first p=7 base used a=2,b=6; no injection from Q into
    # F_7\Q makes the new leaf's six full-cycle spokes distinct.
    p, a, b = 7, 2, 6
    order = [pow(a, j, p) for j in range(3)]
    outside = sorted(set(range(p)) - set(order))
    distribution = Counter()
    for selected in permutations(outside, 3):
        w_hubs = []
        for s, t in zip(order, selected):
            d, e = (1 - a) * s % p, (1 - b) * s % p
            w_hubs.extend(((t - d) % p, (t - e) % p))
        distribution[len(set(w_hubs))] += 1
    assert distribution == {3: 2, 4: 16, 5: 6}
    return dict(sorted(distribution.items()))


if __name__ == "__main__":
    for p, case in CASES.items():
        omitted_w, omitted_short, demoted, cross = check_case(p, case)
        print(f"BRIDGE_PASS p={p} edges={p*(p+2)} "
              f"w_omits={omitted_w} short_omits={omitted_short} "
              f"old_edges_demoted={demoted} cross_spokes={cross}")
    print(f"FIXED_BASE_P7_NO_INJECTION_PASS hub_distinctness_distribution="
          f"{check_fixed_base_seven_failure()}")
