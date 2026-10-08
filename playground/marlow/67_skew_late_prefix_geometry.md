# Late antipodal-pair criterion: exact geometry and a conditional analytic bound

For prime `p ≥ 13` with `p ≡ 5 (mod 8)`, take primitive `g`, `a=g²`, `k=(p−1)/2`,
`D=a+1`, `δ=(1−a)/D`, and the character-good set

    G={w: χ(w(w+δ))=χ((w−1)(w+δ−1))=−1}.

The adjacent-pair note gives, for pair start `c≥2`, the **exact**
relabel-exception set. Under the affine change `X=Dw−a`, its image is

    E_c^X = −I_c ∪ −a I_c,       I_c={0,1,…,c} ⊂ F_p.

Write `B_c` for the complement of the exception set in the original
`w` variable; its affine image is the complement of `E_c^X`. Then

    |B_c|=p−2(c+1)+|I_c∩a I_c|.                         (1)

The [generated thirteen-residue diagram](art/skew_late_prefix_geometry.svg)
shows the two excluded progressions, their complement, and the two
surviving character-good sites. Its [generator](67_skew_late_prefix_diagram.py)
recomputes each set from the formulas above.

The exception sets are nested, and `G` does not depend on `c`. The hardest
allowed odd prefix has `j=k−1` pages and last pair start `c=k−2`;
there `|B_c|=3+|I_c∩aI_c|`. The hardest even prefix has last pair start
`c=k−3`, where `|B_c|=5+|I_c∩aI_c|`. A single point of `G∩B_{k−2}`
works for *every* later adjacent pair in *every* prefix. Together with
the separate first-three-page repair, this settles all odd
prefixes whenever the size condition below holds; it also settles
the even pair prefixes.

## A uniform conditional counting lemma

There is an absolute constant in the following explicit version:

    |G∩B_c| ≥ |B_c|/4 − 2√p(2+log p)² − 2.             (2)

Here is the proof. For an interval of residues, its normalized
additive Fourier transform has ℓ¹ norm at most `1+log p`: for nonzero
frequency `r` represented by `1≤|r|≤(p−1)/2`, the coefficient has
modulus at most `1/(2|r|)`, and the constant coefficient is at most 1.
Affine images have the same bound. Because `1_{B_c}` is the product of
two complementary progression indicators, its Fourier ℓ¹ norm is at
most `(2+log p)²`, uniformly in `a,c`.

The mixed Weil bound for `χ(P(w))e_p(rw)` is at most `4√p` for each of
the squarefree polynomials `P=F1,F2,F1F2` of degrees 2,2,4,
including `r=0` (where the ordinary Weil bound is enough). One source
for the mixed bound is N. Katz, *Estimates for Nonsingular Mixed
Character Sums*, Theorem 1.1, n=1, additive degree 1, multiplicative
degree at most 4, https://web.math.princeton.edu/~nmk/nsingmixedfinal.pdf.
Fourier completion therefore bounds each of the three character sums
over `B_c` by `4√p(2+log p)²`. Expanding
`(1−χ(F1))(1−χ(F2))/4` gives `|B_c|/4` plus three such sums. At the
four roots this expression can contribute at most `1/2` each although
those points are not in `G`, giving the final `−2`. Using the sharper
degree-2 mixed constants for F1,F2 gives the coefficient 2 in (2):
`(2+2+4)/4=2`.

Consequently the *computed geometric condition*

    |B_{k−2}| > 8√p(2+log p)² + 8                     (3)

rigorously supplies a universal late-pair witness for that particular
`p,g`, without testing quadratic characters point by point. The later
[half-interval overlap theorem](68_half_interval_overlap_all_large_primes.md)
proves the uniform geometric bound needed here and gives every prime
`p≡5 (mod 8)` at and above 60 million. The
complete-sum estimate from item60 alone cannot finish the last pairs:
its `N≈p/4` is smaller than the allowed `|E_c|≈3p/4` or more.

## A conditional concrete subfamily

For primes `p=6m+1 ≡ 13 (mod 24)` at which `a=−3` has order
`k=(p−1)/2`, it is a permissible primitive-square parameter (either
square root is primitive). At the maximal odd start `c=3m−2`, direct
interval counting gives

    |I_c∩(−3)I_c|=m+1,
    |B_c|=m+4=(p+23)/6.

Indeed, `q=0` works, and among `1≤q≤3m−2`, precisely
`m+1≤q≤2m` has `−3q mod p` in the same interval. Thus (3) proves
all paired prefixes whenever `(p+23)/6 > 8√p(2+log p)²+8` (for
example at every such prime above `10^9`). This is a conditional
subfamily statement; it does not assert infinitely many primes with
`−3` primitive-square order.

### One fully certified large prime

The [exact arithmetic certificate](67_skew_minus_three_witness.py)
finds `p=1,000,000,453 ≡ 13 (mod 24)`, proves primality by trial
division, and checks that `a=−3` has order `k=500,000,226`.
The distinct prime factors of `k` are `2,3,11,17,445633`; the script
checks `a^k=1` and `a^(k/q)≠1` for each factor. It also certifies

    |B_{k−2}|=(p+23)/6=166,666,746
       > 133,828,544
       > 8√p(2+log p)²+8.

The last comparison uses only integer arithmetic and the elementary
bounds `√p<31623` and `log p<21`. Since `k` is even, either square
root of `a` is primitive, so the preceding conditional lemma applies.
The common late-pair parameter, [item 60](60_skew_adjacent_pairs.md),
and the [first-three-page repair](64_skew_third_base_two_trades.md)
give **every odd base** at this particular `p`. The first odd base
uses [item 57](57_skew_first_base_all_prime_hubs.md), possibly with a
different primitive root; the square and all even bases use
[items 10](10_odd_hub_blocks.md) and [24](24_even_base_residues.md).
Thus the sharp formula

    d(K_{p,t})=t+ceil(((p−1)/2)t/p)

holds for **every `t≥p−1`** at `p=1,000,000,453`. This one-prime
certificate predates the uniform large-prime conclusion of item 68 and
independently checks one instance of it.

## Finite boundary

[The exact-set checker](67_skew_late_prefix_all_roots.py) scanned every primitive-square
parameter (deduplicating `g` and `−g`) for all 78 primes `p≡5 (mod 8)`,
`13≤p≤2000`, at the *hardest odd* start `c=k−2`. Every parameter had
`G∩B_c ≠∅`; the minimum survivor count was 2, at p=13. Output:
the final summary was `ALL_PASS 78 min_survivors (2, 13, 2, 4)`.
This is finite evidence, not a large-prime proof. The scan computes exact sets, not graph partitions;
the earlier page-switch theorem supplies the graph implication.
