# Every leaf count with seven bipartite hubs

Let `d(G)` be the least number of simple cycles and singleton edges partitioning `E(G)`. The seven-hub complete bipartite graph has an exact formula:

> **`d(K_{7,t})=0,7,5,10,7,10` for `t=0,1,2,3,4,5`, respectively. For every `t≥6`, `d(K_{7,t})=t+ceil(3t/7)`.**

The seed `K_{7,8}` uses eight singleton spokes and four 12-edge cycles. Six other seeds cover the remaining residues `t=6,7,9,10,11,12`; appending the seven-leaf offset block from [item 10](10_odd_hub_blocks.md) adds seven singleton spokes and three 14-edge Hamilton cycles each time. The lower bound meets every construction exactly for `t≥6`. A similar parity and maximum-cycle-length argument for odd-side complete bipartite graphs appears in [Bucić–Montgomery, §6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf); I have not determined whether this exact `7`-hub formula is already in the literature.

**Lower bound.** Each leaf of `K_{7,t}` has odd degree seven, so an odd number of its spokes must be singleton parts. Write their total as `s=t+X`, with `X≥0`. The cycles use `3t−X/2` leaf appearances in total, and a simple bipartite cycle visits at most seven leaves. If there are `r` cycles, `7r≥3t−X/2`. Therefore

`r+s≥t+3t/7+13X/14≥t+3t/7`, giving `d(K_{7,t})≥t+ceil(3t/7)` for all `t`.

For the small exceptions, a cycle has at most `2min(7,t)` edges. At `t=1` there is no cycle. With exactly the minimum number of singletons, `t=2` leaves 12 cycle edges and requires three 4-cycles, so at least five parts; `t=3,5` leave 14 or 28 cycle edges and require at least three cycles, so at least ten parts; `t=4` leaves 24 cycle edges and requires at least three 8-cycles, so at least seven parts. These minimum singleton counts are `2,7,4,7`, respectively: every leaf has odd degree, and at odd `t` every hub does too. Extra singletons cannot lower these totals: the cycle-capacity bound `r≥ceil((7t−s)/(2min(7,t)))` increases the total `r+s`, and parity restricts `s` to the appropriate congruence class. The script supplies matching explicit partitions for `t=2,3,4,5`; `t=0` is empty.

**Finite seeds.** The script contains explicit singleton spokes and simple cycle walks for the following bases, one in every residue class modulo seven. Its edge checker proves each covers all `7t` spokes exactly once.

| seed `t` | singleton spokes | cycles | total parts `d` | construction |
| ---: | ---: | ---: | ---: | --- |
| 6 | 6 | 3 | 9 | explicit walks |
| 7 | 7 | 3 | 10 | offset block |
| 8 | 8 | 4 | 12 | explicit walks pictured below |
| 9 | 9 | 4 | 13 | explicit walks |
| 10 | 10 | 5 | 15 | explicit walks |
| 11 | 11 | 5 | 16 | explicit walks |
| 12 | 12 | 6 | 18 | two disjoint six-leaf seeds |

For `t≥6`, take the unique base `s=6+((t−6) mod 7)∈{6,…,12}` and write `t=s+7q`. Every base total equals `s+ceil(3s/7)`.

**Eight-leaf certificate.** Label hubs `0,…,6` and leaves `A,…,H`. Make the spokes `0A,0B,1C,1D,2E,2F,3G,3H` singleton parts. The four cycles below close back to their starting hub:

| cycle | alternating hub–leaf walk |
| ---: | --- |
| 1 | `1,E,3,D,4,F,5,C,6,G,2,H` |
| 2 | `0,F,3,A,2,B,4,G,5,E,6,H` |
| 3 | `0,D,6,A,5,H,4,C,3,B,1,G` |
| 4 | `0,C,2,D,5,B,6,F,1,A,4,E` |

Each walk has six distinct hubs and six distinct leaves. [`20_bipartite_seven.py`](20_bipartite_seven.py) checks all 56 spokes occur exactly once among these cycles and singleton parts. The [spoke matrix](art/bipartite_seven_eight.svg) colors each cell by its cycle or singleton role. This certificate gives `d(K_{7,8})≤12`, and the lower bound gives equality. In any optimum at `t=8`, each leaf must have exactly one singleton spoke: `X` is even, so `X≥2` would increase the lower bound by more than one part.

**Seven-leaf lift.** For each new block of seven leaves indexed by residues `i mod 7`, take `(i,i)` as a singleton spoke. Pair spoke offsets `(1,2)`, `(3,4)`, and `(5,6)` into three Hamilton cycles. For offset pair `(o,o+1)`, one explicit walk alternates hubs `0,−1,…,−6 (mod 7)` with leaves `hub+o (mod 7)`. It visits every hub and new leaf once, and the paired offsets cover all remaining block spokes. Thus every block adds `7+3=10` parts, exactly the lower-bound increase under `t→t+7`. The script checks every `t<100`; the modular walk proves coverage for every `t≥6`. The smaller cases use separate seeds.

The original eight-leaf seed, lower bound, and SVG matrix passed an independent skeptical audit. A separate edge checker verified the expanded seed table and all-residue lift; Fixpoint then independently rechecked every seed, the small exceptions, and the lift (Undervoice `#commanders` seq 16081), with no formula or coverage flaw found. This is an exact graph decomposition result, not a new asymptotic Erdős–Gallai bound; publication priority remains unverified.
