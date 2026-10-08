"""Exact attachment-count census for the next cycle/triangle collision level.

The weighted formula counts every labelled attachment to either fixed critical
base without enumerating cycle edge sets. Run from the repo root with
python3 -I playground/marlow/05_extension_stability.py.
"""

from collections import Counter
from math import comb, factorial, perm
from pathlib import Path


HERE = Path(__file__).resolve().parent


def total(k, a, b, alpha, beta, bridge):
    """Forbidden-copy total; alpha/beta mark the two bridge endpoints."""
    q = factorial(k - 2)
    count = q * (comb(a, 2) + comb(b, 2)) + (k - a) * (k - b)
    if not bridge:
        return count
    count -= (1 - alpha) * (1 - beta)
    for p in range(1, k):
        left = alpha if p == 1 else (a - alpha) * perm(k - 2, p - 2)
        right_size = k - p
        right = beta if right_size == 1 else (b - beta) * perm(k - 2, right_size - 2)
        count += left * right
    return count


def census(m, bridge):
    """Multiplicity of each total among the 2^(2m-2) labelled attachments."""
    k = m - 1
    counts = Counter()
    for a in range(k + 1):
        for b in range(k + 1):
            if not bridge:
                counts[total(k, a, b, 0, 0, False)] += comb(k, a) * comb(k, b)
                continue
            for alpha in (0, 1):
                for beta in (0, 1):
                    if not (0 <= a - alpha <= k - 1 and 0 <= b - beta <= k - 1):
                        continue
                    weight = comb(k - 1, a - alpha) * comb(k - 1, b - beta)
                    counts[total(k, a, b, alpha, beta, True)] += weight
    assert sum(counts.values()) == 1 << (2 * k)
    values = sorted(counts)
    return {'minimum': values[0], 'minimizers': counts[values[0]],
            'second': values[1], 'second_attainers': counts[values[1]],
            'gap': values[1] - values[0]}


def drawing(path, results):
    """Show the gap between the smallest two distinct totals."""
    ink, green, gold, paper = '#242320', '#468875', '#b58a45', '#f7f4ed'
    parts = [f'<rect width="960" height="635" fill="{paper}"/>',
             f'<text x="480" y="43" text-anchor="middle" font-size="25" fill="{ink}">The next collision level</text>',
             f'<text x="480" y="70" text-anchor="middle" font-size="15" fill="{ink}">Gap from the smallest to the second-smallest forbidden-copy total</text>']
    scale = 55
    for row, m in enumerate(range(6, 11)):
        y = 117 + 89 * row
        parts.append(f'<text x="100" y="{y + 28}" text-anchor="end" font-size="18" fill="{ink}">m = {m}</text>')
        for offset, bridge, color in ((0, 0, green), (28, 1, gold)):
            gap = results[(m, bridge)]['gap']
            width = gap * scale
            parts.append(f'<rect x="140" y="{y + offset}" width="{width}" height="22" rx="3" fill="{color}"/>')
            parts.append(f'<text x="{150 + width}" y="{y + offset + 17}" font-size="16" fill="{ink}">+{gap}</text>')
    parts.extend([
        '<rect x="674" y="112" width="245" height="345" rx="8" fill="#eee8da"/>',
        f'<text x="695" y="150" font-size="18" fill="{ink}">For m ≥ 7</text>',
        f'<text x="695" y="197" font-size="16" fill="{ink}">No bridge: + (m−2)</text>',
        f'<text x="695" y="232" font-size="16" fill="{ink}">One bridge: + (m−3)</text>',
        f'<text x="695" y="300" font-size="16" fill="{ink}">Second-level choices</text>',
        f'<text x="695" y="337" font-size="15" fill="{ink}">2(m−1) / 2(m−2)</text>',
        f'<text x="695" y="408" font-size="14" fill="{ink}">Fixed critical base;</text>',
        f'<text x="695" y="432" font-size="14" fill="{ink}">labelled attachments</text>',
        f'<rect x="140" y="555" width="15" height="15" fill="{green}"/>',
        f'<text x="163" y="568" font-size="14" fill="{ink}">two cliques, no bridge</text>',
        f'<rect x="440" y="555" width="15" height="15" fill="{gold}"/>',
        f'<text x="463" y="568" font-size="14" fill="{ink}">two cliques, one red bridge</text>',
        f'<text x="480" y="615" text-anchor="middle" font-size="12" fill="{green}">Critical types: Radziszowski &amp; Jin (1994), Thm 3 · conditional extension result</text>',
    ])
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 635" width="960" height="635" role="img" aria-label="Gap between smallest and second-smallest forbidden-copy totals in critical cycle triangle extensions" font-family="Georgia, serif">' + ''.join(parts) + '</svg>\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)


def main():
    results = {(m, bridge): census(m, bridge)
               for m in range(4, 12) for bridge in (0, 1)}
    assert [(results[(m, 0)]['minimum'], results[(m, 1)]['minimum'])
            for m in (4, 5, 6)] == [(3, 2), (8, 9), (16, 16)]
    for m in range(7, 12):
        k = m - 1
        base = (k - 1) ** 2
        assert results[(m, 0)] == {'minimum': base, 'minimizers': k * k,
                                   'second': base + k - 1, 'second_attainers': 2 * k,
                                   'gap': k - 1}
        assert results[(m, 1)] == {'minimum': base, 'minimizers': 1,
                                   'second': base + k - 2, 'second_attainers': 2 * (k - 1),
                                   'gap': k - 2}
    drawing(HERE / 'art/extension_stability.svg', results)
    for key, value in sorted(results.items()):
        print(key, value)


if __name__ == '__main__':
    main()
