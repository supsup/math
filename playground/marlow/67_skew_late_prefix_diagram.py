"""Draw the exact p=13 transformed late-prefix exclusion geometry.

Run: python3 -I playground/marlow/67_skew_late_prefix_diagram.py
"""
from pathlib import Path
from xml.sax.saxutils import escape


p = 13
a = p - 3
k = (p - 1) // 2
c = k - 2
D = a + 1
delta = (1 - a) * pow(D, -1, p) % p
I = set(range(c + 1))
minus_I = {-x % p for x in I}
minus_aI = {-a * x % p for x in I}
B = set(range(p)) - (minus_I | minus_aI)
G = {
    w for w in range(p)
    if pow(w * (w + delta) % p, k, p) == p - 1
    and pow((w - 1) * (w + delta - 1) % p, k, p) == p - 1
}
G_X = {(D * w - a) % p for w in G}
survivors = B & G_X
assert len(I & {a * x % p for x in I}) == 3
assert len(B) == 6 and G_X == {4, 6, 7, 9} and survivors == {4, 7}

rows = [
    ("−I", minus_I, "#eaa789", "first relabel progression"),
    ("−aI", minus_aI, "#d87956", "second relabel progression"),
    ("B", B, "#83a7d9", "available parameters"),
    ("Gₓ", G_X, "#ebc668", "two character tests pass"),
    ("B ∩ Gₓ", survivors, "#6fb391", "usable for every pair"),
]

left, top, cell, gap = 226, 104, 48, 5
width, height = 1160, 484
pieces = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
    '<rect width="100%" height="100%" fill="#fbfaf7"/>',
    '<text x="36" y="45" font-family="Georgia,serif" font-size="24" fill="#173048">A last-pair witness in thirteen residues</text>',
    '<text x="36" y="72" font-family="Arial,sans-serif" font-size="14" fill="#4c6478">p = 13 · a = −3 · c = 4 · X = (a + 1)w − a</text>',
    '<text x="37" y="130" font-family="Arial,sans-serif" font-size="13" fill="#526777">set</text>',
]
for x in range(p):
    xpos = left + x * (cell + gap)
    pieces.append(f'<text x="{xpos + cell/2:.1f}" y="96" text-anchor="middle" font-family="Arial,sans-serif" font-size="13" fill="#53697d">{x}</text>')

for ri, (label, members, color, meaning) in enumerate(rows):
    ypos = top + ri * 63
    pieces.append(f'<text x="37" y="{ypos + 31}" font-family="Arial,sans-serif" font-size="17" font-weight="bold" fill="#243d53">{escape(label)}</text>')
    for x in range(p):
        xpos = left + x * (cell + gap)
        fill = color if x in members else "#eceff1"
        pieces.append(f'<rect x="{xpos}" y="{ypos}" width="{cell}" height="{cell}" rx="7" fill="{fill}"/>')
        if x in members:
            pieces.append(f'<text x="{xpos + cell/2:.1f}" y="{ypos + 31}" text-anchor="middle" font-family="Arial,sans-serif" font-size="16" font-weight="bold" fill="#173048">{x}</text>')
    pieces.append(f'<text x="{left + p*(cell+gap) + 13}" y="{ypos + 20}" font-family="Arial,sans-serif" font-size="15" font-weight="bold" fill="#243d53">{len(members)}</text>')
    pieces.append(f'<text x="{left + p*(cell+gap) + 13}" y="{ypos + 39}" font-family="Arial,sans-serif" font-size="11" fill="#617587">{escape(meaning)}</text>')

pieces.append('<text x="36" y="454" font-family="Arial,sans-serif" font-size="14" fill="#405a70">|B| = 13 − 5 − 5 + |I ∩ aI| = 6; the two green sites survive both character tests.</text>')
pieces.append('</svg>')
out = Path(__file__).with_name('art') / 'skew_late_prefix_geometry.svg'
out.write_text('\n'.join(pieces) + '\n')
print(out, 'available', len(B), 'character_good', len(G_X), 'survivors', sorted(survivors))
