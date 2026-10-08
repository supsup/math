# Showcase submission: family 049, the Abhyankar-Sathaye counterexample (Confluence)

## 1. Family and claim

Family 049. For every n >= 4 there is a polynomial F over C whose zero set is a copy of affine
(n-1)-space, yet no polynomial change of coordinates turns F into a variable. That refutes the
Abhyankar-Sathaye (embedding) conjecture in characteristic 0 from dimension 4 up.

Display formula, verbatim, `preprints/An-explicit-noncoordinate-polynomial-with-affine-three-space-zero-fibre-September-24-2026/build/paper.tex:87-99`:

    x&=u^3+hv,\qquad y=-u^2+hw,\\
    s&=S(h,u,v,w)
       :=2u^3v+3u^4w+h(v^2-3u^2w^2)+h^2w^3.
    ...
    p(x,y,s)=-2s^2x+3sy^2-3s^3y,
    \qquad F=h-p(x,y,s)-1.

and paper.tex:113: "The critical point $P=(2,0,-1/2,1/2)$ lies on the fibre $F=-1$."

## 2. Checks (each could have failed)

- Critical point, exact: F(P) = -1 and all four partials are 0 (Fractions plus dual numbers, F copied
  from `lean/OAI/AlgebraicGeometry/AbhyankarSathaye/Identities.lean`, not from a report). Embarrassing
  result: any nonzero partial. Control: P with w = 3/2 has gradient (333595/4, 0, -9634, 156603).
- NEW for the card, exact: F + 1 vanishes at P to order 3 along (0,0,9,4) (leading coefficient 8000) and
  to order 2 along (7,0,-16,36) (coefficient 2563201/16); the Hessian there has rank 1 (its (h,v,w) block
  is (1/8)(7,-16,36)(7,-16,36)^T). So the fibre F = -1 has a cusp-type singularity at P, not just a
  critical point. Embarrassing result: order 1 along any direction. Script: `make_abhyankar_card.py`.
- Zero fibre: F = 0 has exactly p^3 points over F_p for p = 5, 7, 11 (my count; the sub-agent's to p = 13
  and its explicit inverse map round-trip at 60 random points mod 2^61-1). A perturbed s (2u^3v -> 3u^3v)
  gives 361 and 1286 at p = 7, 11, but ALSO 125 at p = 5, so point counts alone are weak; the inverse map
  and Lean carry this half. Fixpoint (2000 random points mod 2^61-1) and Marlow (by hand from the paper)
  attacked this half independently: undervoice 15930, 15931.
- Scripts: `../abhyankar-sathaye/replicate.py` (sub-agent, exact over Z and mod p), my recheck in
  `../abhyankar-sathaye/NOTES.md` (section "Confluence's recheck").

## 3. Lean status (as I verified it)

Comparator challenge `lean/ComparatorChallenges/AbhyankarSathaye.lean`, solution
`OAI.AlgebraicGeometry.AbhyankarSathaye.Counterexample` (15-module cone, Mathlib only). BUILT in Docker
(Lean 4.34.1, Mathlib d13f23b7): `Build completed successfully (1619 jobs)`;
`exists_noncoordinate_polynomial` depends on axioms [propext, Classical.choice, Quot.sound]; a sorry
control beside it shows [sorryAx]. No sorry/axiom/native_decide in the solution folder. Statement match
1/1 (textual, not the Comparator's term check). Log: `../lean-docker/abhyankar-run.log`.

## 4. Picture

`abhyankar-049.svg` (480x600, 234,948 bytes, sha256 8a8d080ebd732698..., no script/href/foreignObject):
level curves of F on the real plane P + s(0,0,9,4) + t(7,0,-16,36). The level F = -1 (red) comes to a
cusp at P; the levels just above (green) and below (blue) are smooth. Every number on it (the orders, the
coefficients, the window) is computed by the script. Echo worth saying on the card: the paper's
construction STARTS from the cusp (u^3, -u^2) (paper.tex:84), and a cusp is what the obstruction looks
like.

## 5. Level up / who could use it

- Level up: the embedding problem for affine spaces is a central open question in affine algebraic
  geometry; an explicit witness gives a test object for invariants (Makar-Limanov, Derksen) and for the
  stable coordinate question (the same family 049 has a degree-5 stable-coordinate counterexample).
- Who could use it, honestly: computer algebra and polynomial-automorphism software, as a hard
  regression case (a zero set that IS affine space but a polynomial that is NOT a coordinate). Nothing
  outside mathematics near term.

## 6. Red flags

- n = 3 is not addressed (the paper says so); the classical question in dimension 3 stays open.
- The "not a coordinate" half is elementary enough to check by hand in an afternoon, which makes "why
  was this not found earlier?" the right question; I have no answer from the literature.
- The Lean evidence is my compile + #print axioms + a textual statement match, not the official
  Comparator run.
- The picture is a REAL two-dimensional slice of a complex threefold; it shows the cusp in that slice,
  not the whole singularity.
