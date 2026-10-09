"""Bounded full-edge replay of the uniform large-leaf corollary.

All graph parts are built as explicit edge sets and then checked independently
for simple-cycle connectivity, disjointness, coverage, and the sharp count.
"""


def alternating_edges(hubs, leaves):
    assert len(hubs) == len(leaves) >= 2
    assert len(set(hubs)) == len(hubs)
    assert len(set(leaves)) == len(leaves)
    n = len(hubs)
    edges = set()
    for k in range(n):
        edges.add((hubs[k], leaves[k]))
        edges.add((hubs[(k + 1) % n], leaves[k]))
    assert len(edges) == 2 * n
    return edges


def square_block(t, hub_offset=0, leaf_offset=0):
    lam = (t - 1) // 2
    singles = {(hub_offset + h, leaf_offset + h) for h in range(t)}
    cycles = []
    for a in range(lam):
        hubs = [hub_offset + (-k % t) for k in range(t)]
        leaves = [leaf_offset + ((2 * a + 1 - k) % t) for k in range(t)]
        cycles.append(alternating_edges(hubs, leaves))
    return singles, cycles


def even_weave(q, m):
    assert q % 2 == m % 2 == 0 and 2 <= m <= q
    cycles = []
    for j in range(q // 2):
        hubs = [(2 * j + k) % q for k in range(m)]
        leaves = list(range(m))
        cycles.append(alternating_edges(hubs, leaves))
    return cycles


def selection_row(s, n):
    if n % 2:
        return s
    return (s - n // 2 + 1) % (n - 1)


def odd_small_leaf_partition(P, T):
    """Partition K_(P,T) for odd P>=T>=3, with P on the hub side."""
    assert P % 2 == T % 2 == 1 and P >= T >= 3
    lam = (T - 1) // 2
    a = (P - T) // 2
    r = a % T
    copies = a // T
    if r == 0:
        singles, cycles = square_block(T)
        used_hubs = T
    else:
        m = T - 1
        n = lam + r
        q = 2 * n
        z = m
        u = q
        row_for_s = {selection_row(s, n): s for s in range(lam)}
        assert len(row_for_s) == lam
        selected_hubs = set()
        deleted_edges = set()
        cycles = []
        for j in range(n):
            hubs = [(2 * j + k) % q for k in range(m)]
            edges = alternating_edges(hubs, list(range(m)))
            if j in row_for_s:
                s = row_for_s[j]
                for k in (2 * s, 2 * s + 1):
                    old_edge = (hubs[k], k)
                    assert old_edge in edges
                    edges.remove(old_edge)
                    edges.add((hubs[k], z))
                    edges.add((u, k))
                    deleted_edges.add(old_edge)
                    selected_hubs.add(hubs[k])
            cycles.append(edges)
        assert len(selected_hubs) == m
        singles = deleted_edges | {(h, z) for h in range(q) if h not in selected_hubs} | {(u, z)}
        used_hubs = q + 1
    assert used_hubs == T + 2 * r
    for i in range(2 * copies):
        more_singles, more_cycles = square_block(T, hub_offset=used_hubs + i * T)
        singles |= more_singles
        cycles.extend(more_cycles)
    return singles, cycles


def partition(p, t):
    """Construct K_(p,t) for odd p>=3 and t>=p-1."""
    assert p >= 3 and p % 2 == 1 and t >= p - 1
    if t % 2:
        old_singles, old_cycles = odd_small_leaf_partition(t, p)
        return {(leaf, hub) for hub, leaf in old_singles}, [
            {(leaf, hub) for hub, leaf in cycle} for cycle in old_cycles
        ]
    if t < 2 * p:
        old_cycles = even_weave(t, p - 1)
        singles = {(p - 1, leaf) for leaf in range(t)}
        cycles = [{(hub, leaf) for leaf, hub in cycle} for cycle in old_cycles]
        return singles, cycles
    old_singles, old_cycles = partition(p, t - p)
    new_singles, new_cycles = square_block(p, leaf_offset=t - p)
    return old_singles | new_singles, old_cycles + new_cycles


def check_cycle(edges):
    assert len(edges) >= 4 and len(edges) % 2 == 0
    adjacency = {}
    for hub, leaf in edges:
        a, b = ("h", hub), ("l", leaf)
        adjacency.setdefault(a, set()).add(b)
        adjacency.setdefault(b, set()).add(a)
    assert len(adjacency) == len(edges)
    assert all(len(neighbors) == 2 for neighbors in adjacency.values())
    seen = set()
    stack = [next(iter(adjacency))]
    while stack:
        vertex = stack.pop()
        if vertex not in seen:
            seen.add(vertex)
            stack.extend(adjacency[vertex] - seen)
    assert len(seen) == len(edges)


def check(p, t):
    singles, cycles = partition(p, t)
    assert len(singles) == t
    assert {leaf for _, leaf in singles} == set(range(t))
    used = set(singles)
    for cycle in cycles:
        check_cycle(cycle)
        assert not used.intersection(cycle)
        used.update(cycle)
    expected = {(hub, leaf) for hub in range(p) for leaf in range(t)}
    assert used == expected
    lam = (p - 1) // 2
    assert len(cycles) == (lam * t + p - 1) // p
    assert len(singles) + len(cycles) == t + (lam * t + p - 1) // p


if __name__ == "__main__":
    checked = 0
    for p in range(3, 32, 2):
        for t in range(p - 1, 4 * p + 1):
            check(p, t)
            checked += 1
    print(f"GENERAL_ODD_LARGE_LEAVES_PASS {checked} full K_(p,t) partitions")
