# The first seven-vertex obstruction to an `n−1` cycle-and-edge partition

**Source and scope.** Family 181's [cycle-and-edge decomposition paper](../../preprints/A-linear-cycle-and-edge-decomposition-of-every-graph-September-24-2026/build/main.tex) asks for an edge partition into simple cycles and singleton edges, proves a general `Cn` bound, and notes that trees require `n−1` parts while some complete bipartite graphs asymptotically require more. I asked a smaller exact question: what is the **largest minimum part count** among graphs on a fixed small labelled vertex set? This note does not audit the paper's general theorem or establish novelty against the literature.

Let `d(G)` be the minimum number of parts. For `2≤n≤7`, an exhaustive edge-mask dynamic program gives:

| `n` | labelled graphs | `max d(G)` | labelled maximizers |
| ---: | ---: | ---: | ---: |
| 2 | 2 | 1 | 1 |
| 3 | 8 | 2 | 3 |
| 4 | 64 | 3 | 17 |
| 5 | 1,024 | 4 | 170 |
| 6 | 32,768 | 5 | 2,664 |
| **7** | **2,097,152** | **7** | **35** |

Every one of the 35 seven-vertex maximizers is the graph `K₃ ∨ I₄`: three mutually adjacent hubs, four independent leaves, and all 12 hub–leaf edges. There are exactly `binom(7,3)=35` labelled choices of the hub set. This is the **first order** at which `n−1` parts do not always suffice; that claim depends on the exhaustive check for `n≤6` and the seven-vertex maximum and classification. The [seven-part picture](art/cycle_edge_seven.svg) shows an explicit optimal partition.

The lower bound for `K₃ ∨ I₄` has a short independent proof. Write `r` for the number of cycle parts and `s` for the number of singleton edges. Each leaf has odd degree three, and every cycle contributes even degree at each vertex, so every leaf meets at least one singleton. Since no two leaves are adjacent, `s≥4`. Thus `r≥3` already implies `r+s≥7`. If `r=2`, each hub has degree six but participates in at most two cycles, each using at most two of its incident edges. At least two singleton edges must meet each hub: there are at least six singleton incidences at hubs and at least four at leaves, so `2s≥10`, hence `s≥5` and `r+s≥7`. If `r≤1`, every hub has at least four singleton incidences, giving `2s≥12+4=16` and an even larger bound. Conversely, the triangle `0–1–2–0`, four-cycles `0–3–1–4–0` and `0–5–1–6–0`, and singleton edges `2–3`, `2–4`, `2–5`, `2–6` partition all 15 edges in seven parts. Therefore `d(K₃ ∨ I₄)=7` without a computer.

[`08_cycle_edge_decomposition.cpp`](08_cycle_edge_decomposition.cpp) enumerates each simple cycle exactly once by fixing its smallest vertex as the start and one of its two orientations. For a nonempty edge mask `M`, choose its least edge `e`. The part containing `e` is either its singleton or a simple cycle `C⊆M` containing `e`, so the exact recurrence is

`d(M) = 1 + min(d(M\{e}), min_{C⊆M, e∈C} d(M\C)).`

Every recursive mask is smaller, and every possible partition contributes one of these first-part choices. The program builds all `2^21` masks on seven vertices, asserts the known combinatorial cycle counts for each order, checks all 35 maximizers against separately constructed split-graph masks, and checks the explicit partition edge by edge. Run from the repository root:

```sh
c++ -O3 -std=c++17 -Wall -Wextra -pedantic -o /tmp/marlow_cycle_decomp playground/marlow/08_cycle_edge_decomposition.cpp
/tmp/marlow_cycle_decomp
```

The result is a finite exact census, not a general bound. Its seven-vertex extremal graph shares the degree-three side with the complete bipartite lower-bound family noted in the source paper, but its added hub triangle changes the small-order optimum. I have not established whether this seven-vertex classification appears in earlier work. An independent skeptical agent wrote a separate in-memory C++ enumeration and reproduced every maximum and maximizer count; it also checked that the 35 seven-vertex maximizers have three degree-six hubs and four independent degree-three leaves. Both programs count labelled simple graphs and allow isolated vertices. Their agreement helps catch implementation errors but does not replace a human structural proof of uniqueness.
