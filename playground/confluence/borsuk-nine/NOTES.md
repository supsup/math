# Borsuk's conjecture fails in dimension nine: statement audit and checks

Lean: `lean/ComparatorChallenges/BorsukNine.lean` (statement, proof `sorry`). The `.json` names solution module
`OAI.Geometry.Borsuk.Main` and theorem `OAI.BorsukNine.main_theorem`. The cone is 269 modules, Mathlib-only,
about 79,000 lines, mostly 145 generated `FiniteCases` files, with no `native_decide`.
Docs: `lean/docs/156.md`. Paper: `preprints/A-nine-dimensional-counterexample-to-Borsuks-covering-assertion-September-23-2026/`.

## What it says, in plain words

Borsuk (1933) asked whether every bounded set in R^d can be cut into d + 1 pieces of strictly smaller
diameter. The theorem takes the set X of all rank-one projectors u u^T, for u a unit vector in R^4. This is
the real projective 3-space, embedded by u -> u u^T, with the Frobenius metric. X lives in the trace-one
symmetric 4x4 matrices, a 9-dimensional affine space. It has diameter sqrt 2, and ten pieces of smaller
diameter cannot cover it. So 10 = d + 1 pieces are not enough in dimension 9: a **counterexample** to
Borsuk's assertion in dimension nine.

The paper's prior-art list ends at dimension 63 (Grinsztajn 2026, a public proof note), after 64
(Jenrich and Brouwer 2014) and 65 (Bondarenko 2014). As of my knowledge (training data to June 2026) the
record was 64. I cannot confirm the 63 note or whether dimension 9 is new. **A novelty check is owed before
any card calls it new.**

## Audit verdict

**Matches its name and its Scope.** The conclusion is a NEGATION (`¬ HasTenSmallCover`), so the risk
direction flips. The theorem would be cheap if the definition of a cover were too STRONG, that is, if it
asked for more than Borsuk's covering does and so could never be met. I checked each part for that:

- **The pieces.** `C : Fin 10 → Set Matrix4`, with each `C i ⊆ projectorSet` and their union covering
  `projectorSet`. Exactly ten sets, any of them possibly empty, so "at most ten". Overlaps are allowed,
  and the paper notes that covers and partitions give the same number. This is the standard covering
  notion and asks nothing extra.
- **Small diameter.** `Metric.diam (C i) < Real.sqrt 2`. Mathlib's `Metric.diam` is 0 for an UNBOUNDED
  set, which would make a cover TRIVIALLY small and the negation FALSE. That cannot happen here, because
  every `C i` is a subset of the compact `projectorSet`. So `Metric.diam` is the true supremum of
  distances. The inequality is strict, as Borsuk's question requires.
- **The metric.** `Matrix4 := EuclideanSpace ℝ (Fin 4 × Fin 4)`, so the norm is the l2 norm of the 16
  entries, which is the Frobenius norm.
- **The set.** `projector u = fun ij => u ij.1 * u ij.2` is u u^T, and `projectorSet` is its image on the
  unit sphere.
- **The other three conjuncts** are not decoration:
  - `IsCompact projectorSet` makes it a bounded (indeed compact) set, as Borsuk requires.
  - `projectorSet ⊆ traceOneSymmetric` is what puts it in nine dimensions.
  - `Metric.diam projectorSet = Real.sqrt 2` pins the scale against which "smaller" is measured.
- **The dimension count is the reader's job.** The Lean only says the set lies in `traceOneSymmetric`.
  Symmetric 4x4 matrices form a 10-dimensional space, and trace one removes one dimension, leaving 9. The
  Java and Python checks below also measure the affine SPAN of the projectors: exactly 9. So the set is
  isometric to a subset of R^9, which is what "dimension nine" means for Borsuk.

**My verdict: MATCHES (first reading, Confluence).** A second independent reader is still owed before the
trust table carries the row.

## Checks run

| Check | Result |
|---|---|
| Docker build, 9,193 jobs, Lean 4.34.1, Mathlib d13f23b7 | built |
| `#print axioms OAI.BorsukNine.main_theorem` | `[propext, Classical.choice, Quot.sound]`, permitted only |
| sorry control in the same run | `controlWithSorry` depends on `[sorryAx]`, so the instrument detects a sorry |
| `statement_match.py BorsukNine` | 7 challenge declarations, 7 identical, 0 differ, 0 missing; 4,789 solution-only helpers |
| distance identity, 20,000 random pairs (Python and Java) | max error about 2e-15 for `2 - 2<u,v>^2`; the wrong `2 - 2|<u,v>|` refuted |
| affine span dimension (Python and Java) | 9 |
| Peres' 24 rays: fewest pieces of diameter < sqrt 2 | 5 (Java search, plus independent Python: 4 fails, a valid 5-colouring exists) |

Log: `lean-docker/borsuk-run.log`.

## The method, as the paper states it (not checked by me)

The paper's argument is topological, not a finite colouring. A ten-set cover would yield a
structure that behaves enough like a triangulation of RP^3 to hit Walkup's 11-vertex minimum (1970). The
paper derives that structure from an odd map on symmetric matrices, mod-two degree and local preimage
counts, and then finishes with a finite combinatorial obstruction. Those are the 145 kernel-checked
`FiniteCases`. My first guess, an orthogonality-graph colouring, was wrong as a description of the proof.

Why a finite configuration is not enough, measured: on a FINITE set of lines, a piece has diameter below
sqrt 2 exactly when it holds no orthogonal pair, so the fewest small pieces is the chromatic number of the
orthogonality graph. For Peres' 24 Kochen-Specker rays that number is 5, far from 11. The continuum is
doing the work.

## Java

`java/src/confluence/math/borsuk/BorsukNine.java`, 12 checks plus controls, all pass.

## Open

- Second reader for the trust table.
- A novelty check against the literature after June 2026 (the 63 note, and anything citing this result).
- The paper says the exact value of b(X) and the smallest failing dimension remain open.
