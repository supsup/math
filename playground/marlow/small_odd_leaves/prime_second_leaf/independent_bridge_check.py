"""Independent residual-graph and exact-edge replay of four bridge controls."""

from collections import Counter, defaultdict
from itertools import permutations
from pathlib import Path
from runpy import run_path


source = Path(__file__).with_name('exact_bridge_check.py')
CASES = run_path(str(source))['CASES']  # Import literals only, not its checker.


def one_cycle(edges):
    adj = defaultdict(set)
    for hub, leaf in edges:
        u, v = ('h', hub), ('l', leaf)
        adj[u].add(v)
        adj[v].add(u)
    assert len(edges) == len(adj)
    assert all(len(neighbors) == 2 for neighbors in adj.values())
    reached, todo = set(), [next(iter(adj))]
    while todo:
        v = todo.pop()
        if v not in reached:
            reached.add(v)
            todo.extend(adj[v] - reached)
    assert reached == set(adj)


def walk_edges(walk):
    assert len(walk) == len(set(walk))
    edges = set()
    for u, v in zip(walk, walk[1:] + walk[:1]):
        assert u[0] != v[0]
        edges.add((u[1], v[1]) if u[0] == 0 else (v[1], u[1]))
    assert len(edges) == len(walk)
    one_cycle(edges)
    return edges


def check(p, case):
    n = (p-1)//2
    a, b = case['a'], case['b']
    S = {x*x % p for x in range(1,p)}
    order = [pow(a,j,p) for j in range(n)]
    assert set(order) == S and len(set(order)) == n
    f = case['selected_second']
    assert len(f) == len(set(f)) == n and set(f).isdisjoint(S)
    universe = {(hub,leaf) for hub in range(p) for leaf in range(p+2)}
    full = []
    w_hubs = []
    for s, t in zip(order,f):
        d,e=(1-a)*s%p,(1-b)*s%p
        old={(hub,(hub+shift)%p) for hub in range(p) for shift in (d,e)}
        assert len(old)==2*p
        one_cycle(old)
        hs={a*s%p,b*s%p}
        ht={(t-d)%p,(t-e)%p}
        assert len(hs)==len(ht)==2
        assert {(u,s) for u in hs}|{(u,t) for u in ht} <= old
        new = ((old-{(u,s) for u in hs}-{(u,t) for u in ht})
               | {(u,p) for u in hs} | {(u,p+1) for u in ht})
        assert len(new)==2*p
        one_cycle(new)
        full.append(new)
        w_hubs.extend(ht)
    assert len(set(w_hubs))==p-1
    used=Counter(edge for cycle in full for edge in cycle)
    assert set(used.values())=={1}
    residual=universe-set(used)
    assert len(residual)==3*p
    leaf_degree=Counter(leaf for _,leaf in residual)
    hub_degree=Counter(hub for hub,_ in residual)
    assert all(hub_degree[h]==3 for h in range(p))
    active=S|set(f)
    assert len(active)==p-1
    assert all(leaf_degree[leaf]==(3 if leaf in active else 1)
               for leaf in range(p+2))
    short=walk_edges(case['walk'])
    assert len(short)==2*(p-1) and short<=residual
    assert {leaf for _,leaf in short}==active
    singles=residual-short
    assert Counter(leaf for _,leaf in singles)==Counter(range(p+2))
    assert len(singles)==p+2
    assert len(full)+1+len(singles)==p+2+n+1
    assert p+2+n+1==p+2+((p*(p+2)-(p+2)+2*p-1)//(2*p))
    assert Counter(edge for part in [*full,short,singles] for edge in part)==Counter(universe)
    return sorted(set(range(p))-set(w_hubs)),sorted(set(range(p))-{h for h,_ in short})


def seven_fixed_base():
    p,a,b=7,2,6
    S=[pow(a,j,p) for j in range(3)]
    outside=sorted(set(range(p))-set(S))
    hist=Counter()
    for f in permutations(outside,3):
        hubs=[]
        for s,t in zip(S,f):
            hubs += [(t-(1-a)*s)%p,(t-(1-b)*s)%p]
        hist[len(set(hubs))]+=1
    assert sum(hist.values())==24 and hist=={3:2,4:16,5:6}
    return hist


if __name__=='__main__':
    for p,case in CASES.items():
        print('INDEPENDENT_BRIDGE_PASS',p,'omitted_w_and_short',check(p,case))
    print('P7_FIXED_BASE_24_INJECTIONS',seven_fixed_base())
