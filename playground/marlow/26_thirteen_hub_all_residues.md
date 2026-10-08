# Every large leaf count with thirteen bipartite hubs

Let `d(G)` be the minimum number of simple cycles and singleton edges partitioning `E(G)`. Then

> **`d(K_{13,t})=t+ceil(6t/13)` for every `t≥12`.**

This finite-hub result combines a general lower bound, the [even-base decomposition](24_even_base_residues.md) from Sotteau or the explicit [item-30 weave](30_even_hub_cycle_weave.md), one offset block, and five saved odd-base edge certificates. It does not establish the analogous formula uniformly in the odd hub count. Publication priority has not been checked.

**Lower bound.** Every leaf has odd degree thirteen, hence at least one incident singleton spoke. If there are `s=t+X` singleton spokes, then the remaining cycles make `6t−X/2` leaf appearances. A simple cycle visits at most thirteen leaves, so

`r+s ≥ t+6t/13+(25/26)X ≥ t+6t/13`.

Here `X≥0` is even because every leaf has an odd number of singleton spokes. Thus `d(K_{13,t})≥t+ceil(6t/13)`. Equality requires exactly one singleton spoke at each leaf: `X≥2` raises the displayed real lower bound by `25/13>1`, greater than any rounding slack.

**Thirteen base residues.** For each even `b=12,14,…,24`, make one hub's `b` spokes singleton parts. The remaining `K_{12,b}` decomposes into `b/2` cycles of length 24 by [Sotteau's criterion](24_even_base_residues.md): both part sizes are even and at least 12, and 24 divides `12b`. For `b=13`, use thirteen diagonal singletons and six 26-edge Hamilton cycles in the offset block of [item 10](10_odd_hub_blocks.md). For the odd bases `b=15,17,19,21,23`, the saved [JSON edge walks](26_thirteen_hub_odd_seeds.json) give the singleton spokes and simple cycles. The [checker](26_thirteen_hub_all_residues.py) verifies every edge exactly once, all cycle lengths and counts, and the lifted certificates.

| base leaves `b` | method | cycles | parts |
| ---: | --- | ---: | ---: |
| 12 | Sotteau | 6 | 18 |
| 13 | offset block | 6 | 19 |
| 14 | Sotteau | 7 | 21 |
| 15 | explicit walks | 7 | 22 |
| 16 | Sotteau | 8 | 24 |
| 17 | explicit walks | 8 | 25 |
| 18 | Sotteau | 9 | 27 |
| 19 | explicit walks | 9 | 28 |
| 20 | Sotteau | 10 | 30 |
| 21 | explicit walks | 10 | 31 |
| 22 | Sotteau | 11 | 33 |
| 23 | explicit walks | 11 | 34 |
| 24 | Sotteau | 12 | 36 |

The odd certificate at `b=13+2j`, `1≤j≤5`, has six full 26-edge cycles and `j` 24-edge cycles. Singleton-spoke hub multiplicities are three at `j` hubs and one at the others. The `j` short cycles account exactly for the cycle-capacity deficit `13(6+j)−6(13+2j)=j`. The [residue ladder](art/thirteen_hub_residue_ladder.svg) distinguishes the three seed methods.

**All-residue lift.** Write any `t≥12` uniquely as `t=b+13q`, with `12≤b≤24` and `q≥0`. Add `q` disjoint thirteen-leaf offset blocks, each comprising thirteen diagonal singletons and six 26-edge Hamilton cycles. This adds `19q` parts. Since `ceil(6(b+13q)/13)=ceil(6b/13)+6q`, the result meets the lower bound for every `t≥12`.

The five odd seeds have complete, inspectable edge certificates. The seven even seeds follow from the published theorem or the explicit weave rather than a search witness. The general odd-hub question is reduced further in [item 27](27_odd_hub_design_question.md).
