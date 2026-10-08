# Every large leaf count with fifteen bipartite hubs

For `d(G)`, the minimum number of simple cycles and singleton edges partitioning `E(G)`, we have the finite-hub formula

> **`d(K_{15,t})=t+ceil(7t/15)` for every `t≥14`.**

This uses the lower bound, the [even-base decomposition](24_even_base_residues.md) from Sotteau or the explicit [item-30 weave](30_even_hub_cycle_weave.md) for eight seeds, the fifteen-leaf offset block, and six saved odd-base edge certificates. The result does not prove the formula for every odd hub count; publication priority is unverified.

**Lower bound.** Every leaf has odd degree fifteen and therefore at least one singleton spoke. If the number of singleton spokes is `s=t+X`, the cycles use `7t−X/2` leaf appearances. Since a simple cycle uses at most fifteen leaves,

`r+s ≥ t+7t/15+(29/30)X ≥ t+7t/15`.

The nonnegative `X` is even because every leaf has an odd number of singleton spokes. Thus `d(K_{15,t})≥t+ceil(7t/15)`. If `X≥2`, the real lower bound rises by at least `29/15>1`, so equality in the formula requires exactly one singleton spoke per leaf.

**Fifteen bases.** For each even `b=14,16,…,28`, make one hub's `b` spokes singleton parts. The residual `K_{14,b}` meets [Sotteau's criterion](24_even_base_residues.md): both part sizes are even and at least 14, and 28 divides `14b`. It decomposes into `b/2` cycles of length 28, exactly `ceil(7b/15)` for this base range. At `b=15`, fifteen diagonal singletons and seven 30-edge Hamilton cycles form the offset block of [item 10](10_odd_hub_blocks.md). For the remaining odd bases `b=17,19,21,23,25,27`, the saved [JSON walks](29_fifteen_hub_odd_seeds.json) explicitly give every singleton spoke and alternating hub/leaf cycle. The [checker](29_fifteen_hub_all_residues.py) verifies exact coverage, simplicity, lengths, counts, and lifted copies. A separate read-only checker independently verified all six raw witnesses; the saved JSON has the same SHA-256 digest `ae9dbd18927bc38a938ba3db66d287a037f24269789642ebe1a2113c57c7d272`.

| base `b` | method | cycles | parts |
| ---: | --- | ---: | ---: |
| 14 | Sotteau | 7 | 21 |
| 15 | offset | 7 | 22 |
| 16 | Sotteau | 8 | 24 |
| 17 | walks | 8 | 25 |
| 18 | Sotteau | 9 | 27 |
| 19 | walks | 9 | 28 |
| 20 | Sotteau | 10 | 30 |
| 21 | walks | 10 | 31 |
| 22 | Sotteau | 11 | 33 |
| 23 | walks | 11 | 34 |
| 24 | Sotteau | 12 | 36 |
| 25 | walks | 12 | 37 |
| 26 | Sotteau | 13 | 39 |
| 27 | walks | 13 | 40 |
| 28 | Sotteau | 14 | 42 |

The odd-base witness at `b=15+2j`, `1≤j≤6`, has seven full 30-edge cycles and `j` short 28-edge cycles. Its singleton-spoke hub multiplicities are three at `j` hubs and one at the others; each short cycle omits a different triple-spoke hub. This realizes the sufficient design of [item 27](27_odd_hub_design_question.md), with capacity deficit `15(7+j)−7(15+2j)=j`. The [residue ladder](art/fifteen_hub_residue_ladder.svg) shows which method covers each base.

**All-residue lift.** Every `t≥14` is uniquely `b+15q` for `b∈{14,…,28}`, `q≥0`. Add `q` disjoint fifteen-leaf offset blocks, each with fifteen diagonal singletons and seven Hamilton cycles. Each adds 22 parts, and `t+ceil(7t/15)` rises by 22 under `t→t+15`. This proves the formula for every such `t`. The checker tests the seven odd bases and their lifts through eleven added blocks; the even bases follow from Sotteau or the explicit weave. [Items 31–32](README.md) cover the next two odd hub counts; the first unchecked odd hub count is composite `h=27`; see [items 34, 37, and 38](README.md).
