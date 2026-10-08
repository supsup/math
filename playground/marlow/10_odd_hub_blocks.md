# Exact odd-hub blocks at divisible leaf counts

The `K₃ ∨ I_t` formula in [item 9](09_split_graph_formula.md) prompted a broader exact subfamily. Let `h=2k+1≥3`, let `q≥0`, and put `t=hq`. For the join of an `h`-vertex clique with `t` independent leaves,

> `d(K_h ∨ I_(hq)) = hq + kq + k`, where `d` counts edge-disjoint simple cycles and singleton edges.

This is a self-contained construction and lower bound for a restricted family, not a new global extremal bound. [Bucić and Montgomery, §6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf) use the same odd-degree pressure in complete bipartite examples and recall Walecki's Hamilton decomposition of odd cliques. I have not established whether the exact joined-clique formula has appeared before.

**Lower bound.** More generally take any `t≥0`, not necessarily divisible by `h`. Each independent leaf has odd degree `h`, so an odd number of its spokes must be singleton parts. Write `X` for the total number of singleton spokes *beyond one per leaf*, and `c` for the number of singleton edges inside the hub clique. If the partition has `r` cycles and `s` singletons, then `s=t+X+c`. Every cycle uses two spokes at each leaf it visits, so the sum of leaf appearances over all cycles is `kt−X/2`. The clique has `binom(h,2)=hk` hub edges, of which `hk−c` lie in cycles.

For any simple cycle containing `l` leaves and `e` hub–hub edges, its length is `2l+e`, and it visits no more than `l+h` vertices. Thus `l+e≤h`. Summing over the cycles gives `hr≥kt−X/2+hk−c`. It follows that

`h(r+X+c) ≥ kt+hk+(h−1/2)X+(h−1)c ≥ kt+hk`, so

`r+s ≥ t+k+ceil(kt/h)`.

When `t=hq`, this is exactly `hq+kq+k`. The bound need not be attained for other `t`; for example, `K₅ ∨ I₁=K₆` needs five parts, while this inequality only yields four.

**Construction for `t=hq`.** Index the hubs by the residues `0,…,h−1` modulo `h`. In each block of `h` leaves, index its leaves by the same residues. Make the `h` diagonal spokes `(i,i)` singleton parts. For every `j=1,…,k`, use all spokes with offsets `leaf−hub ≡ 2j−1` or `2j (mod h)` as one cycle. Each hub and leaf has degree two in these two offset classes, and following the alternating edges shifts the hub index by one modulo `h`; hence the class pair is a **single Hamilton cycle** of length `2h`. The block therefore contributes `h` singletons and `k` cycles and covers all `h²` spokes.

The hub clique has a partition into `k` Hamilton cycles. For completeness, label its vertices `∞,0,…,2k−1` and, for `i=0,…,k−1`, take

`∞, i, i−1, i+1, i−2, i+2, …, i−(k−1), i+(k−1), i−k, ∞`,

with arithmetic modulo `2k`. The `∞` edges in these cycles cover each residue once. Within cycle `i`, the other edges have endpoint sums `2i−1` (all `k` pairs with that odd sum) or `2i` (all `k−1` distinct pairs with that even sum) modulo `2k`. These sum classes partition all remaining clique edges. This is the standard Walecki listing, included so the construction does not depend on a black-box existence claim. The `q` leaf blocks plus the hub-clique cycles give `hq+kq+k` parts, meeting the lower bound.

The lower-bound inequalities also constrain **every** optimum partition at these divisible counts. Any `X>0` or `c>0` makes the displayed inequality strictly larger than the attained integer bound, so every leaf has exactly one singleton spoke and no hub–hub edge is singleton. There are then exactly `kq+k` cycles. Equality in the summed cycle inequality forces `l+e=h` in each cycle, meaning each cycle visits all `h` hubs. This rigidity is a consequence of the count, not a uniqueness claim for the cycle partition.

Deleting the clique edges and their `k` Walecki cycles leaves the complete bipartite graph `K_{h,hq}`. The same parity and cycle-capacity count, now with no hub–hub edges, gives its exact value `d(K_{h,hq})=hq+kq`: the offset construction reaches that bound. Thus at these divisible counts the hub clique adds **exactly `k`** parts to the bipartite optimum. This matches the lower-bound mechanism in Bucić and Montgomery's odd-side example rather than changing its leading asymptotic ratio.

[`10_odd_hub_blocks.py`](10_odd_hub_blocks.py) checks every cycle is simple and every edge occurs exactly once for `h=3,5,…,17` and `q=0,…,4`. It generates [the `h=5,q=1` offset diagram](art/odd_hub_blocks.svg); run `python3 -I playground/marlow/10_odd_hub_blocks.py` from the repository root. An independent skeptical audit checked the lower-bound algebra, generated the offset and Walecki cycles separately, and confirmed exact coverage for `h=3,5,7,9,11,17` and `q=0,1,2`. The proof applies to every odd `h` and every `q`, beyond these finite checks. Along a sequence with both `h` and `q` growing, the part-count ratio approaches `3/2`, matching the asymptotic pressure of the known bipartite examples. This exact block construction does not establish the optimum for arbitrary leaf counts or for arbitrary graphs.
