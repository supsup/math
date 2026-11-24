# Card draft (Confluence): Two thirds of the zeros are simple and on the line; and where the rest may be

For Fixpoint to edit into the showcase. Sources per Charles (2026-11-24): both collections, each cited.
Agreed in Undervoice #general 34414-34440 (Marlow's frame: zeta23 asks how many zeros are simple and on
the line; card 003 is the companion asking where zeros are excluded; both denominators labelled; the band
not shaded by density).

## Claim, in plain words

Count the nontrivial zeros of the Riemann zeta function up to height T, each as many times as its
multiplicity. As T grows, at least two thirds of that count are zeros that are simple and lie exactly on
the critical line Re s = 1/2; with the optimal Montgomery-Taylor window the share is at least
2 - 1/c1* = 0.67250..., and at least (3 - 1/c1*)/2 = 0.83625... of the count are distinct zeros. The same
holds for the zeros of L(s, chi) for every primitive Dirichlet character chi modulo q > 1.

## The formulas (verbatim, anthropics/formal-math 11b6c7e, zeta23/Challenge.lean)

    theorem two_thirds_simple_on_critical_line_cumulative :
        ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀, (2 / 3 - ε) * (Ncount 0 T : ℝ) ≤ N0simple 0 T
    theorem montgomery_taylor_simple_on_critical_line_mult_cumulative :
        ∀ ε > 0, ∃ T₀ : ℝ, ∀ T ≥ T₀, (2 - 1 / cMT - ε) * (Ncount 0 T : ℝ) ≤ N0simple 0 T
    def cMT : ℝ := Real.sqrt 2 * Real.tan (1 / Real.sqrt 2) / (1 + 1 / Real.sqrt 2 * Real.tan (1 / Real.sqrt 2))

Ncount counts zeros with multiplicity (`∑ᶠ ρ ∈ zerosIn T₁ T₂, zeroMult ρ`); N0simple counts the distinct
simple zeros on the line (`.ncard`). Theorems A to E carry dyadic forms (T, 2T] too, and E the Dirichlet
analogues.

## The companion (openai/math f5702854, family 003, CLAIMED)

    theorem riemannZeta_ne_zero_of_seven_eighths_lt_re {s : ℂ} (hs : (7 / 8 : ℝ) < s.re) : riemannZeta s ≠ 0
    theorem LFunction_ne_zero_of_seven_eighths_lt_re {q : ℕ} [NeZero q] (χ : DirichletCharacter ℂ q) {s : ℂ}
        (hs : (7 / 8 : ℝ) < s.re) (hpole : ¬ (χ = 1 ∧ s = 1)) : DirichletCharacter.LFunction χ s ≠ 0

A full half-plane (no hypothesis on Im s), for every Dirichlet character of every modulus.

## The combination (ours; elementary; NOT formalized; CONDITIONAL on 003's claim)

From zeta23: N - N0s is the multiplicity-weighted mass of the zeros that are off the line OR multiple
(including repeated zeros on the line), so for every ε > 0, eventually N - N0s <= (1/c1* - 1 + ε) N, that
is at most 0.32750 of the count (1/3 with Theorem B alone). From 003, if it holds: no nontrivial zero has
Re > 7/8, and by the functional equation none has Re < 1/8 (for a complex character, through its
conjugate, which 003 also covers). Together: every off-line nontrivial zero lies in 1/8 <= Re <= 7/8, and
those zeros together with the multiple ones are at most a third of the count. Neither source states this.
The picture says WHERE an off-line zero may be, never how many: the band is deliberately not shaded.

## Checked by

`zeta_strip.py` (this folder), run by Confluence on 2026-11-24 against local checkouts at the two pinned
commits; it refuses any other revision. It (1) verifies both statement files are byte-identical to the
pinned commits; (2) asserts every quoted statement above is present verbatim, that 003 has no imaginary-part
hypothesis and no primitivity restriction; (3) recomputes c1* = 0.7532960679 from the closed form, equal to
both alternative forms in the file's comments, and the proportions 0.67250070 and 0.83625035 (the
comments' decimals); CONTROL: the same formula at the wrong angle (t = 1) gives 0.83887 and is asserted to
differ, so the check can fail; (4) checks the combination's arithmetic (1/c1* - 1 = 0.32749930 < 1/3).
Output: `zeta_strip.out`. What it cannot show: it checks statements and arithmetic, not the proofs; nobody
on the crew built either Lean project.

## Lean status

- zeta23: sorry-free and the three standard axioms per its README and AUDIT.md; the repository's CI checks
  only the folders that change, so the run that verified zeta23 is the push on 2bafb8c (2026-08-28,
  success); no commit has touched zeta23 since (git log), so it covers the files at 11b6c7e. Read: the run
  list, not the job logs. Not built by the crew (a full build is Charles's call on the machine).
- 003: statement unchanged since adc7f124 (2026-10-06); my October kernel build of DirichletSevenEighths
  and QuasiRiemannHypothesis passed (7,062 jobs, confluence/playground 114062e2). The comparator was not run.

## Red flags

- The combination's whole force is 003's CLAIM: a zero-free half-plane at 7/8 would be a quasi-Riemann
  hypothesis, a result of the first rank, which is why 003 is labelled Claimed.
- The functional-equation step (Re < 1/8) is in neither Lean.
- zeta23's proof and Lean are by Claude; the human check is that a paper author read the trusted statement
  against the paper. That is the strongest statement-trust of anything on our page, and still not a
  refereed proof.

## Sources

- Alpoge, Furman, "More than two thirds of the zeros of the Riemann zeta function are simple and on the
  critical line", arXiv:2608.13637; Lean: github.com/anthropics/formal-math/tree/11b6c7e3c9/zeta23
- openai/math family 003 (claimed): github.com/openai/math at f5702854, lean/ComparatorChallenges/
  QuasiRiemannHypothesis.lean and DirichletSevenEighths.lean; our card 003.
