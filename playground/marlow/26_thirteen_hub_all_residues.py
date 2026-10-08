"""Check the explicit odd-base certificates for K_{13,t} and modular lifts.

Run: python3 -I playground/marlow/26_thirteen_hub_all_residues.py
Even bases are supplied by Sotteau's theorem, not this finite checker.
"""

import json
from pathlib import Path


HUBS = 13
HALF = 6
HERE = Path(__file__).resolve().parent
SEEDS = json.loads((HERE / '26_thirteen_hub_odd_seeds.json').read_text())
assert set(SEEDS) == {'15', '17', '19', '21', '23'}


def offset_cycle(offset, start):
    return {'hubs': [(-i) % HUBS for i in range(HUBS)],
            'leaves': [start + ((-i + offset) % HUBS)
                       for i in range(HUBS)]}


def certificate(base, blocks=0):
    """Construct a certificate for an odd base and further 13-leaf blocks."""
    assert base == 13 or base in (15, 17, 19, 21, 23)
    assert blocks >= 0
    t = base + HUBS * blocks
    if base == 13:
        singles = [(hub, hub) for hub in range(HUBS)]
        cycles = [offset_cycle(offset, 0) for offset in range(1, HUBS, 2)]
    else:
        data = SEEDS[str(base)]
        singles = [tuple(edge) for edge in data['singleton_spokes']]
        cycles = list(data['cycles'])
        j = (base - HUBS) // 2
        assert sorted(len(c['hubs']) for c in cycles) == [HUBS - 1]*j + [HUBS]*HALF
        degrees = [sum(hub == a for a, _ in singles) for hub in range(HUBS)]
        assert sorted(degrees) == [1]*(HUBS-j) + [3]*j
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
    assert len(cycles) == (HALF*t + HUBS - 1)//HUBS
    return singles, cycles


def draw(path):
    paper, ink, muted = '#f7f4ed', '#25313a', '#596973'
    even, block, witness = '#567aa5', '#3b927e', '#b47751'
    width, gap, x0 = 75, 8, 38
    parts = [f'<rect width="1165" height="420" fill="{paper}"/>',
             f'<text x="38" y="50" font-size="27" fill="{ink}">Thirteen hubs: one seed for each residue</text>',
             f'<text x="38" y="78" font-size="15" fill="{muted}">t = 12,…,24; add a 13-leaf block for every larger t</text>']
    for b in range(12, 25):
        x = x0 + (b-12)*(width+gap)
        color, label = ((even, 'Sotteau') if b % 2 == 0 else
                        (block, 'offset') if b == 13 else (witness, 'walk'))
        parts.extend([f'<rect x="{x}" y="125" width="{width}" height="155" rx="8" fill="#fffdf8" stroke="#d7d4ca"/>',
                      f'<rect x="{x}" y="125" width="{width}" height="7" fill="{color}"/>',
                      f'<text x="{x+width/2}" y="166" text-anchor="middle" font-size="22" fill="{ink}">{b}</text>',
                      f'<text x="{x+width/2}" y="193" text-anchor="middle" font-size="12" fill="{color}">{label}</text>',
                      f'<text x="{x+width/2}" y="224" text-anchor="middle" font-size="12" fill="{muted}">parts</text>',
                      f'<text x="{x+width/2}" y="251" text-anchor="middle" font-size="20" fill="{ink}">{b+(6*b+12)//13}</text>'])
    parts.extend([f'<text x="38" y="326" font-size="17" fill="{ink}">Seven even bases use a published 24-cycle design; five odd bases use checked edge walks.</text>',
                  f'<text x="38" y="358" font-size="17" fill="{ink}">The green 13-leaf offset block also lifts every seed by 19 parts.</text>',
                  f'<text x="38" y="395" font-size="13" fill="{muted}">Finite theorem for h=13 · General odd-hub design remains open in this playground · Marlow</text>'])
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1165 420" width="1165" height="420" role="img" aria-label="Thirteen base residues for K thirteen t, classified by Sotteau, offset block, and explicit walks" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n')


def main():
    for base in (13, 15, 17, 19, 21, 23):
        for blocks in range(12):
            certificate(base, blocks)
    for b in range(12, 25, 2):
        m, c = 12, 12
        assert m % 2 == b % 2 == 0 and m >= c and b >= c
        assert (m*b) % (2*c) == 0
        assert (6*b+12)//13 == b//2
    draw(HERE / 'art/thirteen_hub_residue_ladder.svg')
    print('Verified six odd bases and their 13-leaf lifts through 11 blocks.')
    print('Even bases use Sotteau; wrote the residue-method ladder.')


if __name__ == '__main__':
    main()
