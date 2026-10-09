"""Independent finite parameter and exact-edge controls for the one-cut family."""

from collections import Counter, defaultdict


def primes(limit):
    return [n for n in range(2, limit+1)
            if all(n%d for d in range(2, int(n**0.5)+1))]


def cycle(edges):
    adj=defaultdict(set)
    for hub,leaf in edges:
        h,l=('h',hub),('l',leaf)
        adj[h].add(l);adj[l].add(h)
    assert len(edges)==len(adj)
    assert all(len(adj[v])==2 for v in adj)
    seen=set();todo=[next(iter(adj))]
    while todo:
        v=todo.pop()
        if v not in seen:
            seen.add(v);todo.extend(adj[v]-seen)
    assert len(seen)==len(adj)


def get_triple(p):
    n=(p-1)//2
    Q={x*x%p for x in range(1,p)}
    chi=lambda x: 0 if x%p==0 else (1 if x%p in Q else -1)
    generators=[a for a in sorted(Q) if len({pow(a,j,p) for j in range(n)})==n]
    assert generators
    eps=-chi(-1)
    found=[]
    for a in generators:
        for c in range(p):
            R=(c+a-1)%p
            F=(c*c+2*(a-1)*c-(a-1))%p
            if not c*R*F*(1-c)%p:
                continue
            if (chi(c),chi(R),chi(F),chi(1-c))!=(-1,1,-1,eps):
                continue
            g=F*pow(c*R,-1,p)%p
            if len({pow(g,j,p) for j in range(n)}) != n:
                continue
            b=a*c*pow(R,-1,p)%p
            L=F*pow(R,-1,p)%p
            assert chi(b)==-1 and chi(1-b)==-chi(1-a)
            assert chi(L)==-1 and L*pow(c,-1,p)%p==g
            assert b*R%p==a*c%p
            found.append((a,b,c,R,L))
    return found


def exact_edges(p, triple):
    a,b,c,R,L=triple
    n=(p-1)//2
    order=[pow(a,j,p) for j in range(n)]
    Q=set(order)
    universe={(h,l) for h in range(p) for l in range(p+2)}
    colors=[]
    for s in order:
        d,e=(1-a)*s%p,(1-b)*s%p
        old={(h,(h+k)%p) for h in range(p) for k in (d,e)}
        assert len(old)==2*p
        cycle(old)
        t=c*s%p
        old_s={(a*s%p,s),(b*s%p,s)}
        old_t={(R*s%p,t),(L*s%p,t)}
        assert len(old_s|old_t)==4 and old_s|old_t <= old
        new=(old-old_s-old_t)|{(h,p) for h,_ in old_s}|{(h,p+1) for h,_ in old_t}
        assert len(new)==2*p
        cycle(new)
        colors.append(new)
    used=Counter(edge for C in colors for edge in C)
    assert set(used.values())=={1}
    P=universe-set(used)
    short={(s,s) for s in Q}|{(a*s%p,s) for s in Q}
    short|={(c*s%p,c*s%p) for s in Q}|{(L*s%p,c*s%p) for s in Q}
    short.remove((a,1));short.remove((b,b))
    short.add((b,1));short.add((a,b))
    assert len(short)==2*(p-1) and short<=P
    cycle(short)
    singles=P-short
    assert len(singles)==p+2
    assert Counter(l for _,l in singles)==Counter(range(p+2))
    assert Counter(edge for part in [*colors,short,singles] for edge in part)==Counter(universe)


if __name__=='__main__':
    checked=0
    for p in primes(401):
        if p<5: continue
        found=get_triple(p)
        if p in (5,13): assert not found
        elif p in (7,11) or p>=17: assert found,p
        if found and p<=101:
            exact_edges(p,found[0]);checked+=1
        print('PRIME',p,'found',len(found),'first',found[0] if found else None)
    print('FINITE_CONTROL_PASS','full_edge_pages',checked)
