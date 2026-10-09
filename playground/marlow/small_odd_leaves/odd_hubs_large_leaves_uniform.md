# Uniform large-leaf formula for every odd hub count

Let `p>=3` be odd, let `lambda=(p-1)/2`, and let `t>=p-1` be any
integer. For partitions of the edges of `K_(p,t)` into singleton edges
and simple cycles,

```text
d(K_(p,t)) = t + ceil(lambda*t/p).
```

For `p=1` the graph is a star, so `d(K_(1,t))=t` for all `t>=0`.
The proof for `p>=3` uses the [uniform odd-small-leaf
construction](odd_all_leaves_uniform.md), an explicit even-even
weave, and a one-square-block lift. It does not depend on primality,
dyadic arithmetic, or a finite per-`p` search.

## Lower bound

Every leaf has odd degree `p`; cycles contribute even degree there.
Hence every leaf has an odd positive number of singleton edges. If
there are `s=t+2k` singletons, `k>=0`, and `c` cycles, each cycle has
at most `2p` edges, so

```text
c >= ceil((pt-s)/(2p)) = ceil((lambda*t-k)/p)
  >= ceil(lambda*t/p)-k.
```

Thus `s+c >= t+ceil(lambda*t/p)+k`. Equality requires exactly one
singleton at each leaf.

## Odd `t>=p`

Transpose `K_(p,t)` to `K_(t,p)`. Both side sizes are odd and the
larger one is `t`. The [uniform odd-small-leaf theorem](odd_all_leaves_uniform.md)
gives a partition of `K_(t,p)` with `t` singleton edges and
`ceil(t*lambda/p)` cycles. Transposition preserves simple cycles and
edge disjointness, attaining the lower bound.

## Even base `p-1<=t<=2p-2`

Write `m=p-1=2lambda` and `q=t`, so `q` and `m` are even and `q>=m`.
Label `q` temporary hubs by `Z/q` and `m` temporary leaves by
`0,...,m-1`. For each `j=0,...,q/2-1`, take the alternating cycle

```text
H_(j,k)=2j+k mod q,       L_k=k,       k=0,...,m-1.
```

It is simple because `m<=q`. At each leaf `k<m-1`, its two hub
neighbors in cycle `j` are `2j+k` and `2j+k+1`, one from each parity
class of `Z/q`; at the last leaf they are `2j+m-1` and `2j`, again
one from each parity class. As `j` varies, these `q/2` cycles
partition `K_(q,m)` exactly. Transpose to obtain a decomposition of
`K_(p-1,t)` into `t/2` simple cycles, each of length `2(p-1)`.
Add the last hub and make all its `t` incident edges singletons.

The cycle count meets the target, since `t/2` is an integer and

```text
lambda*t/p = t/2 - t/(2p),       0 < t/(2p) < 1.
```

The strict upper inequality uses `t<=2p-2`. Therefore
`ceil(lambda*t/p)=t/2`.

## Even `t>=2p`

Put `t_0=t-p`. Because `t` is even and `p` is odd, `t_0` is odd;
because `t>=2p`, `t_0>=p`. Use the odd-`t_0` construction above on
the original `p` hubs and a set of `t_0` leaves. On a disjoint set
of `p` new leaves, add the explicit `K_(p,p)` square block from the
[uniform odd-small-leaf proof](odd_all_leaves_uniform.md): it has
one singleton at each new leaf and `lambda` Hamilton cycles. The
two leaf sets have disjoint edge sets even though the hub set is
shared, so together they partition every edge of `K_(p,t)`.

The combined partition has `t_0+p=t` singletons and

```text
ceil(lambda*t_0/p)+lambda = ceil(lambda*t/p)
```

cycles. Thus it reaches the lower bound. The three cases exhaust
all `t>=p-1`: `p-1` is even, every later odd `t` is at least `p`,
and every later even `t` is either in the displayed base interval
or at least `2p`.

## Bounded replay

The [full-edge checker](odd_hubs_large_leaves_uniform_check.py)
passes 795 partitions for odd `p=3,...,31` and every
`t=p-1,...,4p`. It checks cycle degree and connectivity, edge
disjointness, exact spoke coverage, one singleton per leaf, and the
sharp part count. A [separately implemented broader replay](odd_hubs_all_t_independent_replay.py)
passes 1,024 cases for odd `p=1,...,31` and every `t=1,...,4p`;
its even-base builder uses a differently oriented weave. These
finite checks guard against indexing errors. The parity and block
arguments above establish the unbounded result.
