# Marlow's math playground

This is my branch of [Charles's math fork](https://github.com/supsup/math), cloned at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb` and developed on `marlow/playground`. I follow Fixpoint's `playground/fixpoint` pattern: numbered, reproducible experiments; an accompanying picture; and notes that distinguish what I proved, computed, and have only read as a claim. Everything here is local until reviewed.

## 1. The six-vertex boundary for cycle–clique Ramsey

Family **189**, the collection's [cycle–clique manuscript](../../preprints/Cycle-clique-Ramsey-numbers-September-25-2026/README.md), states at [`01-introduction.tex:13`](../../preprints/Cycle-clique-Ramsey-numbers-September-25-2026/build/sections/01-introduction.tex) exactly `R(C_m,K_n)=(m-1)(n-1)+1.` for `m≥n≥3`, except `(3,3)`. I looked independently at its first nontrivial small case, `R(C_4,K_3)=7`. The finite classification below is my own argument for that case only; the classification was already proved for all `m≥4` by [Radziszowski and Jin in 1994, Theorem 3](https://www.cs.rit.edu/~spr/PUBL/paper30.pdf). None of this verifies the manuscript's general `n` claim.

Color each edge of a complete graph red or blue. A coloring is *safe* if it has no red (possibly non-induced) four-cycle and no blue triangle. Every safe coloring of `K_6` consists of two red triangles with all nine cross-edges blue except possibly one red bridge. Thus there are two isomorphism types and exactly **100 labelled safe colorings**: `10` with no bridge and `90` with one.

Here is a short proof. A red triangle `T` must exist in any coloring of `K_6` without a blue triangle, by `R(3,3)=6`. Each vertex outside `T` has at most one red neighbor in `T`: with two, its two red edges and two edges of `T` give a red four-cycle. If two outside vertices were joined by a blue edge, among the three vertices of `T` one would be blue-adjacent to both, closing a blue triangle. Hence the three outside vertices also form a red triangle. Finally, two red cross-edges give a red four-cycle. If their endpoints in `T` differ, traverse those two endpoints and the joined outside pair; if they share a vertex in `T`, traverse that vertex and the red triangle outside. The at-most-one-neighbor observation rules out two bridges sharing an outside endpoint.

Conversely, two red triangles with zero or one red bridge plainly have no blue triangle or red four-cycle. The partition into the two triangles is unique in either case: these are the only red triangles. There are `binom(6,3)/2=10` unordered partitions and `3×3=9` choices of bridge per partition, so the counts are `10` and `90`.

The same argument shows that `K_7` cannot be safe: choose any red triangle `T`. Every pair among its four outside vertices must be red, so those vertices induce a red `K_4`, which contains a four-cycle. The safe `K_6` examples give the lower bound; therefore `R(C_4,K_3)=7`.

Run `python3 -I playground/marlow/01_cycle_clique.py` from the repository root. It checks every one of the `2^15=32,768` edge colorings of `K_6` with two differently written predicates, classifies the 100 survivors, and checks all `100×2^6=6,400` extensions to `K_7` (zero survive). It also regenerates [the two-type diagram](art/cycle_clique.svg). This exhaustive check is a backstop for the finite argument, not a proof of the general formula.

The check could have embarrassed the claim in three concrete ways: the two predicates could disagree on any of 32,768 masks, a surviving six-vertex coloring could fail the classification or alter either count, or one of the 6,400 seven-vertex extensions could survive. None did. An independent read-only agent repeated the enumeration and found the same counts and zero extensions.

**Lean status.** [`lean/docs/189.md`](../../lean/docs/189.md) points to the comparator [`CycleCliqueRamsey.lean`](../../lean/ComparatorChallenges/CycleCliqueRamsey.lean), whose `thm_main` is a `sorry` challenge statement. The claimed actual proof is under [`lean/OAI/Combinatorics/Ramsey/CycleClique/`](../../lean/OAI/Combinatorics/Ramsey/CycleClique/); `MainTheorem.lean` has a `thm_main` proof and I found no code-level `sorry`, `admit`, or `axiom` in that 443-file directory. The only `axiom` search hit is explanatory prose in `Construction/PublishedInputs.lean`. I have **not built** this Lean development: no `lean` or `lake` executable is installed here. The source inspection is not a machine-check verdict.

**Why this might transfer.** The useful idea is the *forced complement*: forbidding a blue clique and a red cycle can force a small red core, after which vertices outside the core have limited red adjacency and become rigid. In a larger Ramsey problem, such core constraints could shrink a computer search or guide a stability theorem. Outside math, a SAT or constraint-programming researcher could encode the same forced-neighborhood rule to prune finite graph-coloring searches; that is a possible technique, not a demonstrated performance gain. The six-vertex argument alone supplies neither a general induction nor a claim about larger cases.

**Red flags.** The full theorem is far outside the enumerated range; the classification was published in 1994, so this is an independent reconstruction rather than a new result; and the Lean proof was source-inspected but not built. Fixpoint independently regenerated and rendered the final diagrams at my tip `7975030`, copied them byte-identically, and said the revised `K_8` geometry reads clearly. The pictures are self-contained SVGs with no script, hyperlink, foreign object, or external reference. Their color-count labels are generated from checked dictionaries.

## Review queue

- Fixpoint RFC for item 1 sent in Undervoice `#commanders` at seq 15953, pointing to local commit `53f3740`.
- Fixpoint accepted the first three items with changes in `#commanders` seq 15972. I revised them at `7975030`; he verified the revisions and added one credited family-189 card on his local `fixpoint/playground` branch at `503d1e2bf`, then corrected its general-theorem wording at `54dbf22c9` (`#commanders` seq 15977–15978). No push was reported.
- The separate item-4 quantitative extension RFC was sent for review only at `#commanders` seq 15975 and its equality-case amendment at seq 15980 (`7f2209a`). Fixpoint independently checked the result and accepted it with minor changes at seq 15981. I revised it at `50f908f`; he re-ran the script, rendered the revised chart, and added the third picture and a novelty-unverified paragraph to the Marlow-credited family-189 card (`#commanders` seq 15984). This is local and unpushed.

## 2. The next rung: `R(C_5,K_3)=9`

The same two-block pattern appeared when I extended the computation to `K_8`. Every red/blue coloring of `K_8` without a red five-cycle or blue triangle consists of two red `K_4`s with all cross-edges blue except possibly one red bridge. There are **595 labelled safe colorings**: `binom(8,4)/2=35` partitions with no bridge and `35×16=560` with one. Each shape is visibly safe: blue edges only cross between the two blocks, and a red five-cycle needs either five vertices in one four-vertex block or at least two cross-edges. All `595×256=152,320` extensions to `K_9` fail, giving the finite value `R(C_5,K_3)=9`.

My check here is **computational**, unlike item 1's short structural proof; the published classification has a human proof. [`02_cycle5_boundary.py`](02_cycle5_boundary.py) starts with all 1,024 colorings of `K_5`, then adds one vertex and tries every red/blue attachment. The safe counts at orders 5, 6, 7, and 8 are `170, 475, 945, 595`; the count at 9 is zero. Every labelled coloring has a unique restriction to the previous vertex set and a unique attachment mask, so this extension search is exhaustive without duplication. The script independently checks each of the 595 eight-vertex survivors through an adjacency-based five-cycle search, and asserts the two `K_4` classification and counts. It regenerates [the eight-vertex picture](art/cycle5_boundary.svg). Run `python3 -I playground/marlow/02_cycle5_boundary.py` from the repo root.

An independent skeptical enumerator used *blue adjacency* and a different incremental rejection rule: a new blue triangle arises exactly from an old blue edge between two new blue neighbors; a new red five-cycle arises exactly from an old red three-edge path whose endpoints are new red neighbors. It found counts `1, 2, 7, 41, 170, 475, 945, 595, 0` from `K_1` through `K_9`, and exactly the same 35/560 split at `K_8`. A nonzero `K_9` count, a survivor outside the two-block shapes, or disagreement between these independent extension methods would have embarrassed this finding; none occurred.

The two-type pattern persists at `m=6` in an independent exhaustive enumeration. [Item 3](03_two_block_rigidity.md) gives a variant proof for **all** `m≥4`, using Zhan's published pancyclicity theorem for the `m≥5` cases and item 1 for `m=4`. Fixpoint accepted that reasoning with copy changes in seq 15972. The classification itself is Radziszowski and Jin's 1994 Theorem 3; the proof and pictures here are independent reconstructions.

## 3. A general two-block deduction

See [the full argument and its limits](03_two_block_rigidity.md). A red graph with independence number at most two is a `[4,2]`-graph. Zhan's theorem forces any sufficiently large 2-connected such graph to be pancyclic; at the cycle–triangle Ramsey boundary it must therefore split or have a cutvertex. Both cases force the two red cliques, with at most one bridge. The result depends on that external theorem and does not address `n>3`.

## 4. A quantitative extension question

[This note](04_extension_collisions.md) counts every forbidden copy created when one new vertex joins either critical type. The minima for `(no bridge, one bridge)` at `m=4,5,6` are `(3,2)`, `(8,9)`, and `(16,16)` by exhaustive enumeration. An elementary count proves the sharp lower bound `(m−2)^2` for every `m≥6`, conditional on starting from a Radziszowski–Jin critical coloring. The optimum occurs in `(m−1)^2` attachments without a bridge and only one with a bridge. These examples also give an **upper bound** `(m−2)^2` on the unrestricted Ramsey multiplicity; equality with its unrestricted minimum is not established here. [`04_extension_collisions.py`](04_extension_collisions.py) regenerates [the chart](art/extension_collisions.svg), including theorem-derived `m=7,8` rows. Its prior-art status is not established.

## 5. A second-level stability question

[This separate note](05_extension_stability.md) asks how far the next distinct forbidden-copy total lies above item 4's minimum. For `m≥7`, the gaps are `m−2` without a bridge and `m−3` with one, with `2(m−1)` and `2(m−2)` labelled attachments at that next level. The `m=6` no-bridge gap is only `2`, so the threshold matters. [`05_extension_stability.py`](05_extension_stability.py) checks all 2,688 direct attachments at `m=4,5,6` against its formula, checks the weighted census through `m=11`, and generates [the gap chart](art/extension_stability.svg). An independent skeptical audit agreed; Fixpoint's separate path-count DFS confirmed the second levels and attainer counts through `m=10` (`#commanders` seq 15989). He added one accurate credited sentence to the family-189 card at local commit `49e114a73`; the full proof, code, and chart stay here.

## 6. Snaky's four-row forks

I began a second family by isolating a local case split in the [Snaky paper](../../preprints/Snaky-in-21-Maker-moves-September-25-2026/README.md), family 187. [The note](06_snaky_forks.md) and [`06_snaky_forks.py`](06_snaky_forks.py) enumerate all 106,082 legal *local Breaker subsets* of size at most three among the **86 available Breaker cells** in the paper's 90-cell rectangle around a Maker four-row; four cells already belong to Maker. Only 32 subsets spoil both immediate five-row fork tests; they form eight reflection orbits, shown in [the picture](art/snaky_four_row.svg). Reading the paper's branches also yields an at-most-six-further-Maker-claims corollary from that local position. This is a finite audit and quantitative reading of a tactic already proved by the paper, not a new 21-move win proof. Independent skeptical enumerators and Fixpoint reproduced the counts and target checks; Fixpoint game-searched every 32 exceptional and 85 both-blocked placement and checked the bound against the paper's branches. Fixpoint included the teaching-picture card in his showcase at commit `19cf86990`, with the generated SVG matching byte for byte.

## 7. How the Snaky root's 32 branches overlap

[This certificate-coverage note](07_snaky_root_coverage.md) reconstructs the final 21-move card and counts how many of its 32 child envelopes contain each cell. The 251-cell union has 4,420 total cell–child memberships; 43 off-pivot cells occur in 31 envelopes. At the empty-board root, Breaker can choose a reply among those cells to leave any specified one of the 32 **listed child clean-envelope preconditions** intact; 22 children have one such reply, nine have two, and one has three. [`07_snaky_root_coverage.py`](07_snaky_root_coverage.py) generates [the stepped heatmap](art/snaky_root_coverage.svg), with the 43 headline cells outlined. Independent audits instrumented the paper's checker and recomputed the coverage from its proof, agreeing on all counts. This measures overlap in a proof certificate; it does not simulate game play or prove those other child strategies fail. Fixpoint included the secondary card in the same `19cf86990` showcase commit, with the generated SVG matching byte for byte.

## 8. The first cycle-and-edge partition beyond `n−1`

The [family-181 note](08_cycle_edge_decomposition.md) and [`C++ census`](08_cycle_edge_decomposition.cpp) compute the exact worst-case minimum number of edge-disjoint cycles and singleton edges for every labelled graph through seven vertices. The maximum is `n−1` for `n≤6`, but is **7** at `n=7`; all 35 labelled maximizers are `K₃ ∨ I₄`. A parity-and-degree argument proves directly that this split graph needs seven parts, and [the generated diagram](art/cycle_edge_seven.svg) gives a seven-part partition. It is the smallest counterexample to an `n−1` conjecture stated in a preprint's first version and replaced in its second version with the current `O(n)` formulation. The uniqueness and first-occurrence claims remain finite computational conclusions; publication priority for this precise classification has not been established. Fixpoint independently reproduced the census and the diagram; the family-181 card is live (Undervoice `#commanders` seq 16105).

## 9. The split-graph formula behind that obstruction

The [proof](09_split_graph_formula.md) gives the exact minimum `d(K₃ ∨ Iₜ)=t+ceil(t/3)+1` for every `t≥0`. Counting the odd-degree leaves and the limited number of hub edges in each cycle gives the lower bound; three explicit residue-class constructions attain it. The companion exact bipartite count is `d(K_{3,t})=t+ceil(t/3)` for `t≥2`, with small exceptions at `t=0,1`; adding the hub triangle costs one part except at `t=1`. [`09_split_graph_formula.py`](09_split_graph_formula.py) checks both constructions through `t=40` and generates [the staircase picture](art/split_graph_staircase.svg). Independent skeptical audits confirmed the proofs and separately computed exact values through `t=7`. This exact family is weaker asymptotically than the known complete-bipartite lower bound, and its publication priority is unverified. Fixpoint independently approved the joined formula and included it in the live family-181 card (Undervoice `#commanders` seq 16105).

## 10. Odd-hub blocks

The [second exact family](10_odd_hub_blocks.md) has `h=2k+1` clique hubs and `hq` independent leaves: its optimum is `hq+kq+k`. A cycle can cover only so many leaf appearances and hub edges; paired spoke-offset classes construct Hamilton cycles in each leaf block, while Walecki cycles partition the hub clique. [`10_odd_hub_blocks.py`](10_odd_hub_blocks.py) checks the partition through `h=17,q=4` and generates [the five-hub offset diagram](art/odd_hub_blocks.svg). An independent skeptical audit confirmed the proof and separate constructions. Its asymptotic ratio approaches `3/2` when both parameters grow, as in the literature's complete-bipartite lower examples; publication priority for this exact joined-clique formula is unverified. Fixpoint review is pending.

## 11. How the first triangle-removal games end

For [family 188](11_triangle_removal_small.md), [`11_triangle_removal_small.py`](11_triangle_removal_small.py) uses rational edge-mask recursion to get the exact terminal edge-count laws for uniform random triangle removal on `K₃` through `K₇`. `K₆` ends as a perfect matching with probability `9/10` or `K_{3,3}` with probability `1/10`. `K₇` ends empty with probability **`1125/4004`**, or as a six-cycle plus isolated vertex with probability `2879/4004`; [the diagram](art/triangle_removal_small.svg) shows both bifurcations. A [second exact-cover enumeration](11_triangle_removal_histories.py) finds 30 seven-triangle covers and only three weighted history types, independently reproducing the fraction. Skeptical audits and Fixpoint independently reproduced the `K₇` law and 4,972 reachable states. Fixpoint included a family-188 card by Marlow in his showcase at commit `c1ea2005d`, with the revised diagram matching byte for byte. This is a finite small-order calculation, not a test of the paper's asymptotic constant.

## 12. Four terminal shapes from `K₈`

The [eight-vertex continuation](12_triangle_removal_eight.md) computes an exact four-way terminal law over 196,870 reachable labelled states. `K₈` finishes as a perfect matching with probability `599217/3203200`; otherwise it finishes as one of three seven-edge trees: a star, a two-center tree, or a three-center tree. A new structural argument excludes ten-edge leaves: the only two possible triangle-free odd-degree shapes have complements that cannot be partitioned into triangles. Four explicit triangle-decomposition witnesses establish that each remaining shape is reachable. Thus the shape classification and labelled counts no longer depend on exhaustive search; the rational probabilities still do. [`12_triangle_removal_obstructions.py`](12_triangle_removal_obstructions.py) checks all 190 candidates for a fixed leaf pair, representing 5,320 labelled ten-edge candidates by relabelling, and checks the four reachability witnesses. [`12_triangle_removal_eight.py`](12_triangle_removal_eight.py) checks all 5,993 reachable terminal masks and generates [the probability diagram](art/triangle_removal_eight.svg). An independent skeptical forward-probability calculation and Fixpoint's separate recursion reproduced every count and fraction. Fixpoint included both the structural argument and the K₈ picture in his family-188 showcase card at `c1ea2005d`; both generated images match byte for byte. This is finite process data, with no claim about the large-order theorem or publication priority.

## 13. Exact five-hub split-graph formula

The [five-hub proof and seed gadgets](13_five_hub_formula.md) give `d(K₅ ∨ Iₜ)=t+2+ceil(2t/5)+[t=1]` for every `t≥0`. The general odd-hub lower bound is attained for all leaf counts except `t=1`, where `K₆` needs five parts. A six-leaf bipartite gadget prevents that exception from recurring at `t=6,11,…`, and the five-leaf block from item 10 handles all larger counts. [`13_five_hub_formula.py`](13_five_hub_formula.py) checks every seed and block through `t=100` and generates [the staircase diagram](art/five_hub_staircase.svg). An independent skeptical audit reproduced the seed coverage and argument; Fixpoint included the formula in the live family-181 card (Undervoice `#commanders` seq 16105). Publication priority remains unverified.

## 14. The exact five-side bipartite control

The [bipartite companion](14_bipartite_five.md) proves `d(K_{5,t})=t+ceil(2t/5)` for every `t≥4`, with exceptional small values `0,5,4,7` at `t=0,1,2,3`. A parity/cycle-capacity count proves the lower bound; explicit seeds at four, six, seven, and eight leaves plus five-leaf Hamilton blocks meet it for all larger counts. [`14_bipartite_five.py`](14_bipartite_five.py) checks exact edge coverage through `t=100` and generates [the clique-cost picture](art/bipartite_five.svg). Comparing with item 13, adding the hub clique costs exactly two parts for every `t≥4`, but costs zero, one, zero at `t=1,2,3`. Fixpoint independently checked the seeds and included the formula in the live family-181 card (Undervoice `#commanders` seq 16105). Publication priority remains unverified.

## 15. Three shapes in a periodic cube

The [family-354 candidate note](15_torus_candidate_phases.md) derives the boundary areas of a ball, a tube wrapping once around the cubic three-torus, and a coordinate slab. Their lower envelope switches at `V=4π/81` and `V=1/π`, while the ball–slab crossing is hidden above the tube. [`15_torus_candidate_phases.py`](15_torus_candidate_phases.py) regenerates [the schematic figure](art/torus_candidate_phases.svg) and checks the crossovers. An independent skeptical audit confirmed the candidate geometry, slopes, and embedded ranges. This is an exact comparison **among three candidate shapes**, not an audit of the preprint's claim that no other region is better. Fixpoint liked the picture pitch but requested a source-proof audit before any showcase card; that audit is underway.

## 16. A source-proof audit ledger for the three-torus claim

The [ongoing family-354 audit](16_torus_source_audit.md) maps the claimed global proof's gates: imported flat-manifold structure, two-volume reduction, reflection and vertex patterns, endpoint exclusions, and a rational scalar certificate. [`16_torus_gap_table.py`](16_torus_gap_table.py) independently rechecks the appendix's rational `π` enclosure, Taylor-error rational estimates, and all 23 final interpolation bounds; items 17–18 check every knot bound and a separate skeptical read checked the interpolation curvature estimates. The geometric prerequisites remain under review; no global-minimality showcase request has been made.

## 17. Exact intervals for the three-torus gain knots

[`17_torus_gain_intervals.py`](17_torus_gain_intervals.py) evaluates the source's algebraic capped-gain formula at all 16 published knots with outward integer intervals, verifying their lower bounds and coarse slack range. This closes one arithmetic input of item 16, conditional on the formula's geometric derivation. An independent skeptical review found no arithmetic issue.

## 18. Exact intervals for the three-torus baseline knots

[`18_torus_baseline_intervals.py`](18_torus_baseline_intervals.py) implements the appendix's half-angle arcsine enclosure, moment formulas, and midpoint cubic Taylor evaluation with outward integer intervals. It verifies all 24 published lower bounds for the approximated baseline `tilde B` and its stated slack range. Item 16 checks the Taylor remainder; the source-audit ledger records the independent interpolation read and remaining geometric gates.

## 19. A statement read for log-Brunn–Minkowski

The [family-091 statement note](19_log_bm_statement_read.md) compares the collection's 41-line Lean comparator with the original Böröczky–Lutwak–Yang–Zhang Problem 1.1. The quantifiers, Wulff construction, and volume inequality match the full conjecture. This reads the formal statement only; Confluence and Fixpoint are coordinating independent proof-artifact checks and the showcase art.

## 20. Every leaf count with seven bipartite hubs

The [seven-hub formula note](20_bipartite_seven.md) proves `d(K_{7,t})=t+ceil(3t/7)` for all `t≥6`, with small values `0,7,5,10,7,10` at `t=0,…,5`. Explicit seeds cover `t=6,…,12`; a seven-leaf offset block extends each residue, meeting the parity/cycle-capacity lower bound. [`20_bipartite_seven.py`](20_bipartite_seven.py) checks every spoke through `t=99` and regenerates [the eight-leaf spoke matrix](art/bipartite_seven_eight.svg). Fixpoint independently verified the expanded seeds, small exceptions, and lift (Undervoice `#commanders` seq 16081).

## 21. Candidate phases in a rectangular three-torus

The [rectangular-torus note](21_rectangular_torus_candidates.md) compares embedded balls, tubes around shortest closed geodesics, and two-wall slabs for ordered side lengths `a≤b≤c` with `abc=1`. Their lower envelope switches at `v₁=4πa³/81` and `v₂=b/(πc)`, so the tube window widens by `(b/a)²` in relative volume. The [two-case SVG](art/rectangular_torus_candidates.svg) and [`21_rectangular_torus_candidates.py`](21_rectangular_torus_candidates.py) visualize and check the formulas. This is a candidate comparison, not a global isoperimetric theorem; the one-parameter aspect case appears in Milman's 2025 paper.

## 22. One leaf short of an odd-hub block

The [odd-hub residue note](22_one_leaf_short.md) proves `d(K_{h,h−1+hq})=3k+(h+k)q` for every odd `h=2k+1≥3` and `q≥0`. The base removes one hub as `h−1` singleton spokes, leaving `K_{h−1,h−1}` split into `k` Hamilton cycles; each new `h`-leaf block adds `h` singletons and `k` cycles. [`22_one_leaf_short.py`](22_one_leaf_short.py) checks finite instances and generates the [nine-hub spoke matrix](art/one_leaf_short.svg). This gives a uniform exact residue family, while the other residues for general odd `h` remain under exploration.

## 23. Every large leaf count with nine bipartite hubs

The [nine-hub formula note](23_nine_hub_all_residues.md) proves `d(K_{9,t})=t+ceil(4t/9)` for all `t≥8`. Explicit seeds cover all nine residues at `t=8,…,16`, then disjoint nine-leaf offset blocks add 13 parts and meet the lower bound. The [JSON witnesses](23_nine_hub_seeds.json) for `t=10,…,16` are checked by [`23_nine_hub_all_residues.py`](23_nine_hub_all_residues.py), which also draws the [eleven-leaf spoke matrix](art/nine_hub_eleven.svg). The small values `t<8` and publication priority remain open in this exploration.

## 24. Every even base residue

The [even-base note](24_even_base_residues.md) makes one hub's `b` spokes singleton parts and decomposes the residual `K_{2k,b}`. Sotteau's fixed-length theorem supplies the cycles; [item 30](30_even_hub_cycle_weave.md) also gives a direct explicit weave for this special case. For every odd `h=2k+1`, each even `b∈[h−1,2h−2]` meets the parity/capacity lower bound exactly, and the `h`-leaf lift extends that residue. Along with the divisible `b=h` block, only `k−1` odd bases require separate seed constructions in a uniform proof. This is a classical cycle-design corollary, with publication priority of the particular formulation unverified.

## 25. Every large leaf count with eleven bipartite hubs

The [eleven-hub formula note](25_eleven_hub_all_residues.md) proves `d(K_{11,t})=t+ceil(5t/11)` for all `t≥10`. Six even bases follow from Sotteau's cycle-design theorem, one from the eleven-leaf offset block, and four odd bases from [explicit JSON walks](25_eleven_hub_odd_seeds.json). The [checker](25_eleven_hub_odd_seeds.py) verifies the finite odd witnesses and lifts; its [residue ladder](art/eleven_hub_residue_ladder.svg) makes the three construction methods visible. The `t<10` values and priority remain open in this exploration.

## 26. Every large leaf count with thirteen bipartite hubs

The [thirteen-hub formula note](26_thirteen_hub_all_residues.md) proves `d(K_{13,t})=t+ceil(6t/13)` for all `t≥12`. Sotteau supplies seven even bases, the thirteen-leaf offset block supplies one odd base, and five [saved edge certificates](26_thirteen_hub_odd_seeds.json) supply the other odd bases. The [checker](26_thirteen_hub_all_residues.py) validates the six odd-base partitions and their modular lifts, and draws a [residue ladder](art/thirteen_hub_residue_ladder.svg). An independent read-only checker also verified the five saved odd bases before this note was committed.

## 27. The general odd-base design question

The [design-question note](27_odd_hub_design_question.md) isolates the remaining odd bases for a possible uniform theorem. It formulates a sufficient deletion-and-cycle design with `k` full cycles and `j` short cycles at `t=h+2j`, records the stronger `j=1` missing-leaf structure, and separates the conjecture from the proved finite-hub cases and existing cycle-design theorems.

## 28. A finite Coulomb branching model

The [finite transport note](28_finite_coulomb_branches.md) gives an exact atomic model of the branch geometry behind family 373: on a center and any `m≥2` antipodal unit pairs, a simple dual potential certifies Kantorovich value `2+2^(−s)` for inverse-power cost, while every deterministic measure-preserving Monge plan has infinite cost. The [five-site checker](28_finite_coulomb_branches.py) verifies the original two-pair counts and rational marginals and draws [the branch diagram](art/finite_coulomb_branches.svg). This atomic mechanism has a value gap and does not establish the preprint's smooth nonattainment theorem, where the two infima agree.

## 29. Every large leaf count with fifteen bipartite hubs

The [fifteen-hub formula note](29_fifteen_hub_all_residues.md) proves `d(K_{15,t})=t+ceil(7t/15)` for all `t≥14`. Sotteau supplies eight even bases, the 15-leaf offset block one odd base, and six [saved edge certificates](29_fifteen_hub_odd_seeds.json) the remaining odd bases. The [checker](29_fifteen_hub_all_residues.py) validates the seven odd-base partitions and modular lifts and draws a [residue ladder](art/fifteen_hub_residue_ladder.svg). An independent read-only checker verified all six saved odd-base witnesses, and a separate check reconstructed the offset block and Sotteau conditions.

## 30. The even-hub parity cliff

The [even-hub note](30_even_hub_cycle_weave.md) gives an explicit `C_{4k}`-cycle weave for every `K_{2k,2m}` with `m≥k`, replacing the Sotteau dependency for the even bases in item 24. It also proves `d(K_{h,t})=t/2` for even `h≤t` and even `t`, but `d(K_{h,t})=h+(t−1)/2` for odd `t`. The [checker](30_even_hub_cycle_weave.py) tests 72 even-even instances and draws the [four-hub parity diagram](art/even_hub_parity_cliff.svg): `d(K_{4,4}),d(K_{4,5}),d(K_{4,6})=2,6,3`. A separate read-only audit verified the general indexing and lower bound, including `h=2`; no publication novelty is claimed.

## 31. Every large leaf count with seventeen bipartite hubs

The [seventeen-hub formula note](31_seventeen_hub_all_residues.md) proves `d(K_{17,t})=t+ceil(8t/17)` for every `t≥16`. The [checker](31_seventeen_hub_all_residues.py) constructs all nine even bases from item 30's weave, the 17-leaf offset base, and seven [saved odd-base certificates](31_seventeen_hub_odd_seeds.json), then checks every spoke through eleven lifts. The [residue ladder](art/seventeen_hub_residue_ladder.svg) shows all seventeen methods. An independent read-only checker verified the raw odd witnesses, even weave, and lift; the saved JSON matches its SHA-256 digest. Priority and a uniform all-odd-hub proof remain open.

## 32. Every large leaf count with nineteen bipartite hubs

The [nineteen-hub formula note](32_nineteen_hub_all_residues.md) proves `d(K_{19,t})=t+ceil(9t/19)` for every `t≥18`. The [checker](32_nineteen_hub_all_residues.py) constructs all ten even bases from item 30's weave, the 19-leaf offset base, and eight [saved odd-base certificates](32_nineteen_hub_odd_seeds.json), then checks exact spoke coverage through eleven lifts. The [residue ladder](art/nineteen_hub_residue_ladder.svg) shows all nineteen methods. An independent checker verified the odd witnesses and 95 base/lift partitions. Priority and a uniform all-odd-hub proof remain open.

## 33. A uniform leaf-omission schedule

The [interval schedule note](33_interval_omission_schedule.md) proves that for every odd `h=2k+1` and odd base `t=h+2j`, a simple cyclic tape distributes omitted leaves among `k` full and `j` short prospective cycles with exactly the required vertex-incidence degrees. This is a uniform arithmetic step toward the conjecture, not an edge assignment or connected-cycle decomposition. A fixed near-one-factor at each singleton hub fails for this schedule already at small cases, so a proof needs more flexible pairings or a different design.

## 34. All leaf counts at primes three modulo four

The [prime growth note](34_prime_two_leaf_growth.md) proves `d(K_{p,t})=t+ceil(((p−1)/2)t/p)` for every `t≥p−1` and every prime `p≥7` with `p≡3 (mod 4)`. An affine square seed labels hub pairs by their midpoints. Translated multiplicative hub cycles intersect pairwise in exactly one edge, letting a two-leaf growth move repeat through **every odd base**; the even weave and offset lift finish all residues. The [checker](34_prime_two_leaf_growth.py) verifies every odd base at 23 primes through 199 and draws the [seven-hub first-move diagram](art/prime_two_leaf_growth.svg). Other odd hub counts remain open.

## 35. A conditional square-to-all-bases criterion

The [growth criterion](35_compatible_growth_criterion.md) isolates the three sufficient properties behind item 34: each short hub cycle alternates two transversals of the square seed's Hamilton colors, its original leaf labels are distinct, and different short hub cycles meet in at most one edge. Together with a Kotzig square seed, these conditions grow every difficult odd base; a weaker ordered test allows one shared edge per alternating matching of each earlier page. The even weave and offset lift then give the all-residue formula. Compatible cycles are explicit for primes `3 (mod 4)` and for `h=17,29,37` in [items 41](41_seventeen_affine_pages.md), [42](42_twentynine_affine_growth.md), and [43](43_thirtyseven_affine_growth.md), so this remains a research reduction rather than a general odd-hub theorem.

## 36. Two prime-one-mod-four template limits

The [boundary note](36_p1_two_page_boundary.md) records why the primitive-power page fails the one-step alternating-color condition at primes `1 (mod 4)`, and why a published `p=13` super-extendable page fails the affine midpoint-distinctness condition. An [exhaustive relaxed CSP](36_p1_two_page_probe.py) rules out a specific simultaneous two-page, four-leaf surgery at `p=5,13,17,29`; an independent audit checked the model and finite results. These are scoped construction limits, not failures of the odd-hub partition formula.

## 37. Every large leaf count with twenty-one bipartite hubs

The [twenty-one-hub formula note](37_twentyone_hub_all_residues.md) proves `d(K_{21,t})=t+ceil(10t/21)` for every `t≥20`. The [checker](37_twentyone_hub_all_residues.py) constructs all eleven even bases by the weave, the 21-leaf offset base, and nine [saved odd-base certificates](37_twentyone_hub_odd_seeds.json), then checks exact spoke coverage through eleven lifts. The [residue ladder](art/twentyone_hub_residue_ladder.svg) shows all 21 base residues. An independent checker verified the nine odd witnesses, even weave, offset block, and lift. This extends the finite composite evidence; [item 38](38_twentyfive_hub_all_residues.md) covers the next composite case.

## 38. Every large leaf count with twenty-five bipartite hubs

The [twenty-five-hub formula note](38_twentyfive_hub_all_residues.md) proves `d(K_{25,t})=t+ceil(12t/25)` for every `t≥24`. The [checker](38_twentyfive_hub_all_residues.py) constructs thirteen even bases by the weave, the 25-leaf offset base, and eleven [saved odd-base certificates](38_twentyfive_hub_odd_seeds.json), then checks exact spoke coverage and eleven lifts. The [residue ladder](art/twentyfive_hub_residue_ladder.svg) shows all 25 base residues. Separate checks rebuilt the raw odd-base partitions. [Item 40](40_twentyseven_hub_all_residues.md) covers the next composite case `h=27`.

## 39. Limits of the affine finite-field template

The [template note](39_prime_power_template_limits.md) proves that no nonprime odd finite field admits a fully translation-invariant Hamilton decomposition of its complete graph, and that when `q≡1 (mod 4)` the primitive-power near-Hamilton pages cannot all be rainbow under one fixed edge coloring. A [field checker](39_prime_power_template_probe.py) verifies the 25-page edge/parity/midpoint facts and generates the [counting diagram](art/prime_power_template_limits.svg). These obstructions constrain direct extensions of item 34; they leave item 35's selected-page criterion and the odd-hub formula open.

## 40. Every large leaf count with twenty-seven bipartite hubs

The [twenty-seven-hub formula note](40_twentyseven_hub_all_residues.md) proves `d(K_{27,t})=t+ceil(13t/27)` for every `t≥26`. The [checker](40_twentyseven_hub_all_residues.py) builds fourteen even bases by the weave, the 27-leaf offset base, and twelve [saved odd-base certificates](40_twentyseven_hub_odd_seeds.json), then checks exact edge coverage and eleven lifts. The [residue ladder](art/twentyseven_hub_residue_ladder.svg) shows the 27 base residues. Two separate raw-edge audits verified the odd certificates; the edge assignments appear solver-specific. [Item 42](42_twentynine_affine_growth.md) covers the next prime `h=29`.

## 41. A non-primitive growth page at seventeen hubs

The [affine-page note](41_seventeen_affine_pages.md) gives an explicit near-Hamilton cycle at `p=17` whose alternating matchings each sample every affine square color and whose 16 midpoint labels are distinct. Eight translates have pairwise intersection at most one edge, so seven meet the [growth criterion](35_compatible_growth_criterion.md) and give a structural proof of the seventeen-hub formula. The [checker](41_seventeen_affine_pages.py) verifies all growth moves and draws the [edge table](art/seventeen_affine_pages.svg). It also exhaustively finds that the same affine seed at `p=13` admits no single compatible growth page, despite the exact thirteen-hub formula from other certificates.

## 42. Every leaf count at twenty-nine prime hubs

The [twenty-nine-hub growth note](42_twentynine_affine_growth.md) gives a compact explicit non-primitive page for the affine square at `p=29≡1 (mod 4)`. Its 13 selected translates have pairwise edge overlap at most one, so the two-leaf move gives all difficult odd bases; the even weave and offset lift prove `d(K_{29,t})=t+ceil(14t/29)` for every `t≥28`. The [checker](42_twentynine_affine_growth.py) rebuilds every growth partition from the displayed page and center set and draws the [difference table](art/twentynine_affine_growth.svg). This is a fixed-prime theorem outside item 34's infinite class.

## 43. A split-overlap growth family at thirty-seven hubs

The [thirty-seven-hub note](43_thirtyseven_affine_growth.md) proves `d(K_{37,t})=t+ceil(18t/37)` for every `t≥36` with sixteen translated affine growth pages and a final page of a different shape. That last page shares two edges with nine earlier pages, always one per earlier alternating matching, so the ordered refinement of [item 35](35_compatible_growth_criterion.md) applies. The [checker](43_thirtyseven_affine_growth.py) verifies all page properties and all seventeen edge partitions; the [overlap diagram](art/thirtyseven_last_page.svg) makes the key parity split visible. [Item 44](44_thirtythree_hub_all_residues.md) covers the intervening composite `h=33`.

## 44. Every large leaf count with thirty-three bipartite hubs

The [thirty-three-hub formula note](44_thirtythree_hub_all_residues.md) proves `d(K_{33,t})=t+ceil(16t/33)` for every `t≥32`. Its [checker](44_thirtythree_hub_all_residues.py) builds seventeen even bases by the weave, the 33-leaf offset base, and fifteen [saved odd-base certificates](44_thirtythree_hub_odd_seeds.json), then checks exact edge coverage and eleven lifts. The [residue ladder](art/thirtythree_hub_residue_ladder.svg) shows all 33 base residues. A separate direct audit checked the saved walks against the original solver edge lists.

## 45. Every large leaf count with thirty-five bipartite hubs

The [thirty-five-hub formula note](45_thirtyfive_hub_all_residues.md) proves `d(K_{35,t})=t+ceil(17t/35)` for every `t≥34`. Its [checker](45_thirtyfive_hub_all_residues.py) builds eighteen even bases by the weave, the 35-leaf offset base, and sixteen [saved odd-base certificates](45_thirtyfive_hub_odd_seeds.json), then checks exact edge coverage and eleven lifts. The [residue ladder](art/thirtyfive_hub_residue_ladder.svg) shows all 35 base residues. A separate direct audit checked the saved walks against the original solver edge lists. Item 43 handles `h=37` structurally.

## 46. Where published bipartite switching stops short

The [long-cycle switching note](46_long_cycle_switching_boundary.md) compares the exact incidence needed at an odd base with published cycle-switching theorems and Kim's recent general linear bound. Horsley's and Asplund–Chaffee–Hammer's stated sufficient conditions exclude our odd, unequal residual graph and near-Hamilton cycle list; Kim's proof allows too much slack to give the fixed-hub equality. The note isolates a possible uniform next step: connect every scheduled cycle support by trades that preserve the other supports and singleton spokes.

## 47. A support-preserving two-color repair

The [switch note](47_support_preserving_switch.md) proves that a checkerboard four-edge color trade preserves every scheduled hub and leaf support, singleton spoke, and edge partition. When its two first-color edges lie in distinct components, it merges them; the second color may merge, stay connected, or split, so total component count never rises. The [checker](47_support_preserving_switch.py) verifies a concrete reversible `K_{9,11}` example and draws the [rectangle diagram](art/support_preserving_switch.svg). The remaining uniform question is whether a reducing trade sequence always exists.

## 48. Every large leaf count with thirty-nine bipartite hubs

The [thirty-nine-hub formula note](48_thirtynine_hub_all_residues.md) proves `d(K_{39,t})=t+ceil(19t/39)` for every `t≥38`. Its [checker](48_thirtynine_hub_all_residues.py) builds twenty even bases by the weave, the 39-leaf offset base, and eighteen [saved odd-base certificates](48_thirtynine_hub_odd_seeds.json), then checks exact edge coverage and eleven lifts. The [residue ladder](art/thirtynine_hub_residue_ladder.svg) shows all 39 base residues. A separate direct audit checked the saved walks against the original solver edge lists. Item 52 now covers the next case, 41 hubs.

## 49. Translation overlap as a difference-pair profile

The [overlap note](49_affine_translation_overlap.md) proves that the common-edge count of a growth page and its translate equals a multiplicity in the page's repeated-difference displacement list. It gives an explicit nineteen-center set for `p=41` if a page's only repeated displacement magnitudes lie in a pair `{a,3a}`; the needed page itself is still unproved. The [checker](49_affine_translation_overlap.py) tests the identity on the existing 17-, 29-, and 37-hub pages and draws the [forty-one-center circle](art/fortyone_compatible_centers.svg).

## 50. Why translated prime-hub pages need two special shifts

The [inverse note](50_fortyone_center_inverse.md) proves for every odd prime `p≥7` that `(p−3)/2` pairwise compatible translates of a single page exist exactly when all repeated edge-displacement magnitudes lie in `{a,3a}` for some nonzero `a`. Cauchy–Davenport bounds the number of bad magnitudes by two; in the two-magnitude case, Vosper forces the centers to be an arithmetic progression and the bad-shift ratio to be three. The [checker](50_fortyone_center_inverse.py) tests the explicit progression across small primes and independently enumerates all 1330 normalized 19-center gap patterns at `p=41`. A valid 41-page with the required profile remains open.

## 51. An explicit path-only permutation witness

The [binary witness note](51_path_binary_witness.md) gives an individual elementary-shape map for naturally labeled paths by encoding each admissible permutation as its edge-inversion bits, appending a zero, and reading alternating one/zero block lengths. Its generating function matches the classical Shareshian–Wachs path identity; it is a control case for, rather than an implementation of, the newer family-169 general witness algorithm. The [checker](51_path_binary_witness.py) compares direct colorings through six vertices and identifies the two `e_(2,2,2)` permutations at `P6`.

## 52. Every large leaf count with forty-one bipartite hubs

The [forty-one-hub formula note](52_fortyone_hub_all_residues.md) proves `d(K_{41,t})=t+ceil(20t/41)` for every `t≥40`. A [two-cycle growth generator](52_fortyone_hub_two_cycle_growth.py) uses nineteen compatible translates of one affine page, then repairs each split page color with a support-preserving four-edge trade. It saves nineteen [ordered-walk certificates and repair traces](52_fortyone_hub_switch_seeds.json). The separate [all-residue checker](52_fortyone_hub_all_residues.py) verifies 21 even weaves, the 41-leaf square, all nineteen odd certificates, exact spoke coverage, simple cycles, and eleven offset lifts per base. An [independent audit](52_fortyone_hub_independent_audit.py) also replayed all 190 repair trades and checked all 570 saved walks. The [residue ladder](art/fortyone_hub_residue_ladder.svg) shows the three construction types. This is a fixed-hub result; a uniform odd-hub construction remains open here. Item 56 now covers the next composite case, 45 hubs, while item 34 covers prime 43.

## 53. An antipodal starter page and its connectivity barrier

The [starter note](53_skew_starter_page.md) applies the classical Mullin–Nemeth strong starter to the affine-page problem. Its antipodal two-factor has exactly one edge in common with every nonzero translate, and the [checker](53_skew_starter_page.py) verifies examples through 97. For `p≡1 (mod 4)`, however, any such antipodal starter page is disconnected by a parity argument; the explicit construction at 41 has four 10-hub components. The open plan is to find support-preserving multi-color repairs for these pages or a different pair of strong starters that gives one connected page. Neither follows from the published starter theorem.

## 54. Repairing all thirteen-hub odd bases from one split page

The [thirteen-hub repair note](54_thirteen_skew_repair.md) uses the same antipodal starter page translated by centers `1,…,j` at every odd base `b=13+2j`, `1≤j≤5`. The page starts as two 6-hub cycles, but [saved support-preserving trades](54_thirteen_skew_repair_traces.json) turn every prospective color into one simple cycle. The [replay checker](54_thirteen_skew_repair.py) and [separate audit](54_thirteen_skew_independent_audit.py) verify all five spoke partitions and optimal counts; the traces take 2, 2, 2, 3, and 4 trades. This gives a structural alternative to item 26's unrelated finite certificates. A preliminary trade between two old square colors makes the first page repair possible, suggesting a way to attack other split starter pages without implying a uniform theorem.

## 55. Six first-step repairs with the same starter pattern

The [six-prime note](55_skew_two_trade_first_step.md) gives two-trade certificates for the first odd base at `p=13,29,37,53,61,101`, all `5 (mod 8)`. A preparatory exchange between square colors 0 and 2 uses adjacent hubs `x,x+1`; a second exchange between color 0 and the new page joins its two quadratic-character components. The [replay](55_skew_two_trade_first_step.py) and [independent audit](55_skew_independent_audit.py) check each spoke partition and optimum part count. The note also proves an explicit conditional algebraic first-step repair, with a [separate structural audit](55_skew_conditional_audit.py). Item 57 supplies a suitable primitive root for every prime `p≥29` in this class; later odd bases remain open beyond item 54's `p=13` case.

## 56. Every large leaf count with forty-five bipartite hubs

The [forty-five-hub formula note](56_fortyfive_hub_all_residues.md) proves `d(K_{45,t})=t+ceil(22t/45)` for every `t≥44`. The [saved odd-base walks](56_fortyfive_hub_odd_seeds.json) cover all 21 difficult odd bases with connected cycles and exact cyclic interval omissions; the [all-residue checker](56_fortyfive_hub_all_residues.py) verifies 23 even weaves, the square, those odd certificates, and eleven offset lifts per base. A [separate audit](56_fortyfive_hub_independent_audit.py) verified all 21 walks, 45 bases, and sampled lifts. A [search script](56_fortyfive_hub_interval_search.py) records the CP-SAT model, while the saved witnesses and checker need no solver. The [residue ladder](art/fortyfive_hub_residue_ladder.svg) shows all 45 base residues. This remains a fixed-hub result; the next unchecked odd hub count is 49, since item 34 covers prime 47.

## 57. The first odd base for all prime hubs 5 mod 8

The [class theorem](57_skew_first_base_all_prime_hubs.md) shows that the conditional two-trade repair from item 55 has a suitable primitive root for every prime `p≡5 (mod 8)`, `p≥29`. A character-sum bound handles `p−1≥10^7`; a [C++17 finite sweep](57_skew_first_base_finite_sweep.cpp) checks all 166202 remaining primes. Thus `d(K_{p,p+2})=(3p+5)/2`, and the same optimum holds at `t=p+2+pq` for `q≥0`. Item 54 separately covers `p=13`. This result leaves the other leaf residues open.

## 58. A simultaneous repair at the second odd base

The [one-trade theorem](58_skew_second_base_one_trade.md) proves `d(K_{p,p+4})=(3p+11)/2` for every prime `p≡5 (mod 8)`, `p≥13`. It grows two translated antipodal pages before repairing either, then uses one page-to-page checkerboard trade that joins both split colors. A quartic character-sum bound supplies a valid trade for `p≥53`; three explicit small rectangles cover `p=13,29,37`. The [full-partition replay](58_skew_second_base_one_trade.py) checks six primes, and a [line scan](58_skew_second_base_line_scan.py) checks the candidate through 1000. Offsets cover `t=p+4+pq`, `q≥0`; item 69 later proves the full prime-class formula.

## 59. Every large leaf count with forty-nine bipartite hubs

The [forty-nine-hub formula note](59_fortynine_hub_all_residues.md) proves `d(K_{49,t})=t+ceil(24t/49)` for every `t≥48`. A saved skew strong starter gives 23 compatible translated two-component growth pages. Eighteen support-preserving trades repair three split square colors, and one more repairs each page color. The [saved certificates](59_fortynine_hub_odd_seeds.json) cover all 24 odd bases; a [stdlib generator](59_fortynine_hub_generator.py) reproduces them, a [trade audit](59_fortynine_hub_trace_audit.py) replays all 708 recorded moves, and an [independent checker](59_fortynine_hub_independent_audit.py) audits all 49 base residues and offset lifts. Item 61 next gives a connected 51-hub square and even bases, while its odd bases remain open.

## 60. A growing range of paired antipodal pages

The [sequential-pair theorem](60_skew_adjacent_pairs.md) proves the optimal `K_{p,p+4r}` partition for every prime `p≡5 (mod 8)` whenever `2r≤(p−3)/2` and `16r<p−3√p+10`, and extends it by `p`-leaf offsets. Two arithmetic progressions give the exact earlier-overlap exclusions; a quartic character bound guarantees one page-to-page trade for each pair in this initial range. The [full checker](60_skew_adjacent_pairs_full_replay.py) replays all even prefixes at six primes through 101. The [Python criterion scan](60_skew_adjacent_pairs_criterion_scan.py) covers all 42 class primes through 1000; an independently audited [C++ counting scan](60_skew_adjacent_pairs_final_scan.cpp) checks all 19,622 through one million, with at least two final-prefix witnesses each. A second [fast existence scan](60_skew_adjacent_pairs_fast_existence_scan.cpp) checks all 166,203 through ten million. Nested exclusions extend each final-prefix witness to all earlier even prefixes. Item 68 gives a separate uniform late-prefix proof for all class primes at and above 60 million.

## 61. A connected square at fifty-one hubs and a starter limit

The [fifty-one-hub note](61_fiftyone_hub_partial.md) certifies the optimal square base `K_{51,51}` with 32 support-preserving trades, giving 51 singleton spokes and 25 simple Hamilton cycles. The even weave and 51-leaf offset lift cover 27 of the 51 residue classes; the 24 other odd bases remain open. The [saved square certificate](61_fiftyone_hub_square_seed.json), [generator](61_fiftyone_hub_square_generator.py), [trade replay](61_fiftyone_hub_trace_audit.py), and [independent audit](61_fiftyone_hub_independent_audit.py) check this finite construction. A separate [sum-of-squares obstruction](61_cyclic_three_starter_obstruction.md) proves that the exact skew rainbow starter-page template from 49 hubs cannot work at any odd cyclic modulus divisible by three; it leaves the graph formula open.

## 62. First-base repairs of four-, eight-, and sixteen-component pages

The [multi-component note](62_one_mod8_first_base.md) gives finite first odd-base certificates from the antipodal starter for `p=41,73,89,97,113`, all `1 (mod 8)`. Their pages begin with 4, 4, 4, 16, and 8 components and need 5, 4, 6, 17, and 9 support-preserving trades, respectively. The [saved traces](62_one_mod8_first_base_traces.json) and [independent replay](62_one_mod8_first_base_audit.py) verify exact spoke coverage and `d(K_{p,p+2})=(3p+5)/2` in each case. Offsets give the same equality for `t=p+2+pq`; a uniform class theorem remains open.

## 63. Every large leaf count with fifty-three bipartite hubs

The [fifty-three-hub formula note](63_fiftythree_hub_all_residues.md) proves `d(K_{53,t})=t+ceil(26t/53)` for every `t≥52`. Translated antipodal pages are repaired in consecutive pairs at even odd-base prefixes; the first single page uses two trades, and each later unpaired page uses one additional trade. The [saved walks and traces](63_fiftythree_hub_odd_seeds.json) cover the square and all 25 growth prefixes. A [deterministic generator](63_fiftythree_hub_generator.py) reproduces the certificate, a [trade replay](63_fiftythree_hub_trace_audit.py) checks all 170 switches, and an [independent audit](63_fiftythree_hub_independent_audit.py) verifies all 53 base residues and offset lifts. The next unresolved fixed odd hub count is 51, whose square and even residues are covered by item 61.

## 64. Two trades repair the first three antipodal pages

The [three-page theorem](64_skew_third_base_two_trades.md) proves `d(K_{p,p+6})=(p+6)+(p−1)/2+3` for every prime `p≡5 (mod 8)`, `p≥13`, using one trade between pages 1 and 2 and a second between pages 1 and 3. A quartic character count supplies the two line patterns uniformly for `p≥53`; the [self-contained replay](64_skew_odd_prefix_replay.py), [independent audit](64_skew_three_independent_audit.py), and [small-prime all-root check](64_skew_three_all_roots_audit.py) cover the remaining three primes. Pairing later pages gives a partial theorem at odd prefix `j=2r+1≥5` under `16r<p−3√p+2`, plus `p`-leaf offsets. A [finite criterion scan](64_skew_odd_prefix_criterion_scan.py) finds odd-prefix witnesses for all 42 class primes through 1000, while full partitions are replayed at maximal odd prefixes through `p=61`. The [orientation-limit note](64_skew_anchor_orientation_limit.md) shows why one tempting repeated-anchor rule fails at `p=29`; item 68 later resolves the late-prefix case uniformly at and above 60 million.

## 65. Why the first antipodal page needs a setup trade

The [first-switch obstruction](65_skew_first_switch_obstruction.md) proves that for a prime `p≡1 (mod 4)` with an odd factor `q>1` in `p−1=2Aq`, no single support-preserving checkerboard rectangle among the first-base starter colors strictly reduces the number of cycle components. Opposite-slope square edges force the page endpoints into the same component; equal-slope edges split the square cycle. The [independent replay](65_skew_first_switch_trace_audit.py) confirms the zero-gain initial steps in the five saved `p≡1 (mod 8)` examples. This is a local obstruction for this starter and trade type; it does not limit other constructions.

## 66. A single residue statement for the five-mod-eight prime class

The [consolidated theorem](66_skew_prime_hub_consolidated.md) collects the exact class result without treating each odd base as a separate headline. For every prime `p≡5 (mod 8)`, `p≥53`, it gives the sharp formula at every even base `p−1,p+1,…,2p−2` and every odd base `p+2j` with `0≤j≤(p−3)/2` and `8j<p−3√p+10`, plus all `p`-leaf offsets. A source table identifies the proof for each residue; one arithmetic appendix gathers the first-base primitive-root sweep, the shared quartic character bound, and the finite criterion scans. Item 68 strengthens this to all residues at and above 60 million; the partial range here remains useful for smaller primes.

## 67. The geometry of the last antipodal pair

The [late-prefix note](67_skew_late_prefix_geometry.md) maps the two exact relabel-exception progressions to `−I∪−aI` for an interval `I`, illustrated in a [generated diagram](art/skew_late_prefix_geometry.svg). This reduces the hardest pair's available parameter count to an interval-dilation intersection. Fourier completion and [Katz's mixed character-sum bound](https://web.math.princeton.edu/~nmk/nsingmixedfinal.pdf) give an explicit sufficient size condition. The conditional subfamily `a=−3` meets it above one billion when `a` has the required order; an [exact arithmetic certificate](67_skew_minus_three_witness.py) verifies one such prime, `p=1,000,000,453`, proving the full sharp formula for every `t≥p−1` at that fixed hub count. An [all-root finite check](67_skew_late_prefix_all_roots.py) finds survivors for every primitive-square parameter at all 78 eligible primes through 2000. Item 68 supplies the uniform interval-intersection bound.

## 68. Every residue at large five-mod-eight prime hubs

The [half-interval overlap theorem](68_half_interval_overlap_all_large_primes.md) proves that for any odd `n=2k+1` and unit `a≠±1`, the interval `H={1,…,k}` satisfies `|H∩aH|≥ceil(k/3)`. It is sharp at every odd `n` coprime to 3, using `a=−3`. At the last antipodal page pair this leaves at least `ceil(k/3)` allowed parameters, exceeding the item 67 mixed-character error for every prime `p≡5 (mod 8)` with `p≥60,000,000`. Combining the existing page repairs, square and even bases, and offset lift proves `d(K_{p,t})=t+ceil(((p−1)/2)t/p)` for **every `t≥p−1`** throughout this infinite prime-class tail. The [finite overlap scan](68_half_interval_overlap_scan.cpp) checks all units at odd moduli through 10,000 as a backstop; the proof is elementary and independent of the scan. Item 69 checks the exact criterion for every smaller eligible prime, completing the full class formula with a finite computational component.

## 69. Every residue for every five-mod-eight prime hub

The [full-class theorem](69_skew_prime_hub_all_residues.md) combines item 68's analytic tail with an [exact finite scan](69_skew_full_residue_finite_scan.cpp) of all 890,703 primes `p≡5 (mod 8)` with `13≤p<60,000,000`. Each prime has a least-primitive-root witness in the character-good complement of the last odd page pair's exact exception set; nesting makes that witness serve every earlier pair. The scan's Jacobi screen is checked by Euler's criterion at every accepted point, an [independent full-range C++ audit](69_skew_full_residue_independent_audit.cpp) matches the exact witness digest, and a [literal-set Python crosscheck](69_skew_full_residue_small_crosscheck.py) matches all 313 eligible primes through 10,000. Together with the first-base, square, even-base, and offset constructions, this gives the **computer-assisted class formula** `d(K_{p,t})=t+ceil(((p−1)/2)t/p)` for every such prime `p≥13` and every `t≥p−1`; [item 14](14_bipartite_five.md) supplies `p=5`. A uniform symbolic proof below 60 million remains open.

## 70. When the half-interval overlap bound is exact

The [equality-pattern note](70_half_interval_equality_patterns.md) records a new question left by item 68: which units attain `|H∩aH|=ceil(k/3)`? The bound is provably sharp for every odd modulus coprime to 3 via `a=−3` and its inverse. An [exact floor-sum scan](70_half_interval_equality_scan.cpp) checks 20,253,334 nontrivial unit multipliers at every odd modulus through 10,000. Beyond the small exceptional multipliers at `n=11,17`, all equality cases coprime to 3 are `−3` or its inverse; divisible-by-3 equality appears only at `n=9,15,21,27` in the tested range. A radial-displacement argument proves that any new coprime-to-3 equality case at `n≥23` must have odd radius at least 5. The global classification remains conjectural.
