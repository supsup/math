from csv import DictReader
from collections import defaultdict
from itertools import combinations
from pathlib import Path

def comps(edges):
    adj=defaultdict(set)
    for h,l in edges:
        adj[(0,h)].add((1,l));adj[(1,l)].add((0,h))
    if not adj or not all(len(ns)==2 for ns in adj.values()):return None
    unseen=set(adj);out=[]
    while unseen:
        stack=[unseen.pop()]; H=set();L=set()
        while stack:
            node=stack.pop();(H if node[0]==0 else L).add(node[1])
            for nx in adj[node]:
                if nx in unseen:unseen.remove(nx);stack.append(nx)
        if len(H)!=len(L):return None
        out.append(H)
    return out

def build(p,g,a,first_vs):
    k=(p-1)//2;q=(p-1)//8
    half={pow(g,8*i+j,p) for i in range(q) for j in range(4)}
    S={frozenset((z,a*z%p)) for z in half};T={frozenset((-z%p for z in e)) for e in S}
    colors=[set() for _ in range(k)];slots={};inv2=pow(2,-1,p)
    for h1,h2 in combinations(range(p),2):
        d=min((h1-h2)%p,(h2-h1)%p)-1; leaf=(h1+h2)*inv2%p
        colors[d].update(((h1,leaf),(h2,leaf)));slots[h1,h2]=(d,leaf)
    singles={(h,h) for h in range(p)}
    def grow(center):
        page=set();step=center-1
        for side,matching in enumerate((S,T)):
            fresh=p+2*step+side
            for edge in matching:
                h1,h2=sorted((z+center)%p for z in edge)
                d,old=slots[h1,h2]
                assert {(h1,old),(h2,old)}<=colors[d]
                colors[d]-={(h1,old),(h2,old)};colors[d]|={(h1,fresh),(h2,fresh)}
                page|={(h1,old),(h2,old)};slots[h1,h2]=(d,fresh)
        colors.append(page);singles.update(((center,p+2*step),(center,p+2*step+1)))
    grow(1);grow(2)
    beta=(1+a)*inv2%p;gamma=beta*pow(a,-1,p)%p;delta=(1-a)*pow(1+a,-1,p)%p
    def rectangle(v,s):
        u=(v+s*delta)%p;x=(1+beta*(u-1))%p;y=(1+gamma*(v-1))%p
        return {(u,x),(v,y)},{(u,y),(v,x)},(u,v,x,y)
    for v in first_vs:
        one,two,_=rectangle(v,1)
        assert one<=colors[k] and two<=colors[k+1]
        colors[k]-=one;colors[k]|=two;colors[k+1]-=two;colors[k+1]|=one
    assert len(comps(colors[k]))==len(comps(colors[k+1]))==1
    grow(3)
    assert len(comps(colors[k+2]))==4
    return colors,singles,rectangle


def check_row(row):
    p,g,a=(int(row[k]) for k in ("p","g","a"))
    assert a==pow(g,4,p)
    first=[int(row["first"+str(j)]) for j in (1,2,3)]
    second=[int(row["second"+str(j)]) for j in (1,2,3)]
    colors,singles,rect=build(p,g,a,first)
    k=(p-1)//2
    for j,v in enumerate(second,1):
        old1,old3,_=rect(v,2)
        assert len(old1)==len(old3)==2
        assert old1<=colors[k] and old3<=colors[k+2]
        colors[k]=(colors[k]-old1)|old3
        colors[k+2]=(colors[k+2]-old3)|old1
        assert len(comps(colors[k]))==1
        assert len(comps(colors[k+2]))==4-j
    assert all(len(comps(c))==1 for c in colors)
    covered=set(singles)
    for c in colors:
        assert not covered&c
        covered|=c
    assert covered=={(h,l) for h in range(p) for l in range(p+6)}
    assert len(singles)+len(colors)==(3*p+17)//2
    print("PASS full third-base partition",p,"parts",len(singles)+len(colors),flush=True)

if __name__=="__main__":
    here=Path(__file__).parent
    for name in ("81_four_component_third_base_exceptions.csv",
                 "81_four_component_third_base_star_witnesses.csv"):
        rows=list(DictReader((here/name).open()))
        if "exceptions" in name:
            assert {int(r['p']) for r in rows}=={41,73,89,137,233,281,313,457,617,937}
            chosen=rows
        else:
            sample={409,521,569,601,761,809,1609}
            chosen=[r for r in rows if int(r["p"]) in sample]
            assert len(chosen)==len(sample)
        for row in chosen:check_row(row)
