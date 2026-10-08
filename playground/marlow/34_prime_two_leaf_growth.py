"""Construct and check every odd base at primes p = 3 mod 4, p >= 7.

Run: python3 -I playground/marlow/34_prime_two_leaf_growth.py
Even bases and the modular lift are proved in playground items 24 and 10.
"""

import math
from pathlib import Path


HERE = Path(__file__).resolve().parent


def prime(p):
    return p >= 2 and all(p % d for d in range(2, math.isqrt(p)+1))


def primitive_root(p):
    assert prime(p)
    factors = {d for d in range(2, p) if (p-1) % d == 0 and prime(d)}
    return next(g for g in range(2, p)
                if all(pow(g, (p-1)//q, p) != 1 for q in factors))


def affine_square(p):
    """Each difference class gives one full cycle; leaf = hub-pair midpoint."""
    assert prime(p) and p % 2 == 1
    k, inv2 = (p-1)//2, pow(2, -1, p)
    singles = [(a, a) for a in range(p)]
    cycles = []
    for d in range(1, k+1):
        hs = [(i*d) % p for i in range(p)]
        ls = [((hs[i]+hs[(i+1) % p])*inv2) % p for i in range(p)]
        cycles.append({'hubs': hs, 'leaves': ls})
    return singles, cycles


def prime_family(p, j):
    assert prime(p) and p >= 7 and p % 4 == 3
    assert 0 <= j <= (p-3)//2
    g = primitive_root(p)
    k = (p-1)//2
    singles, cycles = affine_square(p)
    edge_slot = {}
    for color, cycle in enumerate(cycles):
        hs = cycle['hubs']
        for position, hub in enumerate(hs):
            edge_slot[frozenset((hub, hs[(position+1) % p]))] = (color, position)
    for center in range(j):
        hubs = [(center+pow(g, i, p)) % p for i in range(p-1)]
        slots, displaced, colors = [], [], [[], []]
        for i, hub in enumerate(hubs):
            next_hub = hubs[(i+1) % (p-1)]
            color, position = edge_slot[frozenset((hub, next_hub))]
            slots.append((color, position))
            displaced.append(cycles[color]['leaves'][position])
            colors[i % 2].append(color)
        assert len(set(displaced)) == p-1
        assert set(colors[0]) == set(colors[1]) == set(range(k))
        for i, (color, position) in enumerate(slots):
            cycles[color]['leaves'][position] = p + 2*center + i % 2
        singles.extend(((center, p+2*center), (center, p+2*center+1)))
        cycles.append({'hubs': hubs, 'leaves': displaced})
    return singles, cycles, g


def verify(p, t, singles, cycles):
    seen = set()
    for hub, leaf in singles:
        assert 0 <= hub < p and 0 <= leaf < t and (hub, leaf) not in seen
        seen.add((hub, leaf))
    for cycle in cycles:
        hs, ls = cycle['hubs'], cycle['leaves']
        assert 2 <= len(hs) == len(ls) <= p
        assert len(set(hs)) == len(hs) and len(set(ls)) == len(ls)
        for i, hub in enumerate(hs):
            assert 0 <= hub < p
            for leaf in (ls[i], ls[i-1]):
                assert 0 <= leaf < t and (hub, leaf) not in seen
                seen.add((hub, leaf))
    assert seen == {(hub, leaf) for hub in range(p) for leaf in range(t)}
    return len(singles)+len(cycles)


def draw(path):
    p, g = 7, 3
    powers = [pow(g, i, p) for i in range(p-1)]
    inv2 = pow(2, -1, p)
    ink, muted, paper = '#24313a', '#5c6970', '#f7f4ed'
    teal, copper = '#348b7b', '#b7754c'
    cx, cy, radius = 270, 235, 125
    coords = [(cx + radius*math.cos(2*math.pi*i/6-math.pi/2),
               cy + radius*math.sin(2*math.pi*i/6-math.pi/2)) for i in range(6)]
    parts = [f'<rect width="940" height="445" fill="{paper}"/>',
             f'<text x="32" y="47" font-size="26" fill="{ink}">Two new leaves from a multiplicative hub cycle</text>',
             f'<text x="32" y="76" font-size="15" fill="{muted}">p = 7, primitive root 3; the short cycle visits hubs 1, 3, 2, 6, 4, 5</text>']
    for i, (x, y) in enumerate(coords):
        nx, ny = coords[(i+1) % 6]
        d = (powers[(i+1) % 6]-powers[i]) % p
        color_class = min(d, p-d)
        midpoint = ((powers[i]+powers[(i+1) % 6])*inv2) % p
        color = teal if i % 2 == 0 else copper
        mx, my = (x+nx)/2, (y+ny)/2
        outward = math.hypot(mx-cx, my-cy)
        label_x = mx + 29*(mx-cx)/outward
        label_y = my + 29*(my-cy)/outward + 4
        parts.extend([f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{color}" stroke-width="8"/>',
                      f'<text x="{label_x:.1f}" y="{label_y:.1f}" text-anchor="middle" font-size="13" fill="{ink}">d{color_class} · ℓ{midpoint}</text>'])
    for i, (x, y) in enumerate(coords):
        parts.extend([f'<circle cx="{x:.1f}" cy="{y:.1f}" r="20" fill="#fffdf8" stroke="{ink}" stroke-width="2"/>',
                      f'<text x="{x:.1f}" y="{y+6:.1f}" text-anchor="middle" font-size="19" fill="{ink}">{powers[i]}</text>'])
    parts.extend([f'<text x="525" y="159" font-size="19" fill="{ink}">Each edge carries:</text>',
                  f'<text x="525" y="192" font-size="17" fill="{teal}">teal → new leaf x</text>',
                  f'<text x="525" y="225" font-size="17" fill="{copper}">copper → new leaf y</text>',
                  f'<text x="525" y="265" font-size="16" fill="{ink}">d = original full-cycle difference</text>',
                  f'<text x="525" y="294" font-size="16" fill="{ink}">ℓ = displaced old leaf midpoint</text>',
                  f'<text x="525" y="334" font-size="16" fill="{muted}">Each color uses d1, d2, d3 once.</text>',
                  f'<text x="32" y="416" font-size="13" fill="{muted}">The six distinct midpoints form the new short cycle; hub 0 is omitted · Marlow</text>'])
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 445" width="940" height="445" role="img" aria-label="Prime seven growth gadget: a six-hub cycle with alternating edges for two new leaves and distinct displaced midpoint leaves" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n')


def main():
    checked = []
    for p in range(7, 202):
        if not prime(p) or p % 4 != 3:
            continue
        singles, cycles = affine_square(p)
        assert verify(p, p, singles, cycles) == p+(p-1)//2
        for j in range(1, (p-1)//2):
            singles, cycles, g = prime_family(p, j)
            t = p+2*j
            assert verify(p, t, singles, cycles) == t+(p-1)//2+j
        checked.append((p, g))
    draw(HERE / 'art/prime_two_leaf_growth.svg')
    print(f'Checked affine square and every odd base at {len(checked)} primes p = 3 mod 4 through 199.')
    print('p, primitive root:', checked)


if __name__ == '__main__':
    main()
