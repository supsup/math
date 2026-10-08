# Every large leaf count with thirty-five bipartite hubs

Another composite odd hub count meets the proposed exact formula. For `d(G)` the least number of simple cycles and singleton edges partitioning `E(G)`,

> **`d(K_{35,t})=t+ceil(17t/35)` for every `t≥34`.**

This is a fixed-hub theorem from explicit even bases, one offset base, sixteen saved odd-base edge certificates, and a residue lift. It does not yield a uniform construction for composite hub counts. Publication priority is unverified.

**Lower bound.** Every leaf has odd degree 35, so at least one singleton spoke. If the singleton count is `s=t+X`, the cycles use `17t−X/2` leaf appearances, at most 35 per simple cycle. Thus `r+s≥t+17t/35+(69/70)X`, giving `d(K_{35,t})≥t+ceil(17t/35)`. The nonnegative `X` is even because each leaf has an odd singleton-spoke count. If `X≥2`, the real bound rises by `69/35>1`, so a partition meeting it has one singleton at each leaf. This parity/cycle-capacity mechanism is the bipartite Erdős/Gallai example discussed by [Bucić–Montgomery, Section 6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf); the upper construction is the finite result here.

**All 35 base residues.** For each even `b=34,36,…,68`, make hub 34's `b` spokes singleton and apply the [even-side weave](30_even_hub_cycle_weave.md) to partition the residual `K_{34,b}` into `b/2` simple 68-edge cycles. Here `ceil(17b/35)=b/2`. At `b=35`, use 35 diagonal singleton spokes and seventeen 70-edge [offset cycles](10_odd_hub_blocks.md). The sixteen odd bases `b=37,39,…,67` use the saved [JSON walks](45_thirtyfive_hub_odd_seeds.json). At `b=35+2j`, `1≤j≤16`, each has seventeen full 70-edge cycles and `j` short 68-edge cycles, giving `b+17+j=b+ceil(17b/35)` parts. Singleton degrees are three at hubs `0,…,j−1` and one elsewhere, with the short cycles omitting those hubs one each. Their omitted leaves obey the [cyclic interval schedule](33_interval_omission_schedule.md). The schedule supplies vertex incidence only; the saved walks supply the connected, simple edge partition.

The [checker](45_thirtyfive_hub_all_residues.py) verifies all 35 base partitions, exact spoke coverage, cycle simplicity, interval omissions, and eleven lifted copies per base, then draws the [residue ladder](art/thirtyfive_hub_residue_ladder.svg). A separate direct audit reconstructed every saved walk and checked it against the original solver edge lists. The JSON SHA-256 is `06f9c12bf80ecf4fb4ffc3e5f01a8af2080f148ff4b972f47662db5170935bb9`.

**Lift.** Every `t≥34` is uniquely `b+35q` with `34≤b≤68`, `q≥0`. A disjoint 35-leaf offset block adds 35 singleton spokes and seventeen Hamilton cycles, or 52 parts. The lower bound rises by 52 under `t→t+35`, proving every residue. [Item 48](48_thirtynine_hub_all_residues.md) handles the next composite count, while [item 43](43_thirtyseven_affine_growth.md) covers prime `h=37` by structural growth.
