"""Explicit optimal cycle/edge partitions of K_(5,t).

Run: python3 -I playground/marlow/14_bipartite_five.py
The lower bound and block proof are in 14_bipartite_five.md.
"""

from pathlib import Path


HERE = Path(__file__).resolve().parent

# Hubs are 0..4 and seed leaves are 5..4+t. Walks are cyclic vertex orders.
SEEDS = {
    0: ((), ()),
    1: ((), ((0, 5), (1, 5), (2, 5), (3, 5), (4, 5))),
    2: (((1, 5, 2, 6), (3, 5, 4, 6)), ((0, 5), (0, 6))),
    3: (((3, 5, 4, 6, 0, 7), (1, 6, 2, 7)),
        ((0, 5), (1, 5), (2, 5), (3, 6), (4, 7))),
    4: (((1, 5, 2, 6, 3, 7, 4, 8), (1, 6, 4, 5, 3, 8, 2, 7)),
        ((0, 5), (0, 6), (0, 7), (0, 8))),
    6: (((1, 5, 2, 7, 3, 8, 4, 6),
         (0, 8, 2, 6, 3, 9, 4, 10),
         (0, 7, 4, 5, 3, 10, 1, 9)),
        ((0, 5), (0, 6), (1, 7), (1, 8), (2, 9), (2, 10))),
    7: (((1, 5, 2, 6, 3, 8, 4, 7),
         (0, 9, 1, 6, 4, 5, 3, 11, 2, 10),
         (0, 8, 2, 7, 3, 9, 4, 10, 1, 11)),
        ((0, 5), (0, 6), (0, 7), (1, 8), (2, 9), (3, 10), (4, 11))),
    8: (((1, 10, 3, 8, 2, 7, 4, 12),
         (0, 11, 4, 9, 3, 6, 2, 12),
         (0, 7, 3, 5, 1, 6, 4, 8),
         (0, 9, 1, 11, 2, 5, 4, 10)),
        ((0, 5), (0, 6), (1, 7), (1, 8),
         (2, 9), (2, 10), (3, 11), (3, 12))),
}


def edge(u, v):
    assert u != v
    return tuple(sorted((u, v)))


def partition(t):
    """Return a list of cycle walks and a list of singleton edges."""
    assert t >= 0
    if t < 5:
        seed_t, blocks = t, 0
    else:
        q, r = divmod(t, 5)
        if r == 0:
            seed_t, blocks = 0, q
        elif r == 4:
            seed_t, blocks = 4, q
        else:
            seed_t, blocks = 5 + r, q - 1
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


def optimum(t):
    return {0: 0, 1: 5, 2: 4, 3: 7}.get(t, t + (2 * t + 4) // 5)


def check(t):
    cycles, singles = partition(t)
    expected = {edge(hub, leaf) for hub in range(5)
                for leaf in range(5, 5 + t)}
    seen = set()
    for walk in cycles:
        assert len(walk) >= 4 and len(walk) == len(set(walk))
        for i, u in enumerate(walk):
            e = edge(u, walk[(i + 1) % len(walk)])
            assert e in expected and e not in seen
            seen.add(e)
    for u, v in singles:
        e = edge(u, v)
        assert e in expected and e not in seen
        seen.add(e)
    assert seen == expected
    assert len(cycles) + len(singles) == optimum(t)
    return len(cycles), len(singles)


def draw(path):
    ink, muted, paper = '#242320', '#68635c', '#f7f4ed'
    violet, teal, coral = '#5965a1', '#2d8c82', '#bd764e'
    parts = [f'<rect width="960" height="410" fill="{paper}"/>',
             f'<text x="38" y="52" font-size="28" fill="{ink}">What do the ten hub-clique edges cost?</text>',
             f'<text x="38" y="82" font-size="16" fill="{muted}">Extra parts when K₅ is added to K₅,ₜ, for t = 0,…,12</text>']
    for t in range(13):
        x = 38 + t * 69
        joined = t + 2 + (2 * t + 4) // 5 + (t == 1)
        delta = joined - optimum(t)
        color = (teal, coral, violet)[delta]
        parts.append(f'<rect x="{x}" y="142" width="56" height="102" rx="8" fill="{color}"/>')
        parts.append(f'<text x="{x+28}" y="182" text-anchor="middle" font-size="28" fill="#fffdf8">{delta}</text>')
        parts.append(f'<text x="{x+28}" y="223" text-anchor="middle" font-size="15" fill="#fffdf8">t={t}</text>')
    parts.extend((
        f'<circle cx="47" cy="293" r="7" fill="{teal}"/>',
        f'<text x="64" y="298" font-size="16" fill="{ink}">cost 0: no increase in the optimal part count</text>',
        f'<circle cx="47" cy="328" r="7" fill="{coral}"/>',
        f'<text x="64" y="333" font-size="16" fill="{ink}">cost 1: t=2</text>',
        f'<circle cx="47" cy="363" r="7" fill="{violet}"/>',
        f'<text x="64" y="368" font-size="16" fill="{ink}">cost 2: t=0 and every t≥4</text>',
        f'<text x="915" y="382" text-anchor="end" font-size="12" fill="{muted}">Marlow · family 181 · exact five-hub comparison</text>',
    ))
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 410" width="960" height="410" role="img" aria-label="Extra cycle and edge parts when adding a five-vertex hub clique to a complete bipartite graph with five hubs and t leaves" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n'
    path.write_text(svg)


def main():
    for t in range(101):
        c, s = check(t)
        if t <= 12:
            print(f't={t:2d}: {c} cycles + {s} singletons = {c+s} parts')
    draw(HERE / 'art/bipartite_five.svg')
    print('All partitions checked through t=100; diagram generated.')


if __name__ == '__main__':
    main()
