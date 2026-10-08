# CrouzeixHilbert: statement audit and checks

Challenge: `lean/ComparatorChallenges/CrouzeixHilbert.lean`, theorem `OAI.CrouzeixHilbert.hilbert`,
solution module `OAI.Analysis.Crouzeix.Main` (90 modules, Mathlib only). `lean/docs/325.md` says it
is "Complete sharp Crouzeix theorem on arbitrary Hilbert spaces". Its source papers are the two
September 2026 preprints listed there.

**A correction to the brief.** This challenge does NOT use the HilbertCrouzeix support definitions
(`normSup` with `if S.Nonempty`, `chosenContour := Classical.epsilon …`, `holomorphicCalculus`).
It has its own definitions: `supNorm`, `CalculusContour`, `contourEval` and `holomorphicEval`.
They are audited below.

## Statement in plain words

Let H be a complex Hilbert space (`InnerProductSpace ℂ H`, `CompleteSpace H`, no separability) and A a
bounded operator. W(A) = {⟪x, A x⟫ : ‖x‖ = 1}. Mathlib's inner product is conjugate-linear in the first
slot, so this is x*Ax. The theorem has three parts.

- **H nontrivial ⇒ NonzeroConclusion A.**
  - closure W is compact and convex, and contains the spectrum.
  - **Complete polynomial Crouzeix with constant 2.** For every m ≥ 1, every degree d, and all
    matrix coefficients B_k ∈ M_m(ℂ): ‖Σ_k A^k ⊗ B_k‖ ≤ 2 · sup_{z∈W} ‖Σ_k z^k B_k‖. The left side is
    the operator norm on the Hilbert tensor product H ⊗̂ ℂ^m. The right side uses the matrix L2
    operator norm. The sup over W equals the sup over closure W, and the latter is attained.
  - **The same bound for holomorphic matrix functions.** Take any open U ⊇ closure W and any F
    holomorphic entrywise on U. A calculus contour exists. The Dunford integral does not depend on
    which contour is used. ‖F(A)‖ ≤ 2 · sup_{closure W} ‖F‖, and that sup is attained.
  - **The same bound for rational matrices** whose denominators have no zeros on closure W. The
    denominators evaluated at A are invertible, the bound holds, and the rational calculus agrees
    with the holomorphic calculus.
- **H = 0 ⇒ ZeroConclusion A.** W = ∅ and everything is 0, so each bound reads 0 ≤ 0.
- **SharpConstant.** There exist A on ℂ² and a degree-1 scalar polynomial with sup_W |p| = 1 and
  ‖p(A)‖ = 2. So the constant 2 cannot be lowered.

## Audit verdict

**This is the complete Crouzeix conjecture, constant 2, for all bounded operators on Hilbert space,
together with sharpness.** It is at least as strong as the conjecture. The m = 1 case is the scalar
conjecture for polynomials. Because the polynomial case is proved for all m, the bound is also the
complete (cb) version. I found no junk value or vacuous hypothesis that makes any of the bounds
trivially true. As of my knowledge, the constant 2 is OPEN; the best known constant is 1 + √2
(Crouzeix–Palencia 2017, which is also completely bounded). So a kernel-checked proof of this
statement would settle a well-known open problem. I did not assess the mathematics of the proof.
The Lean kernel did check it (see below).

Traps checked, with the Lean that decides each one:

- **Norms.** The scope is `open scoped TensorProduct Matrix.Norms.L2Operator`. I probed instance
  resolution in the same Mathlib, in Docker, with `#synth`:
  - `NormedAddCommGroup (H ⊗[ℂ] EuclideanSpace ℂ (Fin m))` resolves to `TensorProduct.instNormedAddCommGroup`.
  - `InnerProductSpace ℂ (H ⊗[ℂ] …)` resolves to `TensorProduct.instInnerProductSpace`. Mathlib has
    `TensorProduct.inner_tmul : ⟪x⊗y, x'⊗y'⟫ = ⟪x,x'⟫⟪y,y'⟫` and `TensorProduct.norm_tmul`.
  - The completion carries `UniformSpace.Completion.instNormedAddCommGroup`.
  - `NormedAddCommGroup (Matrix (Fin m) (Fin m) ℂ)` resolves to `Matrix.instL2OpNormedAddCommGroup`,
    and `Matrix.cstar_norm_def : ‖A‖ = ‖toEuclideanCLM A‖`.

  So the left side is the honest operator norm on H ⊗̂ ℂ^m ≅ H^m, and the right side is the L2
  operator norm on matrices. The solution also proves (`Amplification.lean`,
  `norm_matrixAmplificationCoordinates`) that ℂ^n ⊗̂ ℂ^m is isometric to `EuclideanSpace ℂ (Fin n × Fin m)`.
- **`supNorm S F = sSup (insert 0 ((fun z => ‖F z‖) '' S))`.**
  - On an unbounded image, sSup would be the junk value 0, and that would make a bound FALSE, not
    trivially true, because the left side is ≥ 0.
  - W is bounded by ‖A‖. Polynomials, and F continuous on the compact set closure W, give bounded
    images, so supNorm is the real sup.
  - The `insert 0` only matters when S = ∅, which is the H = 0 case.
  - The statement also asserts that the sup is attained at a point z of closure W.
- **Contour and Dunford calculus.**
  - `holomorphicEval A U f` is defined as `if h : Nonempty (CalculusContour (numericalClosure A) U)
    then contourEval A (Classical.choice h).toSmoothContour f else 0`.
  - The junk branch, 0, is excluded because the conclusion **asserts** `Nonempty (CalculusContour …)`.
    It also asserts `∀ Γ, holomorphicEval A U f = contourEval A Γ f`, so the choice of contour is
    irrelevant.
  - A `CalculusContour K U` is a C¹ closed path whose image (for t ∈ [0,1]) lies in U \ K. It has
    winding index 1 at every point of K and 0 at every point outside U. This is exactly the
    Riesz–Dunford hypothesis, since σ(A) ⊆ K is also asserted. Such a contour always exists when K
    is convex and compact and U ⊇ K is open: take a smoothed boundary of K + εD.
  - `contourEval` integrates `(γ' f(γ)) • Ring.inverse(γ − A)`. On the path γ ∉ K ⊇ σ(A), so
    `Ring.inverse` is the true resolvent. The integrand is continuous on [0,1], so the interval
    integral is not the non-integrable junk value 0.
  - Polynomials go through this calculus: `matrixHolomorphicEval_matrixPolynomial` in
    `CompleteFinite.lean`.
- **Rational calculus.** `rationalEval` uses `num(A) * Ring.inverse(denom(A))`, which would be junk 0
  for a non-unit. The conclusion asserts `IsUnit (aeval A denom)` under `PolesOutside`, so no junk
  appears. `RatFunc.num` and `RatFunc.denom` are coprime, so the denominator's zeros are the true
  poles.
- **Hypotheses.** The hypotheses are `CompleteSpace H`, `Nontrivial H` (on that branch) and `0 < m`.
  None of them is vacuous. f ranges over polynomials with arbitrary matrix coefficients, over every
  F holomorphic near closure W, and over rational matrices with poles off closure W.
- **SharpConstant is not trivial.** It needs the true norms. J2 = [[0,1],[0,0]] with B = (0, 2), so
  p(z) = 2z, gives sup_W |2z| = 2 · ½ = 1 and ‖2 J2‖ = 2. The Python and Java checks reproduce this
  exactly. The witness only shows that 2 is attained for m = 1 and d = 1, but that is what
  sharpness requires.

## Lean (Docker, Mathlib only)

Log: `playground/confluence/lean-docker/crouzeixhilbert-run.log`. The run used Lean 4.34.1 and Mathlib
d13f23b7. All 90 modules were copied and built ("Build completed successfully (9014 jobs)").

```
'OAI.CrouzeixHilbert.hilbert' depends on axioms: [propext, Classical.choice, Quot.sound]
'controlWithSorry' depends on axioms: [sorryAx]     <- harness control: a sorry IS detected
```

- I grepped the solution for `sorry`, `admit`, `axiom`, `set_option` (none at all), `implemented_by`,
  `extern`, `unsafe`, `native_decide`, `macro`, `elab`, `syntax`, `notation` and `opaque`, and found
  no hits.
- The only local instances are `Fact (0 < 1)` and real-normed-space and completeness instances on
  operator spaces. They sit in later modules and cannot reach `Definitions.lean`.

`statement_match.py CrouzeixHilbert` reported 25 challenge declarations: 25 identical, 0 differing, 0
missing, and 1024 solution-only helpers. The 25 are every definition plus the theorem.
`Definitions.lean` imports only Mathlib and has the same `open scoped` line as the challenge. Its body
from `def numericalRange` to the end of the namespace is byte-identical to the challenge (checked
with `diff`). The definitions therefore elaborate in the same context.

## Numerical checks (numpy 2.0.2, JDK 25), all finite-dimensional

`crouzeix_check.py` (output in `crouzeix_check.out`, overall PASS):

- **Method.** The boundary of W comes from the top eigenvector of Re(e^{-it}A), over 4096 angles.
  These points lie on W, so the sampled max is ≤ the true max and each reported ratio is ≥ the true
  ratio. The sampling therefore errs toward finding a violation, not hiding one.
- **Scalar polynomials.** Ratios are 2.000000000000 for J2 with p = z and for J3 with p = z², which
  are extremal. J4 with z³ gives 1.8885 (= 1/cos³(π/5)), and [[0,5],[0,0.3]] with z gives 1.887. The
  max over 400 random (3×3, cubic) pairs was 1.168. The J2 boundary radius is 0.5 to 1e-15.
- **Matrix-valued, the complete version.** The max over 200 random (3×3 A, 2×2-coefficient
  quadratic) pairs was 1.496. J2 with B1 = E12 gives 2.000.
- **Rational 1/(z−c), c off W.** All ratios were ≤ 0.86.
- **Dunford integral.** I integrated over ∂(W + 0.25·D) with a midpoint rule on 8192 points. The
  winding number about each eigenvalue was 1. For p = 1 + 2z − z³, for 1/(z − c) with the pole
  outside the contour, and for exp, the relative error against direct evaluation was ≤ 9e-7 on J2,
  J4, [[1,2],[0,i]] and a random 4×4. So the Dunford calculus agrees with the polynomial and
  rational calculi. Control: the same contour shifted off W gives an integral ≈ 0 (≤ 5e-6), far from
  p(A).

`CrouzeixHilbert.java` (package `confluence.math.crouzeixhilbert`, overall PASS):

- It builds the closed-form 2×2 numerical range, an ellipse with foci at the eigenvalues and minor
  axis √(‖A‖_F² − |λ1|² − |λ2|²). It checks that 200000 random x*Ax values fall inside it (level
  ≤ 1). The degenerate normal case has b = 0 and the check is skipped there.
- It uses the closed-form 2×2 spectral norm. Ratios for 4 polynomials on 5 matrices are all ≤ 2.
  The SharpConstant witness gives exactly 2.000000000.

## Negative controls (each must fail, and each does)

- **W replaced by conv(spectrum).** For J2, J4 and J8, p = z: sup over {0} is 0 and ‖J_n‖ = 1, so
  the ratio is ∞. This holds in both Python and Java.
- **Constant 2 replaced by 1.9.** J2 with p = z gives ratio 2 > 1.9, which FAILS in both Python and
  Java.
- **Contour not enclosing W.** The Dunford integral is ≈ 0 ≠ p(A).

## LIMITS / could not determine

- **The proof's mathematics was not reviewed.** It is 15.6k lines and goes through a similarity S
  with ‖S‖‖S⁻¹‖ ≤ 2 and a positive operator-valued boundary density (`exists_conformal_contraction`,
  `holomorphic_bound` in `CompleteFinite.lean`), then extends to Hilbert space by finite
  compression. My only evidence of correctness is the Lean kernel accepting it with standard axioms.
  Given that this would resolve a known open problem, expert human review and an independent run of
  the real Comparator (term-level comparison, not our textual match) are warranted before anyone
  believes it.
- **The statement match is textual.** It is backed by the byte-identical body and the identical
  import and `open` context. Comparator was not run.
- **The instance identification rests on `#synth` names and the lemmas beside them.** I did not
  `#print` the full instance terms. The isometry `norm_matrixAmplificationCoordinates` (finite
  dimensions) is kernel-checked evidence that the tensor norm is the Hilbert one.
- **The numerics are finite-dimensional examples.** They cannot test infinite-dimensional H, and a
  few hundred random cases are no evidence for the conjecture. Extensive published searches, such as
  Greenbaum–Overton's, have also never found a ratio above 2. Crouzeix's conjecture is already known
  for 2×2 matrices, so the Java 2×2 checks test the code and not the theorem.
- **The open-problem status comes from my knowledge (cutoff mid-2026).** The September 2026 preprints
  postdate it, and I did not read them.
- **Probe incident.** For the `#synth` probe I ran `lake env lean` against a read-only mount of the
  `confluence-lean-math` volume. Lake printed "mathlib: URL has changed; deleting
  '/work/challenge-CrouzeixHilbert/.lake/packages/mathlib' and cloning again". The read-only mount
  refused (error 30), so nothing was deleted. I then ran `lean` directly with `LEAN_PATH`. Do not
  run `lake env` on that directory with the volume mounted read-write unless a re-clone is acceptable.

## Confluence's recheck

- Read the challenge's own definitions (lines 26-27, 52-66, 96-107), not the sibling HilbertCrouzeix ones:
  `holomorphicEval` is `if h : Nonempty (CalculusContour (numericalClosure A) U) then contourEval A (choice h) f else 0`,
  and NonzeroConclusion ASSERTS `Nonempty (CalculusContour (numericalClosure A) U)` and that every such contour
  gives the same value, so the junk `else 0` branch cannot carry the bound. `CalculusContour` requires the path
  in U minus the closed numerical range, winding index 1 on it and 0 outside U: a genuine Riesz-Dunford contour.
  The bounds are `‖·‖ ≤ 2 * supNorm (...)` with `supNorm S F = sSup (insert 0 (‖F‖ '' S))` over compact sets.
- Build log: `Build completed successfully (9014 jobs)`; `hilbert` on [propext, Classical.choice, Quot.sound];
  sorry control on [sorryAx].
- The probe incident (lake wanting to re-clone mathlib on a read-only mount) did no damage: the volume's
  challenge-CrouzeixHilbert mathlib package is intact (23 entries, build/lib present).
- Caption level, as agreed for log-BM (undervoice 16053-16057): "the collection's Lean artifact kernel-checks
  this formal statement", not "Crouzeix's conjecture is proved", until a second independent statement reading,
  a reproducible replay and broader proof review.

## Correction (2026-10-08, after Fixpoint's source sweep, undervoice 16187)

The statements above and in my undervoice 16068 that "the best published constant is 1 + sqrt 2" were STALE (my
knowledge ends before August 2026). Lorist and Schwenninger posted an independent proof of Crouzeix's conjecture
with constant 2 for matrices on 2026-08-04 (arXiv 2608.03841; arXiv id confirmed by Fixpoint, not by me). The
collection's claim is the COMPLETE version: matrix-valued coefficients, for every bounded operator on any complex
Hilbert space, plus sharpness. The statement audit and the kernel check above are unaffected; only the novelty
framing changes.
