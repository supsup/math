# An optimal first odd base for every prime hub count 5 mod 8

Let \(p\ge13\) be prime with \(p\equiv5\pmod8\), and put \(t=p+2\). The [antipodal starter page](53_skew_starter_page.md) and the [two-trade lemma](55_skew_two_trade_first_step.md) give an optimal partition of \(K_{p,t}\) whenever some primitive root \(g\) passes eight explicit algebraic exclusions and one quadratic-character test. **For every such prime \(p\ge29\), a suitable \(g\) exists.** Therefore

\[
d(K_{p,p+2})=p+2+\left\lceil\frac{(p-1)(p+2)}{2p}\right\rceil
=\frac{3p+5}{2}.
\]

The same construction plus disjoint \(p\)-leaf offset blocks gives the equality at \(t=p+2+pq\) for every integer \(q\ge0\). This result concerns that one residue class of leaf counts. In particular, it is not the all-residue fixed-hub formula. The exceptional small prime \(p=13\) also has the optimal first base, by the separate explicit [repair](54_thirteen_skew_repair.md).

## The generator criterion

Write \(a=g^2\). The conditional two-trade lemma requires the two linear factors \(3a+1\) and \(a+3\), and six polynomials

\[
a^2-4a-1,\quad a^2+3,\quad a^2+1,\quad
a^2-2a-1,\quad a^2+4a-1,\quad 3a^2+1
\]

to be nonzero modulo \(p\), and requires

\[
\chi\bigl((a+3)(3a+1)\bigr)=-1.
\]

Here \(\chi\) is the quadratic character. The [lemma](55_skew_two_trade_first_step.md) expands every required square-color slot and proves that these conditions preserve all slots and make both checkerboard trades join the split page without disconnecting an old color. The two linear and six quadratic factors forbid at most \(2+6\cdot2=14\) values of \(a\), hence at most 28 primitive roots \(g\). The least primitive root need not work: changing \(g\) is essential even at some small primes.

## All sufficiently large primes

Put \(n=p-1\), \(\theta=\varphi(n)/n\), \(V(n)=2^{\omega(n)}\), and \(Q(x)=(x^2+3)(3x^2+1)\). For primitive \(g\), \(\chi(Q(g))\) is the character test above. The four roots of \(Q\) are distinct and nonzero in the algebraic closure when \(p\ge13\).

The primitive-element indicator formula in [Cohen–Sharma–Sharma, *Primitive Values of Rational Functions at Primitive Elements of a Finite Field* (2019), §2](https://arxiv.org/pdf/1909.13074) expresses

\[
T=\sum_{g\text{ primitive}}\chi(Q(g))
\]

as a weighted sum of multiplicative-character sums; the absolute coefficients add to \(\theta V(n)\). For each summand, the character belonging to the indicator has squarefree order \(d\). Combining it with \(\chi\) gives a character \(\eta\) of squarefree order \(m=\operatorname{lcm}(d,2)\) and a sum of \(\eta(x^jQ(x)^{m/2})\). Its polynomial has at most five distinct roots, and the exponent \(m/2\) at each root of \(Q\) prevents an \(m\)-th power. The paper's Lemma 2.1 consequently bounds each sum by \(4\sqrt p\); the trivial indicator character has the same bound after accounting for \(x=0\). Thus

\[
|T|\le4\theta V(n)\sqrt p.
\]

At most four primitive \(g\) have \(Q(g)=0\). The number with negative character is therefore at least

\[
\frac{\varphi(n)-4-4\theta V(n)\sqrt p}{2}.
\]

Since \(\theta\ge1/V(n)\), the inequality \(n>V(n)(4\sqrt p+60)\) makes this count greater than 28, leaving a root outside all forbidden algebraic values. The same paper's Lemma 3.2 gives \(V(n)<37.469n^{1/6}\). For \(n\ge10^7\),

\[
V(n)(4\sqrt{n+1}+60)
<187.345n^{2/3}<n;
\]

the last strict inequality holds at \(10^7\) and strengthens as \(n\) grows. This proves the generator criterion for every prime in the class with \(p-1\ge10^7\).

## Exhausting the finite range

The standard-C++17 [finite sweep](57_skew_first_base_finite_sweep.cpp) independently enumerates every prime \(p\equiv5\pmod8\) up to \(10^7\), factors \(p-1\), tests primitive roots using all prime divisors, and evaluates the eight algebraic exclusions and the character by Euler's criterion. It stops with an error if any \(p\ge29\) lacks a witness, or if the criterion unexpectedly holds at 13. The complete sweep returns:

```text
limit=10000000 primes_5mod8=166203 witnesses_p_ge29=166202 max_first_g=134 max_generators_tested=20 hardest_p=963181
```

Reproduce with `g++ -O2 -std=c++17 playground/marlow/57_skew_first_base_finite_sweep.cpp -o /tmp/skew_first_base && /tmp/skew_first_base`. The source uses 64-bit signed products; its largest polynomial product is below \(3\cdot10^{14}\). Its sieve proves primality for the enumerated values, and the cyclic-group generator test is exact. The analytic range starts at \(p-1=10^7\), so together the sweep and bound cover every prime in the stated class.

The first-base construction is separate from the later page-pair repairs.
Together with those repairs, the analytic tail and finite criterion
scan in [item 69](69_skew_prime_hub_all_residues.md) now give the
all-residue formula for this prime class.
