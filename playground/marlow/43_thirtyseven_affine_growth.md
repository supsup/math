# A split-overlap growth family at thirty-seven hubs

At `p=37≡1 (mod 4)`, the affine square and two explicit near-Hamilton page shapes satisfy the **ordered, parity-split overlap test** of [item 35](35_compatible_growth_criterion.md). This proves another fixed-prime exact formula:

> **`d(K_{37,t})=t+ceil(18t/37)` for every `t≥36`.**

As before, `d(G)` counts the fewest simple cycles and singleton edges partitioning `E(G)`. The result is specific to hub count 37; it does not imply the formula at the still unchecked composite counts 33 and 35, or at every prime `1 (mod 4)`. Publication priority of the page construction and its use here is unverified.

Start with the affine square seed of [item 34](34_prime_two_leaf_growth.md): Hamilton hub colors are differences `d=1,…,18`, and an edge `{u,v}` carries midpoint leaf `(u+v)/2 mod 37`. Use this 36-cycle omitting zero for the first sixteen growth steps:

`Q=(1,30,13,20,28,4,14,15,36,10,32,27,33,6,2,17,8,12,5,25,11,29,34,18,16,19,22,31,7,21,3,9,35,23,24,26)`.

Translate `Q` in the order of centers

`(36,35,34,30,29,25,24,23,19,18,14,13,9,8,4,3)`.

For the seventeenth and final move, use a different page centered at zero:

`R=(1,3,16,28,23,19,29,11,5,26,9,20,35,15,18,27,36,31,30,22,14,8,12,34,13,10,17,4,2,32,6,33,21,7,25,24)`.

For each shape, its even-indexed and odd-indexed edges each use every affine difference color exactly once, and its 36 midpoint labels are exactly `1,…,36`. Translation preserves these properties. Among the `binom(16,2)=120` pairs of earlier translated pages, 58 are edge-disjoint and 62 share one edge. The final `R` meets two earlier pages in zero edges, five in one edge, and nine in **two edges**. In every two-edge case, one edge belongs to the earlier page's even matching and one to its odd matching. Indeed, `R` meets *each* earlier matching in at most one edge. Thus item 35's weaker **ordered** criterion applies: an earlier move's two fresh leaf labels occupy separate parity matchings, and neither can be displaced twice by `R`. The [overlap diagram](art/thirtyseven_last_page.svg) gives all sixteen final-page counts.

The repeated two-leaf move constructs all difficult odd bases `t=39,41,…,71`. At `t=37+2j`, `1≤j≤17`, there are `t` singleton spokes, eighteen full 74-edge cycles, and `j` short 72-edge cycles, for `t+18+j=t+ceil(18t/37)` parts. The explicit [even weave](30_even_hub_cycle_weave.md) covers the nineteen even bases `36,38,…,72`, while the 37-leaf [offset block](10_odd_hub_blocks.md) covers base 37 and lifts every base residue. The standard parity/cycle-capacity lower bound, also described for these graphs by [Bucić–Montgomery, Section 6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf), matches this part count.

The [checker](43_thirtyseven_affine_growth.py) verifies each page's difference and midpoint sets, all earlier pairwise intersections, the split final intersections, and every spoke of the seventeen successive growth partitions. A second direct reconstruction of all seventeen partitions from the displayed page lists found the same exact edge cover and simple cycles. The solver was used only to discover a candidate last page; the two explicit page lists and center order are the finite certificate. This example shows that the parity-split refinement is strictly useful: the final page fails item 35's original at-most-one-total-edge condition for nine earlier pages, yet the growth remains valid.
