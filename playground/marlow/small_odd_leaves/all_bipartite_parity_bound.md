# Exact singleton-and-cycle partition count for every complete bipartite graph

For positive integers `p,t`, let `d(K_(p,t))` be the minimum number
of parts in an edge partition into singleton edges and simple cycles.
Put

```text
m  = min(p,t),
s0 = max(p if t is odd else 0,  t if p is odd else 0).
```

Then

```text
d(K_(p,t)) = s0 + ceil((p*t-s0)/(2*m)).
```

This follows from the [uniform odd-small-leaf construction](odd_all_leaves_uniform.md)
and its [odd-hub large-leaf corollary](odd_hubs_large_leaves_uniform.md),
together with one explicit even-even weave. The formula includes
`p=1` or `t=1`, where the graph is a star and all edges are
singletons.

## Lower bound

If `t` is odd, each of the `p` vertices in the first side has odd
degree and needs at least one singleton edge. If `p` is odd, the
same applies to each of the `t` vertices in the second side. A
singleton edge can meet one vertex in each side, so the two
requirements give their maximum `s0`. If a partition has `s`
singletons and `c` cycles, no simple cycle has
more than `2m` edges, so

```text
c >= ceil((p*t-s)/(2*m)).
```

For integer `s`, the function
`s+ceil((p*t-s)/(2*m))` is nondecreasing: adding one singleton can
lower the ceiling by at most one. Its value at `s0` is therefore a
lower bound for the part count.

## Both sides even

Set `q=max(p,t)` and `m=min(p,t)`. Both are even. Orient the larger
side temporarily as hubs labeled by `Z/q`, and the smaller side as
leaves `0,...,m-1`. For each `j=0,...,q/2-1`, the alternating cycle
with hub and leaf sequences

```text
H_(j,k)=2j+k mod q,       L_k=k,       k=0,...,m-1
```

is simple because `m<=q`. At leaf `k<m-1`, the two incident hubs
in cycle `j` are `2j+k` and `2j+k+1`; at the last leaf they are
`2j+m-1` and `2j`. Since `m` is even, these two neighbors range
over the opposite parity classes of `Z/q` as `j` varies. Thus the
`q/2` cycles partition every edge. Here `s0=0` and the lower bound
is `ceil(q*m/(2*m))=q/2`.

## Both sides odd

For `m>=3`, orient the larger side `q=max(p,t)` as hubs. The
[uniform odd-small-leaf theorem](odd_all_leaves_uniform.md)
constructs a partition with `q` singleton edges and
`ceil(q*(m-1)/(2*m))` cycles. Here `s0=q`, so this meets the
displayed lower bound. The `m=1` case is a star.

## One side odd, one side even

Call the odd side size `o` and the even side size `e`; orient the
odd side as hubs. For `o=1` the graph is a star. Assume `o>=3`.

If `e<=o-1`, apply the even-even weave above to
`K_(o-1,e)`, using its `o-1` vertices as hubs. Add one more hub
and make all its `e` edges singleton. There are `e` singletons and
`(o-1)/2` cycles. Since now `m=e` and `s0=e`, the lower bound has
cycle term

```text
ceil((o*e-e)/(2*e)) = (o-1)/2.
```

If `e>=o-1`, the [odd-hub large-leaf construction](odd_hubs_large_leaves_uniform.md)
gives `e` singleton edges and `ceil(e*(o-1)/(2o))` cycles. At
`e=o-1` this agrees with the preceding weave. For `e>o-1`, the
smaller side of `K_(o,e)` is `o`, so this cycle count is exactly
`ceil((o*e-e)/(2o))`, the lower-bound term. Transpose the
construction if the odd side was originally the second side.

These parity cases exhaust all positive `p,t`.

## Bounded replay

The [all-parity full-edge checker](all_bipartite_parity_bound_check.py)
passes every pair `1<=p,t<=41` (1,681 partitions). It constructs
the relevant blocks and checks each cycle's connectivity and degree,
the exact edge multiset, the singleton count, and the formula. It
imports the earlier large-leaf constructors; the separate
[odd-hub replay](odd_hubs_all_t_independent_replay.py) independently
passes 1,024 cases for odd hub sizes `1,...,31` and leaf counts
`1,...,4p`. The unbounded result rests on the written constructions
and case split above.
