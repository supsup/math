"""Independent graph replay of the three-page two-switch witnesses."""
from collections import defaultdict
from itertools import combinations

WITNESSES = [(13,2,3,5),(29,2,2,3),(37,2,16,4),
             (53,2,4,6),(61,2,11,2),(101,2,9,2)]


def cycles(edges):
    adj=defaultdict(list)
    for h,l in edges:
        adj[('h',h)].append(('l',l));adj[('l',l)].append(('h',h))
    assert all(len(v)==2 for v in adj.values())
    unseen=set(adj);out=[]
    while unseen:
        stack=[unseen.pop()];hubs=set()
        while stack:
            v=stack.pop()
            if v[0]=='h':hubs.add(v[1])
            for w in adj[v]:
                if w in unseen:unseen.remove(w);stack.append(w)
        out.append(hubs)
    return out


def raw_growth(p,g):
    k=(p-1)//2
    colors=[set() for _ in range(k+3)]
    slots={}
    inv2=pow(2,-1,p)
    for h,j in combinations(range(p),2):
        d=min((j-h)%p,(h-j)%p)
        m=(h+j)*inv2%p
        colors[d-1].update(((h,m),(j,m)))
        slots[(h,j)]=(d-1,m)
    singleton={(h,h) for h in range(p)}
    A=2
    lower={pow(g,4*i+j,p) for i in range((p-1)//4) for j in (0,1)}
    a=pow(g,A,p)
    first={frozenset((x,a*x%p)) for x in lower}
    antipode={frozenset((-x%p for x in edge)) for edge in first}
    assert len(first)==len(antipode)==k and first.isdisjoint(antipode)
    for step in range(3):
        center=step+1
        for side,matching in enumerate((first,antipode)):
            fresh=p+2*step+side
            for pair in matching:
                h,j=sorted(((center+x)%p for x in pair))
                ci,old=slots[(h,j)]
                assert {(h,old),(j,old)}<=colors[ci]
                colors[ci]-={(h,old),(j,old)}
                colors[ci]|={(h,fresh),(j,fresh)}
                colors[k+step]|={(h,old),(j,old)}
                slots[(h,j)]=(ci,fresh)
            singleton.add((center,fresh))
    return colors,singleton


def rect(p,g,c,sep,z):
    a=g*g%p;D=(a+1)%p
    beta=D*pow(2,-1,p)%p;gamma=beta*pow(a,-1,p)%p
    delta=(1-a)*pow(D,-1,p)%p
    v=(c+sep*z)%p;u=(v+sep*delta)%p
    x=(c+beta*(u-c))%p;y=(c+gamma*(v-c))%p
    return (u,x),(v,y),(u,y),(v,x)


def switch(C,D,R):
    e1,e2,f1,f2=R
    assert len({e1[0],e2[0]})==len({e1[1],e2[1]})==2
    assert (e1,e2,f1,f2)==(e1,e2,(e1[0],e2[1]),(e2[0],e1[1]))
    assert {e1,e2}<=C and {f1,f2}<=D
    C.difference_update((e1,e2));C.update((f1,f2))
    D.difference_update((f1,f2));D.update((e1,e2))


if __name__ == '__main__':
    for p,g,z1,z2 in WITNESSES:
        colors,singles=raw_growth(p,g)
        k=(p-1)//2
        assert [len(cycles(C)) for C in colors]==[1]*k+[2,2,2]
        R1=rect(p,g,1,1,z1);R2=rect(p,g,1,2,z2)
        switch(colors[k],colors[k+1],R1)
        assert [len(cycles(C)) for C in colors[k:]]==[1,1,2]
        switch(colors[k],colors[k+2],R2)
        assert [len(cycles(C)) for C in colors]==[1]*(k+3)
        for C in colors[:k]:assert len(C)==2*p and len(cycles(C)[0])==p
        for C in colors[k:]:assert len(C)==2*(p-1) and len(cycles(C)[0])==p-1
        seen=set(singles)
        for C in colors:
            assert not seen&C
            seen.update(C)
        assert seen=={(h,l) for h in range(p) for l in range(p+6)}
        assert len(singles)+len(colors)==(p+6)+k+3
        print(p,g,z1,z2,'verified',len(singles)+len(colors),'parts')
