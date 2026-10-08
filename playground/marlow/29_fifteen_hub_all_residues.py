"""Check six odd-base certificates for K_{15,t} and their 15-leaf lifts.

Run: python3 -I playground/marlow/29_fifteen_hub_all_residues.py
Eight even bases use Sotteau's theorem rather than this finite checker.
"""

import json
from pathlib import Path


HUBS = 15
HALF = 7
HERE = Path(__file__).resolve().parent
SEEDS = json.loads((HERE / '29_fifteen_hub_odd_seeds.json').read_text())
assert set(SEEDS) == {'17', '19', '21', '23', '25', '27'}


def offset_cycle(offset, start):
    return {'hubs': [(-i) % HUBS for i in range(HUBS)],
            'leaves': [start + ((-i + offset) % HUBS)
                       for i in range(HUBS)]}


def certificate(base, blocks=0):
    """Validate an odd base plus nonnegative modular blocks."""
    assert base == HUBS or base in (17, 19, 21, 23, 25, 27)
    assert blocks >= 0
    t = base + HUBS*blocks
    if base == HUBS:
        singles = [(hub, hub) for hub in range(HUBS)]
        cycles = [offset_cycle(offset, 0) for offset in range(1, HUBS, 2)]
    else:
        data = SEEDS[str(base)]
        singles = [tuple(edge) for edge in data['singleton_spokes']]
        cycles = list(data['cycles'])
        j = (base-HUBS)//2
        assert sorted(len(c['hubs']) for c in cycles) == [HUBS-1]*j + [HUBS]*HALF
        degrees = [sum(hub == a for a, _ in singles) for hub in range(HUBS)]
        assert sorted(degrees) == [1]*(HUBS-j) + [3]*j
        short_omissions = [tuple(set(range(HUBS))-set(c['hubs']))
                           for c in cycles if len(c['hubs']) == HUBS-1]
        assert {a for (a,) in short_omissions} == {a for a, d in enumerate(degrees) if d == 3}
    for block in range(blocks):
        start = base + HUBS*block
        singles.extend((hub, start+hub) for hub in range(HUBS))
        cycles.extend(offset_cycle(offset, start)
                      for offset in range(1, HUBS, 2))
    seen = set()
    for hub, leaf in singles:
        assert 0 <= hub < HUBS and 0 <= leaf < t
        assert (hub, leaf) not in seen
        seen.add((hub, leaf))
    for cycle in cycles:
        hs, ls = cycle['hubs'], cycle['leaves']
        assert 2 <= len(hs) == len(ls) <= HUBS
        assert len(set(hs)) == len(hs) and len(set(ls)) == len(ls)
        for i, hub in enumerate(hs):
            assert 0 <= hub < HUBS
            for leaf in (ls[i], ls[i-1]):
                assert 0 <= leaf < t and (hub, leaf) not in seen, (t, hub, leaf)
                seen.add((hub, leaf))
    assert seen == {(hub, leaf) for hub in range(HUBS) for leaf in range(t)}
    assert len(singles) == t
    assert len(cycles) == (HALF*t + HUBS-1)//HUBS
    return singles, cycles


def draw(path):
    paper, ink, muted = '#f7f4ed', '#25313a', '#5c6970'
    even, block, witness = '#567aa5', '#3b927e', '#b47751'
    width, gap, x0 = 75, 9, 35
    parts = [f'<rect width="1330" height="420" fill="{paper}"/>',
             f'<text x="35" y="49" font-size="27" fill="{ink}">Fifteen hubs: fifteen base residues</text>',
             f'<text x="35" y="78" font-size="15" fill="{muted}">t = 14,…,28; add one 15-leaf block to move up a row</text>']
    for b in range(14, 29):
        x = x0 + (b-14)*(width+gap)
        color, label = ((even, 'Sotteau') if b % 2 == 0 else
                        (block, 'offset') if b == 15 else (witness, 'walk'))
        parts.extend([f'<rect x="{x}" y="124" width="{width}" height="155" rx="8" fill="#fffdf8" stroke="#d7d4ca"/>',
                      f'<rect x="{x}" y="124" width="{width}" height="7" fill="{color}"/>',
                      f'<text x="{x+width/2}" y="165" text-anchor="middle" font-size="22" fill="{ink}">{b}</text>',
                      f'<text x="{x+width/2}" y="192" text-anchor="middle" font-size="12" fill="{color}">{label}</text>',
                      f'<text x="{x+width/2}" y="223" text-anchor="middle" font-size="12" fill="{muted}">parts</text>',
                      f'<text x="{x+width/2}" y="250" text-anchor="middle" font-size="20" fill="{ink}">{b+(7*b+14)//15}</text>'])
    parts.extend([f'<text x="35" y="323" font-size="17" fill="{ink}">Blue: eight even bases from a published 28-cycle theorem. Copper: six explicit edge certificates.</text>',
                  f'<text x="35" y="355" font-size="17" fill="{ink}">Green: the 15-leaf offset block. Every lift adds 22 parts.</text>',
                  f'<text x="35" y="395" font-size="13" fill="{muted}">Finite theorem for h=15 · A uniform odd-hub construction remains open in this playground · Marlow</text>'])
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1330 420" width="1330" height="420" role="img" aria-label="Fifteen base residues for K fifteen t, classified by Sotteau, offset block, and explicit walks" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n')


def main():
    for base in (15, 17, 19, 21, 23, 25, 27):
        for blocks in range(12):
            certificate(base, blocks)
    for b in range(14, 29, 2):
        m, c = 14, 14
        assert m % 2 == b % 2 == 0 and m >= c and b >= c
        assert (m*b) % (2*c) == 0
        assert (7*b+14)//15 == b//2
    draw(HERE / 'art/fifteen_hub_residue_ladder.svg')
    print('Verified seven odd bases and their 15-leaf lifts through 11 blocks.')
    print('Even bases use Sotteau; wrote the residue-method ladder.')


if __name__ == '__main__':
    main()
