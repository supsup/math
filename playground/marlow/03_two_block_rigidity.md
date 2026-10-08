# A two-block classification at the cycle–triangle Ramsey boundary

**Status:** proposed deduction for Fixpoint's independent review; it uses a published pancyclicity theorem. I have not established whether the resulting classification is already known. This is a structural supplement to family 189, not a verification of that manuscript's general `n` claim.

Let `m≥4`, and color the edges of `K_{2m−2}` red/blue with no red (not necessarily induced) `C_m` and no blue triangle. Then the red graph is exactly two cliques `K_{m−1}` with zero or one red edge between them. Consequently there are two isomorphism types and exactly

`(1/2) binom(2m−2,m−1) [1+(m−1)^2]`

labelled safe colorings. At `m=4,5,6`, this gives `100, 595, 3276`, respectively, matching independent exhaustive enumerations. The case `m=4` has the elementary proof in [item 1](README.md); here is the deduction for `m≥5`.

Write `G` for the red graph, so `α(G)≤2`. Such a graph is a `[4,2]`-graph in the terminology of [Xingzhi Zhan, *A Sufficient Condition for Pancyclic Graphs*, Bulletin of the Australian Mathematical Society 112 (2025), 220–226](https://doi.org/10.1017/S0004972724001102): every induced four-vertex subgraph has at least two edges, since one with zero or one edge would contain three independent vertices. Zhan proves that every 2-connected `[4,2]`-graph of order at least seven is pancyclic. Here `|G|=2m−2≥8`, so `G` cannot be 2-connected: it would contain a cycle of length `m`.

If `G` is disconnected, it has at most two components, since one vertex from each of three would be independent. It has exactly two, and both are cliques: a nonadjacent pair in one component together with any vertex in the other would be independent. Each component has at most `m−1` vertices, or it would contain `C_m`; their sizes sum to `2m−2`, hence both have exactly `m−1` vertices.

Otherwise `G` is connected but has a cutvertex `v`. The graph `G−v` has exactly two components `A,B` by the same independence argument, and each is a clique. The vertex `v` must be adjacent to every vertex of at least one component, say `A`, or a nonneighbor in each component would join `v` to an independent triple. Thus `A∪{v}` is a clique, so `|A|≤m−2`; `B` is a clique, so `|B|≤m−1`. As `|A|+|B|=2m−3`, both inequalities are equalities. Since `G` is connected, `v` has a red neighbor in `B`. It has at most one: two such neighbors, together with all `m−1` vertices of the clique `B`, make a red `C_m`. Therefore `A∪{v}` and `B` are two red `K_{m−1}`s with exactly one bridge.

Conversely, both constructions are safe. Blue edges only run between the two cliques, so they contain no blue triangle; and a red cycle using both cliques would need at least two red bridges, while a single clique is too small to contain `C_m`. These two cliques are the unique red `K_{m−1}`s, so the partition count does not double count. Choose the unordered partition in `binom(2m−2,m−1)/2` ways and either no bridge or one of `(m−1)^2` bridges.

The same proof also gives the upper bound `R(C_m,K_3)≤2m−1` for `m≥5`: on `2m−1` vertices, a disconnected graph or a graph with a cutvertex would have at most `(m−1)+(m−1)=2m−2` vertices under the bounds above, while a 2-connected graph would be pancyclic. The two-block construction supplies the matching lower bound. The `m=4` value follows from item 1.

**Scope and checks.** The non-elementary input is exactly Zhan's theorem, as stated in the publisher's abstract; I have not independently proved or formalized it. I checked the `[4,2]` implication and every cutvertex count above directly. Scripts [01](01_cycle_clique.py) and [02](02_cycle5_boundary.py) exhaustively verify `m=4,5`; a separate blue-adjacency/path-extension enumeration independently checked `m=6`: safe counts on orders 1 through 11 were `1, 2, 7, 41, 388, 811, 2331, 5411, 9261, 3276, 0`, with `126` no-bridge and `3150` one-bridge colorings at order 10. That computation is corroboration, not the general proof.

**Potential value and red flags.** The formula classifies all critical colorings in the `n=3` slice, beyond the Ramsey number alone. A structural form might help stability arguments and pruning algorithms for graph searches; an algorithmic speedup remains unmeasured. Prior art needs checking: the cycle–triangle Ramsey *number* is old, and the two-block rigidity may already be known. The argument depends on the precise pancyclicity theorem and does not extend automatically to `n>3` or to fewer than `2m−2` vertices.
