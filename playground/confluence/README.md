# Confluence's math playground

Charles, 2026-10-08: "pause stafficy work, and play around / learn from coderefs/math -- create a
folder playground that has notes and fun things you try". Fixpoint has a sibling folder
(`../fixpoint/`); I do not touch it. Charles also said Docker containers are fine for isolating
replications, and asked for Java examples, each in its own folder/package (all under `java/`).

## Where this lives

Moved 2026-10-08 (Charles: "checkout https://github.com/supsup/math in your commanders folder -- make your own branch and
move your stuff there"): my own clone of the fork at `commander-worktrees/confluence/math`, branch
`confluence/playground`. Nothing is pushed; Charles walks through it before anything goes to the remote. Scripts derive
the repo root from their own location, so they work from any checkout.

## How I am treating this collection

The repo's own README says these 722 manuscripts were produced by an internal OpenAI model, that
"some of the unformalized results could have issues", and that many but not all have Lean
formalizations. So nothing here is taken on trust: I prefer results with an explicit finite object I
can CHECK by computation, I say what I checked and what I did not, and a claim I only read stays
labelled as the paper's claim. There is no Lean toolchain on this host, so Lean proofs are built in a
Docker container (`lean-docker/`); the computational replications are Python and Java.

## Layout

| Folder | What |
|---|---|
| [sidorenko/](sidorenko/) | Notes + Python for the Sidorenko counterexample |
| [truffet/](truffet/) | Notes + Python for the Truffet tropical-LP counterexample |
| [permanent/](permanent/) | Notes for the robust four-row permanent inequality |
| [plane-coloring/](plane-coloring/) | Notes + Python for the plane 7-colouring (Hadwiger-Nelson upper bound) |
| [midpoint-lenses/](midpoint-lenses/) | Notes, exact Python and an SVG picture for the midpoint-lens tail bound in James-tree duals |
| [clause-threshold/](clause-threshold/) | Notes + exact DP and Monte Carlo for the random k-SAT threshold claim |
| [triangular-covering/](triangular-covering/) | Notes + exact Python for covering a tetrahedron by triangular cylinders below half the shadow cost |
| [congruence-graph/](congruence-graph/) | Notes + exhaustive Python for the finite congruence-lattice graph criterion |
| [abhyankar-sathaye/](abhyankar-sathaye/) | Notes + Python for the claimed Abhyankar-Sathaye counterexample in dimension 4 |
| [bogomolov-pop/](bogomolov-pop/) | Notes + a finite toy for the uniqueness half of Bogomolov-Pop reconstruction |
| [artin-cat0/](artin-cat0/) | Notes + exact checks for an Artin group with no geometric CAT(0) action |
| [mub-six/](mub-six/) | Notes for the mutually unbiased bases bound in C^6 |
| [planar-anderson/](planar-anderson/) | Notes + random-box spectra for the 2D Anderson almost-sure spectrum |
| [naimark/](naimark/) | Notes + finite-dimensional definition checks for the counterexample to Naimark's problem |
| [rokhlin/](rokhlin/) | Notes + exact and Monte Carlo illustrations for Rokhlin's multiple-mixing problem |
| [crouzeix-hilbert/](crouzeix-hilbert/) | Notes + Python for the complete Crouzeix inequality with constant 2 on Hilbert space |
| [hilbert-crouzeix/](hilbert-crouzeix/) | Notes, Python and an SVG for numerical-range geometry (Crouzeix support lemmas) |
| [common-bases/](common-bases/) | Notes + Python for the FPRAS for common bases of two matroids |
| [log-brunn-minkowski/](log-brunn-minkowski/) | Notes + Python for the origin-symmetric log-Brunn-Minkowski inequality |
| [graham-spherical/](graham-spherical/) | Notes + exact Python for an explicit 12-point spherical set that is not Ramsey (Graham's conjecture refuted) |
| [ramsey-nine/](ramsey-nine/) | Notes + Python for the nine-point non-Ramsey circle configuration |
| [hadwiger/](hadwiger/) | Notes for the Hadwiger's conjecture counterexample (statement read by hand, Lean build) |
| [hadamard-cube-fiber/](hadamard-cube-fiber/) | Notes + Python for the 6x6 Hadamard cube-fibre lemma |
| [lean-docker/](lean-docker/) | Container scripts + logs for checking Lean proofs (no Lean on the host) |
| [lean-cones/](lean-cones/) | Script measuring each Comparator challenge's dependency cone (which formal results are cheap to check) |
| [java/](java/) | ALL Java examples, one package per result (`confluence.math.*`) |

## Results so far

| Result | Checked | Outcome |
|---|---|---|
| Sidorenko counterexample: structure of H | Python + Java, from the paper's table incl. its opposite-face columns | Every stated property holds (35 vertices, 66 edges, connected, 33 pairs each in exactly 2 faces, 0 table mismatches) |
| Sidorenko: can a tiny kernel already violate it? | Python (2x2..3x3) + Java (2x2..2x4), exact computation + search | No: minimum ratio 1.000 (search collapses toward a constant kernel). Consistent with the paper needing a large construction; NOT a check of the paper's kernel |
| Truffet counterexample (Lean theorem `finite_execution_not_optimal`) | Python + Java replications of the Lean definitions, with negative controls | All 13 conjuncts hold: forced execution stops at cost 1, a feasible point costs 0. One conjunct (for-all/exists) only sampled |
| Truffet: does the Lean PROOF check? | Docker, pinned Lean 4.34.1 + Mathlib d13f23b7, build + `#print axioms` + sorry control; textual statement match | Proved: axioms exactly [propext, Classical.choice, Quot.sound], no sorryAx (control shows sorryAx); 31/31 declarations match the challenge |
| Robust four-row permanent (Lean `robust_permanent`) | Docker build + axioms + sorry control; statement match; Java search with a closed form | Proved: permitted axioms only, 10/10 declarations match. At the uniform law the inequality FAILS for p < 4 ln4/ln24 = 1.7448 (permutation matrix, closed form); proof's witness p0 = 1.99999 sits above it |
| Plane 7-colouring (Lean `properColoring_seven`) | Docker build + axioms + sorry control; statement match; Python + Java over all admissible colour choices; my own independent recheck | Proved: permitted axioms only, 3/3 declarations match. 0 clashes in 1.4M unit pairs incl. boundary pairs; 6 controls fire (wrong spacing, wrong rule, 6 colours, broken instrument). Built by a sub-agent, rechecked by me |
| 6x6 Hadamard cube fibres (Lean `rowRatio_cubeFiber_sum_zero`) | Docker build + axioms + sorry control; statement match; Python + Java on Tao's matrix, equivalents, standard families; my own recheck | Proved: permitted axioms only, 8/8 match. BUT the H∘H hypothesis forces Tao's matrix, where no row pair has two cube values, so matrix tests reach only the trivial case; the real content shows only on vectors. Built by a sub-agent, rechecked by me |
| Plane is not 5-colourable (Lean `no_proper_five_coloring`, family 158, chi(R^2) >= 6) | Docker build of the 70-module cone + axioms + sorry control; statement read by hand | Proved: permitted axioms only (control shows sorryAx). The colouring is an ARBITRARY function C -> Fin 5, so the measurable-to-arbitrary transfer (`proper_to_borel_weak`) is inside the checked proof. statement_match reports 2 differences that are only renamed bound variables (`point`/`x`, `coloring`/`c`), which the textual tool cannot see through; I read both by hand. Not a check of the paper's prose |
| Hadwiger's conjecture is false (Lean `not_hadwiger_conjecture`, `exists_counterexamples`) | Docker build of the 288-module cone + axioms + sorry control; definitions read by hand (sSup over ℕ bounded, nonempty branch sets, direction, toNat guard); statement match 6/6 | Proved: permitted axioms only for both theorems. Probabilistic construction, so no explicit graph to replicate; I checked the statement, not the 38,704-line argument |
| Nine points on a circle are not Ramsey (Lean `nine_circle_configuration`) | Docker build + axioms + sorry control; statement match 5/5; Python + Java exact-rational replication of the determinant certificate; my own recheck | Proved: permitted axioms only. The certificate det = 8^6 on the grid (0,1,-1)^2 reproduced exactly; controls (U = T, repeated parameter, perturbed grid) all singular. The deep step (Ramsey implies the field criterion) is checked only by Lean. Built by a sub-agent, rechecked by me |
| Abhyankar-Sathaye conjecture fails over C for n >= 4 (Lean `exists_noncoordinate_polynomial`) | Docker build + axioms + sorry control; statement match 1/1; Python + Java exact and modular checks of the explicit degree-17 F, its inverse map and the singular fibre; my own recheck from the Lean definitions | Proved: permitted axioms only. F = -1 is singular at (2, 0, -1/2, 1/2) (so F is not a coordinate), checked exactly twice; F = 0 has p^3 points over F_p and the explicit inverse round-trips. Whether experts accept it is beyond computation. Built by a sub-agent, rechecked by me |
| Finite congruence lattices: a colouring criterion (Lean `graph_criterion`) | Docker build + axioms + sorry control; statement match 11/11; exhaustive Python + Java over all lattices up to size 7 and carriers up to 4 (size 5 up to 5 points); my own recheck of the control | Proved: permitted axioms only. Both sides agree on all 312 (lattice, n) pairs; dropping condition 5 makes them disagree (explicit M4 case, rechecked by me). A reformulation, not a solution, of the open Finite Lattice Representation Problem. Built by a sub-agent, rechecked by me |
| Triangular cylinders cover a tetrahedron for less than half (Lean `TriangularCovering.main`) | Docker build + axioms + sorry control; statement match 17/17; exact-rational Python + Java of the cover at eps = 1/2001 (16,016,004 cylinders), the area expansion and the shadow minimum; my own recheck | Proved: permitted axioms only. Refutes the half-area cylinder covering conjecture for the regular tetrahedron; cover sampled at 10,660 points, uncovered-point controls exact. Built by a sub-agent, rechecked by me |
| Random k-SAT has a sharp fixed threshold for every k >= 3 (Lean `FixedClauseThreshold.main`) | Docker build + axioms + sorry control; statement match 9/9; exact integer DP (Python = Java) for small n, closed form at n = 3, seeded Monte Carlo with Wilson intervals; my own recheck | Proved: permitted axioms only. The statement is the full satisfiability threshold conjecture, k = 3 included. No value of alpha is claimed; finite checks cover definitions only. Built by a sub-agent, rechecked by me |
| Midpoint lenses in James-tree duals (Lean `midpoint_lens_main`) | Docker build + axioms + sorry control; statement match 35/35; exact-rational Python + Java on trees up to 5 vertices; my own recheck of the two-vertex instance | Proved: permitted axioms only. The tail bound 2 sqrt(R^2 - ||x||^2) holds on every certified instance; a closed form shows no constant below sqrt 2 works. Built by a sub-agent, rechecked by me |
| An explicit 12-point spherical set that is not Ramsey (Lean `GrahamSpherical.full_main`) | Docker build + axioms + sorry control; statement match 13/13; exact Python + Java of the points, the derivation identities and the copy invariant; my own recheck with independently built copies | Proved: permitted axioms only. 50 colours avoid every congruent copy in every dimension, refuting Graham's conjecture with an explicit set (the paper credits Palvolgyi with the first refutation). The derivation on R and t's transcendence are Lean/Mathlib only. Built by a sub-agent, rechecked by me |
| The log-Brunn-Minkowski conjecture, origin-symmetric, all dimensions (Lean `LogBrunnMinkowski.main`) | Docker build + axioms + sorry control; statement read by hand and matched 7/7 (after three matcher fixes); Python + Java planar bounds and 3D quadrature; my own planar recheck | Proved: permitted axioms only. The statement is the full BLYZ conjecture, not a special case; symmetric planar cases hold with margins up to 17%, and a non-symmetric control fails. One 24,490-line file; the kernel's word is the only proof check. Built by a sub-agent, rechecked by me |
| An FPRAS for counting common bases of two matroids (Lean `common_bases_fpras`) | Docker build + axioms + sorry control; statement read by hand (machine model, per-tape time bound, fair-coin probability) and matched 15/15; brute-force counts by two channels in Python + Java; my own statement recheck | Proved: permitted axioms only. The statement is a real FPRAS: one fixed program, polynomial step and oracle budget on every tape, (1 +- eps) with probability 1 - delta. Degree and constant unknown; the chain's mixing is the kernel's word. Built by a sub-agent, rechecked by me |
| Numerical-range geometry for Hilbert-space operators (Lean `HilbertCrouzeix`, four theorems) | Docker build + axioms + sorry control; statement match 30/30; Python + Java numerical ranges with three controls; my own recheck of the Jordan-block values | Proved: permitted axioms only. Classical support results (Toeplitz-Hausdorff, spectrum in the closure of W, finite compression), NOT Crouzeix's conjecture itself, which is the separate challenge CrouzeixHilbert. Built by a sub-agent, rechecked by me |
| Crouzeix's conjecture with constant 2, complete (matrix-valued), on any Hilbert space (Lean `CrouzeixHilbert.hilbert`) | Docker build + axioms + sorry control; statement match 25/25; the contour and calculus definitions read by hand for junk branches; Python ratios and a Dunford-integral cross-check, Java 2x2 closed form; my own recheck | Proved: permitted axioms only. The conclusion asserts the contour exists and the calculus is contour-independent, so no junk value trivialises the bound; J2 attains 2 exactly. (Constant 2 for matrices was proved independently by Lorist-Schwenninger, arXiv 2608.03841, Aug 2026; the collection's claim is the complete, all-operator version.) Caption level: kernel-checks the formal statement, pending review. Built by a sub-agent, rechecked by me |
| Every invertible mixing transformation is mixing of all orders (Lean `Rokhlin.mixing_all_finite_orders`) | Docker build + axioms + sorry control; statement read by hand (all measurable sets, all k >= 3, every gap to infinity) and matched 5/5; Python + Java illustrations with an irrational-rotation control; my own statement recheck | Proved: permitted axioms only. The statement is Rokhlin's 1949 problem in full. Numerics only illustrate the definitions (Bernoulli, cat map, rotation control). Caption level: kernel-checks the formal statement. Built by a sub-agent, rechecked by me |
| A counterexample to Naimark's problem without extra axioms (Lean `NaimarkZFC.main`) | Docker build + axioms + sorry control; definitions read by hand (irreducibility, unitary equivalence, uniqueness over all Hilbert spaces in every universe) and matched 8/8; finite-dimensional definition checks with a C+C control | Proved: permitted axioms only. A unital, simple, infinite-dimensional C*-algebra with a faithful trace and exactly one irreducible representation up to equivalence, so not K(H). 'In ZFC' is the paper's claim: Lean's foundations are stronger. Built by a sub-agent, rechecked by me |
| The 2D Anderson model's almost-sure spectrum is [-4-h, 4+h] (Lean `anderson_spectrum_ae`) | Docker build + axioms + sorry control; statement read (Z^2, uniform disorder, junk-measure branch excluded by h > 0) and matched 7/7; random-box spectra with planted-patch Weyl bounds and checkerboard controls | Proved: permitted axioms only. The CLASSICAL spectrum identity, not localization: the paper's pure-point claim is not formalised, as lean/docs/261.md itself says. Built by a sub-agent, rechecked by me |
| No 6 mutually unbiased bases in C^6, plus a Hadamard Fourier vanishing lemma (Lean `MUB6.fourier_and_family_bound`) | Docker build of the 3,381-module cone (about 2.5 hours) + axioms + sorry control; statement read by hand; matched 17/17 | Proved: permitted axioms only, no native_decide. NARROWER than the paper's 'at most three' (docs/266), but 'at most five' alone already rules out a complete set of 7 in dimension 6. Checked by me directly |
| An Artin group (116 generators, labels 2, 3, infinity) with no geometric action on any proper CAT(0) space (Lean `ArtinCAT0.main`) | Docker build + axioms + sorry control; CAT(0) and geometric-action definitions read by hand (full comparison inequality re-derived); matched 14/14; exact Python + Java checks of the presentation with S_40 and sphere controls | Proved: permitted axioms only. A negative answer to whether every Artin group is CAT(0), with an explicit group. Built by a sub-agent, rechecked by me |
| Uniqueness half of Bogomolov-Pop reconstruction (Lean `BogomolovPop.main_graph_injective`) | Docker build + axioms + sorry control; statement and docs scope read; matched 27/27; a finite PGammaL2 toy with coarse-invariant controls | Proved: permitted axioms only. NARROWER: injectivity only, existence is outside it (docs/009). Possibly a formalisation of a known half (Pop 2012); unchecked. Built by a sub-agent, rechecked by me |
| Borsuk's conjecture fails in dimension nine: the rank-one projectors of R^4 (an RP^3 in 9-dimensional space) cannot be covered by ten smaller pieces (Lean `BorsukNine.main_theorem`) | Docker build (9,193 jobs) + axioms + sorry control; cover, diameter and metric definitions read for the negation's risk direction (too strong a cover would make it cheap; `Metric.diam` of an unbounded set is 0, ruled out by compactness); matched 7/7; 9-dimensional affine span and the distance identity measured in Python and Java; Peres' 24 rays need only 5 pieces | Proved: permitted axioms only. MATCHES, read twice (Confluence; Fixpoint 16375, who also found an 11-cap cover, so b(X) = 11 given the claim). Novelty (dimension 9 vs the previous 63/64) unchecked past my June 2026 knowledge; Fixpoint finds no contradiction in print |
| Barnette's conjecture: every cubic bipartite planar 3-connected graph is Hamiltonian (Lean `Barnette.main`) | Docker build (8,955 jobs) + axioms + sorry control; planarity, 3-connectivity and Hamiltonian-cycle definitions read for vacuity (planarity satisfiable by convex polyhedra; the conclusion is a single cycle, not a 2-factor); matched 6/6; Java checks of 8 polyhedral Barnette graphs with Petersen, odd-prism and cut-pair controls | Proved: permitted axioms only. MATCHES on my first reading; a second reader is owed. Claims to settle a 1969 conjecture that was open as of my June 2026 knowledge: novelty check owed |
| Which formal results are cheap to check | `lean-cones/cones.py` over all 405 Comparator challenges | 390 of 416 need only Mathlib after Charles's pull of 2026-10-08 (was 379 of 405); smallest solution cones are 1-2 modules (e.g. Truffet: 2) |

## Log

- ~12:10Z: started; surveyed CONTENTS.md and lean/formalization.yaml (121 papers formalized); no Lean on host.
- Sidorenko: structure check, then tiny-kernel search.
- Measured the 405 Comparator dependency cones to find cheap formal targets; picked Truffet (2 modules).
- Truffet: Python and Java replications, all 13 conjuncts hold.
- Moved all Java into `java/src/confluence/math/<topic>/` per Charles.
- Generalized the container check (`lean-docker/check.sh <Challenge>`); FourRowPermanent proof checks; found the real exponent floor p* = 1.7448 and confirmed the proof's p0 = 1.99999 respects it.
- Lean in Docker: Truffet proof compiles, permitted axioms only; three failed runs on the way, documented in lean-docker/README.md.

- Charles pulled the repo (adc7f12 -> fd4aeeb, "Update manuscripts and Lean formalizations", 1185 files). Checked what it
  touched: NONE of my results' inputs changed (lean-toolchain, lake-manifest, lakefile, the Truffet and FourRowPermanent
  challenges and solution dirs, the Sidorenko preprint: 0 files each; control: the same diff reports the one modified
  challenge file, the challenges README). So every result above still stands. New: 11 challenges, all Mathlib-only,
  among them HadwigerCounterexample (288 modules); the README now says the four `...Support` challenges verify
  SUPPORTING results, not the papers' main theorems.

## Next ideas

- Sidorenko: see whether the paper's kernel (sections/kernel.tex) is explicit enough to evaluate numerically.
- More small cones from `lean-cones/`: PlaneColoring (9 modules), HadamardCubeFiber (6).
- HadwigerCounterexample is newly formalized (288-module cone): a long but feasible container build, and a counterexample with an explicit graph to compute on.
