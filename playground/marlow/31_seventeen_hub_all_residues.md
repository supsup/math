# Every large leaf count with seventeen bipartite hubs

With `d(G)` the minimum number of simple cycles and singleton edges partitioning `E(G)`, the next finite-hub case is

> **`d(K_{17,t})=t+ceil(8t/17)` for every `t≥16`.**

The proof combines a parity/cycle-capacity lower bound, the explicit [even-side cycle weave](30_even_hub_cycle_weave.md), the seventeen-leaf offset block, and seven saved odd-base edge certificates. It is not a uniform theorem over all odd hub counts, and publication priority is unverified.

**Lower bound.** Every leaf has odd degree seventeen and must have at least one singleton spoke. With `s=t+X` singleton spokes, cycles use `8t−X/2` leaf appearances, at most seventeen per simple cycle. Thus

`r+s ≥ t+8t/17+(33/34)X ≥ t+8t/17`.

Because every leaf has an odd singleton-spoke count, `X` is nonnegative and even. Hence `d(K_{17,t})≥t+ceil(8t/17)`. If `X≥2`, the lower real bound rises by at least `33/17>1`, so every optimum uses exactly one singleton spoke per leaf.

**Seventeen base residues.** For each even `b=16,18,…,32`, make one hub's `b` spokes singleton parts. The remaining `K_{16,b}` is explicitly partitioned by the [item-30 weave](30_even_hub_cycle_weave.md) into `b/2` cycles of length 32; `ceil(8b/17)=b/2` on this range. At `b=17`, use seventeen diagonal singletons and eight 34-edge Hamilton cycles from the [odd-hub offset block](10_odd_hub_blocks.md). For the seven remaining odd bases `b=19,21,…,31`, the saved [JSON walks](31_seventeen_hub_odd_seeds.json) give every singleton and alternating hub/leaf cycle. The [checker](31_seventeen_hub_all_residues.py) verifies all seventeen base constructions explicitly, every spoke exactly once, and eleven lifted copies of each base. A separate read-only checker independently validated the seven raw odd witnesses and the even weave; the saved JSON matches the audited SHA-256 `7e6438d6505ecd8188ce6fc6d19a8971d04070aef4a312f701ecc2fc8e31f4bd`.

| base `b` | method | cycles | parts |
| ---: | --- | ---: | ---: |
| 16 | weave | 8 | 24 |
| 17 | offset | 8 | 25 |
| 18 | weave | 9 | 27 |
| 19 | walks | 9 | 28 |
| 20 | weave | 10 | 30 |
| 21 | walks | 10 | 31 |
| 22 | weave | 11 | 33 |
| 23 | walks | 11 | 34 |
| 24 | weave | 12 | 36 |
| 25 | walks | 12 | 37 |
| 26 | weave | 13 | 39 |
| 27 | walks | 13 | 40 |
| 28 | weave | 14 | 42 |
| 29 | walks | 14 | 43 |
| 30 | weave | 15 | 45 |
| 31 | walks | 15 | 46 |
| 32 | weave | 16 | 48 |

At odd `b=17+2j`, `1≤j≤7`, each witness uses eight full 34-edge cycles and `j` short 32-edge cycles. Its singleton-spoke multiplicities are three at `j` hubs and one at the others, and each short cycle omits a different triple-spoke hub. The capacity deficit is `17(8+j)−8(17+2j)=j`. The [residue ladder](art/seventeen_hub_residue_ladder.svg) shows the even weave, offset block, and saved-walk methods.

**Lift.** Every `t≥16` is uniquely `b+17q` for `16≤b≤32` and `q≥0`. Append `q` disjoint seventeen-leaf offset blocks, each containing seventeen diagonal singletons and eight Hamilton cycles. Each block adds 25 parts; `t+ceil(8t/17)` also rises by 25 under `t→t+17`. Thus every base reaches equality for its entire residue class. [Item 32](32_nineteen_hub_all_residues.md) handles `h=19`; the first unchecked odd hub count is prime `h=29≡1 (mod 4)`, beginning with `t=31`; see [items 34, 37, 38, and 40](README.md).
