# Fourier tail for every even prefix with four-component pages

For every prime `p≡9 (mod 16)` with `p≥10^14`, every even translated
page-growth prefix `j=2r` with `2≤j≤(p−3)/2` can be repaired by three
rectangle trades per adjacent pair. Hence

    d(K_{p,p+2j}) = p+2j + (p−1)/2 + j,

and the same sharp formula holds after any number of `p`-leaf offset
blocks. This extends [item 80's early-prefix range](80_four_component_even_prefix_range.md)
to all even prefixes for sufficiently large primes. It does not by
itself repair odd prefixes.

Put `k=(p−1)/2`, `a=g⁴`, and use the fictitious pair start `c=k−2`.
Let `E_c` be the exact relabel set from [item 80](80_four_component_even_prefix_range.md), and
`B=F_p\(E_c−c)` in the translated parameter `w`. Under
`X=(a+1)w−a`, [item 67's](67_skew_late_prefix_geometry.md) algebra gives

    E_c^X = −I ∪ −aI,   I={0,...,k−2}.

[Item 68's](68_half_interval_overlap_all_large_primes.md) elementary overlap theorem applies to any unit `a≠±1` and
gives `|B|≥ceil(k/3)≥(p−1)/6`. Its Fourier calculation applies to
the same two interval complements of length `(p+3)/2` and gives

    ||hat 1_B||_1 < A(p)^2,
    A(p)=2+3π/8+(log p)/2.

Fix one quartic star pattern `s=1,2,3` on the four distinct affine
forms `L=(w+δ,w,w+δ−1,w−1)`. Expand each prescribed label indicator
using the quartic character, on the domain where all four forms are
nonzero. For a nontrivial exponent tuple supported on `r` forms,
the mixed complete sum at any nonzero additive frequency is

    Σ_w e_p(ξw) ∏_{i in support} ψ^{e_i}(L_i(w)).

[Katz, *Estimates for Nonsingular Mixed Character Sums* (2007)](https://web.math.princeton.edu/~nmk/nsingmixedfinal.pdf),
Theorem 1.2, with `n=1`, `f(w)=ξw`, `r` distinct linear `g_i=L_i`,
and nontrivial multiplicative characters `ψ^{e_i}`, has constant
`C(1,1,1,...,1)=r`; thus its absolute value is at most `r√p`.
The zero-frequency pure sum is at most `(r−1)√p` by the arbitrary-order
polynomial character-sum bound cited in item 79, so `r√p` works uniformly.
Fourier completion gives at most `r√p A(p)^2` over `B`.

There are `binom(4,r)3^r` exponent tuples with support `r`, and
`Σ_r binom(4,r)3^r r=768`. Omitting the four roots costs `4/256`
from the trivial term plus
`Σ_r binom(4,r)3^r(4−r)/256=252/256` from nontrivial terms.
Therefore each prescribed pattern occurs at least

    N_s(B) ≥ |B|/256 − 3√p A(p)^2 − 1
           ≥ (p−1)/1536 − 3√p A(p)^2 − 1.          (F)

At `p=10^14`, the elementary bounds `log(10^14)<33` and `π<22/7`
give `A(p)<20`, so the right side of (F) exceeds `5×10^10`, far above
the `8` potential hub conflicts when choosing the third star edge.
The ratio `A(p)^2/√p` decreases for all `p≥10^14` (differentiate its
logarithm: `1/A−1/2<0`), and `1/p` decreases; hence (F) remains
greater than 9 thereafter. Thus for all eligible primes
`p≥10^14`, three hub-disjoint star rectangles exist at `c=k−2`.
The nested exceptions make the same three parameters work for every
earlier page pair; thus **all even growth prefixes** `2≤j≤k−2`
attain the lower bound. The square-color slot table is unaffected by
page trades, so all pairs can be repaired independently. The
odd-hub parity/capacity bound proves equality. Katz's `n=1`,
degree-one constant and the transfer of item 68's overlap and
Fourier bounds from `a=g²` to `a=g⁴` were independently audited.

The [finite exploratory scan](80_four_component_final_pair_small_scan.py)
finds a double-tree triple at the same conservative final start for
all 151 eligible primes through 10,000. This evidence does not bridge
the gap to `10^14`; the theorem above is the analytic tail.
