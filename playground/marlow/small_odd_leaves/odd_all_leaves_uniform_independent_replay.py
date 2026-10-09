"""Independent finite stress test of the proposed uniform odd-t all-seed switch.

Constructs every odd-leaf seed directly from the claimed row/column mapping,
then checks edge multiplicity and that each cycle is a connected simple cycle.
"""
from collections import Counter, defaultdict


def choice(lam, r):
    n = lam + r
    if n % 2:
        rows = {s:s for s in range(lam)}
    else:
        sig = {j:(j+n//2-1)%(n-1) for j in range(n-1)}
        inv = {s:j for j,s in sig.items()}
        rows = {inv[s]:s for s in range(lam)}
    assert len(rows) == lam
    assert set(rows.values()) == set(range(lam))
    assert len({(j+s)%n for j,s in rows.items()}) == lam
    return rows


def verify(t, r):
    lam = (t-1)//2
    assert t == 2*lam+1 and 1 <= r < t
    n = lam+r
    q=2*n
    m=t-1
    z=m
    u=q
    rows=choice(lam,r)
    cycles=[]
    taken=[]
    for j in range(n):
        hubs=[(2*j+k)%q for k in range(m)]
        edges=[(hubs[k],k) for k in range(m)] + [(hubs[(k+1)%m],k) for k in range(m)]
        if j in rows:
            s=rows[j]
            for k in (2*s,2*s+1):
                edges.remove((hubs[k],k))
                edges.extend(((hubs[k],z),(u,k)))
                taken.append((hubs[k],k))
        cycles.append(edges)
    assert len({h for h,k in taken})==m
    singleton=taken+[(h,z) for h in range(q) if h not in {a for a,b in taken}]+[(u,z)]
    assert len(singleton)==q+1==t+2*r
    got=Counter(singleton)
    full=short=0
    for edges in cycles:
        adj=defaultdict(set)
        for h,l in edges:
            got[h,l]+=1
            adj[('H',h)].add(('L',l)); adj[('L',l)].add(('H',h))
        assert len(edges)==len(adj)
        assert all(len(neighbors)==2 for neighbors in adj.values())
        pending=[next(iter(adj))];seen=set()
        while pending:
            x=pending.pop()
            if x in seen:continue
            seen.add(x);pending.extend(adj[x]-seen)
        assert len(seen)==len(adj)
        if len(edges)==2*t:full+=1
        elif len(edges)==2*(t-1):short+=1
        else:raise AssertionError((t,r,'bad cycle length',len(edges)))
    p=q+1
    assert got==Counter((h,l) for h in range(p) for l in range(t)),(t,r,'edge mismatch')
    assert full==lam and short==r,(t,r,full,short)
    assert len(cycles)==(p*lam+t-1)//t==lam+r,(t,r,'count')


if __name__=='__main__':
    count=0
    for t in range(3,102,2):
        for r in range(1,t):
            verify(t,r);count+=1
    print('PASS',count,'odd-leaf seed blocks, t=3..101; exact edges and simple connected cycles')
