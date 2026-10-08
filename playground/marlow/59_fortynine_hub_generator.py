"""Deterministic K_{49,t} odd-base generator; Python stdlib only.

Writes a generated JSON beside this file. The hard-coded 24-edge strong
starter was found by CP-SAT, but generation and verification need no solver.
A trace tuple (target, partner, target_spoke_1, target_spoke_2,
partner_spoke_1, partner_spoke_2) records a support-preserving four-edge
checkerboard trade; each spoke is a (hub, leaf) pair.
"""
import json
from collections import defaultdict
from pathlib import Path

H, K, INV2 = 49, 24, 25
STARTER = (
    (1, 20), (2, 34), (3, 16), (4, 19), (5, 13), (6, 31),
    (7, 10), (8, 17), (9, 38), (11, 44), (12, 33), (14, 21),
    (15, 37), (18, 30), (22, 36), (23, 41), (24, 47), (25, 35),
    (26, 28), (27, 32), (29, 40), (39, 43), (42, 48), (45, 46),
)
CENTERS = tuple(range(1, 24))
MATCHINGS = (STARTER, tuple(((-u) % H, (-v) % H) for u, v in STARTER))


def edge(u, v):
    return tuple(sorted((u, v)))


def parts(spokes):
    adj = defaultdict(set)
    for hub, leaf in spokes:
        adj[('h', hub)].add(('l', leaf))
        adj[('l', leaf)].add(('h', hub))
    assert all(len(neighbors) == 2 for neighbors in adj.values())
    unseen, result = set(adj), []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        stack, component = [root], {root}
        while stack:
            for neighbor in sorted(adj[stack.pop()]):
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    stack.append(neighbor)
        result.append(component)
    return sorted(result, key=lambda c: min(v for kind, v in c if kind == 'h'))


def verify_starter():
    assert len(STARTER) == K
    assert {z for u, v in STARTER for z in (u, v)} == set(range(1, H))
    assert {min((u-v) % H, (v-u) % H) for u, v in STARTER} == set(range(1, K+1))
    mids = {(u+v)*INV2 % H for u, v in STARTER}
    assert {min(m, H-m) for m in mids} == set(range(1, K+1))
    page = {edge(u, v) for side in MATCHINGS for u, v in side}
    assert len(page) == H-1
    assert sorted(len(c)//2 for c in parts({(a,(u+v)*INV2 % H)
        for side in MATCHINGS for u,v in side for a in (u,v)})) == [24,24]
    for shift in range(1,H):
        moved = {edge((u+shift)%H,(v+shift)%H) for u,v in page}
        assert len(page & moved) == 1


def grow(prefix):
    colors, slots = [set() for _ in range(K)], {}
    for d in range(1, K+1):
        for u in range(H):
            v = (u+d) % H
            midpoint = (u+v)*INV2 % H
            pair = edge(u,v)
            assert pair not in slots
            slots[pair] = (d-1,midpoint)
            colors[d-1].update(((u,midpoint),(v,midpoint)))
    assert len(slots) == H*K
    singles = {(a,a) for a in range(H)}
    for step, center in enumerate(CENTERS[:prefix]):
        page, displaced = set(), []
        for parity, side in enumerate(MATCHINGS):
            new_leaf = H+2*step+parity
            for u,v in side:
                x,y=(u+center)%H,(v+center)%H
                color,old_leaf=slots[edge(x,y)]
                old_spokes={(x,old_leaf),(y,old_leaf)}
                assert old_spokes <= colors[color]
                colors[color].difference_update(old_spokes)
                colors[color].update(((x,new_leaf),(y,new_leaf)))
                page.update(old_spokes)
                displaced.append(old_leaf)
                slots[edge(x,y)] = color,new_leaf
        assert len(page)==2*(H-1) and len(set(displaced))==H-1
        colors.append(page)
        singles.update(((center,H+2*step),(center,H+2*step+1)))
    assert [len(parts(c)) for c in colors[:K]] == [7 if d in (6,13,20) else 1 for d in range(K)]
    assert [sorted(len(p)//2 for p in parts(c)) for c in colors[K:]] == [[24,24]]*prefix
    return singles,colors


def repair(colors):
    colors = [set(color) for color in colors]
    trace = []
    for target in (6,13,20,*range(K,len(colors))):
        while len(parts(colors[target])) > 1:
            components = parts(colors[target])
            owners = {spoke: index for index,color in enumerate(colors)
                      if index != target and len(parts(color)) == 1
                      for spoke in color}
            bypart = [sorted(spoke for spoke in colors[target]
                       if ('h',spoke[0]) in component) for component in components]
            choice = None
            for a in range(len(components)):
                if choice: break
                for b in range(a+1,len(components)):
                    if choice: break
                    for u,x in bypart[a]:
                        if choice: break
                        for v,y in bypart[b]:
                            cross1,cross2=(u,y),(v,x)
                            partner=owners.get(cross1)
                            if partner is None or owners.get(cross2)!=partner:
                                continue
                            target_new=(colors[target]-{(u,x),(v,y)})|{cross1,cross2}
                            if len(parts(target_new))!=len(components)-1:
                                continue
                            partner_new=(colors[partner]-{cross1,cross2})|{(u,x),(v,y)}
                            if len(parts(partner_new))!=1:
                                continue
                            choice=(partner,(u,x),(v,y),cross1,cross2,target_new,partner_new)
                            break
            assert choice is not None, (target,len(components))
            partner,p1,p2,q1,q2,target_new,partner_new=choice
            assert {a for a,_ in target_new}=={a for a,_ in colors[target]}
            assert {b for _,b in target_new}=={b for _,b in colors[target]}
            assert {a for a,_ in partner_new}=={a for a,_ in colors[partner]}
            assert {b for _,b in partner_new}=={b for _,b in colors[partner]}
            colors[target],colors[partner]=target_new,partner_new
            trace.append((target,partner,p1,p2,q1,q2))
    assert all(len(parts(color))==1 for color in colors)
    return colors,trace


def walk(spokes):
    by_hub,by_leaf=defaultdict(set),defaultdict(set)
    for hub,leaf in spokes:
        by_hub[hub].add(leaf);by_leaf[leaf].add(hub)
    hub=min(by_hub);leaf=min(by_hub[hub]);hubs=[];leaves=[]
    while True:
        hubs.append(hub);leaves.append(leaf)
        nxt=next(a for a in by_leaf[leaf] if a!=hub)
        if nxt==hubs[0]: break
        leaf=next(b for b in by_hub[nxt] if b!=leaf)
        hub=nxt
    assert len(hubs)==len(leaves)==len(by_hub)==len(by_leaf)
    return {'hubs':hubs,'leaves':leaves}


def verify(prefix,singles,colors):
    t=H+2*prefix
    assert len(singles)==t and len(colors)==K+prefix
    seen=set(singles)
    assert len(seen)==t
    for index,color in enumerate(colors):
        assert len(color)==2*(H if index<K else H-1)
        assert len({a for a,_ in color})==len({b for _,b in color})==len(color)//2
        assert len(parts(color))==1 and not seen&color
        seen.update(color)
    assert seen=={(a,b) for a in range(H) for b in range(t)}
    assert len(singles)+len(colors)==t+(K*t+H-1)//H


def main():
    verify_starter()
    certificates,traces={},{}
    for prefix in range(K):
        singles,colors=grow(prefix)
        colors,trace=repair(colors)
        verify(prefix,singles,colors)
        t=H+2*prefix
        assert len(trace)==18+prefix
        certificates[str(t)]={'singleton_spokes':sorted(map(list,singles)),
                              'cycles':[walk(color) for color in colors]}
        traces[str(t)]=trace
    data={'h':H,'starter_matching':STARTER,'centers':CENTERS,
          'odd_base_certificates':certificates,'repair_traces':traces}
    out=Path(__file__).with_name('59_fortynine_hub_odd_seeds.generated.json')
    out.write_text(json.dumps(data,separators=(',',':'),sort_keys=True))
    print('wrote',out,'all 24 odd bases; 18+j trades at prefix j')

if __name__=='__main__':main()
