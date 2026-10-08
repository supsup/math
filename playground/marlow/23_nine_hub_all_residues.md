# Every large leaf count with nine bipartite hubs

Let `d(G)` be the minimum number of simple cycles and singleton edges partitioning `E(G)`. A nine-hub complete bipartite graph has an exact formula throughout the range `t≥8`:

> **`d(K_{9,t})=t+ceil(4t/9)` for every `t≥8`.**

The cases `t<8` are not part of this statement. This is another fixed-hub exact subfamily of the Erdős–Gallai bipartite examples discussed by [Bucić–Montgomery, §6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf). That source gives a similar odd-degree and cycle-length lower bound, not these explicit nine-hub residues. Publication priority for this formula is unverified.

**Lower bound.** Each of the `t` leaves has odd degree nine, so at least one incident spoke must be a singleton. Write the number of singleton spokes as `s=t+X`, `X≥0`. The cycles then use `4t−X/2` leaf appearances, while each simple cycle visits at most nine leaves. If there are `r` cycles, `9r≥4t−X/2`; hence

`r+s≥t+4t/9+17X/18≥t+4t/9`, proving `d(K_{9,t})≥t+ceil(4t/9)`.

Because each leaf has an odd number of singleton spokes, `X` is even. If `X≥2`, the displayed lower bound rises by at least `17/9>1`, while rounding `4t/9` costs less than one part. Therefore **every** partition attaining the formula has exactly one singleton spoke at each leaf.

**One finite seed per residue.** The `t=8` seed is the uniform one-leaf-short construction of [item 22](22_one_leaf_short.md): eight singleton spokes from one hub, then four 16-edge Hamilton cycles on `K_{8,8}`. The `t=9` seed is the [item-10](10_odd_hub_blocks.md) offset block: nine diagonal singletons and four 18-edge Hamilton cycles. For `t=10,…,16`, [`23_nine_hub_seeds.json`](23_nine_hub_seeds.json) records each singleton and alternating hub/leaf cycle walk. The checker [`23_nine_hub_all_residues.py`](23_nine_hub_all_residues.py) verifies that all walks are simple, every spoke occurs exactly once, and the count meets the lower bound.

| seed leaves `t` | singleton spokes | cycle lengths | parts |
| ---: | ---: | --- | ---: |
| 8 | 8 | four 16-edge cycles | 12 |
| 9 | 9 | four 18-edge cycles | 13 |
| 10 | 10 | five 16-edge cycles | 15 |
| 11 | 11 | four 18-edge, one 16-edge | 16 |
| 12 | 12 | six 16-edge cycles | 18 |
| 13 | 13 | four 18-edge, two 16-edge | 19 |
| 14 | 14 | seven 16-edge cycles | 21 |
| 15 | 15 | four 18-edge, three 16-edge | 22 |
| 16 | 16 | eight 16-edge cycles | 24 |

The [nine-by-eleven spoke matrix](art/nine_hub_eleven.svg) pictures the `t=11` seed. Four cycles visit all nine hubs; the fifth visits eight. Its 11 singletons and five cycles meet the lower bound `11+ceil(44/9)=16`. This cycle-length pattern is forced in any optimum at `t=11`: five cycles have capacity for 45 leaf visits, but exactly 44 are needed, so exactly one cycle misses one hub.

**All-residue lift.** For any `t≥8`, take `b=8+((t−8) mod 9)∈{8,…,16}` and write `t=b+9q`. Append `q` disjoint nine-leaf blocks. In each block take the nine diagonal spokes as singleton parts and pair the remaining offset matchings `(1,2),(3,4),(5,6),(7,8)` into four Hamilton cycles. Consecutive offsets differ by one, so an alternating walk advances its hub index by one modulo nine and visits every hub and leaf. Each block adds `9+4=13` parts, exactly the lower-bound increase under `t→t+9`. This proves the formula for every `t≥8`; finite checking through `t=200` is an additional implementation check.

An OR-Tools CP-SAT search found the finite `t=10,…,16` witnesses by solving degree constraints and adding connectivity cuts. The saved JSON and the modular lift make the final proof independent of the solver or its search path. Fixpoint's later independent review checked all nine seeds, the lift through `t=200`, 44 planted errors, and byte-for-byte regeneration of the figure (Undervoice `#commanders` seq 16105). No claim is made about a new general Erdős–Gallai bound.
