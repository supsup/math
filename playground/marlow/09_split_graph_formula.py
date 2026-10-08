"""Construct the exact cycle-and-edge partition of K3 joined to I_t.

Run: python3 -I playground/marlow/09_split_graph_formula.py
The lower bound is proved in 09_split_graph_formula.md, not by this script.
"""

from pathlib import Path


HERE = Path(__file__).resolve().parent


def edge(u, v):
    assert u != v
    return tuple(sorted((u, v)))


def cycle_edges(walk):
    assert len(walk) >= 3 and len(set(walk)) == len(walk)
    return {edge(walk[i], walk[(i + 1) % len(walk)])
            for i in range(len(walk))}


def partition(t):
    """Return (cycle vertex walks, singleton edges) on hubs 0,1,2."""
    assert t >= 0
    leaves = list(range(3, t + 3))
    cycles, singles = [], []
    groups, remainder = divmod(t, 3)
    for j in range(groups):
        a, b, c = leaves[3 * j:3 * j + 3]
        cycles.append((0, a, 1, b, 2, c))
        singles.extend((edge(2, a), edge(0, b), edge(1, c)))
    rest = leaves[3 * groups:]
    if remainder == 0:
        cycles.append((0, 1, 2))
    elif remainder == 1:
        (d,) = rest
        cycles.append((0, d, 1, 2))
        singles.extend((edge(2, d), edge(0, 1)))
    else:
        d, e = rest
        cycles.extend(((0, d, 1, 2), (0, e, 1)))
        singles.extend((edge(2, d), edge(2, e)))
    return cycles, singles


def check(t):
    cycles, singles = partition(t)
    all_edges = {edge(u, v) for u in range(3) for v in range(u + 1, 3)}
    all_edges |= {edge(h, leaf) for h in range(3)
                  for leaf in range(3, t + 3)}
    seen = set()
    for walk in cycles:
        for e in cycle_edges(walk):
            assert e in all_edges and e not in seen
            seen.add(e)
    for e in singles:
        assert e in all_edges and e not in seen
        seen.add(e)
    assert seen == all_edges
    expected = t + (t + 2) // 3 + 1
    assert len(cycles) + len(singles) == expected
    return len(cycles), len(singles)


def draw(path):
    ink, faded, paper, violet, teal = '#242320', '#68635c', '#f7f4ed', '#5965a1', '#2d8c82'
    parts = [f'<rect width="900" height="550" fill="{paper}"/>',
             f'<text x="46" y="53" font-size="28" fill="{ink}">A split-graph staircase</text>',
             f'<text x="46" y="82" font-size="16" fill="{faded}">Exact parts for K₃ joined to t independent vertices</text>']
    x0, y0, dx, dy = 88, 456, 34, 22
    parts.append(f'<path d="M{x0} {y0-345}V{y0}H{x0+22*dx}" fill="none" stroke="{ink}" stroke-width="2"/>')
    for y in (0, 5, 10, 15):
        py = y0 - y * dy
        parts.append(f'<path d="M{x0} {py}H{x0+20*dx}" stroke="#ded8cb" stroke-width="1"/>')
        parts.append(f'<text x="{x0-12}" y="{py+5}" text-anchor="end" font-size="14" fill="{faded}">{y}</text>')
    for t in (0, 5, 10, 15, 20):
        px = x0 + t * dx
        parts.append(f'<text x="{px}" y="{y0+23}" text-anchor="middle" font-size="14" fill="{faded}">{t}</text>')
    for t in range(21):
        px = x0 + t * dx
        exact = t + (t + 2) // 3 + 1
        tree = t + 2
        # Plot the excess over t, so the vertical range remains readable.
        # The axis labels are values of d(G_t)-t.
        parts.append(f'<circle cx="{px}" cy="{y0-(exact-t)*dy}" r="4" fill="{violet}"/>')
        parts.append(f'<circle cx="{px}" cy="{y0-(tree-t)*dy}" r="2.7" fill="{teal}"/>')
    parts.append(f'<text x="90" y="119" font-size="14" fill="{faded}">vertical axis: number of parts minus t</text>')
    parts.append(f'<text x="814" y="503" text-anchor="end" font-size="14" fill="{faded}">independent vertices t</text>')
    parts.append(f'<circle cx="99" cy="520" r="5" fill="{violet}"/>')
    parts.append(f'<text x="113" y="525" font-size="15" fill="{ink}">exact d(K₃ ∨ Iₜ) = t + ⌈t/3⌉ + 1</text>')
    parts.append(f'<circle cx="510" cy="520" r="4" fill="{teal}"/>')
    parts.append(f'<text x="523" y="525" font-size="15" fill="{ink}">n−1 = t+2</text>')
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 550" width="900" height="550" role="img" aria-label="Exact split-graph cycle-and-edge partition number minus t, compared with n minus one" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n'
    path.write_text(svg)


def main():
    for t in range(41):
        cycles, singles = check(t)
        if t <= 11:
            print(f't={t:2d} cycles={cycles:2d} singletons={singles:2d} total={cycles + singles:2d}')
    draw(HERE / 'art/split_graph_staircase.svg')
    print('All construction checks passed through t=40.')


if __name__ == '__main__':
    main()
