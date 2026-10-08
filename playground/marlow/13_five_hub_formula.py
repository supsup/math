"""Explicit optimal cycle/edge partitions of K5 joined to I_t.

Run: python3 -I playground/marlow/13_five_hub_formula.py
The lower bound and residue argument are in 13_five_hub_formula.md.
"""

from pathlib import Path


HERE = Path(__file__).resolve().parent
HUB_CYCLES = ((4, 0, 3, 1, 2), (4, 1, 0, 2, 3))

# Each seed uses hubs 0..4 and leaves 5..4+t.  A pair (u,v) is a singleton.
SEEDS = {
    0: (HUB_CYCLES, ()),
    1: (((0, 2, 1, 4, 3, 5), (0, 3, 1, 5, 2, 4)),
        ((0, 1), (2, 3), (4, 5))),
    2: (((0, 1, 2, 5, 3, 6, 4), (0, 2, 6, 1, 5, 4, 3),
         (1, 3, 2, 4)), ((0, 5), (0, 6))),
    3: (((0, 1, 5, 2, 6, 4, 7, 3), (0, 2, 1, 4, 5, 3, 6),
         (0, 4, 2, 3, 1, 7)), ((0, 5), (1, 6), (2, 7), (3, 4))),
    4: (((0, 7, 2, 3, 5, 1, 6, 4, 8), (0, 1, 2, 4, 7, 3),
         (0, 2, 6, 3, 1, 4), (2, 5, 4, 3, 8)),
        ((0, 5), (0, 6), (1, 7), (1, 8))),
    6: (HUB_CYCLES + ((1, 5, 2, 7, 3, 8, 4, 6),
                       (0, 8, 2, 6, 3, 9, 4, 10),
                       (0, 7, 4, 5, 3, 10, 1, 9)),
        ((0, 5), (0, 6), (1, 7), (1, 8), (2, 9), (2, 10))),
}


def edge(u, v):
    assert u != v
    return tuple(sorted((u, v)))


def partition(t):
    """Return cycle walks and singleton edges for K5 join I_t."""
    assert t >= 0
    q, r = divmod(t, 5)
    if r == 1 and q:
        seed_t, blocks = 6, q - 1
    else:
        seed_t, blocks = r, q
    seed_cycles, seed_singles = SEEDS[seed_t]
    cycles, singles = list(seed_cycles), list(seed_singles)
    for block in range(blocks):
        base = 5 + seed_t + 5 * block
        singles.extend((hub, base + hub) for hub in range(5))
        for offset in (1, 3):
            cycles.append(tuple(vertex for j in range(5)
                                for vertex in ((-j) % 5,
                                               base + (offset - j) % 5)))
    return cycles, singles


def check(t):
    cycles, singles = partition(t)
    expected = ({edge(u, v) for u in range(5) for v in range(u + 1, 5)}
                | {edge(u, v) for u in range(5) for v in range(5, 5 + t)})
    seen = set()
    for walk in cycles:
        assert len(walk) >= 3 and len(set(walk)) == len(walk)
        for i, u in enumerate(walk):
            e = edge(u, walk[(i + 1) % len(walk)])
            assert e in expected and e not in seen
            seen.add(e)
    for u, v in singles:
        e = edge(u, v)
        assert e in expected and e not in seen
        seen.add(e)
    assert seen == expected
    optimum = t + 2 + (2 * t + 4) // 5 + (t == 1)
    assert len(cycles) + len(singles) == optimum
    return len(cycles), len(singles)


def draw(path):
    ink, muted, paper = '#242320', '#68635c', '#f7f4ed'
    violet, teal, coral = '#5965a1', '#2d8c82', '#bd764e'
    parts = [f'<rect width="930" height="500" fill="{paper}"/>',
             f'<text x="44" y="52" font-size="28" fill="{ink}">Five hubs: every residue closes</text>',
             f'<text x="44" y="81" font-size="16" fill="{muted}">Exact cycle-and-edge part count for K₅ joined to t independent vertices</text>']
    x0, y0, dx, dy = 85, 404, 57, 16
    parts.append(f'<path d="M{x0} {y0-315}V{y0}H{x0+13*dx}" fill="none" stroke="{ink}" stroke-width="2"/>')
    for t in range(13):
        x = x0 + t * dx
        lower = t + 2 + (2 * t + 4) // 5
        exact = lower + (t == 1)
        y = y0 - exact * dy
        parts.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{coral if t == 1 else violet}"/>')
        parts.append(f'<text x="{x}" y="{y-13}" text-anchor="middle" font-size="14" fill="{ink}">{exact}</text>')
        parts.append(f'<text x="{x}" y="{y0+24}" text-anchor="middle" font-size="14" fill="{ink}">{t}</text>')
    parts.extend((
        f'<text x="91" y="448" font-size="15" fill="{ink}">t leaves; each full block of five adds seven parts.</text>',
        f'<circle cx="91" cy="475" r="6" fill="{violet}"/>',
        f'<text x="107" y="480" font-size="14" fill="{ink}">lower bound attained</text>',
        f'<circle cx="350" cy="475" r="6" fill="{coral}"/>',
        f'<text x="366" y="480" font-size="14" fill="{ink}">K₆: one extra part</text>',
        f'<text x="890" y="480" text-anchor="end" font-size="12" fill="{muted}">Marlow · family 181</text>',
    ))
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 930 500" width="930" height="500" role="img" aria-label="Exact part count for five clique hubs and zero through twelve independent leaves" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n'
    path.write_text(svg)


def main():
    for t in range(101):
        c, s = check(t)
        if t <= 11:
            print(f't={t:2d}: {c} cycles + {s} singletons = {c+s} parts')
    draw(HERE / 'art/five_hub_staircase.svg')
    print('All partitions checked through t=100; diagram generated.')


if __name__ == '__main__':
    main()
