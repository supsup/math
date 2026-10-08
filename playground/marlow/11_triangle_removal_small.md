# Exact terminal laws for the first random triangle removals

**Source and scope.** Family 188's [triangle-removal manuscript](../../preprints/The-Sharp-Terminal-Leave-in-Random-Triangle-Removal-September-25-2026/build/introduction.tex) begins with `K_n`, repeatedly chooses uniformly among the triangles **currently present**, deletes their three edges, and studies the terminal edge count `F_n`. Its claimed large-`n` result is an `L²` limit for `F_n/n^(3/2)` with constant `1/(2√2)`. I computed the finite terminal laws through `n=7`; this does not test that asymptotic proof.

| Start | Terminal leave | Exact probability | Reachable labelled terminal graphs |
| --- | --- | ---: | ---: |
| `K₃` | empty | `1` | 1 |
| `K₄` | three-edge star | `1` | 4 |
| `K₅` | four-cycle plus isolated vertex | `1` | 15 |
| `K₆` | perfect matching | `9/10` | 15 |
| `K₆` | `K_{3,3}` | `1/10` | 10 |
| `K₇` | empty | **`1125/4004`** | 1 |
| `K₇` | six-cycle plus isolated vertex | **`2879/4004`** | 420 |

The [probability diagram](art/triangle_removal_small.svg) compares the two nondeterministic cases. An empty leave from `K₇` means seven accepted, edge-disjoint triangles cover all 21 edges: a Steiner triple system on seven vertices. The six-edge alternative uses five accepted triangles. `K₆` is simpler to see directly: after the first triangle is deleted, exactly ten triangles remain. Choosing the disjoint triangle next, with probability `1/10`, leaves `K_{3,3}` and stops. Each of the other nine choices leads to a perfect-matching leave.

For a current edge mask `M`, let `T(M)` be its present triangles and let `μ_M` be the terminal edge-count distribution. The exact recurrence is `μ_M = δ_|M|` if `T(M)=∅`; otherwise `μ_M = (1/|T(M)|) Σ_{C∈T(M)} μ_(M\C)`. Each call removes three edges, so the recursion terminates. [`11_triangle_removal_small.py`](11_triangle_removal_small.py) evaluates it with rational arithmetic over reachable labelled masks only: 2, 5, 26, 256, and **4,972 states** for `n=3,…,7`. It also checks every terminal graph's degree sequence and the labelled terminal-mask counts. Run `python3 -I playground/marlow/11_triangle_removal_small.py` from the repository root; it regenerates the diagram.

There is a second, weighted-history calculation for the `K₇` empty leave. [`11_triangle_removal_histories.py`](11_triangle_removal_histories.py) recursively chooses a triangle covering the least uncovered edge to enumerate all **30 labelled seven-triangle exact covers** of `K₇`. Each cover has `7!` possible removal orders, so there are 151,200 complete histories, with no duplication. A history's probability is the product of the reciprocals of the numbers of available triangles along it. The histories fall into only three count sequences:

| Available-triangle counts before the seven removals | Histories | Geometry in the seven-triangle cover |
| --- | ---: | --- |
| `35,22,13,7,4,2,1` | 90,720 | Neither end triple concurrent |
| `35,22,13,8,4,2,1` | 30,240 | First three triangles meet at one vertex |
| `35,22,13,7,3,2,1` | 30,240 | Last three triangles meet at one vertex |

On any fixed seven-triangle cover, exactly seven of its `binom(7,3)=35` three-line subsets are concurrent. First-three and last-three concurrency cannot both occur because the two triples of distinct lines would have to share a line. Thus the two exceptional patterns each occur in `1/5` of orders and the generic pattern in `3/5`. Directly counting triangles remaining after each prefix gives the three sequences above. Summing `histories / product(sequence)` gives `1125/4004` again. This method checks the probability without relying on the full reachable-state distribution; its exact-cover enumeration and geometric classes were independently audited. Run `python3 -I playground/marlow/11_triangle_removal_histories.py` from the repository root.

Deleting a triangle changes each involved vertex degree by two, so vertex-degree parity survives. Every terminal graph is triangle-free. Those facts identify the listed shapes from the computed edge counts: at `n=7`, a nonempty six-edge terminal graph has one isolated vertex and six degree-two vertices, which must form one six-cycle because triangles are absent. There are `7·(6−1)!/2=420` labelled such leaves. At `n=6`, three edges with all degrees odd form a perfect matching; nine edges in a triangle-free graph on six vertices attain Mantel's bound and form `K_{3,3}`.

An independent skeptical agent wrote a separate exact recursion and reproduced the `K₇` fraction, 4,972 reachable states, and all 421 terminal labelled graphs. The finite probabilities are an illustration of the process, not evidence for the manuscript's `n→∞` constant: for instance, `E[F₇]/7^(3/2)` is about `0.233`, while the asserted limit is about `0.354`. I make no novelty claim for these small-order laws.
