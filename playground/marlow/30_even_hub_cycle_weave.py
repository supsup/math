"""Check an explicit C_{4k} decomposition of K_{2k,2m} and draw K4,6.

Run: python3 -I playground/marlow/30_even_hub_cycle_weave.py
"""

from pathlib import Path


HERE = Path(__file__).resolve().parent


def cycles(k, m):
    assert 1 <= k <= m
    h = 2*k
    return [([i for i in range(h)],
             [2*((c+j) % m)+q for j in range(k) for q in (0, 1)])
            for c in range(m)]


def assignment(k, m):
    h, t = 2*k, 2*m
    seen = {}
    for color, (hs, ls) in enumerate(cycles(k, m)):
        assert len(hs) == len(set(hs)) == h
        assert len(ls) == len(set(ls)) == h
        for i, hub in enumerate(hs):
            for leaf in (ls[i], ls[i-1]):
                assert 0 <= leaf < t
                edge = (hub, leaf)
                assert edge not in seen, (k, m, edge)
                seen[edge] = color
    assert set(seen) == {(hub, leaf) for hub in range(h) for leaf in range(t)}
    assert len(seen) == h*t
    return seen


def draw(path):
    ink, muted, paper = '#25313a', '#5e6b72', '#f7f4ed'
    colors = ['#537fa9', '#bd7956', '#459783']
    edge_color = assignment(2, 3)
    parts = [f'<rect width="940" height="420" fill="{paper}"/>',
             f'<text x="34" y="48" font-size="27" fill="{ink}">The even-hub parity cliff</text>',
             f'<text x="34" y="78" font-size="15" fill="{muted}">Every square is one spoke of K₄,₆; each color forms one 8-edge cycle.</text>',
             '<rect x="30" y="104" width="480" height="276" rx="12" fill="#fffdf9" stroke="#d7d4ca"/>',
             '<rect x="535" y="104" width="373" height="276" rx="12" fill="#fffdf9" stroke="#d7d4ca"/>']
    x0, y0, cell, gap = 86, 152, 52, 5
    for leaf in range(6):
        x = x0+leaf*(cell+gap)
        parts.append(f'<text x="{x+cell/2}" y="139" text-anchor="middle" font-size="14" fill="{muted}">L{leaf}</text>')
    for hub in range(4):
        y = y0+hub*(cell+gap)
        parts.append(f'<text x="70" y="{y+33}" text-anchor="end" font-size="14" fill="{muted}">H{hub}</text>')
        for leaf in range(6):
            x = x0+leaf*(cell+gap)
            color = colors[edge_color[hub,leaf]]
            parts.extend([f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="6" fill="{color}"/>',
                          f'<text x="{x+cell/2}" y="{y+33}" text-anchor="middle" font-size="19" fill="#fffdf9">{edge_color[hub,leaf]+1}</text>'])
    data = [(4, 2, colors[0]), (5, 6, '#777391'), (6, 3, colors[2])]
    subscript = {4: '₄', 5: '₅', 6: '₆'}
    for row, (t, parts_count, color) in enumerate(data):
        y = 153+row*76
        parts.extend([f'<text x="558" y="{y+19}" font-size="16" fill="{ink}">K₄,{subscript[t]}</text>',
                      f'<rect x="650" y="{y}" width="{parts_count*31}" height="27" rx="5" fill="{color}"/>',
                      f'<text x="{658+parts_count*31}" y="{y+20}" font-size="17" fill="{ink}">{parts_count}</text>'])
    parts.extend([f'<text x="558" y="357" font-size="14" fill="{muted}">Even t: t/2 cycles. Odd t: one leaf star</text>',
                  f'<text x="558" y="377" font-size="14" fill="{muted}">plus (t−1)/2 cycles.</text>',
                  f'<text x="34" y="406" font-size="13" fill="{muted}">Explicit weave · classical cycle-design corollary · Marlow</text>'])
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 420" width="940" height="420" role="img" aria-label="Three cycle colors partition K four six, and parity bars show minimum counts two, six, three" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n')


def main():
    count = 0
    for k in range(1, 9):
        for m in range(k, k+9):
            assignment(k, m)
            count += 1
    draw(HERE / 'art/even_hub_parity_cliff.svg')
    print(f'Checked exact cycle edges for {count} even-even instances; wrote parity diagram.')


if __name__ == '__main__':
    main()
