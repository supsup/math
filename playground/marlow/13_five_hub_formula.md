# Every leaf count with five clique hubs

Write `d(G)` for the fewest parts in an edge partition of `G` into simple cycles and singleton edges. For every integer `t≥0`,

> **Exact formula.** `d(K₅ ∨ Iₜ) = t + 2 + ceil(2t/5) + [t=1]`,

where `[t=1]` is one at `t=1` and zero otherwise. Thus `K₆` is the sole exception to the five-hub lower bound. This extends [the odd-hub block construction](10_odd_hub_blocks.md) from leaf counts divisible by five to every leaf count. The proof is an explicit finite set of residue gadgets plus the general lower bound. I have not established publication priority for this exact split-graph formula.

**Lower bound.** Item 10 proves, for every odd `h=2k+1` and every `t`, that `d(K_h ∨ I_t) ≥ t+k+ceil(kt/h)`. In particular, `d(K₅ ∨ Iₜ) ≥ t+2+ceil(2t/5)`. At `t=1` the graph is `K₆`. All six vertices have odd degree, so the singleton edges in any cycle-and-edge partition must cover every vertex with odd degree. This takes at least three singleton edges. If there are exactly three, twelve edges remain and require at least two simple cycles because each cycle has at most six edges. If there are at least four, a partition with only four parts would have to consist solely of four singleton edges, too few to cover `K₆`. Hence `d(K₆)≥5`, one more than the general bound of four.

**Upper bound and the six seeds.** Label the five hubs `0,…,4`; a seed with `s` leaves labels them `5,…,4+s`. The table gives `s`, the number of cycles, the number of singleton edges, and the resulting part count. All walks and singleton endpoints appear explicitly in [`13_five_hub_formula.py`](13_five_hub_formula.py), which checks simple cycles and exact edge coverage. The `s=0` gadget is the two-cycle Walecki decomposition of `K₅`.

| `s` | cycles | singleton edges | parts | purpose |
|---:|---:|---:|---:|---|
| 0 | 2 | 0 | 2 | divisible counts |
| 1 | 2 | 3 | 5 | exceptional `K₆` |
| 2 | 3 | 2 | 5 | residue 2 |
| 3 | 3 | 4 | 7 | residue 3 |
| 4 | 4 | 4 | 8 | residue 4 |
| 6 | 5 | 6 | 11 | positive residue 1 |

The `s=6` gadget explains why the one-leaf exception does **not** recur at `t=6,11,…`. Its six singleton spokes are `(0,5),(0,6),(1,7),(1,8),(2,9),(2,10)`. The remaining 24 spokes split into the three eight-cycles

`(1,5,2,7,3,8,4,6)`, `(0,8,2,6,3,9,4,10)`, and `(0,7,4,5,3,10,1,9)`.

The hub clique has the two cycles `(4,0,3,1,2)` and `(4,1,0,2,3)`. Thus six singletons and five cycles cover `K₅ ∨ I₆` in eleven parts, meeting the lower bound. In particular, its spoke gadget alone gives `d(K_{5,6})=9`: six singletons and three cycles meet the same odd-leaf/cycle-capacity lower bound with no clique edges.

For each *additional* block of five leaves, index the leaves `0,…,4` and use the five diagonal spokes `(i,i)` as singletons. The two pairs of spoke-offset classes `(1,2)` and `(3,4)` are each one ten-vertex Hamilton cycle, exactly as in item 10. The block adds seven parts and does not use a hub-clique edge. If `t=5q+r`, use the seed `r` and `q` blocks for `r=0,2,3,4`. For `r=1,q≥1`, use seed six and `q−1` blocks. The part counts are respectively `7q+2`, `7q+5`, `7q+7`, `7q+8`, and `7q+4`; these are `t+2+ceil(2t/5)` in each case. At `t=1`, use the exceptional seed. This proves the formula.

The construction is checked through `t=100`, including every residue and several added blocks, by running `python3 -I playground/marlow/13_five_hub_formula.py` from the repository root. Its [generated diagram](art/five_hub_staircase.svg) plots the first thirteen values and marks the sole exception. An independent skeptical audit checked each seed's edge coverage and the all-`t` argument. These finite checks support the explicit gadgets; the all-`t` assertion follows from the block argument. This is an exact formula for this graph family, not a stronger global extremal theorem. [Bucić and Montgomery's §6 complete-bipartite examples](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf) already exhibit the underlying odd-degree pressure.
