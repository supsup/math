# Asymptotic one-cut bridge for the second leaf

**Status: Fixpoint reviewed this as a sound sufficient-family proof (Stafficy/35474).** This is a sufficient result for the
specific multiplicative two-ring splice in the adjacent
[`bridge.md`](bridge.md), not a
claim about all small primes. The [independent skeptical audit](asymptotic_one_cut_skeptical_audit.md)
and [exact edge replay](independent_one_cut_check.py) accompany this packet.
Let `p ≥ 5` be prime, `n=(p−1)/2`, and
`W(n)=2^{ω(n)}`. The argument below gives a parameter triple and hence an
one-short cycle profile at the known optimal part count for `K_(p,p+2)` whenever

```text
                  sqrt(p) ≥ 66 W(n).                       (A)
```

In particular it is an all-sufficiently-large-primes construction, since
`W(n)=n^{o(1)}`. The bound (A) is intentionally crude. It is independent
of the choice of generator `a` of the quadratic-residue group.

An explicit absolute corollary is **every prime `p ≥ 3,000,000,000`**.
This is a convenient sufficient cutoff, not a claimed sharp threshold;
it does not settle every prime below it. The optimal part count itself
is already known for odd hub order and these leaf counts from
[`odd_hubs_large_leaves_uniform.md`](../odd_hubs_large_leaves_uniform.md).
The contribution here is the profile: `(p−1)/2` simple `2p`-cycles,
each spanning all `p` hubs and omitting two of the `p+2` leaves, plus
one `2(p−1)`-cycle and `p+2` singleton spokes.
For each prime `q≥37`, `2≤q^(1/5)`; the smaller primes are
`2,3,5,7,11,13,17,19,23,29,31`, whose product is
`200560490130`. Their combined excess factor
`2^11 / 200560490130^(1/5)` is less than `12`. Hence
`W(n)≤12 n^(1/5)≤12(p/2)^(1/5)`. For `p≥3,000,000,000`,
`sqrt(p)≥792(p/2)^(1/5)`, equivalently
`4p³≥792^10`, true at the endpoint and increasingly so.

## One-parameter specialization

Choose any generator `a` of `Q=QR(F_p)`. Put

```text
  R(c)=c+a−1,
  F(c)=c²+2(a−1)c−(a−1),
  b(c)=a c/R(c),
  L(c)=F(c)/R(c),
  g(c)=L(c)/c=F(c)/(c R(c)),
  epsilon=−χ(−1).
```

Choose `c` avoiding zeroes of `c`, `R`, `F`, `1−c` and satisfying

```text
  χ(c)=−1, χ(R)=+1, χ(F)=−1, χ(1−c)=epsilon,
  ord(g)=n.                                                (B)
```

Then `b` is a nonresidue because `a,R` are residues and `c` is a
nonresidue. Also

```text
  1−b=(a−1)(1−c)/R,
  χ(1−b)=χ(a−1)epsilon=−χ(1−a).
```

Thus `(a,b)` satisfies the original shift-pair condition. The second
leaf's spokes have multipliers `U=c+a−1=R` and
`V=c+b−1=F/R=L`, whose characters are opposite. Since `χ(L/c)=+1`
and `ord(L/c)=n`, both internal rings are single `2n`-cycles. Finally
`bR=ac`, precisely the two-edge splice condition with `τ=a, M=c`.
The exact graph lemma in `bridge.md` then produces the one-short page.

## Counting `c` by a multiplicative-character sieve

The five geometric points that matter are roots of `c`, `R`, `F`, and
`1−c`; they are distinct over the algebraic closure. Indeed the
discriminant of `F` is `4a(a−1)≠0`, while

```text
  F(0)=−(a−1), F(1)=a, F(1−a)=−a(a−1)
```

are nonzero. Let `A` exclude the at most five corresponding elements
of `F_p`. On `A`, the four-sign indicator is

```text
  P(c)=(1−χ(c))(1+χ(R))(1−χ(F))
       (1+epsilon χ(1−c))/16.
```

For every nonempty term in this expansion, the quadratic-character
polynomial is not a square, because at least one of the five distinct
roots has odd valuation. The standard Weil bound for a nontrivial
multiplicative-character sum of a polynomial with at most five distinct
roots bounds its complete sum by `4 sqrt(p)`; restricting to `A` adds
at most five. Therefore

```text
          sum_(c in A) P(c) ≥ (p−5)/16−(4 sqrt(p)+5).
```

For `x∈Q`, the exact primitive-element indicator in the cyclic group
`Q` is

```text
  1_{ord(x)=n} = theta(n)
    sum_(d|n) mu(d)/phi(d) sum_(psi:ord psi=d) psi(x),
  theta(n)=phi(n)/n.
```

For every nontrivial `psi`, select an extension `Psi` to `F_p^×` of
order `2d` (the two extensions differ by `χ`; at least one has this
order). Each of the 16 sums in `sum P(c)Psi(g(c))` remains
nontrivial: at each root of `F`, its exponent modulo `2d` is `1` or
`1+d`, neither zero for `d>1`. The same five-point Weil estimate gives
absolute value at most `4 sqrt(p)+5`. The aggregate absolute
coefficient of the primitive sieve is
`sum_(d|n)|mu(d)| = W(n)` after summing characters of each order.
Because (B)'s signs force `g(c)∈Q`, the primitive indicator applies to
every selected `c`. The number of valid `c` is therefore at least

```text
 theta(n) [(p−5)/16−W(n)(4 sqrt(p)+5)].                  (C)
```

If `sqrt(p)≥66 W(n)`, then the bracket in (C) is positive: with
`x=sqrt(p)` and `W≥1`,
`x²−64Wx−80W−5 ≥ 132W²−80W−5 > 0`.
Thus (B) has a solution.

For clarity on the rational denominator in `g`: with `Psi` of order
`2d`, replace every negative exponent on `c` or `R` by its nonnegative
representative modulo `2d`. This changes the summand only at their
zeroes (already excluded from `A`) and yields a **polynomial** with at
most the same five distinct roots. It has a simple nonzero exponent
modulo `2d` at each root of `F`, so the usual polynomial form of the
Weil bound applies even when `2d` is not squarefree. For background on
the primitive-character sieve and this type of Weil estimate, see
[Cohen–Sharma–Sharma, *Primitive Values of Rational Functions at
Primitive Elements of a Finite Field*](https://arxiv.org/pdf/1909.13074),
§2; their displayed rational-function lemma has a squarefree-order
hypothesis, while the polynomial reduction just given uses the general
polynomial form.

## Sanity checks and limitations

Direct integer scanning of this *restricted* `b=ac/R` family found a
triple at all `73` primes `17≤p≤401` (and also `p=7,11`), while
`p=5,13` have none in this family. The existing independent exact-edge
checker also replayed all `20` restricted-family cases `17≤p≤101`
successfully. Reproduce this bounded check with
`python3 -I restricted_family_check.py` in this directory.
The reported threshold is far too large to replace a finite census
practically, but it does turn the previously heuristic asymptotic
existence of the **one-cut** family into a standard character-sum
argument. The Weil bound, extension-order assertion, and graph lemma
received an independent skeptical audit and Fixpoint's soundness review
at Stafficy/35474. Publication remains Charles's decision.
