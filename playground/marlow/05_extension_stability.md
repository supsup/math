# The next collision level above a cycle–triangle critical coloring

**Scope.** Fix either critical coloring in [Radziszowski and Jin (1994), Theorem 3](https://www.cs.rit.edu/~spr/PUBL/paper30.pdf): two red `K_{m−1}`s with zero or one red bridge, all remaining cross-edges blue. Attach one new vertex with arbitrary edge colors. Count red `C_m` copies by undirected edge set and blue `K_3` copies by vertex triple. This is a conditional count over attachments to a *fixed critical base*, not a statement about all colorings of `K_{2m−1}`.

**Finding.** Put `H=(m−2)²`. For every `m≥7`, the smallest forbidden-copy total is `H` for both base types, as in [item 04](04_extension_collisions.md). The **second distinct smallest** total is:

| Base type | Second total | Gap above `H` | Labelled attachments attaining it |
| --- | ---: | ---: | ---: |
| No red bridge | `H+(m−2)` | `m−2` | `2(m−1)` |
| One red bridge | `H+(m−3)` | `m−3` | `2(m−2)` |

The `m=6` no-bridge case is a genuine exception: its second level is `18=16+2`, attained by `100` attachments. The one-bridge second level is `19=16+3`, attained by `8`. The [chart](art/extension_stability.svg) displays the gaps for `m=6,…,10`. I have not established whether these conditional second-level formulas occur in prior work; the critical-base classification is published.

## Proof for `m≥7`

Write `k=m−1≥6`, `q=(k−2)!`, and let `a,b` be the new vertex's red-neighbor counts in the two blocks. With no red bridge, [item 04](04_extension_collisions.md) gives

`F(a,b)=q[binom(a,2)+binom(b,2)]+(k−a)(k−b)`.

Its unique minimum is `H=(k−1)²` at `(a,b)=(1,1)`. If `a=0`, then `F(0,b)` is minimized at `b=1` because `F(0,b+1)−F(0,b)=qb−k`: the first step lowers it and every later step raises it. The value is `k(k−1)=H+(k−1)`. The same holds with the blocks exchanged. If `a,b≥1` but not both `1`, increasing a positive count above `1` costs at least `q−(k−1)>k−1` for `k≥6`. Thus the second level is `H+k−1`, and exactly the `(0,1)` and `(1,0)` attachments attain it. Choosing the lone red neighbor gives `2k` labelled attachments.

Now add one red bridge `x–y`. Its extension count has the form `G=F−I+X`, where `I=1` exactly when both new edges to `x,y` are blue (the bridge removes one blue triangle), and `X≥0` counts new red cycles using the bridge. When `(a,b)≠(1,1)`, the preceding gap gives `G≥H+k−2`. Equality requires `F=H+k−1`, `I=1`, and `X=0`; hence `(a,b)` is `(0,1)` or `(1,0)`, with its lone red neighbor **away** from the bridge endpoint. Those choices indeed have `X=0` because one block has no new red neighbor, and there are `2(k−1)` of them.

For `(a,b)=(1,1)`, item 04 shows the unique minimum `H` occurs when the two new red edges meet `x,y`. Every other attachment at these counts lies above `H+k−2`: if exactly one red neighbor is off its bridge endpoint, the bridge supplies at least `q` red cross-cycles and deletes no blue triangle; if both are off, it supplies at least `q` cross-cycles and deletes one blue triangle. For the latter bound, count the cycles with two old vertices in the first block and `k−2` in the second, then reverse the roles of the blocks; each group has `q/2` cycles and the groups are disjoint because `k≥6`. Since `q−1>k−2`, none competes with the displayed second level. This proves both formulas and attainer counts.

## Exact census and limits

Run `python3 -I playground/marlow/05_extension_stability.py` from the repo root. It evaluates every neighbor-count/bridge-endpoint pattern with its binomial multiplicity, so the weights sum to all `2^(2m−2)` labelled attachments for each fixed base. Within-block red cycles and blue triangles use the `F` formula. For the bridge-crossing red cycles, the new vertex and bridge split the cycle into paths of `p` and `k−p` old vertices, for `1≤p≤k−1`. If `α,β∈{0,1}` say whether the new red edges meet the bridge endpoints, the number of first-block paths is `α` for `p=1` and `(a−α) P(k−2,p−2)` otherwise; the second-block factor is analogous. The script sums their products. This independently checkable formula reproduces the direct edge-mask enumerator's full attachment totals for `m=4,5,6` in a separate comparison, not just the minima. It asserts the stated second levels and counts through `m=11` and regenerates the SVG. A skeptical independent graph-DFS audit reproduced both second levels and attainer counts at `m=7`, and the no-bridge values at `m=8`; separate count-pattern checks agreed at `m=8,9`. That audit also checked the proof's equality cases.

The proof concerns the immediate next level among extensions of critical witnesses. It neither determines the unrestricted Ramsey multiplicity nor describes near-minimal arbitrary colorings of `K_{2m−1}`. A possible use is to give a finite constraint solver a certified gap when it searches near a critical witness; no solver benefit has been measured.
