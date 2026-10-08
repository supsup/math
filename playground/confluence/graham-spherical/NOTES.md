# GrahamSpherical: verification notes (2026-10-08)

Target: `lean/ComparatorChallenges/GrahamSpherical.lean`, theorem `OAI.GrahamSpherical.full_main`,
solution module `OAI.Combinatorics.SphericalRamsey.Main` (18-module, Mathlib-only cone, 982 lines).
Paper (context only): `preprints/A-classification-of-finite-Euclidean-Ramsey-configurations-September-23-2026/`,
Proposition `cons:twelve` in `build/sections/07-consequences.tex` (via `lean/docs/172.md`).

## The statement in plain words

Let t = sum_{k>=1} 10^(-k!) = 0.110001000...0001... (Liouville's constant), u = (1-t^2)/(1+t^2),
v = 2t/(1+t^2), so (u, v) = (cos theta, sin theta) with theta = 2 arctan t (about 12.6 degrees). Let X be
the union of three squares inscribed in the unit circle: the coordinate square
Q0 = {(+-1,0), (0,+-1)}, Q0 rotated by +theta, and Q0 rotated by -theta. Then:

1. X has exactly 12 points,
2. X lies on the unit circle,
3. for every dimension n >= 1 there is a 50-colouring of R^n with no monochromatic congruent copy of X,
4. hence X is not Euclidean Ramsey.

**Relation to Graham's conjecture.** Erdos et al. proved Ramsey => spherical. Graham conjectured the
converse (every finite spherical set is Ramsey). X is finite and spherical (on a circle) and not Ramsey,
so the Lean statement, if the definitions are faithful (they are; see below), is an explicit
**counterexample to Graham's conjecture**. It is not new as a refutation: the paper credits Palvolgyi
(arXiv 2609.23327, a seven-point circle configuration) with disproving the spherical conjecture first,
and the sibling EuclideanRamseyNine result (already checked, `../ramsey-nine/NOTES.md`) is a
non-explicit refutation. What this one adds is an EXPLICIT set (a named transcendental, not "some
algebraically independent reals") and an explicit colour count (50) uniform in the dimension.

The Lean statement (verbatim from the challenge file):

```lean
def EuclideanRamsey {d : ℕ} (X : Set (Point d)) : Prop :=
  ∀ r : ℕ, 0 < r → ∃ n : ℕ, 0 < n ∧
    ∀ color : Point n → Fin r,
      ∃ f : X → Point n, Isometry f ∧ ∃ c : Fin r, ∀ x, color (f x) = c

def FullAuthoredResult : Prop :=
  witness.ncard = 12 ∧
  witness ⊆ Metric.sphere (0 : Point 2) 1 ∧
  (∀ n : ℕ, 0 < n → ∃ color : Point n → Fin 50, AvoidsCopy witness color) ∧
  ¬ EuclideanRamsey witness
```

## Definitions audit

| Item | Reading | Trap check |
|---|---|---|
| `Point n := EuclideanSpace ℝ (Fin n)` | R^n, Euclidean metric | L2, not sup metric. |
| `EuclideanRamsey` | for all r > 0 there is n > 0 such that EVERY r-colouring of R^n has a monochromatic isometric copy | Quantifier order correct: r, then n, then all colourings, then a copy. Colourings arbitrary (no measurability). `0 < n` makes Ramsey only harder, but for n = 0 (one point) a 12-point set has no isometric copy anyway, so it changes nothing; `0 < r` harmless. Negation = "some r defeats every n", which conjunct 3 gives with r = 50. |
| `Isometry f`, `f : X → Point n` | distance-preserving map of the subtype X (induced metric) = congruent copy | Standard; no orientation or same-dimension requirement, so not an over-strict copy notion that would make non-Ramsey cheap. |
| `AvoidsCopy` | no isometric copy is monochromatic | Literally the negation of the inner clause of `EuclideanRamsey`. |
| `witness.ncard = 12` | X finite with 12 points | `ncard` of an infinite set is 0, so 12 forces finiteness. Proved from injectivity of `vertex`. |
| `witness ⊆ Metric.sphere 0 1` | X on the unit circle | This is the "spherical" hypothesis of Graham's conjecture (a circle is a sphere in R^2). |
| `parameter := ∑' m, 1/10^((m+1)!)` | Liouville's constant from k = 1 | `tsum` is 0 if not summable: ruled out, Lean proves `parameter = liouvilleNumber 10 - 1/10` and `11/100 < parameter < 12/100`. Mathlib's `liouvilleNumber` starts at k = 0, hence the -1/10; matches the paper's t. |
| `u, v` divisions | by 1 + t^2 >= 1 | Lean `x/0 = 0` never bites. |
| no `sSup/sInf`, no hypotheses | the theorem has NO premises | Nothing vacuous; `definition_names` in the JSON is empty and the solution's `Model.lean` restates the same definitions (statement_match 13/13). |

## How the Lean proof goes (read in full; 982 lines)

The Lean proof is DIRECT: it builds the colouring. It does not go through the paper's classification
theorem (the paper's own proof of `cons:twelve` does, via the field criterion); the Lean route is the
self-contained "derivation colouring".

1. `Parameter`: t transcendental over Q (from Mathlib's `transcendental_liouvilleNumber`), bounds.
2. `RealTranscendenceBasis` + `BasisDerivation` + `AlgebraicExtension` + `RealDerivation`: extend {t}
   to a transcendence basis of R over Q, take d/dt on the rational function field, extend to R
   (algebraic extension, char 0): a `Derivation ℤ ℝ ℝ` D with D t = (1+t^2)/2 (uses choice; D is
   discontinuous). The extension lemma is built on Mathlib's `Differential` machinery.
3. `DerivationCoordinates`: D u = -v, D v = u (quotient rule only).
4. `AffineCopy*`: any isometric copy of the 12 points in R^n is y_i = c + x_i A + y_i B with A, B
   orthonormal (proved from three anchor points of Q0; no dimension hypothesis).
5. `EnergyIdentity` + `CopyInvariant`: with E(y) = sum_j D(y_j)^2 and weights +1 (rotated squares),
   -2 (Q0), sum_i w_i E(y_i) = 4(|A|^2 + |B|^2) = 8 for EVERY copy. Key identity
   `weighted_coordinate_square`: sum_i w_i (p + a x_i + b y_i + c Dx_i + d Dy_i)^2 = 4(c^2+d^2).
   The +theta / -theta pairing is what cancels the mixed (a,b)x(c,d) terms.
6. `Coloring` + `MonochromaticObstruction`: colour = floor(3E) mod 50. If all 12 colours agree, then
   S = sum w_i floor(3 e_i) is = 0 mod 50 (weights sum to 0) but 16 < S < 32. Contradiction.
7. `Ramsey`: 50 colours in every n >= 1 => not Ramsey.

## What I checked, and how

### Lean in Docker (`../lean-docker/grahamspherical-run.log`)

Serialized under the shared lock, machine-free gate admitted (busy_cores=0). Lean 4.34.1, 18 modules
copied, `Build completed successfully (2676 jobs)`. Output:

```
'OAI.GrahamSpherical.full_main' depends on axioms: [propext, Classical.choice, Quot.sound]
'controlWithSorry' depends on axioms: [sorryAx]
```

Exactly the three permitted axioms, no `sorryAx`; the sorry control proves the instrument can report one.
A grep of the 18 files for `sorry|axiom|admit|native_decide|implemented_by|extern` hit only the word
"admits" in a docstring.

`statement_match.py GrahamSpherical`: challenge declarations 13, identical 13, differ 0, missing 0
(49 solution-only helpers).

### Python (`replicate.py`, exact `fractions.Fraction`; sympy not installed)

`python3 -I replicate.py` -> exit 0, all checks PASS, all controls fail as required.

- t_3 = 0.110001 exactly, and 11/100 < t_3 < t < t_3 + 2*10^-24 < 12/100.
- With t replaced by rationals (t_3, 1/10, 11/100, 3/25; u, v are rational in t so circle facts stay
  exact): 12 distinct points, x^2 + y^2 = 1 exactly; all 495 four-point concyclicity determinants
  vanish; 10 distinct squared distances, min ~ 0.0478 > 0.
- Dual numbers (a + b eps) as an exact model of a derivation on a finitely generated field:
  D t = (1+t^2)/2 gives D u = -v, D v = u at 50 rational t.
- The moment identity of `weighted_coordinate_square` as an exact polynomial identity in
  u, v, p, a, b, c, d: LHS = 4(u^2+v^2)(c^2+d^2) + 4(u^2+v^2-1)(a^2+b^2), the Lean `calc` first step.
- Copy invariant: 20 random exact isometric copies in R^2, R^3, R^5, R^8 (orthonormal pair from a
  rational Cayley transform, arbitrary D-values for z, A, B) have weighted energy exactly 8, and their
  66 squared distances match the original exactly.
- Rounding: m = 50 works. The floor(3E) mod m argument works exactly for m = 16 and m >= 32 (no
  multiple of m in the open interval (16, 32)); so 50 is sufficient, not tight for this argument
  (16 would do). This does NOT say anything about the true colour threshold of X.

### Java (`../java/src/confluence/math/grahamspherical/GrahamSpherical.java`, BigInteger rationals)

Independent code, same checks and controls (minus the symbolic polynomial identity, which the
dual-number copy check covers numerically-exactly): all PASS, all controls OK.

## Controls (each must fail; all did, in Python and Java)

- One point scaled by 11/10: 165 of 495 concyclicity determinants nonzero.
- D t = 1 instead of (1+t^2)/2: D u != -v; weighted energy 8 lambda^2 = 31.2394 (lambda = 2/(1+t^2)).
- Non-isometric copy (A scaled by 2): energy 20, not 8.
- Both rotated squares turned the same way (+theta, +theta): polynomial identity fails (4 residual
  monomials, the mixed a*d, b*c terms) and copy energy is not 8. Shows the -theta square is necessary.
- All weights 1: identity fails (3 residual monomials).
- Moduli 15, 17, 31: explicit exact energies with weighted sum 8 whose floor(3e) all share one residue,
  so the rounding step genuinely depends on the modulus.

## LIMITS / could not determine

- **The existence of D on R is Lean-only.** Steps 2 (transcendence basis + extension of a derivation
  through an algebraic extension) need choice and cannot be computed. My dual-number checks verify the
  identities D satisfies on the finitely generated field Q(t, coordinates of the copy), which is all the
  energy argument touches, but not the extension theorem itself. I did not re-check
  `AlgebraicExtension.lean` beyond reading it.
- **Transcendence of t** is taken from Mathlib (`transcendental_liouvilleNumber`), not re-proved.
  It matters: for algebraic t every derivation kills t, so no such D exists and the argument says
  nothing.
- **Random copies are evidence; the proof-grade facts are the exact polynomial identity** (which I
  reproduced) plus the affine-copy lemma (Lean-only: I generated copies already in affine form, I did
  not re-prove that every isometric copy has that form).
- **Not the official Comparator check.** Compile + `#print axioms` + textual statement match only; no
  kernel export / term comparison sandbox.
- **Literature/novelty unverified.** The paper says Palvolgyi refuted Graham's conjecture first with a
  heptagon and that this twelve-point obstruction uses "the same type of weighted derivation moments";
  I did not read Palvolgyi's paper. Whether 50 is close to the true minimum number of colours for X is
  not addressed by anything here.

## Confluence's recheck

- Build log: `Build completed successfully (2676 jobs)`, `full_main` on [propext, Classical.choice,
  Quot.sound], sorry control on [sorryAx].
- D u = -v and D v = u from D t = (1 + t^2)/2, exactly, by the chain rule at rational t: D acts on the
  circle as d/dtheta.
- Rounding: with weights +1 on the 8 rotated points and -2 on Q0 and weighted energy 8, S = 24 - (sum of
  8 fractional parts) + 2 (sum of 4) lies strictly in (16, 32) (200,000 random draws, and by the bound).
  The moduli with no multiple strictly inside (16, 32) are exactly m = 16 and m >= 32, so 50 colours works.
- Copy invariant with MY OWN random copies in R^2, R^3, R^5, R^8, R^13: random orthonormal A, B and
  derivatives obeying the constraints orthonormality forces (A.DA = 0, B.DB = 0, A.DB + DA.B = 0), random
  c and Dc: weighted energy 8.0 in every one (floats, 9 decimals).
