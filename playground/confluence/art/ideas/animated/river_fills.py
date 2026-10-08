"""The river fills: Confluence's Collatz river (collatz_confluence.py), animated with SVG SMIL only.

Same geometry as the original: the trajectories of 1..3000 walked OUTWARD from 1 (turn +EVEN after
halving, -ODD after 3n+1, unit step), width and brightness by log(flow), edges bucketed into 14 width
levels. New here: each edge is also given a depth band, depth = its child's number of steps to 1.
Water enters at the rim (the deepest band, 216 steps out) and the wavefront moves inward one band at a
time, so the far tributaries light first and the trunk near 1 lights last; the gold mouth at 1 appears
when the wave arrives. Then the picture HOLDS (fill="freeze", no loop).

No-animation fallback: every path's static attributes ARE the final river. Each <animate> starts at
t=0 and runs values="0;0;peak;final;final" (opacity; the last keyTime must be 1 or SMIL drops it), so while it runs it overrides the static value from the very
first frame (which a delayed begin= would not do: before a begin time the static, fully-drawn value
shows). A renderer that ignores SMIL simply never applies the override and shows the whole river.

No script, no event handlers, no href/url(), no foreignObject. Standard library, deterministic:
python3 -I river_fills.py  ->  river_fills.svg
"""
import math
import pathlib
import sys

ART = pathlib.Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True  # importing must not drop a __pycache__ into the art folder
sys.path.insert(0, str(ART))
import collatz_confluence as cc  # noqa: E402  (build, constants; its main() is not run)

N, EVEN, ODD, W, H, LEVELS = cc.N, cc.EVEN, cc.ODD, cc.W, cc.H, cc.LEVELS
BG, INK, DIM, GOLD = cc.BG, cc.INK, cc.DIM, cc.GOLD
BANDS = 24            # depth bands -> animation groups along the river
T0, T1 = 0.4, 10.0    # wavefront leaves the rim at T0 s, reaches 1 at T1 s
FADE = 0.9            # seconds for one group to come up
TOTAL = T1 + FADE + 0.4


def main():
    parent, halved, flow, children, steps = cc.build(N)
    depth = {1: 0}
    order = [1]
    for p in order:                       # BFS from 1: depth = steps to 1 for every visited value
        for c in children[p]:
            depth[c] = depth[p] + 1
            order.append(c)
    dmax = max(depth.values())

    # layout: identical to collatz_confluence.main()
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
    groups = {}                            # (bucket, band) -> edges; band 0 = rim, BANDS-1 = mouth
    for v, p in parent.items():
        if p is None:
            continue
        t = math.log(flow[v]) / top
        bucket = min(LEVELS - 1, int(t * LEVELS))
        band = min(BANDS - 1, int((dmax - depth[v]) * BANDS / dmax))
        groups.setdefault((bucket, band), []).append(v)

    def kt(sec):
        return f"{sec / TOTAL:.4f}"

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect width="{W}" height="{H}" fill="{BG}"/>',
           f'<text x="240" y="38" text-anchor="middle" font-family="serif" font-size="23" fill="{INK}">'
           'The river fills</text>']
    for (bucket, band) in sorted(groups):  # bucket-major keeps the original's paint order
        vs = groups[(bucket, band)]
        t = (bucket + 0.5) / LEVELS
        colour = f"rgb({int(110 + 134 * t)},{int(196 + 17 * t)},{int(226 - 85 * t)})"
        op = 0.3 + 0.7 * t
        d = "".join(f"M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}"
                    for (x1, y1), (x2, y2) in ((P(v), P(parent[v])) for v in vs))
        start = T0 + (T1 - T0) * band / (BANDS - 1)
        out.append(f'<path d="{d}" fill="none" stroke="{colour}" stroke-opacity="{op:.2f}" '
                   f'stroke-width="{0.3 + 3.4 * t ** 1.7:.2f}" stroke-linecap="round">'
                   f'<animate attributeName="stroke-opacity" dur="{TOTAL:.1f}s" fill="freeze" '
                   f'values="0;0;{min(1, op + 0.3):.2f};{op:.2f};{op:.2f}" '
                   f'keyTimes="0;{kt(start)};{kt(start + FADE * 0.5)};{kt(start + FADE)};1"/></path>')
    mx, my = P(1)
    arrive = kt(T1)
    out.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="3.6" fill="{GOLD}">'
               f'<animate attributeName="r" dur="{TOTAL:.1f}s" fill="freeze" values="0;0;6;3.6" '
               f'keyTimes="0;{arrive};{kt(T1 + FADE * 0.5)};1"/></circle>')
    out.append(f'<text x="{mx + 9:.1f}" y="{my + 4:.1f}" font-family="serif" font-style="italic" font-size="15" '
               f'fill="{GOLD}">1</text>')
    deepest = max(steps, key=lambda s: (steps[s], -s))
    lines = [
        (f"all {N:,} starts drain to 1 under n -> n/2 or 3n+1", INK, 12.5),
        (f"{len(parent):,} values visited, the highest {max(parent):,}; the longest run, from {deepest},", DIM, 11),
        (f"takes {steps[deepest]} steps. Water enters at the rim, {dmax} steps out, and reaches 1 last.", DIM, 11),
        (f"Turn +{EVEN} rad after halving, -{ODD} after 3n+1, walking out from 1.", DIM, 11),
        ("Checked here for these starts only: the Collatz conjecture is open.", DIM, 11),
    ]
    y = 500
    for text, colour, size in lines:
        out.append(f'<text x="240" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" '
                   f'fill="{colour}">{text}</text>')
        y += 18
    out.append(f'<text x="240" y="590" text-anchor="middle" font-family="sans-serif" font-size="9.5" '
               f'fill="{DIM}">ideas after Confluence at 1 · Confluence</text>')
    out.append("</svg>")
    p = pathlib.Path(__file__).with_name("river_fills.svg")
    p.write_text("".join(out), encoding="utf-8")
    print(p.name, p.stat().st_size, "bytes; groups", len(groups), "values", len(parent), "highest", max(parent),
          "longest", deepest, steps[deepest], "max depth", dmax, "flow(1)", flow[1])


if __name__ == "__main__":
    main()
