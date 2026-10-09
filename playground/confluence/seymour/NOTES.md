# Seymour's second-neighbourhood conjecture: statement audit and checks

Lean: `lean/ComparatorChallenges/SeymourSecondNeighborhood.lean` (statement, proof `sorry`). The `.json` names
solution module `OAI.Combinatorics.SecondNeighborhood.Main`, theorem
`OAI.SeymourSecondNeighborhood.exists_goodVertex`. The cone is 43 modules, Mathlib-only.
Docs: `lean/docs` (the Scope entry for this challenge). Paper: `preprints/A-proof-of-Seymours-second-neighborhood-conjecture-September-23-2026/`.

## What it says, in plain words

In every nonempty finite oriented graph (arcs, no loops, never both u -> v and v -> u), some vertex v has at
least as many vertices at directed distance exactly 2 as at distance 1. That is Seymour's
second-neighbourhood conjecture (1990), in full. As of my knowledge (training data to June 2026) it was
OPEN in general. It was known for tournaments (Fisher 1996, and Havet and Thomasse's median orders) and for
some other classes. **This claims to settle it. A novelty and literature check is owed.**

## Audit verdict

**Matches its name and its Scope.** It is a positive existence statement over all oriented graphs, so it
would be cheap if the hypothesis were too strong or the conclusion too weak. I checked each part:

- **`IsOriented`**: `loopless` and `asymmetric` (r u v implies not r v u). That is exactly an oriented graph.
  The relation is otherwise arbitrary, on any `Fintype` with decidable equality, and `Nonempty V` is required.
  The Java control shows that the asymmetry hypothesis is load-bearing: the complete symmetric digraph has
  no good vertex.
- **`firstNeighbors r v`**: every w with r v w.
- **`secondNeighbors r v`**: every w with w != v, not r v w, and some u with r v u and r u w. That is
  directed distance exactly 2, excluding v and its first neighbours, as the docs Scope says. It is not the
  weaker "reachable in two steps" (which would include first neighbours). The Java control counts how often
  that wrong reading would change a verdict: 10,999,816 of the 14,348,907 six-vertex graphs.
- **`GoodVertex`**: |first| <= |second|. A sink has |first| = 0 and is trivially good. The Scope says sinks
  are included, and the conjecture is stated that way.

**Verdict: MATCHES, read twice.** First reading, Confluence. Second reading, a Fixpoint skeptic (undervoice 16407), who re-derived the proof's inequalities by hand and found no gap; CONSISTENT. Showcase card 173.

## Checks run

| Check | Result |
|---|---|
| Docker build, 1,872 jobs, Lean 4.34.1, Mathlib d13f23b7 | built |
| `#print axioms ...exists_goodVertex` | `[propext, Classical.choice, Quot.sound]`, permitted only |
| sorry control in the same run | `controlWithSorry` depends on `[sorryAx]` |
| `statement_match.py SeymourSecondNeighborhood` | 5 challenge declarations, 5 identical; 327 solution-only helpers |
| Java, EXHAUSTIVE: every labelled oriented graph on n = 1..6 vertices (3^C(n,2), 14,348,907 at n = 6) | every one has a good vertex; 1.4 s |
| Java, EXHAUSTIVE at n = 7: all 10,460,353,203 labelled oriented graphs (3^21), `java ... SecondNeighborhood 7` | every one has a good vertex; 16 min 55 s, log `seymour/n7-run.log` |
| Java controls | the complete symmetric digraph (n = 2..6) has no good vertex; the wrong "two-step reach" definition changes a verdict in 10,999,816 six-vertex graphs |

Log: `lean-docker/seymour-run.log`.

## Open

- Novelty and literature check (claimed resolution of a 1990 conjecture, a September 2026 preprint).
- The paper's method was not read.
