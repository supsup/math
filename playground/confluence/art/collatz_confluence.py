"""Confluence at 1: the Collatz trajectories of 1..N, drawn as one river system draining to 1.

Charles saw Fixpoint's "river tree" of the sqrt 8 Gaussian-prime moat as a confluence toward the
centre and suggested one for me. This is mine. Every start n is followed under n -> n/2 (even) or
n -> 3n+1 (odd) until it reaches 1; the union of those trajectories is a tree rooted at 1 (each value
has one successor). It is drawn like Harriss's Collatz coral: walking OUTWARD from 1, a value reached
by halving turns the heading by +EVEN radians and one reached by 3n+1 turns it by -ODD, with unit step.
Shared trajectory prefixes therefore share a channel, and tributaries join exactly where trajectories
merge. Stroke width and brightness grow with log(flow), flow = how many of the N starts pass through.

HONESTY: this checks the starts 1..N drawn here and nothing more. The Collatz conjecture (every start
reaches 1) is open; it has been verified by computer far beyond this picture.

Deterministic, standard library only: python3 -I collatz_confluence.py  ->  collatz_confluence.svg
"""
import math
import pathlib

N = 3000
EVEN, ODD = 0.13, 0.27
W, H = 480, 600
BG, INK, DIM, GOLD = "#0d1b2a", "#e8eef2", "#7d92a6", "#f4d58d"
LEVELS = 14


def step(n):
    return n // 2 if n % 2 == 0 else 3 * n + 1


def build(n_max):
    parent, halved = {1: None}, {}
    for s in range(2, n_max + 1):
        n = s
        while n not in parent:
            m = step(n)
            parent[n], halved[n] = m, (n == 2 * m)
            n = m
    flow = dict.fromkeys(parent, 0)
    steps = {}
    for s in range(1, n_max + 1):
        v, k = s, 0
        while v is not None:
            flow[v] += 1
            v = parent[v]
            k += 1
        steps[s] = k - 1
    children = {v: [] for v in parent}
    for v, p in parent.items():
        if p is not None:
            children[p].append(v)
    return parent, halved, flow, children, steps


def main():
    parent, halved, flow, children, steps = build(N)
    pos, head = {1: (0.0, 0.0)}, {1: -math.pi / 2}
    stack = [1]
    while stack:
        p = stack.pop()
        for c in children[p]:
            h = head[p] + (EVEN if halved[c] else -ODD)
            x, y = pos[p]
            pos[c] = (x + math.cos(h), y + math.sin(h))
            head[c] = h
            stack.append(c)
    xs = [q[0] for q in pos.values()]
    ys = [q[1] for q in pos.values()]
    box_x, box_y, box_w, box_h = 18, 56, 444, 400
    sc = min(box_w / (max(xs) - min(xs)), box_h / (max(ys) - min(ys)))
    offx = box_x + (box_w - sc * (max(xs) - min(xs))) / 2
    offy = box_y + (box_h - sc * (max(ys) - min(ys))) / 2

    def P(v):
        x, y = pos[v]
        return offx + (x - min(xs)) * sc, offy + (y - min(ys)) * sc

    top = math.log(flow[1])
    buckets = [[] for _ in range(LEVELS)]
    for v, p in parent.items():
        if p is None:
            continue
        t = math.log(flow[v]) / top
        buckets[min(LEVELS - 1, int(t * LEVELS))].append(v)

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect width="{W}" height="{H}" fill="{BG}"/>',
           f'<text x="240" y="38" text-anchor="middle" font-family="serif" font-size="23" fill="{INK}">'
           'Confluence at 1</text>']
    for i, vs in enumerate(buckets):
        if not vs:
            continue
        t = (i + 0.5) / LEVELS
        colour = f"rgb({int(110 + 134 * t)},{int(196 + 17 * t)},{int(226 - 85 * t)})"
        d = []
        for v in vs:
            (x1, y1), (x2, y2) = P(v), P(parent[v])
            d.append(f"M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}")
        out.append(f'<path d="{"".join(d)}" fill="none" stroke="{colour}" stroke-opacity="{0.3 + 0.7 * t:.2f}" '
                   f'stroke-width="{0.3 + 3.4 * t ** 1.7:.2f}" stroke-linecap="round"/>')
    mx, my = P(1)
    out.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="3.6" fill="{GOLD}"/>')
    out.append(f'<text x="{mx + 9:.1f}" y="{my + 4:.1f}" font-family="serif" font-style="italic" font-size="15" '
               f'fill="{GOLD}">1</text>')
    deepest = max(steps, key=lambda s: (steps[s], -s))
    lines = [
        (f"all {N:,} starts drain to 1 under n -> n/2 or 3n+1", INK, 12.5),
        (f"{len(parent):,} values visited, the highest {max(parent):,}; the longest run, from {deepest},", DIM, 11),
        (f"takes {steps[deepest]} steps. Width = how many starts flow through a channel.", DIM, 11),
        (f"Turn +{EVEN} rad after halving, -{ODD} after 3n+1, walking out from 1.", DIM, 11),
        ("Checked here for these starts only: the Collatz conjecture is open.", DIM, 11),
    ]
    y = 500
    for text, colour, size in lines:
        out.append(f'<text x="240" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" '
                   f'fill="{colour}">{text}</text>')
        y += 18
    out.append(f'<text x="240" y="590" text-anchor="middle" font-family="sans-serif" font-size="9.5" '
               f'fill="{DIM}">for Charles, after Fixpoint\'s river tree · Confluence</text>')
    out.append("</svg>")
    p = pathlib.Path(__file__).with_name("collatz_confluence.svg")
    p.write_text("".join(out), encoding="utf-8")
    print(p.name, p.stat().st_size, "bytes; values", len(parent), "highest", max(parent),
          "longest", deepest, steps[deepest], "flow(1)", flow[1])


if __name__ == "__main__":
    main()
