"""Independent full-partition replay of five 1 mod 8 first-base traces.

Run: python3 -I playground/marlow/62_one_mod8_first_base_audit.py
"""
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

DATA=json.loads(Path(__file__).with_name('62_one_mod8_first_base_traces.json').read_text())


def prime_factors(n):
    out=[]
    d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:
                n//=d
        d+=1
    if n>1:out.append(n)
    return out


def pair(u,v):
    return tuple(sorted((u,v)))


def components(edges):
    adj=defaultdict(set)
    for u,l in edges:
        adj[(0,u)].add((1,l))
        adj[(1,l)].add((0,u))
    assert all(len(v)==2 for v in adj.values())
    todo=set(adj)
    out=[]
    while todo:
        stack=[todo.pop()]
        hubs=set()
        leaves=set()
        while stack:
            x=stack.pop()
            (hubs if x[0]==0 else leaves).add(x[1])
            for y in adj[x]:
                if y in todo:
                    todo.remove(y)
                    stack.append(y)
        assert len(hubs)==len(leaves)
        out.append((hubs,leaves))
    return out


def build(p,g):
    assert p%8==1 and all(p%d for d in range(2,int(p**0.5)+1))
    n=p-1
    assert all(pow(g,n//q,p)!=1 for q in prime_factors(n))
    t=n;e=0
    while t%2==0:
        t//=2;e+=1
    assert t>1
    A=2**(e-1)
    a=pow(g,A,p)
    half={pow(g,2*i*A+j,p) for i in range(t) for j in range(A)}
    first={pair(x,a*x%p) for x in half}
    second={pair(-u%p,-v%p) for u,v in first}
    assert len(first)==len(second)==n//2 and first.isdisjoint(second)
    assert {min((u-v)%p,(v-u)%p) for u,v in first}==set(range(1,(p+1)//2))
    k=n//2;inv2=pow(2,-1,p)
    colors=[set() for _ in range(k)]
    slots={}
    for u,v in combinations(range(p),2):
        d=min((u-v)%p,(v-u)%p)-1
        mid=(u+v)*inv2%p
        colors[d].update(((u,mid),(v,mid)))
        slots[(u,v)]=(d,mid)
    assert all(len(components(c))==1 for c in colors)
    page=set()
    for side,matching in enumerate((first,second)):
        fresh=p+side
        for u,v in matching:
            x,y=pair((u+1)%p,(v+1)%p)
            color,old=slots[(x,y)]
            assert {(x,old),(y,old)}<=colors[color]
            colors[color].difference_update(((x,old),(y,old)))
            colors[color].update(((x,fresh),(y,fresh)))
            page.update(((x,old),(y,old)))
    colors.append(page)
    singles={(h,h) for h in range(p)}|{(1,p),(1,p+1)}
    assert [len(components(c)) for c in colors]==[1]*k+[A]
    return singles,colors,A


for name,entry in sorted(DATA.items(),key=lambda z:int(z[0])):
    p=int(name);k=(p-1)//2
    singles,colors,A=build(p,entry['g'])
    totals=[sum(len(components(c)) for c in colors)]
    for raw in entry['trades']:
        ci,di,*four=raw
        x1,x2,y1,y2=map(tuple,four)
        assert ci!=di and 0<=ci<k+1 and 0<=di<k+1
        assert x1[0]!=x2[0] and x1[1]!=x2[1]
        assert y1==(x1[0],x2[1]) and y2==(x2[0],x1[1])
        assert {x1,x2}<=colors[ci] and {y1,y2}<=colors[di]
        support=[({h for h,l in colors[z]},{l for h,l in colors[z]}) for z in (ci,di)]
        colors[ci].difference_update((x1,x2));colors[ci].update((y1,y2))
        colors[di].difference_update((y1,y2));colors[di].update((x1,x2))
        assert support==[({h for h,l in colors[z]},{l for h,l in colors[z]}) for z in (ci,di)]
        totals.append(sum(len(components(c)) for c in colors))
        assert totals[-1]<=totals[-2]
    assert totals[0]==k+A and totals[-1]==k+1
    assert all(len(components(c))==1 for c in colors)
    seen=set(singles)
    assert len(seen)==p+2
    for i,color in enumerate(colors):
        n=p-(i==k)
        assert len(color)==2*n and len({h for h,l in color})==len({l for h,l in color})==n
        assert not seen&color
        seen.update(color)
    assert seen=={(h,l) for h in range(p) for l in range(p+2)}
    assert len(singles)+len(colors)==p+2+(k*(p+2)+p-1)//p
    print(p,'A',A,'trades',len(entry['trades']),'components',totals,'optimal parts',len(singles)+len(colors))
