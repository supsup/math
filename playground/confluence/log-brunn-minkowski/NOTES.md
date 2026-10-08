# LogBrunnMinkowski: statement audit and replication (2026-10-08)

Challenge: `lean/ComparatorChallenges/LogBrunnMinkowski.lean` (+ `.json`), theorem `OAI.LogBrunnMinkowski.main`.
Solution: ONE module, `lean/OAI/Geometry/LogVolume/BrunnMinkowski.lean` (24,490 lines, `import Mathlib` only).
Paper (context only): `preprints/The-logarithmic-Brunn-Minkowski-conjecture-September-23-2026/`, linked from `lean/docs/091.md`.

## The statement in plain words

For every dimension n >= 1, all origin-symmetric convex bodies K, L in R^n (compact, convex, nonempty
interior, `x in K iff -x in K`) and every t in [0,1]:

    vol(K)^(1-t) * vol(L)^t  <=  vol( W[ h_K^(1-t) * h_L^t ] ),

where `h_K(u) = sSup { <x,u> : x in K }` and `W[f] = { x : <x,u> <= f(u) for all u with |u| = 1 }`.

## Relation to the classical conjecture: it IS the full origin-symmetric conjecture

Compared against Boroczky, Lutwak, Yang, Zhang, "The log-Brunn-Minkowski inequality", Adv. Math. 231 (2012)
1974-1997, Problem/Conjecture 1.1: for origin-symmetric convex bodies K, L in R^n and 0 <= lambda <= 1,
`|(1-lambda)K +_0 lambda L| >= |K|^(1-lambda) |L|^lambda`, where the L_0 (log) combination is
`∩_{u in S^{n-1}} {x : <x,u> <= h_K(u)^(1-lambda) h_L(u)^lambda}`. The Lean statement is that, term for term:
same class of bodies, all n, all lambda, same combination, Lebesgue volume. It is not a special case (no
planarity, no unconditionality, no smoothness, no closeness to the ball). To my knowledge it was open for
n >= 3 (proved: n = 2 by BLYZ 2012; unconditional bodies, Saroglou 2015; local/near-ball results by
Colesanti-Livshyts-Marsiglietti, Kolesnikov-Milman, Chen-Huang-Li-Liu; the paper itself cites a 2018 Stancu
announcement with deferred details). My knowledge of the literature is not verified here.

The symmetric restriction is the conjecture's own (log-BM is false for general bodies containing the origin;
see control 1 below), not a weakening.

## Definitions audit

| Item | Finding |
|---|---|
| `IsConvexBody` | `IsCompact ∧ Convex ℝ ∧ (interior K).Nonempty`: the standard definition. Nonempty, so no `sSup ∅ = 0`. |
| `OriginSymmetric` | `∀ x, x ∈ K ↔ -x ∈ K`: standard. With convexity and nonempty interior it puts 0 in the interior (midpoint of x and -x for an interior x), so `h_K(u) >= r > 0` on the unit sphere. |
| `support` | `sSup` of the image of a compact nonempty set: bounded above, attained; equals the classical max. No empty/unbounded `sSup`. |
| powers | `(support K u) ^ (1 - t)` is `Real.rpow` with a strictly positive base on unit u (the only u `wulff` reads), so no negative-base or `0^0` quirk matters. Off the sphere f is junk but unread. |
| `wulff` | quantifies over `‖u‖ = 1` exactly; for n >= 1 the sphere is nonempty, so no vacuous `univ`. |
| `volume` | the `MeasureSpace` instance on `EuclideanSpace ℝ (Fin n)` (Lebesgue / additive Haar). Even an unnormalized Haar measure c·Lebesgue would not matter: both sides scale by c^(1-t)·c^t = c. Outer measure is applied to the Wulff set, which is closed anyway. |
| `(volume K) ^ (1-t)` | `ENNReal` rpow; vol K is finite (compact) and positive (interior), so no `∞`/`0` edge. At t = 0, `x^0 = 1`. |
| `hn : 1 ≤ n` | excludes the degenerate n = 0 point space. n = 1 is the (true, equality) symmetric-interval case; the solution handles it separately (`main_dimension_one ... .ge`). |
| division, truncation | none in the statement. No `ℕ`/`ℝ` coercion on any quantity that matters. |

Nothing vacuous, nothing weaker than its name that I could find.

## Lean check (Docker, `playground/confluence/lean-docker/logbm-run.log`)

Cone: 1 module, Mathlib only. Build: `Built OAI.Geometry.LogVolume.BrunnMinkowski (152s)`, no errors, no `sorry`
warning from the solution. The file contains no `axiom`, `set_option`, `implemented_by`, `extern`, `unsafe`, or
`open Lean` metaprogramming (grep).

    'OAI.LogBrunnMinkowski.main' depends on axioms: [propext, Classical.choice, Quot.sound]
    'controlWithSorry' depends on axioms: [sorryAx]

Exactly the three permitted axioms; the sorry control shows the instrument can report an unproved theorem.

### statement_match

`statement_match.py LogBrunnMinkowski`: 7 challenge declarations, 4 identical, 3 "differ". All 3 are the
matcher's mistakes, not real differences:
- `support`, `logCombination`: the solution adds the `noncomputable` keyword (the challenge gets it from
  `noncomputable section`). Text otherwise identical.
- `Space`: the matcher keys on short names, and the solution file has four OTHER `abbrev Space (ι : Type*) := ι → ℝ`
  in other namespaces (`MatrixOperator`, `MomentCoordinates`, `DensityEnergy`, `EvenClosure`, lines 12945+); one
  overwrote the right one. The solution's `OAI.LogBrunnMinkowski.Space` (line 15) is `EuclideanSpace ℝ (Fin n)`.
- Independent check: the whole challenge block from `abbrev Space` to before `theorem main` equals the
  solution's first `namespace LogBrunnMinkowski` block after whitespace normalization and deleting
  `noncomputable `; and the `theorem main` statement (up to `:= by`) is character-identical after whitespace
  normalization. The theorem is in `namespace OAI.LogBrunnMinkowski` (reopened at line 24464, inside the
  file's single `namespace OAI`), and the name printed by `#print axioms` is the full name.

## Independent computations (`logbm_check.py`, output `logbm_check.out`; Java `confluence.math.logbm.LogBrunnMinkowski`)

Method (plane): keep N sampled constraint directions; the resulting polygon A_N CONTAINS the Wulff body and is
computed exactly as the polar of conv{u_j / f(u_j)}. A Lipschitz argument (h_K is R_K-Lipschitz, f >= m_f,
`W[f+eps] ⊆ (1+eps/m_f) W[f]`) turns area(A_N) into a proved LOWER bound on vol W, modulo double rounding.
A case "passes" only if that lower bound reaches the left side.

- 10 symmetric planar pairs (squares vs rotated squares, rectangle vs rotated, square vs hexagon, thin
  rectangles at 60 degrees, 6 random symmetric polygons): all PASS with proved margins from 0.2% to 17%.
  Python and Java agree to the printed 6 digits on the shared deterministic cases.
- Equality cases come out as "NEAR-EQUALITY (not proved)", as they must: common-axis rectangles (W is exactly
  box(a^(1-t) b^t): Hoelder gives inclusion, axis constraints the reverse), t = 0, dilates (W = 3^t K). This is
  the instrument showing it can withhold a pass.
- R^3 (quadrature, NOT a bound): cube vs rotated cube, cube vs octahedron, box vs rotated box all show volume
  ratios 1.17-1.48; common-axis boxes give 0.99999 (equality). Quadrature on f = h_K reproduces vol K to 1e-5
  after adding facet normals to the constraint grid (without them it was 4% high; measured and fixed).

Controls, all FAIL as required (judged on the OUTER area, which over-estimates the true volume):
1. Non-symmetric: square vs the same square shifted by (0.95, 0.95) (origin still interior, so all powers are
   defined): vol W <= 2.6245 < 4 = LHS. 3D analogue: ratio 0.53. So the symmetry hypothesis is load-bearing.
2. Wrong combination `W[min(h_K, h_L)] = K ∩ L`: 0.25 < 1.

## LIMITS / could not determine

- I did NOT verify the mathematics of the 24k-line proof. The evidence that it is a proof is: the Lean kernel
  accepted the module under `lake build` against the pinned Mathlib, with only the standard axioms. This is not the
  official `leanprover/comparator` run (compiled-term comparison, sandboxed kernel export); the JSON sets
  `enable_nanoda: false`, and I ran no second kernel checker. Trust therefore rests on Lean 4.34.1's kernel,
  Mathlib at the pinned rev, and the textual statement match above.
- Given that, the honest reading: either this is a formally verified resolution of the origin-symmetric
  log-Brunn-Minkowski conjecture in all dimensions (extraordinary, and it would also give the symmetric L_p
  BM inequality for 0 < p < 1 and, via Saroglou, the B-conjecture, per the paper), or there is a soundness issue
  in the toolchain that my checks cannot see. I found no statement-level loophole.
- Numerics are checks of instances, not of the theorem; floats are not interval-controlled; R^3 checks are
  quadrature only. Literature status ("open for n >= 3") is from my own knowledge, not checked here.
- I did not read the paper's argument beyond the introduction.

## Confluence's recheck

- Read `lean/ComparatorChallenges/LogBrunnMinkowski.lean` myself: origin-symmetric convex bodies (compact,
  convex, nonempty interior, x in K iff -x in K) in EuclideanSpace R (Fin n) for every n >= 1, the L_0
  combination as the Wulff body of h_K^(1-t) h_L^t over unit vectors, and volume. That is the
  Boroczky-Lutwak-Yang-Zhang log-Brunn-Minkowski conjecture as posed, not a special case.
- Build log: `main` on [propext, Classical.choice, Quot.sound]; sorry control on [sorryAx].
- My own planar check (half-plane clipping over 20,000 directions, code independent of logbm_check.py):
  square vs its 45 degree rotation, t = 1/2: |K|^(1/2)|L|^(1/2) = 4, log-combination area 4.6863 (ratio
  1.1716, matching the 17% margin reported); t = 1/4: 1.1290; 22.5 degrees: 1.1329; identical squares: 1.0000.
- statement_match now reports 7/7. Its three "differences" were matcher bugs, fixed: (1) one solution FILE
  declares `abbrev Space` five times in different namespaces and the per-file dict kept the last; (2) the
  body of `Space` swallowed the following `variable (...)` line; (3) `noncomputable` on the solution's
  defs, which the challenge inherits from `noncomputable section`. Remaining limit: the matcher still keys
  by short name and accepts ANY same-named candidate, so a namespace-blind match is possible; namespace
  tracking is the follow-up.
- What this does NOT settle: whether the 24,490-line proof is right is the Lean kernel's word alone (no
  second checker, not the official Comparator). For a famous open problem that is the question to keep open.
