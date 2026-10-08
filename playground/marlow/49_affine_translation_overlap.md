# Translation overlap is a difference-pair count

The [affine growth criterion](35_compatible_growth_criterion.md) needs near-Hamilton pages whose selected translates share at most one edge. A page's overlap profile has a compact description that separates this translation problem from finding the page itself.

Let `p` be an odd prime, `k=(p−1)/2`, and let `Q` be a cycle on the nonzero residues with `p−1` edges. Suppose each cyclic difference color `d∈{1,…,k}` occurs exactly twice among its edges, once in each alternating matching. For color `d`, the two edges are translates of one another by a nonzero shift `δ_d`, unique up to sign. Write `D_d=min(δ_d,p−δ_d)`. Then for every nonzero shift `c`,

> **`|E(Q)∩E(Q+c)| = #{d : D_d=min(c,p−c)}`.**

Indeed, translation preserves the difference color, so an overlapping edge must match the *other* edge of its color. That happens exactly at the shift taking one edge to the other. Thus a shift is compatible with `Q` precisely when its displacement magnitude occurs at most once among the `D_d`. The [checker](49_affine_translation_overlap.py) verifies this identity directly for the existing `p=17,29,37` pages and prints their multiplicities.

This gives a conditional route at `p=41`. Suppose one 40-cycle `Q` also has the distinct midpoint labels and alternating rainbow matchings required by item 35, and every displacement magnitude that occurs more than once among its twenty `D_d` lies in `{a,3a}` up to sign for some nonzero `a`. Take the nineteen centers

`a·{1,3,5,…,19,24,26,28,…,40} (mod 41)`.

No two listed residues differ by `±1` or `±3` modulo 41, so any two selected translates have at most one common edge. The list is maximal under those two forbidden shifts: avoiding `±1` alone permits at most twenty points on the 41-cycle; a twenty-point selection would have nineteen cyclic gaps of size two and one gap of size three, violating the `±3` condition. The checker verifies the explicit nineteen-point set and draws its [residue circle](art/fortyone_compatible_centers.svg).

Under the stated **unproved page-existence hypothesis**, those nineteen translates supply all nineteen difficult odd bases at 41 hubs, and the even weave plus offset lift would prove `d(K_{41,t})=t+ceil(20t/41)` for every `t≥40`. The overlap identity and center set are proved here; no forty-one-hub page meeting the hypothesis has yet been found. Existing pages at `p=17,29,37` show how the displacement multiplicities can cluster, but do not establish the required `p=41` pattern.
