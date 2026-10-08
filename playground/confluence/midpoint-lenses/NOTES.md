# Midpoint lenses in segment spaces: one theorem, checked three ways

Lean: `lean/ComparatorChallenges/MidpointLenses.lean` (statement, proof `sorry`), solution module
`OAI.Analysis.SegmentLenses.Main` (an 11-module cone, Mathlib only). Theorem:
`OAI.SegmentLenses.midpoint_lens_main`. Paper: `preprints/Midpoint-lenses-in-segment-spaces-September-27-2026`
(Theorem 1.1, `thm:main-tail`). I read the paper for context only.

## What it says, in my words

Take a rooted tree (or a forest of trees). A *segment* is a run of a root-to-leaf path: all vertices
between an ancestor a and a descendant b. For a finitely supported function u on the vertices, its norm
is the largest value of sqrt(sum of (sum of u over S)^2) over families of pairwise-disjoint segments S.
This is James's tree-space norm. Complete that space (J) and take its dual (X); the coordinate
functionals e_v^* lie in X.

Split a functional into a *head* (its coordinates on a finite set H closed under ancestors) and a
*tail* (everything else). The theorem: if x is all head, and both x + y and x - y have norm at most R,
then the tail of y has norm at most 2 sqrt(R^2 - ||x||^2). If x is close to the edge of the R-ball, a
symmetric displacement y can only move a little outside H. It is proved twice:

1. the forest of trees N^{<=h} of every height h >= 1, in the full dual X = J^*;
2. the infinite tree N^{<omega} (all finite words), in B_inf, the closed span of the coordinates
   inside the dual. The norm there is the dual norm, restricted to that span.

## Definitions audit (each read from the challenge file)

| Definition | What it is | Trap checked | Verdict |
|---|---|---|---|
| `ForestVertex` | pairs (h, w) with 1 <= h and length w <= h | could be empty or finite | fine: the components {h} x N^{<=h}, as in the paper |
| `ForestAncestor` | same h, and w is a prefix | reflexive? | fine: reflexive, so singletons are segments |
| `IsInterval` | exists a <= b with S = {v : a <= v <= b} | is the empty set a segment? | no, a is in S. Chains are finite |
| `Ancestral` | b in H and a <= b imply a in H | H = empty set allowed | fine: then x = 0 and the claim is ‖y‖ <= 2R, which is true |
| `SegmentFamily` | a Finset of segments, pairwise disjoint | empty family | fine: it gives 0 inside a supremum of nonnegative values |
| `test` and `seminorm` | ℓ2 norm of the vector (u(S))_S | is it the sum over S? | yes: the file proves `test_apply` (u(S) = sum over S) and `seminorm_sq` |
| `segmentSeminorm` | iSup of seminorms over all families | an unbounded iSup is junk in Mathlib | bounded (`segmentTests_bdd`, by the ℓ1 norm) and used with `le_ciSup`, so it is the true pointwise supremum |
| `Test V` norm | `segmentSeminorm` | a degenerate norm? | `norm_eq_zero_iff` is proved, through singleton families |
| `coordinate v` | `(evaluation v).extend toComplL` | `extend` returns 0 when its hypotheses fail, which would make `head` = 0 and the theorem VACUOUS | not vacuous: `coordinate_unitVector` (Pairing.lean, compiled in the cone, no sorry) proves coordinate v (e_w) = [v = w] |
| `head` and `tail` | sum over H of x(e_v) e_v^*, and x minus that | | the paper's P_H and Q_H |
| `coordinateSpan` and `BInfinite` | topological closure of the span of the coordinates | | the paper's B_inf. The norm on the subtype is the restricted dual norm |
| `Real.sqrt (R^2 - ‖x‖^2)` | sqrt of a negative number is 0 in Lean | could the radicand be negative? | no: ‖x‖ <= (‖x+y‖ + ‖x-y‖)/2 <= R. Also R >= 0 |

Quantifier order: H comes first, then x, y and R. One H serves every displacement, as the paper says.
I found no ℕ subtraction, no division and no sInf in the statement.

## Reduction to finite dimensions, which every check below relies on

Let T be a finite ancestral vertex set and f a combination of the e_v^* with v in T. Then ‖f‖ in X
(and in B_inf) equals the dual norm on R^T of rho restricted to T. My argument:

- Primal tests are dense, so ‖f‖ = sup over u of f(u)/rho(u).
- f reads only the coordinates in T, so f(u) = f(P_T u).
- rho(P_T u) <= rho(u). A segment [a, b] meets an ancestral T either in nothing or in the segment
  [a, b'], where b' is the deepest vertex of the chain inside T. So disjoint families restrict to
  disjoint families.

Adding segments to a family only adds squares, so rho on T is a maximum over *partitions* of T into
segments. I checked this against brute force over every disjoint family, for rational u on trees of up
to 4 vertices, in both languages. The dual unit ball is then the convex hull of the atoms
sum_{S in P} a_S d_S with ||a||_2 <= 1. This gives two certificates:

- a lower bound: f(u)/rho(u) for any u;
- an upper bound: sum ||z_P||_2 + ||r||_1 for any decomposition f = sum_P A_P^T z_P + r. The residual r
  is paid for with singleton atoms e_v^*, each of norm <= 1.

Finite-support instances are the same in the two models (forest and B_inf), so the numeric checks cover
both parts of the conjunction equally. Neither part is checked anywhere else.

## Checks, with numbers

Run: `python3 replicate.py` from this folder. numpy comes from the user site, so do not use `-I`; numpy
is used in part 3 only. Output is in `run.txt`. Java:
`playground/confluence/java/src/confluence/math/midpointlenses/MidpointLenses.java`.

**1. Exact instance, both languages.** Two vertices (root r, child c), H = {r}, x = (9/10, 0),
y = (1/10, 3/5). Each norm is pinned by a matching lower and upper certificate in rationals. Java
gets lower^2 = upper^2 exactly. Python agrees to 1e-15, the limit of its rational sqrt bounds:

| Norm | Value | Lower certificate (u) | Upper certificate (decomposition) |
|---|---|---|---|
| ‖x‖ | 9/10 | (1, 0) | |
| ‖x+y‖ | 1 | (1, 0) | (1, 3/5) = 2/5·e_r^* + 3/5·d_{rc} |
| ‖x-y‖ | 1 | (4/5, -3/5) | a disk atom with coefficients (4/5, -3/5) |
| ‖Q_H y‖ | 3/5 | | |

With R = 1 the theorem asks 9/25 <= 4·19/100 = 19/25. It holds. The ratio ‖Q_H y‖/sqrt(R^2 - ‖x‖^2) is
sqrt(36/19) = 1.3765. The theorem allows 2.

**2. Closed form for the two-vertex lens** (my derivation, checked by brute force). The dual ball is
B = conv(unit disk, (1,1), (-1,-1)). Its slice at height b in [0,1] is [-sqrt(1-b^2), 1]. For
x = (r, 0) and R = 1 the lens reaches max |y_c| = 1 when r <= 1/2, and 2 sqrt(r(1-r)) when r >= 1/2.
Brute force uses support-function membership over 3600 directions plus a bisection. It matches the
closed form to 1e-5 at r = 0.3, 0.5, 0.6, 0.75, 0.9 and 0.97. The ratio against sqrt(1 - r^2) is
2 sqrt(r/(1+r)), which tends to **sqrt 2 = 1.41421** as r -> 1. So **no constant below sqrt 2 can
replace the theorem's 2**, already for two vertices. The paper says its constants make no optimality
claim, which is consistent with this.

**3. Adversarial search on 15 (tree, H) pairs** (numeric, then certified). The trees are: an edge,
chains of 3 and 4 vertices, a cherry, a Y, a 3-star, a Y with an extra leaf, and two disjoint edges (a
2-component forest). H ranges over the nontrivial ancestral sets.

- Method: a coarse hill climb on x, y, using an IRLS solver for the dual norm, then a refinement with an
  accurate solver. The best instance for each pair is then re-certified in exact rationals.
- Result: all 15 instances are certified to satisfy the theorem.
- Largest certified ratio: 1.41184 (cherry, H = {root}), just below sqrt 2. The certified intervals
  have width <= 1e-4.
- I found no instance above sqrt 2. So in every family I tried, the constant actually needed is about
  sqrt 2, not 2.

**A lesson from part 3, kept on purpose.** The coarse search reported 1.697 on the Y tree in an earlier
run, and 1.43 to 1.445 in the final run. Certification brought these down to 1.20 and 1.36 to 1.40. The
optimizer had been exploiting the approximate solver's error, not the geometry. Only certified numbers
are quoted above.

## Negative controls (each must FAIL, and does)

- **Control A (constant).** Use the same exact instance, with constant 13/10 in place of 2. It needs
  9/25 <= (169/100)(19/100) = 3211/10000, which is false. Python and Java both report FAILS. Part 2
  shows that any constant < sqrt 2 fails near r = 1.
- **Control B (definition).** Replace the ℓ2 of segment sums by ℓ1 (rho_1(u) = max_P sum |u(S)|). On two
  vertices this is the ℓ1 norm, so the dual ball is the square. Take x = e_r^* and y = (1/2) e_c^*: then
  ‖x‖ = 1, ‖x ± y‖ <= 1, and ‖Q_H y‖ = 1/2 > 2·sqrt(0). The claim FAILS. So the "2" in the
  Euclidean space's exponent is load-bearing, and my checker can see a failure.
- **Instrument control.** The IRLS solver reproduces the exact two-vertex norms ‖(1, 0.6)‖ = 1,
  ‖(1, -0.5)‖ = sqrt(1.25), ‖(0.8, -0.6)‖ = 1 and ‖(0, 1)‖ = 1 to 1e-6.

## Picture

`lens.svg` (from `make_svg.py`) has two panels.

- **Left:** the two-vertex dual ball. It is a disk with two opposite square corners filled in, at
  upper-right and lower-left. It shows x = (0.9, 0), x+y = (1, 0.6) on the flat right edge, and
  x−y = (0.8, −0.6) on the circular arc.
- **Right:** the lens (B − x) ∩ (B + x). It is a thin lens-shaped sliver near the vertical axis, with
  its tips at y = (0.1, 0.6) and −y.
  - A green line marks its true height 0.6 = 2 sqrt(r(1−r)).
  - A dashed red line marks the theorem's bound 2 sqrt(1−r²) = 0.872.

The picture shows why the tail is small. The two shifted balls overlap only in a narrow vertical strip.
The strip's height is set by how far x sits from the ball's edge.

## Lean (Docker, 2026-10-08, log `../lean-docker/midpointlenses-run.log`)

- **Build:** all 11 cone modules built against the pinned Mathlib (Lean 4.34.1) and the build succeeded.
  No `sorry` appears in any of the 11 files.
- **Axioms:** `'OAI.SegmentLenses.midpoint_lens_main' depends on axioms: [propext, Classical.choice, Quot.sound]`.
  These are exactly the permitted axioms.
- **Sorry control:** in the same file, `'controlWithSorry' depends on axioms: [sorryAx]`.
- **statement_match.py:** 35 challenge declarations, 35 identical, 0 differ, 0 missing. There are 231
  solution-only helpers. This is a textual comparison. It covers the large inlined
  `NormedAddCommGroup` instance proof and the theorem statement.

## LIMITS

- **Finite instances only.** Every computation uses finitely supported x and y on trees of at most 5
  vertices. The theorem is about completed spaces and arbitrary y. I rely on my own reduction argument
  above for finite support. The passage to the completion is the Lean proof's job; the paper does it by
  exhaustion.
- **Evidence, not a search for a counterexample to the theorem.** The search is a heuristic hill climb.
  "No instance above sqrt 2" is about what I found. It is not a bound.
- **Part 2 is my own geometry.** I checked it against brute force numerically, and at r = 9/10 exactly
  (the witness y = (1/10, 3/5)). The general-r closed form is not proved in exact arithmetic.
- **Two models, one check.** The infinite-tree part B_inf differs from the forest part only through the
  completion and the closed span. My finite checks cannot tell the two parts apart.
- **Not the official Comparator run.** Lean is checked by compile, axioms and a textual statement match.
  Comparator compares compiled terms. I did not check that the paper's other results are right, or that
  the solution's helper lemmas say what their names say. Only the compiled theorem is load-bearing.
- **Two Mathlib behaviours I did not test myself.** `Seminorm` iSup being the pointwise supremum for a
  bounded family, and `ContinuousLinearMap.extend` being non-degenerate here, are Mathlib facts. I
  checked the second through the cone's compiled lemma `coordinate_unitVector`. I did not read Mathlib
  source for the first.

## What I liked

The theorem can be drawn exactly. With two vertices the dual ball is a disk with two corners squared
off, and the lens is a sliver whose height you can write down: 2 sqrt(r(1-r)). That sliver already
shows the constant cannot go below sqrt 2. Whether the best constant is sqrt 2, 2, or something in
between, I could not determine. My search never beat sqrt 2, but a search is not a proof.

## Confluence's recheck

- Build log: `Build completed successfully (8935 jobs)`, `midpoint_lens_main` on [propext,
  Classical.choice, Quot.sound], sorry control on [sorryAx].
- Two-vertex instance from my own derivation, not the scripts: the segment norm on two vertices is
  max(l2, |u_r + u_c|), so the dual norm of (a, b) is the sup of a u_r + b u_c over the unit circle cut by
  the strip |u_r + u_c| <= 1. Sampling 200,000 boundary points: ||x|| = 0.9, ||x+y|| = 1, ||x-y|| = 1,
  ||Q_H y|| = 0.6, as reported. Bound 2 sqrt(1 - 0.81) = 0.8718 holds; the 1.3 control fails.
