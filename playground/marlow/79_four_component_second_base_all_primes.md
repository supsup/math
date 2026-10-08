# Three simultaneous page trades at the second odd base, p ≡ 9 (mod 16)

Let \(d(G)\) be the minimum number of simple cycles and singleton edges
partitioning \(E(G)\). For **every prime** \(p\equiv9\pmod{16}\),

\[
d(K_{p,p+4})=\frac{3p+11}{2}.
\]

The [\(p\)-leaf offset block](10_odd_hub_blocks.md) gives the corresponding
sharp value at \(t=p+4+rp\), \(r\ge0\). This is a **second-base and offset**
result, not an all-residue theorem. It extends the double-growth page
construction of [item 58](58_skew_second_base_one_trade.md) from two page
components to four. The finite part is a reproducible computational proof;
publication priority has not been investigated.

## The page rectangle and tree criterion

Write \(p-1=8q\), \(q\) odd. Choose a primitive root \(g\) and set
\(a=g^4\), of order \(2q\), and

\[
\beta=(1+a)/2,\quad\gamma=\beta/a,\quad
\delta=(1-a)/(1+a)\quad\text{in }\mathbb F_p.
\]

Grow the antipodal pages centered at 1 and 2 in the affine square before
repairing either page. Each page has four components, indexed at hub \(h\)
by \(\lambda_c(h)=\operatorname{ind}_g(h-c)\bmod4\). As in item 58, the
pages share exactly one hub edge, with hubs
\((a+2)/(a+1)\) and \((2a+1)/(a+1)\). Only the two page-2 spokes on this
edge have their old leaf labels changed by the first growth move.

For \(v\in\mathbb F_p\), set

\[
u=v+\delta,\qquad x=1+\beta(u-1),\qquad y=1+\gamma(v-1).
\]

The identities \(x=2+\beta(v-2)\) and \(y=2+\gamma(u-2)\) give page-1
spokes \((u,x),(v,y)\) and crossed page-2 spokes \((u,y),(v,x)\). Exclude
parameters whose hubs meet the shared edge (at most four values) or have
\(x=y\) (at most one). For a remaining parameter, exchanging the two
spoke pairs preserves the full edge partition. If three such rectangles
have pairwise disjoint hub sets and their component-pair edges form a
spanning tree in **each** of the two four-vertex page quotients, each trade
joins two current cycles in each page. The pages both become single cycles.

## Analytic existence above 300,000

Let \(\psi(g)=i\) be the quartic character. For \(j=1,2,3\), seek a
parameter with four hub-component labels

\[
(\lambda_1(u),\lambda_1(v),\lambda_2(u),\lambda_2(v))=(0,j,0,j).
\]

These three rectangles give the star \(0\!-!1,0\!-!2,0\!-!3\) in both
quotient graphs. Their four label arguments are the affine forms
\(u-1,v-1,u-2,v-2\). The four roots are distinct since
\(\delta\notin\{0,1,-1\}\).

For any prescribed vector of four nonzero quartic labels, orthogonality
of \(\psi\) on the domain excluding these roots gives a count \(N\).
For a nontrivial character monomial supported on \(r\) forms, the
polynomial has \(r\) distinct roots with exponents 1, 2, or 3 and is not a
fourth power. The [arbitrary-order polynomial character-sum bound of
Weil, stated as Theorem 3.7 by Babai–Gál–Wigderson](https://people.cs.uchicago.edu/~laci/papers/span1.pdf),
gives \((r-1)\sqrt p\) for its complete sum. Omitting the other roots
costs at most \(4-r\). There are \(\binom4r3^r\) such monomials, and

\[
\sum_{r=1}^4\binom4r3^r(r-1)=513,\qquad
\sum_{r=1}^4\binom4r3^r(4-r)=252.
\]

The trivial term is \(p-4\), so

\[
N\ge\frac{p-4-513\sqrt p-252}{256}
 =\frac{p-256-513\sqrt p}{256}>13\qquad(p\ge300{,}000).
\]

The bound increases from this threshold onward. At most five candidate
parameters per pattern violate the shared-edge or \(x=y\) exclusions.
Each previously chosen rectangle excludes at most four further
parameters by hub reuse. Thus the three patterns can be chosen in turn,
even for the third after at most \(5+4+4=13\) exclusions. This proves
existence for every eligible prime at least 300,000. The squarefree-order
hypothesis of the Cohen–Sharma–Sharma lemma used in item 58 does **not**
cover the quartic character here; the arbitrary-order theorem above does.

## Finite certificate and graph replays

The [C++ scanner](79_four_component_second_base_finite_scan.cpp) found
three hub-disjoint, double-tree line rectangles for **all 6,123** primes
\(p\equiv9\pmod{16}\) below 600,000. The
[witness table](79_four_component_second_base_witnesses.csv) records
\((p,g,a,v_1,v_2,v_3)\) for each prime; its SHA-256 is
`8eb56b00491c41f02c2f6e11cd08c74c5f0e38ac4099d6cb6c733b1fca7795e8`.
The scanner keeps the first nine candidates for each of 36 quotient-edge
pair types. That cap is complete for a three-rectangle search: the three
tree edges necessarily have distinct types, and at most eight candidates
of a chosen type can conflict with two earlier hub pairs.

The [independent witness audit](79_four_component_second_base_witness_audit.py)
rechecks every row's primality, primitive root, affine spoke identities,
exclusions, hub disjointness, and both spanning trees. A separate
[Python finite scan](79_four_component_second_base_independent_scan.py)
covers all 3,230 eligible primes below 300,000 with a different search
order, testing at most 80 line parameters per prime; it finds zero misses
and FNV-1a digest `cc4e987155c509d5` over its ordered 32-bit
\((p,g,v_1,v_2,v_3)\) words. The
[full partition replay](79_four_component_second_base_partition_replay.py)
checks the square, both growth moves, each of the three component merges,
and exact spoke coverage at \(p=41,73,89,137,233\).

From the two repaired pages, there are \(p+4\) singleton spokes,
\((p-1)/2\) full cycles, and two short cycles: \((3p+11)/2\) parts.
The odd-hub parity and cycle-capacity lower bound is
\(p+4+\lceil((p-1)/2)(p+4)/p\rceil=(3p+11)/2\), proving equality.

Reproduce from the repository root:

```sh
c++ -O3 -std=c++17 -Wall -Wextra -Werror playground/marlow/79_four_component_second_base_finite_scan.cpp -o /tmp/marlow79_scan
/tmp/marlow79_scan 600000 /tmp/marlow79_witnesses.csv
shasum -a 256 /tmp/marlow79_witnesses.csv playground/marlow/79_four_component_second_base_witnesses.csv
python3 playground/marlow/79_four_component_second_base_witness_audit.py
python3 playground/marlow/79_four_component_second_base_independent_scan.py
python3 playground/marlow/79_four_component_second_base_partition_replay.py
```
