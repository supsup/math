"""Independent finite stress test of the multiplicative prime shift-pair trade."""

from collections import Counter, defaultdict


def primes(bound):
    ans = []
    for n in range(2, bound + 1):
        if all(n % d for d in range(2, int(n**0.5) + 1)):
            ans.append(n)
    return ans


def is_one_cycle(edges):
    adj = defaultdict(set)
    for hub, leaf in edges:
        x, y = (0, hub), (1, leaf)
        adj[x].add(y)
        adj[y].add(x)
    assert len(adj) == len(edges)
    assert all(len(v) == 2 for v in adj.values())
    start = next(iter(adj))
    seen, todo = set(), [start]
    while todo:
        x = todo.pop()
        if x in seen:
            continue
        seen.add(x)
        todo.extend(adj[x] - seen)
    assert len(seen) == len(adj)


def audit(p):
    lam = (p - 1) // 2
    S = {x * x % p for x in range(1, p)}
    assert len(S) == lam
    chi = lambda x: 0 if x % p == 0 else (1 if x % p in S else -1)
    generators = [a for a in S if len({pow(a, j, p) for j in range(lam)}) == lam]
    assert generators and 1 not in generators
    exemplar = None
    for a in generators:
        t = chi(1-a)
        admissible = [b for b in range(1, p) if chi(b) == -1 and chi(1-b) == -t]
        predicted = (p - 1 + t * (1 - chi(-1))) // 4
        assert 4 * len(admissible) == p - 1 + t * (1 - chi(-1))
        assert len(admissible) == predicted >= 1
        if exemplar is None:
            exemplar = a, admissible[0], len(admissible)
    a, b, first_b_count = exemplar
    ordered = [pow(a, j, p) for j in range(lam)]
    rows = [((1-a)*s % p, (1-b)*s % p, s, a*s % p, b*s % p)
            for s in ordered]
    shifts = [t for d,e,_,_,_ in rows for t in (d,e)]
    assert sorted(shifts) == list(range(1,p))
    assert {h for _,_,_,h,_ in rows} == S
    assert {g for _,_,_,_,g in rows} == set(range(1,p)) - S
    assert {((d-e) % p) for d,e,_,_,_ in rows}.isdisjoint({0})

    parts=[]
    short=set()
    for d,e,s,h,g in rows:
        old={(u,(u+v)%p) for u in range(p) for v in (d,e)}
        assert len(old)==2*p
        is_one_cycle(old)
        assert (h,s) in old and (g,s) in old
        new=old-{(h,s),(g,s)} | {(h,p),(g,p)}
        assert len(new)==2*p
        is_one_cycle(new)
        parts.append(new)
        short |= {(s,s),(h,s)}
    assert len(short)==p-1
    is_one_cycle(short)
    parts.append(short)
    singles={(g,s) for _,_,s,_,g in rows}
    singles |= {(v,v) for v in range(p) if v not in S}
    singles.add((0,p))
    assert len(singles)==p+1
    parts += [{e} for e in singles]
    counts=Counter(e for part in parts for e in part)
    assert counts==Counter((u,v) for u in range(p) for v in range(p+1))
    assert len(parts)==p+lam+2
    assert len(parts)==p+1+(lam+1)
    for block_count in (1, 2):
        grown = list(parts)
        for j in range(block_count):
            first = p + 1 + j*p
            for k in range(lam):
                x, y = 2*k+1, 2*k+2
                cycle = {(u, first+(u+v)%p) for u in range(p) for v in (x,y)}
                is_one_cycle(cycle)
                grown.append(cycle)
            grown.extend([{(u, first+u)} for u in range(p)])
        q = (block_count+1)*p+1
        assert Counter(e for part in grown for e in part) == Counter(
            (u,v) for u in range(p) for v in range(q))
        assert len(grown) == q + (lam*q+p-1)//p
    return a,b,len(generators),first_b_count,rows


if __name__=='__main__':
    ps=[p for p in primes(199) if p>=5]
    for p in ps:
        a,b,ng,nb,rows=audit(p)
        print('PASS',p,a,b,'generators',ng,'b_count_for_first_generator',nb)
        if p in (5,7,11,13):
            print('ROWS',p,rows)
    print('PASS_TOTAL',len(ps))
