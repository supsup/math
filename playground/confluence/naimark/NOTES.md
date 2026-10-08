# Naimark (OAI.NaimarkZFC.main): verification notes

Challenge: `lean/ComparatorChallenges/Naimark.lean` (+ `.json`, solution module
`OAI.Analysis.Naimark.Tracial`, 16-module Mathlib-only cone, about 26k lines).
Paper: `preprints/A-counterexample-to-Naimarks-problem-in-ZFC-September-24-2026/` (read for
context only: the abstract, the introduction and the outline; the proofs were not checked by hand).

## The statement in plain words

There is a unital, infinite-dimensional, simple complex C\*-algebra A with a faithful tracial
state, such that any two irreducible representations of A, on any two Hilbert spaces (in any
universes), are unitarily equivalent; and A is not \*-isomorphic to the compact operators K(H)
on any Hilbert space H.

That is a counterexample to Naimark's problem, plus extras (unital, simple, tracial), proved
with no set-theoretic hypothesis beyond Lean's own foundations.

```lean
theorem main :
    ∃ (A : Type u) (_ : CStarAlgebra A),
      IsSimpleCStar A ∧ ¬ FiniteDimensional ℂ A ∧
      (∃ τ : A →L[ℂ] ℂ, IsFaithfulTracialState τ) ∧
      HasUniqueIrreducibleRepresentation.{u, v, w} A ∧
      ∀ (H : Type v) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H],
        ¬ IsIsomorphicToCompacts A H
```

## Statement audit (adversarial): verdict FAITHFUL

I checked each definition against the standard one.

| Definition (challenge) | Reading | Standard? |
| --- | --- | --- |
| `CStarAlgebra A` (Mathlib) | extends `NormedRing` (so it has a 1), `StarRing`, `CompleteSpace`, `CStarRing`, `NormedAlgebra ℂ`, `StarModule ℂ`. So **unital**. The non-unital class is `NonUnitalCStarAlgebra`. | yes (unital C\*-algebra) |
| `IsSimpleCStar A := Nontrivial A ∧ ∀ I : TwoSidedIdeal A, IsClosed I → I = ⊥ ∨ I = ⊤` | no proper nonzero closed two-sided ideal; A ≠ 0 | yes |
| `IsState f := ‖f‖ = 1 ∧ ∀ a, (f (a⋆a)).im = 0 ∧ 0 ≤ (f (a⋆a)).re` | norm-one positive functional | yes |
| `IsFaithfulTracialState f := IsState f ∧ f(ab)=f(ba) ∧ ∀ a ≠ 0, 0 < (f (a⋆a)).re` | faithful trace | yes |
| `IsIrreducible π := π ≠ 0 ∧ ∀ M closed submodule, π-invariant → M = ⊥ ∨ M = ⊤`, π : `A →⋆ₙₐ[ℂ] (H →L[ℂ] H)` | nonzero, topologically irreducible \*-representation. π need not be unital, but for unital A, π(1) is an invariant projection, nonzero since π ≠ 0, hence 1. The zero space is excluded by π ≠ 0. | yes |
| `UnitarilyEquivalent π ρ := ∃ U : H ≃ₗᵢ[ℂ] K, ∀ a x, U (π a x) = ρ a (U x)` | unitary intertwiner | yes |
| `HasUniqueIrreducibleRepresentation.{u,v,w} A := ∀ H : Type v, ∀ K : Type w, ∀ π ρ, IsIrreducible π → IsIrreducible ρ → UnitarilyEquivalent π ρ` | any two irreducibles are equivalent, on **arbitrary** Hilbert spaces of any cardinality (any type in the universe) | yes, see below |
| `IsIsomorphicToCompacts A H := ∃ φ, Injective φ ∧ ∀ T, (T ∈ range φ ↔ IsCompactOperator T)` | A ≅ K(H) as \*-algebras | yes |

The traps the brief listed, one by one:

- **Representations on a fixed space or a fixed universe.** No. `H` and `K` range over every
  complete inner product space in universes `v` and `w`, and `main` is universe-polymorphic in
  `u v w`, so the proof must work for every choice, including `u = v = w = 0`. The solution
  builds `X : Type` (universe 0, `TracialStage.carrier : Type`) and takes `A := ULift.{u} X`.
  The vacuity attack ("make A too big to act on any H in universe v, so it has no irreducible
  representations there") is not available: for `v = 0`, H ranges over all of `Type`, which
  contains GNS spaces of `X`.
- **Vacuous uniqueness.** The formal statement only says "any two irreducibles are equivalent";
  it does not assert that one exists. For a nonzero C\*-algebra one always exists (GNS of a pure
  state), and `IsSimpleCStar` includes `Nontrivial`, so this is a standard fact, not a hole.
  It is not itself proved inside `main`, but it is not needed for the statement to mean
  "exactly one up to equivalence".
- **"Irreducible" weaker than standard.** No. It is topological irreducibility plus π ≠ 0, the
  standard definition (and the paper's, Introduction).
- **x/0, sSup/sInf, trivial algebra.** None of these occur in the statement. The trivial algebra
  is excluded by `Nontrivial` and by `¬ FiniteDimensional`.
- **The last conjunct is weak.** True but harmless: since A is unital and infinite-dimensional,
  `¬ IsIsomorphicToCompacts A H` is automatic (K(H) is unital only when H is finite-dimensional),
  and the solution proves it from `hinf` alone (`not_isIsomorphicToCompacts hinf H`). The paper
  says the same. The content of the theorem is the other four conjuncts.
- **Unital is a restriction?** It makes the counterexample stronger, not weaker: Naimark's
  question is about arbitrary C\*-algebras, and one unital counterexample answers it.
- **Instances inside the existential.** The `CStarAlgebra` instance is part of the witness, and
  every later conjunct elaborates against it. The solution's local `PartialOrder` /
  `StarOrderedRing` instances do not occur in the statement.

## Relation to Naimark's problem and to Akemann-Weaver

Akemann and Weaver (2004) built a counterexample from the diamond principle and showed that
"there is a counterexample generated by aleph_1 elements" is independent of ZFC. That does NOT
make the unrestricted existence statement independent: as far as I know, unrestricted existence
in ZFC was open. So a Lean proof of `main` does not contradict any known independence result.
The construction here has length c^+ (c = 2^aleph_0). Under CH c^+ = aleph_2, so nothing forces
the algebra to be aleph_1-generated. The paper says explicitly that it makes no claim about the
density.

How the proof avoids diamond (from the paper's outline, and visible in the Lean): diamond is used
by Akemann-Weaver to guess the pure states of the limit algebra. Here every pure state of a stage
is determined by its restriction to a separable, dependency-closed subalgebra, which it is the
unique extension of (`literal_countable_determination`, `Omission.lean`). That bounds the pure
states of each stage by c (`literal_pureStates_le_continuum`). With c^+ steps and a pairing
schedule, every pure state is treated. Kishimoto-Ozawa-Sakai homogeneity (`KOS.homogeneity`) and
reduced HNN extensions join one pair of inequivalent pure states at each step.

The paper also cites a ZFC construction by "Tanaka 2026" with the same conclusion. I could not
check that reference; it is after my knowledge cutoff.

**Foundations.** Lean's type theory is stronger than ZFC (it proves the consistency of ZFC plus
countably many inaccessibles). So a Lean proof shows the statement in that stronger theory. To
say "in ZFC" one also needs the proof not to use universes in an essential way. The construction
lives in universe 0 (`Ordinal.{0}`, `constructionCardinal := Order.succ 𝔠`, carriers in `Type`),
and nothing I saw uses a universe as a set. But I did not audit all 26k lines for this. This is
the usual caveat for Mathlib results, not a defect I found.

## Kernel check (Docker, Lean 4.34.1, Mathlib d13f23b)

Log: `playground/confluence/lean-docker/naimark-run.log`. The run copied 16 modules and built all
of them (`Build completed successfully (8940 jobs)`). The slowest module was HNN, at 225 s.

```
'OAI.NaimarkZFC.main' depends on axioms: [propext, Classical.choice, Quot.sound]
Check.lean:6:8: warning: declaration uses `sorry`
'controlWithSorry' depends on axioms: [sorryAx]
```

These axioms are exactly the JSON's `permitted_axioms`. There is no `sorryAx`. The negative
control shows `sorryAx`, so the instrument can detect a `sorry`.

## Textual statement match

`python3 -I playground/confluence/lean-docker/statement_match.py Naimark`:
`identical: 8  differ: 0  missing from solution: 0`.

Independent of the matcher: I extracted the seven `def`s from the challenge and from
`OAI/Analysis/Naimark/Basic.lean` with `sed` and ran `diff`. The only difference was the
challenge's trailing `theorem main ... sorry` block, which my range included on one side. The
`theorem main` statement lines also `diff` identical against `Tracial.lean`. `Basic.lean`
imports only Mathlib and opens nothing before the definitions. `Tracial.lean` has
`open ... Classical`, `open scoped CStarAlgebra ComplexOrder` above `main`. These affect
notation and instances on ℂ, and none of them occur in `main`'s statement. A textual match is
not a term-level Comparator check.

Constructs grep: no `sorry`, `axiom`, `native_decide`, `implemented_by`, `extern`, `unsafe`,
`opaque`, `ofReduceBool`, `run_cmd`, `#eval`, `elab` or `macro` in the 16 Naimark files.

## Finite-dimensional checks of the definitions (not of the theorem)

`checks.py` (numpy). Run with `python3 checks.py` from this folder. All PASS:

- M_n (n = 1..4): the defining representation has commutant dimension 1, so it is irreducible.
  A rotated copy U(.)U\* is irreducible, with a 1-dimensional intertwiner space, and U
  intertwines. The k-fold amplification has commutant M_k (dim k^2) and Hom(defining, amplified)
  of dim k: every representation is a multiple of the defining one.
- M_n satisfies simplicity, has a faithful tracial state, and is K(C^n). Only
  `¬ FiniteDimensional` excludes it, so that conjunct is load-bearing.
- **NEGATIVE CONTROL, C ⊕ C:** both characters are irreducible and Hom(chi1, chi2) = 0, so the
  uniqueness hypothesis FAILS, as it must. Its defining diagonal representation is reducible
  (commutant dim 2), and C ⊕ C is not simple. These non-1 results also show the commutant
  instrument can report "reducible".

Java: `playground/confluence/java/src/confluence/math/naimark/Naimark.java`: the same commutant
test by real Gaussian elimination (exact for these real generators). M_2 and M_3 give 1, the
doubled M_2 gives 4, the diagonal C ⊕ C gives 2, and the characters of C ⊕ C are inequivalent.
All PASS.

## LIMITS / could not determine

- I did not check the mathematics of the 26k-line proof by hand. Correctness rests on the Lean
  kernel check above.
- Comparator itself was not run. The statement match is textual plus a manual diff.
- "In ZFC" versus "in Lean's foundations": see Foundations above. I did not audit for essential
  use of universes.
- I did not verify Tanaka 2026, Calderon-Farah 2022 Prop 7.2, or the other citations.
- The finite-dimensional checks test the definitions only. No finite computation bears on the
  theorem.

## Confluence's recheck

- Read the definitions myself (challenge lines 21-41): IsIrreducible = nonzero and no closed invariant subspace
  besides 0 and everything; UnitarilyEquivalent = a linear isometric equivalence intertwining the two;
  HasUniqueIrreducibleRepresentation.{u,v,w} ranges over ALL Hilbert spaces H : Type v and K : Type w. `main` is
  universe-polymorphic, so it holds at every v, w, including universes large enough for any GNS space of A: no
  universe-size escape. The last conjunct (not isomorphic to any K(H)) is automatic for a unital
  infinite-dimensional algebra, as the report says; the content is simplicity, the faithful trace and uniqueness.
- Build log: `Build completed successfully (8940 jobs)`; `main` on [propext, Classical.choice, Quot.sound];
  sorry control on [sorryAx]. statement_match 8/8.
- Foundations caveat kept: Lean's type theory is stronger than ZFC (consistency strength around ZFC plus
  countably many inaccessibles), so "in ZFC" is the paper's claim, not something this check certifies.
- Caption level as agreed: "the collection's Lean artifact kernel-checks this formal statement".
