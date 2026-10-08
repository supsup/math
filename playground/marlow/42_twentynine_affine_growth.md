# Every leaf count at twenty-nine prime hubs

The affine square has a compatible non-primitive growth page at `p=29≡1 (mod 4)`. It gives the first exact case beyond the finite-hub ladder and the prime `3 (mod 4)` family:

> **`d(K_{29,t})=t+ceil(14t/29)` for every `t≥28`.**

Here `d(G)` is the least number of simple cycles and singleton edges partitioning `E(G)`. This theorem is for the single hub count 29; it does not prove all primes `1 (mod 4)`. Publication priority of the explicit page and this application is unverified.

Start from the affine `K_{29,29}` square in [item 34](34_prime_two_leaf_growth.md): each difference class `d=1,…,14` gives a Hamilton hub cycle, with each hub-pair edge labeled by its midpoint modulo 29. The following 28-cycle omits hub 0:

`Q=(1,2,13,15,6,20,19,12,18,27,10,4,9,25,11,8,16,24,28,23,26,7,5,22,3,14,21,17)`.

Around `Q`, the even-indexed difference classes are

`(1,2,14,7,9,6,13,3,8,5,10,12,11,4)`,

and the odd-indexed classes are

`(11,9,1,6,12,5,14,8,4,3,2,10,7,13)`.

Each is a permutation of `1,…,14`, so each alternating matching takes one edge from every full-cycle color. The 28 midpoint labels of `Q` are exactly `1,…,28`, without repetition. Translation preserves both facts. For the thirteen centers

`A={2,5,8,11,12,14,15,18,21,24,25,27,28}`,

the pages `Q+a` have pairwise edge intersection at most one: of the 78 center pairs, 39 are disjoint and 39 share exactly one hub edge. Thus the affine square and these thirteen pages satisfy every hypothesis of the [conditional growth criterion](35_compatible_growth_criterion.md). Applying the two-leaf move successively gives all difficult odd bases `t=31,33,…,55`, with 14 full cycles and `j` short cycles at `t=29+2j` (`1≤j≤13`). The part count is `t+14+j=t+ceil(14t/29)`. The [even-side weave](30_even_hub_cycle_weave.md) gives the fifteen even bases `28,30,…,56`; the 29-leaf [offset block](10_odd_hub_blocks.md) supplies base 29 and lifts every base residue by 29. The parity/cycle-capacity argument, whose general bipartite form appears in [Bucić–Montgomery, Section 6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf), gives the matching lower bound.

The [checker](42_twentynine_affine_growth.py) verifies both rainbow difference lists, the exact midpoint set, all 78 page intersections, and exact spoke coverage and simple-cycle partitions after each of the thirteen growth moves. Its [edge table](art/twentynine_affine_growth.svg) shows the two selected edges and midpoints for every difference class. A bounded CP-SAT search found the page; the explicit 28-term page and 13-term center set are the mathematical certificate, so no solver output is needed to reproduce the proof. This construction also shows why the primitive-power parity obstruction in [item 36](36_p1_two_page_boundary.md) is specific to that page family.
