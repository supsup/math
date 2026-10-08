"""Full spoke-partition replay for selected rows from the A=4 finite certificate."""
from collections import defaultdict
from csv import DictReader
from itertools import combinations
from pathlib import Path

def components(edges):
    adj=defaultdict(set)
    for h,l in edges:
        adj[('h',h)].add(('l',l));adj[('l',l)].add(('h',h))
    assert adj and all(len(ns)==2 for ns in adj.values())
    unseen=set(adj); result=[]
    while unseen:
        stack=[unseen.pop()];hubs=set();leaves=set()
        while stack:
            node=stack.pop()
            (hubs if node[0]=='h' else leaves).add(node[1])
            for nx in adj[node]:
                if nx in unseen:unseen.remove(nx);stack.append(nx)
        assert len(hubs)==len(leaves)
        result.append(hubs)
    return result

def replay(row):
    p,g,a=(int(row[k]) for k in ('p','g','a'))
    k=(p-1)//2;q=(p-1)//8
    half={pow(g,8*i+j,p) for i in range(q) for j in range(4)}
    S={frozenset((z,a*z%p)) for z in half}
    T={frozenset((-z%p for z in e)) for e in S}
    assert len(S)==len(T)==k and not S&T
    colors=[set() for _ in range(k)]
    slots={}
    inv2=pow(2,-1,p)
    for h1,h2 in combinations(range(p),2):
        d=min((h1-h2)%p,(h2-h1)%p)-1
        leaf=(h1+h2)*inv2%p
        colors[d].update(((h1,leaf),(h2,leaf)))
        slots[h1,h2]=(d,leaf)
    assert all(len(components(c))==1 for c in colors)
    singles={(h,h) for h in range(p)}
    for step in range(2):
        center=step+1; page=set()
        for side,matching in enumerate((S,T)):
            fresh=p+2*step+side
            for edge in matching:
                h1,h2=sorted((z+center)%p for z in edge)
                d,old=slots[h1,h2]
                assert {(h1,old),(h2,old)}<=colors[d]
                colors[d]-={(h1,old),(h2,old)}
                colors[d]|={(h1,fresh),(h2,fresh)}
                page|={(h1,old),(h2,old)}
                slots[h1,h2]=(d,fresh)
        colors.append(page)
        singles|={(center,p+2*step),(center,p+2*step+1)}
    assert all(len(components(c))==1 for c in colors[:k])
    assert all(len(components(c))==4 for c in colors[k:])
    beta=(1+a)*inv2%p;gamma=beta*pow(a,-1,p)%p;delta=(1-a)*pow(1+a,-1,p)%p
    for key in ('v1','v2','v3'):
        v=int(row[key]);u=(v+delta)%p
        x=(1+beta*(u-1))%p;y=(1+gamma*(v-1))%p
        old1={(u,x),(v,y)};old2={(u,y),(v,x)}
        assert old1<=colors[k] and old2<=colors[k+1]
        before=[len(components(colors[k+i])) for i in range(2)]
        colors[k]-=old1;colors[k]|=old2
        colors[k+1]-=old2;colors[k+1]|=old1
        after=[len(components(colors[k+i])) for i in range(2)]
        assert after==[n-1 for n in before],(p,key,before,after)
    assert all(len(components(c))==1 for c in colors)
    seen=set(singles)
    assert len(seen)==p+4
    for c in colors:
        assert not seen&c
        seen|=c
    assert seen=={(h,l) for h in range(p) for l in range(p+4)}
    assert len(singles)+len(colors)==(3*p+11)//2
    print('PASS p',p,'g',g,'v',tuple(row[k] for k in ('v1','v2','v3')),'parts',len(singles)+len(colors))

rows=list(DictReader(Path(__file__).with_name('79_four_component_second_base_witnesses.csv').open()))
for p in (41,73,89,137,233):
    replay(next(r for r in rows if int(r['p'])==p))
