"""Check a support-preserving two-color switch in the saved K_{9,11} seed.

Run: python3 -I playground/marlow/47_support_preserving_switch.py
"""

import json
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
SEED = json.loads((HERE / '23_nine_hub_seeds.json').read_text())['11']


def cycle_edges(walk):
    hs, ls = walk['hubs'], walk['leaves']
    assert len(hs) == len(ls) == len(set(hs)) == len(set(ls))
    return {(a, b) for i, a in enumerate(hs) for b in (ls[i], ls[i-1])}


def component_lengths(edges):
    adj = defaultdict(set)
    for a, b in edges:
        x, y = ('h', a), ('l', b)
        adj[x].add(y)
        adj[y].add(x)
    assert all(len(ns) == 2 for ns in adj.values())
    unseen = set(adj)
    sizes = []
    while unseen:
        root = unseen.pop()
        stack = [root]
        size = 0
        while stack:
            v = stack.pop()
            size += 1
            for w in adj[v]:
                if w in unseen:
                    unseen.remove(w)
                    stack.append(w)
        sizes.append(size)
    return sorted(sizes)


def draw(path):
    ink, muted, paper = '#25313a', '#63717a', '#f7f4ed'
    teal, copper = '#2d897c', '#b36c49'
    out = [f'<rect width="1050" height="560" fill="{paper}"/>',
           f'<text x="38" y="49" font-size="28" fill="{ink}">A rectangle trade can reconnect a scheduled cycle</text>',
           f'<text x="39" y="80" font-size="16" fill="{muted}">K₉,₁₁ · colors P and Q retain every hub and leaf support</text>']
    for x0, title, swapped in ((52, 'Before', False), (567, 'After', True)):
        out.extend([f'<rect x="{x0}" y="117" width="428" height="365" rx="14" fill="#fffdf9" stroke="#d7d4ca"/>',
                    f'<text x="{x0+25}" y="151" font-size="22" fill="{ink}">{title}</text>',
                    f'<text x="{x0+24}" y="183" font-size="14" fill="{muted}">hubs</text>',
                    f'<text x="{x0+331}" y="183" font-size="14" fill="{muted}">leaves</text>'])
        hx, lx = x0+81, x0+350
        top, bottom = 242, 353
        edge_colors = [(hx, top, lx, top, copper if not swapped else teal),
                       (hx, top, lx, bottom, teal if not swapped else copper),
                       (hx, bottom, lx, top, teal if not swapped else copper),
                       (hx, bottom, lx, bottom, copper if not swapped else teal)]
        for x1, y1, x2, y2, color in edge_colors:
            out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="5"/>')
        for x, y, label in ((hx, top, '0'), (hx, bottom, '3'),
                            (lx, top, '3'), (lx, bottom, '6')):
            out.extend([f'<circle cx="{x}" cy="{y}" r="20" fill="#fffdf9" stroke="{ink}" stroke-width="2"/>',
                        f'<text x="{x}" y="{y+6}" text-anchor="middle" font-size="18" fill="{ink}">{label}</text>'])
        desc = ('P: one 18-cycle  ·  Q: one 18-cycle' if not swapped
                else 'P: 14-cycle + 4-cycle  ·  Q: 18-cycle')
        out.append(f'<text x="{x0+24}" y="434" font-size="16" fill="{ink}">{desc}</text>')
    out.extend([f'<text x="522" y="310" text-anchor="middle" font-size="42" fill="{muted}">→</text>',
                f'<text x="39" y="520" font-size="16" fill="{ink}"><tspan fill="{teal}">Teal P</tspan> and <tspan fill="{copper}">copper Q</tspan> exchange four edges; reversing the arrow repairs P.</text>',
                f'<text x="1010" y="543" text-anchor="end" font-size="12" fill="{muted}">Marlow · item 47</text>'])
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1050 560" width="1050" height="560" role="img" aria-label="A two-color rectangle switch merges two P cycles while keeping Q connected, shown by reversing a checked K nine eleven split">' + ''.join(out) + '</svg>\n')


def main():
    singles = {tuple(e) for e in SEED['singleton_spokes']}
    colors = [cycle_edges(w) for w in SEED['cycles']]
    universe = {(a, b) for a in range(9) for b in range(11)}
    assert len(colors) == 5
    assert len(singles) == 11
    assert singles | set().union(*colors) == universe
    assert sum(map(len, colors)) + len(singles) == 9*11
    before = [component_lengths(c) for c in colors]
    assert before == [[18], [18], [18], [18], [16]]

    p_old, q_old = {(0, 6), (3, 3)}, {(0, 3), (3, 6)}
    assert p_old <= colors[0] and q_old <= colors[1]
    assert p_old.isdisjoint(colors[1]) and q_old.isdisjoint(colors[0])
    switched = [set(c) for c in colors]
    switched[0].difference_update(p_old)
    switched[0].update(q_old)
    switched[1].difference_update(q_old)
    switched[1].update(p_old)
    after = [component_lengths(c) for c in switched]
    assert after == [[4, 14], [18], [18], [18], [16]]
    assert singles | set().union(*switched) == universe
    assert sum(map(len, switched)) + len(singles) == 9*11
    for old, new in zip(colors, switched):
        assert {a for a, _ in old} == {a for a, _ in new}
        assert {b for _, b in old} == {b for _, b in new}
    draw(HERE / 'art/support_preserving_switch.svg')
    print('Verified K_9,11 edge coverage, scheduled supports, and components before/after switch.')


if __name__ == '__main__':
    main()
