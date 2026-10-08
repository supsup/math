"""Horton debate (undervoice 16042): is the Collatz river's departure from random trees Collatz-specific?

NULL: 'coin-flip Collatz'. Odd n -> 3n+1 or 3n-1, chosen by a fixed hash of n; even n -> n/2. Both odd rules
give an even number, so the step structure, the cut at N and the tree-building are identical to Collatz;
only the arithmetic of the odd step is scrambled. Trajectories end in a cycle (1, or the 3n-1 cycles), so the
union is a forest; each tree is rooted at its cycle's smallest member. Compare bifurcation ratios with
Collatz itself, both at the same N, against the same 20 Remy trees.
Standard library only: python3 -I strahler_null.py [N]
"""
import hashlib
import pathlib
import random
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import strahler as s  # noqa: E402


def coin(n, salt):
    return hashlib.blake2b(f"{salt}:{n}".encode(), digest_size=1).digest()[0] & 1


def forest(n_max, step):
    parent = {}
    roots = set()
    for st in range(1, n_max + 1):
        path, seen, n = [], {}, st
        while n not in parent and n not in seen:
            seen[n] = len(path)
            path.append(n)
            n = step(n)
        if n in seen:                      # new cycle: root it at its smallest member
            cyc = path[seen[n]:]
            r = min(cyc)
            roots.add(r)
            for v in cyc:
                parent[v] = None if v == r else step(v)
            for v in path[:seen[n]]:
                parent[v] = step(v)
        else:
            for v in path:
                parent[v] = step(v)
    children = {v: [] for v in parent}
    for v, p in parent.items():
        if p is not None:
            children[p].append(v)
    # one super-root joining the cycle roots, so horton() sees a single tree; it adds no stream of its own
    # when there is one root, and when there are several it merges them at the very top only
    return children, sorted(roots)


def horton_forest(children, roots):
    total = {}
    for r in roots:
        sub = {}
        stack = [r]
        while stack:
            v = stack.pop()
            sub[v] = children[v]
            stack.extend(children[v])
        cnt, _ = s.horton(sub, r)
        for k, c in cnt.items():
            total[k] = total.get(k, 0) + c
    return total


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
    collatz = lambda n: n // 2 if n % 2 == 0 else 3 * n + 1
    rows = []
    ch, roots = forest(N, collatz)
    cnt = horton_forest(ch, roots)
    rows.append(("Collatz 3n+1", roots, cnt))
    for salt in range(3):
        step = (lambda sl: (lambda n: n // 2 if n % 2 == 0 else (3 * n + 1 if coin(n, sl) else 3 * n - 1)))(salt)
        ch, roots = forest(N, step)
        rows.append((f"coin-flip, salt {salt}", roots, horton_forest(ch, roots)))
    rng = random.Random(7)
    per_k = {}
    for _ in range(20):
        rc, rr = s.remy_tree(rows[0][2][1], rng)
        r, _ = s.horton(rc, rr)
        for k, v in enumerate(s.ratios(r), start=1):
            per_k.setdefault(k, []).append(v)
    print(f"N = {N:,}; Remy control (20 trees, {rows[0][2][1]:,} sources): R_k mean +- sd")
    print("   " + "  ".join(f"k={k}: {statistics.mean(per_k[k]):.3f}+-{statistics.stdev(per_k[k]):.3f}" for k in range(1, 5)))
    for name, roots, cnt in rows:
        rb = s.ratios(cnt)
        z = [(rb[k - 1] - statistics.mean(per_k[k])) / statistics.stdev(per_k[k]) for k in range(1, 5)]
        print(f"{name:22s} roots {roots[:4]} sources {cnt[1]:,}  R_1..R_4 {rb[:4]}  z {[round(x, 1) for x in z]}")


if __name__ == "__main__":
    main()
