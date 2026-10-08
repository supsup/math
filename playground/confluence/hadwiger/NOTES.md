# A counterexample to Hadwiger's conjecture (Comparator: HadwigerCounterexample)

Paper: `preprints/A-counterexample-to-Hadwigers-conjecture-September-23-2026/`. Lean solution:
`lean/OAI/Combinatorics/HadwigerCounterexample/` (about 290 files, 38,704 lines; the theorem's cone is
288 modules, all Mathlib).

## The statement, in plain words

Hadwiger's conjecture (1943): every graph with chromatic number k has the complete graph K_k as a minor,
i.e. chi(G) <= h(G). The challenge claims it is FALSE:

- `not_hadwiger_conjecture : ¬ ∀ m (G : SimpleGraph (Fin m)), G.chromaticNumber ≤ hadwigerNumber G`
- `exists_counterexamples M`: for arbitrarily large m there is a graph on m vertices with
  - independence number at most 2 (no three pairwise non-adjacent vertices),
  - Hadwiger number below 26m/75 + 2/3 (about 0.347m),
  - chromatic number at least m/2,
  - and the "connected matching number" below m/100.

With independence number at most 2, each colour class has at most 2 vertices, so chi >= m/2 is free.
The real content is the minor bound: these graphs have no K_{m/2} minor. That refutes the special case
of Hadwiger for independence number 2, itself an open conjecture (Seymour's survey; Plummer, Stiebitz
and Toft) that such graphs have a K_{ceil(m/2)} minor. The known unconditional bound for that class is
about m/3 (Duchet and Meyniel), and 26/75 = 0.3467 sits just above 1/3, so the numbers do not collide
with anything already proved.

## Definitions I read for faithfulness (by hand; this is where a formal result can quietly go wrong)

- `HasCliqueMinor G t`: t branch sets, each inducing a CONNECTED subgraph, pairwise disjoint, and
  pairwise joined by an edge. Mathlib's `Connected` includes `Nonempty`, so empty branch sets are
  excluded (otherwise every graph would have every minor).
- `hadwigerNumber = sSup {t | HasCliqueMinor G t}` over ℕ. In Lean `sSup` of an UNBOUNDED set of
  naturals is 0, which would make the conjecture trivially false. Here the set is bounded (disjoint
  nonempty branch sets number at most m) and nonempty (t = 0 holds vacuously), so sSup is the true
  maximum. This was the first trap I checked.
- The direction is the conjecture's: chi <= h, negated.
- `chromaticNumber.toNat` maps ⊤ to 0; the statement separately asserts `chromaticNumber ≠ ⊤` and that
  it equals its toNat, so the conversion cannot hide an infinite chromatic number.

## What I checked

| Check | Result |
|---|---|
| Docker build, pinned Lean 4.34.1 + Mathlib d13f23b7, 288-module cone | `Build completed successfully (9212 jobs)`, about 3.5 minutes with cached Mathlib |
| `#print axioms exists_counterexamples` | `[propext, Classical.choice, Quot.sound]` |
| `#print axioms not_hadwiger_conjecture` | `[propext, Classical.choice, Quot.sound]` |
| sorry control beside them | `[sorryAx]` (the check can fail) |
| `grep` for `axiom`, `native_decide`, `sorry` in the solution folder | none |
| statement_match | 6/6 identical, after fixing two instrument false findings (below) |

Log: `../lean-docker/hadwiger-run.log`.

statement_match first reported 2 differences. Both were mine: the next declaration's doc comment was
glued onto `IsTouchingMatching`'s body, and `(m:ℕ)(G:` vs `(m : ℕ) (G :` counted as different. The
script now drops comments and ignores spacing next to brackets, colons and commas; controls show a
changed constant, a changed relation and merged identifiers are still caught.

## Limits

- The construction is PROBABILISTIC (`SampledGraphs`, mixers, entropy bounds): the proof shows suitable
  graphs exist without writing one down. So unlike Truffet, Sidorenko or the plane colourings there is
  no explicit object here for Python or Java to replicate, and I did not attempt to.
- A textual statement match is not the Comparator's term-level check, and I did not run the Comparator.
- The axioms line rules out sorry and extra axioms in the theorem's dependencies. It does not check that
  the definitions mean what the paper's prose says; that part is my reading above.
- I did not read the 38,704-line proof. The Lean kernel checked it; my contribution is that the
  statement it checked is the one the title claims.
