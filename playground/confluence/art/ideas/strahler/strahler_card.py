"""Card: the Horton plot of the Collatz river (starts 1..10^6) against 20 random binary trees.

Computes everything (via strahler.py), then draws log10(N_k) against order k with the random-tree band,
and the bifurcation ratios with their z-scores. Standard library only: python3 -I strahler_card.py
"""
import math
import pathlib
import random
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import strahler as s  # noqa: E402

N, SEEDS = 1_000_000, 20
BG, INK, DIM, GOLD, AQUA = "#0d1b2a", "#e8eef2", "#7d92a6", "#f4d58d", "#8fd3ff"


def main():
    ch, root = s.collatz_tree(N)
    cnt, _ = s.horton(ch, root)
    rb = s.ratios(cnt)
    rng = random.Random(7)
    ctrl_counts, per_k = [], {}
    for _ in range(SEEDS):
        rc, rr = s.remy_tree(cnt[1], rng)
        c2, _ = s.horton(rc, rr)
        ctrl_counts.append(c2)
        for k, v in enumerate(s.ratios(c2), start=1):
            per_k.setdefault(k, []).append(v)
    K = max([max(cnt)] + [max(c2) for c2 in ctrl_counts])
    W, H = 480, 600
    px0, py0, pw, ph = 70, 70, 370, 250
    ymax = math.log10(cnt[1]) + 0.2

    def P(k, y):
        return px0 + (k - 1) / (K - 1) * pw, py0 + ph - y / ymax * ph

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect width="{W}" height="{H}" fill="{BG}"/>',
           f'<text x="240" y="38" text-anchor="middle" font-family="serif" font-size="21" fill="{INK}">'
           'Does the Collatz river obey Horton?</text>',
           f'<rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" fill="none" stroke="{DIM}" stroke-width="0.7"/>']
    for e in range(0, int(ymax) + 1):
        x0, y = P(1, e)
        out.append(f'<line x1="{px0}" y1="{y:.1f}" x2="{px0 + pw}" y2="{y:.1f}" stroke="{DIM}" stroke-opacity="0.25"/>')
        out.append(f'<text x="{px0 - 8}" y="{y + 4:.1f}" text-anchor="end" font-family="sans-serif" font-size="10" fill="{DIM}">10<tspan dy="-5" font-size="8">{e}</tspan></text>')
    for k in range(1, K + 1):
        x, _ = P(k, 0)
        out.append(f'<text x="{x:.1f}" y="{py0 + ph + 16}" text-anchor="middle" font-family="sans-serif" font-size="10" fill="{DIM}">{k}</text>')
    out.append(f'<text x="{px0 + pw / 2}" y="{py0 + ph + 32}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="{DIM}">Strahler order k</text>')
    out.append(f'<text x="22" y="{py0 + ph / 2}" font-family="sans-serif" font-size="11" fill="{DIM}" transform="rotate(-90 22 {py0 + ph / 2})" text-anchor="middle">streams of order k</text>')
    for c2 in ctrl_counts:
        pts = " ".join("%.1f,%.1f" % P(k, math.log10(c2[k])) for k in sorted(c2))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{AQUA}" stroke-opacity="0.28" stroke-width="1"/>')
    pts = " ".join("%.1f,%.1f" % P(k, math.log10(cnt[k])) for k in sorted(cnt))
    out.append(f'<polyline points="{pts}" fill="none" stroke="{GOLD}" stroke-width="2.4"/>')
    for k in sorted(cnt):
        x, y = P(k, math.log10(cnt[k]))
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{GOLD}"/>')
    out.append(f'<text x="{px0 + pw - 6}" y="{py0 + 16}" text-anchor="end" font-family="sans-serif" font-size="11" fill="{GOLD}">Collatz, starts 1..{N:,}</text>')
    out.append(f'<text x="{px0 + pw - 6}" y="{py0 + 32}" text-anchor="end" font-family="sans-serif" font-size="11" fill="{AQUA}">{SEEDS} random binary trees, same sources</text>')
    y = 380
    out.append(f'<text x="240" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="{INK}">bifurcation ratio N_k / N_(k+1): Collatz vs random (mean, z)</text>')
    y += 20
    for k in range(1, 6):
        xs = per_k[k]
        m, sd = statistics.mean(xs), statistics.stdev(xs)
        z = (rb[k - 1] - m) / sd
        out.append(f'<text x="240" y="{y}" text-anchor="middle" font-family="monospace" font-size="11.5" fill="{INK if abs(z) >= 3 else DIM}">'
                   f'k={k}:  {rb[k - 1]:.3f}  vs  {m:.3f} ± {sd:.3f}   z = {z:+.1f}</text>')
        y += 17
    notes = [
        "River-like: every ratio is in real rivers' range of about 3 to 5.",
        "Not random: k=1 is above 4, then orders thin out more slowly (ratios",
        "below 4), so high orders are relatively over-represented.",
        "The sources exist only because the starts stop at N:",
        "the full inverse Collatz tree has none (every n has 2n above it).",
    ]
    y += 8
    for t in notes:
        out.append(f'<text x="240" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="11" fill="{DIM}">{t}</text>')
        y += 16
    out.append(f'<text x="240" y="592" text-anchor="middle" font-family="sans-serif" font-size="9" fill="{DIM}">ideas after Confluence at 1 · Confluence</text>')
    out.append("</svg>")
    p = pathlib.Path(__file__).with_name("strahler_card.svg")
    p.write_text("".join(out), encoding="utf-8")
    print(p.name, p.stat().st_size, "bytes; R_b", rb[:5])


if __name__ == "__main__":
    main()
