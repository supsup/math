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
| `confluence.math.bogomolov` | `BogomolovPop` | A finite Kummer toy: automorphisms of F_q(x) are determined by their action on the Kummer piece modulo scalars, with coarse-invariant and mutant controls |
| `confluence.math.artin` | `ArtinCAT0` | The explicit 116-letter Coxeter matrix, braid relators checked in S_40, the exact CAT(0) comparison identity, and sphere and wrong-relator controls |
| `confluence.math.anderson` | `PlanarAnderson` | Jacobi eigenvalues of a random 2D Anderson box, a planted-patch Weyl bound, and periodic-potential controls |
| `confluence.math.naimark` | `Naimark` | Commutant dimensions by exact elimination: irreducible M_n, an amplified (reducible) copy, and the C+C control |
| `confluence.math.rokhlin` | `Rokhlin` | Exact Bernoulli cylinder probabilities, a cat-map Monte Carlo and the golden-rotation control for multiple mixing |
| `confluence.math.crouzeixhilbert` | `CrouzeixHilbert` | 2x2 closed-form numerical ranges and spectral norms: Crouzeix ratios <= 2, the J2 sharpness witness, and a 1.9 control |
| `confluence.math.crouzeix` | `HilbertCrouzeix` | 2x2 numerical ranges in closed form, convexity and spectral inclusion, with a missing-conjugate control |
| `confluence.math.commonbases` | `CommonBases` | Brute-force common-base counts by two channels (direct and the paired reduction with the dual), with a dual-swap control |
| `confluence.math.logbm` | `LogBrunnMinkowski` | Planar lower bounds for the L_0 combination of symmetric polygons, equality cases withheld, and a non-symmetric control |
| `confluence.math.grahamspherical` | `GrahamSpherical` | Exact checks of the 12 circle points, the derivation D u = -v, D v = u, and the weighted-energy invariant of isometric copies, with controls |
| `confluence.math.ramseynine` | `RamseyNine` | Exact BigInteger-rational check of the nine-point determinant certificate (det = 8^6) and four controls that must come out singular |
| `confluence.math.hadamard` | `HadamardCubeFiber` | Tao's 6x6 matrix and its equivalents satisfy the cube-fibre lemma; F6 and all-ones show which hypothesis each failure needs |
| `confluence.math.borsuk` | `BorsukNine` | Projector distance identity with a wrong-identity control, diameter sqrt 2 at orthogonal lines, a 9-dimensional affine span, and the exact chromatic number (5) of Peres' 24 rays as the finite-versus-continuum control |
| `confluence.math.barnette` | `Barnette` | The literal cubic, bipartite and 3-connected definitions on 8 polyhedral graphs (even prisms, the truncated octahedron), each with a verified Hamiltonian cycle; Petersen (no cycle found), odd-prism and cut-pair controls |
| `confluence.math.seymour` | `SecondNeighborhood` | Exhaustive check of every oriented graph on up to 6 vertices (14,348,907 at n = 6) for a good vertex, with the complete-symmetric-digraph and two-step-reach controls |

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
java -cp out confluence.math.commonbases.CommonBases
java -cp out confluence.math.crouzeix.HilbertCrouzeix
java -cp out confluence.math.crouzeixhilbert.CrouzeixHilbert
java -cp out confluence.math.rokhlin.Rokhlin
java -cp out confluence.math.naimark.Naimark
java -cp out confluence.math.anderson.PlanarAnderson
java -cp out confluence.math.artin.ArtinCAT0
java -cp out confluence.math.bogomolov.BogomolovPop
java -cp out confluence.math.abhyankar.AbhyankarSathaye
java -cp out confluence.math.congruencegraph.CongruenceGraph
java -cp out confluence.math.triangularcovering.TriangularCovering
java -cp out confluence.math.clausethreshold.FixedClauseThreshold
java -cp out confluence.math.midpointlenses.MidpointLenses
```

Every example prints its own negative controls, so a pass can be told apart from a check that cannot fail.
`out/` is build output.

Each class Javadoc (markdown `///`) ends with a "What this could mean for Java code" section (Charles asked for one): concrete consequences for Java programs and tests, labelled as possible uses I can defend, not claims from the paper.
