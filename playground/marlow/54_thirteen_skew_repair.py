"""Replay all five repaired antipodal-starter growth bases at thirteen hubs.

Run: python3 -I playground/marlow/54_thirteen_skew_repair.py
The saved trades are exact spoke exchanges, not solver instructions.
"""

import json
from collections import defaultdict
from pathlib import Path


H, K = 13, 6
HERE = Path(__file__).resolve().parent
TRACES = json.loads((HERE / '54_thirteen_skew_repair_traces.json').read_text())
assert set(TRACES) == {str(j) for j in range(1, K)}


def pair(u, v):
    return (u, v) if u < v else (v, u)


def components(spokes):
    adjacent = defaultdict(set)
    for hub, leaf in spokes:
        adjacent[('h', hub)].add(('l', leaf))
        adjacent[('l', leaf)].add(('h', hub))
    assert all(len(neighbors) == 2 for neighbors in adjacent.values())
    remaining = set(adjacent)
    count = 0
    while remaining:
        count += 1
        stack = [remaining.pop()]
        while stack:
            for neighbor in adjacent[stack.pop()]:
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    stack.append(neighbor)
    return count


def matchings():
    g, A, t = 2, 2, 3
    a = pow(g, A, H)
    half = {pow(g, 2*i*A+j, H) for i in range(t) for j in range(A)}
    first = {pair(x, a*x % H) for x in half}
    second = {pair(-u % H, -v % H) for u, v in first}
    assert len(first) == len(second) == K and first.isdisjoint(second)
    assert {min((u-v) % H, (v-u) % H) for u,v in first} == set(range(1,K+1))
    assert {min((u-v) % H, (v-u) % H) for u,v in second} == set(range(1,K+1))
    mids = {((u+v)*pow(2,-1,H))%H for u,v in first|second}
    assert mids == set(range(1,H))
    return sorted(first), sorted(second)


def square():
    singles = {(hub, hub) for hub in range(H)}
    colors = [set() for _ in range(K)]
    slots = {}
    for d in range(1,K+1):
        for u in range(H):
            v = (u+d)%H
            midpoint = (u+v)*pow(2,-1,H)%H
            edge = pair(u,v)
            assert edge not in slots
            slots[edge] = (d-1,midpoint)
            colors[d-1].update({(u,midpoint),(v,midpoint)})
    assert all(len(c)==2*H and components(c)==1 for c in colors)
    return singles,colors,slots


def grow(prefix):
    singles,colors,slots=square()
    sides=matchings()
    for step in range(prefix):
        center=step+1
        page=set()
        displaced=[]
        for side,matching in enumerate(sides):
            fresh_leaf=H+2*step+side
            for u,v in matching:
                x,y=(u+center)%H,(v+center)%H
                color,old_leaf=slots[pair(x,y)]
                old={(x,old_leaf),(y,old_leaf)}
                assert old <= colors[color]
                colors[color].difference_update(old)
                colors[color].update({(x,fresh_leaf),(y,fresh_leaf)})
                page.update(old)
                displaced.append(old_leaf)
                slots[pair(x,y)]=(color,fresh_leaf)
        assert len(page)==2*(H-1) and len(set(displaced))==H-1
        colors.append(page)
        singles.update({(center,H+2*step),(center,H+2*step+1)})
    assert [components(c) for c in colors] == [1]*K+[2]*prefix
    return singles,colors


def apply_trade(colors, move):
    first,second,*spokes=move
    e1,e2,f1,f2=map(tuple,spokes)
    u,x=e1;v,y=e2
    assert u!=v and x!=y and f1==(u,y) and f2==(v,x)
    assert {e1,e2} <= colors[first] and {f1,f2} <= colors[second]
    colors[first].difference_update({e1,e2})
    colors[first].update({f1,f2})
    colors[second].difference_update({f1,f2})
    colors[second].update({e1,e2})
    assert all(len(c) == 2*(H-(i>=K)) for i,c in enumerate(colors))


def verify(prefix,singles,colors):
    t=H+2*prefix
    assert len(singles)==t and len(colors)==K+prefix
    assert [components(c) for c in colors] == [1]*(K+prefix)
    seen=set()
    for part in [singles,*colors]:
        for hub,leaf in part:
            assert 0<=hub<H and 0<=leaf<t and (hub,leaf) not in seen
            seen.add((hub,leaf))
    assert seen=={(hub,leaf) for hub in range(H) for leaf in range(t)}
    for i,color in enumerate(colors):
        n=H-(i>=K)
        assert len(color)==2*n
        assert len({a for a,_ in color})==len({b for _,b in color})==n
    assert len(singles)+len(colors)==t+(K*t+H-1)//H


def main():
    for prefix in range(1,K):
        singles,colors=grow(prefix)
        before=sum(components(c) for c in colors)
        for move in TRACES[str(prefix)]:
            apply_trade(colors,move)
            after=sum(components(c) for c in colors)
            assert after<=before
            before=after
        verify(prefix,singles,colors)
        print(f'K_{{13,{H+2*prefix}}}: {len(TRACES[str(prefix)])} trades; '
              f'{H+2*prefix} singletons + {len(colors)} cycles; all spokes exact')


if __name__=='__main__':
    main()
