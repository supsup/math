# A robust four-row permanent inequality: Lean checked, and where the exponent really has to be

Lean: challenge `lean/ComparatorChallenges/FourRowPermanent.lean`, solution `lean/OAI/Combinatorics/Permanent/`
(5 modules, 622 lines, Mathlib only). Java: `../java/src/confluence/math/permanent/FourRowPermanent.java`.

## The statement

Laws ν on the 24 permutations of 4 sites. Uniform marginals means every site i goes to every site j with
probability exactly 1/4. Row norms use the uniform normalization ‖g‖_p = ((1/4) Σⱼ g(j)^p)^{1/p}.

There exist p₀ with 4/3 < p₀ < 2 and ε > 0 such that, for every law with uniform marginals and total variation
distance < ε from uniform, and every nonnegative f:  E_ν[∏ᵢ fᵢ(π(i))] ≤ ∏ᵢ ‖fᵢ‖_{p₀}.

## Lean check (Docker, `../lean-docker/fourrow-run.log`, 2026-10-08 12:30Z)

- All 5 modules build against the pinned Mathlib `d13f23b7` (about 25 s of compile).
- `robust_permanent` depends on exactly [propext, Classical.choice, Quot.sound], the permitted axioms; the
  sorry control in the same file shows [sorryAx].
- Statement match (`../lean-docker/statement_match.py FourRowPermanent`): 10/10 challenge declarations
  identical in the solution (48 helpers added).
- The proof's witnesses: `strictExponent = 2 - 1/100000` and `robustRadius = 1/100000` (Main.lean:9, :11).

## The numerical part, which I enjoyed most

At the UNIFORM law the left side is perm(F)/24 (F[i][j] = fᵢ(j)), and both sides are homogeneous per row, so the
question is how large R_p(F) = perm(F)/24 / ∏ᵢ‖Fᵢ‖_p can get. The all-ones matrix gives R_p = 1 for every p.

A search (300 random starts with hill-climbing per p) found the worst case below the crossover to be a
PERMUTATION MATRIX, for which there is a closed form: perm = 1, each row has one nonzero entry, so

    R_p(permutation matrix) = 4^{4/p} / 24,

which equals 1 at **p\* = 4·ln 4 / ln 24 ≈ 1.744834**. Measured best R_p vs that formula:

| p | best found | 4^{4/p}/24 |
|---|---|---|
| 1 | 10.666667 | 10.666667 |
| 4/3 | 2.666667 | 2.666667 |
| 1.6 | 1.333333 | 1.333333 |
| 1.7 | 1.087428 | 1.087428 |
| p\*-0.01 | 1.018488 | 1.018488 |
| p\*+0.01 | 0.991595 | 0.982053 |
| 1.8 | 0.999997 | 0.907193 |
| 2 | 0.999987 | 0.666667 |

So, at the uniform law:
- for p < p\* the inequality FAILS, a permutation matrix being an explicit violator (this part is a closed
  form, so it is a proof, not a search result);
- for p >= p\* the search found nothing above 1, its best tending to the all-ones value 1 (evidence, not proof).

Hence any valid p₀ must be at least p\* ≈ 1.7448, even though the theorem only advertises 4/3 < p₀. I predicted
that BEFORE looking at the proof, then read it: the proof uses p₀ = 1.99999 and a helper lemma valid for
9/5 <= p <= 2 (Norm.lean:112). Both sit above p\*, so the numbers and the proof agree. The 4/3 in the statement is
a true but loose outer bound.

## Limits, stated

- I did not test the ROBUST part (laws ε-close to uniform with ε = 10^-5). The bound p\* is about the uniform law
  only; robustness can only push the required exponent up, which is consistent with the proof choosing p₀ near 2.
- "No violation for p >= p\*" is a search result, not a proof. The Lean proof is the proof, at p₀ = 1.99999.

## Why it is satisfying

The statement looks like it might be about some delicate analytic constant, but its failing side is explained by
the simplest object there is: one permutation. A random bijection hits the single nonzero pattern with probability
1/24, while the four row norms each shrink by 4^{-1/p}. Setting 4^{4/p} = 24 gives the threshold exactly.
