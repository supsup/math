# Every leaf count with five bipartite hubs

Let `d(G)` be the minimum number of simple cycles and singleton edges partitioning `E(G)`. For the complete bipartite graph with a five-vertex side,

> `d(K_{5,t}) = 0, 5, 4, 7` for `t=0,1,2,3` respectively; for **every `t≥4`**, `d(K_{5,t}) = t+ceil(2t/5)`.

The formula is exact, not just an asymptotic lower example. The proof consists of a parity/cycle-capacity lower bound and five finite seeds, extended by the same five-leaf offset block used in [item 10](10_odd_hub_blocks.md). [Bucić and Montgomery, §6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf) use the odd-side complete bipartite family for a general cycle-and-edge lower bound; I have not established whether this exact five-side formula is already in the literature.

**General lower bound.** Let `s` spokes be singleton parts, and write `s=t+X`. Every leaf has odd degree five, so at least one of its spokes is a singleton and `X≥0`. The cycles have `2t−X/2` total leaf appearances, while a simple cycle can visit at most five distinct leaves. Thus, if there are `r` cycles, `5r≥2t−X/2`. Consequently

`r+s ≥ t+2t/5+9X/10 ≥ t+2t/5`, so `d(K_{5,t}) ≥ t+ceil(2t/5)`.

Three small graphs exceed that bound. `K_{5,1}` is a five-edge star, giving `d=5`. For `K_{5,2}`, at least two spokes are singletons. If there are exactly two, eight spokes remain and each simple cycle uses at most four, requiring two cycles; with more singletons there are at least four of them because each leaf has an odd number. Hence `d≥4`. For `K_{5,3}`, all five hubs have odd degree, so each must be incident with a singleton spoke: `s≥5`. Each of the three leaves has an odd number of singleton spokes, so `s` is odd. If `s=5`, ten spokes remain and a cycle uses at most six, requiring two cycles. If `s≥7`, seven parts are already present. Hence `d≥7`. The zero-leaf graph is empty.

**Seed partitions and block extension.** [`14_bipartite_five.py`](14_bipartite_five.py) lists every cycle walk and singleton endpoint for the small exceptions and for seeds with 4, 6, 7, and 8 leaves. The table summarizes the partitions; the script checks that each cycle is simple and every spoke appears exactly once.

| leaves in seed | cycles | singleton spokes | parts | role |
|---:|---:|---:|---:|---|
| 0 | 0 | 0 | 0 | divisible counts |
| 1 | 0 | 5 | 5 | small exception |
| 2 | 2 | 2 | 4 | small exception |
| 3 | 2 | 5 | 7 | small exception |
| 4 | 2 | 4 | 6 | residue 4 |
| 6 | 3 | 6 | 9 | residue 1 after one block |
| 7 | 3 | 7 | 10 | residue 2 after one block |
| 8 | 4 | 8 | 12 | residue 3 after one block |

The seven-leaf seed uses one eight-cycle and two ten-cycles; its singleton incidence is `(3,1,1,1,1)` across the hubs. The eight-leaf seed uses four eight-cycles; its singleton incidence is `(2,2,2,2,0)`. These incidence patterns make the parity constraints explicit, but exact coverage comes from the listed walks. The six-leaf seed is the three-eight-cycle gadget already used in [item 13](13_five_hub_formula.md).

Each extra block of five leaves has five diagonal singleton spokes and two ten-cycles made of spoke-offset pairs `(1,2)` and `(3,4)`. It adds seven parts, precisely the increase in `t+ceil(2t/5)` when `t` increases by five. For `t=5q+r≥4`, use `q` blocks with seed 0 when `r=0`, `q` blocks with seed 4 when `r=4`, and `q−1` blocks with seed `5+r` when `r=1,2,3`. Every residue is covered, proving the formula for all `t≥4`.

There is a useful comparison with the joined graph of item 13. Adding the ten edges of the hub clique increases the optimal part count by exactly **two** for `t=0` and every `t≥4`. At `t=1,2,3`, the increases are `0,1,0` respectively; optimal partitions reorganize the hub edges among the cycle parts. [The generated diagram](art/bipartite_five.svg) displays this small-count anomaly. Run `python3 -I playground/marlow/14_bipartite_five.py` from the repository root to check every seed and the block construction through `t=100` and regenerate the diagram. An independent skeptical audit parsed all seeds separately, recomputed exact optima through `t=4`, and checked the lower bound and residue lift. The finite checks support the explicit gadgets; the all-`t` statement follows from the block argument. Publication priority is unverified.
