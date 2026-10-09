"""Exact finite audit of the all-odd fixed-leaf construction.

The proof note establishes the unbounded result. This replays every edge,
cycle connectivity, and singleton ownership in a range of seed blocks.
"""


def cycle_edges(hubs, leaves):
    assert len(hubs) == len(leaves) >= 2
    assert len(set(hubs)) == len(hubs)
    assert len(set(leaves)) == len(leaves)
    length = len(hubs)
    edges = set()
    for k, leaf in enumerate(leaves):
        edges.add((hubs[k], leaf))
        edges.add((hubs[(k + 1) % length], leaf))
    assert len(edges) == 2 * length
    return edges


def check_simple_cycle(edges, expected_length):
    assert len(edges) == expected_length
    adjacency = {}
    for hub, leaf in edges:
        h = (0, hub)
        l = (1, leaf)
        adjacency.setdefault(h, set()).add(l)
        adjacency.setdefault(l, set()).add(h)
    assert len(adjacency) == expected_length
    assert all(len(neighbors) == 2 for neighbors in adjacency.values())
    visited = set()
    stack = [next(iter(adjacency))]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(adjacency[vertex] - visited)
    assert len(visited) == expected_length


def selected_row(column, lam, r):
    n = lam + r
    if n % 2:
        return column
    half = n // 2
    for row in range(n - 1):
        if (row + half - 1) % (n - 1) == column:
            return row
    raise AssertionError("column not present in near transversal")


def check(t, r):
    assert t >= 3 and t % 2
    lam = (t - 1) // 2
    assert 1 <= r < t
    n = lam + r
    q = 2 * n
    m = 2 * lam
    assert m <= q and lam <= n - 1
    chosen = {selected_row(s, lam, r): s for s in range(lam)}
    assert len(chosen) == lam
    assert len({(j + s) % n for j, s in chosen.items()}) == lam

    used = set()
    selected_hubs = set()
    selected_edges = set()
    full_cycles = short_cycles = 0
    for j in range(n):
        hubs = [(2 * j + k) % q for k in range(m)]
        leaves = list(range(m))
        edges = cycle_edges(hubs, leaves)
        if j in chosen:
            s = chosen[j]
            for k in (2 * s, 2 * s + 1):
                old_edge = (hubs[k], k)
                assert old_edge in edges
                edges.remove(old_edge)
                edges.add((hubs[k], m))
                edges.add((q, k))
                assert old_edge not in selected_edges
                selected_edges.add(old_edge)
                assert hubs[k] not in selected_hubs
                selected_hubs.add(hubs[k])
            check_simple_cycle(edges, 2 * t)
            full_cycles += 1
        else:
            check_simple_cycle(edges, 2 * (t - 1))
            short_cycles += 1
        assert not used.intersection(edges)
        used.update(edges)

    assert full_cycles == lam and short_cycles == r
    assert len(selected_hubs) == m
    singletons = selected_edges | {(h, m) for h in range(q) if h not in selected_hubs} | {(q, m)}
    assert len(singletons) == q + 1
    assert {h for h, _ in singletons} == set(range(q + 1))
    assert not used.intersection(singletons)
    complete = {(h, leaf) for h in range(q + 1) for leaf in range(t)}
    assert used | singletons == complete
    assert len(used) + len(singletons) == len(complete)
    assert len(singletons) + full_cycles + short_cycles == q + 1 + ((q + 1) * lam + t - 1) // t


if __name__ == "__main__":
    checked = 0
    for t in range(3, 52, 2):
        for r in range(1, t):
            check(t, r)
            checked += 1
    print(f"GENERAL_ODD_ALL_SEEDS_PASS odd t=3..51, {checked} nonzero seed blocks")
