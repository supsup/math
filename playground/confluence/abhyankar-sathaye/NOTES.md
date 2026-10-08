# AbhyankarSathaye: verification notes (2026-10-08)

Target: `lean/ComparatorChallenges/AbhyankarSathaye.lean`, theorem
`OAI.AbhyankarSathaye.exists_noncoordinate_polynomial`. The solution module is
`OAI.AlgebraicGeometry.AbhyankarSathaye.Counterexample`, a 15-module cone that depends only on Mathlib. The paper is
`preprints/An-explicit-noncoordinate-polynomial-with-affine-three-space-zero-fibre-September-24-2026/`.
I read it for context only.

## The statement in plain words

For every natural number n ≥ 4 there is a polynomial F in ℂ[X_0, …, X_{n-1}] with two properties:

1. ℂ[X]/(F) ≅ ℂ[Y_0, …, Y_{n-2}] as ℂ-algebras, so the hypersurface F = 0 is affine (n-1)-space.
2. No ℂ-algebra automorphism e of ℂ[X] and no index i satisfy e(X_i) = F, so F is not a coordinate (variable).

## How this relates to the classical conjecture

The Abhyankar–Sathaye (epimorphism / embedding) conjecture, hypersurface form, says: over a field of
characteristic 0, if k[x_1..x_n]/(f) ≅ k^[n-1], then f is a coordinate. The Lean statement is exactly the
negation of that conjecture over ℂ, for every n ≥ 4:

- **Field:** ℂ, so characteristic 0. This is not the positive-characteristic situation, where
  non-rectifiable embeddings have long been known (Segre/Nagata-type examples). That trap does not apply.
- **Dimension:** ambient n ≥ 4. The paper says it does not address n = 3. n = 2 is the Abhyankar–Moh–Suzuki
  theorem, which is true.
- **"Isomorphic to affine space":** an `AlgEquiv` over ℂ between the quotient by `Ideal.span {F}` and
  `MvPolynomial (Fin (n-1)) ℂ`. This is the ring-level statement the conjecture uses. Because n ≥ 4, the
  natural-number subtraction n - 1 does not truncate.
- **"Coordinate":** the image of a variable under a ℂ-algebra automorphism. This is the standard notion. It
  is not weaker than its name: being part of a generating system is equivalent to being the image of some
  variable under an automorphism. A coordinate shifted by a constant is still a coordinate (compose with a
  translation), so the definition does not miss that case.

Checks for traps:

- **No vacuous hypothesis.** The only hypothesis is 4 ≤ n, which can be satisfied.
- **No trivial witness.** F = 0 gives the quotient ℂ[X], and a unit F gives the zero ring; neither is a
  polynomial ring in n-1 variables. In any case the solution's witness is explicit.
- **Quantifiers.** ∃F, then (∃ iso) ∧ ¬(∃ e, ∃ i). This is the correct shape.
- **Witness for n > 4.** It is the same 4-variable F, renamed into the first four variables. That is
  standard stabilization. Its quotient by (F) is ℂ^[3] ⊗ ℂ^[n-4].

If the Lean is right, this is a counterexample to the Abhyankar–Sathaye conjecture over ℂ in dimension 4.
That would be a major result. I could not check how it fits the literature; see LIMITS.

## The explicit data, transcribed from the Lean

The variables are (h,u,v,w):

- S = 2u³v + 3u⁴w + h(v² − 3u²w²) + h²w³
- x = u³ + hv, y = −u² + hw, s = S
- P(x,y,s) = −2s²x + 3sy² − 3s³y
- **F = h − P(x,y,s) − 1**: total degree 17, 69 terms, integer coefficients with |c| ≤ 594, degrees in
  (h,u,v,w) = (7,14,6,10)

Inverse ψ: ℂ[X,Y,T] → R/(F) sends:

- X ↦ x + s³
- Y ↦ y − s²
- T ↦ αu + β(v + uw), where α = 1 + 2s²x + 4s⁵ and β = (3s³ − 3sy)(1 + 2s²x) − 4s⁴y²

Forward φ sends (h,u,v,w) ↦ (freeH, freeU, freeV, freeW). These are defined in FiberFormulas.lean through
freeS = X² + Y³, freeX = X − freeS³, freeY = Y + freeS², inverseU/G/W/V.

Non-coordinate argument (NonCoordinate.lean): at (2, 0, −1/2, 1/2), F = −1 and grad F = 0. The fibre F = −1
is therefore singular. A coordinate cannot have a critical point, because by the chain rule
1 = Σ e⁻¹(∂_j F)·∂_i e⁻¹(X_j). That proof is elementary and sound.

## Checks run

`python3 replicate.py` → `replicate-output.txt`. No CAS is installed (no sympy), so the script has its own
sparse integer polynomial class. Run time is about 2 s.

| | Check | Result |
|---|---|---|
| A | cusp x²+y³ = hs, shift identity, **ambient (x+s³)²+(y−s²)³ = s(1+F)**, Bézout certificate; exact in ℤ[h,u,v,w] | PASS |
| B | F(2,0,−1/2,1/2) = −1 and all 4 partials of the **expanded** F are 0, in exact rationals. This does not go through the Lean's ambient-identity route. | PASS |
| C | φ(F) = 0, φ(x+s³) = X, φ(y−s²) = Y, φ(param) = T. Schwartz–Zippel at 40 random points mod 2⁶¹−1 (expansion is infeasible: degrees run into the thousands) | PASS |
| D | Full enumeration of F_p⁴ for p = 2,3,5,7,11,13: #V(F) = p³ exactly; φ: F_p³ → V(F)(F_p) is a bijection with inverse ψ | PASS |
| D2 | 60 random points **on** V(F) mod 2⁶¹−1, found by root-finding in w on random (h,u,v) lines; ψ∘φ = id at each | PASS |
| D3 | φ(1,0,0) = (1,0,0,1) is on V(F) with grad F = (10,0,2,15) ≠ 0 | PASS |

Why C + D2 + D3 together make the isomorphism plausible independently of Lean:

- C shows that φ̄: R/(F) → ℂ[X,Y,T] is surjective with section ψ̄.
- Its kernel is then a prime P = (g), with g an irreducible factor of F.
- The isomorphism holds iff F is a unit times g. D2 would see any other factor as points of V(F) that φ
  cannot reach. D3 rules out g being a repeated factor, since grad F would vanish on V(g).
- The finite-field results are reductions of a ℤ-identity, so they are evidence, not proof. The Lean is the proof.

A side observation (D): every fibre F = c has exactly p³ points over each F_p tested, including the singular
fibre c = −1. Equal point counts do not imply isomorphism, so this neither supports nor undercuts anything.

The Java replication is `java/src/confluence/math/abhyankar/AbhyankarSathaye.java`. It runs the same
formulas over ℤ-polynomials, ℚ and ℤ/p. It reproduces A (ambient, cusp), B, C (30 points), and D for
p = 7 and 11, and all three of its controls fail as required. Run time is about 0.2 s.

## Controls (each must fail, and does)

- **Perturbed S** (2u³v → 3u³v): φ(F′) ≠ 0 at a random point. Over F_7, #V(F′) = 361 ≠ 343.
- **Wrong inverse** (2UyG → 3UyG in inverseW): φ(F) ≠ 0, or φ(shiftY) ≠ Y.
- **Moved point** (2,0,−1/2,3/2): gradient = (333595/4, 0, −9634, 156603) ≠ 0. Java agrees on ∂_h = 333595/4.
- **D2 instrument on G = F·(w−h)**, which has the extra component w = h: ψ∘φ = id fails at its roots.
  So D2 can see an extra component.

## Lean (Docker, `lean-docker/abhyankar-run.log`)

All 15 modules built against the pinned Mathlib `d13f23b7` / Lean 4.34.1 (`Build completed successfully`).

```
'OAI.AbhyankarSathaye.exists_noncoordinate_polynomial' depends on axioms: [propext, Classical.choice, Quot.sound]
'controlWithSorry' depends on axioms: [sorryAx]
```

- **Axioms:** exactly the three the challenge permits, and no `sorryAx`. The control shows that the
  instrument does report a sorry.
- **`statement_match.py`:** 1 challenge declaration, 1 identical, 0 differ, 0 missing. The solution has 219
  helper declarations.

## LIMITS / could not determine

- **Not the official Comparator.** There was no term-level comparison and no kernel replay in a sandbox. The
  check was compile + `#print axioms` + a textual statement match.
- **The challenge file was not compiled itself.** Its text matches the solution's theorem. Its odd-looking
  import `Mathlib.Basic.Complex.Basic` also appears in the solution's `Identities.lean`, which compiled, so
  the module exists at this Mathlib rev.
- **Python/Java checks of φ(F) = 0 and φ∘ψ = id are probabilistic.** They use Schwartz–Zippel mod a 61-bit
  prime, with error ≤ deg/p per point. The ψ∘φ ≡ id (mod F) direction was checked only pointwise (small
  fields exhaustively, plus random large-field points). Ideal membership mod F was not expanded symbolically
  because it is too large.
- **Irreducibility of F was not checked by factorization** (no CAS). It is inferred from D2/D3 as argued above.
- **Literature consistency not determined.** I did not establish whether a known theorem rules out such an F
  for n = 4 (for example results on affine-space fibres or Kaliman-type theorems, which I know only for
  n = 3). The paper cites only affirmative special cases (KVZ, Maubach, Ghosh) and claims none applies.
  Whether this result is accepted by experts is outside what computation here can settle.
- I did not read the full paper beyond its introduction.

## Confluence's recheck (independent of the sub-agent's scripts)

- Read the challenge statement myself: for every n >= 4, some F in C[X_0..X_{n-1}] has
  C[X]/(F) isomorphic to C[n-1 variables] as C-algebras, and F is the image of no variable under any
  C-algebra automorphism. That is the negation of the Abhyankar-Sathaye (embedding) conjecture in
  characteristic 0, dimension 4 and up.
- Copied S, P and F from `Identities.lean` (not from the report) and `criticalPoint` from
  `CriticalPoint.lean`; with exact rationals and dual numbers: F(2, 0, -1/2, 1/2) = -1 and all four
  partial derivatives are 0. A coordinate has no critical points, so this half of the claim is
  elementary and now checked twice. Control point (2, 0, -1/2, 3/2): gradient (333595/4, 0, -9634,
  156603), matching the report.
- Zeros of F over F_p: 125, 343, 1331 for p = 5, 7, 11, exactly p^3 each. The 2u^3v -> 3u^3v control
  gives 361 and 1286 at p = 7 and 11, but ALSO 125 at p = 5: point counts are weak evidence on their
  own. The explicit inverse map (the sub-agent's C/D2 checks) and the Lean proof carry the
  isomorphism half.
- Build log: 15 modules, `Build completed successfully (1619 jobs)`, permitted axioms only, sorry
  control shows sorryAx.
