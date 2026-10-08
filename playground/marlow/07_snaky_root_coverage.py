"""Measure how the 32 children of Snaky's final certificate cover its board.

Run: python3 -I playground/marlow/07_snaky_root_coverage.py
This reconstructs certificate sets; it does not play the game.
"""

from collections import Counter
from hashlib import sha256
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERT = HERE.parent.parent / 'preprints/Snaky-in-21-Maker-moves-September-25-2026/verification/certificate.txt'
CERT_SHA256 = '3fa12d36a6d4dbb185e3f2808c8dfde13d85ee309afbca030d6ad17ae9fe3d04'
SYMBOLS = '0123456789ABCDEFG'
SNAKY = {(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (4, 1)}


def point(token):
    assert len(token) == 2
    return tuple(SYMBOLS.index(c) for c in token)


def transform(points, code, dx, dy):
    result = set()
    for x, y in points:
        if code & 2:
            x = -x
        if code & 4:
            y = -y
        if code & 1:
            x, y = y, x
        result.add((x + dx, y + dy))
    return result


def reconstruct(data):
    """Return final required/envelope/height and its 32 child envelopes."""
    cards = [(SNAKY - {p}, set(SNAKY), 1) for p in sorted(SNAKY)]

    def ref(token):
        prefix, sep, suffix = token.partition(':')
        index = int(prefix)
        assert 0 <= index < len(cards)
        a, t, h = cards[index]
        if not sep:
            return set(a), set(t), h
        assert len(suffix) == 3 and suffix[0] in '01234567'
        dx, dy = point(suffix[1:])
        code = int(suffix[0])
        return transform(a, code, dx, dy), transform(t, code, dx, dy), h

    def parse(tokens):
        pivot = point(next(tokens))
        children = []
        while True:
            token = next(tokens)
            if token == ')':
                break
            children.append(parse(tokens) if token == '(' else ref(token))
        assert children
        required = set().union(*(child[0] for child in children))
        common = set.intersection(*(child[1] for child in children))
        envelope = {pivot} | set().union(*(child[1] for child in children))
        return ((required | common) - {pivot}, envelope,
                1 + max(child[2] for child in children))

    final_tokens = None
    for line in data.splitlines():
        words = line.replace('(', ' ( ').replace(')', ' ) ').split()
        assert int(words[0]) == len(cards)
        final_tokens = words[2:]
        tokens = iter(words[1:] + [')'])
        card = parse(tokens)
        assert next(tokens, None) is None
        assert card[0] <= card[1]
        cards.append(card)
    assert len(cards) == 728 and final_tokens is not None
    assert len(final_tokens) == 32 and all(token != '(' for token in final_tokens)
    children = [ref(token)[1] for token in final_tokens]
    return cards[-1], children


def coverage(root, children):
    a, t, h = root
    assert a == set() and len(t) == 251 and h == 21
    assert all(0 <= x <= 16 and 0 <= y <= 16 for x, y in t)
    counts = Counter(cell for child in children for cell in child)
    assert set(counts) == t and counts[(8, 8)] == 32
    assert sum(counts.values()) == 4420
    assert max(n for cell, n in counts.items() if cell != (8, 8)) == 31
    assert sum(n == 31 for cell, n in counts.items() if cell != (8, 8)) == 43
    assert sum(n == 1 for cell, n in counts.items() if cell != (8, 8)) == 3
    assert set.intersection(*children) == {(8, 8)}
    return counts


def color(value):
    """Pale blue to rust; dark pivot uses its own color."""
    lo, hi = (184, 207, 213), (173, 79, 54)
    f = (value - 1) / 30
    rgb = tuple(round(a + f * (b - a)) for a, b in zip(lo, hi))
    return '#%02x%02x%02x' % rgb


def drawing(path, counts):
    ink, paper = '#242320', '#f7f4ed'
    parts = [f'<rect width="950" height="750" fill="{paper}"/>',
             f'<text x="475" y="43" text-anchor="middle" font-size="26" fill="{ink}">One root move, 32 certified branches</text>',
             f'<text x="475" y="71" text-anchor="middle" font-size="15" fill="{ink}">How many child envelopes contain each cell of the 21-move Snaky certificate?</text>']
    size, x0, y0 = 29, 58, 111
    for y in range(16, -1, -1):
        for x in range(17):
            px, py = x0 + x * size, y0 + (16 - y) * size
            cell = (x, y)
            if cell == (8, 8):
                fill = '#242320'
            elif cell in counts:
                fill = color(counts[cell])
            else:
                fill = '#fffdf8'
            parts.append(f'<rect x="{px}" y="{py}" width="{size-2}" height="{size-2}" rx="2" fill="{fill}"/>')
    parts.extend([
        '<rect x="600" y="122" width="297" height="420" rx="8" fill="#eee8da"/>',
        f'<text x="623" y="164" font-size="18" fill="{ink}">The root pivot is (8, 8)</text>',
        f'<text x="623" y="204" font-size="16" fill="{ink}">32 child envelopes</text>',
        f'<text x="623" y="245" font-size="16" fill="{ink}">251-cell union</text>',
        f'<text x="623" y="307" font-size="19" fill="{ink}">43 cells touch 31</text>',
        f'<text x="623" y="337" font-size="15" fill="{ink}">of the 32 child envelopes.</text>',
        f'<text x="623" y="391" font-size="15" fill="{ink}">A Breaker cell there leaves</text>',
        f'<text x="623" y="417" font-size="15" fill="{ink}">one child precondition intact.</text>',
        f'<text x="623" y="497" font-size="14" fill="{ink}">This counts proof preconditions,</text>',
        f'<text x="623" y="521" font-size="14" fill="{ink}">not winning probabilities.</text>',
        f'<rect x="58" y="652" width="25" height="19" fill="{color(1)}"/>',
        f'<text x="90" y="667" font-size="14" fill="{ink}">1 child</text>',
        f'<rect x="170" y="652" width="25" height="19" fill="{color(31)}"/>',
        f'<text x="202" y="667" font-size="14" fill="{ink}">31 children</text>',
        f'<rect x="324" y="652" width="25" height="19" fill="{ink}"/>',
        f'<text x="356" y="667" font-size="14" fill="{ink}">Maker pivot</text>',
        f'<rect x="490" y="652" width="25" height="19" fill="#fffdf8"/>',
        f'<text x="522" y="667" font-size="14" fill="{ink}">outside support</text>',
        f'<text x="475" y="721" text-anchor="middle" font-size="12" fill="{ink}">From family 187 certificate; this picture does not simulate the game.</text>',
    ])
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 750" width="950" height="750" role="img" aria-label="Coverage heatmap of the 32 Snaky final certificate child envelopes" font-family="Georgia, serif">' + ''.join(parts) + '</svg>\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)


def main():
    payload = CERT.read_bytes()
    assert sha256(payload).hexdigest() == CERT_SHA256
    root, children = reconstruct(payload.decode('ascii'))
    counts = coverage(root, children)
    drawing(HERE / 'art/snaky_root_coverage.svg', counts)
    print('root:', len(root[1]), 'cells; height:', root[2], '; children:', len(children))
    print('child membership total:', sum(counts.values()))
    print('off-pivot coverage histogram:', sorted(Counter(n for cell, n in counts.items()
                                                   if cell != (8, 8)).items()))


if __name__ == '__main__':
    main()
