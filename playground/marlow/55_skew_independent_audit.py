import ast
from collections import defaultdict, deque
from itertools import combinations
from pathlib import Path

source=Path(__file__).resolve().with_name('55_skew_two_trade_first_step.py').read_text()
tree=ast.parse(source)
assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TRADES' for t in n.targets))
trades=ast.literal_eval(assignment.value)
assert set(trades)=={13,29,37,53,61,101}


def prime(p):
    return p>1 and all(p%d for d in range(2,int(p**0.5)+1))


def primitive(p):
    for g in range(2,p):
        if len({pow(g,e,p) for e in range(p-1)})==p-1:
            return g
    raise AssertionError(p)


def shape(edges):
    neighbors=defaultdict(list)
    for hub,leaf in edges:
        neighbors[('H',hub)].append(('L',leaf))
        neighbors[('L',leaf)].append(('H',hub))
    assert all(len(n)==2 and len(set(n))==2 for n in neighbors.values())
    unseen=set(neighbors); sizes=[]
    while unseen:
        start=unseen.pop();stack=[start];hubs=leaves=0
        while stack:
            v=stack.pop()
            if v[0]=='H':hubs+=1
            else:leaves+=1
            for w in neighbors[v]:
                if w in unseen:
                    unseen.remove(w);stack.append(w)
        assert hubs==leaves
        sizes.append(hubs)
    return sorted(sizes),{x for side,x in neighbors if side=='H'},{x for side,x in neighbors if side=='L'}


def exact(colors,singles,p,connected=False):
    t=p+2;k=(p-1)//2
    assert len(colors)==k+1 and len(singles)==t
    seen=set()
    for edge in singles:
        assert 0<=edge[0]<p and 0<=edge[1]<t and edge not in seen
        seen.add(edge)
    sizes=[]
    for i,color in enumerate(colors):
        assert len(color)==2*(p-(i==k))
        assert all(0<=a<p and 0<=b<t and (a,b) not in seen for a,b in color)
        seen.update(color)
        comp,hubs,leaves=shape(color)
        assert len(hubs)==len(leaves)==p-(i==k)
        assert hubs==(set(range(p)) if i<k else set(range(p))-{1})
        if connected:assert comp==[p-(i==k)]
        sizes.append(comp)
    assert seen=={(a,b) for a in range(p) for b in range(t)}
    assert len(singles)+len(colors)==t+(k*t+p-1)//p
    return sizes

for p,moves in trades.items():
    assert p%8==5 and prime(p)
    k=(p-1)//2;u=(p-1)//4
    assert u%2==1
    g=primitive(p)
    half={pow(g,e,p) for i in range(u) for e in (4*i,4*i+1)}
    first={frozenset((x,pow(g,2,p)*x%p)) for x in half}
    second={frozenset((-x%p for x in pair)) for pair in first}
    assert len(first)==len(second)==k and not first&second
    for matching in (first,second):
        assert {x for pair in matching for x in pair}==set(range(1,p))
        assert {min((a-b)%p,(b-a)%p) for pair in matching for a,b in [tuple(pair)]}==set(range(1,k+1))
    assert {sum(pair)*pow(2,-1,p)%p for pair in first|second}==set(range(1,p))
    page_edges=first|second
    assert all(len(page_edges & {frozenset(((x+c)%p for x in edge)) for edge in page_edges})==1 for c in range(1,p))

    colors=[set() for _ in range(k)]
    for a,b in combinations(range(p),2):
        ci=min((a-b)%p,(b-a)%p)-1
        leaf=(a+b)*pow(2,-1,p)%p
        colors[ci].update({(a,leaf),(b,leaf)})
    assert [shape(part)[0] for part in colors]==[[p]]*k
    singles={(a,a) for a in range(p)}|{(1,p),(1,p+1)}
    page=set();displaced=[]
    for side,matching in enumerate((first,second)):
        fresh=p+side
        for pair in matching:
            a,b=sorted((x+1)%p for x in pair)
            ci=min((a-b)%p,(b-a)%p)-1
            common={leaf for hub,leaf in colors[ci] if hub==a}&{leaf for hub,leaf in colors[ci] if hub==b}
            assert len(common)==1
            old=common.pop()
            assert (a,fresh) not in colors[ci] and (b,fresh) not in colors[ci]
            colors[ci]-={(a,old),(b,old)}
            colors[ci]|={(a,fresh),(b,fresh)}
            page|={(a,old),(b,old)}
            displaced.append(old)
    assert len(set(displaced))==p-1
    colors.append(page)
    initial=exact(colors,singles,p)
    assert initial==[[p]]*k+[[2*u,2*u]]
    assert len(moves)==2
    for step,(color_pair,e1,e2,f1,f2) in enumerate(moves):
        c,d=color_pair
        e1,e2,f1,f2=map(tuple,(e1,e2,f1,f2))
        assert color_pair==((0,2) if step==0 else (0,k))
        assert e1[0]!=e2[0] and e1[1]!=e2[1]
        assert f1==(e1[0],e2[1]) and f2==(e2[0],e1[1])
        assert {e1,e2}<=colors[c] and {f1,f2}<=colors[d]
        support_before=[shape(colors[i])[1:] for i in (c,d)]
        colors[c]-={e1,e2};colors[c]|={f1,f2}
        colors[d]-={f1,f2};colors[d]|={e1,e2}
        assert [shape(colors[i])[1:] for i in (c,d)]==support_before
        cur=exact(colors,singles,p,connected=step==1)
        if step==0: assert cur==initial
    x=moves[0][1][0]
    assert moves[0][1:]==((x,x+k),(x+1,x+k+2),(x,x+k+2),(x+1,x+k))
    print(f'p={p} root={g} t={p+2} x={x} first_components={initial[-1]} parts={len(colors)+len(singles)} verified')
