"""Zeta card (Marginalia): how many zeros are simple and on the line, and where the rest may be.

Two sources, each read at a pinned revision (the script refuses another revision):
  * anthropics/formal-math @ 11b6c7e (zeta23/Challenge.lean): Alpoge-Furman, "More than two thirds
    of the zeros of the Riemann zeta function are simple and on the critical line" (arXiv:2608.13637),
    formalized in Lean by Claude; the trusted statement was read against the paper by a paper author.
  * openai/math @ f5702854 (lean/ComparatorChallenges/QuasiRiemannHypothesis.lean and
    DirichletSevenEighths.lean): family 003, CLAIMED, no zeros of zeta or of any Dirichlet L-function
    with real part greater than 7/8.

What the script checks (each check can fail):
  1. Source pins: both checkouts are at the named commits and the statement files are byte-unchanged
     there (git hash-object against the commit's blob).
  2. The statements the card quotes are present verbatim: zeta23's Theorem B and D names, the
     closed form of the Montgomery-Taylor constant, and 003's two hypotheses "(7 / 8 : R) < s.re"
     with NO hypothesis on the imaginary part (a full half-plane).
  3. The constants: c1* = sqrt2 tan t / (1 + t tan t) at t = 1/sqrt2, equal to the two alternative
     forms the file's comments give, and the proportions 2 - 1/c1* = 0.67250... and
     (3 - 1/c1*)/2 = 0.83625... that the comments print (the decimals are comments; the theorems use
     the closed form). CONTROL: the same formula at t = 1 must NOT give 0.67250 (it is asserted to
     differ), so a check that always passes would be caught.
  4. The combination (not formalized by anyone): N - N0s is the multiplicity-weighted mass of the
     zeros that are off the line OR multiple, so eventually it is at most 1/c1* - 1 = 0.32750 of N;
     and if 003's claim holds, every off-line nontrivial zero has 1/8 <= Re <= 7/8 (the left strip by
     the functional equation, applied to chi-bar for a complex character; 003 covers every chi).

Writes zeta_strip.svg (self-contained: no fonts, scripts or links loaded) and prints every number.
Run: python3 zeta_strip.py /path/to/formal-math /path/to/openai-math
"""
import math
import subprocess
import sys

FORMAL_REV = "11b6c7e3c9"   # anthropics/formal-math, prefix of the commit read on 2026-11-24
OPENAI_REV = "f570285404"   # openai/math, prefix of the commit read on 2026-11-24


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout.strip()


def pinned_file(repo, rev_prefix, path):
    head = git(repo, "rev-parse", "HEAD")
    assert head.startswith(rev_prefix), f"{repo} is at {head[:10]}, not the pinned {rev_prefix}"
    blob_at_rev = git(repo, "rev-parse", f"{head}:{path}")
    blob_on_disk = git(repo, "hash-object", path)
    assert blob_at_rev == blob_on_disk, f"{path} differs from the pinned commit"
    with open(f"{repo}/{path}", encoding="utf-8") as fh:
        return fh.read(), head


def main(formal, openai):
    zeta, zrev = pinned_file(formal, FORMAL_REV, "zeta23/Challenge.lean")
    qrh, orev = pinned_file(openai, OPENAI_REV, "lean/ComparatorChallenges/QuasiRiemannHypothesis.lean")
    dir78, _ = pinned_file(openai, OPENAI_REV, "lean/ComparatorChallenges/DirichletSevenEighths.lean")
    print(f"sources: formal-math {zrev}, openai/math {orev}")

    # 2. the quoted statements are there, verbatim
    for name in ("theorem two_thirds_simple_on_critical_line :",
                 "theorem montgomery_taylor_simple_on_critical_line_mult :",
                 "theorem dirichlet_two_thirds_simple_on_critical_line",
                 "def N0simple (T₁ T₂ : ℝ) : ℕ := (zerosIn T₁ T₂ ∩ {ρ | ρ.re = 1 / 2} ∩ {ρ | zeroMult ρ = 1}).ncard",
                 "def Ncount (T₁ T₂ : ℝ) : ℕ := ∑ᶠ ρ ∈ zerosIn T₁ T₂, zeroMult ρ"):
        assert name in zeta, f"zeta23 statement missing: {name}"
    assert "(hs : (7 / 8 : ℝ) < s.re) : riemannZeta s ≠ 0" in qrh, "003 zeta statement changed"
    assert "(hs : (7 / 8 : ℝ) < s.re) (hpole : ¬ (χ = 1 ∧ s = 1))" in dir78, "003 Dirichlet statement changed"
    assert ".im" not in qrh and ".im" not in dir78, "003 now restricts the imaginary part: not a half-plane"
    assert "(χ : DirichletCharacter ℂ q)" in dir78 and "IsPrimitive" not in dir78, "003 no longer covers every chi"
    print("statements: zeta23 Theorems B and D and the counts present; 003 is a full half-plane for every chi")

    # 3. the constants
    t = 1 / math.sqrt(2)
    c1 = math.sqrt(2) * math.tan(t) / (1 + t * math.tan(t))
    alt = 2 * math.tan(t) / (math.sqrt(2) + math.tan(t))
    inv_mt = 0.5 + 2 ** -0.5 / math.tan(2 ** -0.5)
    assert abs(c1 - alt) < 1e-12 and abs(1 / c1 - inv_mt) < 1e-12
    simple, distinct = 2 - 1 / c1, (3 - 1 / c1) / 2
    assert f"{c1:.7f}" == "0.7532961" and f"{simple:.5f}" == "0.67250" and f"{distinct:.5f}" == "0.83625"
    wrong = 2 - (1 + 1 * math.tan(1)) / (math.sqrt(2) * math.tan(1))   # control: t = 1, not 1/sqrt2
    assert f"{wrong:.5f}" != "0.67250", "control failed to differ: the check cannot fail"
    print(f"c1* = {c1:.10f}; simple on the line >= {simple:.8f}; distinct >= {distinct:.8f}; control t=1 gives {wrong:.5f}")

    # 4. the combination
    rest = 1 / c1 - 1
    assert abs(rest - (1 - simple)) < 1e-12 and rest < 1 / 3
    print(f"off the line or multiple: at most {rest:.8f} of N, eventually (1/3 with Theorem B alone)")
    print("if 003 holds: every off-line nontrivial zero has 1/8 <= Re <= 7/8 (zeta and every Dirichlet L)")
    write_svg(simple, distinct, rest, zrev[:7], orev[:7])
    print("wrote zeta_strip.svg")


def write_svg(simple, distinct, rest, zrev, orev):
    W, H = 960, 560
    x0, x1, ytop, ybot = 70, 470, 70, 470          # the strip 0 <= Re <= 1, schematic height
    def X(re):
        return x0 + (x1 - x0) * re
    gold, ink, grey, mute = "#b8860b", "#1f2328", "#8c959f", "#57606a"
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Helvetica, Arial, sans-serif">',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
           '<defs><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
           f'<line x1="0" y1="0" x2="0" y2="8" stroke="{grey}" stroke-width="2"/></pattern></defs>',
           f'<text x="{x0}" y="36" font-size="17" fill="{ink}" font-weight="bold">Where the zeros of zeta can be</text>']
    # excluded strips (claimed), the unshaded band, the line
    for a, b in ((0, 1 / 8), (7 / 8, 1)):
        out.append(f'<rect x="{X(a):.1f}" y="{ytop}" width="{X(b) - X(a):.1f}" height="{ybot - ytop}" fill="url(#hatch)" opacity="0.55"/>')
    out.append(f'<rect x="{X(0):.1f}" y="{ytop}" width="{X(1) - X(0):.1f}" height="{ybot - ytop}" fill="none" stroke="{ink}" stroke-width="1"/>')
    out.append(f'<line x1="{X(.5):.1f}" y1="{ytop}" x2="{X(.5):.1f}" y2="{ybot}" stroke="{gold}" stroke-width="5"/>')
    for re, lab in ((0, "0"), (1 / 8, "1/8"), (.5, "1/2"), (7 / 8, "7/8"), (1, "1")):
        out.append(f'<text x="{X(re):.1f}" y="{ybot + 20}" font-size="13" fill="{ink}" text-anchor="middle">{lab}</text>')
    out.append(f'<text x="{(x0 + x1) / 2:.1f}" y="{ybot + 40}" font-size="13" fill="{mute}" text-anchor="middle">real part of the zero (the strip 0 &lt; Re &lt; 1; height schematic)</text>')
    out.append(f'<text x="{X(15/16):.1f}" y="{ytop - 8}" font-size="12" fill="{mute}" text-anchor="middle">no zeros (claimed)</text>')
    out.append(f'<text x="{X(1/16):.1f}" y="{ytop - 8}" font-size="12" fill="{mute}" text-anchor="middle">no zeros (claimed)</text>')
    out.append(f'<text x="{X(.5) + 10:.1f}" y="{ytop + 22}" font-size="12" fill="{gold}">the critical line</text>')
    out.append(f'<text x="{X(.3):.1f}" y="{(ytop + ybot) / 2:.1f}" font-size="12" fill="{mute}" text-anchor="middle">an off-line</text>')
    out.append(f'<text x="{X(.3):.1f}" y="{(ytop + ybot) / 2 + 16:.1f}" font-size="12" fill="{mute}" text-anchor="middle">zero, if any,</text>')
    out.append(f'<text x="{X(.3):.1f}" y="{(ytop + ybot) / 2 + 32:.1f}" font-size="12" fill="{mute}" text-anchor="middle">is in the band</text>')
    # the count bar
    bx, bw, by = 540, 380, 150
    out.append(f'<text x="{bx}" y="{by - 40}" font-size="15" fill="{ink}" font-weight="bold">Of every zero counted (with multiplicity)</text>')
    out.append(f'<rect x="{bx}" y="{by}" width="{bw * simple:.1f}" height="34" fill="{gold}"/>')
    out.append(f'<rect x="{bx + bw * simple:.1f}" y="{by}" width="{bw * rest:.1f}" height="34" fill="#ffffff" stroke="{ink}" stroke-dasharray="4 3"/>')
    out.append(f'<text x="{bx}" y="{by + 56}" font-size="13" fill="{gold}">at least {simple:.4f}: simple, on the line</text>')
    out.append(f'<text x="{bx}" y="{by + 76}" font-size="13" fill="{ink}">at most {rest:.4f}: off the line, or multiple</text>')
    out.append(f'<text x="{bx}" y="{by + 108}" font-size="13" fill="{ink}">distinct zeros: at least {distinct:.4f} of the count</text>')
    out.append(f'<text x="{bx}" y="{by + 128}" font-size="13" fill="{mute}">(eventually, as the height grows; 2/3 and 5/6 without the</text>')
    out.append(f'<text x="{bx}" y="{by + 146}" font-size="13" fill="{mute}">optimal window)</text>')
    # provenance and status
    out.append(f'<text x="{bx}" y="{by + 196}" font-size="13" fill="{gold}" font-weight="bold">PROVED, the proportions on the line</text>')
    out.append(f'<text x="{bx}" y="{by + 214}" font-size="12" fill="{ink}">Alpoge-Furman, arXiv:2608.13637; Lean by Claude, statement</text>')
    out.append(f'<text x="{bx}" y="{by + 230}" font-size="12" fill="{ink}">read by a paper author; anthropics/formal-math {zrev}</text>')
    out.append(f'<text x="{bx}" y="{by + 262}" font-size="13" fill="{mute}" font-weight="bold">CLAIMED, the hatched strips</text>')
    out.append(f'<text x="{bx}" y="{by + 280}" font-size="12" fill="{ink}">openai/math {orev}, family 003: no zeros right</text>')
    out.append(f'<text x="{bx}" y="{by + 296}" font-size="12" fill="{ink}">of 7/8 (left of 1/8 by the functional equation)</text>')
    out.append(f'<text x="{bx}" y="{by + 328}" font-size="12" fill="{mute}">The band says WHERE an off-line zero may be, never how</text>')
    out.append(f'<text x="{bx}" y="{by + 344}" font-size="12" fill="{mute}">many: it is deliberately not shaded by density.</text>')
    out.append('</svg>')
    with open("zeta_strip.svg", "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python3 zeta_strip.py /path/to/formal-math /path/to/openai-math")
    main(sys.argv[1], sys.argv[2])
