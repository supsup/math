# TriangularCovering: finite triangular-cylinder covers of a regular tetrahedron below half the minimum shadow

Lean: `lean/ComparatorChallenges/TriangularCovering.lean` (statement, proof `sorry`). Its `.json` names the
solution `OAI.Geometry.TriangularCovering.Main`, which pulls in 9 modules under `lean/OAI/Geometry/TriangularCovering/`
(2247 lines, Mathlib only). Paper (context only): `preprints/Finite-angular-cylinder-covers-below-the-half-area-bound-September-27-2026/`.

## What it says, in my words

Take K = {(x, y, H t) : 0 <= t <= 1, |x| <= 1-t, |y| <= t}, with H = sqrt 2. The slice at height t is the
rectangle [-(1-t),1-t] x [-t,t], which is (1-t)*bottom edge + t*top edge. So K is the convex hull of
(+-1,0,0) and (0,+-1,H), a regular tetrahedron with edge 2. A "TriCylinder" is a unit axis u and a
non-degenerate triangle B lying in the plane u-perp through the origin. Its carrier is B + R*u, infinite in
both directions and including its boundary.

`main` is the conjunction of three claims:

1. **A_min = H.** The infimum over unit u of the area of K's orthogonal shadow on u-perp is sqrt 2. The minimum
   is reached looking along an edge, where the shadow is a triangle with base 2 and height sqrt 2.
2. **MainAsymptotic.** There are delta > 0 and C > 0 such that for every 0 < eps < delta, some family of exactly
   2*ceil(2/eps^2) TriCylinders covers every point of K, with
   |totalArea/H - (1/2 - (13/6000) eps^2)| <= C eps^4 and totalArea < A_min/2.
   The solution uses delta = 1/2000 and C = 14.
3. **NormalizedCounterexample.** Some finite cover has sum_i area(B_i) / shadowArea(u_i) < 1/2, where each
   denominator is K's shadow along that cylinder's own axis.

In the paper this refutes the "half-area cylinder covering conjecture" (sum |B_i| >= A_min/2), and claim 3
refutes its normalized form.

## Definitions audit (traps checked)

- **sInf (A_min).** The set {shadowArea u : |u| = 1} is nonempty and bounded below by 0, so `sInf` is a real
  infimum and not the empty-set default. Lean proves it equals H, and the value is attained (x-axis).
- **area = (euclideanHausdorffMeasure 2 B).toReal.** `toReal` would send an infinite measure to 0. That cannot
  happen here: bases carry a `finite_area` field, and shadows are compact images of a compact set. The
  normalization question (is this Lebesgue area or an unnormalized Hausdorff measure?) is settled by the
  solution rewriting with `InnerProductSpace.euclideanHausdorffMeasure_eq_volume` on 2-dimensional subspaces.
  It is also settled numerically: my exact Lebesgue area of the x-axis shadow is sqrt 2, which is the value Lean
  proves. I did NOT open the Mathlib source of the definition itself.
- **Division (relativeCost).** It divides by shadowArea(axis), which Lean bounds below by H > 0
  (`shadowArea_ge_H`). My sphere search agrees (min = 1.41421356237357). So the x/0 = 0 trap that could make
  the cost artificially small does not occur.
- **n eps = ceil(2/eps^2) as a natural number.** This is positive for eps > 0. No natural-number subtraction
  appears anywhere.
- **TriCylinder.** `triangular` forces a genuine (affinely independent) triangle. `perpendicular` puts it in
  u-perp through 0. `compact`, `convex`, `measurable` and `finite_area` all follow from that and do not weaken
  it. The carrier is the full two-sided cylinder, which matches the paper's B + R u.
- **Covers.** It quantifies over every point of the closed K, boundary included, not almost every point.
  This matters: the bottom edge is covered only on the boundary of the j = 0 lower cylinder, with exact
  equality (checked below).
- **Quantifier order.** It is exists delta, C, then for all eps, then exists a cover. That is a genuine uniform
  O(eps^4), and it is not vacuous because delta > 0. The count 2*n(eps) is exact (the type is `Fin (2 * n eps)`).
- **Lean is weaker than the paper in three ways. None is a defect, but they are worth knowing.**
  - The paper says eps <= 1/2000 with a remainder of at most 2 eps^4. Lean says there exist delta and C, and
    the proof uses delta = 1/2000 (open) and C = 14.
  - The paper's corollary covers every nondegenerate tetrahedron. Lean's `NormalizedCounterexample` covers
    only this regular K.
  - `MainAsymptotic` pins the coefficient 13/6000, so it is not a loose existence claim. The last conjunct,
    totalArea < A_min/2, is the conjecture's negation.

## Checks, with numbers

Python script: `replicate.py`, output in `replicate-output.txt`, about 20 s. It uses the stdlib plus numpy. Run
it from this folder with plain `python3`, not `-I`, because numpy is a user-site package and sympy is absent.
Java: `../java/src/confluence/math/triangularcovering/TriangularCovering.java`, about 6 s. Both were written
from the Lean definitions.

**The coordinate trick.** In (x, y, t) coordinates the Euclidean inner product is xx' + yy' + 2tt'. So squared
lengths, squared areas (Gram determinants) and carrier membership are all RATIONAL, and both programs check them
exactly: Python with `fractions.Fraction`, Java with a BigInteger rational. Carrier membership,
"P in conv(V0,V1,V2) + R D", is a 3x3 Cramer solve for the barycentric coordinates. It is affine-invariant, so
rescaling z by 1/H is harmless.

A. **Tetrahedron and A_min.**
   - All 6 squared edge lengths are exactly 4.
   - Along the x-axis, the projected vertices form a triangle with area^2 = 2 exactly, so the area is H.
   - The face direction gives sqrt 3 and the z-axis gives 2.
   - Closed form for the shadow: shadow(u) = max(H|u1|,|u3|) + max(H|u2|,|u3|). It comes from the four faces,
     each of area sqrt 3, with shadow = (1/2) sum |u . N_i|. It agrees with a convex-hull area of the projected
     vertices to 2e-15 over 2000 random directions.
   - Python: 200k Fibonacci sphere points plus local refinement give a minimum of 1.414213562373572
     (H + 4.8e-13), at u = (-1/2, 1/2, -1/sqrt 2). That is a second family of minimizers besides the edge
     directions.
   - Java: 400k points, minimum 1.41524 (no refinement).
   - Nothing went below H. This is evidence; the Lean proof is the proof of the lower bound.

B. **Base areas, exact.** At eps = 1/2001, n = ceil(2*2001^2) = 8,008,002, so there are 16,016,004 cylinders.
   For 96 cylinders in Python (14 in Java), lower and upper, I computed the exact squared area of the triangle
   projected onto the plane normal to its axis. It equals the Lean closed form
   (H (b-a) T^2 / (2 sqrt(1 + eps^2 (A^2 + 2B^2))))^2 in every case: 0 mismatches. The squared axis length
   equals 1 + eps^2 (A^2 + 2B^2) exactly.

C. **Area expansion.** I computed totalArea/H - 1/2 as a sum of corrections. The sum of (b-a)/4 is exactly 1/2.
   (1 + x)^(-1/2) - 1 is evaluated via expm1/log1p, with fsum or Neumaier summation. Cross-check against a direct
   60-digit Decimal sum of the unexpanded terms: the two agree to 8e-21 at eps = 1/20 and 2e-21 at eps = 1/50.

   | eps    | n(eps)     | R = total/H - (1/2 - 13/6000 eps^2) | R/eps^4 | total/H < 1/2 |
   |--------|------------|-------------------------------------|---------|---------------|
   | 1/2001 |  8,008,002 | 8.469e-15                           | 0.1358  | yes           |
   | 1/2500 | 12,500,000 | 3.476e-15                           | 0.1358  | yes           |
   | 1/3000 | 18,000,000 | 1.676e-15                           | 0.1358  | yes           |
   | 1/4000 | 32,000,000 | 5.304e-16                           | 0.1358  | yes           |
   | 1/5000 | 50,000,000 | 2.172e-16                           | 0.1358  | yes           |

   The ratio R/eps^4 is constant at 0.1358, inside Lean's C = 14 and the paper's 2. Java gets the same
   R = 8.469118e-15 at eps = 1/2001.

D. **Covering, exact, at eps = 1/2001.**
   - Near t = 1/2 the two families, lower (axes near x) and upper (axes near y), meet. For each (x, y) I computed
     the combined cutoff slack G = (T_j - r) + (T_k - s), where r + s does not depend on t. If G > 0, every t is
     covered by one family or the other.
   - Over a 161x161 grid, min G/eps^2 = 0.001997 (about 2 eta = 0.002) and no grid value is negative. So the
     margin really is the eta = 1/1000 slack, which is about 5e-10 in absolute terms.
   - I then tested points exactly, each with a rational witness cylinder found:
     - the 150 worst grid points, at the t* that splits the slack evenly;
     - vertices and the bottom, top and lateral edges, plus faces near t = 1/2;
     - 6000 random interior points and 3000 random points in the slab |t - 1/2| <= 3e-7.
   - Total 10,660 points in Python and 6,065 in Java, with 0 uncovered.
   - The bottom edge (t = 0) is covered only on the boundary of the j = 0 lower cylinder, where -A/|B| = -1 = a
     exactly. Exact arithmetic is needed to see this.

## Controls (each must fail, and does)

- **Control A.** "A_min = sqrt 3" (the face-shadow value) is refuted: a shadow of 1.414214 < 1.732051 exists.
- **Control C.** Using 12/6000 instead of 13/6000 gives |R'|/eps^4 = 667 at eps = 1/2001, rising to 4167 at
  1/5000, far outside C = 14.
- **Control D: cutoff T = 1/2.** I kept the same cylinders but dropped the eps^2 * cutoffCoeff term.
  - min G/eps^2 = -0.0625, and 6560 of the 6561 grid points are negative.
  - Test point P = (-4999/10000, 0, 499999992192967979/10^18).
  - Exhaustive check over all 16,016,004 cylinders: the float prefilter at -1e-9 leaves 0 candidates, and the
    best float margin is -7.8e-9, far beyond double error. So P is UNCOVERED.
  - The real family covers P (upper cylinder j = 800). Java reproduces this.
- **eta = 0 (extra; shows the 1/1000 slack is load-bearing).** min G/eps^2 = -3e-6, with 60 negative grid
  points. The point (-4999/200000, 4999/800000, 62499990238540807/1.25e17) has 1 float candidate per family,
  and both fail the exact check. So it is UNCOVERED with eta = 0, while the real family covers it (lower
  j = 4054066, upper j = 3803847).

## Lean (Docker, `../lean-docker/triangularcovering-run.log`, 2026-10-08 16:02-16:03Z)

- The 9-module cone builds against the pinned Mathlib (Lean 4.34.1).
- `'OAI.TriangularCovering.main' depends on axioms: [propext, Classical.choice, Quot.sound]` is exactly the
  permitted set, with no sorryAx.
- The sorry control `'controlWithSorry' depends on axioms: [sorryAx]` shows the axiom printer can say no.
- `statement_match.py TriangularCovering`: 17 challenge declarations, 17 identical, 0 differ, 0 missing. That
  covers all 16 definitions plus `main`. I also read the solution's `Basic.lean` and `Main.lean` by eye; the
  definitions and the statement of `main` are textually the same as the challenge.

## LIMITS / could not determine

- **Coverage is sampled, not proved.** I checked about 10k points at one eps (1/2001), with exact arithmetic
  plus the slack-G grid. The Lean proof (`finite_coordinate_cover`) is the proof for all of K and all eps.
- **The expansion is checked at 5 values of eps** (1/2001 to 1/5000), not uniformly. The float pipeline is
  validated against Decimal only at eps = 1/20 and 1/50, because a direct Decimal sum of 8 million terms was
  too slow to run.
- **The A_min lower bound is a numerical sphere search.** I have no independent proof that the shadow is never
  below sqrt 2. Lean proves it (`shadowArea_ge_H`).
- **The exhaustive "uncovered" checks use the coordinate form of membership as a float prefilter** (Lean's
  LowerHit/UpperHit shape). I derived that form independently: the lower triangle lies in x = 0 and the axis
  has x-component 1, so the parameter lam = x, and for the upper family lam = y. Candidates passing the
  prefilter are then decided by the exact Cramer test.
- **I did not open Mathlib's definition of `euclideanHausdorffMeasure`.** Normalization is inferred from the
  solution's rewrite lemma, plus the agreement of my exact Lebesgue value with Lean's proven H.
- **I did not check the paper's general-tetrahedron corollary**, which is not in the Lean statement, and I did
  not check the paper's 2 eps^4 bound beyond the 5 sampled eps (all at 0.136 eps^4).

## Confluence's recheck

- Build log: `Build completed successfully (8933 jobs)`, `main` on [propext, Classical.choice,
  Quot.sound], sorry control on [sorryAx].
- K read from the challenge myself: slice at height t is |x| <= 1-t, |y| <= t, exactly the convex
  combinations (1-t)(a,0,0) + t(0,b,√2) of the edges (±1,0,0) and (0,±1,√2); so K is their hull, a regular
  tetrahedron (all six squared edges 4, computed).
- Shadow minimum by my own convex-hull projection (not the script's closed form): along an edge exactly
  √2, along the z axis 2, and the minimum over 200,000 random directions 1.41495, nothing below √2.
  Consistent with the classical fact that a regular tetrahedron's smallest shadow is taken along an edge.
