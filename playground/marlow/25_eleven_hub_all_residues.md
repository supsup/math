# Every large leaf count with eleven bipartite hubs

With `d(G)` the minimum number of simple cycles and singleton edges partitioning `E(G)`, the eleven-hub complete bipartite graph satisfies

> **`d(K_{11,t})=t+ceil(5t/11)` for every `t≥10`.**

The range `t<10` is not evaluated here. The proof combines the general parity/cycle-capacity bound, the [even-base decomposition](24_even_base_residues.md) (from Sotteau or the explicit [item-30 weave](30_even_hub_cycle_weave.md)) for six seeds, the eleven-leaf offset block, and four explicitly checked odd-base certificates. The saved edge certificates make the result independent of how the witnesses were found. Publication priority is unverified.

**Lower bound.** Each leaf has odd degree eleven, so at least one of its spokes is a singleton. If `s=t+X` spokes are singleton parts, the cycles have `5t−X/2` leaf appearances, at most eleven per simple cycle. Hence

`r+s≥t+5t/11+21X/22`, and therefore `d(K_{11,t})≥t+ceil(5t/11)`.

The excess `X` is even: every leaf has an odd number of singleton spokes. If `X≥2`, the displayed bound increases by at least `21/11>1`, more than the rounding gap. Thus every partition attaining the formula uses **exactly one singleton spoke per leaf**.

**Eleven base residues.** For even `b=10,12,14,16,18,20`, make all `b` spokes from one hub singleton parts. The residual `K_{10,b}` satisfies [Sotteau's criterion](24_even_base_residues.md) and decomposes into `b/2` simple 20-edge cycles, meeting the lower bound. At `b=11`, use the offset block of [item 10](10_odd_hub_blocks.md): eleven diagonal singletons and five 22-edge Hamilton cycles. For the remaining odd bases, [`25_eleven_hub_odd_seeds.json`](25_eleven_hub_odd_seeds.json) gives all singleton endpoints and alternating hub/leaf cycle walks. [`25_eleven_hub_odd_seeds.py`](25_eleven_hub_odd_seeds.py) checks their simplicity, exact spoke coverage, and part counts.

| base leaves `b` | method | cycle count | parts |
| ---: | --- | ---: | ---: |
| 10 | Sotteau | 5 | 15 |
| 11 | offset block | 5 | 16 |
| 12 | Sotteau | 6 | 18 |
| 13 | explicit walks | 6 | 19 |
| 14 | Sotteau | 7 | 21 |
| 15 | explicit walks | 7 | 22 |
| 16 | Sotteau | 8 | 24 |
| 17 | explicit walks | 8 | 25 |
| 18 | Sotteau | 9 | 27 |
| 19 | explicit walks | 9 | 28 |
| 20 | Sotteau | 10 | 30 |

The odd seeds share a sharp shape. At `b=11+2j` for `j=0,…,4`, the certificate has five 22-edge cycles and `j` 20-edge cycles. Its singleton spokes have multiplicity three at `j` hubs and one at each other hub. This matches the cycle-capacity deficit exactly: with `r=5+j`, the total number of missing hub visits is `11r−5b=j`. The [residue ladder](art/eleven_hub_residue_ladder.svg) shows which seed method covers each of the eleven bases.

**All-residue lift.** For `t≥10`, choose the unique `b∈{10,…,20}` with `t=b+11q`, `q≥0`. Each new block of eleven leaves has eleven diagonal singleton spokes and five 22-edge Hamilton cycles from adjacent offset pairs `(1,2),…,(9,10)`. The block adds 16 parts, while `t+ceil(5t/11)` also rises by 16 under `t→t+11`. Thus the seed plus `q` blocks is optimal for every `t≥10`. The script additionally checks the five odd bases and their lifts through `q=11`; the six even base decompositions follow from Sotteau rather than the finite checker.

The four JSON witnesses are directly inspectable and reproducible with the supplied checker; the even bases follow from Sotteau or the explicit weave, outside that finite checker. The result makes no claim of a new general Erdős–Gallai bound or a uniform construction for every odd hub count.
