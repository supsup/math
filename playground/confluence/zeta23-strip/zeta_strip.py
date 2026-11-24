"""Zeta card (Marginalia): every zero is on the line; how many are simple?

Three sources, each read at a pinned revision (the script refuses any other revision):
  * anthropics/formal-math @ 11b6c7e (zeta23/Challenge.lean): Alpoge-Furman, "More than two thirds
    of the zeros of the Riemann zeta function are simple and on the critical line" (arXiv:2608.13637),
    formalized in Lean by Claude; the trusted statement was read against the paper by a paper author.
  * the Riemann Hypothesis release (Alpoge with Claude, announced 2026-11-20), mirror
    1337isnot1337/riemann-hypothesis-solved @ 6193bb5 (extracted/lean/src/Main.lean, Statements.lean):
    Mathlib's own RiemannHypothesis, and GRH for every Dirichlet L-function. RH certified by the Lean FRO
    and the Mathlib Initiative (2026-11-21); kernel and statement checks in Sutherland's record (11-24).
  * openai/math @ f5702854 (family 003, CLAIMED in October): no zeros of zeta or of any Dirichlet
    L-function with real part greater than 7/8. Shown historically: the release above implies it.

What the script checks (each check can fail):
  1. Source pins: all three checkouts are at the named commits and the files read are byte-identical
     to those commits.
  2. The quoted statements are present verbatim: zeta23's Theorem B and D and its two counts; the
     release's `theorem riemannHypothesis : RiemannHypothesis` (Mathlib's own definition: the statement
     file must not redefine it) and its Dirichlet non-vanishing for 1/2 < Re s, for every character;
     003's two 7/8 statements, a full half-plane for every character.
  3. The constants: c1* = sqrt2 tan t / (1 + t tan t) at t = 1/sqrt2, equal to the two alternative forms
     the file's comments give; the proportions 2 - 1/c1* = 0.67250... and (3 - 1/c1*)/2 = 0.83625....
     CONTROL: the same formula at t = 1 must NOT give 0.67250 (asserted to differ).
  4. The reading (ours, elementary, not formalized): with every nontrivial zero on the line, N - N0s
     (zeta23's counts) is exactly the multiplicity mass of the MULTIPLE zeros, so eventually at most
     1/c1* - 1 = 0.32750 of the count; the simple-zeros conjecture says 0. And 003's 7/8 is implied
     (7/8 > 1/2), except its separate Hecke result over Q(sqrt -3), which the release does not state.

Writes zeta_strip.svg (self-contained: no fonts, scripts or links loaded) and prints every number.
Run: python3 zeta_strip.py /path/to/formal-math /path/to/openai-math /path/to/riemann-hypothesis-solved
"""
import math
import subprocess
import sys

FORMAL_REV = "11b6c7e3c9"   # anthropics/formal-math, read 2026-11-24
OPENAI_REV = "f570285404"   # openai/math, read 2026-11-24
RH_REV = "6193bb5e"         # 1337isnot1337/riemann-hypothesis-solved, the visualizer's and Sutherland's pin


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout.strip()


def pinned_file(repo, rev_prefix, path):
    head = git(repo, "rev-parse", "HEAD")
    assert head.startswith(rev_prefix), f"{repo} is at {head[:10]}, not the pinned {rev_prefix}"
    assert git(repo, "rev-parse", f"{head}:{path}") == git(repo, "hash-object", path), f"{path} differs from the pin"
    with open(f"{repo}/{path}", encoding="utf-8") as fh:
        return fh.read(), head


def main(formal, openai, rh):
    zeta, zrev = pinned_file(formal, FORMAL_REV, "zeta23/Challenge.lean")
    qrh, orev = pinned_file(openai, OPENAI_REV, "lean/ComparatorChallenges/QuasiRiemannHypothesis.lean")
    dir78, _ = pinned_file(openai, OPENAI_REV, "lean/ComparatorChallenges/DirichletSevenEighths.lean")
    rhmain, rrev = pinned_file(rh, RH_REV, "extracted/lean/src/Main.lean")
    rhstat, _ = pinned_file(rh, RH_REV, "extracted/lean/src/Statements.lean")
    print(f"sources: formal-math {zrev[:10]}, openai/math {orev[:10]}, RH release mirror {rrev[:10]}")

    # 2. the quoted statements, verbatim
    for s in ("theorem two_thirds_simple_on_critical_line_cumulative :",
              "theorem montgomery_taylor_simple_on_critical_line_mult_cumulative :",
              "def N0simple (T₁ T₂ : ℝ) : ℕ := (zerosIn T₁ T₂ ∩ {ρ | ρ.re = 1 / 2} ∩ {ρ | zeroMult ρ = 1}).ncard",
              "def Ncount (T₁ T₂ : ℝ) : ℕ := ∑ᶠ ρ ∈ zerosIn T₁ T₂, zeroMult ρ"):
        assert s in zeta, f"zeta23 statement missing: {s}"
    assert "theorem riemannHypothesis : RiemannHypothesis" in rhmain, "release no longer proves RiemannHypothesis"
    assert "RiemannHypothesis" not in rhstat.replace("RiemannZetaZerosOnLine", ""), "Statements.lean redefines RiemannHypothesis"
    assert "1 / 2 < s.re → (χ ≠ 1 ∨ s ≠ 1) → DirichletCharacter.LFunction χ s ≠ 0" in rhstat, "release's Dirichlet statement changed"
    assert "(hs : (7 / 8 : ℝ) < s.re) : riemannZeta s ≠ 0" in qrh and "(hs : (7 / 8 : ℝ) < s.re) (hpole" in dir78, "003 changed"
    assert 7 / 8 > 1 / 2, "003's half-plane is not inside the release's"
    print("statements: zeta23 B and D; the release proves Mathlib's RiemannHypothesis and Dirichlet non-vanishing "
          "for Re s > 1/2 (every character), which implies 003's 7/8 for zeta and every Dirichlet L")

    # 3. the constants
    t = 1 / math.sqrt(2)
    c1 = math.sqrt(2) * math.tan(t) / (1 + t * math.tan(t))
    alt = 2 * math.tan(t) / (math.sqrt(2) + math.tan(t))
    inv_mt = 0.5 + 2 ** -0.5 / math.tan(2 ** -0.5)
    assert abs(c1 - alt) < 1e-12 and abs(1 / c1 - inv_mt) < 1e-12
    simple, distinct = 2 - 1 / c1, (3 - 1 / c1) / 2
    assert f"{c1:.7f}" == "0.7532961" and f"{simple:.5f}" == "0.67250" and f"{distinct:.5f}" == "0.83625"
    wrong = 2 - (1 + math.tan(1)) / (math.sqrt(2) * math.tan(1))   # control: t = 1, not 1/sqrt2
    assert f"{wrong:.5f}" != "0.67250", "control failed to differ: the check cannot fail"
    print(f"c1* = {c1:.10f}; simple >= {simple:.8f}; distinct >= {distinct:.8f}; control t=1 gives {wrong:.5f}")

    # 4. the reading
    multiple = 1 / c1 - 1
    assert abs(multiple - (1 - simple)) < 1e-12 and multiple < 1 / 3
    print(f"with every zero on the line: multiple zeros carry at most {multiple:.8f} of the count, eventually "
          "(the simple-zeros conjecture: 0)")
    write_svg(simple, distinct, multiple, zrev[:7], orev[:7], rrev[:7])
    print("wrote zeta_strip.svg")


def write_svg(simple, distinct, multiple, zrev, orev, rrev):
    """The simple version, for a first-time reader: one idea per panel, plain words, honest rounding."""
    lo = math.floor(simple * 100)       # a LOWER bound rounds down: 67.25% -> at least 67%
    hi = math.ceil(multiple * 100)      # an UPPER bound rounds up:  32.75% -> at most 33%
    assert lo / 100 <= simple and hi / 100 >= multiple and lo + hi == 100
    W, H = 960, 520
    x0, x1, ytop, ybot = 60, 440, 80, 420
    def X(re):
        return x0 + (x1 - x0) * re
    gold, ink, grey, mute = "#b8860b", "#1f2328", "#8c959f", "#57606a"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Helvetica, Arial, sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<defs><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         f'<line x1="0" y1="0" x2="0" y2="8" stroke="{grey}" stroke-width="2"/></pattern></defs>']
    # left: where the zeros are
    o.append(f'<text x="{x0}" y="40" font-size="18" fill="{ink}" font-weight="bold">1. Where the zeros are</text>')
    for a, b in ((0, 0.5 - 0.004), (0.5 + 0.004, 1)):
        o.append(f'<rect x="{X(a):.1f}" y="{ytop}" width="{X(b) - X(a):.1f}" height="{ybot - ytop}" fill="url(#hatch)" opacity="0.45"/>')
    o.append(f'<rect x="{X(0):.1f}" y="{ytop}" width="{X(1) - X(0):.1f}" height="{ybot - ytop}" fill="none" stroke="{ink}" stroke-width="1"/>')
    o.append(f'<line x1="{X(.5):.1f}" y1="{ytop}" x2="{X(.5):.1f}" y2="{ybot}" stroke="{gold}" stroke-width="6"/>')
    o.append(f'<text x="{X(.5):.1f}" y="{ytop - 10}" font-size="14" fill="{gold}" text-anchor="middle" font-weight="bold">every zero is on this line</text>')
    o.append(f'<text x="{X(.23):.1f}" y="{(ytop + ybot) / 2:.1f}" font-size="14" fill="{mute}" text-anchor="middle">none here</text>')
    o.append(f'<text x="{X(.77):.1f}" y="{(ytop + ybot) / 2:.1f}" font-size="14" fill="{mute}" text-anchor="middle">none here</text>')
    for re, lab in ((0, "0"), (.5, "1/2"), (1, "1")):
        o.append(f'<text x="{X(re):.1f}" y="{ybot + 22}" font-size="14" fill="{ink}" text-anchor="middle">{lab}</text>')
    o.append(f'<text x="{x0}" y="{ybot + 52}" font-size="13" fill="{mute}">Proved in 2026 and checked by computer (the Riemann Hypothesis).</text>')
    # right: how many are single
    bx, bw, by = 520, 380, 150
    o.append(f'<text x="{bx}" y="40" font-size="18" fill="{ink}" font-weight="bold">2. How many are single?</text>')
    o.append(f'<text x="{bx}" y="{by - 30}" font-size="14" fill="{ink}">Out of every 100 zeros (a repeated one counts twice):</text>')
    o.append(f'<rect x="{bx}" y="{by}" width="{bw * simple:.1f}" height="40" fill="{gold}"/>')
    o.append(f'<rect x="{bx + bw * simple:.1f}" y="{by}" width="{bw * multiple:.1f}" height="40" fill="#ffffff" stroke="{ink}" stroke-dasharray="4 3"/>')
    o.append(f'<text x="{bx + 10}" y="{by + 26}" font-size="15" fill="#ffffff" font-weight="bold">at least {lo}</text>')
    o.append(f'<text x="{bx}" y="{by + 70}" font-size="15" fill="{gold}" font-weight="bold">at least {lo} are single</text>')
    o.append(f'<text x="{bx}" y="{by + 92}" font-size="13" fill="{ink}">(the graph cuts through zero with a slope, like x)</text>')
    o.append(f'<text x="{bx}" y="{by + 128}" font-size="15" fill="{ink}" font-weight="bold">at most {hi} could be repeated</text>')
    o.append(f'<text x="{bx}" y="{by + 150}" font-size="13" fill="{ink}">(the graph would be flat at zero, like x squared)</text>')
    o.append(f'<text x="{bx}" y="{by + 188}" font-size="13" fill="{mute}">Mathematicians expect none to be repeated, but</text>')
    o.append(f'<text x="{bx}" y="{by + 206}" font-size="13" fill="{mute}">nobody has proved that. This result proves at least {lo}.</text>')
    o.append(f'<text x="{bx}" y="{by + 250}" font-size="12" fill="{mute}">Sources: Alpoge-Furman (arXiv:2608.13637; Lean, formal-math {zrev});</text>')
    o.append(f'<text x="{bx}" y="{by + 266}" font-size="12" fill="{mute}">Riemann Hypothesis: Alpoge with Claude, 2026-11-20 (mirror {rrev}).</text>')
    o.append('</svg>')
    with open("zeta_strip.svg", "w", encoding="utf-8") as fh:
        fh.write("\n".join(o) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("usage: python3 zeta_strip.py /path/to/formal-math /path/to/openai-math /path/to/riemann-hypothesis-solved")
    main(*sys.argv[1:])
