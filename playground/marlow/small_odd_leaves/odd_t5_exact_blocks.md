# Exact five-leaf cycle partitions

Let `d(K_(p,5))` be the minimum number of parts in an edge partition into
single edges and simple cycles. For every odd `p>=5`, parity forces at least
one singleton incident to each of the `p` hubs. A cycle has at most ten edges,
so the bound in [the small-leaf note](p12289_small_leaf_exact.md) specializes to

```text
d(K_(p,5)) >= p + ceil(2p/5).
```

The bound is attained at **every odd `p>=5`**. In particular,

```text
d(K_(12289,5)) = 12289 + ceil(24578/5) = 17205.
```

All blocks below use the same five leaves `0,...,4`; their hub sets are
disjoint. In a cycle row `(L;H)`, with equally long lists `L=(l_0,...,l_(r-1))`
and `H=(h_0,...,h_(r-1))`, the successive vertices are
`l_0,h_0,l_1,h_1,...,l_(r-1),h_(r-1),l_0`. Thus its edges are
`(h_i,l_i)` and `(h_i,l_(i+1 mod r))`. The displayed hub and leaf entries
are each distinct, so every row is a simple cycle.

**Four hubs.** Index hubs by `0,...,3`; make `(j,4)` singleton for each `j`.
The remaining `K_(4,4)` on leaves `0,...,3` splits into two 8-cycles:

| length | leaves `L` | hubs `H` |
|---:|---|---|
| 8 | `0,1,2,3` | `0,1,2,3` |
| 8 | `2,3,0,1` | `0,1,2,3` |

At hub `j`, the first row uses leaves `j,j+1 mod 4` and the second uses
`j+2,j+3 mod 4`. Thus the two cycles cover all four nonsingleton edges at
every hub exactly once. This block costs four singletons plus two cycles.

**Five hubs.** Index hubs by `0,...,4`; make `(i,i)` singleton for each `i`.
For `k=1,2`, put `h_j=-2kj mod 5` and `l_j=h_j+k mod 5` for `j=0,...,4`.
The row `(L;H)` is one 10-cycle. Its edges at hub `h` go to leaves `h+k`
and `h-k` modulo five. The two cycles therefore cover every off-diagonal
edge exactly once. This block costs five singletons plus two cycles.

**Seven hubs.** Index hubs by `0,...,6`; make `(i,m_i)` singleton, where
`(m_0,...,m_6)=(0,1,2,3,4,0,0)`. The remaining 28 edges are these cycles:

| length | leaves `L` | hubs `H` |
|---:|---|---|
| 10 | `0,1,3,2,4` | `4,2,6,3,1` |
| 10 | `1,0,4,2,3` | `3,2,0,1,5` |
| 8 | `1,3,2,4` | `0,4,5,6` |

The three rows are edge-disjoint and avoid every singleton; their 28 edges
exhaust the residual graph. This block costs seven singletons plus three
cycles.

**Nine hubs.** Index hubs by `0,...,8`; make `(i,m_i)` singleton, where
`(m_0,...,m_8)=(0,1,2,3,4,3,3,4,4)`. The remaining 36 edges are:

| length | leaves `L` | hubs `H` |
|---:|---|---|
| 10 | `2,1,4,3,0` | `3,6,0,4,1` |
| 10 | `4,0,2,1,3` | `3,8,4,7,1` |
| 8 | `0,4,1,2` | `5,2,0,6` |
| 8 | `0,3,1,2` | `2,8,5,7` |

These four rows are edge-disjoint, avoid the nine singleton edges, and have
36 edges in total, exactly the residual count. This block costs nine
singletons plus four cycles. The explicit checker
[`odd_t5_edge_check.py`](odd_t5_edge_check.py) independently checks every
edge and the simplicity of every cycle, including the full `p=12289`
partition.

The four-hub block fills the two remaining small cases: `7+4=11` hubs cost
`3+2=5=ceil(22/5)` cycles, and `9+4=13` hubs cost
`4+2=6=ceil(26/5)` cycles. Hence `d(K_(11,5))=16` and
`d(K_(13,5))=19`. The separate
[extension note](odd_t5_exception_extension.md) and its
[no-import checker](odd_t5_exception_extension_check.py) give an additional
certificate. The updated [skeptical audit](odd_t5_skeptical_audit.md)
independently replays the four-hub block and both assemblies.

For `p=12289`, use one nine-hub block and 2456 five-hub blocks:
`9+2456*5=12289`, and `4+2456*2=4916=ceil(2*12289/5)` cycles. The singleton
count is 12289, giving 17205 parts and meeting the lower bound.

For the broader claim, write an odd `p>=15`, except `p=23`, as `p=5a+7b`
with `a>=0` and `0<=b<=4`: choose the unique `b` for which `p-7b` is
divisible by five. Directly checking `p=15,17,19,21,25,27,29,31,33` and
then adding ten shows `a>=0` throughout this range. The resulting cycle
count is `2a+3b=(2p+b)/5=ceil(2p/5)`; the last equality follows by checking
`b=0,1,2,3,4` modulo five. For `p=23`, use a nine-hub block and two
seven-hub blocks, costing `4+3+3=10=ceil(46/5)` cycles. Combined with the
four-hub extension above, this proves the claim for every odd `p>=5`.
