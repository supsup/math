# An exact split-graph cycle-and-edge formula

The [family-181 manuscript](../../preprints/A-linear-cycle-and-edge-decomposition-of-every-graph-September-24-2026/build/main.tex) studies partitions of a graph's edges into simple cycles and singleton edges. [Bucić and Montgomery, §6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf) explain how odd degrees on one side of a complete bipartite graph force many singleton parts. I extended that elementary counting idea to the graph `G_t = K₃ ∨ I_t`: three adjacent hubs joined to `t` mutually nonadjacent leaves. This is an independent derivation of an exact formula for this one family, with **prior-art status unverified**:

> **Claim.** For every integer `t≥0`, the minimum number of edge-disjoint simple cycles and singleton edges partitioning `E(G_t)` is
>
> `d(G_t) = t + ceil(t/3) + 1`.

**Lower bound.** Suppose a partition has `r` cycles and `s` singleton edges. Every leaf has degree three; cycles contribute even degree at each vertex. Consequently a leaf has either one or three singleton spokes. Let `q` be the number with three. Let `c` of the three hub–hub edges be singleton parts. Counting singleton parts gives `s=(t−q)+3q+c=t+2q+c`.

Every leaf with one singleton spoke belongs to exactly one cycle, so the total number of *leaf occurrences* among the cycles is `t−q`. The cycles also contain exactly `3−c` hub–hub edges. In one simple cycle, write `k` for its number of leaves and `h` for its number of hub–hub edges. Its length is `2k+h`, while it has at most `k+3` vertices; because a simple cycle has as many edges as vertices, `k+h≤3`. Summing over the `r` cycles gives `3r≥(t−q)+(3−c)`. Therefore

`3(r+2q+c) ≥ t+3+5q+2c ≥ t+3`, hence

`r+s = t+(r+2q+c) ≥ t+ceil((t+3)/3) = t+ceil(t/3)+1`.

**Construction.** Name the hubs `0,1,2`. For each full block of three leaves `a,b,c`, use the six-cycle `0–a–1–b–2–c–0` and singleton spokes `a–2`, `b–0`, `c–1`. These four parts cover all nine spokes in the block. Handle the remaining `t mod 3` leaves and the hub triangle as follows:

| Remaining leaves | Added cycle parts | Added singleton parts |
| --- | --- | --- |
| none | `0–1–2–0` | none |
| `d` | `0–d–1–2–0` | `d–2`, `0–1` |
| `d,e` | `0–d–1–2–0`; `0–e–1–0` | `d–2`, `e–2` |

The listed parts are edge-disjoint and cover every remaining edge. Their count meets the lower bound in each residue class, proving the formula. [`09_split_graph_formula.py`](09_split_graph_formula.py) builds these partitions and checks edge-by-edge coverage, disjointness, and part counts for `0≤t≤40`; it generates [the staircase picture](art/split_graph_staircase.svg). Run `python3 -I playground/marlow/09_split_graph_formula.py` from the repository root. An independent skeptical audit checked the proof and construction, and a separately written exact cycle-mask search confirmed `t=0,…,7` with values `1,3,4,5,7,8,9,11`.

At `t=4`, this gives the seven-part obstruction found in the [small-graph census](08_cycle_edge_decomposition.md), and the formula gives a direct proof for it. With `n=t+3`, this family's excess over `n−1` is `ceil(t/3)−1`, which first becomes positive at `t=4` and grows by one every three further leaves. Its asymptotic ratio is `4/3` parts per vertex. Bucić and Montgomery's complete bipartite examples approach `3/2`, so this family is a transparent exact model, not a stronger asymptotic lower bound. It says nothing about the general linear theorem in family 181 or the maximum over *all* larger graphs.
