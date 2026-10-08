"""Check the explicit odd-base witnesses for the eleven-hub formula.

Run: python3 -I playground/marlow/25_eleven_hub_odd_seeds.py
Even bases use Sotteau's theorem, not this finite checker.
"""

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SEEDS = json.loads((HERE / '25_eleven_hub_odd_seeds.json').read_text())
assert set(SEEDS) == {'13', '15', '17', '19'}


def offset_cycle(first_offset, start):
    return {'hubs': [(-i) % 11 for i in range(11)],
            'leaves': [start + ((-i + first_offset) % 11)
                       for i in range(11)]}


def certificate(t):
    assert t >= 11
    base = 11 + (t-11) % 11
    assert base in (11, 13, 15, 17, 19)
    q = (t-base)//11
    if base == 11:
        singleton = [(hub, hub) for hub in range(11)]
        cycles = [offset_cycle(offset, 0) for offset in range(1, 11, 2)]
    else:
        data = SEEDS[str(base)]
        singleton = [tuple(edge) for edge in data['singleton_spokes']]
        cycles = list(data['cycles'])
    for block in range(q):
        start = base + 11*block
        singleton.extend((hub, start+hub) for hub in range(11))
        cycles.extend(offset_cycle(offset, start)
                      for offset in range(1, 11, 2))
    seen = set()
    for hub, leaf in singleton:
        assert 0 <= hub < 11 and 0 <= leaf < t
        assert (hub, leaf) not in seen
        seen.add((hub, leaf))
    for cycle in cycles:
        hubs, leaves = cycle['hubs'], cycle['leaves']
        assert 2 <= len(hubs) == len(leaves) <= 11
        assert len(set(hubs)) == len(hubs)
        assert len(set(leaves)) == len(leaves)
        for i, hub in enumerate(hubs):
            assert 0 <= hub < 11
            for leaf in (leaves[i], leaves[i-1]):
                edge = (hub, leaf)
                assert 0 <= leaf < t and edge not in seen, (t, edge)
                seen.add(edge)
    assert seen == {(hub, leaf) for hub in range(11) for leaf in range(t)}
    assert len(singleton) == t
    assert len(cycles) == (5*t+10)//11
    return singleton, cycles


def draw(path):
    paper, ink, muted = '#f7f4ed', '#25313a', '#5d6970'
    even, block, witness = '#5d79ad', '#419484', '#b97751'
    parts = [f'<rect width="1130" height="460" fill="{paper}"/>',
             f'<text x="42" y="52" font-size="28" fill="{ink}">Eleven hubs: eleven base residues, three construction rules</text>',
             f'<text x="42" y="82" font-size="16" fill="{muted}">One optimal seed for each t = 10,…,20; repeat an 11-leaf block for larger counts</text>']
    x0, y0, width, gap = 44, 130, 88, 10
    for b in range(10, 21):
        x = x0 + (b-10)*(width+gap)
        if b % 2 == 0:
            color, label = even, 'Sotteau'
        elif b == 11:
            color, label = block, 'offset'
        else:
            color, label = witness, 'JSON walk'
        parts += [f'<rect x="{x}" y="{y0}" width="{width}" height="164" rx="9" fill="#fffdf8" stroke="#d7d4ca"/>',
                  f'<rect x="{x}" y="{y0}" width="{width}" height="7" rx="3" fill="{color}"/>',
                  f'<text x="{x+width/2}" y="{y0+43}" text-anchor="middle" font-size="23" fill="{ink}">{b}</text>',
                  f'<text x="{x+width/2}" y="{y0+73}" text-anchor="middle" font-size="13" fill="{color}">{label}</text>',
                  f'<text x="{x+width/2}" y="{y0+111}" text-anchor="middle" font-size="13" fill="{muted}">parts</text>',
                  f'<text x="{x+width/2}" y="{y0+137}" text-anchor="middle" font-size="21" fill="{ink}">{b+(5*b+10)//11}</text>']
    parts += [f'<text x="45" y="337" font-size="18" fill="{ink}">Blue even bases: one hub gives singleton edges, then Sotteau decomposes K₁₀,ₜ into 20-cycles.</text>',
              f'<text x="45" y="372" font-size="17" fill="{ink}">Green: the 11-leaf offset block. Copper: four explicit odd-base edge certificates.</text>',
              f'<text x="45" y="422" font-size="13" fill="{muted}">Proof combines a published cycle-design theorem, checked finite walks, and an all-residue modular lift · Marlow</text>']
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1130 460" width="1130" height="460" role="img" aria-label="Eleven base residues for K eleven t, colored by Sotteau, offset block, and explicit odd seed method" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n')


def main():
    for base in (11, 13, 15, 17, 19):
        for q in range(12):
            certificate(base + 11*q)
    for b in range(10, 21, 2):
        m, c = 10, 10
        assert m % 2 == b % 2 == 0 and m >= c and b >= c
        assert (m*b) % (2*c) == 0  # Sotteau's exact conditions.
        assert (5*b+10)//11 == b//2
    draw(HERE / 'art/eleven_hub_residue_ladder.svg')
    print('Verified five odd bases and their eleven-leaf lifts through q=11.')
    print('Even bases use Sotteau; wrote residue-method ladder.')


if __name__ == '__main__':
    main()
