"""Exact full-spoke replay: item81 first-three repair + item80 late pairs."""
from collections import defaultdict
from csv import DictReader
from itertools import combinations
from pathlib import Path

def components(edges):
    adj=defaultdict(set)
    for h,l in edges:
        adj[(0,h)].add((1,l));adj[(1,l)].add((0,h))
    assert adj and all(len(ns)==2 for ns in adj.values())
    unseen=set(adj);out=[]
    while unseen:
        todo=[unseen.pop()]; hubs=set()
        while todo:
            node=todo.pop()
            if node[0]==0:hubs.add(node[1])
            for nxt in adj[node]:
                if nxt in unseen:unseen.remove(nxt);todo.append(nxt)
        out.append(hubs)
    return out

def replay(p,j,first,second,later):
    g,a=first[0],first[1]
    assert (p,j) in ((41,19),(73,35))
    k=(p-1)//2;q=(p-1)//8
    half={pow(g,8*i+s,p) for i in range(q) for s in range(4)}
    S={frozenset((z,a*z%p)) for z in half}
    T={frozenset((-z%p for z in e)) for e in S}
    assert len(S)==len(T)==k and not S&T
    colors=[set() for _ in range(k)];slots={};inv2=pow(2,-1,p)
    for h1,h2 in combinations(range(p),2):
        d=min((h1-h2)%p,(h2-h1)%p)-1;leaf=(h1+h2)*inv2%p
        colors[d].update(((h1,leaf),(h2,leaf)));slots[h1,h2]=(d,leaf)
    singles={(h,h) for h in range(p)}
    for step in range(j):
        center=step+1;page=set()
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
    def rectangle(c,s,v):
        u=(v+s*delta)%p
        x=(c+beta*(u-c))%p;y=(c+gamma*(v-c))%p
        assert x==(c+s+beta*(v-c-s))%p
        assert y==(c+s+gamma*(u-c-s))%p
        return {(u,x),(v,y)},{(u,y),(v,x)}
    for n,v in enumerate(first[2:],1):
        e1,e2=rectangle(1,1,v)
        assert e1<=colors[k] and e2<=colors[k+1],(p,'first',n,v)
        colors[k]=(colors[k]-e1)|e2;colors[k+1]=(colors[k+1]-e2)|e1
        assert [len(components(colors[k+i])) for i in (0,1)]==[4-n]*2
    assert len(components(colors[k+2]))==4
    for n,v in enumerate(second,1):
        e1,e3=rectangle(1,2,v)
        assert e1<=colors[k] and e3<=colors[k+2],(p,'second',n,v)
        colors[k]=(colors[k]-e1)|e3;colors[k+2]=(colors[k+2]-e3)|e1
        assert len(components(colors[k]))==1
        assert len(components(colors[k+2]))==4-n
    for c in range(4,j,2):
        page1,page2=colors[k+c-1],colors[k+c]
        assert len(components(page1))==len(components(page2))==4
        for n,w in enumerate(later,1):
            v=(c+w)%p;e1,e2=rectangle(c,1,v)
            assert e1<=page1 and e2<=page2,(p,'late',c,n,w,'source')
            page1-=e1;page1|=e2;page2-=e2;page2|=e1
            assert len(components(page1))==len(components(page2))==4-n,(p,'late',c,n,w,'component')
    assert all(len(components(c))==1 for c in colors)
    seen=set(singles)
    assert len(seen)==p+2*j
    for page in colors:
        assert not seen&page
        seen|=page
    assert seen=={(h,l) for h in range(p) for l in range(p+2*j)}
    assert len(singles)+len(colors)==p+2*j+k+j
    print('PASS full odd-prefix',p,'j',j,'parts',len(singles)+len(colors))

if __name__=='__main__':
    with Path(__file__).with_name('81_four_component_third_base_exceptions.csv').open() as source:
        rows={int(r['p']):r for r in DictReader(source)}
    for p,j,w in ((41,19,(9,19,36)),(73,35,(8,17,22))):
        r=rows[p]
        first=tuple(int(r[x]) for x in ('g','a','first1','first2','first3'))
        second=tuple(int(r['second'+str(i)]) for i in (1,2,3))
        replay(p,j,first,second,w)
