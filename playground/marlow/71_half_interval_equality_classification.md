# Exact equality cases for half intervals away from three

Let \(n=2k+1\ge5\) be odd, let \(H=\{1,\ldots,k\}\) in
\(\mathbb Z/n\mathbb Z\), and put \(m(a)=|H\cap aH|\) for a unit
\(a\ne\pm1\).

**Equality theorem.** If \(3\nmid n\), then
\(m(a)=\lceil k/3\rceil\) exactly when

1. \(a\equiv-3\pmod n\) or \(a\equiv(-3)^{-1}\pmod n\); or
2. \((n,a)\) is one of \((11,2),(11,6),(17,10),(17,12)\).

The lower bound is [item 68](68_half_interval_overlap_all_large_primes.md).
For \(a=-3\), it also gives the exact count
\(\lfloor2k/3\rfloor-\lfloor k/3\rfloor=\lceil k/3\rceil\)
when \(3\nmid n\). Multiplying an intersection by \(a^{-1}\)
shows \(m(a)=m(a^{-1})\), so both named multipliers attain equality.
Also \(aH\) and \(-aH\) partition the nonzero residues, whence

    m(a)+m(-a)=k.                                      (1)

For \(n\ge7\) with \(3\nmid n\), \(\lceil k/3\rceil<k/2\);
thus (1) fixes the sign
once the radial value \(r=\|a\|\) is known. The \(n=5\) case has
both named multipliers and is checked directly.

## The radial constraints

Write

    M=max_{1≤t≤k} | ||at||−t |.

The symmetric-difference argument in item 68 gives
\(M\le2m(a)\). Its evaluations at \(t=1,k\) show the following
when \(r=\|a\|\) is even:

* If \(k=3j\), equality forces \(r=2j\), the radius of
  \((-3)^{-1}\) modulo \(6j+1\).
* If \(k=3j+2\), equality leaves \(r=2j\) or \(2j+2\).
  For \(j\ge3\), the first candidate has
  \(\|2r\|=2j+5\), so its displacement at \(t=2\) is
  \(2j+3>2\lceil k/3\rceil\). The remaining radius
  \(2j+2\) belongs to \((-3)^{-1}\) modulo \(6j+5\).

At odd radius \(r=3\), (1) selects \(a=-3\). It remains to
exclude odd \(r\ge5\) at all sufficiently large moduli.

For odd \(r\), the value at \(t=k-1\) has the exact norm

    ||r(k−1)||=|n−3r|/2,                              (2)

because \(r(k-1)\equiv(n-3r)/2\pmod n\) and
\(|n-3r|/2<n/2\). Equality gives both \(r-1\le2m(a)\)
from \(t=1\) and

    |n−3r|≥2(k−1−2m(a))                              (3)

from \(t=k-1\).

First let \(k=3j\) with \(j\ge6\), so \(m(a)=j\).
The first inequality yields \(r\le2j+1\). The endpoint
\(r=2j+1\) has norm 1 in (2), hence displacement
\(3j-2>2j\), impossible. For the remaining values
\(n-3r>0\), and (3) gives \(3r\le4j+3\). Since
\((4j+3)/3\le3j/2=k/2\) for \(j\ge6\), we have
\(q=\lfloor k/r\rfloor\ge2\).

Next let \(k=3j+2\) with \(j\ge8\), so \(m(a)=j+1\).
Now \(r\le2j+3\). The endpoint \(r=2j+3\) has norm 2
in (2), hence displacement \(3j-1>2j+2\), impossible.
For the remaining values (3) yields \(3r\le4j+7\).
Since \((4j+7)/3\le(3j+2)/2=k/2\) for \(j\ge8\),
again \(q=\lfloor k/r\rfloor\ge2\).

## The two nearby radial samples finish the large cases

Write \(k=rq+s\), \(0\le s<r\). At \(t=q,q+1\),
item 68 proves

    M≥(r−1)q+max(0,2s−r).

If \(2s\le r\), this gives
\(3M-2k\ge(r-3)q-2s\). If \(2s>r\), it gives
\(3M-2k\ge(r-3)q+4s-3r\).

For \(k=3j\), equality would require \(3M-2k\le0\).
With odd \(r\ge7,q\ge2\), the first lower bound is at
least \(r-5\ge2\), and the second is at least
\(r-4>0\). For \(r=5\), both are positive except
\((q,s)=(2,2)\), where \(k=12,n=25\) and \(r=5\)
is not a unit. Thus no odd \(r\ge5\) remains.

For \(k=3j+2\), equality would require
\(3M-2k\le2\). At \(r\ge9,q\ge2\), the two lower
bounds are at least \(r-5\ge4\) and \(r-4\ge5\).
For \(r=7\), \(k\ge26\) gives \(q\ge3\), and the bounds
are at least 6 and 7. For \(r=5\), \(q\ge5\), and
they are again at least 6 and 7. This contradiction
finishes every large modulus coprime to 3.

The remaining cases are \(n=6j+1\) with \(j<6\) and
\(n=6j+5\) with \(j<8\), hence \(n\le47\).
Directly computing \(m(a)\) for each unit in this
small range leaves only the four extra pairs in the
theorem. The [direct-set checker](70_half_interval_equality_small_crosscheck.py)
recomputes every unit through \(n=501\); the
[floor-sum census](70_half_interval_equality_scan.cpp)
extends the check through 10,000. Neither long scan is
needed for the large-\(n\) proof.

At moduli divisible by 3, \(-3\) is not a unit;
[item 72](72_half_interval_equality_complete.md) proves the
remaining eleven equality cases. Publication priority for
this equality theorem has not been established.
