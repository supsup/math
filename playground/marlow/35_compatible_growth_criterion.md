# A conditional bridge from square designs to all odd bases

The [prime-class construction](34_prime_two_leaf_growth.md) uses three properties of its square seed and growth cycles. They can be isolated without finite-field notation. This is a **sufficient criterion**, not an existence theorem for every odd hub count.

Let `h=2k+1≥5`, and let `H` be a set of `h` hub labels. Suppose `K_H` has a Hamilton decomposition `F_1,…,F_k` and an edge labeling `ℓ:E(K_H)→H` with the following *Kotzig* property: each `F_i` has every leaf label once, and, for each `x∈H`, the `k` edges labeled `x` are a perfect matching on `H\{x}`. Expanding a hub edge `uv` labeled `x` to the path `u–x–v`, and adding the diagonal singleton `(x,x)`, gives an optimal square partition of `K_{h,h}`. [Horton proved that Kotzig factorizations exist at every odd order](https://www.sciencedirect.com/science/article/pii/0012365X83901565); the extra compatibility below is the open part.

Choose `k−1` distinct centers `a_1,…,a_{k−1}∈H` and simple cycles `Q_a` on `H\{a}`, each of length `h−1=2k`. Require, for every chosen `a`:

1. The even-indexed and odd-indexed edges of `Q_a` each contain **one edge of every** Hamilton color `F_i`.
2. The `h−1` labels `ℓ(e)` on the edges of `Q_a` are pairwise distinct.
3. For different chosen centers `a,b`, `|E(Q_a)∩E(Q_b)|≤1`.

> **Conditional growth theorem.** Under these three conditions, `d(K_{h,t})=t+ceil(kt/h)` for every `t≥h−1`.

**Proof.** Start with the expanded square partition. At center `a`, add two fresh leaves with singleton spokes to `a`. In each full cycle `F_i`, replace the leaf occupying its one even-indexed `Q_a` edge by the first new leaf, and the leaf occupying its one odd-indexed edge by the second. Each fresh leaf therefore occupies one slot in every full cycle. Because alternating edges of an even cycle are perfect matchings, each new leaf receives its spokes to all `h−1` hubs other than `a` exactly once. The displaced old leaf paths, in `Q_a` order, form a short alternating cycle omitting `a`.

Condition 2 makes those displaced labels distinct at the first step. At a later step, any original square label still in a full-cycle slot occupies one of its original edges, so the original labels encountered along `Q_a` remain distinct. A leaf introduced at a previous center `b` occupies full-cycle slots only on edges of `Q_b`; condition 3 lets `Q_a` encounter at most one such slot. New labels from different steps are distinct, so the displaced labels remain pairwise distinct and each new short cycle is simple. Edge coverage is preserved at every replacement: the old leaf's two spokes move from its full cycle to the new short cycle, while the fresh leaf takes that full-cycle slot. Previous short cycles and singleton spokes remain untouched.

After `j` centers, `0≤j≤k−1`, the graph is `K_{h,h+2j}` with `h+2j` singleton spokes, `k` full cycles, and `j` short cycles. Its part count is `h+2j+k+j=(h+2j)+ceil(k(h+2j)/h)`, meeting the [parity/capacity lower bound](27_odd_hub_design_question.md). The [explicit even-side weave](24_even_base_residues.md) supplies all even bases in `h−1,…,2h−2`, and the [h-leaf offset block](10_odd_hub_blocks.md) lifts every base residue. This proves the conditional theorem.

For primes `h≡3 (mod 4)`, the affine midpoint labeling and translated primitive-power cycles satisfy all three conditions: the odd value of `k` gives condition 1, distinct affine midpoints give condition 2, and the classical orthogonal-double-cover intersection gives condition 3. This is the [infinite proved subfamily](34_prime_two_leaf_growth.md); [item 41](41_seventeen_affine_pages.md) gives a different compatible page family at `h=17≡1 (mod 4)`. The criterion is only sufficient; failure for a chosen square seed would not disprove the target formula. For example, the five-hub formula is known from [item 14](14_bipartite_five.md), while the standard offset seed cannot start this particular growth move. No claim of publication novelty is made for the criterion or its inputs.
