# All odd fixed-leaf cycle partitions: explicit uniform construction

Let `p>=t>=3` be odd, and put `lambda=(t-1)/2`. Then the minimum
number of parts in an edge partition of `K_(p,t)` into singleton edges
and simple cycles is

```text
d(K_(p,t)) = p + ceil(p*lambda/t).
```

The construction below uses only a cyclic even-hub weave and a
two-edge switch. No search or cycle-decomposition existence theorem is
needed. The [standalone checker](odd_all_leaves_uniform_check.py)
replays every nonzero seed with odd `t=3,...,51`; the proof is algebraic
and covers all odd `t` and `p` in the stated range.

## Lower bound

At every hub, cycles contribute even degree, whereas `t` is odd.
Thus every hub has an odd positive number of singleton spokes. If
there are `s=p+2k` singletons, `k>=0`, and `c` cycles, then each cycle
has at most `2t` edges, so

```text
c >= ceil((pt-s)/(2t)) = ceil((p*lambda-k)/t)
  >= ceil(p*lambda/t)-k.
```

Therefore `s+c >= p+ceil(p*lambda/t)+k`. Equality requires exactly
one singleton at every hub.

## An even-hub cyclic weave

Fix a seed `p=t+2r` with `1<=r<t`. Write

```text
m=2lambda=t-1,       n=lambda+r,       q=2n=p-1.
```

Label the old hubs by `Z/q` and the active leaves by `0,...,m-1`.
For each `j=0,...,n-1`, form an alternating cycle `C_j` with ordered
hub and leaf sequences

```text
H_(j,k) = 2j+k mod q,       L_k=k,       k=0,...,m-1.
```

The `m` hubs in each cycle are distinct because `m<=q`; the leaves
are distinct. These `n` cycles partition all edges of `K_(q,m)`.
Indeed, at leaf `k<m-1`, cycle `j` uses the hubs `2j+k` and
`2j+k+1` modulo `q`, which run through the two parity classes of
`Z/q` as `j` varies. At leaf `m-1`, it uses `2j+m-1` and `2j`, again
the two parity classes because `m` is even.

Now add leaf `z=m` and make all `q` old edges to `z` singleton spokes.
Add one new hub `u=q`. The graph is now `K_(p,t)`; its edges from `u`
are not yet assigned.

## Choosing disjoint switches

We need `lambda` distinct cycle indices `j_s`, one for each
`s=0,...,lambda-1`, such that the residues `j_s+s mod n` are all
distinct. This choice is explicit:

* If `n` is odd, take `j_s=s`. Then `j_s+s=2s mod n` are distinct.
* If `n=2a` is even, define a permutation of `0,...,n-2` by
  `sigma(j)=(j+a-1) mod (n-1)`, and take `j_s=sigma^(-1)(s)`.
  This is defined because `lambda<=n-1`. For `0<=j<a`, the integer
  `j+sigma(j)` runs through `a-1,a+1,...,3a-3`. For
  `a<=j<=2a-2`, it runs through `a,a+2,...,3a-4`.
  Together these are the `n-1` consecutive integers
  `a-1,...,3a-3`, so their residues modulo `n` are distinct.

The selected rows `j_s` are distinct in either case. In selected
cycle `C_(j_s)`, let `b=2s`. Delete the two directed hub-to-leaf
edges

```text
H_(j_s,b)-L_b,       H_(j_s,b+1)-L_(b+1),
```

and insert four edges

```text
H_(j_s,b)-z,       H_(j_s,b+1)-z,
u-L_b,             u-L_(b+1).
```

This transforms `C_(j_s)` into one simple `2t`-cycle. To see the
connectivity explicitly, removing the two old edges leaves the short
path `L_b-H_(j_s,b+1)` and a second path from `L_(b+1)` around the
remaining old cycle to `H_(j_s,b)`. The new paths
`L_b-u-L_(b+1)` and `H_(j_s,b+1)-z-H_(j_s,b)` join them into one
cycle. All old vertices remain distinct and `u,z` are new. The
unselected `r=n-lambda` cycles remain simple `2(t-1)`-cycles.

Every active leaf appears in exactly one selected pair
`(L_(2s),L_(2s+1))`, so every edge from `u` to an active leaf is
used once. The old hubs selected for the two cuts in row `j_s` are

```text
H_(j_s,2s)   = 2(j_s+s)     mod 2n,
H_(j_s,2s+1) = 2(j_s+s)+1   mod 2n.
```

These `2lambda=m` hubs are all distinct: each selected residue
`j_s+s mod n` supplies one even and one odd hub. Make each deleted
old edge a singleton. Its hub has had its former `z` singleton
switched into a cycle, so it still has one singleton. The other
`q-m=2r` old hubs keep their singleton edge to `z`; make `(u,z)`
the new hub's singleton. Thus every hub has exactly one singleton.
All old-to-active edges, old-to-`z` edges, and new-hub edges have
been assigned exactly once.

There are `lambda` cycles of length `2t` and `r` cycles of length
`2(t-1)`, hence `lambda+r` cycles. Since

```text
p*lambda = (t+2r)*lambda = t*(lambda+r)-r,
```

and `0<r<t`, we have `ceil(p*lambda/t)=lambda+r`. The block reaches
the lower bound. Its singleton edges end `2r+1` times at `z` and
once at each other leaf, consistent with total cycle deficiency `r`.

## The zero seed and all larger odd hub counts

For `r=0`, use the explicit `t`-hub square block. Label hubs and
leaves by `Z/t`, make `(h,h)` a singleton for each `h`, and for
`a=0,...,lambda-1` take the alternating cycle

```text
H_i=-i mod t,       L_i=2a+1-i mod t,       i=0,...,t-1.
```

At leaf `L_i`, its two spoke differences are `2a+1` and `2a+2`;
the `lambda` cycles use every nonzero shift once and are simple.
Thus the square block has `t` singletons and `lambda` cycles.

Every odd `p>=t` has a unique expression
`p=t+2r+2tm` with `0<=r<t` and `m>=0`. Use the `r`-seed block
above and `2m` disjoint copies of the square block, all on the same
`t` leaves. Their hub edge sets are disjoint. The resulting partition
has `p` singletons and `lambda+r+2m*lambda` cycles, equal to
`ceil(p*lambda/t)` by the displayed seed identity. This proves the
formula for every odd `p>=t>=3`.

## Verification and provenance

`python3 -I odd_all_leaves_uniform_check.py` checks all 650
nonzero seed blocks for odd `t=3,...,51`: cycle simplicity and
connectivity, exact edge-disjoint coverage, one singleton per hub,
and sharp cycle count. A [separately written skeptical audit](odd_all_leaves_uniform_skeptical_audit.md) and [independent edge-multiset replay](odd_all_leaves_uniform_independent_replay.py) check all 2,550 nonzero seeds with odd `t=3,...,101`. A second [adversarial proof audit](odd_all_leaves_uniform_peer_audit.md) and [no-import checker](odd_all_leaves_uniform_peer_check.py) independently cover 665 cases, including large `t=257` boundary seeds. The scripts use different cycle-reconstruction methods and import neither one another nor any search code. These finite replays test the formulas; the parity, weave, switch, and modulo arguments above prove the unbounded assertion.
