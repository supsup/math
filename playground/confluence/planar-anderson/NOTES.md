# PlanarAndersonSpectrum: what it says and what was checked

Challenge: `lean/ComparatorChallenges/PlanarAndersonSpectrum.lean`. Theorem:
`OAI.PlanarAnderson.anderson_spectrum_ae`. Solution module:
`OAI.MathematicalPhysics.PlanarAnderson.Spectrum` (one file, Mathlib only).
Paper (context only): `preprints/Pure-Point-Spectrum-for-the-Two-Dimensional-Anderson-Model-at-Every-Positive-Disorder-September-23-2026/`.
Scope doc: `lean/docs/261.md`.

## The statement in plain words

Fix h > 0. Put an independent random number v(x), uniform on [-h, h], at every site x of the
infinite lattice Z^2. Then, with probability 1, the operator on l^2(Z^2; C)

    (H u)(x) = u(x+e1) + u(x-e1) + u(x+e2) + u(x-e2) + v(x) u(x)

is a bounded self-adjoint operator, and its spectrum is exactly the real interval [-4-h, 4+h].

```lean
abbrev Site := ℤ × ℤ
abbrev Configuration := Site → ℝ
abbrev Hilbert := lp (fun _ : Site => ℂ) 2

def disorderLaw (h : ℝ) : Measure Configuration :=
  Measure.infinitePi (fun _ : Site => ProbabilityTheory.cond volume (Set.Icc (-h) h))

def IsAndersonOperator (v : Configuration) (H : Hilbert →L[ℂ] Hilbert) : Prop :=
  ∀ (u : Hilbert) (x : Site),
    (H u) x = u (x.1 + 1, x.2) + u (x.1 - 1, x.2) +
      u (x.1, x.2 + 1) + u (x.1, x.2 - 1) + (v x : ℂ) * u x

def spectralInterval (h : ℝ) : Set ℂ :=
  {z | z.im = 0 ∧ -4 - h ≤ z.re ∧ z.re ≤ 4 + h}

theorem anderson_spectrum_ae {h : ℝ} (hh : 0 < h) :
    ∀ᵐ v ∂disorderLaw h, ∃ H : Hilbert →L[ℂ] Hilbert,
      IsAndersonOperator v H ∧ IsSelfAdjoint H ∧ spectrum ℂ H = spectralInterval h
```

## Audit verdict

**This is the classical almost-sure spectrum identity, stated correctly and non-trivially. It is
NOT localization.** The theorem says nothing about spectral type: no pure point spectrum, no
eigenfunction decay, no dynamical localization. The open problem the paper claims to solve, pure
point spectrum in d = 2 at every disorder, is defined in the solution file as `MainStatement` (with
`PurePoint` and `HasCompleteOrthonormalEigenbasis`) and is **never proved anywhere in the repo**. A
grep of `lean/` finds `PlanarAnderson` only in this challenge, its JSON, `OAI.lean`, `docs/261.md`
and the solution file. `docs/261.md` says the same thing: "It does not assert the pure-point spectral
type claimed in the accompanying paper."

Adversarial checks of the statement:

| Possible weakness | Finding |
| --- | --- |
| Finite box instead of Z^2 | No. `Site := ℤ × ℤ`, `Hilbert := lp _ 2`, the infinite lattice. |
| Laplacian sign or normalisation | This is the adjacency (hopping) operator with no `-4` diagonal and no minus sign. Its spectrum on Z^2 is [-4, 4], so the formula [-4-h, 4+h] matches this convention. With -Δ = 4 - adjacency the answer would be [-h, 8+h]. The two differ only by a convention. |
| Potential law | `cond volume (Icc (-h) h)` is Lebesgue measure restricted to [-h, h] and normalised: Uniform[-h, h]. It is bounded and absolutely continuous, but only this one law is covered, not a general μ. supp μ = [-h, h], so the identity reads σ(adjacency) + supp μ. |
| Degenerate probability space (junk measure) | **This was the real risk, and it is avoided.** At the pinned Mathlib rev `d13f23b7`, `Measure.infinitePi μ` is defined as `if h : ∀ i, IsProbabilityMeasure (μ i) then … else 0`. If the factors were not probability measures, the measure would be 0 and `∀ᵐ` would hold vacuously. For h > 0 the factor has volume 2h, which is in (0, ∞), so the factor IS a probability measure. The solution proves this (`uniform_probability`, via `cond_isProbabilityMeasure_of_finite`) and uses it, so the `then` branch is taken. Note that h = 0 would give the junk 0 measure. That case is excluded by `hh : 0 < h`. |
| `∃ H` admits a junk H | No. `IsAndersonOperator v H` fixes `(H u) x` for every u and x, so H is unique. The solution proves this (`anderson_unique`). `spectrum ℂ H` is Mathlib's Banach-algebra spectrum in `Hilbert →L[ℂ] Hilbert`, the standard notion. |
| Spectrum trivially ℂ, ℝ or empty | No. The claimed set is a compact interval, and the proof needs both inclusions. The ⊆ direction uses ‖H‖ ≤ 4+h and self-adjointness. The ⊇ direction uses Weyl sequences on almost-surely-existing large boxes where v is nearly constant. |
| Division by zero, sSup or sInf junk, vacuous hypotheses | No division, sSup or sInf appears. The only hypothesis is `0 < h`. |
| Measurability of the event | `∀ᵐ` only needs the bad set to lie inside a null set, which is standard and not a weakening of the claim. |

How it relates to known results: this is the Kunz-Souillard / Pastur statement that the
almost-sure spectrum equals σ(Δ) + supp μ, in d = 2 for uniform μ. It is textbook material
(e.g. Kirsch, "An invitation to random Schrödinger operators"; section not re-checked) and much easier than localization. It
is consistent with the paper's claim but adds nothing to it. The open problem is untouched by this
formalization.

## How the solution proves it (read, not re-derived line by line)

- `spectrum_subset`: self-adjointness makes the spectrum real, and ‖hopping‖ ≤ 4 together with
  ‖potential‖ ≤ h gives |z| ≤ 4 + h.
- `bounded_ae`: almost surely |v x| ≤ h at all countably many sites.
- `constant_boxes_ae`: almost surely, for every rational q in (-h, h), every tolerance 1/(l+1) and
  every box size n, some disjoint translate of the n×n box has |v - q| < tolerance everywhere.
  This is a Borel-Cantelli-style infinite-trials argument (`iid_exists_ae`). Rational density then
  extends it to real w (`HasConstantBoxes`).
- `spectrum_contains_shifted_free`: a cut-off plane wave on such a box is an approximate eigenvector
  for freeEnergy(q) + w (`spectrum_of_approximate`).
- `spectrum_contains_interior`: this covers the open interval (-4-h, 4+h), and closedness of the
  spectrum gives the closed interval (`spectrum_eq_interval`).

## Checks run

1. **Lean (Docker, check.sh).** See the "Lean run" section below.
2. **Python, `replicate.py`** (numpy, fixed seed). This is an illustration of what the statement
   says, on finite periodic L×L boxes. It is not a proof: the box matrices are not the Z^2 operator.
   - Every eigenvalue of every sampled box lies in [-4-h, 4+h]. This is the norm bound, and it
     holds exactly for every box: PASS.
   - The largest interior gap between consecutive eigenvalues shrinks as L grows. For h=1:
     0.57 → 0.17 → 0.049 → 0.040 (L = 8, 16, 32, 48).
   - The extreme eigenvalues approach ±(4+h) only **slowly**. For h=1 at L=48 they are about ±4.23,
     against the edge at 5. This is expected (Lifshitz tails): reaching within δ of 4+h needs an
     n×n patch with v ≈ h, and its probability decays like exp(-c n²). Typical finite boxes
     therefore stop well short of the edges. The theorem is about Z^2, where such patches occur
     almost surely.
   - Weyl mechanism: planting a constant n×n patch v = w inside a random box forces the top
     eigenvalue ≥ 4cos(π/(n+1)) + w, which is a Rayleigh-quotient lower bound and was checked:
     n=8 gives 4.770 ≥ 4.709, n=16 gives 4.891 ≥ 4.882, n=24 (w=0.99) gives 4.962 ≥ 4.959. This
     is how the proof reaches the edges.
   - **Controls (each must fail, and does):**
     - A checkerboard periodic potential ±h has edges ±sqrt(16+h²) = ±4.1231 and a gap (-1, 1),
       as theory predicts. It does not fill [-5, 5].
     - The zero potential tops out at 4.000, so it misses (4, 5].
     - The wrong formula [-2-h, 2+h] is rejected: 436 of 2304 random-box eigenvalues lie outside it.
   - The brief's localization branch (inverse participation ratios) was **not run**. The
     statement is not about localization, so an IPR study would illustrate the paper, not the
     theorem, and finite-box IPRs cannot decide spectral type on Z^2 in any case.
3. **Java, `confluence.math.anderson.PlanarAnderson`.** This is the same illustration on a 10×10
   torus with a cyclic Jacobi solver.
   - The solver matches the exact torus spectrum {2cos(2πj/L) + 2cos(2πk/L)} to 1e-13.
   - The random box has eigenvalues in [-4.200, 4.069], inside [-5, 5].
   - The planted 8×8 patch gives 4.787 ≥ 4.709.
   - The checkerboard control fails (edges ±4.1231, gap (-1, 1)), and so does the zero-potential
     control (top 4.000).
   - The program prints "ALL CHECKS AS EXPECTED".

## Lean run

Run 2026-10-08 19:09Z with Lean 4.34.1, a one-module cone, and Mathlib only. Log:
`playground/confluence/lean-docker/anderson-run.log`. The output was "Build completed successfully
(8925 jobs)", followed by:

    'OAI.PlanarAnderson.anderson_spectrum_ae' depends on axioms: [propext, Classical.choice, Quot.sound]
    'controlWithSorry' depends on axioms: [sorryAx]        <- negative control, fires as it must

These axioms equal the permitted set in the JSON exactly. There is no `sorryAx`.

`statement_match.py PlanarAndersonSpectrum` reported 7 challenge declarations and 7 identical, with
0 that differ and 0 missing. It also found 38 helpers that exist only in the solution. I diffed the
two files by hand and found only additions in the solution: a doc comment,
`instance : Nontrivial Hilbert`, the `eigenvalues` / `PurePoint` / `HasCompleteOrthonormalEigenbasis`
/ `MainStatement` definitions, and the proof. The extra `Nontrivial` instance could in principle
change elaboration. It does not enter the stated types: `spectrum`, `IsSelfAdjoint` and
`infinitePi` need no `Nontrivial`. The matcher also says the declarations are identical, which I
take as corroboration rather than proof.

## LIMITS

- The numerics illustrate. They cannot prove an almost-sure statement on Z^2, and finite boxes
  never show the exact edges.
- I read the Lean proof's structure but did not re-derive each lemma by hand. Trust in the proof
  rests on the kernel check plus `#print axioms`.
- The Mathlib `infinitePi` junk branch was checked against the source at the pinned rev
  (`Mathlib/Probability/ProductMeasure.lean`, fetched from GitHub at `d13f23b7`), not against
  the copy inside the Docker volume.
- I did not read the paper. Nothing here assesses its pure-point claim.

## Confluence's recheck

- `lean/docs/261.md:11`: "This selected statement identifies the spectral set. It does not assert the pure-point
  spectral type claimed in the accompanying paper." So the formal result is the classical a.s. spectrum identity
  (Pastur / Kunz-Souillard, d = 2, uniform disorder), and the paper's headline (2D localization at every disorder)
  is NOT kernel-checked anywhere in the collection.
- `hh : 0 < h` is what keeps `Measure.infinitePi` off its junk-zero branch (at h = 0 the factor is not a
  probability measure and the a.e. statement would hold vacuously).
- Axioms: [propext, Classical.choice, Quot.sound]; sorry control on [sorryAx]. statement_match 7/7.
- The planted-patch bounds use w = 0.95, 0.95, 0.99 (replicate.py line 69): 4 cos(pi/(n+1)) + w = 4.709, 4.882,
  4.958 for n = 8, 16, 24, matching the report.
