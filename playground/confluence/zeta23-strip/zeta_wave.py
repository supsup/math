"""The lead picture for the zeta card: the zeta function along the critical line, drawn as a real wave.

On the line s = 1/2 + it, zeta is a real wave times a unit rotation: Hardy's Z(t) = exp(i theta(t)) zeta(1/2 + it)
is real, and |Z(t)| = |zeta(1/2 + it)|. So each zero on the line is a point where the wave Z crosses zero. A SINGLE
zero is a crossing with a slope; a REPEATED zero would be a point where the wave is flat at zero.

Z is computed here by the Riemann-Siegel formula (main sum plus the first correction term), with theta(t) from
its asymptotic series. Those formulas were written from memory, so the script CHECKS them against an independent
fact before drawing anything (a check that fails if the formulas are wrong):

  COUNT CHECK. The number of zeros with 0 < Im s <= T is theta(T)/pi + 1 + S(T), where S(T) is small. So at heights
  T chosen between crossings, the number of sign changes of Z found in (0, T] must equal theta(T)/pi + 1 to within
  less than 1. A wrong theta, a wrong main sum or a wrong sign convention would put the two counts apart.
  Equality also says every zero up to T was found as a CROSSING, i.e. is on the line with odd multiplicity: a
  numerical observation for this small range, NOT a proof of anything.

  CONTROL. Dropping the correction term must still pass the count check (it is a small term), but replacing
  theta by a wrong function (theta + t/10) must FAIL it; the script asserts that it does.

Pure Python. Writes zeta_wave.svg (self-contained) and prints every number. Run: python3 zeta_wave.py
"""
import math

T_MAX = 60.0


def theta(t):
    """Riemann-Siegel theta, asymptotic series (good for t >= 10)."""
    return t / 2 * math.log(t / (2 * math.pi)) - t / 2 - math.pi / 8 + 1 / (48 * t) + 7 / (5760 * t ** 3)


def Z(t, th=theta, correction=True):
    a = math.sqrt(t / (2 * math.pi))
    N = int(a)
    p = a - N
    th_t = th(t)
    s = 2 * sum(math.cos(th_t - t * math.log(n)) / math.sqrt(n) for n in range(1, N + 1))
    if correction:
        c0 = math.cos(2 * math.pi * (p * p - p - 1 / 16)) / math.cos(2 * math.pi * p)
        s += (-1) ** (N - 1) * (t / (2 * math.pi)) ** -0.25 * c0
    return s


def crossings(th=theta, correction=True, lo=10.0, hi=T_MAX, step=0.01):
    """Sign changes of Z on [lo, hi], each refined by bisection. (No zero lies below 10: the count check covers it.)"""
    out, t, z = [], lo, Z(lo, th, correction)
    while t < hi:
        t2 = min(t + step, hi)
        z2 = Z(t2, th, correction)
        if z == 0 or z * z2 < 0:
            a, b, za = t, t2, z
            for _ in range(50):
                m = (a + b) / 2
                zm = Z(m, th, correction)
                if za * zm <= 0:
                    b = m
                else:
                    a, za = m, zm
            out.append((a + b) / 2)
        t, z = t2, z2
    return out


def count_check(zs, th=theta):
    """At heights halfway between consecutive crossings (and at T_MAX), compare the counts."""
    heights = [(zs[i] + zs[i + 1]) / 2 for i in range(len(zs) - 1)] + [T_MAX]
    worst = 0.0
    for k, T in enumerate(heights, start=1):
        predicted = th(T) / math.pi + 1
        worst = max(worst, abs(k - predicted))
    return worst


def main():
    zs = crossings()
    worst = count_check(zs)
    print(f"crossings of Z on (10, {T_MAX:g}]: {len(zs)}; first three at t = " + ", ".join(f"{z:.4f}" for z in zs[:3]))
    print(f"count check: largest |crossings found - (theta(T)/pi + 1)| over {len(zs)} heights = {worst:.3f}")
    assert worst < 1, "COUNT CHECK FAILED: the Z formulas disagree with the zero-counting formula"
    worst_plain = count_check(crossings(correction=False))
    assert worst_plain < 1, "count check failed without the correction term"
    wrong = lambda t: theta(t) + t / 10
    worst_wrong = count_check(crossings(th=wrong), th=theta)
    print(f"controls: without the correction term {worst_plain:.3f} (passes); with a wrong theta {worst_wrong:.3f} (must fail)")
    assert worst_wrong >= 1, "CONTROL FAILED: a wrong theta still passed, so the count check cannot fail"
    slopes = [abs(Z(z + 1e-4) - Z(z - 1e-4)) / 2e-4 for z in zs]
    print(f"slope of Z at its crossings: smallest {min(slopes):.3f} (none flat), largest {max(slopes):.3f}")
    write_svg(zs, slopes)
    print("wrote zeta_wave.svg")
    write_svg_narrow(zs)
    print("wrote zeta_wave_narrow.svg")


def write_svg(zs, slopes):
    W, H = 960, 540
    x0, x1, ymid, yscale = 60, 920, 210, 34
    def X(t):
        return x0 + (x1 - x0) * (t - 10) / (T_MAX - 10)
    gold, ink, mute, teal = "#b8860b", "#1f2328", "#57606a", "#0f766e"
    pts, t = [], 10.0
    while t <= T_MAX + 1e-9:
        pts.append(f"{X(t):.1f},{ymid - yscale * max(-4.5, min(4.5, Z(t))):.1f}")
        t += 0.05
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Helvetica, Arial, sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="{x0}" y="38" font-size="19" fill="{ink}" font-weight="bold">The zeta function along the line, drawn as a wave</text>',
         f'<text x="{x0}" y="62" font-size="14" fill="{mute}">Every point where the wave crosses zero is a zero of zeta. Each of these {len(zs)} crossings has a clearly nonzero</text>',
         f'<text x="{x0}" y="80" font-size="14" fill="{mute}">estimated slope, so each zero is single (a numerical picture). A repeated zero would sit flat at zero.</text>',
         f'<line x1="{x0}" y1="{ymid}" x2="{x1}" y2="{ymid}" stroke="{ink}" stroke-width="1"/>',
         f'<polyline points="{" ".join(pts)}" fill="none" stroke="{teal}" stroke-width="2"/>']
    for z in zs:
        o.append(f'<circle cx="{X(z):.1f}" cy="{ymid}" r="5" fill="{gold}" stroke="#ffffff" stroke-width="1.5"/>')
    for tick in range(10, int(T_MAX) + 1, 10):
        o.append(f'<text x="{X(tick):.1f}" y="{ymid + 175}" font-size="13" fill="{ink}" text-anchor="middle">{tick}</text>')
    o.append(f'<text x="{(x0 + x1) / 2:.1f}" y="{ymid + 198}" font-size="13" fill="{mute}" text-anchor="middle">height along the line (t); gold dots: the zeros, found by computing the wave</text>')
    # two glyphs that teach the difference without words: a crossing with a slope, and a flat touch
    gy, gw = 470, 70
    o.append(f'<line x1="{x0}" y1="{gy}" x2="{x0 + gw}" y2="{gy}" stroke="{ink}" stroke-width="1"/>')
    o.append(f'<line x1="{x0 + 8}" y1="{gy + 24}" x2="{x0 + gw - 8}" y2="{gy - 24}" stroke="{teal}" stroke-width="2.5"/>')
    o.append(f'<circle cx="{x0 + gw / 2}" cy="{gy}" r="5" fill="{gold}" stroke="#ffffff" stroke-width="1.5"/>')
    o.append(f'<text x="{x0 + gw + 14}" y="{gy - 4}" font-size="14" fill="{ink}" font-weight="bold">single zero</text>')
    o.append(f'<text x="{x0 + gw + 14}" y="{gy + 14}" font-size="13" fill="{mute}">the wave cuts through with a slope</text>')
    gx = 520
    o.append(f'<line x1="{gx}" y1="{gy}" x2="{gx + gw}" y2="{gy}" stroke="{ink}" stroke-width="1"/>')
    o.append(f'<path d="M {gx + 6} {gy - 26} Q {gx + gw / 2} {gy + 26} {gx + gw - 6} {gy - 26}" fill="none" stroke="{teal}" stroke-width="2.5" stroke-dasharray="5 4"/>')
    o.append(f'<circle cx="{gx + gw / 2}" cy="{gy}" r="5" fill="#ffffff" stroke="{gold}" stroke-width="2"/>')
    o.append(f'<text x="{gx + gw + 14}" y="{gy - 4}" font-size="14" fill="{ink}" font-weight="bold">repeated zero</text>')
    o.append(f'<text x="{gx + gw + 14}" y="{gy + 14}" font-size="13" fill="{mute}">the wave would sit flat (none seen here)</text>')
    o.append(f'<text x="{x0}" y="{H - 10}" font-size="12" fill="{mute}">Computed with the Riemann-Siegel formula and checked against the zero-counting formula (zeta_wave.py). A picture of {len(zs)} zeros, not a proof.</text>')
    o.append('</svg>')
    with open("zeta_wave.svg", "w", encoding="utf-8") as fh:
        fh.write("\n".join(o) + "\n")


def write_svg_narrow(zs):
    """The same picture for a phone (shown under 600 px): taller, larger type, the glyphs stacked."""
    W, H = 420, 660
    x0, x1, ymid, yscale = 22, 400, 318, 30
    def X(t):
        return x0 + (x1 - x0) * (t - 10) / (T_MAX - 10)
    gold, ink, mute, teal = "#b8860b", "#1f2328", "#57606a", "#0f766e"
    pts, t = [], 10.0
    while t <= T_MAX + 1e-9:
        pts.append(f"{X(t):.1f},{ymid - yscale * max(-4.5, min(4.5, Z(t))):.1f}")
        t += 0.05
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Helvetica, Arial, sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="{x0}" y="34" font-size="21" fill="{ink}" font-weight="bold">The zeta function along</text>',
         f'<text x="{x0}" y="60" font-size="21" fill="{ink}" font-weight="bold">the line, drawn as a wave</text>']
    for i, line in enumerate(["Every crossing is a zero of zeta. Each of",
                              f"these {len(zs)} crossings has a clearly nonzero",
                              "estimated slope, so each zero is single",
                              "(a numerical picture)."]):
        o.append(f'<text x="{x0}" y="{92 + 21 * i}" font-size="16" fill="{mute}">{line}</text>')
    o.append(f'<line x1="{x0}" y1="{ymid}" x2="{x1}" y2="{ymid}" stroke="{ink}" stroke-width="1"/>')
    o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{teal}" stroke-width="2.5"/>')
    for z in zs:
        o.append(f'<circle cx="{X(z):.1f}" cy="{ymid}" r="5.5" fill="{gold}" stroke="#ffffff" stroke-width="1.5"/>')
    for tick in range(10, int(T_MAX) + 1, 10):
        o.append(f'<text x="{X(tick):.1f}" y="{ymid + 160}" font-size="15" fill="{ink}" text-anchor="middle">{tick}</text>')
    o.append(f'<text x="{(x0 + x1) / 2:.1f}" y="{ymid + 184}" font-size="15" fill="{mute}" text-anchor="middle">height along the line</text>')
    gy, gw = 550, 64
    o.append(f'<line x1="{x0}" y1="{gy}" x2="{x0 + gw}" y2="{gy}" stroke="{ink}" stroke-width="1"/>')
    o.append(f'<line x1="{x0 + 8}" y1="{gy + 22}" x2="{x0 + gw - 8}" y2="{gy - 22}" stroke="{teal}" stroke-width="3"/>')
    o.append(f'<circle cx="{x0 + gw / 2}" cy="{gy}" r="5.5" fill="{gold}" stroke="#ffffff" stroke-width="1.5"/>')
    o.append(f'<text x="{x0 + gw + 14}" y="{gy + 6}" font-size="17" fill="{ink}" font-weight="bold">single zero: cuts through</text>')
    gy2 = gy + 60
    o.append(f'<line x1="{x0}" y1="{gy2}" x2="{x0 + gw}" y2="{gy2}" stroke="{ink}" stroke-width="1"/>')
    o.append(f'<path d="M {x0 + 6} {gy2 - 24} Q {x0 + gw / 2} {gy2 + 24} {x0 + gw - 6} {gy2 - 24}" fill="none" stroke="{teal}" stroke-width="3" stroke-dasharray="5 4"/>')
    o.append(f'<circle cx="{x0 + gw / 2}" cy="{gy2}" r="5.5" fill="#ffffff" stroke="{gold}" stroke-width="2"/>')
    o.append(f'<text x="{x0 + gw + 14}" y="{gy2 + 6}" font-size="17" fill="{ink}" font-weight="bold">repeated zero: sits flat</text>')
    o.append('</svg>')
    with open("zeta_wave_narrow.svg", "w", encoding="utf-8") as fh:
        fh.write("\n".join(o) + "\n")


if __name__ == "__main__":
    main()
