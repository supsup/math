# A half-interval overlap theorem closes all large 5-mod-8 prime hubs

**Graph theorem.** For every prime \(p\equiv5\pmod8\) with
\(p\ge10^9\), and every integer \(t\ge p-1\), put \(k=(p-1)/2\).
Then

\[
d(K_{p,t})=t+\left\lceil\frac{kt}{p}\right\rceil.
\]

The new ingredient is the elementary overlap theorem below. Together
with the [exact late-pair criterion and mixed character bound](67_skew_late_prefix_geometry.md),
it repairs every remaining odd leaf residue. The even-base, first-base,
and offset constructions are identified at the end. This proves a
large-prime tail; it makes no all-residue claim below the stated prime
threshold or below \(t=p-1\).

**Theorem.** Let `n=2k+1≥5` be odd, let `H={1,…,k}` in `Z/nZ`, and
let `a` be a unit with `a≠±1 (mod n)`. Then

    |H∩aH| ≥ ceil(k/3).

The prime hypothesis is unnecessary for this overlap theorem. The bound is exactly sharp for
every modulus `n=6j+1`: with `a=−3`, one has `k=3j` and
`|H∩aH|=j`. Here `−3` is always a unit.

## Metric reduction

For a nonzero residue `x`, write `||x||=min(x mod n, (−x) mod n)∈H`.
For every `s∈Z/nZ`, the cyclic interval identity is

    |H △ (H+s)| = 2||s||.                              (1)

Set `m=|H∩aH|`. Because `H` chooses one element of every nonzero
pair `{x,−x}` and multiplication by a unit preserves these pairs,
`aH` also chooses exactly one. Thus `−aH` is its complement within
the nonzero residues.
Consequently `|H△(−aH)|=2m`. For `1≤t≤k`, triangle inequality for
symmetric difference, translation invariance, and (1) yield

    2||at|| = |H△(H+at)|
             ≤ |H△(−aH)|
               + |−aH △ (−aH+at)|
               + |−aH+at △ H+at|
             = 4m+2t.

Thus `||at||−t≤2m`. Also `m(a)=m(a^−1)`. If `s=||at||`, then
`||a^−1s||=t`, so applying the same inequality to `a^−1` and `s`
gives `t−||at||≤2m`. Hence

    max_{1≤t≤k} | ||at||−t | ≤ 2m.                     (2)

Write `M=max_{1≤t≤k}| ||at||−t |`. It remains to show that
`M≥T=2ceil(k/3)−1` for every unit `a≠±1`.

## Radial expansion lemma

Put `r=||a||∈{2,…,k}`. Replacing `a` by `−a` changes no norms.

**Even `r=2v`.** At `t=1` the displacement is `r−1`. Also
`rk ≡ −v (mod n)`, so at `t=k` it is `k−r/2`. Thus
`M≥max(r−1,k−r/2)`. To see this is at least `T`, write
`k=3j,3j+1,3j+2`:

* For `k=3j`, if `r−1<T=2j−1`, then `r≤2j−1`, whence
  `k−r/2>2j≥T`.
* For `k=3j+1`, if `r−1<T=2j+1`, then evenness gives
  `r≤2j`, whence `k−r/2≥2j+1=T`.
* For `k=3j+2`, the same assumption gives `r≤2j`, whence
  `k−r/2≥2j+2>T`.

**Odd `r≥5`.** Write `k=rq+s`, `0≤s<r`, `q≥1`.
At `t=q`, since `rq≤k`, the displacement is `L=(r−1)q`.
At `t=q+1`, since `k<r(q+1)≤k+r≤2k<n`, the displacement has
absolute value `|L+2s−r|`. Hence

    M≥L+max(0,2s−r).                               (3)

If `q≥2`, (3) is at least `2k/3`:

* If `2s≤r`, then `3L−2k=(r−3)q−2s ≥ 2r−6−(r−1)=r−5≥0`.
* If `2s>r`, then
  `3(L+2s−r)−2k=(r−3)q+4s−3r`
  `≥2r−6+2(r+1)−3r=r−4>0`, since odd `r` has
  `s≥(r+1)/2`.

Equality in the first bound occurs only at `(r,q,s)=(5,2,2)`,
where `k=12` and `M=8>T=7`; otherwise the bound is strict. In any
case, integrality gives `M≥ceil(2k/3)≥T`.

If `q=1`, (3) gives at least `max(r−1, 2k−2r−1)`; the latter
term may be negative, which only weakens this lower bound. For
`k=3j`, both terms being `<T=2j−1` would require at once
`r≤2j−1` and `r>2j`, impossible. For `k=3j+2`, both terms
`<T=2j+1` would require `r≤2j+1` and `r≥2j+2`, impossible.
For `k=3j+1`, the only possible failure is `r=2j+1`, but then
`n=6j+3=3r`, so `r` (and hence `a`) is not a unit. Thus `M≥T`.

**Odd `r=3`.** If `k=3j`, choose `t=j`; then `||3t||=k`
and `M≥2j≥T=2j−1`. If `k=3j+2`, choose `t=j+1`;
then `3t=k+1`, `||3t||=k`, and `M≥2j+1=T`.
The remaining case `k=3j+1` has `n=6j+3` divisible by 3,
so `r=3` is not a unit.

This proves the radial lemma. Combining it with (2) yields
`2m≥2ceil(k/3)−1`, hence `m≥ceil(k/3)`.

## Consequence for the antipodal late-prefix criterion

In the math problem, `p≡5 (mod 8)` is prime, `k=(p−1)/2`, and
`a=g²` has order `k≥6`; thus `a≠±1`. At the hardest odd pair start
`c=k−2`, put `I_c={0,…,k−2}`. Removing the two elements
`k−1,k` from `H` can destroy at most four pairs `(x,ax)` from
`H∩aH` (two by domain deletion and two by image deletion).
Including `0` gives

    |I_c∩aI_c| ≥ 1+ceil(k/3)−4 = ceil(k/3)−3,
    |B_c| = 3+|I_c∩aI_c| ≥ ceil(k/3).               (4)

Combining (4) with the [Fourier–Weil bound](67_skew_late_prefix_geometry.md)
proves `G∩B_c≠∅` whenever

    ceil(k/3) > 8√p(2+log p)²+8.                    (5)

Here is an explicit threshold check. From (4),
`|B_c|≥ceil(k/3)≥(p−1)/6`; it suffices that

    p−49 > 48√p(2+log p)².                              (6)

The ratio `(2+log p)²/√p` decreases for `p>e²`, as its logarithmic
derivative has the sign of `2−log p`. At `p=10^9`,
`log p<21` and `√p>31622`, so the right side of (6), divided by
`p`, is less than `48·23²/31622<0.81`. The left side divided by
`p` is at least `1−49/10^9>0.99`. Thus (6) holds for every
`p≥10^9`. The elementary bounds can be checked without floating
point: `e>27/10` from its first six series terms and
`(27/10)^21>10^9` show `log(10^9)<21`, while
`31622²<10^9`.

The positive point in `G∩B_{k−2}` survives **all** earlier adjacent
pairs because the exception sets are nested. For every even growth
prefix `j≥2`, [item 60](60_skew_adjacent_pairs.md) pairs the pages.
For every odd `j≥3`, [item 64](64_skew_third_base_two_trades.md)
repairs pages 1–3 and pairs the rest. The [first odd base](57_skew_first_base_all_prime_hubs.md)
uses two trades and may choose a different primitive root; the
[square and offsets](10_odd_hub_blocks.md) and [all even bases](24_even_base_residues.md)
complete the `p` residue classes. Their partitions meet the shared
lower bound, proving the graph theorem at the top.

The [finite overlap checker](68_half_interval_overlap_scan.cpp)
tests all units at every odd modulus through 10,000, as a backstop
for the elementary proof. The separate late-pair scans in item 67
are finite evidence for smaller primes. Publication priority for
this particular overlap lemma and graph corollary has not been
established.
