# An Artin group with no geometric CAT(0) action: statement audit and checks

Lean: `lean/ComparatorChallenges/ArtinCAT0.lean` (statement, proof `sorry`), `.json` naming solution module
`OAI.GroupTheory.ArtinCAT0.Main`, theorem `OAI.ArtinCAT0.main`. 20-module, Mathlib-only cone (about 9,400 lines).
Docs: `lean/docs/254.md`. Paper: `preprints/An-Artin-group-with-no-geometric-CAT-0-action-September-23-2026/`.

## What it says, in plain words

There is one explicit Coxeter matrix on 116 letters, with labels 2, 3 and infinity. Its Artin group has no
action on any nonempty proper CAT(0) space that is isometric, proper and cocompact. This is a
**counterexample**, a negative answer to "is every Artin group CAT(0)?" (Charney's problem; Haettel's
Conjecture 1.1, as the paper's introduction cites it). It is not a special case of the positive conjecture.

Docs Scope (254.md), quoted: "The geometric-action question asks whether every Artin group acts properly and
cocompactly by isometries on a proper CAT(0) space. The formalized result gives a counterexample: an Artin
group defined by a symmetric matrix on $116$ generators, with diagonal entries $1$ and off-diagonal entries in
$\{2,3,\infty\}$. It admits no such action on any nonempty proper CAT(0) space, in any dimension."

## Audit verdict

**Matches its name and its Scope. It is a full negative resolution of the conjecture, assuming the definitions
below are the standard ones; it is not weaker than named.** It is also not the "full open problem" in the
positive direction. One example group is enough to refute "every Artin group is CAT(0)", and that is what
this proves.

`main` has four conjuncts. The first three say the matrix is a genuine Coxeter matrix: it is symmetric, its
diagonal is 1, and every off-diagonal entry is in {2, 3, ⊤}. The fourth is the content:

```lean
(∀ (X : Type u) [MetricSpace X] [ProperSpace X] [Nonempty X]
  [MulAction (ArtinGroup explicitMatrix) X],
  ¬ GeometricAction (ArtinGroup explicitMatrix) X)
```

Because the theorem is a NEGATION, the direction of the risk flips. A weak definition of `GeometricAction`
would make the theorem *stronger*. The way it could be cheap is if the definitions were too strong or could
never be satisfied, so that "no such action" became trivially true. I checked each one for that:

- **Artin group.** The relators are `alternating s t n * (alternating t s n)⁻¹` whenever `M s t = (n : Label)`.
  ⊤ gives no relation, and a diagonal 1 gives the trivial relator s·s⁻¹. This is the standard presentation.
  No s² = 1 is imposed, so this is the Artin group and not the Coxeter group. Lean and the Python check agree.
- **The group is not finite.** If it were finite, it would act geometrically on a point, and the theorem would
  be false; it would not be a cheap truth. Every relator has exponent sum 0, so s ↦ 1 maps the group onto Z
  (checked for all relators). The group is therefore infinite, and the properness clause rules out the
  one-point space. Nothing makes the conclusion vacuous.
- **`CAT0`.** It asks for two things. First, a geodesic `Segment` must exist between every pair of points.
  Second, for EVERY pair of segments from a common vertex x and every t, u ∈ [0,1],
  d(γt, ηu)² ≤ (t²−tu)d(x,y)² + (u²−tu)d(x,z)² + tu·d(y,z)². I checked exactly that the right-hand side is
  the squared Euclidean comparison distance (law of cosines; it holds as an identity in R²). Any two
  points on a triangle lie on sides that share a vertex, or on one side, where equality holds. So this is the
  full CAT(0) comparison, and it is not a midpoint-only weakening. It is satisfiable: a point, R, and trees
  all meet it (tree sampled below). It holds only for nonpositive curvature: the sphere fails it (control).
  There is no division, no sSup or sInf, and no `x/0`.
- **`GeometricAction`.** It is the conjunction of: CAT0 X; each g acts as an `Isometry`; for every compact K,
  `{g | gK ∩ K ≠ ∅}` is finite (metric properness); and ∃ compact K with G·K = X (cocompactness).
  `ProperSpace X` and `Nonempty X` are hypotheses. On a proper space, this is the standard notion of a
  geometric action. It is satisfiable (Z on R by translations: the K=[−3/2, 7/3] case is checked).
- **The hypotheses are not contradictory.** `ProperSpace`, `Nonempty`, `MulAction` and universe-polymorphic
  `Type u` can all be satisfied, so the statement is not vacuously true.
- **Relation to the standard question.** Requiring X to be proper is a restriction on the spaces that are
  excluded. The paper (intro) says properness of X follows from the other action hypotheses for a length
  space, and cites Bridson–Haefliger Exercise I.8.4(1). **I did not verify that citation.** If it is
  wrong, the formal result still excludes all geometric actions on *proper* CAT(0) spaces, and that is the
  setting the docs Scope names.

The structure of the matrix, computed from the Lean definitions:

- **Three blocks.** Each block is a 39-letter path, with label 3 between neighbours and 2 otherwise. That is
  type A_39, the braid group B_40. The Gram matrix is positive definite with det 40/2³⁹.
- **How the blocks join.** Block b begins with letters b and b+1 mod 3, so letters 0, 1, 2 form a (3,3,3)
  triangle (affine Ã₂, Gram det 0).
- **Sentinels.** Letters 3 and 4 commute with 0, 1, 2 and are free (⊤) toward each other and toward
  everything else.
- **Census over the 6,670 unordered pairs.** 114 pairs are labelled 3, 2,115 are labelled 2, and 4,441 are ⊤.
- **No ambiguity in the labels.** No pair is both Adjacent and Distant, so the order of the `if` branches
  never decides a label.

The solution uses these pieces. `Main.lean` takes the centralizer of the free group ⟨3,4⟩, the triangle group,
and each block's B_40 embedding. It finishes with `SixSector.no_strict_ratios`, a stable-length ratio
contradiction.

## Checks and controls

- `replicate.py`: exact Python (int/Fraction), `python3 -I replicate.py`, exit 0, prints "ALL CHECKS AND
  CONTROLS BEHAVE". The checks:
  - the three decidable conjuncts;
  - relator lengths of 2n;
  - exponent sums of 0;
  - all 4,446 intra-block relators die in S_40 under the map i ↦ (i i+1);
  - the Gram determinants;
  - the R² identity, exact on 2,000 random rational triangles;
  - the tripod tree inequality, on 2,000 exact samples;
  - Z on R properness.
- `../java/src/confluence/math/artin/ArtinCAT0.java` (package `confluence.math.artin`) independently
  re-transcribes the same definitions. It also gets census {3:114, 2:2115, ⊤:4441} and 4,446 S_40 relators,
  and checks the R² identity exactly in `long`. Exit 0.
- **Negative controls. Each one must fail, and each one does:**
  - a length-2 relator on an adjacent pair does not die in S_40;
  - a length-3 relator on a commuting pair does not die in S_40;
  - the unit-sphere octant triangle violates the Lean CAT0 inequality at its two side-midpoints
    (t = u = 1/2): d² = (π/3)² ≈ 1.0966, against a comparison value of 0.6169.
- **A prediction of mine that was wrong, kept here on purpose.** I first wrote the commuting-pair control
  expecting S_40 could NOT detect a length-3 relator there. It can: for commuting s, t we get sts = t and
  tst = s. The check flagged my expectation, and I corrected the control rather than the data.
- **LEAN, in Docker** (2026-10-08 23:02Z, `../lean-docker/artin-run.log`; Lean 4.34.1):
  - the build succeeded (8,944 jobs);
  - `'OAI.ArtinCAT0.main' depends on axioms: [propext, Classical.choice, Quot.sound]`. These are exactly
    the permitted axioms, and there is no sorryAx;
  - the sorry control in the same file shows `[sorryAx]`.
- **statement_match:** 14 challenge declarations, all 14 textually identical in the solution, none missing,
  997 helper declarations only in the solution.

## Limits

- The non-existence claim is a statement about every proper CAT(0) space, so no computation can test it.
  Its evidence is the Lean compile plus the axioms output. I did not read the 9,400-line proof.
- Textual statement match is not Comparator's compiled-term comparison. Matching names in the same
  namespace with identical text is strong evidence, not proof.
- The S_40 check shows the relators hold in the Coxeter quotient of each block. It does not show they are
  *all* the relations (that the Artin group is not smaller). The relator *set* is checked by reading the Lean
  and by the length checks.
- The tree and sphere checks are samples. The sphere control is done in floating point, with a margin of
  about 0.48.
- **Could not determine:**
  - whether this counterexample is correct mathematics beyond what Lean certifies, which depends on whether
    the definitions above are faithful (I judge they are);
  - whether the result is new or known. The paper's intro claims it refutes Haettel's Conjecture 1.1 and
    surveys positive cases (RAAGs, three-generator large type, XXL, braid groups up to 7 strands). I did not
    check those citations;
  - the B–H Exercise I.8.4(1) claim that properness of X is automatic.
- The Lean build log lists only 11 of the 20 cone modules by name. Lake prints modules selectively, and the
  build reported success with `Main` built. `#print axioms` on `main` needs the whole cone.

## Confluence's recheck

- Read `main` and the definitions myself (challenge lines 49-71). CAT0 requires a constant-speed segment between every
  pair of points and, for every two segments from a common vertex x and every t, u in [0,1],
  d(gamma t, eta u)^2 <= (t^2 - tu)|xy|^2 + (u^2 - tu)|xz|^2 + tu|yz|^2. I re-derived the right side: for Euclidean
  p = x + t(y - x), q = x + u(z - x), |p - q|^2 = t^2 a + u^2 b - tu(a + b - c) with a = |xy|^2, b = |xz|^2, c = |yz|^2,
  which is the same expression. Choosing the common vertex covers every pair of sides, so it is the full CAT(0)
  comparison, not a midpoint weakening. GeometricAction = CAT0 + isometries + proper (finitely many g with gK
  meeting K, for every compact K) + cocompact: the standard notion, satisfiable (Z on R).
- Build log: `Build completed successfully (8944 jobs)`; `main` on [propext, Classical.choice, Quot.sound]; sorry
  control on [sorryAx]. statement_match 14/14.
- Caption level: kernel-checks this formal statement; one statement reading so far (mine, with the sub-agent).
