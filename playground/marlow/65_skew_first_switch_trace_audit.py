"""Independent replay of p=1 mod 8 first-base rectangle certificates."""
import json
from pathlib import Path
from itertools import combinations

DATA = Path(__file__).with_name("62_one_mod8_first_base_traces.json")


def prime_divisors(n):
    ds = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            ds.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        ds.append(n)
    return ds


def comps(edges, p):
    links = {}
    for h, l in edges:
        links.setdefault(('h', h), []).append(('l', l))
        links.setdefault(('l', l), []).append(('h', h))
    assert all(len(v) == 2 for v in links.values()), "not a 2-factor"
    unseen = set(links)
    out = []
    while unseen:
        start = next(iter(unseen))
        stack = [start]
        unseen.remove(start)
        hubs = set()
        while stack:
            v = stack.pop()
            if v[0] == 'h':
                hubs.add(v[1])
            for w in links[v]:
                if w in unseen:
                    unseen.remove(w)
                    stack.append(w)
        out.append(hubs)
    return out


def construct(p, g):
    assert p % 4 == 1 and p > 2
    assert all(p % d for d in range(2, int(p**0.5)+1)), "p not prime"
    assert all(pow(g, (p-1)//q, p) != 1 for q in prime_divisors(p-1)), "g not primitive"
    n = p-1
    odd = n
    while odd % 2 == 0:
        odd //= 2
    A = n // (2*odd)
    log = {}
    z = 1
    for i in range(n):
        assert z not in log
        log[z] = i
        z = z*g % p
    assert len(log) == n
    a = pow(g, A, p)
    # Each x with log(x) in first half of a 2A block starts one S edge.
    S = {frozenset((x, x*a % p)) for x in log if log[x] % (2*A) < A}
    R = {frozenset((-x % p for x in edge)) for edge in S}
    assert len(S) == len(R) == n//2 and not S.intersection(R)
    for M in (S, R):
        assert {x for edge in M for x in edge} == set(range(1, p))
    colors = [set() for _ in range(n//2)]
    slot = {}
    inv2 = pow(2, -1, p)
    for x, y in combinations(range(p), 2):
        d = min((y-x) % p, (x-y) % p)
        m = (x+y)*inv2 % p
        colors[d-1].add((x,m))
        colors[d-1].add((y,m))
        slot[(x,y)] = (d-1,m)
    singleton = {(x,x) for x in range(p)}
    page = set()
    for j, M in enumerate((S,R)):
        leaf = p+j
        for pair in M:
            x,y = sorted(((z+1) % p for z in pair))
            c,m = slot[(x,y)]
            removed = {(x,m),(y,m)}
            assert removed <= colors[c], "slot already moved"
            colors[c] -= removed
            colors[c] |= {(x,leaf),(y,leaf)}
            page |= removed
    colors.append(page)
    singleton |= {(1,p),(1,p+1)}
    assert all(len(c) == 2*p for c in colors[:-1])
    assert len(colors[-1]) == 2*(p-1)
    assert len(singleton) == p+2
    assert [len(comps(c,p)) for c in colors] == [1]*(n//2) + [A]
    return colors, singleton, A


def audit(p, obj):
    colors,singleton,A = construct(p,obj['g'])
    initial = A
    histories = []
    for step,m in enumerate(obj['trades'],1):
        c,d,e1,e2,f1,f2 = m
        e1,e2,f1,f2 = map(tuple,(e1,e2,f1,f2))
        u,x = e1; v,y = e2
        assert len({u,v}) == len({x,y}) == 2
        assert f1 == (u,y) and f2 == (v,x), "not rectangle"
        assert c != d and {e1,e2} <= colors[c] and {f1,f2} <= colors[d]
        before = sum(len(comps(col,p)) for col in colors)
        colors[c].difference_update((e1,e2))
        colors[c].update((f1,f2))
        colors[d].difference_update((f1,f2))
        colors[d].update((e1,e2))
        after = sum(len(comps(col,p)) for col in colors)
        assert after <= before + 2, (p,step,before,after,m)
        histories.append((before,after))
    assert all(len(comps(col,p)) == 1 for col in colors)
    seen = set(singleton)
    for color in colors:
        assert not seen.intersection(color), "duplicate edge"
        seen.update(color)
    assert seen == {(h,l) for h in range(p) for l in range(p+2)}, "coverage gap"
    assert len(colors)+len(singleton) == (p-1)//2 + p+3
    return A, len(obj['trades']), histories


if __name__ == '__main__':
    data = json.load(open(DATA))
    for key in sorted(data,key=int):
        p=int(key)
        A,trades,hist = audit(p,data[key])
        print(f'p={p}: A={A}, trades={trades}, component excess {A-1} -> 0, '
              f'drops={[a-b for a,b in hist]}, parts={(3*p+5)//2}')
