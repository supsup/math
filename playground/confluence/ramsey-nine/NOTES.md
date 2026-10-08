# EuclideanRamseyNine — verification notes (2026-10-08)

Target: `lean/ComparatorChallenges/EuclideanRamseyNine.lean`, theorem
`OAI.EuclideanRamsey.NineStatement.nine_circle_configuration`, solution module
`OAI.Combinatorics.EuclideanRamsey.NineStatement` (16-module, Mathlib-only cone).
Paper (context only): `preprints/A-classification-of-finite-Euclidean-Ramsey-configurations-September-23-2026/`,
Proposition `cons:nine` in `build/sections/07-consequences.tex`.

## The statement in plain words

Let t_0..t_8 be nine real numbers that are algebraically independent over Q. Put point i at
((1 - t_i^2)/(1 + t_i^2), 2 t_i/(1 + t_i^2)) in the plane. Then
1. the nine points are pairwise distinct,
2. each is at distance 1 from the origin (they lie on the unit circle), and
3. the configuration is NOT Ramsey: there is a number of colours r >= 2 such that for EVERY dimension
   D >= 1 there is a colouring of R^D with r colours containing no monochromatic congruent copy of the
   nine points.

So: some nine-point subsets of a circle (a spherical set) are not Euclidean-Ramsey.

## Definitions audit

| Definition | Reading | Trap check |
|---|---|---|
| `Space d := EuclideanSpace ℝ (Fin d)` | R^d with the Euclidean (L2) metric | `dist` is the Euclidean distance, not sup-norm (it is `EuclideanSpace`, i.e. `PiLp 2`). |
| `Congruent a b := ∀ i j, dist (b i) (b j) = dist (a i) (a j)` | b is a labelled copy of a with all pairwise distances preserved, in any dimension D | Standard: a finite distance-preserving map extends to an isometry. Not stronger (no same-dimension or orientation requirement), so `¬Ramsey` is not weakened by an over-strict notion of copy. |
| `Ramsey a := ∀ r ≥ 2, ∃ D ≥ 1, ∀ c : Space D → Fin r, ∃ b, Congruent a b ∧ ∃ k, ∀ i, c (b i) = k` | The standard Erdős–Graham–Montgomery–Rothschild–Spencer–Straus definition: for every number of colours there is a dimension where every colouring has a monochromatic congruent copy | Quantifiers are in the right order (r, then D, then all colourings c, then a copy). Colourings are arbitrary functions (no measurability), as in the classical definition. No sSup/sInf, no ℕ-valued extremum. `r ≥ 2` and `D ≥ 1` are harmless (r = 1 is trivially Ramsey anyway). Its negation is the strong claim stated above. |
| `literalCircleConfig t i` | the stereographic/rational parametrization of the unit circle | `1 + t^2 ≥ 1` on ℝ, so Lean's `x/0 = 0` convention never bites. |
| hypothesis `AlgebraicIndependent ℚ t` | the nine reals satisfy no nonzero rational polynomial relation | NOT vacuous: ℝ has uncountable transcendence degree over ℚ, so such t exist (by cardinality; no explicit nine are known to be provably independent). It also forces t injective, which is how conjunct 1 is proved. |

`statement_match.py EuclideanRamseyNine`: challenge declarations 5, identical 5, differ 0, missing 0
(202 solution-only helpers). Note the matcher keys on SHORT names and the cone has two
`nine_circle_configuration` theorems (in `Nine.lean`, stated for `circleConfig`, and in
`NineStatement.lean`, for `literalCircleConfig`); the later one in sorted module order, `NineStatement`,
is the one compared, which is the right one. The match being 5/5 confirms it (the `Nine.lean` statement
mentions `circleConfig` and would have differed).

## How the Lean proof goes (read, not re-proved)

1. `NineGeometry`: points on the circle; injectivity via t = y/(1+x); any 5 distinct circle points span
   the plane affinely.
2. `TensorDescent.ramsey_fieldCriterion` (the deep step, the paper's classification, necessity
   direction): a Ramsey configuration spanning R^d admits a `FieldCriterion` witness P, a 3x3 matrix
   over F ⊗_Q F (F = coordinate field) with sum_{α,β} (ã_iα ⊗ 1) P_αβ (1 ⊗ ã_iβ) = 0 for every point i
   (ã = augmented coordinates (1, x, y)) and multiply(P_spatial) = identity.
3. `NineField`: algebraic independence identifies F with Q(t_1..t_9), and F ⊗ F embeds injectively into
   Q(T_1..T_9, U_1..U_9) (left copy -> T, right copy -> U).
4. `NineRational` / `NineGrid`: the 9x9 matrix with rows (p_α(T_i) p_β(U_i)) has nonzero determinant,
   shown by clearing denominators and evaluating at the grid T_(a,b) = g[a], U_(a,b) = g[b],
   g = (0, 1, -1), where it is C ⊗ C with det C = 8, so det = 8^6.
5. `NineLinearObstruction`: nonzero determinant forces P = 0, contradicting multiply(P_xx) = 1.

## What I checked, and how

### Lean in Docker (`../lean-docker/ramseynine-run.log`)

Serialized under the shared lock, machine-free gate admitted. Lean 4.34.1, Mathlib `d13f23b7`,
16 modules copied, `Build completed successfully (8940 jobs)` (the log's `tail -12` shows the last 11
OAI modules built; the other 5 are earlier in the build). Output:

```
'OAI.EuclideanRamsey.NineStatement.nine_circle_configuration' depends on axioms: [propext, Classical.choice, Quot.sound]
'controlWithSorry' depends on axioms: [sorryAx]
```

Exactly the three permitted axioms; no `sorryAx`; the in-file sorry control shows `sorryAx`, so the
instrument can report an unproved theorem. A grep of the Nine*/Model/TensorDescent files for
`sorry|axiom|admit|native_decide|implemented_by|extern` found nothing.

### Python (`replicate.py`, exact `fractions.Fraction`; sympy is not installed)

`python3 -I replicate.py` -> exit 0. Positive checks:
- (1-t^2)^2 + (2t)^2 = (1+t^2)^2 as coefficient lists `[1,0,2,0,1]` both sides; x^2+y^2 = 1 exactly at
  200 random rationals.
- t = y/(1+x) exactly at 200 random rationals; 1+x = 2/(1+t^2) > 0.
- t = 0, 1, -1 are not collinear (2*area = 2).
- Grid certificate built FROM THE DEFINITION of E (not via the Kronecker rule): C = [[1,1,0],[2,0,2],[2,0,-2]],
  det C = 8, E(grid) = C ⊗ C entrywise, det E(grid) = 262144 = 8^6.
- Paper cross-check: the paper uses the uncleared matrix, C' with det 2 and det = 2^6 = 64; I get
  det C' = 2, det M(grid) = 64, and 64 · 4^6 = 8^6 (the row denominators at the grid multiply to 4^6),
  so the paper's 64 and Lean's 8^6 are the same fact.
- 20/20 random independent rational (T, U) in Q^18 give det M != 0, and det E = ∏(1+T_i^2)(1+U_i^2) · det M
  at every one (the `cleared_matrix` lemma).

### Java (`../java/src/confluence/math/ramseynine/RamseyNine.java`, BigInteger rationals)

Same checks and controls, independent code; all PASS, det E(grid) = 262144, 20/20 nonzero, U = T rank 5.

## Controls (must come out singular; all did, in both Python and Java)

- **C1, no tensor independence (U = T).** det = 0, rank 5 (of 9). The circle equation
  P = diag(-1, 1, 1) (i.e. x·x + y·y − 1·1) is an explicit kernel vector that also satisfies the spatial
  condition. This is the field-criterion witness that EXISTS when the two tensor factors collapse (e.g.
  rational parameters, where Q ⊗ Q = Q); it shows the obstruction lives in the tensor square, not in F.
- **C1b.** The same vector is not in the kernel once T, U are independent (row-0 residual -1352/725
  in Python, -3025/4033 in Java; same seed, different RNG implementations, so different random points).
- **C2, repeated parameter** (t_1 = t_0): det = 0 (duplicate rows).
- **C3, perturbed grid** (0, 1, 1): det C = 0 and det E = 0, so the evaluation certificate dies.
- **C4, drop a point:** 8 points give an 8x9 system of rank 8 with a nonzero kernel; the determinant
  argument says nothing about eight points (this does NOT show eight such points are Ramsey).

## LIMITS / could not determine

- **The deep step is Lean-only.** `ramsey_fieldCriterion` (Ramsey ⇒ field criterion) is the paper's
  classification theorem; I did not re-derive it. My computations check only the circle facts and the
  determinant certificate that feeds the obstruction. Trust in the non-Ramsey conclusion rests on the
  Lean build plus `#print axioms`.
- **This is not the official Comparator check.** It is compile + `#print axioms` + a textual statement
  comparison. Comparator compares compiled terms and runs a kernel export in a sandbox; I did not run it.
- **No explicit instance.** No nine reals are known to be provably algebraically independent, so the
  configuration cannot be computed; random rationals stand in for the 18 independent tensor variables
  T, U only (that is exactly the field the Lean proof embeds into). Non-vacuity of the hypothesis is a
  cardinality argument, not something checked here or (as far as I looked) in the Lean files.
- **Random-point det checks are evidence, not proof** that the rational function is nonzero; the
  proof-grade fact is the single grid evaluation 8^6 != 0, which I reproduced exactly.
- **Novelty context (from the paper, unverified):** the paper says Pálvölgyi's earlier generic
  seven-point claim already implies this non-Ramsey conclusion and presents the nine-point determinant
  as an illustration of the classification. I did not check the literature.
