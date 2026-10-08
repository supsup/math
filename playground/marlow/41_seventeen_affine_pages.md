# A non-primitive growth page at seventeen hubs

The primitive-power pages in [item 34](34_prime_two_leaf_growth.md) fail their alternating-color test when `p≡1 (mod 4)`. That does not prevent a different page from satisfying the [conditional growth criterion](35_compatible_growth_criterion.md). At `p=17`, an explicit 16-cycle does, and eight of its translates have pairwise overlap at most one edge. Seven suffice to give a structural alternative to the finite [seventeen-hub proof](31_seventeen_hub_all_residues.md).

Use the affine square seed from item 34: for each difference class `d=1,…,8`, the hub cycle `0,d,2d,…,16d` labels its edge `{u,v}` by midpoint `(u+v)/2 mod 17`. Every full cycle and every near-one-factor label is complete. Take the following page, omitting center `0`:

`Q=(1,2,9,14,8,16,13,6,7,11,15,12,4,10,5,3)`.

Its even-indexed edge differences are `(1,5,8,7,4,3,6,2)` and its odd-indexed differences are `(7,6,3,1,4,8,5,2)`. Each list is a permutation of `1,…,8`, so each alternating matching takes one edge from every affine full-cycle color. The midpoints around `Q` are

`(10,14,3,11,12,6,1,15,9,13,5,8,7,16,4,2)`,

which are exactly `F_17\{0}`. Translation preserves both properties. For centers

`A={0,1,2,3,8,9,10,11}`,

the pages `Q+a` have **at most one hub edge in common for every distinct `a,b∈A`**: among the 28 pairs, 17 are edge-disjoint and 11 share one edge. This is a finite exact check on the displayed 16-edge set and its eight translates. In particular any seven centers meet all three hypotheses of item 35. Repeated two-leaf replacement therefore constructs the difficult odd bases `t=19,21,…,31` from the affine `K_{17,17}` square; the explicit even weave and 17-leaf offset lift yield `d(K_{17,t})=t+ceil(8t/17)` for all `t≥16`. The eighth center also yields an optimal partition at `t=33`, though that residue is already covered by lifting the even `t=16` base.

The [checker](41_seventeen_affine_pages.py) verifies the displayed differences, midpoints, 28 intersections, and every edge of the resulting partitions through eight growth moves. Its [diagram](art/seventeen_affine_pages.svg) lists each difference class's even and odd selected edges. The check is a finite certificate for this `p=17` construction, not a construction for all primes `1 (mod 4)`. Publication priority of this particular page and its use here is unverified.

**A boundary at `p=13` for this affine seed.** A page satisfying the first two hypotheses of item 35 would split into two perfect matchings on `F_13\{0}`, each using all six difference classes and having six distinct midpoint labels; the two midpoint sets must be disjoint, and their union must be one 12-cycle. An exhaustive enumeration of all `11!!=10,395` perfect matchings leaves only eight with rainbow differences and distinct midpoints. Exactly eight eligible pairs have disjoint edges and midpoint sets. Four pairs form two 6-cycles, and four form three 4-cycles; none is connected. Translation gives the same conclusion at every center. Thus **no single growth page for the affine square exists at `p=13`**, even though [item 26](26_thirteen_hub_all_residues.md) proves the target formula there by other finite certificates. The script performs a pruned enumeration; a separate all-10,395-matching enumeration reproduced the count of eight. This obstruction is specific to the affine seed and the one-step criterion.
