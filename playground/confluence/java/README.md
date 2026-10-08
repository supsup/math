# Java examples (Confluence's math playground)

Charles: "in your playground could you try to make java examples of them as you review" and "please keep
all java examples in their own folder/package". So every Java example lives here, one package per
reviewed result, under `confluence.math.<topic>`.

| Package | Class | What it does |
|---|---|---|
| `confluence.math.truffet` | `Truffet` | Replicates the 13-conjunct Lean theorem that Truffet's tropical LP algorithm is forced to a non-optimal answer |
| `confluence.math.permanent` | `FourRowPermanent` | Searches perm(F)/24 / prod row norms; finds the exponent floor 4 ln4/ln24 via permutation matrices |
| `confluence.math.sidorenko` | `SidorenkoPattern` | Checks the Sidorenko counterexample's pattern graph H from its table; exact t(H,W)/(EW)^66 for tiny kernels |
| `confluence.math.planecoloring` | `PlaneColoring` | The proof's 7-colouring of the plane (lattice spacing 4/5, colour (a+3b) mod 7, disks of radius 7/15): exact side conditions, random and boundary unit pairs, 6 controls |
| `confluence.math.midpointlenses` | `MidpointLenses` | Exact rational lower and upper bounds pinning segment-dual norms on small trees, with a wrong-constant and an l1 control |
| `confluence.math.clausethreshold` | `FixedClauseThreshold` | Exact satisfiable-formula counts by DP over surviving assignments, a seeded DPLL Monte Carlo, and a wrong-bound control |
| `confluence.math.triangularcovering` | `TriangularCovering` | Exact BigInteger rationals: tetrahedron shadows, cylinder base areas against Lean's closed form, sampled coverage, and an uncovered-point control |
| `confluence.math.congruencegraph` | `CongruenceGraph` | Exhaustive check that representable lattices and the colouring criterion agree on small sizes, with a dropped-condition control |
| `confluence.math.abhyankar` | `AbhyankarSathaye` | Sparse integer polynomials: the cusp and ambient identities, the singular fibre, and the inverse map mod p, with controls |
| `confluence.math.logbm` | `LogBrunnMinkowski` | Planar lower bounds for the L_0 combination of symmetric polygons, equality cases withheld, and a non-symmetric control |
| `confluence.math.grahamspherical` | `GrahamSpherical` | Exact checks of the 12 circle points, the derivation D u = -v, D v = u, and the weighted-energy invariant of isometric copies, with controls |
| `confluence.math.ramseynine` | `RamseyNine` | Exact BigInteger-rational check of the nine-point determinant certificate (det = 8^6) and four controls that must come out singular |
| `confluence.math.hadamard` | `HadamardCubeFiber` | Tao's 6x6 matrix and its equivalents satisfy the cube-fibre lemma; F6 and all-ones show which hypothesis each failure needs |

Build and run (JDK 25; plain javac, no build tool):

```sh
cd java
javac -d out $(find src -name "*.java")
java -cp out confluence.math.truffet.Truffet
java -cp out confluence.math.sidorenko.SidorenkoPattern
java -cp out confluence.math.permanent.FourRowPermanent
java -cp out confluence.math.planecoloring.PlaneColoring
java -cp out confluence.math.hadamard.HadamardCubeFiber
java -cp out confluence.math.ramseynine.RamseyNine
java -cp out confluence.math.grahamspherical.GrahamSpherical
java -cp out confluence.math.logbm.LogBrunnMinkowski
java -cp out confluence.math.abhyankar.AbhyankarSathaye
java -cp out confluence.math.congruencegraph.CongruenceGraph
java -cp out confluence.math.triangularcovering.TriangularCovering
java -cp out confluence.math.clausethreshold.FixedClauseThreshold
java -cp out confluence.math.midpointlenses.MidpointLenses
```

Every example prints its own negative controls, so a pass can be told apart from a check that cannot fail.
`out/` is build output.

Each class Javadoc (markdown `///`) ends with a "What this could mean for Java code" section (Charles asked for one): concrete consequences for Java programs and tests, labelled as possible uses I can defend, not claims from the paper.
