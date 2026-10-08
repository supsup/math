# Rokhlin: `OAI.Rokhlin.mixing_all_finite_orders`

Challenge: `lean/ComparatorChallenges/Rokhlin.lean` (+ `.json`, solution module
`OAI.Dynamics.MultipleMixing.Main`, 13-module Mathlib-only cone, about 27.9k lines).
Paper: `preprints/Rokhlins-multiple-mixing-problem-for-one-transformation-September-23-2026/`.
Its abstract reads "Every invertible mixing probability-preserving transformation is mixing of
every finite order." Docs page: `lean/docs/145.md`.

## Statement in plain words

Take any measurable space `Ω`, any probability measure `μ` on it, and any measurable bijection
`T` with measurable inverse (`Ω ≃ᵐ Ω`) that preserves `μ`. Suppose `T` is mixing: for all
measurable `A` and `B`, `μ(A ∩ T^{-n} B) → μ(A) μ(B)` as `|n| → ∞` over the integers. Then for
every `k ≥ 3` and all measurable `A_0, …, A_{k-1}`, the following holds. Put
`t_i = g_0 + … + g_{i-1}`, where every gap `g_j` is at least 1. Then
`μ(⋂_i T^{-t_i} A_i) → ∏ μ(A_i)` as ALL gaps go to infinity together.

## Audit verdict: this is the FULL Rokhlin problem, not a weakening

The challenge states, in full, Rokhlin's 1949 problem for a single invertible transformation.
It is in fact slightly more general, because `Ω` need not be a standard Borel space. I found
none of the weakenings I looked for. Item by item:

| Possible weakening | Finding |
|---|---|
| Restricted class of systems | None. Any `Ω`, any probability `μ`, any `T : Ω ≃ᵐ Ω` with `MeasurePreserving T μ μ`. There is no standardness or rank assumption, so the class is a superset of the classical one. |
| Trivial space (Dirac) | `μ` is universally quantified. A Dirac measure is one allowed instance, not the only one. |
| Mixing definition too strong (vacuous hypothesis) | `IsMixing` uses `n : ℤ` with filter `comap Int.natAbs atTop`, which is `|n| → ∞`. For an invertible measure-preserving `T`, the negative-`n` half is equivalent to the positive half: `μ(A ∩ T^{|n|}B) = μ(T^{-|n|}A ∩ B)`. So this is standard mixing, and Bernoulli shifts satisfy it. |
| Mixing definition too weak | It is quantified over ALL measurable `A` and `B`, not over a generating family. |
| "All orders" collapsing to 2-mixing | The conclusion is `∀ k ≥ 3`, with `k` sets and `k-1` independent gaps. |
| Gaps at a fixed rate or along one direction | The filter is `atTop` on `Fin (k-1) → ℕ+` with the product (Pi) order. Its basic sets are `{g : ∀ j, g j ≥ a j}`, so this means "every gap ≥ N eventually", which is the standard definition. `ℕ+` is nonempty and directed, so the Pi type is too. Hence `atTop` is `NeBot`, and the `Tendsto` is not vacuous. |
| Time layout | `layoutTime gaps i = ∑_{j<i} gaps j` gives the times `0, g0, g0+g1, …`. This was checked in Python and Java (`(5,7,11) → [0,5,12,23]`). |
| `x/0`, `sSup`/`sInf` | Neither appears. Values are `ℝ≥0∞`, and limits are taken in the order topology of `ℝ≥0∞` at finite targets. |
| Preimage direction | `timeMap T t = ⇑(T.toEquiv ^ t)`, and the conclusion uses `timeMap T t ⁻¹' A`, i.e. `T^{-t} A`. That is standard. |

The Lean evidence, quoted from the challenge:

```lean
def IsMixing (μ : Measure Ω) (T : Ω ≃ᵐ Ω) : Prop :=
  ∀ A B : Set Ω, MeasurableSet A → MeasurableSet B →
    Tendsto (fun n : ℤ => μ (A ∩ timeMap T n ⁻¹' B))
      (comap Int.natAbs atTop) (𝓝 (μ A * μ B))

def MixingOfOrder (μ : Measure Ω) (T : Ω ≃ᵐ Ω) (k : ℕ) : Prop :=
  ∀ A : Fin k → Set Ω, (∀ i, MeasurableSet (A i)) →
    Tendsto
      (fun gaps : Fin (k - 1) → ℕ+ =>
        μ (⋂ i : Fin k, timeMap T (layoutTime gaps i : ℤ) ⁻¹' A i))
      atTop (𝓝 (∏ i : Fin k, μ (A i)))

theorem mixing_all_finite_orders (μ : Measure Ω) [IsProbabilityMeasure μ]
    (T : Ω ≃ᵐ Ω) (h_pres : MeasurePreserving T μ μ) (h_mix : IsMixing μ T) :
    ∀ k : ℕ, 3 ≤ k → MixingOfOrder μ T k
```

Consequence: if the formal proof is sound, it settles an open problem from 1949. Partial cases
were known before, for example rank one (Kalikow), finite rank (Ryzhikov), and positive entropy
or Bernoulli systems. That makes it an extraordinary claim. The checks below raise confidence in
the kernel-level claim, but none of them check the mathematics independently.

## Lean check (Docker, `check.sh Rokhlin`, log `../lean-docker/rokhlin-run.log`)

- Lean 4.34.1, Mathlib at `d13f23b7…`. The 13-module cone built successfully (8937 jobs).
  `Joinings` was the longest module at 89s.
- `'OAI.Rokhlin.mixing_all_finite_orders' depends on axioms: [propext, Classical.choice, Quot.sound]`.
  These are exactly the permitted three, with no `sorryAx`.
- Negative control: `'controlWithSorry' depends on axioms: [sorryAx]`. The axiom printer is live.
- A grep of the cone for `sorry`, `axiom`, `admit`, `native_decide`, `implemented_by`, `extern`,
  `unsafe` and `csimp` found no hits.

## statement_match

`identical: 5  differ: 0  missing from solution: 0` (1869 helper declarations exist only in the
solution). I confirmed this by hand. The four definitions sit in `HilbertCodes.lean` in namespace
`OAI.Rokhlin` and are textually identical to the challenge's. The theorem header in `Main.lean`
(line 317) is identical too.

The matcher is textual, so I also looked for context that could change how identical text
elaborates. The cone adds no instance on `Pi`, `ℕ+`, `ℤ`, `ℝ≥0∞`, `Measure` or a general
`MeasurableSpace`. It adds no `notation`, `macro` or `syntax` overrides. Its instances are on its
own types (`StandardSpace`, `HilbertCode`, kernels), plus `local` ones on `Circle`/`Fact`. The
extra `open scoped InnerProductSpace CStarAlgebra` and `open ContinuousLinearMap` in
`HilbertCodes` do not touch any symbol used in the four definitions, as far as I can see.

## Computations (illustration of the DEFINITIONS, not evidence for the theorem)

`numerics.py` (output in `numerics-output.txt`) and
`java/src/confluence/math/rokhlin/Rokhlin.java` compute the triple correlation
`μ(A ∩ T^{-g1}B ∩ T^{-(g1+g2)}C)` against `μ(A)μ(B)μ(C)`:

- **Bernoulli(3/10) two-sided shift, cylinder sets, exact rationals.** The value equals the
  product EXACTLY once the minimum gap is at least the window length (gaps 3, 4, 10, 100, 1000).
  It differs at gaps 1 and 2. With gaps (50,1) it is not the product, which confirms that BOTH
  gaps must grow.
- **Doubling map (non-invertible, so outside Lean's class).** Monte Carlo, 200k samples, exact
  400-bit orbits. Product 0.0600 ± 0.0005. Gaps (1,1) give 0.0998, and gaps (60,90) give 0.0603.
- **Arnold cat map (invertible and mixing, so inside the class).** Monte Carlo on an exact
  integer lattice. Product 0.0180. Python: gaps (1,1) give 0.0247, and (30,50) give 0.0180.
  Java (400k samples): (15,20) give 0.0179 ± 0.0002.
- **NEGATIVE CONTROL: rotation by the golden mean (invertible, ergodic, NOT mixing).** Exact
  interval arithmetic with `A = [0, 0.4)`. Along Fibonacci `n` the 2-fold correlation is 0.4000,
  not 0.16. Along consecutive-Fibonacci gap pairs up to (832040, 1346269) the 3-fold correlation
  is 0.4000, not 0.064. Over `n ∈ [1e5, 1e5+2000)` it ranges from 0.0000 to 0.3998 and its
  Cesàro mean is 0.1600: ergodic but not mixing. The control fails both definitions as it
  should, so the check can tell the two cases apart.
- Java run: `ALL CHECKS PASSED`, exit 0. The Java check asserts that Bernoulli is exact at
  gaps ≥ 4, that the cat map is within 5σ at (15,20), and that the rotation stays more than 0.2
  away from μ(A)³.

## LIMITS / could not determine

- **I did not check the mathematics of the proof.** That covers about 28k lines of joinings,
  fibre measures, Hilbert codes and entropy, and I did not read the paper's argument. The claim
  rests on the Lean kernel accepting the build plus the axiom list.
- **The real Comparator was NOT run** (`leanprover/comparator`, a term-level comparison of the
  challenge against the solution). Nanoda is disabled in the JSON, and no second kernel was run.
  The statement match is textual plus a manual context review. It is not a term equality.
- `#print axioms` was run in the same environment that compiled the solution. I did not separately
  rebuild the challenge file and compare `Expr`s.
- I did not prove that `atTop` on the Pi type is the min-gap filter. I argued it from the
  definition `atTop = ⨅ a, 𝓟 (Ici a)` and the Pi order, without running a Lean lemma check
  (for example `Filter.tendsto_atTop` or `atTop_pi` in this Mathlib revision).
- I did not compute a Gaussian or Chacon system. Chacon would be a second negative control,
  weakly mixing but not mixing.
- Numerics cover a handful of interval and rectangle sets and finitely many gaps. They illustrate
  the definitions. They say nothing about the open problem, since every positive example is
  Bernoulli, where all-orders mixing is classical.

## Confluence's recheck

- Read the challenge myself: any measurable space, any probability measure, any measurable bijection T
  preserving it; IsMixing over ALL measurable A, B with |n| -> infinity over Z; MixingOfOrder k for every k >= 3,
  times 0, g0, g0 + g1, ... as partial sums of k - 1 positive gaps, along `atTop` on `Fin (k - 1) -> ℕ+`, whose
  basic sets are {g | g >= a} coordinatewise, i.e. every gap eventually large. That is Rokhlin's problem in full
  (no rank, standardness or rate restriction).
- Build log: `Build completed successfully (8937 jobs)`; theorem on [propext, Classical.choice, Quot.sound];
  sorry control on [sorryAx]. statement_match 5/5.
- Caption level as agreed for log-BM and Crouzeix: "the collection's Lean artifact kernel-checks this formal
  statement", pending a second independent statement reading and proof review.
