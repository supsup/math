"""Replay six two-trade repairs for the first odd base at p=5 mod 8.

Run: python3 -I playground/marlow/55_skew_two_trade_first_step.py
These are finite certificates, not a class-level existence proof.
"""

from collections import Counter, defaultdict


TRADES = {
    13: (((0, 2), (0, 6), (1, 8), (0, 8), (1, 6)),
         ((0, 6), (0, 7), (8, 2), (0, 2), (8, 7))),
    29: (((0, 2), (5, 19), (6, 21), (5, 21), (6, 19)),
         ((0, 14), (4, 18), (5, 21), (4, 21), (5, 18))),
    37: (((0, 2), (0, 18), (1, 20), (0, 20), (1, 18)),
         ((0, 18), (0, 19), (23, 5), (0, 5), (23, 19))),
    53: (((0, 2), (9, 35), (10, 37), (9, 37), (10, 35)),
         ((0, 26), (9, 37), (48, 21), (9, 21), (48, 37))),
    61: (((0, 2), (16, 46), (17, 48), (16, 48), (17, 46)),
         ((0, 30), (16, 47), (38, 8), (16, 8), (38, 47))),
    101: (((0, 2), (21, 71), (22, 73), (21, 73), (22, 71)),
          ((0, 50), (22, 72), (54, 3), (22, 3), (54, 72))),
}


def pair(u, v):
    return (u, v) if u < v else (v, u)


def primitive_root(p):
    prime_divisors = {
        q for q in range(2, p) if (p-1) % q == 0 and
        all(q % d for d in range(2, int(q**0.5)+1))
    }
    for g in range(2, p):
        if all(pow(g, (p-1)//q, p) != 1 for q in prime_divisors):
            return g
    raise ValueError(p)


def components(spokes):
    neighbors = defaultdict(set)
    for hub, leaf in spokes:
        neighbors[('h', hub)].add(('l', leaf))
        neighbors[('l', leaf)].add(('h', hub))
    assert all(len(v) == 2 for v in neighbors.values())
    unseen = set(neighbors)
    sizes = []
    while unseen:
        stack = [unseen.pop()]
        size = 0
        while stack:
            size += 1
            for v in neighbors[stack.pop()]:
                if v in unseen:
                    unseen.remove(v)
                    stack.append(v)
        assert size % 2 == 0
        sizes.append(size//2)
    return sorted(sizes)


def build(p,g=None):
    assert p % 8 == 5 and all(p % d for d in range(2,int(p**0.5)+1))
    k,t=(p-1)//2,(p-1)//4
    g=primitive_root(p) if g is None else g
    assert len({pow(g,i,p) for i in range(p-1)})==p-1
    assert t % 2 == 1
    half={pow(g,4*i+j,p) for i in range(t) for j in range(2)}
    first={pair(x,pow(g,2,p)*x%p) for x in half}
    second={pair(-u%p,-v%p) for u,v in first}
    assert first.isdisjoint(second)
    for side in (first,second):
        assert len(side)==k
        assert {x for e in side for x in e}==set(range(1,p))
        assert {min((u-v)%p,(v-u)%p) for u,v in side}==set(range(1,k+1))
    mids={(u+v)*pow(2,-1,p)%p for u,v in first|second}
    assert mids==set(range(1,p))
    colors=[set() for _ in range(k)]
    slots={}
    for d in range(1,k+1):
        for u in range(p):
            v=(u+d)%p
            m=(u+v)*pow(2,-1,p)%p
            e=pair(u,v)
            assert e not in slots
            slots[e]=(d-1,m)
            colors[d-1].update({(u,m),(v,m)})
    assert all(components(c)==[p] for c in colors)
    page=set()
    displaced=[]
    for side,matching in enumerate((first,second)):
        new_leaf=p+side
        for u,v in matching:
            x,y=(u+1)%p,(v+1)%p
            ci,old_leaf=slots[pair(x,y)]
            old={(x,old_leaf),(y,old_leaf)}
            assert old<=colors[ci]
            colors[ci].difference_update(old)
            colors[ci].update({(x,new_leaf),(y,new_leaf)})
            page.update(old)
            displaced.append(old_leaf)
            slots[pair(x,y)]=(ci,new_leaf)
    assert len(set(displaced))==p-1
    colors.append(page)
    singles={(hub,hub) for hub in range(p)}|{(1,p),(1,p+1)}
    assert all(components(c)==[p] for c in colors[:k])
    assert components(colors[k])==[2*t,2*t]
    return singles,colors


def exchange(colors,move):
    (ci,cj),e1,e2,f1,f2=move
    u,x=e1;v,y=e2
    assert u!=v and x!=y and f1==(u,y) and f2==(v,x)
    assert {e1,e2}<=colors[ci] and {f1,f2}<=colors[cj]
    colors[ci].difference_update({e1,e2})
    colors[ci].update({f1,f2})
    colors[cj].difference_update({f1,f2})
    colors[cj].update({e1,e2})


def verify(p,singles,colors):
    t=p+2;k=(p-1)//2
    assert len(singles)==t and len(colors)==k+1
    seen=set()
    for part in [singles,*colors]:
        for a,b in part:
            assert 0<=a<p and 0<=b<t and (a,b) not in seen
            seen.add((a,b))
    assert seen=={(a,b) for a in range(p) for b in range(t)}
    assert all(components(c)==[p-(i==k)] for i,c in enumerate(colors))
    assert len(singles)+len(colors)==t+(k*t+p-1)//p


def algebraic_template(p,g=None):
    """Return the conditional two-trade formula, or a failed hypothesis."""
    assert p % 8 == 5 and all(p % d for d in range(2,int(p**0.5)+1))
    g=primitive_root(p) if g is None else g
    assert len({pow(g,i,p) for i in range(p-1)})==p-1
    a=g*g%p
    inv=lambda value:pow(value%p,-1,p)
    half=inv(2)
    D=(a-1)**2%p
    Z=(1+3*a)*inv(D)%p
    W=a*(a+3)*inv(D)%p
    if not Z or not W:
        return None,'degenerate'
    if pow(W*inv(Z)%p,(p-1)//2,p)!=p-1:
        return None,'same component'
    b,v=(1+Z)%p,(1+W)%p
    mu=lambda d:d*(1+a)*inv(2*(a-1))%p
    selected=lambda d:{(1+mu(d))%p,(1-mu(d))%p}
    needed1={(b-half)%p,(b+half)%p,(b+3*half)%p,(v+half)%p}
    needed3={(b-half)%p,(b+3*half)%p}
    if needed1 & selected(1) or needed3 & selected(3):
        return None,'selected slot'
    m,y=(b+half)%p,(v+half)%p
    first=((0,2),(b,(b-half)%p),((b+1)%p,(b+3*half)%p),
           (b,(b+3*half)%p),((b+1)%p,(b-half)%p))
    second=((0,(p-1)//2),(b,m),(v,y),(b,y),(v,m))
    return (first,second),'ready'


def main():
    for p,moves in TRADES.items():
        singles,colors=build(p)
        k=(p-1)//2
        assert moves[0][0]==(0,2) and moves[1][0]==(0,k)
        exchange(colors,moves[0])
        assert all(components(c)==[p] for c in colors[:k])
        assert components(colors[k])==[(p-1)//2]*2
        exchange(colors,moves[1])
        verify(p,singles,colors)
        print(f'p={p} first odd base t={p+2}: two trades, '
              f'{len(singles)+len(colors)} optimal parts, all spokes exact')
    for p in (13,29,37,53,61,101):
        moves,status=algebraic_template(p)
        if p in (37,61,101):
            assert status=='ready'
            singles,colors=build(p)
            for move in moves:
                exchange(colors,move)
            verify(p,singles,colors)
        else:
            assert status in ('degenerate','same component')
    assert algebraic_template(157)[1]=='selected slot'
    # Different primitive roots can satisfy the same proved criterion when
    # the least root fails it. These four are direct full-partition checks.
    for p,g in ((29,11),(53,18),(109,11),(157,72)):
        moves,status=algebraic_template(p,g)
        assert status=='ready'
        singles,colors=build(p,g)
        for move in moves:
            exchange(colors,move)
        verify(p,singles,colors)
    print('Changed-root formula repairs also verified at p=29,53,109,157')
    scan=Counter(algebraic_template(p)[1] for p in range(13,1001,8)
                 if all(p % d for d in range(2,int(p**0.5)+1)))
    assert scan=={'ready':21,'same component':18,
                  'degenerate':2,'selected slot':1}
    print('Conditional template, primes 13..1000: '
          '21 ready, 18 same-component, 2 degenerate, 1 selected-slot failure')


if __name__=='__main__':
    main()
