"""Check all 45 base residues at 45 hubs and eleven lifts per base.

Run: python3 -I playground/marlow/56_fortyfive_hub_all_residues.py
The odd-base walks are read directly; no CP-SAT dependency is needed.
"""
import json
from pathlib import Path

H,K=45,22
HERE=Path(__file__).resolve().parent
SEEDS=json.loads((HERE/'56_fortyfive_hub_odd_seeds.json').read_text())
assert set(SEEDS)=={str(H+2*j) for j in range(1,K)}

def offset_cycle(offset,start):
    return {'hubs':[(-i)%H for i in range(H)],
            'leaves':[start+((-i+offset)%H) for i in range(H)]}

def base_certificate(base):
    assert H-1<=base<=2*H-2
    if base%2==0:
        half=base//2
        singles=[(H-1,leaf) for leaf in range(base)]
        cycles=[{'hubs':list(range(H-1)),
                 'leaves':[2*((shift+j)%half)+parity
                           for j in range(K) for parity in (0,1)]}
                for shift in range(half)]
    elif base==H:
        singles=[(hub,hub) for hub in range(H)]
        cycles=[offset_cycle(offset,0) for offset in range(1,H,2)]
    else:
        seed=SEEDS[str(base)]
        singles=[tuple(e) for e in seed['singleton_spokes']]
        cycles=seed['cycles']
        j=(base-H)//2
        assert len(cycles)==K+j
        assert sorted(len(c['hubs']) for c in cycles)==[H-1]*j+[H]*K
        degrees=[sum(a==hub for a,_ in singles) for hub in range(H)]
        assert degrees==[3]*j+[1]*(H-j)
        short=[set(range(H))-set(c['hubs']) for c in cycles if len(c['hubs'])==H-1]
        assert {next(iter(s)) for s in short}==set(range(j))
    return singles,cycles

def certificate(base,blocks):
    singles,cycles=base_certificate(base)
    singles,cycles=list(singles),list(cycles)
    for block in range(blocks):
        start=base+H*block
        singles.extend((hub,start+hub) for hub in range(H))
        cycles.extend(offset_cycle(offset,start) for offset in range(1,H,2))
    t=base+H*blocks
    seen=set()
    for a,b in singles:
        assert 0<=a<H and 0<=b<t and (a,b) not in seen
        seen.add((a,b))
    for c in cycles:
        hubs,leaves=c['hubs'],c['leaves']
        assert 2<=len(hubs)==len(leaves)<=H
        assert len(set(hubs))==len(hubs) and len(set(leaves))==len(leaves)
        for i,a in enumerate(hubs):
            assert 0<=a<H
            for b in (leaves[i],leaves[i-1]):
                assert 0<=b<t and (a,b) not in seen
                seen.add((a,b))
    assert seen=={(a,b) for a in range(H) for b in range(t)}
    assert len(singles)==t
    assert len(cycles)==(K*t+H-1)//H
    return len(singles)+len(cycles)

def draw(path):
    paper,ink,muted='#f7f4ed','#25313a','#5e6c75'
    blue,green,amber='#567aa5','#3b927e','#b47751'
    width,gap,x0=60,8,30
    total_width=2*x0+H*width+(H-1)*gap
    parts=[
        f'<rect width="{total_width}" height="455" fill="{paper}"/>',
        f'<text x="30" y="49" font-size="27" fill="{ink}">Forty-five hubs: every base residue opens</text>',
        f'<text x="30" y="79" font-size="15" fill="{muted}">t = 44,…,88 · every 45-leaf offset block adds 67 parts</text>',
    ]
    for base in range(H-1,2*H-1):
        x=x0+(base-(H-1))*(width+gap)
        color,label=((blue,'weave') if base%2==0 else
                     (green,'square') if base==H else
                     (amber,'interval'))
        count=base+(K*base+H-1)//H
        parts.extend([
            f'<rect x="{x}" y="125" width="{width}" height="172" rx="8" fill="#fffdf9" stroke="#d8d4ca"/>',
            f'<rect x="{x}" y="125" width="{width}" height="8" fill="{color}"/>',
            f'<text x="{x+width/2}" y="169" text-anchor="middle" font-size="21" fill="{ink}">{base}</text>',
            f'<text x="{x+width/2}" y="197" text-anchor="middle" font-size="11" fill="{color}">{label}</text>',
            f'<text x="{x+width/2}" y="232" text-anchor="middle" font-size="12" fill="{muted}">parts</text>',
            f'<text x="{x+width/2}" y="264" text-anchor="middle" font-size="20" fill="{ink}">{count}</text>',
        ])
    parts.extend([
        f'<text x="30" y="344" font-size="17" fill="{ink}">Blue: 23 even-side weaves. Green: affine square. Amber: 21 saved connected-cycle interval certificates.</text>',
        f'<text x="30" y="377" font-size="17" fill="{ink}">Each base reaches the singleton and cycle-capacity lower bound.</text>',
        f'<text x="30" y="427" font-size="13" fill="{muted}">Finite theorem for h=45 · every base/lift verified · Marlow</text>',
    ])
    path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_width} 455" '
        f'width="{total_width}" height="455" role="img" '
        'aria-label="All forty-five base residues at forty-five hubs, by even weave, affine square, and interval certificates" '
        'font-family="Georgia,serif">'+''.join(parts)+'</svg>\n'
    )

if __name__=='__main__':
    for b in range(H-1,2*H-1):
        for blocks in range(12):
            certificate(b,blocks)
    draw(HERE/'art/fortyfive_hub_residue_ladder.svg')
    print('45 bases and eleven lifts each independently verified')
