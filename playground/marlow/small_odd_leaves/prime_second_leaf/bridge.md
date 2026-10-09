# A second-leaf bridge criterion for multiplicative prime shift pairs

**Local research, unreviewed by Fixpoint.** Start with the prime-order
shift-pair `K_(p,p+1)` page from the independently audited
[`prime_shift_pair_all_primes.md`](../prime_shift_pair_all_primes.md). This note asks whether a
second new leaf `w` can replace one old leaf in every full color, while the
old new leaf `z` remains in those colors, to give the optimal one-short
profile for `K_(p,p+2)`. The criterion is exact for this **two-substitutions
per color, `w` outside the short cycle** scheme; it does not restrict
other trades.

Write `p=2n+1≥5`, `Q=QR(F_p)`, and choose base multipliers `a,b` as in
the prime shift-pair theorem. For `s∈Q`, the full color has offsets
`d_s=(1−a)s`, `e_s=(1−b)s`, with the old leaf `s` replaced by `z`.
Choose an old leaf `f(s)` to replace by `w` in that color. Its two
neighbors before replacement are

```text
              U_s=f(s)−(1−a)s,   V_s=f(s)−(1−b)s.       (1)
```

The new `w` spokes in the full colors must be distinct. Since there are
`2n=p−1` of them, exactly one hub `r_w` remains for its singleton.

## Exact leftover-graph criterion

In any optimal page of this form, `f` is an injection from `Q` into
`F_p\Q`. To see this, the existing page leaves three unassigned edges
at each old leaf in `Q` and one at each old leaf outside `Q`. Replacing
an old leaf in a full color frees two more edges at that leaf. An
optimal `K_(p,p+2)` page has exactly `p+2` singletons: every leaf has
odd degree `p` and hence needs at least one, while the intended one-short
profile attains the lower bound with exactly one per leaf. Any old leaf
can lie in at most one short cycle, contributing degree zero or two
there. Thus its unassigned degree must be one or three. No leaf of `Q`
can be chosen again, and each leaf outside `Q` can be chosen at most
once. As there are `n` full colors, the chosen leaves form precisely an
injection `f:Q→F_p\Q`.

Let `T=f(Q)`, and let `P` be the graph of all spokes left after both
substitutions in all `n` full colors. Assume the `2n` hubs in (1) are
distinct. Each old leaf in `Q∪T` has degree three in `P`; the one old
leaf outside `Q∪T`, and `z,w`, have degree one. Every hub has degree
three, because each of the `n` full cycles still traverses every hub
with degree two and the whole graph has `p+2` spokes at that hub.

**Criterion.** This second-leaf scheme gives the one-short optimum if
and only if the subgraph of `P` on the active old leaves `Q∪T` and the
hubs contains a simple cycle of length `2(p−1)`. The cycle then uses
every active old leaf and all but one hub. Each active leaf has exactly
one residual edge, and the omitted old leaf plus `z,w` each have their
unique residual edge. These are the `p+2` singleton spokes; all edges
are used exactly once. Conversely a page with the prescribed `n` full
cycles, one `2(p−1)` short cycle, and `p+2` singletons must take this
cycle from `P`.

The full colors remain simple `2p`-cycles because they merely relabel
two *distinct* old leaf vertices of their original simple square
cycle by `z,w`. Distinctness of (1) prevents overlap between their
`w` spokes; the first substitution already gives distinct `z` spokes.

**Uniform inherited-cycle obstruction.** The old short cycle uses all
leaves and hubs in `Q` and has degree two at every one of its vertices.
If every edge of that old cycle is retained in the new short cycle,
none of the additional active leaves can attach to it. Hence any
one-short second-leaf bridge of this kind must send at least one old
short-cycle edge to the singleton pool and splice in at least two
cross-coset spokes. Merely adjoining the newly freed edges to the old
cycle cannot work for any prime `p≥5`.

## Multiplicative submodel and a sufficient splice

Take `f(s)=c s` with `c` a nonresidue. Put

```text
              U=c+a−1,  V=c+b−1.                         (2)
```

The second leaf's spokes partition `F_p^*` precisely when `U,V` are
nonzero and have opposite quadratic characters. Then `T` is all the
nonresidues; the omitted old leaf, the omitted `w` hub, and the
eventual short-cycle hub are `0` if the latter exists, because the
three edges at hub zero are already `(0,0),(0,z),(0,w)` singletons.
Write `R` for the one of `U,V` in `Q`, and `L` for the nonresidue one.
The leftover cubic graph has:

* an internal `Q` ring with leaf `s` joined to hubs `s,a s`;
* an internal nonresidue subgraph with leaf `c s` joined to hubs
  `c s,L s`;
* cross spokes `s→b s` and `c s→R s`.

Let `r` be the order of `L/c` in `Q`. The nonresidue internal
subgraph has `k=n/r` disjoint cycles of length `2r`.
**Repair-distance lemma:** every Hamilton short cycle in this
multiplicative submodel must demote at least `k` edges of the old
`Q` short cycle to singletons. Each of the `k` nonresidue components
must enter and leave through at least two cross spokes, so the new
short cycle uses at least `2k` cross spokes. Each demoted edge of
the original `Q` cycle frees its two endpoints for exactly two cross
spokes, giving the bound. For `p=13,a=4,b=6,c=5`, one has
`L/c=12` of order two in `Q` of order six, hence `k=3`. The literal
certificate below demotes exactly three old short edges and uses
six cross spokes. This rules out a single two-edge splice for this
*specific parameter triple*, while leaving other parameters open.

If `L/c` generates `Q`, both internal subgraphs are single
`2n`-cycles. A **sufficient**, explicitly checkable two-edge switch is

```text
             b R ∈ {c, a c, L, a L}.                     (3)
```

Indeed choose `τ∈{1,a}` and `M∈{c,L}` with `bR=Mτ`.
Cut the internal `Q` edge from leaf `1` to hub `τ`, and the internal
nonresidue edge from leaf `cτ/R` to hub `b`. The two cross spokes
from leaf `1` to hub `b` and from leaf `cτ/R` to hub `τ` join the
two opened paths into one `2(p−1)`-cycle. Condition (3) is not
necessary: at `p=13`, `a=4,b=6,c=5` gives a Hamilton leftover graph
even though `L/c=12` has order two instead of `n=6`.

This submodel does **not** give a universal construction by itself.
At `p=5`, the base has `a=4,b=2`, and the only nonresidue choices are
`c=2,3`. For `c=2`, (2) gives `U=0`, repeating hub zero in the `w`
spokes. For `c=3`, it gives `U=1,V=4`, the same quadratic coset,
again repeating spokes. Nevertheless the unrestricted injection
`f(1)=0,f(4)=3` works: the short cycle uses old leaf zero and omits
hub two, while `w` omits hub four. Insisting on a common omitted hub
would wrongly exclude this valid smallest case.

## Exact finite controls and scope

[`exact_bridge_check.py`](exact_bridge_check.py) contains literal
parameters, replacement leaves, and short-cycle walks for
`p=5,7,11,13`. It rebuilds every full cycle, confirms every full and
short cycle is simple and connected, verifies exactly one singleton
per leaf, and checks all `p(p+2)` spokes once. All four cases pass.
The `p=7` positive page uses `a=4,b=5,f(s)=6s`; the earlier base
choice `a=2,b=6` has **no** valid injection even at the spoke-coverage
stage: among its 24 injections, two produce only three distinct `w`
hubs, sixteen produce four, and six produce five, never the required
six. The checker exhausts these cases. This is a finite
base-specific obstruction, not an obstruction to `K_(7,9)`.

There is no proof here that the Hamilton condition holds for every
prime `p`, even though the displayed small cases are positive. The
two-ring condition (3) gives a simple sufficient arithmetic route at
many primes; a theorem that these parameters always exist would need
a separate argument, and the `p=5,13` examples already show that this
particular route is too restrictive to cover all primes unchanged.
The [bounded finite continuation](multiplicative_splice_finite.md)
checks the one-cut route with full edge replays at every prime
`17≤p≤101` and stores literal short-cycle walks at `p=17,19,23`.
