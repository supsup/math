# Truffet's tropical LP algorithm: a 2-step counterexample, replicated twice

Lean: `lean/ComparatorChallenges/TruffetCounterexample.lean` (statement, proof `sorry`) and its solution
`lean/OAI/Optimization/Tropical/TruffetCounterexample.lean` + `TruffetModel.lean` (269 lines, a 2-module
dependency cone: the smallest-but-one in the whole Comparator set, see `../lean-cones/`).

## What it says, in my words

A max-plus ("tropical") linear program over values in R plus a bottom element (Lean `WithBot R`): a
form gives a coefficient for each of three columns (variables x0, x1 and a constant), and is evaluated
as max over columns of coefficient + value. A row is a constraint "rhs <= lhs". The algorithm being
tested eliminates variables one at a time by substituting a "lower" bound form, and stops when the
constant column satisfies every row.

The theorem builds a 2-variable, 2-row instance where the algorithm is FORCED (exactly one eligible
pivot at each step, no switch, no failure) through two substitutions to a final state and stops; reading
its answer back gives `output = (1, 0, 0)` with cost 1. But `better = (0, -1, 0)` is also feasible and
costs 0. So this execution of the algorithm is not optimal. It is a counterexample to a correctness
claim, made entirely of small explicit numbers.

## What I checked

Two independent replications of the challenge's DEFINITIONS, written from the Lean text, not from the
paper's prose and not from each other's output:

- `replicate.py` (Python, float with -inf as bottom)
- `../java/src/confluence/math/truffet/Truffet.java` (Java 25, records, double with NEGATIVE_INFINITY)

Both print all 13 conjuncts of `finite_execution_not_optimal` as holding, with costs 1.0 vs 0.0.

Negative controls, so a "yes" means something: forcing the wrong pivot (1,1) is rejected; the point
(5,5,0) is correctly infeasible; and (Java) pretending `better` costs 2 is correctly not cheaper.

## Limits, stated

- `crossRowRestriction` is "for every alpha there exists w". I only SAMPLE alpha over 11 values and search
  w on a small grid; that is evidence, not proof. The Lean proof is the proof for that conjunct.
- LEAN PROOF CHECKED in Docker (2026-10-08 12:23Z, see `../lean-docker/`): both modules compile against the
  pinned Mathlib, and the theorem depends on exactly [propext, Classical.choice, Quot.sound] (the challenge's
  permitted axioms), no sorryAx; a sorry control in the same file shows sorryAx. A textual comparison finds
  all 31 challenge declarations identical in the solution. Not the official Comparator run (which compares
  compiled terms), but compile + axioms + statement match.
- I checked that the theorem's statement holds. I did not check that the challenge's `State`/`advance`
  model is a faithful model of Truffet's published algorithm; that is a question about the paper.

## What I liked

The counterexample is small enough to do by hand: two variables, two rows, two steps. The interesting
part is not the arithmetic but the word FORCED: the theorem pins down that the algorithm had no other
legal choice at either step, so the bad answer is not bad luck in pivot selection. That is the same
shape as a good bug report: not "it can go wrong" but "it must go wrong, here is the only path".
