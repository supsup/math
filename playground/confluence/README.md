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
labelled as the paper's claim. There is no Lean toolchain on this host, so my checks so far are
Python and Java; Lean would go in a container.

## Layout

| Folder | What |
|---|---|
| [sidorenko/](sidorenko/) | Notes + Python for the Sidorenko counterexample |
| [truffet/](truffet/) | Notes + Python for the Truffet tropical-LP counterexample |
| [permanent/](permanent/) | Notes for the robust four-row permanent inequality |
| [plane-coloring/](plane-coloring/) | Notes + Python for the plane 7-colouring (Hadwiger-Nelson upper bound) |
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
