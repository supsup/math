"""Variations on Confluence at 1: other Collatz-type maps and turning angles, drawn as river systems.

Same drawing rule as collatz_confluence.py: the union of the trajectories of the starts is a forest
whose roots are the map's cycles; walking OUTWARD from a root, a value reached by the "divide" branch
turns the heading by +even radians and one reached by the "multiply" branch by -odd, unit steps.
Width and brightness grow with log(flow) = how many starts pass through. A map with several cycles
gets several mouths, placed on a small circle at the centre and flowing outward from it.

A start whose trajectory passes CAP (value or steps) before meeting anything known is counted as an
ESCAPEE and not drawn: for maps like 5n+1 most starts appear to grow without bound, which nobody has
proved either way; the caption counts them rather than hiding them.

Standard library only: python3 -I collatz_variations.py  ->  variations/*.svg + variations/index.html
"""
import math
import pathlib

OUT = pathlib.Path(__file__).with_name("variations")
CAP_VALUE, CAP_STEPS = 10**15, 3000
BG, INK, DIM, GOLD = "#0d1b2a", "#e8eef2", "#7d92a6", "#f4d58d"
PALETTE = ["#f4d58d", "#ff8fa3", "#8fd3ff", "#b8f28f", "#d7a6ff"]


def collatz(n):
    return (n // 2, True) if n % 2 == 0 else (3 * n + 1, False)


def collatz_minus(n):
    return (n // 2, True) if n % 2 == 0 else (3 * n - 1, False)


def shortcut(n):
    return (n // 2, True) if n % 2 == 0 else ((3 * n + 1) // 2, False)


def five(n):
    return (n // 2, True) if n % 2 == 0 else (5 * n + 1, False)


def build(f, starts):
    """parent[v] = successor (None for a cycle root), divided[v] = branch used to reach parent."""
    parent, divided, root_of = {}, {}, {}
    roots, escaped = [], 0
    for s in starts:
        path, seen, n = [], {}, s
        while n not in parent and n not in seen:
            if abs(n) > CAP_VALUE or len(path) > CAP_STEPS:
                break
            seen[n] = len(path)
            path.append(n)
            n, _ = f(n)
        else:
            if n in seen:  # closed a NEW cycle inside this path: root it at its smallest |value|
                cyc = path[seen[n]:]
                r = min(cyc, key=abs)
                roots.append(r)
                for v in cyc:
                    m, d = f(v)
                    parent[v], divided[v] = (None, None) if v == r else (m, d)
                for v in path[:seen[n]]:
                    m, d = f(v)
                    parent[v], divided[v] = m, d
            else:
                for v in path:
                    m, d = f(v)
                    parent[v], divided[v] = m, d
            continue
        escaped += 1
    flow = dict.fromkeys(parent, 0)
    for s in starts:
        if s not in parent:
            continue
        v, guard = s, 0
        while v is not None and guard < CAP_STEPS * 4:
            flow[v] += 1
            v = parent[v]
            guard += 1
    return parent, divided, flow, roots, escaped


def draw(name, title, f, starts, even, odd, notes):
    parent, divided, flow, roots, escaped = build(f, starts)
    children = {v: [] for v in parent}
    for v, p in parent.items():
        if p is not None:
            children[p].append(v)
    pos, head = {}, {}
    k = len(roots)
    for i, r in enumerate(sorted(roots, key=abs)):
        a = -math.pi / 2 + 2 * math.pi * i / max(k, 1)
        pos[r] = (0.0, 0.0) if k == 1 else (22 * math.cos(a), 22 * math.sin(a))
        head[r] = a
        stack = [r]
        while stack:
            p = stack.pop()
            for c in children[p]:
                if c in pos:
                    continue
                h = head[p] + (even if divided[c] else -odd)
                x, y = pos[p]
                pos[c] = (x + math.cos(h), y + math.sin(h))
                head[c] = h
                stack.append(c)
    xs = [q[0] for q in pos.values()]
    ys = [q[1] for q in pos.values()]
    W, H, bx, by, bw, bh = 480, 600, 16, 54, 448, 404
    sc = min(bw / (max(xs) - min(xs) or 1), bh / (max(ys) - min(ys) or 1))
    ox = bx + (bw - sc * (max(xs) - min(xs))) / 2
    oy = by + (bh - sc * (max(ys) - min(ys))) / 2

    def P(v):
        x, y = pos[v]
        return ox + (x - min(xs)) * sc, oy + (y - min(ys)) * sc

    basin = {}
    for r_i, r in enumerate(sorted(roots, key=abs)):
        stack = [r]
        while stack:
            p = stack.pop()
            basin[p] = r_i
            stack.extend(c for c in children[p] if c not in basin)
    top = math.log(max(flow.values()))
    groups = {}
    for v, p in parent.items():
        if p is None or v not in pos or p not in pos:
            continue
        t = math.log(flow[v]) / top if top > 0 else 1
        key = (basin.get(v, 0), min(13, int(t * 14)))
        groups.setdefault(key, []).append(v)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect width="{W}" height="{H}" fill="{BG}"/>',
           f'<text x="240" y="36" text-anchor="middle" font-family="serif" font-size="21" fill="{INK}">{title}</text>']
    for (b, lvl), vs in sorted(groups.items(), key=lambda kv: kv[0][1]):
        t = (lvl + 0.5) / 14
        base = PALETTE[b % len(PALETTE)] if k > 1 else None
        colour = base if base and t > 0.55 else f"rgb({int(110 + 134 * t)},{int(196 + 17 * t)},{int(226 - 85 * t)})"
        d = "".join("M%.1f %.1fL%.1f %.1f" % (*P(v), *P(parent[v])) for v in vs)
        out.append(f'<path d="{d}" fill="none" stroke="{colour}" stroke-opacity="{0.3 + 0.7 * t:.2f}" '
                   f'stroke-width="{0.3 + 3.2 * t ** 1.7:.2f}" stroke-linecap="round"/>')
    for i, r in enumerate(sorted(roots, key=abs)):
        x, y = P(r)
        col = PALETTE[i % len(PALETTE)] if k > 1 else GOLD
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{col}"/>')
        out.append(f'<text x="{x + 7:.1f}" y="{y + 4:.1f}" font-family="serif" font-style="italic" font-size="13" '
                   f'fill="{col}">{r}</text>')
    drawn = sum(1 for s in starts if s in parent)
    lines = [(f"{drawn:,} of {len(starts):,} starts drawn; {len(parent):,} values; mouths at {', '.join(str(r) for r in sorted(roots, key=abs))}", INK, 12)]
    if escaped:
        lines.append((f"{escaped:,} starts passed {CAP_VALUE:.0e} or {CAP_STEPS} steps first: not drawn", "#ffb3a7", 11))
    lines += [(n, DIM, 11) for n in notes]
    lines.append((f"turn +{even} after dividing, -{odd} after multiplying", DIM, 10.5))
    y = 480
    for text, colour, size in lines:
        out.append(f'<text x="240" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" '
                   f'fill="{colour}">{text}</text>')
        y += 18
    out.append(f'<text x="240" y="592" text-anchor="middle" font-family="sans-serif" font-size="9" fill="{DIM}">'
               'variations on Confluence at 1 · Confluence</text>')
    out.append("</svg>")
    path = OUT / f"{name}.svg"
    path.write_text("".join(out), encoding="utf-8")
    return name, drawn, len(starts), len(parent), sorted(roots, key=abs), escaped, path.stat().st_size


def main():
    OUT.mkdir(exist_ok=True)
    pos3000 = list(range(1, 3001))
    specs = [
        ("a_original", "3n+1, gentle (the original)", collatz, pos3000, 0.13, 0.27,
         ["the conjecture: every start reaches 1"]),
        ("b_curl", "3n+1, curling", collatz, pos3000, 0.21, 0.40, ["same rivers, sharper bends"]),
        ("c_storm", "3n+1, storm", collatz, pos3000, 0.30, 0.60, ["sharper still: the river knots"]),
        ("d_reed", "3n+1, reeds", collatz, pos3000, 0.06, 0.11, ["almost straight: it stretches into reeds"]),
        ("e_shortcut", "(3n+1)/2 shortcut", shortcut, pos3000, 0.13, 0.27,
         ["odd n jumps straight to (3n+1)/2: fewer, longer reaches"]),
        ("f_minus", "3n-1: three seas", collatz_minus, pos3000, 0.13, 0.27,
         ["three cycles, three river systems", "(the same as 3n+1 on the negative integers)"]),
        ("g_negative", "3n+1 on -1 .. -3000", collatz, list(range(-1, -3001, -1)), 0.13, 0.27,
         ["the same tree as 3n-1, value for value: negating n turns one map into the other"]),
        ("h_five", "5n+1: rivers that run off", five, pos3000, 0.13, 0.27,
         ["three cycles catch a few starts", "most appear to climb forever (unproved)"]),
    ]
    rows = [draw(*s) for s in specs]
    for r in rows:
        print(*r)
    cards = "".join(f'<figure><img src="{r[0]}.svg" alt="{r[0]}"><figcaption>{r[0]}</figcaption></figure>' for r in rows)
    (OUT / "index.html").write_text(
        "<!doctype html><meta charset=utf-8><title>Confluence variations</title>"
        "<style>body{margin:0;background:#06101a;display:grid;grid-template-columns:repeat(4,240px);gap:0}"
        "figure{margin:0}img{width:240px;height:300px;display:block}figcaption{display:none}</style>" + cards,
        encoding="utf-8")


if __name__ == "__main__":
    main()
