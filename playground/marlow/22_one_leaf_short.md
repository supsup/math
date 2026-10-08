# One leaf short of an odd-hub square block

Let `d(G)` count the fewest simple cycles and singleton edges partitioning `E(G)`. The divisible-leaf construction in [item 10](10_odd_hub_blocks.md) has a companion exact residue for **every** odd hub count. Write `h=2k+1≥3` and `t=(h−1)+hq` with `q≥0`. Then

> `d(K_{h,t})=t+ceil(kt/h)=3k+(h+k)q`.

The result is an exact subfamily of the Erdős–Gallai bipartite examples discussed by [Bucić–Montgomery, §6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf). It is an elementary construction, and I have not established publication priority. It does not assert an all-residue formula for arbitrary odd `h`.

**Lower bound.** Every leaf has odd degree `h`, so at least one incident spoke is a singleton. If there are `s=t+X` singleton spokes, then the cycles use `kt−X/2` leaf appearances. A simple cycle visits at most `h` leaves, so with `r` cycles, `hr≥kt−X/2`. Hence

`r+s ≥ t+kt/h+(1−1/(2h))X ≥ t+kt/h`, and thus `d(K_{h,t})≥t+ceil(kt/h)`.

**Seed at `t=h−1=2k`.** Name the hubs `0,…,2k` and leaves `0,…,2k−1`. Make all `2k` spokes incident with hub `2k` singleton parts. The remaining graph is `K_{2k,2k}`. Its spokes split into `2k` offset matchings `leaf−hub≡j (mod 2k)`. Pair offsets `(0,1),(2,3),…,(2k−2,2k−1)`. Each pair is one Hamilton cycle: traversing it advances the hub index by one modulo `2k`, so it visits every remaining hub and leaf exactly once. There are `k` cycles and `2k` singletons, giving `3k` parts, exactly the lower bound. The [nine-hub spoke matrix](art/one_leaf_short.svg) shows the `h=9,t=8` case: one singleton row and four colored Hamilton cycles.

**Lift.** For each new block of `h` leaves, use the odd-hub block from item 10: `h` diagonal singleton spokes, and `k` Hamilton cycles from adjacent offset pairs `(1,2),…,(2k−1,2k)`. The block is edge-disjoint from earlier leaf blocks and adds `h+k` parts. Algebraically, `ceil(k(t+h)/h)=ceil(kt/h)+k`, so each lift continues to attain the lower bound. The script [`22_one_leaf_short.py`](22_one_leaf_short.py) checks simple cycles and exact spoke coverage for odd `h=3,…,21` and `q=0,…,7`; the modular argument proves all odd `h` and all `q`.

For `h=5` this recovers the residue `t=4 mod 5` from [item 14](14_bipartite_five.md), and for `h=7` the residue `t=6 mod 7` from [item 20](20_bipartite_seven.md). The new point here is the uniform seed and proof for all odd hub counts, with no finite search needed for this residue. An independent skeptical audit rederived the bound and modular walks, checked additional `h≤29,q≤19` certificates, and matched every role in the nine-hub SVG; it found no material flaw.

At the smallest odd hub count, `h=3`, one more four-leaf seed completes the other residue: take singleton spokes `(0,0),(0,1),(1,2),(1,3)` and the 4-cycles `(1,0,2,1)` and `(0,2,2,3)`, where each tuple alternates hub, leaf, hub, leaf before closing. Together with the `t=2` seed above and the `t=3` offset block, the three-leaf lift proves `d(K_{3,t})=t+ceil(t/3)` for every `t≥2`; `t=1` is a three-edge star and needs three singleton parts.
