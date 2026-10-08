# Sotteau's theorem supplies every even base residue

Write `h=2k+1≥3`, and let `d(G)` be the minimum number of simple cycles and singleton edges partitioning `E(G)`. For any **even** `b` in the interval `h−1≤b≤2h−2` and any `q≥0`,

> **`d(K_{h,b+hq})=b+b/2+(h+k)q=(b+hq)+ceil(k(b+hq)/h)`.**

This is a corollary of a known cycle-design theorem, not a claim of a new decomposition theorem. [Sotteau's 1981 paper](https://www.sciencedirect.com/science/article/pii/0095895681900939) gives necessary and sufficient conditions for a complete bipartite graph to decompose into cycles of one fixed even length. For `c≥2`, the conditions are stated explicitly in [Mahmoodian–Mirzakhani, introduction](https://mathsmartinthomas.wordpress.com/wp-content/uploads/2018/08/mahmoodian-mirzakhani1995_chapter_decompositionofcompletetripart.pdf): `K_{m,n}` has a `C_{2c}`-decomposition iff `m,n` are even, both at least `c`, and `2c` divides `mn`. Publication priority for this particular cycle-and-singleton corollary has not been checked.

**Lower bound.** The odd degree `h` at each leaf forces at least one singleton spoke per leaf. If there are `s=t+X` singletons, the cycles have `kt−X/2` leaf appearances, at most `h` per simple cycle. Thus `d(K_{h,t})≥t+ceil(kt/h)`, as in [item 22](22_one_leaf_short.md). For `t=b=2r` in the stated interval, `r≤h−1`, so

`kb/h = r−r/h ∈ (r−1,r)`, hence `ceil(kb/h)=r=b/2`.

**Even seed.** Make all `b` spokes incident with one hub singleton parts. The residual graph is `K_{2k,b}`. Apply Sotteau with `m=2k`, `n=b`, and desired cycle length `2c=4k` (`c=2k`). Both sides are even and at least `2k`; moreover `4k` divides `2kb` because `b` is even. The residual graph therefore splits into exactly `(2kb)/(4k)=b/2` simple `4k`-cycles. This gives `b+b/2` parts, matching the lower bound.

**Odd-hub lift.** Append `q` disjoint `h`-leaf blocks from [item 10](10_odd_hub_blocks.md). Each has `h` diagonal singleton spokes and `k` Hamilton cycles made from adjacent offset matchings, so it adds `h+k` parts. The lower bound grows by precisely `h+k` under `t→t+h`; hence equality persists for every `b+hq`.

There are `k+1` even bases `b=2k,2k+2,…,4k`, each a different residue modulo the odd number `h`. The divisible base `b=h` supplies one more residue via item 10. Therefore, for a proposed all-residue formula at a fixed odd `h`, only the `k−1` odd bases `h+2,h+4,…,2h−3` still need separate seeds. For `h=9`, those are `11,13,15`; [item 23](23_nine_hub_all_residues.md) supplies them explicitly. For `h=11`, the remaining odd bases are `13,15,17,19`; this note makes no assertion about them.
