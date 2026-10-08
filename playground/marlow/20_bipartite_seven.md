# A seven-hub seed one leaf beyond the offset block

Let `d(G)` be the least number of simple cycles and singleton edges partitioning `E(G)`. The seven-hub complete bipartite graph has an exact residue family:

> **For every `q≥0`, `d(K_{7,8+7q})=12+10q`.**

The seed `K_{7,8}` uses eight singleton spokes and four 12-edge cycles. Appending the seven-leaf offset block from [item 10](10_odd_hub_blocks.md) adds seven singleton spokes and three 14-edge Hamilton cycles each time. The lower bound meets this construction exactly. [Bucić–Montgomery, §6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf) give the general odd-side bipartite parity/capacity lower-bound mechanism; I have not determined whether this exact `7`-hub residue family is already in the literature.

**Lower bound.** Each leaf of `K_{7,t}` has odd degree seven, so an odd number of its spokes must be singleton parts. Write their total as `s=t+X`, with `X≥0`. The cycles use `3t−X/2` leaf appearances in total, and a simple bipartite cycle visits at most seven leaves. If there are `r` cycles, `7r≥3t−X/2`. Therefore

`r+s≥t+3t/7+13X/14≥t+3t/7`, giving `d(K_{7,t})≥t+ceil(3t/7)` for all `t`. At `t=8+7q`, this becomes `12+10q`.

**Eight-leaf certificate.** Label hubs `0,…,6` and leaves `A,…,H`. Make the spokes `0A,0B,1C,1D,2E,2F,3G,3H` singleton parts. The four cycles below close back to their starting hub:

| cycle | alternating hub–leaf walk |
| ---: | --- |
| 1 | `1,E,3,D,4,F,5,C,6,G,2,H` |
| 2 | `0,F,3,A,2,B,4,G,5,E,6,H` |
| 3 | `0,D,6,A,5,H,4,C,3,B,1,G` |
| 4 | `0,C,2,D,5,B,6,F,1,A,4,E` |

Each walk has six distinct hubs and six distinct leaves. [`20_bipartite_seven.py`](20_bipartite_seven.py) checks all 56 spokes occur exactly once among these cycles and singleton parts. The [spoke matrix](art/bipartite_seven_eight.svg) colors each cell by its cycle or singleton role. This certificate gives `d(K_{7,8})≤12`, and the lower bound gives equality. In any optimum at `t=8`, each leaf must have exactly one singleton spoke: `X` is even, so `X≥2` would increase the lower bound by more than one part.

**Seven-leaf lift.** For each new block of seven leaves indexed by residues `i mod 7`, take `(i,i)` as a singleton spoke. Pair spoke offsets `(1,2)`, `(3,4)`, and `(5,6)` into three Hamilton cycles. For offset pair `(o,o+1)`, one explicit walk alternates hubs `0,−1,…,−6 (mod 7)` with leaves `hub+o (mod 7)`. It visits every hub and new leaf once, and the paired offsets cover all remaining block spokes. Thus every block adds `7+3=10` parts, exactly the lower-bound increase under `t→t+7`. The script checks edge coverage for `q=0,…,6`; the modular walk proves it for every `q`.

This says nothing yet about the other six residue classes. A separate exploratory search is underway for small seeds; no broad all-`t` formula is assumed. An independent skeptical audit checked the lower bound, all 56 seed spokes, the modular seven-leaf lift, and every cell in the SVG matrix.
