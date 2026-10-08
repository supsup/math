"""Build nineteen exact odd bases from a repairable two-cycle 41-hub page.

Run: python3 -I playground/marlow/52_fortyone_hub_two_cycle_growth.py
Each prefix is constructed anew; each split page is reconnected by a
support-preserving four-edge trade. The program saves ordered cycle walks.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
H, K = 41, 20
INV2 = pow(2, -1, H)
MATCHINGS = (
    ((22, 23), (11, 13), (4, 7), (12, 16), (33, 38),
     (26, 32), (39, 5), (35, 2), (20, 29), (37, 6),
     (8, 19), (15, 27), (21, 34), (17, 31), (3, 18),
     (24, 40), (25, 1), (10, 28), (36, 14), (30, 9)),
    ((28, 29), (22, 24), (5, 8), (34, 38), (35, 40),
     (25, 31), (6, 13), (7, 15), (10, 19), (32, 1),
     (12, 23), (14, 26), (30, 2), (3, 17), (18, 33),
     (36, 11), (4, 21), (9, 27), (20, 39), (37, 16)),
)
CENTERS = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19,
           24, 26, 28, 30, 32, 34, 36, 38, 40)


def edge(u, v):
    return tuple(sorted((u, v)))


def components(spokes):
    adj = defaultdict(set)
    for hub, leaf in spokes:
        adj[('h', hub)].add(('l', leaf))
        adj[('l', leaf)].add(('h', hub))
    assert all(len(ns) == 2 for ns in adj.values())
    unseen, result = set(adj), []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        stack, part = [root], {root}
        while stack:
            vertex = stack.pop()
            for neighbor in sorted(adj[vertex]):
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    part.add(neighbor)
                    stack.append(neighbor)
        result.append(part)
    return sorted(result, key=lambda c: min(v for kind, v in c if kind == 'h'))


def walk(spokes):
    assert len(components(spokes)) == 1
    by_hub, by_leaf = defaultdict(set), defaultdict(set)
    for hub, leaf in spokes:
        by_hub[hub].add(leaf)
        by_leaf[leaf].add(hub)
    hub = min(by_hub)
    leaf = min(by_hub[hub])
    hubs, leaves = [], []
    while True:
        hubs.append(hub)
        leaves.append(leaf)
        next_hub = next(v for v in by_leaf[leaf] if v != hub)
        if next_hub == hubs[0]:
            break
        next_leaf = next(v for v in by_hub[next_hub] if v != leaf)
        hub, leaf = next_hub, next_leaf
    assert len(hubs) == len(leaves) == len(by_hub) == len(by_leaf)
    assert len(set(hubs)) == len(hubs) and len(set(leaves)) == len(leaves)
    assert {(a, b) for i, a in enumerate(hubs)
            for b in (leaves[i], leaves[i-1])} == spokes
    return {'hubs': hubs, 'leaves': leaves}


def check_page():
    all_edges, mids = set(), set()
    displacement = Counter()
    assert all(len(side) == K for side in MATCHINGS)
    for side in MATCHINGS:
        vertices = []
        for d, (u, v) in enumerate(side, 1):
            assert min((u-v) % H, (v-u) % H) == d
            assert edge(u, v) not in all_edges
            all_edges.add(edge(u, v))
            vertices.extend((u, v))
            midpoint = (u+v)*INV2 % H
            assert midpoint and midpoint not in mids
            mids.add(midpoint)
        assert set(vertices) == set(range(1, H))
    assert mids == set(range(1, H))
    for (u, v), (x, y) in zip(*MATCHINGS):
        shift = ((x+y)-(u+v))*INV2 % H
        displacement[min(shift, H-shift)] += 1
    assert displacement[1] == 4
    assert all(count == 1 for d, count in displacement.items() if d != 1)
    page_spokes = {(hub, (u+v)*INV2 % H)
                   for side in MATCHINGS for u, v in side for hub in (u, v)}
    assert sorted(len(c)//2 for c in components(page_spokes)) == [8, 32]
    assert len(CENTERS) == K-1 and len(set(CENTERS)) == K-1
    assert all((a-b) % H not in (1, H-1)
               for a in CENTERS for b in CENTERS if a != b)
    for shift in range(1, H):
        translated = {edge((u+shift) % H, (v+shift) % H)
                      for u, v in all_edges}
        assert len(all_edges & translated) == displacement[min(shift, H-shift)]


def square():
    colors, slots = [set() for _ in range(K)], {}
    for d in range(1, K+1):
        for u in range(H):
            v = (u+d) % H
            midpoint = (u+v)*INV2 % H
            pair = edge(u, v)
            assert pair not in slots
            slots[pair] = (d-1, midpoint)
            colors[d-1].update({(u, midpoint), (v, midpoint)})
    assert len(slots) == H*K
    assert all(len(c) == 2*H and len(components(c)) == 1 for c in colors)
    return {(a, a) for a in range(H)}, colors, slots


def grow(prefix):
    singles, colors, slots = square()
    for step, center in enumerate(CENTERS[:prefix]):
        page, displaced = set(), []
        for parity, side in enumerate(MATCHINGS):
            new_leaf = H+2*step+parity
            for u, v in side:
                x, y = (u+center) % H, (v+center) % H
                color, old_leaf = slots[edge(x, y)]
                old_spokes = {(x, old_leaf), (y, old_leaf)}
                assert old_spokes <= colors[color]
                colors[color].difference_update(old_spokes)
                colors[color].update({(x, new_leaf), (y, new_leaf)})
                page.update(old_spokes)
                displaced.append(old_leaf)
                slots[edge(x, y)] = color, new_leaf
        assert len(page) == 2*(H-1) and len(set(displaced)) == H-1
        assert sorted(len(c)//2 for c in components(page)) == [8, 32]
        colors.append(page)
        singles.update({(center, H+2*step), (center, H+2*step+1)})
    assert all(len(components(c)) == 1 for c in colors[:K])
    return singles, colors


def repair(colors):
    colors = [set(c) for c in colors]
    trace = []
    for target in range(K, len(colors)):
        parts = components(colors[target])
        assert len(parts) == 2
        candidates_by_part = [
            sorted(e for e in colors[target] if ('h', e[0]) in part)
            for part in parts
        ]
        owners = {
            spoke: color
            for color, part in enumerate(colors)
            if color != target and len(components(part)) == 1
            for spoke in part
        }
        candidates = []
        for u, x in candidates_by_part[0]:
            for v, y in candidates_by_part[1]:
                cross1, cross2 = (u, y), (v, x)
                color = owners.get(cross1)
                if color is None or owners.get(cross2) != color:
                    continue
                p_new = (colors[target] - {(u, x), (v, y)}) | {cross1, cross2}
                q_new = (colors[color] - {cross1, cross2}) | {(u, x), (v, y)}
                if len(components(p_new)) == len(components(q_new)) == 1:
                    candidates.append((color >= K, color, (u, x), (v, y),
                                       cross1, cross2, p_new, q_new))
        assert candidates, f'no repair for page color {target}'
        _, color, p1, p2, q1, q2, p_new, q_new = min(
            candidates, key=lambda c: c[:6])
        assert {a for a, _ in p_new} == {a for a, _ in colors[target]}
        assert {b for _, b in p_new} == {b for _, b in colors[target]}
        assert {a for a, _ in q_new} == {a for a, _ in colors[color]}
        assert {b for _, b in q_new} == {b for _, b in colors[color]}
        colors[target], colors[color] = p_new, q_new
        trace.append({'page_color': target, 'partner_color': color,
                      'page_old_spokes': [p1, p2],
                      'partner_old_spokes': [q1, q2]})
    assert all(len(components(c)) == 1 for c in colors)
    return colors, trace


def verify_odd(prefix, singles, colors):
    t = H+2*prefix
    assert len(singles) == t and len(colors) == K+prefix
    universe = {(hub, leaf) for hub in range(H) for leaf in range(t)}
    used = set()
    for part in [singles, *colors]:
        assert part <= universe and not (used & part)
        used |= part
    assert used == universe
    for i, color in enumerate(colors):
        assert len(color) == (2*H if i < K else 2*(H-1))
        assert len({a for a, _ in color}) == len(color)//2
        assert len({b for _, b in color}) == len(color)//2
        assert len(components(color)) == 1
    assert len(singles)+len(colors) == t+(K*t+H-1)//H


def main():
    check_page()
    seeds, traces = {}, {}
    for prefix in range(1, K):
        singles, colors = grow(prefix)
        colors, trace = repair(colors)
        verify_odd(prefix, singles, colors)
        t = H+2*prefix
        seeds[str(t)] = {
            'singleton_spokes': sorted(map(list, singles)),
            'cycles': [walk(color) for color in colors],
        }
        traces[str(t)] = trace
    output = {
        'matchings': {'even': MATCHINGS[0], 'odd': MATCHINGS[1]},
        'centers': CENTERS,
        'traces': traces,
        'seeds': seeds,
    }
    (HERE / '52_fortyone_hub_switch_seeds.json').write_text(
        json.dumps(output, separators=(',', ':'), sort_keys=True)+'\n')
    print('Verified all 19 repaired odd bases t=43..79; '
          'saved ordered walks and repair traces.')


if __name__ == '__main__':
    main()
