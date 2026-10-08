# A half-interval overlap theorem closes all large 5-mod-8 prime hubs

**Graph theorem.** For every prime \(p\equiv5\pmod8\) with
\(p\ge60{,}000{,}000\), and every integer \(t\ge p-1\), put \(k=(p-1)/2\).
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

The [Fourier–Weil count](67_skew_late_prefix_geometry.md) can be
sharpened here because the two complementary interval factors of
`1_{B_c}` both have length `L=p-(k-1)=(p+3)/2`. For an interval of
that length, write its normalized additive Fourier coefficient at
`r`, represented by `1≤|r|≤k`, in the standard form

    |hat 1_J(r)| = |sin(πrL/p)| / (p|sin(πr/p)|).

Since `p sin(πr/p)≥2r` for `1≤r≤k`, the two frequencies `±r`
together contribute at most `1/r` for odd `r`. For even `r`,
`sin(πrL/p)=±sin(3πr/(2p))`, so their joint contribution is at
most `3π/(2p)`. Summing the odd terms by
`1/r≤(1/2)log(r/(r−2))` for odd `r≥3`, and noting there are at
most `k/2` positive even frequencies, gives

    ||hat 1_J||_1
       < 1 + (1 + (1/2)log k) + 3π/8
       < A(p) := 2+3π/8+(1/2)log p.                  (5)

Affine images have the same Fourier ℓ¹ norm. The product bound
therefore gives `||hat 1_{B_c}||_1<A(p)²`. The two quadratic mixed
sums and one quartic mixed sum in item 67 contribute respectively
`2√p,2√p,4√p` times this norm; its four polynomial roots cost at
most 2 more. Hence

    |G∩B_c| > |B_c|/4 − 2√p A(p)² − 2.              (6)

From (4), `|B_c|≥ceil(k/3)≥(p−1)/6`. A sufficient condition is

    p−49 > 48√p A(p)².                              (7)

The ratio `A(p)²/√p` decreases with `p`, since its logarithmic
derivative with respect to `p` is `1/A(p)−1/2<0`. At
`p=60,000,000`, `log p<18`, `π<22/7`, and `√p>7745` give
`A(p)<341/28`, so the right side of (7), divided by `p`, is less
than `48(341/28)²/7745<0.92`. The left side divided by `p`
is greater than `1−49/60,000,000>0.999`. Thus (7) holds for every
`p≥60,000,000`. Integer checks certify the elementary inputs:
the first seven series terms give `e>271/100`,
`(271/100)^18>60,000,000`, and `7745²<60,000,000`.

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
for the elementary proof. [Item 69](69_skew_prime_hub_all_residues.md)
then checks the exact late-pair criterion at every smaller eligible
prime, completing the full prime-class formula with a finite
computational component. Publication priority for this particular
overlap lemma and graph corollary has not been established.
