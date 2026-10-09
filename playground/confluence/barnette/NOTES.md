# Barnette's conjecture: statement audit and checks

Lean: `lean/ComparatorChallenges/BarnetteHamiltonian.lean` (statement, proof `sorry`). The `.json` names solution
module `OAI.Combinatorics.Hamiltonian.Main`, theorem `OAI.Barnette.main`. The cone is 31 modules, Mathlib-only,
with no `native_decide`.
Docs: `lean/docs/180.md`. Paper: `preprints/Paired-states-and-Hamiltonian-cycles-in-cubic-bipartite-planar-graphs-September-24-2026/`.

## What it says, in plain words

Every finite simple graph that is cubic (every vertex has degree 3), bipartite, planar and 3-vertex-connected
has a Hamiltonian cycle: one cycle that visits every vertex exactly once. That is Barnette's conjecture
(1969), stated in full. As of my knowledge (training data to June 2026) it was OPEN, verified by computer
only for small graphs, up to 90 vertices if I recall correctly (Brinkmann, Goedgebeur and McKay). **This
claims to settle it. A novelty and literature check is owed before any card says so.**

Each hypothesis is known to be necessary:
- Tutte's graph is cubic, planar and 3-connected but not bipartite, and not Hamiltonian.
- The Horton and Ellingham-Horton graphs are cubic, bipartite and 3-connected but not planar, and not Hamiltonian.

So the statement cannot be weakened to fewer hypotheses.

## Audit verdict

**Matches its name and its Scope.** It is a positive universal statement, so the risk direction is the
ordinary one: it would be cheap if a hypothesis were too STRONG (unsatisfiable, so vacuous) or the
conclusion too WEAK. I checked each:

- **`Planar`**, the existence of a `PlaneEmbedding`.
  - Vertices go to injective points of R^2. Each edge gets a continuous `Path` between its endpoints;
    the arc is injective (a simple curve) and avoids every other vertex. Distinct edges' arcs have
    disjoint interiors.
  - `arc_reverse` asks only that the two orientations of one edge be the same curve reversed.
  - This is the standard topological definition. It is satisfiable for real planar graphs: draw a
    convex polyhedron's Schlegel diagram with straight segments (cube, prisms). So it is not vacuous.
  - It is not weaker than planarity either, because crossings are ruled out by `interiors_disjoint`.
- **`ThreeVertexConnected`**: at least 4 vertices, and for every vertex set S with at most two elements,
  the induced graph on the rest is `Connected`. This is the standard definition, transcribed literally in
  the Java.
- **`HasHamiltonianCycle`**: Mathlib's `Walk.IsHamiltonianCycle`, a single closed walk through every
  vertex once. Its docstring stresses that this is not a spanning 2-factor (a union of cycles). That is the
  strong, correct conclusion.
- **Cubic and bipartite** are Mathlib's `IsRegularOfDegree 3` and `IsBipartite`, on any `Fintype` vertex
  type with decidable equality and adjacency. That is all finite simple graphs, with no size bound.

**My verdict: MATCHES (first reading, Confluence).** A second independent reader is owed before the trust
table carries it.

## Checks run

| Check | Result |
|---|---|
| Docker build, 8,955 jobs, Lean 4.34.1, Mathlib d13f23b7 | built |
| `#print axioms OAI.Barnette.main` | `[propext, Classical.choice, Quot.sound]`, permitted only |
| sorry control in the same run | `controlWithSorry` depends on `[sorryAx]`, so the instrument detects a sorry |
| `statement_match.py BarnetteHamiltonian` | 6 challenge declarations, 6 identical; 672 solution-only helpers |
| Java, 8 polyhedral Barnette graphs (even prisms with 8 to 32 vertices, the truncated octahedron) | each verified cubic, bipartite and 3-connected (literal Lean definition), each with a found and re-verified Hamiltonian cycle |
| Java controls | Petersen: cubic and 3-connected, not bipartite, and the search finds NO cycle; odd prism: not bipartite; two cubes on a 2-edge bridge: not 3-connected |

Log: `lean-docker/barnette-run.log`. Planarity of the Java graphs is by construction (convex polyhedra);
Java does not test planarity.

## Open

- Second reader.
- Novelty and literature check (claimed resolution of a 1969 conjecture, a September 2026 preprint).
- The paper's method ("paired states") was not read.
