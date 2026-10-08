"""Verify the exact odd-hub bipartite family one leaf short of a block.

Run: python3 -I playground/marlow/22_one_leaf_short.py
"""

from pathlib import Path


HERE = Path(__file__).resolve().parent


def offset_cycle(m, first_offset, start):
    """Hamilton cycle on m hubs and a disjoint block of m leaves."""
    walk = []
    for j in range(m):
        hub = (-j) % m
        walk.extend((hub, start + (hub + first_offset) % m))
    return tuple(walk)


def edges(walk):
    assert len(walk) >= 4 and len(walk) % 2 == 0
    hubs, leaves = walk[::2], walk[1::2]
    assert len(set(hubs)) == len(hubs)
    assert len(set(leaves)) == len(leaves)
    output = []
    for i in range(len(walk)):
        a, b = walk[i], walk[(i+1) % len(walk)]
        output.append((a, b) if i % 2 == 0 else (b, a))
    assert len(set(output)) == len(output)
    return output


def certificate(h, q):
    assert h >= 3 and h % 2 == 1 and q >= 0
    k, m = (h-1)//2, h-1
    t = m + h*q
    singleton = [(m, leaf) for leaf in range(m)]
    cycles = [offset_cycle(m, offset, 0) for offset in range(0, m, 2)]
    for block in range(q):
        start = m + h*block
        singleton.extend((hub, start+hub) for hub in range(h))
        cycles.extend(offset_cycle(h, offset, start)
                      for offset in range(1, h-1, 2))
    seen = set()
    for edge in singleton:
        assert edge not in seen
        seen.add(edge)
    for walk in cycles:
        for edge in edges(walk):
            assert 0 <= edge[0] < h and 0 <= edge[1] < t
            assert edge not in seen, edge
            seen.add(edge)
    assert seen == {(hub, leaf) for hub in range(h) for leaf in range(t)}
    expected = t + (k*t + h-1)//h
    assert len(singleton) + len(cycles) == expected == 3*k + (h+k)*q
    return singleton, cycles


def draw(path):
    h, m = 9, 8
    singleton, cycles = certificate(h, 0)
    role = {edge: 'S' for edge in singleton}
    for index, walk in enumerate(cycles):
        for edge in edges(walk):
            assert edge not in role
            role[edge] = index
    colors = ('#5a77af', '#b97851', '#4b988c', '#9b77ad')
    paper, ink, muted = '#f7f4ed', '#26313c', '#5d6870'
    parts = [f'<rect width="930" height="590" fill="{paper}"/>',
             f'<text x="43" y="53" font-family="Georgia,serif" font-size="27" fill="{ink}">One leaf short: remove a hub, then close four cycles</text>',
             f'<text x="43" y="80" font-family="Arial,sans-serif" font-size="15" fill="{muted}">K₉,₈ · each cell is one spoke · 8 singleton spokes + 4 Hamilton cycles = 12 parts</text>']
    x0, y0, cell = 112, 133, 43
    for leaf in range(m):
        parts.append(f'<text x="{x0+leaf*cell+19}" y="{y0-15}" text-anchor="middle" font-size="16" fill="{ink}">L{leaf}</text>')
    for hub in range(h):
        y = y0+hub*cell
        parts.append(f'<text x="{x0-17}" y="{y+27}" text-anchor="end" font-size="16" fill="{ink}">H{hub}</text>')
        for leaf in range(m):
            x = x0+leaf*cell
            val = role[(hub,leaf)]
            color = '#d7ae59' if val == 'S' else colors[val]
            label = 'S' if val == 'S' else f'C{val+1}'
            parts.append(f'<rect x="{x}" y="{y}" width="39" height="39" rx="4" fill="{color}"/>')
            parts.append(f'<text x="{x+19.5}" y="{y+25}" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" fill="#fffdf8">{label}</text>')
    parts += [f'<text x="505" y="178" font-family="Georgia,serif" font-size="20" fill="{ink}">The seed mechanism</text>',
              f'<text x="505" y="215" font-family="Arial,sans-serif" font-size="16" fill="{muted}">H8: one singleton per leaf</text>',
              f'<text x="505" y="246" font-family="Arial,sans-serif" font-size="16" fill="{muted}">H0–H7: K₈,₈ remains</text>',
              f'<text x="505" y="277" font-family="Arial,sans-serif" font-size="16" fill="{muted}">pair adjacent offset matchings</text>',
              f'<text x="505" y="308" font-family="Arial,sans-serif" font-size="16" fill="{muted}">each pair walks through all 8 + 8 vertices</text>',
              f'<text x="505" y="368" font-family="Georgia,serif" font-size="19" fill="{ink}">Append nine leaves</text>',
              f'<text x="505" y="403" font-family="Arial,sans-serif" font-size="16" fill="{muted}">9 diagonal spokes + 4 cycles</text>',
              f'<text x="505" y="432" font-family="Arial,sans-serif" font-size="16" fill="{muted}">repeat for t = 8 + 9q</text>',
              f'<text x="43" y="558" font-family="Arial,sans-serif" font-size="13" fill="{muted}">Exact edge partition · general odd-hub residue, not an all-residue formula · Marlow</text>']
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 930 590" width="930" height="590" role="img" aria-label="A nine-by-eight spoke matrix with one singleton row and four Hamilton cycle colors">' + ''.join(parts) + '</svg>\n')


def main():
    for h in range(3, 22, 2):
        for q in range(8):
            certificate(h, q)
    draw(HERE / 'art/one_leaf_short.svg')
    print('Checked exact spoke coverage for odd h=3..21 and q=0..7.')
    print('Wrote one-leaf-short spoke matrix.')


if __name__ == '__main__':
    main()
