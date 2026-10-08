"""Replay six one-trade antipodal second-growth witnesses.

Run: python3 -I playground/marlow/58_skew_second_base_one_trade.py
"""
from collections import defaultdict
from itertools import combinations

SMALL=(13,29,37,53,61,101)

def primitive(p):
    n=p-1;factors=[];m=n;d=2
    while d*d<=m:
        if m%d==0:
            factors.append(d)
            while m%d==0:m//=d
        d+=1
    if m>1:factors.append(m)
    return next(g for g in range(2,p) if all(pow(g,n//q,p)!=1 for q in factors))

def component_hubs(edges):
    adj=defaultdict(set)
    for a,b in edges:
        adj[('h',a)].add(('l',b));adj[('l',b)].add(('h',a))
    assert all(len(neighbors)==2 for neighbors in adj.values())
    unseen=set(adj);result=[]
    while unseen:
        stack=[unseen.pop()];hubs=set();leaves=set()
        while stack:
            node=stack.pop()
            (hubs if node[0]=='h' else leaves).add(node[1])
            for nxt in adj[node]:
                if nxt in unseen:unseen.remove(nxt);stack.append(nxt)
        assert len(hubs)==len(leaves)
        result.append(hubs)
    return result

def build(p):
    g=primitive(p);a=g*g%p;k=(p-1)//2;u=(p-1)//4
    half={pow(g,e,p) for i in range(u) for e in (4*i,4*i+1)}
    first={frozenset((x,a*x%p)) for x in half}
    second={frozenset((-z%p for z in edge)) for edge in first}
    assert len(first)==len(second)==k and not first&second
    colors=[set() for _ in range(k)];slots={}
    for x,y in combinations(range(p),2):
        d=min((x-y)%p,(y-x)%p)-1
        leaf=(x+y)*pow(2,-1,p)%p
        colors[d].update(((x,leaf),(y,leaf)))
        slots[x,y]=(d,leaf)
    assert all(len(component_hubs(c))==1 for c in colors)
    singles={(a,a) for a in range(p)}
    for step in range(2):
        center=step+1;page=set()
        for side,matching in enumerate((first,second)):
            fresh=p+2*step+side
            for edge in matching:
                x,y=sorted((z+center)%p for z in edge)
                d,old=slots[x,y]
                assert {(x,old),(y,old)}<=colors[d]
                colors[d]-={(x,old),(y,old)}
                colors[d]|={(x,fresh),(y,fresh)}
                page|={(x,old),(y,old)}
                slots[x,y]=(d,fresh)
        colors.append(page)
        singles|={(center,p+2*step),(center,p+2*step+1)}
    assert all(len(component_hubs(c))==1 for c in colors[:k])
    for step in (0,1):
        comps=component_hubs(colors[k+step])
        assert len(comps)==2 and sorted(map(len,comps))==[k,k]
        assert set().union(*comps)==set(range(p))-{step+1}
    return g,singles,colors

def line_move(p,g,colors):
    a=g*g%p;inv=lambda z:pow(z%p,-1,p)
    beta=(1+a)*inv(2)%p;gamma=beta*inv(a)%p
    delta=(1-a)*inv(1+a)%p
    chi=lambda z:pow(z%p,(p-1)//2,p)
    for v in range(p):
        u=(v+delta)%p
        if u in (1,2) or v in (1,2):continue
        x=(1+beta*(u-1))%p;y=(1+gamma*(v-1))%p
        if x==y:continue
        if chi((u-1)*(v-1))!=p-1 or chi((u-2)*(v-2))!=p-1:continue
        e1,e2,f1,f2=(u,x),(v,y),(u,y),(v,x)
        if {e1,e2}<=colors[-2] and {f1,f2}<=colors[-1]:
            return v,(e1,e2,f1,f2)
    raise AssertionError(f'no line move p={p}')

def check(p,singles,colors):
    k=(p-1)//2;t=p+4
    seen=set(singles)
    assert len(seen)==len(singles)==t and len(colors)==k+2
    for idx,color in enumerate(colors):
        assert len(color)==2*(p-(idx>=k)) and not seen&color
        seen|=color
        components=component_hubs(color)
        assert len(components)==1
        assert components[0]==(set(range(p)) if idx<k else set(range(p))-{idx-k+1})
    assert seen=={(a,b) for a in range(p) for b in range(t)}
    assert len(singles)+len(colors)==t+(k*t+p-1)//p

for p in SMALL:
    g,singles,colors=build(p)
    v,(e1,e2,f1,f2)=line_move(p,g,colors)
    colors[-2]-={e1,e2};colors[-2]|={f1,f2}
    colors[-1]-={f1,f2};colors[-1]|={e1,e2}
    check(p,singles,colors)
    print(f'p={p} g={g} v={v} trade {e1},{e2} <-> {f1},{f2}: exact optimal partition')
