"""The trust-boundary card: what each family's Lean comparator states, who read it, and the gap to the paper.

Rows come from rows.json. A row is drawn only when it has at least TWO statement readers (Fixpoint's rule,
undervoice 16127); the rest are listed as pending in the footer count. The word 'proved' never appears.
Standard library only: python3 -I make_trust_card.py  ->  trust-boundary.svg
"""
import json
import pathlib
import textwrap
from xml.sax.saxutils import escape

HERE = pathlib.Path(__file__).resolve().parent
BG, INK, DIM, GOLD, AQUA, ROSE = "#0d1b2a", "#e8eef2", "#7d92a6", "#f4d58d", "#8fd3ff", "#ff8fa3"


def row_height(r):
    return 15 + 13 * len(textwrap.wrap("Lean: " + r["lean"], 82)) + 13 * len(textwrap.wrap("Gap: " + r["gap"], 82)) + 22


def main():
    data = json.loads((HERE / "rows.json").read_text())
    rows = [r for r in data["rows"] if len(set(r["readers"])) >= 2]
    pending = [r for r in data["rows"] if len(set(r["readers"])) < 2]
    text = json.dumps(rows).lower()
    long = [r["family"] for r in rows if len(r["title"]) > 58]
    assert not long, f"titles too long to sit beside the verdict: {long}"
    assert "proved" not in text, "the table must not say 'proved'"
    pages, cur, used = [], [], 0
    for r in rows:
        h = row_height(r)
        if cur and 84 + used + h > 548:
            pages.append(cur)
            cur, used = [], 0
        cur.append(r)
        used += h
    if cur:
        pages.append(cur)
    for pi, page in enumerate(pages, start=1):
        draw(page, pi, len(pages), len(rows), len(pending))


def draw(rows, pi, npages, nrows, npending):
    W = 480
    o = [
         f'<text x="240" y="36" text-anchor="middle" font-family="serif" font-size="21" fill="{INK}">Where the trust boundary sits</text>',
         f'<text x="240" y="57" text-anchor="middle" font-family="serif" font-style="italic" font-size="12.5" fill="{DIM}">'
         'what the Lean kernel checks, against what each paper claims'
         + (f' ({pi} of {npages})' if npages > 1 else '') + '</text>']
    y = 84
    for r in rows:
        colour = AQUA if r["verdict"] == "MATCHES" else ROSE
        o.append(f'<text x="20" y="{y}" font-family="sans-serif" font-size="12.5" fill="{INK}">'
                 f'<tspan fill="{GOLD}">{escape(r["family"])}</tspan>  {escape(r["title"])}</text>')
        o.append(f'<text x="460" y="{y}" text-anchor="end" font-family="sans-serif" font-size="10.5" fill="{colour}">{r["verdict"]}</text>')
        y += 15
        for line in textwrap.wrap("Lean: " + r["lean"], 82):
            o.append(f'<text x="28" y="{y}" font-family="sans-serif" font-size="10" fill="{DIM}">{escape(line)}</text>')
            y += 13
        for line in textwrap.wrap("Gap: " + r["gap"], 82):
            o.append(f'<text x="28" y="{y}" font-family="sans-serif" font-size="10" fill="{colour if r["verdict"] != "MATCHES" else DIM}">{escape(line)}</text>')
            y += 13
        o.append(f'<text x="28" y="{y}" font-family="sans-serif" font-size="9.5" fill="{DIM}">'
                 f'statement read by: {escape(", ".join(r["readers"]))}</text>')
        y += 22
    assert y < 548, f"rows overflow the card (y = {y}); split into two cards"
    notes = ["Every row: the Lean artifact kernel-checks the stated formal statement (permitted axioms only)."]
    if pi == npages:  # counts only on the LAST page, so earlier (published) pages stay byte-stable as rows are added
        notes.append(f"All {nrows} rows have two independent statement readings." if npending == 0 else
                     f"{nrows} rows read twice; {npending} more " + ("awaits" if npending == 1 else "await")
                     + " a second independent reading.")
    # A full page keeps the 480x600 card shape (and its bytes); a short LAST page is sized to its content
    # (Fixpoint 16291: page 3 was 70% empty), never below 300.
    H = 600 if (pi < npages or y > 548 - 120) else max(300, int(y) + 80)
    o.insert(0, f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    o.insert(0, f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    yy = H - 44
    for t in notes:
        o.append(f'<text x="240" y="{yy}" text-anchor="middle" font-family="sans-serif" font-size="10.5" fill="{DIM}">{escape(t)}</text>')
        yy += 15
    o.append(f'<text x="240" y="{H - 8}" text-anchor="middle" font-family="sans-serif" font-size="9" fill="{DIM}">trust-boundary table · Confluence, with Fixpoint, Lattice and Marlow</text>')
    o.append("</svg>")
    p = HERE / ("trust-boundary.svg" if pi == 1 else f"trust-boundary-{pi}.svg")
    p.write_text("".join(o), encoding="utf-8")
    print(p.name, p.stat().st_size, "bytes; rows", [r["family"] for r in rows])


if __name__ == "__main__":
    main()
