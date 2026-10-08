# Every large leaf count with twenty-one bipartite hubs

The first composite odd hub count beyond the earlier finite certificates also meets the proposed formula. With `d(G)` the minimum number of simple cycles and singleton edges partitioning `E(G)`,

> **`d(K_{21,t})=t+ceil(10t/21)` for every `t≥20`.**

The proof uses a general lower bound, the explicit [even-side weave](30_even_hub_cycle_weave.md), the 21-leaf [offset block](10_odd_hub_blocks.md), and nine independently checked odd-base edge certificates. This is a fixed-hub theorem, not a composite-hub construction for all orders; publication priority is unverified.

**Lower bound.** Every leaf has odd degree 21 and hence at least one singleton incident edge. If there are `s=t+X` singleton spokes, cycles use `10t−X/2` leaf appearances, at most 21 in a simple cycle. Thus

`r+s ≥ t+10t/21+(41/42)X ≥ t+10t/21`,

so `d(K_{21,t})≥t+ceil(10t/21)`. Here `X` is a nonnegative even integer. If `X≥2`, the real bound rises by `41/21>1`, so an optimum at this value has exactly one singleton spoke per leaf.

**All 21 base residues.** For each even `b=20,22,…,40`, make hub 20's `b` spokes singleton parts and weave the remaining `K_{20,b}` into `b/2` simple 40-edge cycles. On this range `ceil(10b/21)=b/2`. At `b=21`, take 21 diagonal singleton spokes and ten 42-edge offset cycles. At the nine remaining odd bases `b=23,25,…,39`, the saved [JSON walks](37_twentyone_hub_odd_seeds.json) specify every singleton and alternating simple cycle. For `b=21+2j`, `1≤j≤9`, each certificate has ten full 42-edge cycles and `j` short 40-edge cycles; there are `b+10+j=b+ceil(10b/21)` parts. Its singleton degrees are three at `j` hubs and one elsewhere; the short cycles omit those triple-spoke hubs one apiece. The omitted leaves follow the proved [cyclic interval schedule](33_interval_omission_schedule.md), but the actual edge assignments and connectivity come from these finite certificates.

The [checker](37_twentyone_hub_all_residues.py) reconstructs all 21 base partitions, verifies every spoke exactly once and every cycle simple, checks eleven lifted copies of each base, confirms the interval omission blocks, and draws the [residue ladder](art/twentyone_hub_residue_ladder.svg). A separate read-only checker independently rebuilt all nine odd bases, all eleven even bases, the offset base, and the lift. The saved JSON SHA-256 is `fb2e882a785228420ff6b806dd3a7278277f16aadc3aa1ff4b7c9ef5d3081d4a`.

**Lift.** Every `t≥20` is uniquely `b+21q` for `20≤b≤40`. Append `q` disjoint 21-leaf offset blocks, each adding 21 singleton spokes and ten Hamilton cycles. Each block adds 31 parts; `t+ceil(10t/21)` also rises by 31 under `t→t+21`. Hence every residue meets the lower bound. [Item 38](38_twentyfive_hub_all_residues.md) covers `h=25`. The next odd hub count outside the fixed cases and the [prime `3 (mod 4)` theorem](34_prime_two_leaf_growth.md) is composite `h=27`.
