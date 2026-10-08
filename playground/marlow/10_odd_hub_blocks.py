"""Construct exact cycle/edge partitions of K_h join I_(hq), odd h.

Run: python3 -I playground/marlow/10_odd_hub_blocks.py
The lower bound and the Walecki-cycle argument are in the accompanying note.
"""

from pathlib import Path


HERE = Path(__file__).resolve().parent


def edge(u, v):
    assert u != v
    return tuple(sorted((u, v)))


def partition(h, q):
    """Return cycle walks and singleton edges; hubs 0..h-1, q leaf blocks."""
    assert h >= 3 and h % 2 == 1 and q >= 0
    k = (h - 1) // 2
    cycles, singles = [], []
    for block in range(q):
        base = h + block * h
        for index in range(h):
            singles.append(edge(index, base + index))
        for first_offset in range(1, h, 2):
            # Consecutive offset classes form one Hamilton cycle of K_(h,h).
            walk = tuple(vertex for j in range(h)
                         for vertex in ((-j) % h,
                                        base + (first_offset - j) % h))
            cycles.append(walk)
    # Walecki's Hamilton decomposition of the clique, with hub h-1 as infinity.
    for i in range(k):
        walk = [h - 1, i]
        for j in range(1, k):
            walk.extend(((i - j) % (2 * k), (i + j) % (2 * k)))
        walk.append((i - k) % (2 * k))
        cycles.append(tuple(walk))
    return cycles, singles


def check(h, q):
    cycles, singles = partition(h, q)
    t = h * q
    expected = ({edge(u, v) for u in range(h) for v in range(u + 1, h)}
                | {edge(u, v) for u in range(h) for v in range(h, h + t)})
    seen = set()
    for walk in cycles:
        assert len(walk) >= 3 and len(walk) == len(set(walk))
        for i, u in enumerate(walk):
            e = edge(u, walk[(i + 1) % len(walk)])
            assert e in expected and e not in seen
            seen.add(e)
    for e in singles:
        assert e in expected and e not in seen
        seen.add(e)
    assert seen == expected
    k = (h - 1) // 2
    assert len(cycles) == k * (q + 1)
    assert len(singles) == t
    assert len(cycles) + len(singles) == t + k * q + k
    return len(cycles), len(singles)


def draw(path):
    """Show K5,5 spoke offset classes and the two K5 hub cycles."""
    ink, muted, paper = '#252420', '#66615a', '#f7f4ed'
    colors = ('#bd764e', '#488c83', '#5965a1')
    parts = [f'<rect width="940" height="610" fill="{paper}"/>',
             f'<text x="42" y="53" font-size="28" fill="{ink}">Five hubs, five leaves</text>',
             f'<text x="42" y="81" font-size="16" fill="{muted}">The 25 spokes split into five singleton edges and two Hamilton cycles.</text>']
    for hub in range(5):
        parts.append(f'<text x="{183+hub*91}" y="132" text-anchor="middle" font-size="17" fill="{ink}">hub {hub}</text>')
    for leaf in range(5):
        parts.append(f'<text x="103" y="{177+leaf*64}" text-anchor="middle" font-size="17" fill="{ink}">leaf {leaf}</text>')
        for hub in range(5):
            offset = (leaf - hub) % 5
            group = 0 if offset == 0 else (1 if offset <= 2 else 2)
            x, y = 150+hub*91, 147+leaf*64
            parts.append(f'<rect x="{x}" y="{y}" width="65" height="50" rx="8" fill="{colors[group]}"/>')
            parts.append(f'<text x="{x+32}" y="{y+32}" text-anchor="middle" font-size="19" fill="#fffdf8">{offset}</text>')
    parts += [
        f'<rect x="670" y="152" width="27" height="24" rx="5" fill="{colors[0]}"/>',
        f'<text x="710" y="170" font-size="16" fill="{ink}">offset 0: 5 singletons</text>',
        f'<rect x="670" y="198" width="27" height="24" rx="5" fill="{colors[1]}"/>',
        f'<text x="710" y="216" font-size="16" fill="{ink}">offsets 1,2: cycle 1</text>',
        f'<rect x="670" y="244" width="27" height="24" rx="5" fill="{colors[2]}"/>',
        f'<text x="710" y="262" font-size="16" fill="{ink}">offsets 3,4: cycle 2</text>',
        f'<text x="670" y="331" font-size="17" fill="{ink}">Hub clique K₅:</text>',
        f'<text x="670" y="365" font-size="16" fill="{colors[1]}">4–0–3–1–2–4</text>',
        f'<text x="670" y="394" font-size="16" fill="{colors[2]}">4–1–0–2–3–4</text>',
        f'<text x="42" y="533" font-size="17" fill="{ink}">Result: five singleton edges + four cycles = nine parts, exactly optimal.</text>',
        f'<text x="42" y="562" font-size="15" fill="{muted}">The two offset classes in each pair differ by 1, so they form one 10-vertex cycle.</text>',
        f'<text x="900" y="593" font-size="12" text-anchor="end" fill="{muted}">Marlow · family 181 · odd-hub block construction</text>',
    ]
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 940 610" width="940" height="610" role="img" aria-label="K5 joined to five independent vertices: spoke offset matrix with five singleton diagonals and two Hamilton cycles, plus two hub cycles" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n'
    path.write_text(svg)


def main():
    for h in range(3, 18, 2):
        for q in range(5):
            check(h, q)
        print(f'h={h:2d}: construction verified for q=0..4')
    draw(HERE / 'art/odd_hub_blocks.svg')
    print('Generated odd-hub block diagram.')


if __name__ == '__main__':
    main()
