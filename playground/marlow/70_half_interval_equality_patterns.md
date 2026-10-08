# Equality patterns in the half-interval overlap bound

Let \(n=2k+1\ge5\) be odd, \(H=\{1,\ldots,k\}\) in
\(\mathbb Z/n\mathbb Z\), and
\(m_n(a)=|H\cap aH|\) for a unit \(a\ne\pm1\).
[Item 68](68_half_interval_overlap_all_large_primes.md) proves
\(m_n(a)\ge\lceil k/3\rceil\). It also proves exact
sharpness whenever \(3\nmid n\):
\[
m_n(-3)=\lfloor 2k/3\rfloor-\lfloor k/3\rfloor
       =\lceil k/3\rceil.
\]
Because \(m_n(a)=m_n(a^{-1})\), the inverse of \(-3\)
also attains equality. These are proved statements, not patterns
inferred from the scan.

The [exact equality scanner](70_half_interval_equality_scan.cpp)
tested all 20,253,334 nontrivial unit multipliers over every odd
modulus \(5\le n\le10{,}000\). It evaluates the overlap by
integer floor sums and stops on any violation of the lower bound.
Its summary is:

    PASS odd_moduli=4998 units=20253334 equalities=6679 noncanonical=4 divisible3_equalities=11

A [direct-set Python crosscheck](70_half_interval_equality_small_crosscheck.py)
recomputes every multiplier through \(n=501\) without floor sums;
its 50,532 unit cases give the same exception lists.

For \(3\nmid n\), every equality in this finite range has
\(a=-3\) or \(a=(-3)^{-1}\), except the four extra pairs
\((n,a)=(11,2),(11,6),(17,10),(17,12)\). For
\(3\mid n\), equality occurs only at these eleven tested
pairs:

| \(n\) | equality multipliers \(a\) |
|:--|:--|
| 9 | 2, 4, 5, 7 |
| 15 | 2, 4, 8 |
| 21 | 4, 16 |
| 27 | 16, 22 |

The later [equality theorem](71_half_interval_equality_classification.md)
proves that the four extra pairs at \(n=11,17\) are the **only**
exceptions when \(3\nmid n\). For \(3\mid n\), it remains an
**unproved conjecture** that the eleven pairs in the table are
complete beyond the finite scan. A counterexample would be
mathematically interesting even though it would not affect the
lower bound or the graph theorem.

There is a small structural reduction. Put
\(r=\|a\|=\min(a\bmod n,(-a)\bmod n)\).
If equality holds, the radial displacement \(M\) in item 68
satisfies \(M\le2\lceil k/3\rceil\). For even
\(r\), evaluating \(M\) at \(t=1\) and
\(t=k\) gives
\[
r-1\le2\lceil k/3\rceil,\qquad
k-r/2\le2\lceil k/3\rceil.
\]
When \(k=3j\), evenness forces \(r=2j\), exactly the
radius of \((-3)^{-1}\) modulo \(6j+1\). When
\(k=3j+2\), the only candidates are \(r=2j\) and
\(r=2j+2\). For \(j\ge3\), the former is excluded at
\(t=2\): its norm is \(2j+5\), so its displacement is
\(2j+3>2\lceil k/3\rceil\). The latter is the radius
of \((-3)^{-1}\) modulo \(6j+5\). Finally
\(m_n(a)+m_n(-a)=k\) fixes the sign for all but the tiny
\(n=5\) case. Thus any new equality example at an odd
modulus coprime to 3 and at least 23 would have **odd radius
\(r\ge5\)**. Item 71 excludes those radii uniformly.

This note's divisible-by-3 classification is finite evidence,
not a proof. Publication priority for the overlap theorem and
equality problem has not been established.
