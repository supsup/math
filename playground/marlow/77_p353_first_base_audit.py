"""Standalone replay of the saved 19-trade K_{353,355} partition.

Run: python3 -I playground/marlow/77_p353_first_base_audit.py
This rebuilds the antipodal starter and reads only its adjacent JSON trace.
"""

from collections import defaultdict
import json
from math import gcd, isqrt
from pathlib import Path

P = 353
G = 3
A = 16
Q = 11
K = (P - 1) // 2
TRACE = Path(__file__).with_name("77_p353_first_base_trace.json")


def components(edges):
    adjacent = defaultdict(set)
    for hub, leaf in edges:
        adjacent[(0, hub)].add((1, leaf))
        adjacent[(1, leaf)].add((0, hub))
    assert all(len(neighbors) == 2 for neighbors in adjacent.values())
    unseen = set(adjacent)
    count = 0
    while unseen:
        count += 1
        stack = [unseen.pop()]
        while stack:
            for vertex in adjacent[stack.pop()]:
                if vertex in unseen:
                    unseen.remove(vertex)
                    stack.append(vertex)
    return count, len(adjacent) // 2


def build():
    assert all(P % divisor for divisor in range(2, isqrt(P) + 1))
    assert pow(G, (P - 1) // 2, P) != 1
    assert pow(G, (P - 1) // 11, P) != 1
    assert len({pow(G, i, P) for i in range(P - 1)}) == P - 1
    a = pow(G, A, P)
    generators_a = {pow(G, A * exponent, P)
                    for exponent in range(1, 2 * Q)
                    if gcd(exponent, 2 * Q) == 1}
    assert len(generators_a) == 10
    assert all(pow((value + 3) * (1 + 3 * value) % P,
                   (P - 1) // 2, P) == 1 for value in generators_a)
    half = {pow(G, 2 * A * i + j, P) for i in range(Q) for j in range(A)}
    assert len(half) == K
    sides = []
    for sign in (1, -1):
        side = {frozenset((sign * x % P, sign * a * x % P)) for x in half}
        assert len(side) == K
        sides.append(side)
    assert not sides[0] & sides[1]

    inv2 = pow(2, -1, P)
    colors = [set() for _ in range(K)]
    slots = {}
    for difference in range(1, K + 1):
        for hub in range(P):
            neighbor = (hub + difference) % P
            leaf = (hub + neighbor) * inv2 % P
            key = frozenset((hub, neighbor))
            assert key not in slots
            slots[key] = (difference - 1, leaf)
            colors[difference - 1].update(((hub, leaf), (neighbor, leaf)))
    assert len(slots) == P * K
    assert all(components(color) == (1, P) for color in colors)

    page = set()
    for side_index, side in enumerate(sides):
        for pair in side:
            hub, neighbor = ((x + 1) % P for x in pair)
            color_index, leaf = slots[frozenset((hub, neighbor))]
            old = {(hub, leaf), (neighbor, leaf)}
            assert old <= colors[color_index]
            colors[color_index].difference_update(old)
            colors[color_index].update(((hub, P + side_index),
                                        (neighbor, P + side_index)))
            page.update(old)
    assert len(page) == 2 * (P - 1)
    assert components(page) == (A, P - 1)
    assert all(components(color) == (1, P) for color in colors)
    colors.append(page)
    return colors


def rectangle(x1, x2, y1, y2):
    assert x1[0] != x2[0] and x1[1] != x2[1]
    assert y1 == (x1[0], x2[1])
    assert y2 == (x2[0], x1[1])


def exchange(first, second, x1, x2, y1, y2):
    rectangle(x1, x2, y1, y2)
    assert {x1, x2} <= first
    assert {y1, y2} <= second
    assert {x1, x2}.isdisjoint(second)
    assert {y1, y2}.isdisjoint(first)
    first.difference_update((x1, x2))
    first.update((y1, y2))
    second.difference_update((y1, y2))
    second.update((x1, x2))


def audit():
    colors = build()
    trace = json.loads(TRACE.read_text())
    assert len(trace) == 19
    pending_split = None
    joins = repairs = 0
    for step, row in enumerate(trace):
        assert set(row) == {"kind", "color", "source", "target"}
        assert len(row["source"]) == len(row["target"]) == 2
        ci = row["color"]
        x1, x2 = map(tuple, row["source"])
        y1, y2 = map(tuple, row["target"])
        if row["kind"] == "page":
            assert pending_split is None
            before = components(colors[-1])[0]
            exchange(colors[-1], colors[ci], x1, x2, y1, y2)
            assert components(colors[-1])[0] == before - 1, step
            square_parts = components(colors[ci])[0]
            assert square_parts in (1, 2), (step, square_parts)
            if square_parts == 2:
                pending_split = ci
            joins += 1
        elif row["kind"] == "repair":
            assert pending_split is not None
            assert ci != pending_split
            page_parts = components(colors[-1])[0]
            exchange(colors[pending_split], colors[ci], x1, x2, y1, y2)
            assert components(colors[pending_split])[0] == 1
            assert components(colors[ci])[0] == 1
            assert components(colors[-1])[0] == page_parts
            pending_split = None
            repairs += 1
        else:
            raise AssertionError((step, row))
    assert pending_split is None and (joins, repairs) == (15, 4)
    assert components(colors[-1]) == (1, P - 1)

    singles = {(hub, hub) for hub in range(P)} | {(1, P), (1, P + 1)}
    assert len(singles) == P + 2
    seen = set(singles)
    for index, color in enumerate(colors):
        expected_hubs = P - (index == K)
        assert components(color) == (1, expected_hubs), index
        assert len(color) == 2 * expected_hubs
        assert seen.isdisjoint(color), index
        seen.update(color)
    assert seen == {(hub, leaf) for hub in range(P) for leaf in range(P + 2)}
    assert len(colors) + len(singles) == (3 * P + 5) // 2
    print("PASS K353,355: 15 joins + 4 repairs; 125315 spokes exact; 532 optimal parts")


if __name__ == "__main__":
    audit()
