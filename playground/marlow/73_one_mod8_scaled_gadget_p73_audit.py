"""Independent exact replay of a 6-trade K_{73,75} antipodal-page repair.

Run: python3 -I playground/marlow/73_one_mod8_scaled_gadget_p73_audit.py
This does not import the gadget search or repository checkers.
"""
from collections import defaultdict

P=73
G=13
A=4
Q=9
ALPHA=pow(G,A,P)
SCALES=(4,7,44)
MOVES=(
    (3,11,(25,23),(29,31),(25,31),(29,23)),
    (3,36,(25,27),(8,10),(25,10),(8,27)),
    (6,20,(43,3),(50,17),(43,17),(50,3)),
    (6,36,(43,10),(68,35),(43,35),(68,10)),
    (28,13,(46,24),(17,39),(46,39),(17,24)),
    (28,36,(46,68),(5,27),(46,27),(5,68)),
)

def audit_scaled_template():
    z=(1+3*ALPHA)*pow((ALPHA-1)**2,-1,P)%P
    w=ALPHA*(ALPHA+3)*pow((ALPHA-1)**2,-1,P)%P
    assert (z,w)==(6,20)
    rho=w*pow(z,-1,P)%P
    assert rho==52 and pow(rho,(P-1)//2,P)==P-1
    quotient={pow(G,e,P):e%A for e in range(P-1)}
    assert [(quotient[s*z%P],quotient[s*w%P]) for s in SCALES] == [
        (2,3),(1,2),(3,0)]
    b=(1+z)%P
    v=(1+w)%P
    half=pow(2,-1,P)
    prep=((b,(b-half)%P),((b+1)%P,(b+3*half)%P),
          (b,(b+3*half)%P),((b+1)%P,(b-half)%P))
    join=((b,(b+half)%P),(v,(v+half)%P),
          (b,(v+half)%P),(v,(b+half)%P))
    for i,scale in enumerate(SCALES):
        transform=lambda x:(1+scale*(x-1))%P
        expected_prep=tuple((transform(h),transform(l)) for h,l in prep)
        expected_join=tuple((transform(h),transform(l)) for h,l in join)
        assert MOVES[2*i][2:]==expected_prep
        assert MOVES[2*i+1][2:]==expected_join
        assert MOVES[2*i][:2]==(
            min(scale,P-scale)-1,min(3*scale%P,-3*scale%P)-1)
        assert MOVES[2*i+1][:2]==(MOVES[2*i][0],(P-1)//2)
    assert len({c for i in (0,2,4) for c in MOVES[i][:2]})==2*(A-1)

def components(edges):
    graph=defaultdict(set)
    for h,l in edges:
        graph[(0,h)].add((1,l))
        graph[(1,l)].add((0,h))
    assert all(len(neighbors)==2 for neighbors in graph.values())
    unseen=set(graph);pieces=[]
    while unseen:
        v=unseen.pop();stack=[v];piece={v}
        while stack:
            for w in graph[stack.pop()]:
                if w in unseen:
                    unseen.remove(w);piece.add(w);stack.append(w)
        pieces.append(piece)
    return pieces

def construct():
    assert len({pow(G,i,P) for i in range(P-1)})==P-1
    assert ALPHA==18
    half={pow(G,2*A*i+j,P) for i in range(Q) for j in range(A)}
    sides=[]
    for sign in (1,-1):
        side={frozenset((sign*x%P,sign*ALPHA*x%P)) for x in half}
        assert len(side)==36
        sides.append(side)
    assert not sides[0]&sides[1]
    colors=[set() for _ in range(36)]
    slot={}
    inv2=pow(2,-1,P)
    for d in range(1,37):
        for h in range(P):
            v=(h+d)%P
            leaf=(h+v)*inv2%P
            edge=frozenset((h,v))
            assert edge not in slot
            slot[edge]=(d-1,leaf)
            colors[d-1]|={(h,leaf),(v,leaf)}
    assert all(len(components(C))==1 for C in colors)
    page=set()
    for i,side in enumerate(sides):
        for edge in side:
            h,v=((x+1)%P for x in edge)
            key=frozenset((h,v))
            d,leaf=slot[key]
            old={(h,leaf),(v,leaf)}
            assert old<=colors[d]
            colors[d]-=old
            colors[d]|={(h,P+i),(v,P+i)}
            page|=old
            slot[key]=(d,P+i)
    colors.append(page)
    assert all(len(components(C))==1 for C in colors[:-1])
    assert len(components(page))==A
    return colors

def audit():
    audit_scaled_template()
    colors=construct()
    square_colors=[c for move in MOVES[::2] for c in move[:2]]
    assert len(square_colors)==len(set(square_colors))==6
    page_spokes=[e for move in MOVES[1::2] for e in move[4:6]]
    assert len(page_spokes)==len(set(page_spokes))==6
    expected=4
    for i,(ci,cj,e1,e2,f1,f2) in enumerate(MOVES):
        assert e1[0]!=e2[0] and e1[1]!=e2[1]
        assert f1==(e1[0],e2[1]) and f2==(e2[0],e1[1])
        assert {e1,e2}<=colors[ci] and {f1,f2}<=colors[cj]
        colors[ci]-={e1,e2};colors[ci]|={f1,f2}
        colors[cj]-={f1,f2};colors[cj]|={e1,e2}
        assert all(len(components(C))==1 for C in colors[:-1])
        if i%2==1:
            expected-=1
        assert len(components(colors[-1]))==expected
    assert expected==1
    singles={(h,h) for h in range(P)}|{(1,P),(1,P+1)}
    seen=set(singles)
    assert len(singles)==75
    for i,C in enumerate(colors):
        assert len(C)==2*(P-(i==36))
        pieces=components(C)
        assert len(pieces)==1
        hubs={h for h,l in C}
        leaves={l for h,l in C}
        assert hubs==(set(range(P)) if i<36 else set(range(P))-{1})
        assert len(leaves)==P-(i==36)
        assert not C&seen
        seen|=C
    assert seen=={(h,l) for h in range(P) for l in range(P+2)}
    assert len(singles)+len(colors)==112
    print('PASS K73,75: 75 singletons, 36 full cycles, 1 short cycle; '
          'page components 4→3→2→1; 112 optimal parts; all 5475 spokes exact')

if __name__=='__main__':audit()
