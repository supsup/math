"""Do Collatz rivers obey Horton's laws?

Build the Collatz tree of the starts 1..N (union of trajectories, rooted at 1; every value has one
successor, and at most two predecessors in the tree). Compute each node's Horton-Strahler order
(sources = 1; a node's order is the max over its children, plus 1 when two or more children share
that max). A STREAM of order k is a maximal chain of order-k nodes. Report N_k (streams of order k),
the bifurcation ratios N_k / N_(k+1), and the mean stream length (edges) per order.

CONTROL: Shreve's random-topology model, the classical null model for river networks, predicts
bifurcation ratio -> 4. A uniformly random binary tree with the same number of sources (Remy's
algorithm, seeded) shows what "random" looks like at this size, so a Collatz ratio near 4 would not by
itself mean anything special. Standard library only: python3 -I strahler.py
"""
import random
import statistics
import sys


def collatz_tree(n_max):
    parent = {1: None}
    for s in range(2, n_max + 1):
        n = s
        while n not in parent:
            m = n // 2 if n % 2 == 0 else 3 * n + 1
            parent[n] = m
            n = m
    children = {v: [] for v in parent}
    for v, p in parent.items():
        if p is not None:
            children[p].append(v)
    return children, 1


def remy_tree(leaves, rng):
    """Uniform random rooted binary tree with `leaves` leaves (Remy). Nodes 0..2L-2, root returned."""
    left, right, par = {0: None}, {0: None}, {0: None}
    nodes = [0]
    nxt = 1
    root = 0
    for _ in range(leaves - 1):
        v = rng.choice(nodes)
        new_int, new_leaf = nxt, nxt + 1
        nxt += 2
        p = par[v]
        par[new_int] = p
        if p is None:
            root = new_int
        elif left[p] == v:
            left[p] = new_int
        else:
            right[p] = new_int
        if rng.random() < 0.5:
            left[new_int], right[new_int] = v, new_leaf
        else:
            left[new_int], right[new_int] = new_leaf, v
        par[v] = par[new_leaf] = new_int
        left[new_leaf] = right[new_leaf] = None
        nodes += [new_int, new_leaf]
    children = {v: [c for c in (left[v], right[v]) if c is not None] for v in nodes}
    return children, root


def horton(children, root):
    order = {}
    stack = [(root, False)]
    while stack:
        v, done = stack.pop()
        if not done:
            stack.append((v, True))
            stack.extend((c, False) for c in children[v])
            continue
        ks = [order[c] for c in children[v]]
        if not ks:
            order[v] = 1
        else:
            top = max(ks)
            order[v] = top + 1 if ks.count(top) >= 2 else top
    # streams: a node starts a new stream unless one of its... count stream HEADS from the downstream
    # side: a stream of order k ends where its order rises (or at the root). Count streams by their
    # upstream ends: node v is the top of a stream if no child has the same order.
    counts, lengths = {}, {}
    for v in order:
        if all(order[c] != order[v] for c in children[v]):
            k = order[v]
            counts[k] = counts.get(k, 0) + 1
            # walk downstream while the order stays k (length in edges), using the parent map
    par = {c: v for v in children for c in children[v]}
    for v in order:
        if all(order[c] != order[v] for c in children[v]):
            k, n, u = order[v], 0, v
            while par.get(u) is not None and order[par[u]] == k:
                u = par[u]
                n += 1
            lengths.setdefault(k, []).append(n + 1)
    return counts, {k: statistics.mean(v) for k, v in lengths.items()}


def ratios(counts):
    ks = sorted(counts)
    return [round(counts[k] / counts[k + 1], 3) for k in ks if k + 1 in counts]


def main():
    sizes = [int(a) for a in sys.argv[1:]] or [1000, 10000, 100000, 1000000]
    rng = random.Random(20261008)
    for N in sizes:
        ch, root = collatz_tree(N)
        cnt, ln = horton(ch, root)
        leaves = cnt[1]
        print(f"COLLATZ N={N:,}: nodes {len(ch):,}, sources {leaves:,}, max order {max(cnt)}")
        print("   N_k", [cnt[k] for k in sorted(cnt)])
        print("   bifurcation N_k/N_k+1", ratios(cnt))
        print("   mean stream length", [round(ln[k], 2) for k in sorted(ln)])
        rr = []
        for trial in range(3):
            rch, rroot = remy_tree(leaves, rng)
            rc, _ = horton(rch, rroot)
            rr.append(ratios(rc))
        print(f"   CONTROL Remy random binary trees, {leaves:,} sources, 3 seeds:")
        for r in rr:
            print("     ", r)


if __name__ == "__main__":
    main()
