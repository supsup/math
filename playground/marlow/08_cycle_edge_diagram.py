"""Validate and draw the seven-part partition of K3 joined to I4.

Run: python3 -I playground/marlow/08_cycle_edge_diagram.py
This is the source of art/cycle_edge_seven.svg.
"""

from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
CYCLES = ((0, 1, 2), (0, 3, 1, 4), (0, 5, 1, 6))
SINGLETONS = ((2, 3), (2, 4), (2, 5), (2, 6))
COLORS = ('#5b629b', '#319184', '#a86845')


def edge(u, v):
    return tuple(sorted((u, v)))


def check_partition():
    expected = {edge(u, v) for u, v in combinations(range(3), 2)}
    expected |= {edge(u, v) for u in range(3) for v in range(3, 7)}
    seen = set()
    for walk in CYCLES:
        assert len(walk) >= 3 and len(set(walk)) == len(walk)
        for j, u in enumerate(walk):
            e = edge(u, walk[(j + 1) % len(walk)])
            assert e in expected and e not in seen
            seen.add(e)
    for u, v in SINGLETONS:
        e = edge(u, v)
        assert e in expected and e not in seen
        seen.add(e)
    assert seen == expected and len(seen) == 15
    assert len(CYCLES) + len(SINGLETONS) == 7


def draw(path):
    ink, muted, paper = '#242320', '#5f5c55', '#f7f4ed'
    parts = [f'<rect width="920" height="520" fill="{paper}"/>',
             f'<text x="44" y="55" fill="{ink}" font-size="28">Seven parts on seven vertices</text>',
             f'<text x="44" y="83" fill="{muted}" font-size="16">K₃ joined to four independent vertices · hubs 0, 1, 2 · leaves 3, 4, 5, 6</text>',
             '<rect x="43" y="112" width="834" height="268" rx="13" fill="#fffdf8" stroke="#ddd6c8"/>',
             f'<text x="65" y="151" fill="{muted}" font-size="16">CYCLES</text>']
    for row, walk in enumerate(CYCLES):
        y, color = 143 + 80 * row, COLORS[row]
        xs = [230 + 110 * j for j in range(len(walk))]
        parts.append(f'<path d="M {xs[0]} {y} H {xs[-1]}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round"/>')
        for x, vertex in zip(xs, walk):
            parts.append(f'<circle cx="{x}" cy="{y}" r="17" fill="#fffdf8" stroke="{color}" stroke-width="3"/>')
            parts.append(f'<text x="{x}" y="{y+6}" text-anchor="middle" font-size="18" fill="{ink}">{vertex}</text>')
        parts.append(f'<text x="610" y="{y+6}" font-size="15" fill="{muted}">closes at 0</text>')
    parts.append(f'<text x="65" y="356" fill="{muted}" font-size="16">SINGLETONS</text>')
    for j, (u, v) in enumerate(SINGLETONS):
        x = 192 + 125 * j
        parts.append(f'<rect x="{x}" y="330" width="100" height="35" rx="17" fill="#e9d7c9" stroke="#ba754e"/>')
        parts.append(f'<text x="{x+50}" y="353" text-anchor="middle" font-size="17" fill="#583b2d">{u}–{v}</text>')
    parts.extend([
        f'<text x="44" y="425" fill="{ink}" font-size="17">The three cycles use 3 + 4 + 4 edges; the four singletons use the remaining edges.</text>',
        f'<text x="44" y="453" fill="{muted}" font-size="15">Every leaf needs a singleton by parity; with fewer than three cycles, hub degrees force more.</text>',
        '<text x="876" y="495" fill="#77736c" font-size="12" text-anchor="end">Marlow · family 181 · finite exact census</text>',
    ])
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 520" width="920" height="520" role="img" aria-label="A seven-part cycle-and-singleton-edge decomposition of a seven-vertex split graph" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n'
    path.write_text(svg)


def main():
    check_partition()
    draw(HERE / 'art/cycle_edge_seven.svg')
    print('Validated all 15 edges in seven parts and generated the diagram.')


if __name__ == '__main__':
    main()
