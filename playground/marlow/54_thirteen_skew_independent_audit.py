import json
from collections import defaultdict, deque
from itertools import combinations
from pathlib import Path

DATA=Path(__file__).resolve().with_name('54_thirteen_skew_repair_traces.json')
traces=json.loads(DATA.read_text())
P=13
assert set(traces)=={str(i) for i in range(1,6)}
all_hubs=set(range(P))

# Independently enumerate each unordered hub pair and its affine color/leaf.
base=[set() for _ in range(6)]
for a,b in combinations(range(P),2):
    color=min((b-a)%P,(a-b)%P)-1
    leaf=((a+b)*7)%P
    base[color].add((a,leaf))
    base[color].add((b,leaf))

# The explicit p=13 Mullin--Nemeth half-set: exponents 0,1,4,5,8,9.
first={frozenset((pow(2,e,P),4*pow(2,e,P)%P)) for e in (0,1,4,5,8,9)}
second={frozenset((-x%P for x in pair)) for pair in first}
assert len(first)==len(second)==6 and not first.intersection(second)
for matching in (first,second):
    assert sorted(x for pair in matching for x in pair)==list(range(1,P))
    assert {min((tuple(pair)[0]-tuple(pair)[1])%P,(tuple(pair)[1]-tuple(pair)[0])%P) for pair in matching}==set(range(1,7))


def structure(color):
    adj=defaultdict(set)
    for a,b in color:
        assert 0<=a<P and b>=0
        adj[('h',a)].add(('l',b))
        adj[('l',b)].add(('h',a))
    assert len(color)==sum(len(v) for u,v in adj.items() if u[0]=='h')
    assert all(len(v)==2 for v in adj.values())
    unseen=set(adj); components=[]
    while unseen:
        start=next(iter(unseen)); unseen.remove(start)
        q=deque([start]); n=0
        while q:
            u=q.popleft();n+=1
            for v in adj[u]:
                if v in unseen:
                    unseen.remove(v);q.append(v)
        components.append(n)
    return sorted(components),{a for side,a in adj if side=='h'},{b for side,b in adj if side=='l'}


def partition(colors,singles,t,final=False):
    seen=set()
    assert len(singles)==t and len(set(singles))==t
    for e in singles:
        assert 0<=e[0]<P and 0<=e[1]<t and e not in seen
        seen.add(e)
    component_counts=[]
    for idx,color in enumerate(colors):
        assert len(color)==2*(P-(idx>=6)),(idx,len(color))
        assert all(0<=a<P and 0<=b<t and (a,b) not in seen for a,b in color)
        seen.update(color)
        cc,hubs,leaves=structure(color)
        assert len(hubs)==len(leaves)==P-(idx>=6)
        if idx<6: assert hubs==all_hubs
        else: assert hubs==all_hubs-{idx-5}
        component_counts.append(len(cc))
        if final: assert len(cc)==1,(t,idx,cc)
    assert seen=={(a,b) for a in range(P) for b in range(t)}
    if final:
        assert len(singles)+len(colors)==t+(6*t+12)//13
    return component_counts

for prefix in range(1,6):
    colors=[set(part) for part in base]
    singles={(a,a) for a in range(P)}
    assert partition(colors,singles,P,final=True)==[1]*6
    for step in range(prefix):
        center=step+1
        fresh=(P+2*step,P+2*step+1)
        new_short=set(); displaced=[]
        for side,matching in enumerate((first,second)):
            new_leaf=fresh[side]
            for pair in matching:
                a,b=sorted((x+center)%P for x in pair)
                color=min((b-a)%P,(a-b)%P)-1
                common={leaf for hub,leaf in colors[color] if hub==a} & {leaf for hub,leaf in colors[color] if hub==b}
                assert len(common)==1,(prefix,step,a,b,common)
                old_leaf=common.pop()
                assert (a,old_leaf) in colors[color] and (b,old_leaf) in colors[color]
                assert (a,new_leaf) not in colors[color] and (b,new_leaf) not in colors[color]
                colors[color].difference_update({(a,old_leaf),(b,old_leaf)})
                colors[color].update({(a,new_leaf),(b,new_leaf)})
                new_short.update({(a,old_leaf),(b,old_leaf)})
                displaced.append(old_leaf)
        assert len(displaced)==len(set(displaced))==12
        colors.append(new_short)
        singles.update({(center,fresh[0]),(center,fresh[1])})
        counts=partition(colors,singles,P+2*(step+1))
        assert counts[:6]==[1]*6 and counts[6:]==[2]*(step+1),(prefix,step,counts)
    before=sum(partition(colors,singles,P+2*prefix))
    for m,move in enumerate(traces[str(prefix)]):
        c,d,*pieces=move
        assert len(pieces)==4 and 0<=c<d<len(colors)
        e1,e2,f1,f2=[tuple(v) for v in pieces]
        assert e1[0]!=e2[0] and e1[1]!=e2[1]
        assert f1==(e1[0],e2[1]) and f2==(e2[0],e1[1])
        assert e1 in colors[c] and e2 in colors[c]
        assert f1 in colors[d] and f2 in colors[d]
        old_support=[structure(colors[i])[1:] for i in (c,d)]
        colors[c]-={e1,e2};colors[c]|={f1,f2}
        colors[d]-={f1,f2};colors[d]|={e1,e2}
        assert [structure(colors[i])[1:] for i in (c,d)]==old_support
        after=sum(partition(colors,singles,P+2*prefix))
        assert after<=before,(prefix,m,before,after)
        before=after
    counts=partition(colors,singles,P+2*prefix,final=True)
    print(f'prefix={prefix} t={P+2*prefix} trades={len(traces[str(prefix)])} parts={len(singles)+len(colors)} components={counts}')
