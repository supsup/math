"""Check F_25 ODC page facts and draw the two scoped template obstructions.

Run: python3 -I playground/marlow/39_prime_power_template_probe.py
"""
from collections import Counter, defaultdict
from pathlib import Path

Q = 25


def add(x, y):
    return ((x % 5 + y % 5) % 5) + 5 * ((x // 5 + y // 5) % 5)


def mul(x, y):
    a, b, c, d = x % 5, x // 5, y % 5, y // 5
    return ((a*c - 2*b*d) % 5) + 5*((a*d + b*c) % 5)


def power(x, n):
    y = 1
    for _ in range(n):
        y = mul(y, x)
    return y


def edge(u, v):
    return tuple(sorted((u, v)))


g = next(x for x in range(2, Q) if len({power(x, i) for i in range(24)}) == 24)
assert power(g, 12) == 4  # -1 in F_25
inv2 = 3
pages = {}
incidences = defaultdict(list)
for center in range(Q):
    vertices = [add(center, power(g, i)) for i in range(24)]
    mids = []
    for i, u in enumerate(vertices):
        v = vertices[(i+1) % 24]
        incidences[edge(u, v)].append((center, i % 2))
        mids.append(mul(inv2, add(u, v)))
    assert len(set(vertices)) == len(set(mids)) == 24
    assert center not in vertices and center not in mids
    pages[center] = vertices

assert len(incidences) == 300
assert all(len(hits) == 2 for hits in incidences.values())
assert all(hits[0][1] == hits[1][1] for hits in incidences.values())
assert all(len({e for e, hits in incidences.items() if any(c == a for c, _ in hits)} &
               {e for e, hits in incidences.items() if any(c == b for c, _ in hits)}) == 1
           for a in range(Q) for b in range(a+1, Q))


def draw(path):
    paper, ink, muted = '#f7f4ed', '#25313a', '#5c6970'
    teal, copper = '#3b927e', '#b47751'
    parts = [f'<rect width="1180" height="340" fill="{paper}"/>',
             f'<text x="34" y="48" font-size="27" fill="{ink}">Two limits of the F₂₅ affine template</text>',
             f'<rect x="32" y="78" width="535" height="200" rx="12" fill="#fffdf8" stroke="#d7d4ca"/>',
             f'<rect x="588" y="78" width="560" height="200" rx="12" fill="#fffdf8" stroke="#d7d4ca"/>',
             f'<text x="52" y="114" font-size="19" fill="{teal}">Translation-invariant seed</text>',
             f'<text x="52" y="149" font-size="16" fill="{ink}">C₅ × C₅ acts on 12 Hamilton cycles</text>',
             f'<text x="52" y="180" font-size="16" fill="{ink}">12 ≢ 0 mod 5 ⇒ a cycle is fixed</text>',
             f'<text x="52" y="211" font-size="16" fill="{ink}">but C₅ × C₅ cannot embed in D₅₀</text>',
             f'<text x="52" y="248" font-size="15" fill="{muted}">No fully translation-invariant Hamilton seed</text>',
             f'<text x="608" y="114" font-size="19" fill="{copper}">All primitive-power pages rainbow</text>',
             f'<text x="608" y="149" font-size="16" fill="{ink}">25 pages demand 25 even incidences per color</text>',
             f'<text x="608" y="180" font-size="16" fill="{ink}">each edge belongs to 0 or 2 even pages</text>',
             f'<text x="608" y="211" font-size="16" fill="{ink}">odd demand ≠ even supply</text>',
             f'<text x="608" y="248" font-size="15" fill="{muted}">This does not rule out 11 selected pages</text>',
             f'<text x="34" y="316" font-size="13" fill="{muted}">Template limits only; finite K₂₅,t certificates establish the exact partition formula · Marlow</text>']
    path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 340" width="1180" height="340" role="img" aria-label="Two scoped finite-field template obstructions at 25 hubs" font-family="Georgia,serif">' + ''.join(parts) + '</svg>\n')


draw(Path(__file__).resolve().parent / 'art/prime_power_template_limits.svg')
print('primitive g:', g)
print('page 0:', pages[0])
print('edges:', len(incidences), 'page-pair intersections:', Q*(Q-1)//2)
print('edge parity incidences:', Counter(p for hits in incidences.values() for _, p in hits))
print('all 300 edges occur in exactly two pages, with the same parity in both')
