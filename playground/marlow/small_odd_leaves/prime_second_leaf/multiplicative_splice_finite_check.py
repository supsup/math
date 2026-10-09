"""Finite exact-edge certificates for the two-ring second-leaf splice.

No existence claim outside the listed primes. Run with --generate to
refresh the committed JSON; ordinary execution re-derives every row,
checks literal representative walks, and replays all graph edges.
"""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path


CERT = Path(__file__).with_name("multiplicative_splice_finite_cert.json")
REPRESENTATIVES = {17, 19, 23}


def primes(a, b):
    return [p for p in range(a, b + 1) if p >= 2 and
            all(p % d for d in range(2, int(p**0.5) + 1))]


def chi(x, p):
    x %= p
    return 0 if not x else (1 if pow(x, (p - 1) // 2, p) == 1 else -1)


def order(x, p):
    seen = set()
    value = 1
    while value not in seen:
        seen.add(value)
        value = value * x % p
    assert value == 1
    return len(seen)


def first_case(p):
    n = (p - 1) // 2
    Q = {x for x in range(1, p) if chi(x, p) == 1}
    for a in sorted(Q):
        if order(a, p) != n:
            continue
        for b in range(1, p):
            if chi(b, p) != -1 or chi(1 - b, p) != -chi(1 - a, p):
                continue
            for c in range(1, p):
                if chi(c, p) != -1:
                    continue
                U, V = (c + a - 1) % p, (c + b - 1) % p
                if chi(U, p) * chi(V, p) != -1:
                    continue
                R, L = (U, V) if chi(U, p) == 1 else (V, U)
                if order(L * pow(c, -1, p) % p, p) != n:
                    continue
                for tau in (1, a):
                    for M in (c, L):
                        if b * R % p == M * tau % p:
                            return {"p": p, "a": a, "b": b, "c": c,
                                    "U": U, "V": V, "R": R, "L": L,
                                    "tau": tau, "M": M}
    return None


def cycle_walk(edges, start=(1, 1)):
    adjacency = defaultdict(set)
    for hub, leaf in edges:
        adjacency[(0, hub)].add((1, leaf))
        adjacency[(1, leaf)].add((0, hub))
    assert len(adjacency) == len(edges)
    assert all(len(neighbors) == 2 for neighbors in adjacency.values())
    assert start in adjacency
    walk = [start]
    previous = None
    current = start
    while True:
        choices = sorted(adjacency[current] - ({previous} if previous else set()))
        assert choices
        nxt = choices[0]
        if nxt == start:
            break
        assert nxt not in walk
        walk.append(nxt)
        previous, current = current, nxt
    assert len(walk) == len(edges)
    return [list(vertex) for vertex in walk]


def edges_from_walk(walk):
    edges = set()
    for j, raw in enumerate(walk):
        x, y = tuple(raw), tuple(walk[(j + 1) % len(walk)])
        assert x[0] != y[0]
        hub, leaf = (x[1], y[1]) if x[0] == 0 else (y[1], x[1])
        edges.add((hub, leaf))
    assert len(edges) == len(walk)
    return edges


def check_case(c):
    p, a, b, mult = (c[key] for key in ("p", "a", "b", "c"))
    U, V, R, L, tau, M = (c[key] for key in ("U", "V", "R", "L", "tau", "M"))
    n = (p - 1) // 2
    Q = {pow(a, j, p) for j in range(n)}
    assert len(Q) == n == len({x * x % p for x in range(1, p)})
    assert Q == {x * x % p for x in range(1, p)}
    assert chi(b, p) == chi(mult, p) == -1
    assert chi(1 - b, p) == -chi(1 - a, p)
    assert (U, V) == ((mult + a - 1) % p, (mult + b - 1) % p)
    assert chi(R, p) == 1 and chi(L, p) == -1
    assert {U, V} == {R, L}
    assert order(L * pow(mult, -1, p) % p, p) == n
    assert tau in (1, a) and M in (mult, L)
    assert b * R % p == M * tau % p
    assert sorted(k for s in Q for k in ((1 - a) * s % p,
                                         (1 - b) * s % p)) == list(range(1, p))

    old_ring = {(s, s) for s in Q} | {(a * s % p, s) for s in Q}
    other_ring = {(mult * s % p, mult * s % p) for s in Q}
    other_ring |= {(L * s % p, mult * s % p) for s in Q}
    r = tau * pow(R, -1, p) % p
    removed_q = (tau, 1)
    removed_other = (b, mult * r % p)
    assert removed_q in old_ring and removed_other in other_ring
    short = (old_ring | other_ring) - {removed_q, removed_other}
    short |= {(b, 1), (tau, mult * r % p)}
    assert len(short) == 2 * (p - 1)
    walk = cycle_walk(short)
    if "walk" in c:
        assert edges_from_walk(c["walk"]) == short
        assert c["walk"] == walk

    z, w = p, p + 1
    full = []
    all_z_hubs, all_w_hubs = [], []
    for s in sorted(Q):
        d, e = (1 - a) * s % p, (1 - b) * s % p
        t = mult * s % p
        color = {(hub, (hub + offset) % p)
                 for hub in range(p) for offset in (d, e)}
        remove_s = {(a * s % p, s), (b * s % p, s)}
        remove_t = {(U * s % p, t), (V * s % p, t)}
        assert len(remove_s | remove_t) == 4
        assert remove_s | remove_t <= color
        color.difference_update(remove_s | remove_t)
        color.update((hub, z) for hub, _ in remove_s)
        color.update((hub, w) for hub, _ in remove_t)
        assert len(color) == 2 * p
        cycle_walk(color, start=(1, z))
        all_z_hubs.extend(hub for hub, _ in remove_s)
        all_w_hubs.extend(hub for hub, _ in remove_t)
        full.append(color)
    assert set(all_z_hubs) == set(all_w_hubs) == set(range(1, p))
    all_edges = {(hub, leaf) for hub in range(p) for leaf in range(p + 2)}
    used = Counter(edge for part in full for edge in part)
    assert len(used) == 2 * p * n and all(v == 1 for v in used.values())
    assert short <= all_edges - set(used)
    singles = all_edges - set(used) - short
    assert len(singles) == p + 2
    assert Counter(leaf for _, leaf in singles) == Counter(range(p + 2))
    assert len(full) + 1 + len(singles) == p + 2 + n + 1
    assert Counter(edge for part in [*full, short, *({edge} for edge in singles)]
                   for edge in part) == Counter(all_edges)
    assert len(old_ring - short) == 1
    return walk


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()
    expected = []
    for p in primes(17, 101):
        case = first_case(p)
        assert case is not None, f"NO_TWO_RING_SPLICE p={p}"
        walk = check_case(case)
        if p in REPRESENTATIVES:
            case["walk"] = walk
        expected.append(case)
    if args.generate:
        CERT.write_text(json.dumps(expected, indent=2) + "\n")
    else:
        saved = json.loads(CERT.read_text())
        assert saved == expected
        for case in saved:
            check_case(case)
            print(f"SPLICE_PASS p={case['p']} a={case['a']} "
                  f"b={case['b']} c={case['c']} edges={case['p']*(case['p']+2)} "
                  f"literal_walk={case['p'] in REPRESENTATIVES}")
        print(f"SPLICE_RANGE_PASS primes={len(saved)} first=17 last=101")


if __name__ == "__main__":
    main()
