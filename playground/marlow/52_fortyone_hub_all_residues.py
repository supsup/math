"""Independently verify all K_(41,t) base residues and sample lifts.

Run: python3 -I playground/marlow/52_fortyone_hub_all_residues.py
The odd-base JSON walks are checked directly as edge partitions, without
importing or running the two-cycle growth and repair generator.
"""

import json
from pathlib import Path


H, K = 41, 20
HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / '52_fortyone_hub_switch_seeds.json').read_text())
SEEDS = DATA['seeds']
CENTERS = DATA['centers']
assert set(SEEDS) == {str(H+2*j) for j in range(1, K)}


def offset_cycle(offset, start):
    return {'hubs': [(-i) % H for i in range(H)],
            'leaves': [start+((-i+offset) % H) for i in range(H)]}


def base_certificate(base):
    assert H-1 <= base <= 2*H-2
    if base % 2 == 0:
        half = base//2
        singles = [(H-1, leaf) for leaf in range(base)]
        cycles = [
            {'hubs': list(range(H-1)),
             'leaves': [2*((shift+j) % half)+parity
                        for j in range(K) for parity in (0, 1)]}
            for shift in range(half)
        ]
    elif base == H:
        singles = [(hub, hub) for hub in range(H)]
        cycles = [offset_cycle(offset, 0) for offset in range(1, H, 2)]
    else:
        seed = SEEDS[str(base)]
        singles = [tuple(spoke) for spoke in seed['singleton_spokes']]
        cycles = seed['cycles']
        prefix = (base-H)//2
        assert sorted(len(c['hubs']) for c in cycles) == [H-1]*prefix + [H]*K
        singleton_degree = [sum(a == hub for a, _ in singles)
                            for hub in range(H)]
        assert {hub for hub, degree in enumerate(singleton_degree)
                if degree == 3} == set(CENTERS[:prefix])
        assert all(degree in (1, 3) for degree in singleton_degree)
        omitted_hubs = [set(range(H))-set(c['hubs'])
                        for c in cycles if len(c['hubs']) == H-1]
        assert {next(iter(missing)) for missing in omitted_hubs} == set(CENTERS[:prefix])
    return singles, cycles


def certificate(base, blocks=0):
    assert H-1 <= base <= 2*H-2 and blocks >= 0
    singles, cycles = base_certificate(base)
    singles, cycles = list(singles), list(cycles)
    for block in range(blocks):
        start = base+H*block
        singles.extend((hub, start+hub) for hub in range(H))
        cycles.extend(offset_cycle(offset, start) for offset in range(1, H, 2))
    t = base+H*blocks
    seen = set()
    for hub, leaf in singles:
        assert 0 <= hub < H and 0 <= leaf < t and (hub, leaf) not in seen
        seen.add((hub, leaf))
    for cycle in cycles:
        hubs, leaves = cycle['hubs'], cycle['leaves']
        assert 2 <= len(hubs) == len(leaves) <= H
        assert len(set(hubs)) == len(hubs)
        assert len(set(leaves)) == len(leaves)
        for i, hub in enumerate(hubs):
            assert 0 <= hub < H
            for leaf in (leaves[i], leaves[i-1]):
                assert 0 <= leaf < t and (hub, leaf) not in seen, (t, hub, leaf)
                seen.add((hub, leaf))
    assert seen == {(hub, leaf) for hub in range(H) for leaf in range(t)}
    assert len(singles) == t
    assert len(cycles) == (K*t+H-1)//H
    return singles, cycles


def draw(path):
    paper, ink, muted = '#f7f4ed', '#25313a', '#5e6c75'
    blue, green, amber = '#567aa5', '#3b927e', '#b47751'
    width, gap, x0 = 60, 8, 30
    parts = [
        f'<rect width="2830" height="455" fill="{paper}"/>',
        f'<text x="30" y="49" font-size="27" fill="{ink}">Forty-one hubs: every base residue opens</text>',
        f'<text x="30" y="79" font-size="15" fill="{muted}">t = 40,…,80 · every 41-leaf offset block adds 61 parts</text>',
    ]
    for base in range(H-1, 2*H-1):
        x = x0+(base-(H-1))*(width+gap)
        color, label = ((blue, 'weave') if base % 2 == 0 else
                        (green, 'square') if base == H else
                        (amber, 'switch'))
        count = base+(K*base+H-1)//H
        parts.extend([
            f'<rect x="{x}" y="125" width="{width}" height="172" rx="8" fill="#fffdf9" stroke="#d8d4ca"/>',
            f'<rect x="{x}" y="125" width="{width}" height="8" fill="{color}"/>',
            f'<text x="{x+width/2}" y="169" text-anchor="middle" font-size="21" fill="{ink}">{base}</text>',
            f'<text x="{x+width/2}" y="197" text-anchor="middle" font-size="11" fill="{color}">{label}</text>',
            f'<text x="{x+width/2}" y="232" text-anchor="middle" font-size="12" fill="{muted}">parts</text>',
            f'<text x="{x+width/2}" y="264" text-anchor="middle" font-size="20" fill="{ink}">{count}</text>',
        ])
    parts.extend([
        f'<text x="30" y="344" font-size="17" fill="{ink}">Blue: 21 even-side weaves. Green: affine square. Amber: 19 translated two-cycle pages repaired by four-edge trades.</text>',
        f'<text x="30" y="377" font-size="17" fill="{ink}">Each construction reaches the singleton and cycle-capacity lower bound.</text>',
        f'<text x="30" y="427" font-size="13" fill="{muted}">Finite theorem for h=41 · nineteen independently checkable odd-base walks · Marlow</text>',
    ])
    path.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2830 455" '
        'width="2830" height="455" role="img" '
        'aria-label="All forty-one base residues at forty-one hubs, by even weave, affine square, and repaired two-cycle pages" '
        'font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n'
    )


def main():
    for base in range(H-1, 2*H-1):
        for blocks in range(12):
            certificate(base, blocks)
    draw(HERE / 'art/fortyone_hub_residue_ladder.svg')
    print('Independently verified all 41 base residues and 11 lifts per base.')


if __name__ == '__main__':
    main()
