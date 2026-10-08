# HilbertCrouzeix: statement audit and checks

Challenge: `lean/ComparatorChallenges/HilbertCrouzeix.lean`. The JSON says the solution module is
`OAI.Analysis.HilbertCrouzeix.Main` and lists **four** theorems, not one:
`numericalClosure_geometry`, `exists_finite_compression`, `rational_denominator_isUnit`, `zeroConclusion`.
`lean/docs/325.md` calls this file "Numerical-range geometry and finite-compression support" for the
collection's Crouzeix papers. The headline claim (the complete Crouzeix inequality with constant 2
on any Hilbert space) is a **different** challenge, `CrouzeixHilbert.lean` (`OAI.CrouzeixHilbert.hilbert`,
solution `OAI.Analysis.Crouzeix.Main`). This audit does not cover it.

## Statement in plain words

Setting: `H` is a complex inner-product space and `A : H →L[ℂ] H` is a bounded operator. `CompleteSpace H`
(Hilbert space) is assumed for theorems 1, 3 and 4 and explicitly dropped for theorem 2.

`numericalRange A = {z | ∃ x, ‖x‖ = 1 ∧ inner ℂ x (A x) = z}`, and `numericalClosure A = closure (numericalRange A)`.

1. **`numericalClosure_geometry`**: `IsCompact (closure W(A)) ∧ Convex ℝ (closure W(A)) ∧ spectrum ℂ A ⊆ closure W(A)`.
   This is the Toeplitz-Hausdorff theorem (W is convex), together with the facts that W is bounded by
   ‖A‖ and that the spectrum lies in the closure of W. All of these are classical textbook results.
2. **`exists_finite_compression`**: take an *algebraic* tensor ξ ∈ H ⊗ ℂ^m and a matrix polynomial
   Σ_k A^k ⊗ B_k. Then there is a finite-dimensional subspace E ⊆ H, and an η, such that ι(η) = ξ and
   ι(p(P_E A|_E) η) = p(A) ξ. This holds because E = span{A^j x_i : j ≤ d} works: (P_E A)^k x_i = A^k x_i
   for k ≤ d. It is elementary and true.
3. **`rational_denominator_isUnit`** (with `[Nontrivial H]`): if closure W(A) avoids every zero of each
   denominator `(R i j).denom`, then `aeval A denom` is invertible. Proof: theorem 1 plus spectral mapping.
   It is true. The `Nontrivial` hypothesis is not needed for the truth of the statement: on a trivial
   space every operator is a unit.
4. **`zeroConclusion`** (with `[Subsingleton H]`): this is the degenerate case H = 0. Here W(A) = ∅
   (there are no unit vectors), `normSup ∅ _ = 0` by definition, and every operator on the amplification
   is 0. So each Crouzeix-type bound reads 0 ≤ 2·0. The theorem is true and vacuous in content. It
   pins down the empty-set convention the main theorem needs.

## Relation to Crouzeix's conjecture

None of the four theorems is Crouzeix's conjecture, and none of them is a Crouzeix-type inequality
except in the trivial H = 0 case (theorem 4). They are support lemmas, all of them known or
elementary. Theorem 1 is what lets the main development replace sup over W by max over closure W
(see `normSup_closure` and `polynomial_sup_eq_max` in the solution). It also places the spectrum, and
so the poles a rational or holomorphic calculus must avoid, inside the closure. Proving these four
says nothing about whether the constant 2 holds.

## Definitions audit (traps checked)

- **Unit vectors, not all vectors.** The definition uses `‖x‖ = 1`. Over all vectors the set would be
  a cone, and over ‖x‖ ≤ 1 it would be conv(W ∪ {0}).
- **Inner product slot.** Mathlib's `inner ℂ x y` is conjugate-linear in `x`, so `inner ℂ x (A x)` is
  x*Ax, the standard numerical range. The Java mutant that drops the conjugate makes the checks FAIL
  (see Checks), so the convention is load-bearing.
- **Closure.** It is taken in ℂ, after the image. This matters only in infinite dimension: diag(1/k)
  on ℓ² has W = (0,1], which is not closed, while 0 is in the spectrum. Truncations give min Re W_N =
  1/N → 0.
- **Bounded operators.** These are `H →L[ℂ] H`, and spectrum is taken in the Banach algebra of
  bounded operators (Mathlib `spectrum ℂ A`). That is the standard meaning when `CompleteSpace H`.
- **Empty set.** If H = 0, then W = ∅, the closure is ∅ (compact and convex), and the spectrum is ∅
  (every element of a subsingleton algebra is a unit). Theorem 1 therefore holds, and is not vacuous
  for nontrivial H. `normSup` has an explicit `if S.Nonempty then sSup … else 0`. For bounded S it is
  the true sup. For unbounded images `sSup` would be 0 (Lean's junk value), but W is bounded and the
  functions involved are continuous or polynomial on it. That matters for the main challenge, not
  for these four statements.
- **Theorem 1 has no vacuous hypotheses.** Its only binders are `A` and the ambient instances.
- **No division** appears in the statements of theorems 1 and 2. In 3, `Ring.inverse` (junk 0 when
  not a unit) appears only in definitions that the conclusion does not use. The conclusion is the
  honest `IsUnit`.
- Unused machinery: `chosenContour` uses `Classical.epsilon` and `holomorphicCalculus` is a Dunford
  integral. Both appear only inside `ZeroConclusion`, where everything is 0 anyway. Their faithfulness
  is a question for the main challenge, not this one.

## Checks (independent, numpy 2.0.2 / JDK 25)

`numerical_range.py` (overall PASS):

| matrix | K: \|x*Ax\| ≤ ‖A‖ | C1: samples in support half-planes | C2: midpoint attained (max resid) | S: eigenvalues in W |
|---|---|---|---|---|
| normal diag(1, i, -1+0.5i) | ok | ok | 6.7e-12 | ok (excess 0.0: on boundary) |
| Jordan J2 | ok | ok | 6.1e-14 | ok |
| Jordan J4 | ok | ok | 1.3e-13 | ok |
| [[1,2],[0,i]] (ellipse) | ok | ok | 1.2e-13 | ok |
| random 3x3, 4x4, 5x5 | ok | ok | ≤ 3.9e-13 | ok |

- The boundary of W comes from the top eigenvector of Re(e^{-it}A), over 2048 directions. The
  support half-planes cut out conv W. C1 alone is containment and does not show convexity. C2 is the
  convexity check: it constructs a unit vector in span{x, y} whose value equals the midpoint.
- W(J_n) is a disk of radius cos(π/(n+1)). The sampled boundary has |z| = 0.5 for J2 and
  0.809016994375 for J4, matching to 1e-12.
- `HilbertCrouzeix.java` runs the same checks on 2x2 matrices in closed form (no eigen-solver), with
  overall PASS. **Mutant:** with the conjugate dropped in x*Ax, three of four matrices FAIL and the
  overall result is FAIL with exit 1.
- `numerical-range.svg` comes from `make_svg.py`, and every point in it is computed by the script.
  It shows the ellipse W([[1,2],[0,i]]) with foci at the eigenvalues 1 and i. It marks two sample
  points and their midpoint, which a unit vector attains with residual 7.6e-14, and draws the
  real-vector control curve dashed.

## Negative controls (each must fail the property, and each does)

- N1, real-vector variant {xᵀAx : x real unit} of [[1,2],[0,i]]: this set is a closed curve, and the
  midpoint of two of its points is missed by up to 0.42 (Python) and 0.44 (Java). Convexity fails.
- N2, "spectrum in the interior of W", for a normal matrix: the eigenvalues are vertices of W, with
  half-plane excess exactly 0, so they sit on the boundary. The statement fails. The theorem claims
  only ⊆ closure W.
- N3, "W = conv(spectrum)", for J2: 0.45 ∈ W but conv σ = {0}. The statement fails for non-normal A.

## Context only, not a check of this theorem: Crouzeix ratios ‖p(A)‖ / max_W |p|

J2 with p = z gives exactly 2.0000, the known extremal case. J4 with p = z³ gives 1.8885
(= 1/cos³(π/5)). Random cubics on all the examples gave at most 1.33. Nothing exceeded 2.
These are a handful of examples and are not evidence for the conjecture.

## Lean (Docker, Mathlib-only cone)

Log: `playground/confluence/lean-docker/crouzeix-run.log`. The run used Lean 4.34.1 on a 7-module
cone. All 7 `OAI.Analysis.HilbertCrouzeix.*` modules built ("Build completed successfully"), and the
script exited with 0.

```
'OAI.HilbertCrouzeix.numericalClosure_geometry' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.HilbertCrouzeix.exists_finite_compression' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.HilbertCrouzeix.rational_denominator_isUnit' depends on axioms: [propext, Classical.choice, Quot.sound]
'OAI.HilbertCrouzeix.zeroConclusion' depends on axioms: [propext, Classical.choice, Quot.sound]
'controlWithSorry' depends on axioms: [sorryAx]     <- harness control: a sorry IS detected
```

Every theorem uses only the permitted axioms, and none uses `sorryAx`. I grepped the solution files
and found no `sorry`, `admit` or `axiom`.

`statement_match.py HilbertCrouzeix` reported 30 challenge declarations, 30 identical, 0 differing,
0 missing, and 58 solution-only helpers. The match is textual. The 30 compared declarations include
all the definitions and the four theorem statements.

Proof route, read for context: spectrum ⊆ closure W uses a standard argument. If dist(z, W) ≥ δ,
then ‖(z−A)x‖ ≥ δ‖x‖, and the same bound holds for the adjoint. This makes z − A injective with
closed dense range, so it is invertible. Convexity is proved directly in `NumericalRange.lean`
(`convex_numericalRange`).

## LIMITS / could not determine

- The numerics are finite-dimensional only. The theorem is about arbitrary, possibly
  non-separable, Hilbert spaces. The diag(1/k) truncation only illustrates why the closure is
  needed and proves nothing.
- Sampling: there are 2048 or 4096 support directions and finitely many random vectors. C2's
  search can fail to *find* an attaining vector, which would be a false FAIL. It cannot produce a
  false PASS, because the residual is computed from an actual unit vector.
- This audit covers the four statements in this challenge only. The headline Crouzeix claim
  (`CrouzeixHilbert`), and whether its `holomorphicCalculus` and `chosenContour` (`Classical.epsilon`)
  definitions are faithful, are out of scope and not assessed.
- The textual statement_match is weaker than Comparator's term-level comparison.

## Confluence's recheck

- Build log: all four theorems on [propext, Classical.choice, Quot.sound]; sorry control on [sorryAx].
- By hand: W(J_2) is the disk of radius cos(pi/3) = 1/2, so ||J_2|| / max_W |z| = 1 / (1/2) = 2, the extremal case;
  W(J_4) has radius cos(pi/5), and 1 / cos(pi/5)^3 = 1.8885, matching the reported Crouzeix ratio for p = z^3.
- Scope, as the report says: this challenge is support material (Toeplitz-Hausdorff, spectral inclusion,
  finite compression, the H = 0 case). The headline claim, Crouzeix with constant 2 on Hilbert space, is the
  separate challenge CrouzeixHilbert, not audited here.
