# Card draft (Confluence): Every nontrivial zero is on the line. How many are single?

For Fixpoint to edit into the showcase. Plain reading first, then the details (Charles's rule, 2026-11-24:
break the card down and simplify). Sources from both collections, each cited.

## The pictures (lead with the first)

1. `zeta_wave.svg`, the lead: the zeta function along the line drawn as a real wave (Hardy's Z, computed).
   Every gold dot is a zero; each of the 13 crossings up to height 60 has a clearly nonzero estimated slope, so
   each of those zeros is single. A numerical picture: a sign change alone could also be a triple zero, and the
   slope is what says single (Lattice, 34476).
   Two small glyphs under it show 'cuts through' against 'would sit flat'. Readable without the text.
2. `zeta_strip.svg`: the two plain panels, where the zeros are, and at least 67 in 100 single.
3. Interactive: `crew_visuals/zeta_wave.html` in supsup/new_math_review (Confluence's branch
   confluence/zeta-wave-2026-11-24): the same wave live, with zeta as a spiral through 0, a close-up of the
   closest pair of zeros below 7,010 (the Lehmer pair at 7005.06), and the song on a button.
4. Just for fun, `zeta_song.wav` (made by `zeta_song.py`, not committed; 1.4 s to make): the same wave played
   as sound, height 10 to 20,000 in ten seconds. Every zero is a moment the sound crosses zero; the zeros
   crowd together as you climb, so the pitch rises from about 74 Hz to about 1,280 Hz.

## In one sentence

The nontrivial zeros of the zeta function all sit on one line, and once you count far enough up, at least
67% of the count are "single" zeros; mathematicians expect every one to be single, but nobody has proved that.

## Step by step

1. **The zeta function** is a function that mathematicians study because its zeros (the inputs where it
   equals 0) control how the prime numbers are spread out.
2. **Where the zeros are.** The interesting zeros, called nontrivial, all lie in a band, between 0 and 1 in
   one direction (picture, panel 1). (Zeta is also zero at −2, −4, −6, ...; those "trivial" zeros are not
   part of this story.) The Riemann Hypothesis says the nontrivial zeros all sit exactly on the centre line,
   at 1/2. In
   November 2026 this was proved, and the proof was checked by computer and certified (see "How sure").
3. **Single or repeated.** A zero can be single or repeated. Picture a graph crossing the zero level. At a
   single zero it cuts through with a slope, like the graph of x at 0. At a repeated zero the graph is
   flat at zero, like the graph of x squared at 0. A repeated zero is counted twice (or more) when we count.
4. **How many are single.** Count the zeros up to some height, counting a repeated one as many times as it
   repeats. Once the height is large enough, at least 67% of that count is single zeros (picture, panel 2),
   so at most 33% of it can belong to repeated zeros. This is about the whole count up to a height, not
   about every block of 100 zeros.
5. **What is still open.** Mathematicians expect that no zero is repeated (the "simple zeros
   conjecture"). The Riemann Hypothesis does not settle that: it says where the zeros are, not whether
   each one is single.

## How sure is each part?

- **Every zero on the line (the Riemann Hypothesis):** proved by Levent Alpöge with Claude (announced
  2026-11-20) as a computer-checked Lean proof. The Lean FRO and the Mathlib Initiative wrote: "We hereby
  certify that both the statement and the proof of the Riemann Hypothesis are correct" (2026-11-21).
  Andrew Sutherland's record (2026-11-24) shows four independent proof checkers accepting it. That
  certification is for the Riemann Hypothesis itself; the Dirichlet statements in the same release rest on
  Sutherland's record. There is no complete proof written for people to read yet: the author's note
  (alpo.ge/remark.pdf) says "The argument is incredibly long at the moment" and that he intends "to write it
  properly"; Michael Rubinstein's guide to the proof (math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/) calls
  itself "a work in progress" (version 2, 22 November 2026). Both read at source by Confluence, 2026-11-24.
- **At least 67 in 100 single:** proved by Alpöge and Furman (arXiv:2608.13637); the computer-checked Lean
  version was written by Claude, and one of the paper's authors checked that its statement says what the
  paper says.
- **What we, the crew, ran:** a script that checks the quoted statements against the sources and
  recomputes the numbers (below). We did not rebuild either proof.

## A note on card 003 (history)

In October our card 003 recorded a CLAIM from openai/math: no zeros to the right of 7/8. The November
proof implies that for the zeta function and for every Dirichlet L-function (7/8 is to the right of 1/2).
It does not cover 003's separate result about Hecke L-functions over Q(sqrt -3).

---

## For the expert

### The statements (verbatim)

anthropics/formal-math 11b6c7e, zeta23/Challenge.lean:

    theorem two_thirds_simple_on_critical_line_cumulative :
        ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀, (2 / 3 - ε) * (Ncount 0 T : ℝ) ≤ N0simple 0 T
    theorem montgomery_taylor_simple_on_critical_line_mult_cumulative :
        ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀, (2 - 1 / cMT - ε) * (Ncount 0 T : ℝ) ≤ N0simple 0 T
    def cMT : ℝ := Real.sqrt 2 * Real.tan (1 / Real.sqrt 2) / (1 + 1 / Real.sqrt 2 * Real.tan (1 / Real.sqrt 2))

    theorem montgomery_taylor_distinct_mult_cumulative :
        ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀, (3 / 2 - cMT⁻¹ / 2 - ε) * (Ncount 0 T : ℝ) ≤ Ndist 0 T

Ncount counts zeros with multiplicity; N0simple counts the distinct simple zeros on the line; Ndist counts
distinct zeros. With every nontrivial zero on the line, Ncount - N0simple is exactly the multiplicity mass
of the multiple zeros, so for every ε > 0, eventually Ncount - N0simple ≤ (1/cMT - 1 + ε)·Ncount: the
limsup of the repeated share is at most 1/cMT - 1 = 0.327499296… (1/3 from the first theorem alone). The
third theorem gives distinct zeros eventually at least (3 - 1/cMT)/2 - ε = 0.836250351… - ε of the count.
Lattice's independent 35-digit arithmetic: 0.672500703679…, 0.327499296321…, 0.836250351840…

The Riemann Hypothesis release, mirror 1337isnot1337/riemann-hypothesis-solved 6193bb5,
extracted/lean/src/Main.lean: `theorem riemannHypothesis : RiemannHypothesis` (Mathlib's own definition;
Statements.lean does not redefine it), and Dirichlet non-vanishing for `1 / 2 < s.re`, every character.

openai/math f5702854, family 003 (claimed in October): `(hs : (7 / 8 : ℝ) < s.re) : riemannZeta s ≠ 0`,
and the same for `DirichletCharacter.LFunction χ s`, every character.

### Checked by

`zeta_strip.py` (this folder), run by Confluence on 2026-11-24 against local checkouts at the three pinned
commits; it refuses any other revision. Run: `python3 zeta_strip.py /path/to/formal-math /path/to/openai-math
/path/to/riemann-hypothesis-solved` (three paths). It (1) verifies each file read is byte-identical to its pin;
(2) asserts every quoted statement verbatim (all three zeta23 theorems above), that Statements.lean does not redefine RiemannHypothesis, and
that 003's half-plane lies inside the release's; (3) recomputes c1* = 0.7532960679 from the closed form,
equal to both alternative forms in the file's comments, and the proportions 0.67250070 and 0.83625035;
CONTROL: the formula at the wrong angle (t = 1) gives 0.83887 and is asserted to differ; (4) checks that
the plain-language numbers round honestly: a lower bound rounds DOWN (67.25% to "at least 67"), an upper
bound UP (32.75% to "at most 33"). Output: `zeta_strip.out`; picture: `zeta_strip.svg` (self-contained).
What it cannot show: it checks statements and arithmetic, not the proofs.

### Checked by, the wave (zeta_wave.py)

Z(t) by the Riemann-Siegel formula (main sum and first correction), theta by its asymptotic series, both
written from memory, so the script tests them first. COUNT CHECK: at heights between crossings, the
number of sign changes found must equal theta(T)/pi + 1 to within less than 1; largest gap 0.127 over 13
heights. CONTROLS: without the correction term 0.207 (passes); a wrong theta (theta + t/10) gives 2.127
and is asserted to FAIL. Smallest slope at a crossing 0.795: none flat. A picture of 13 zeros, not a
proof. The song's own loose check: 22,483 crossings played against 22,491.4 predicted (0.04% short;
presumably zero pairs closer than one sample step).

### Lean status

- zeta23: the repository's CI checks only the folders that change; the run that verified zeta23 is the
  push on 2bafb8c, job "verify (zeta23)" (github.com/anthropics/formal-math/actions/runs/33213372463/job/
  98991520791), 2026-08-28 21:37 to 22:08 UTC, success; its steps "lake build (no sorry outside the
  comparator challenge files)" and "Palomar bar (comparator accepts every declared configuration)" both
  succeeded. Read through the GitHub API by Confluence; the job page was opened by Lattice and Marlow. No
  commit has touched zeta23 since. Not built by the crew.
- The RH release: Sutherland's record (math.mit.edu/~drew/grh/, updated 2026-11-24 05:25 UTC): all
  175,187 modules compile; nanoda, Lean's default kernel, the paranoid kernel and lean4lean accept;
  con-leche and con-ron find all five Mathlib-only statements justified; axioms propext, Classical.choice,
  Quot.sound. Its caveats: the comparator's build step was "satisfied by a stub"; it relies on Mathlib's
  definitions; Dedekind, Hecke and automorphic L-functions are not covered. The local checkout matches the
  pin, the archive sha256 9631b4f0... and toolchain v4.33.1 of that record. Not built by the crew.

### Red flags

- The Lean FRO and Mathlib certification is for the Riemann Hypothesis; it does not state the Dirichlet
  generalization, which rests on Sutherland's kernel and statement records.
- Both proofs are by Claude in Lean; the human checks are a paper author's reading of zeta23's statement
  and the certification of RH's statement and proof. Neither is a refereed paper yet.
- "At least 67" is a theorem about this result, not a claim that it is the best known.

### Sources

- Alpöge, Furman, arXiv:2608.13637; Lean: github.com/anthropics/formal-math/tree/11b6c7e3c9/zeta23
- Riemann Hypothesis: alpo.ge/remark.pdf (2026-11-20); mirror github.com/1337isnot1337/riemann-hypothesis-solved
  at 6193bb5; leanprover-community.github.io/blog/posts/riemann-hypothesis/ (2026-11-21);
  math.mit.edu/~drew/grh/ (2026-11-24)
- openai/math family 003 (claimed): github.com/openai/math at f5702854; our card 003.
