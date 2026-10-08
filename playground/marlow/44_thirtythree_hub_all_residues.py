"""Verify exact K_{33,t} partitions for all base residues and sample lifts.

Run: python3 -I playground/marlow/44_thirtythree_hub_all_residues.py
The fifteen saved odd-base walks are data, not an algorithm for all odd hubs.
"""

import json
from pathlib import Path


H = 33
K = 16
HERE = Path(__file__).resolve().parent
SEEDS = json.loads((HERE / '44_thirtythree_hub_odd_seeds.json').read_text())
assert set(SEEDS) == {str(H + 2*j) for j in range(1, K)}


def offset_cycle(offset, start):
    return {'hubs': [(-i) % H for i in range(H)],
            'leaves': [start + ((-i + offset) % H) for i in range(H)]}


def base_certificate(base):
    assert H-1 <= base <= 2*H-2
    if base % 2 == 0:
        # Singleton hub 32, then the item-30 weave on K_{32,base}.
        m = base // 2
        singles = [(H-1, leaf) for leaf in range(base)]
        cycles = [{'hubs': list(range(H-1)),
                   'leaves': [2*((c+j) % m)+q for j in range(K) for q in (0, 1)]}
                  for c in range(m)]
    elif base == H:
        singles = [(hub, hub) for hub in range(H)]
        cycles = [offset_cycle(offset, 0) for offset in range(1, H, 2)]
    else:
        data = SEEDS[str(base)]
        singles = [tuple(edge) for edge in data['singleton_spokes']]
        cycles = data['cycles']
        j = (base-H) // 2
        assert sorted(len(c['hubs']) for c in cycles) == [H-1]*j + [H]*K
        degrees = [sum(hub == a for a, _ in singles) for hub in range(H)]
        assert sorted(degrees) == [1]*(H-j) + [3]*j
        omitted = [set(range(H))-set(c['hubs'])
                   for c in cycles if len(c['hubs']) == H-1]
        assert {next(iter(missing)) for missing in omitted} == {
            a for a, d in enumerate(degrees) if d == 3}
        assert [a for a, d in enumerate(degrees) if d == 3] == list(range(j))
        tape, prescribed = 0, []
        for length in [2*j]*K + [2*j+1]*j:
            prescribed.append(frozenset(p % base for p in range(tape, tape+length)))
            tape += length
        assert tape == j*base
        actual = [frozenset(set(range(base))-set(c['leaves'])) for c in cycles]
        assert sorted(map(sorted, prescribed)) == sorted(map(sorted, actual))
    return singles, cycles


def certificate(base, blocks=0):
    assert H-1 <= base <= 2*H-2 and blocks >= 0
    t = base + H*blocks
    singles, cycles = base_certificate(base)
    singles, cycles = list(singles), list(cycles)
    for block in range(blocks):
        start = base + H*block
        singles.extend((hub, start+hub) for hub in range(H))
        cycles.extend(offset_cycle(offset, start) for offset in range(1, H, 2))
    seen = set()
    for hub, leaf in singles:
        assert 0 <= hub < H and 0 <= leaf < t and (hub, leaf) not in seen
        seen.add((hub, leaf))
    for cycle in cycles:
        hs, ls = cycle['hubs'], cycle['leaves']
        assert 2 <= len(hs) == len(ls) <= H
        assert len(set(hs)) == len(hs) and len(set(ls)) == len(ls)
        for i, hub in enumerate(hs):
            assert 0 <= hub < H
            for leaf in (ls[i], ls[i-1]):
                assert 0 <= leaf < t and (hub, leaf) not in seen, (t, hub, leaf)
                seen.add((hub, leaf))
    assert seen == {(hub, leaf) for hub in range(H) for leaf in range(t)}
    assert len(singles) == t
    assert len(cycles) == (K*t + H-1)//H
    return singles, cycles


def draw(path):
    paper, ink, muted = '#f7f4ed', '#25313a', '#5c6970'
    even, block, witness = '#567aa5', '#3b927e', '#b47751'
    width, gap, x0 = 62, 9, 32
    parts = [f'<rect width="2450" height="420" fill="{paper}"/>',
             f'<text x="32" y="49" font-size="27" fill="{ink}">Thirty-three hubs: every base residue has a construction</text>',
             f'<text x="32" y="78" font-size="15" fill="{muted}">t = 32,…,64; each 33-leaf block adds 49 parts</text>']
    for b in range(H-1, 2*H-1):
        x = x0 + (b-(H-1))*(width+gap)
        color, label = ((even, 'weave') if b % 2 == 0 else
                        (block, 'offset') if b == H else (witness, 'walk'))
        parts.extend([f'<rect x="{x}" y="124" width="{width}" height="155" rx="8" fill="#fffdf8" stroke="#d7d4ca"/>',
                      f'<rect x="{x}" y="124" width="{width}" height="7" fill="{color}"/>',
                      f'<text x="{x+width/2}" y="165" text-anchor="middle" font-size="22" fill="{ink}">{b}</text>',
                      f'<text x="{x+width/2}" y="192" text-anchor="middle" font-size="11" fill="{color}">{label}</text>',
                      f'<text x="{x+width/2}" y="223" text-anchor="middle" font-size="12" fill="{muted}">parts</text>',
                      f'<text x="{x+width/2}" y="250" text-anchor="middle" font-size="20" fill="{ink}">{b+(K*b+H-1)//H}</text>'])
    parts.extend([f'<text x="32" y="323" font-size="17" fill="{ink}">Blue: seventeen explicit even-side weaves. Copper: fifteen saved odd-base edge certificates.</text>',
                  f'<text x="32" y="355" font-size="17" fill="{ink}">Green: the 33-leaf offset block. Each color reaches the parity/capacity lower bound.</text>',
                  f'<text x="32" y="395" font-size="13" fill="{muted}">Finite theorem for h=33 · Uniform odd-hub edge construction still open here · Marlow</text>'])
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2450 420" width="2450" height="420" role="img" aria-label="Thirty-three base residues for K thirty-three t, classified by even weave, offset block, and explicit walks" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n')


def main():
    for base in range(H-1, 2*H-1):
        for blocks in range(12):
            certificate(base, blocks)
    draw(HERE / 'art/thirtythree_hub_residue_ladder.svg')
    print('Verified all 33 base residues and lifts through 11 added blocks.')


if __name__ == '__main__':
    main()
