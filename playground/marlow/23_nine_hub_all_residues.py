"""Verify exact K_(9,t) cycle/edge partitions from explicit seed witnesses.

Run: python3 -I playground/marlow/23_nine_hub_all_residues.py
The JSON certificates, not the search solver, are the proof witnesses.
"""

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SEEDS = json.loads((HERE / '23_nine_hub_seeds.json').read_text())
assert set(SEEDS) == {str(t) for t in range(10, 17)}


def offset_cycle(m, first_offset, start):
    return {'hubs': [(-j) % m for j in range(m)],
            'leaves': [start + ((-j + first_offset) % m)
                       for j in range(m)]}


def base(t):
    if t == 8:
        return {'singleton_spokes': [[8, leaf] for leaf in range(8)],
                'cycles': [offset_cycle(8, offset, 0)
                           for offset in range(0, 8, 2)]}
    if t == 9:
        return {'singleton_spokes': [[hub, hub] for hub in range(9)],
                'cycles': [offset_cycle(9, offset, 0)
                           for offset in range(1, 9, 2)]}
    assert 10 <= t <= 16
    return SEEDS[str(t)]


def certificate(t):
    assert t >= 8
    b = 8 + (t-8) % 9
    q = (t-b)//9
    datum = base(b)
    singleton = [tuple(edge) for edge in datum['singleton_spokes']]
    cycles = list(datum['cycles'])
    for block in range(q):
        start = b + 9*block
        singleton.extend((hub, start+hub) for hub in range(9))
        cycles.extend(offset_cycle(9, offset, start)
                      for offset in range(1, 9, 2))
    seen = {}
    for edge in singleton:
        assert 0 <= edge[0] < 9 and 0 <= edge[1] < t
        assert edge not in seen, edge
        seen[edge] = 'S'
    for index, cycle in enumerate(cycles):
        hubs, leaves = cycle['hubs'], cycle['leaves']
        assert 2 <= len(hubs) == len(leaves) <= 9
        assert len(set(hubs)) == len(hubs)
        assert len(set(leaves)) == len(leaves)
        for i, hub in enumerate(hubs):
            assert 0 <= hub < 9
            for leaf in (leaves[i], leaves[i-1]):
                assert 0 <= leaf < t
                edge = (hub, leaf)
                assert edge not in seen, (t, index, edge)
                seen[edge] = index
    assert set(seen) == {(hub, leaf) for hub in range(9) for leaf in range(t)}
    assert len(singleton) == t
    assert len(cycles) == (4*t+8)//9
    assert len(singleton)+len(cycles) == t+(4*t+8)//9
    return seen, singleton, cycles


def draw(path):
    t = 11
    seen, singleton, cycles = certificate(t)
    colors = ('#5275ad', '#ba784f', '#3f9889', '#9b78b4', '#617d69')
    paper, ink, muted = '#f7f4ed', '#26323d', '#606b72'
    parts = [f'<rect width="1080" height="650" fill="{paper}"/>',
             f'<text x="42" y="53" font-size="27" fill="{ink}">Eleven leaves, five cycles, one missing hub</text>',
             f'<text x="42" y="81" font-size="16" fill="{muted}">K₉,₁₁ · each cell is one spoke · 11 singletons + 5 cycles = 16 parts</text>']
    x0, y0, cell = 101, 138, 40
    for leaf in range(t):
        parts.append(f'<text x="{x0+leaf*cell+18}" y="{y0-13}" text-anchor="middle" font-size="14" fill="{ink}">L{leaf}</text>')
    for hub in range(9):
        y = y0+hub*cell
        parts.append(f'<text x="{x0-14}" y="{y+25}" text-anchor="end" font-size="15" fill="{ink}">H{hub}</text>')
        for leaf in range(t):
            x = x0+leaf*cell
            role = seen[(hub,leaf)]
            color = '#d1a555' if role == 'S' else colors[role]
            label = 'S' if role == 'S' else str(role+1)
            parts.append(f'<rect x="{x}" y="{y}" width="36" height="36" rx="4" fill="{color}"/>')
            parts.append(f'<text x="{x+18}" y="{y+24}" text-anchor="middle" font-size="15" fill="#fffdf8">{label}</text>')
    parts += [f'<text x="610" y="174" font-size="21" fill="{ink}">Why 16 is optimal</text>',
              f'<text x="610" y="213" font-size="16" fill="{muted}">s=11+X; parity makes X even.</text>',
              f'<text x="610" y="242" font-size="16" fill="{muted}">r+s ≥ 11+44/9+17X/18.</text>',
              f'<text x="610" y="286" font-size="16" fill="{muted}">X≥2 forces more than 16 parts;</text>',
              f'<text x="610" y="315" font-size="16" fill="{muted}">so an optimum has 11 singletons.</text>',
              f'<text x="610" y="359" font-size="16" fill="{muted}">Then 44 visits need ≥5 cycles.</text>',
              f'<text x="610" y="424" font-size="16" fill="{muted}">Four cycles visit all 9 hubs;</text>',
              f'<text x="610" y="453" font-size="16" fill="{muted}">the fifth visits 8 hubs.</text>',
              f'<text x="42" y="568" font-size="17" fill="{ink}">Seeds K₉,₈ through K₉,₁₆ cover all nine residues; append nine-leaf blocks for every larger t.</text>',
              f'<text x="42" y="616" font-size="13" fill="{muted}">Exact checked edge partition · search-found finite witnesses, modular all-t lift · Marlow</text>']
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 650" width="1080" height="650" role="img" aria-label="K nine eleven spoke matrix showing eleven singleton edges and five cycles">' + ''.join(parts) + '</svg>\n')


def main():
    for t in range(8, 201):
        certificate(t)
    draw(HERE / 'art/nine_hub_eleven.svg')
    print('Verified K_(9,t) witnesses through t=200; modular lift proves all t>=8.')
    print('Wrote nine-by-eleven spoke matrix.')


if __name__ == '__main__':
    main()
