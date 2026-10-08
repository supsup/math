# Every equality case in the half-interval overlap theorem

Let \(n=2k+1\ge5\) be odd, \(H=\{1,\ldots,k\}\) in
\(\mathbb Z/n\mathbb Z\), and \(a\) a unit other than \(\pm1\).
The lower bound \(m(a)=|H\cap aH|\ge\lceil k/3\rceil\)
is [item 68](68_half_interval_overlap_all_large_primes.md).

**Complete equality classification.** Equality holds exactly in
these cases:

* If \(3\nmid n\), then \(a=-3\) or \(a=(-3)^{-1}\),
  except that \(n=11\) also permits \(a=2,6\) and
  \(n=17\) also permits \(a=10,12\).
* If \(3\mid n\), the full list is
  \((n,a)=(9,2),(9,4),(9,5),(9,7),
  (15,2),(15,4),(15,8),(21,4),(21,16),
  (27,16),(27,22)\).

The first bullet is proved in
[item 71](71_half_interval_equality_classification.md).
This note proves that no multiple of three beyond \(27\)
attains equality, closing the finite pattern in
[item 70](70_half_interval_equality_patterns.md).

## Even radial multipliers at a multiple of three

Write \(n=6j+3\), \(k=3j+1\), and suppose
\(m(a)=j+1\). The symmetric-difference argument of item 68
gives \(M\le2j+2\), where

    M=max_{1≤t≤k}| ||at||−t |,    r=||a||.

For even \(r\), sampling \(t=1,k\) gives
\(r-1\le2j+2\) and \(k-r/2\le2j+2\).
Thus

    r ∈ {2j−2, 2j, 2j+2}.                          (1)

At \(r=2j-2\), the \(t=2\) displacement exceeds
\(2j+2\) for every \(j\ge5\): when \(j=5\),
\(\|2r\|=16\) and the displacement is 14 versus 12;
when \(j\ge6\), \(\|2r\|=2j+7\) and the
displacement is \(2j+5\). So this radius is impossible
in the large range.

The other two radii can be counted directly. Put
\(h=2j+1\), so \(n=3h\), and write \(x=3q+s\)
with \(s\in\{0,1,2\}\). For \(r=h-1=2j\),
one has \(rx\equiv sh-x\pmod n\). The overlap
therefore includes exactly the \(x\equiv1\pmod3\)
with \(1\le x<2j+1\), and the \(x\equiv2\pmod3\)
with \(j+1\le x\le3j+1\). It follows that

    j+2 ≤ floor((2j+2)/3)+floor((2j+1)/3) ≤ m(r)
         ≤ ceil(2j/3)+ceil((2j+1)/3)
         ≤ (4j+5)/3 < 2j.                            (2)

for \(j\ge11\). The lower bound uses the minimum
number of residue-2 values in an interval of length
\(2j+1\); the upper bound uses the maximum. Since
\(m(-r)=k-m(r)\), (2) places **both signs** strictly
above the target \(j+1\).

For \(r=h+1=2j+2\), one has
\(rx\equiv sh+x\pmod n\). All \(j\) multiples
of three in \(H\) remain in \(H\), as do \(x=1,4\)
when \(j\ge4\). The counted values besides the multiples
of three are
\(x\equiv1\pmod3\) with \(1\le x\le j\) and
\(x\equiv2\pmod3\) with \(h<x\le k\), each in
an interval of length \(j\). Thus, for \(j\ge11\),

    j+2 ≤ m(r) ≤ j+2ceil(j/3) ≤ (5j+4)/3 < 2j.    (3)

Again \(m(-r)=k-m(r)>j+1\), so neither sign
attains equality.

## Odd radial multipliers

Assume now \(r\ge5\) odd and \(j\ge11\).
At \(t=1\), \(M\le2j+2\) gives \(r\le2j+3\).
At \(t=k-1\), the exact identity from item 71 is

    ||r(k−1)||=|n−3r|/2.

If \(r=2j+3\), this norm is 3, so its
displacement \(3j-3>2j+2\), impossible.
The value \(r=2j+1=n/3\) is not a unit.
Thus \(r\le2j-1\), where \(n-3r>0\).
The same \(t=k-1\) constraint gives
\(3r\le4j+7\). Since \(j\ge11\),

    r≤(4j+7)/3≤(3j+1)/2=k/2.

Write \(k=rq+s\), \(0\le s<r\); then \(q\ge2\).
The \(t=q,q+1\) samples in item 68 give

    3M−2k ≥ (r−3)q−2s       if 2s≤r,
    3M−2k ≥ (r−3)q+4s−3r   if 2s>r.            (4)

Equality would require \(3M-2k\le4\).
For \(r\ge11\), the bounds in (4) are at least
\(r-5\ge6\) and \(r-4\ge7\).
For \(r=9\), \(q\ge3\), giving at least 10 and 11;
for \(r=7\), \(q\ge4\), giving at least 10 and 11;
for \(r=5\), \(q\ge6\), giving at least 8 and 9.
Every possibility contradicts equality.

The remaining multiples of three have \(j\le10\),
so \(n\le63\). Direct evaluation of
\(|H\cap aH|\) for their units yields precisely the
eleven pairs in the theorem. The
[direct-set checker](70_half_interval_equality_small_crosscheck.py)
covers every odd modulus through \(501\), and the
[floor-sum census](70_half_interval_equality_scan.cpp)
reproduces the list through \(10{,}000\).
The long census is evidence; the proof only needs
the small \(n\le63\) check.

Publication priority for the complete equality theorem
has not been established.
