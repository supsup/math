"""Self-contained exact replay of formulaic three-page two-trade repairs.

Usage: python3 -I playground/marlow/64_skew_odd_prefix_replay.py [13 29 37 53 61 101]
Self-contained; no imports from other repository scripts.
"""
import sys
from collections import defaultdict
from itertools import combinations
from math import isqrt


def prime(p):
    return p > 1 and all(p % d for d in range(2, isqrt(p)+1))


def primitive_root(p):
    factors={q for q in range(2,p) if (p-1)%q==0 and prime(q)}
    for g in range(2,p):
        if all(pow(g,(p-1)//q,p)!=1 for q in factors): return g
    raise AssertionError(p)


def pair(u,v):
    return (u,v) if u<v else (v,u)


def component_sizes(edges):
    adj=defaultdict(set)
    for h,l in edges:
        adj[('h',h)].add(('l',l))
        adj[('l',l)].add(('h',h))
    assert all(len(n)==2 for n in adj.values())
    unseen=set(adj);sizes=[]
    while unseen:
        stack=[unseen.pop()];hubs=0
        while stack:
            vertex=stack.pop();hubs+=(vertex[0]=='h')
            for nxt in adj[vertex]:
                if nxt in unseen:
                    unseen.remove(nxt);stack.append(nxt)
        sizes.append(hubs)
    return sorted(sizes)


def grow_pages(p,g,j=3):
    k=(p-1)//2;t=(p-1)//4;a=g*g%p
    half={pow(g,4*i+j,p) for i in range(t) for j in (0,1)}
    first={pair(x,a*x%p) for x in half}
    second={pair(-u%p,-v%p) for u,v in first}
    assert len(first)==len(second)==k and first.isdisjoint(second)
    colors=[set() for _ in range(k)]
    slots={};i2=pow(2,-1,p)
    for u,v in combinations(range(p),2):
        d=min((u-v)%p,(v-u)%p)
        m=(u+v)*i2%p
        colors[d-1].update(((u,m),(v,m)))
        slots[(u,v)]=(d-1,m)
    singles={(h,h) for h in range(p)}
    for step in range(j):
        c=step+1;page=set();displaced=[]
        for side,matching in enumerate((first,second)):
            new_leaf=p+2*step+side
            for u,v in matching:
                x,y=sorted(((u+c)%p,(v+c)%p))
                ci,old_leaf=slots[(x,y)]
                old={(x,old_leaf),(y,old_leaf)}
                assert old<=colors[ci]
                colors[ci]-=old
                colors[ci].update(((x,new_leaf),(y,new_leaf)))
                page|=old
                displaced.append(old_leaf)
                slots[(x,y)]=(ci,new_leaf)
        assert len(displaced)==len(set(displaced))==p-1
        colors.append(page)
        singles.update(((c,p+2*step),(c,p+2*step+1)))
    assert [component_sizes(C) for C in colors]==[[p]]*k+[[(p-1)//2]*2]*j
    return singles,colors


def chi(p,z):
    z%=p
    if not z:return 0
    return 1 if pow(z,(p-1)//2,p)==1 else -1


def rectangle(p,a,c,s,z):
    inv=lambda x:pow(x%p,-1,p)
    beta=(a+1)*inv(2)%p
    gamma=beta*inv(a)%p
    delta=(1-a)*inv(a+1)%p
    v=(c+s*z)%p;u=(v+s*delta)%p
    x=(c+beta*(u-c))%p
    y=(c+gamma*(v-c))%p
    return ((u,x),(v,y),(u,y),(v,x))


def switch(A,B,R):
    e1,e2,f1,f2=R
    assert e1!=e2 and f1!=f2 and e1[0]!=e2[0] and e1[1]!=e2[1]
    assert {e1,e2}<=A and {f1,f2}<=B
    A.difference_update((e1,e2));A.update((f1,f2))
    B.difference_update((f1,f2));B.update((e1,e2))


def verify(p,singles,colors,j=3):
    k=(p-1)//2;leaf_count=p+2*j
    assert len(singles)==leaf_count and len(colors)==k+j
    assert {leaf for _,leaf in singles}==set(range(leaf_count))
    seen=set(singles)
    for i,C in enumerate(colors):
        expected=p-(i>=k)
        assert len(C)==2*expected
        assert component_sizes(C)==[expected]
        assert len({h for h,_ in C})==len({l for _,l in C})==expected
        assert not seen&C
        seen|=C
    assert seen=={(h,l) for h in range(p) for l in range(leaf_count)}
    assert len(singles)+len(colors)==leaf_count+(k*leaf_count+p-1)//p


def run(p,j=3):
    assert p%8==5 and prime(p)
    assert j>=3 and j%2==1 and j<=(p-3)//2
    g=primitive_root(p);a=g*g%p;delta=(1-a)*pow(a+1,-1,p)%p
    singles,colors=grow_pages(p,g,j);k=(p-1)//2
    first_good=[z for z in range(p) if chi(p,z*(z+delta))==-1
                and chi(p,(z-1)*(z+delta-1))==-1]
    second_good=[z for z in range(p) if chi(p,z*(z+delta))==1
                 and chi(p,(z-1)*(z+delta-1))==-1]
    assert first_good and second_good
    for z1 in first_good:
        R1=rectangle(p,a,1,1,z1)
        if not ({R1[0],R1[1]}<=colors[k] and {R1[2],R1[3]}<=colors[k+1]):
            continue
        switch(colors[k],colors[k+1],R1)
        assert component_sizes(colors[k])==component_sizes(colors[k+1])==[p-1]
        for z2 in second_good:
            R2=rectangle(p,a,1,2,z2)
            if R2[0][1]==R2[1][1]:continue
            if not ({R2[0],R2[1]}<=colors[k] and {R2[2],R2[3]}<=colors[k+2]):
                continue
            switch(colors[k],colors[k+2],R2)
            assert component_sizes(colors[k])==component_sizes(colors[k+2])==[p-1]
            tail=[]
            for c in range(4,j,2):
                for z in first_good:
                    R=rectangle(p,a,c,1,z)
                    if {R[0],R[1]}<=colors[k+c-1] and {R[2],R[3]}<=colors[k+c]:
                        switch(colors[k+c-1],colors[k+c],R)
                        assert component_sizes(colors[k+c-1])==component_sizes(colors[k+c])==[p-1]
                        tail.append((c,z,R))
                        break
                else:
                    raise AssertionError(('no later pair',p,j,c))
            verify(p,singles,colors,j)
            return g,z1,z2,R1,R2,len(first_good),len(second_good),tail
        switch(colors[k],colors[k+1],(R1[2],R1[3],R1[0],R1[1]))
    raise AssertionError(('no formulaic repair',p))


if __name__=='__main__':
    for token in (sys.argv[1:] or ('13','29','37','53','61','101')):
        p,j=map(int,token.split(':')) if ':' in token else (int(token),3)
        g,z1,z2,R1,R2,n1,n2,tail=run(p,j)
        print(f'p={p} g={g} z1={z1} z2={z2} good_sign_counts={n1},{n2} '
              f'j={j} parts={(p+2*j)+(p-1)//2+j} R1={R1} R2={R2} '
              f'later_pairs={[(c,z) for c,z,_ in tail]}',flush=True)
