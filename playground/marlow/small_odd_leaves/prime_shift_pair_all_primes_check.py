"""Self-contained exact checks for the prime-order multiplicative shift-pair trade.

The theorem is proved in prime_shift_pair_all_primes.md. This script is a finite
corroboration and is not used to infer the universal quantifier.
"""

import argparse
from collections import Counter, defaultdict
from math import gcd


def primes_through(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for d in range(2, int(limit**0.5) + 1):
        if sieve[d]:
            sieve[d * d::d] = b"\x00" * len(sieve[d * d::d])
    return [p for p in range(limit + 1) if sieve[p]]


def character(x, p):
    x %= p
    if not x:
        return 0
    return 1 if pow(x, (p - 1) // 2, p) == 1 else -1


def rows_for_prime(p):
    assert p >= 5 and p in primes_through(p)
    n = (p - 1) // 2
    residues = {x for x in range(1, p) if character(x, p) == 1}
    a = next(x for x in sorted(residues) if len({pow(x, j, p) for j in range(n)}) == n)
    b = next(x for x in range(1, p)
             if character(x, p) == -1 and character(1 - x, p) == -character(1 - a, p))
    order = [pow(a, j, p) for j in range(n)]
    rows = [((1 - a) * s % p, (1 - b) * s % p,
             s, a * s % p, b * s % p) for s in order]
    return a, b, rows


def is_cycle(edges):
    adjacency = defaultdict(set)
    for hub, leaf in edges:
        adjacency[(0, hub)].add((1, leaf))
        adjacency[(1, leaf)].add((0, hub))
    assert len(adjacency) == len(edges)
    assert all(len(neighbors) == 2 for neighbors in adjacency.values())
    seen, todo = set(), [next(iter(adjacency))]
    while todo:
        vertex = todo.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        todo.extend(adjacency[vertex] - seen)
    assert len(seen) == len(adjacency)


def verify(p, rows, full_edges=True):
    n = (p - 1) // 2
    assert len(rows) == n
    assert sorted([offset for d, e, *_ in rows for offset in (d, e)]) == list(range(1, p))
    selected = {s for _, _, s, _, _ in rows}
    assert len(selected) == n == len({h for _, _, _, h, _ in rows})
    assert selected == {h for _, _, _, h, _ in rows}
    outside = [g for _, _, _, _, g in rows]
    assert len(set(outside)) == n and selected.isdisjoint(outside)
    successor = {s: h for _, _, s, h, _ in rows}
    start = rows[0][2]
    seen, current = set(), start
    while current not in seen:
        seen.add(current)
        current = successor[current]
    assert current == start and seen == selected
    assert all(gcd(d - e, p) == 1 and h == (s - d) % p and g == (s - e) % p
               for d, e, s, h, g in rows)
    if not full_edges:
        return None
    parts = []
    short = set()
    for d, e, s, h, g in rows:
        color = {(hub, (hub + offset) % p) for hub in range(p) for offset in (d, e)}
        assert len(color) == 2 * p
        is_cycle(color)
        color.difference_update({(h, s), (g, s)})
        color.update({(h, p), (g, p)})
        is_cycle(color)
        parts.append(color)
        short.update({(s, s), (h, s)})
    assert len(short) == 2 * n
    is_cycle(short)
    parts.append(short)
    remaining = (set(range(p)) - selected - set(outside))
    assert len(remaining) == 1
    singles = {(g, s) for _, _, s, _, g in rows}
    singles.update((t, t) for t in range(p) if t not in selected)
    singles.add((remaining.pop(), p))
    assert len(singles) == p + 1
    parts.extend([{edge} for edge in singles])
    assert len(parts) == p + n + 2
    covered = Counter(edge for part in parts for edge in part)
    assert covered == Counter((hub, leaf) for hub in range(p) for leaf in range(p + 1))
    return parts


def verify_lift(p, base_parts, blocks):
    """Replay disjoint p-leaf square blocks, with consecutive shift pairs."""
    n = (p - 1) // 2
    parts = list(base_parts)
    for block in range(blocks):
        start = p + 1 + block * p
        for d in range(1, p, 2):
            e = d + 1
            cycle = {(hub, start + (hub + offset) % p)
                     for hub in range(p) for offset in (d, e)}
            assert len(cycle) == 2 * p
            is_cycle(cycle)
            parts.append(cycle)
        parts.extend({(hub, start + hub)} for hub in range(p))
    q = (blocks + 1) * p + 1
    assert len(parts) == q + n * (blocks + 1) + 1
    covered = Counter(edge for part in parts for edge in part)
    assert covered == Counter((hub, leaf) for hub in range(p) for leaf in range(q))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-prime", type=int, default=500)
    parser.add_argument("--full-edge-through", type=int, default=500)
    parser.add_argument("--lift-blocks", type=int, default=2)
    args = parser.parse_args()
    checked = 0
    for p in primes_through(args.max_prime):
        if p < 5:
            continue
        a, b, rows = rows_for_prime(p)
        parts = verify(p, rows, p <= args.full_edge_through)
        if p <= args.full_edge_through and p <= 101:
            verify_lift(p, parts, args.lift_blocks)
        checked += 1
        print(f"PASS p={p} a={a} b={b} full_edges={p <= args.full_edge_through}")
    print(f"PASS total_primes={checked}")
