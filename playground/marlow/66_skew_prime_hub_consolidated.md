# A consolidated residue range for prime hubs 5 modulo 8

Write \(d(K_{p,t})\) for the fewest simple cycles and singleton edges in
an edge partition, and put \(k=(p-1)/2\). The following gathers the
separate constructions in items 10, 24, 57, 58, 60, and 64 into one
statement. It is a **partial residue theorem** that begins at \(p=53\).
The later [half-interval overlap theorem](68_half_interval_overlap_all_large_primes.md)
strengthens this to **every residue** for every such prime \(p\ge60{,}000{,}000\).
The [finite criterion scan](69_skew_prime_hub_all_residues.md)
then covers all smaller eligible primes, yielding the full class
formula with a computational component.

**Theorem.** Let \(p\ge53\) be prime with \(p\equiv5\pmod8\). Set

\[
J_p=\{j\in\mathbb Z:0\le j\le (p-3)/2,\quad
                 8j<p-3\sqrt p+10\},
\]

and define the exact set of covered base leaf counts

\[
B_p=\{p-1,p+1,p+3,\ldots,2p-2\}
       \;\cup\;\{p+2j:j\in J_p\}.
\]

Then, for every \(b\in B_p\) and integer \(q\ge0\),

\[
d(K_{p,b+pq})=(b+pq)+\left\lceil\frac{k(b+pq)}p\right\rceil.
\]

The first set in \(B_p\) is **every even base** from \(p-1\) through
\(2p-2\); the second is an initial run of odd bases. For example,
\(J_{53}=\{0,1,2,3,4,5\}\), so the theorem covers every even base
and the odd bases \(53,55,57,59,61,63\), with all their 53-leaf
offsets. Other odd residues below the large-prime threshold are not claimed by this partial theorem;
the [fixed 53-hub certificate](63_fiftythree_hub_all_residues.md)
covers them at that particular prime.

| Base family | Proof source | Construction |
|:--|:--|:--|
| Even \(b=p-1,p+1,\ldots,2p-2\) | [Item 24](24_even_base_residues.md) | Explicit even-hub cycle weave after one singleton per leaf |
| \(b=p\), \(j=0\) | [Item 10](10_odd_hub_blocks.md) | Diagonal singletons and offset Hamilton cycles |
| \(j=1\) | [Item 57](57_skew_first_base_all_prime_hubs.md), using [item 55](55_skew_two_trade_first_step.md) | One antipodal page, two trades; choose a suitable primitive root |
| \(j=2\) | [Item 58](58_skew_second_base_one_trade.md) | Two antipodal pages, one page-page trade |
| \(j=3\) | [Item 64](64_skew_third_base_two_trades.md) | Three antipodal pages, two page-page trades |
| Even \(j=2r\ge4\) in \(J_p\) | [Item 60](60_skew_adjacent_pairs.md) | Pair adjacent pages in order, one trade per pair |
| Odd \(j=2r+1\ge5\) in \(J_p\) | [Item 64](64_skew_third_base_two_trades.md) | Repair the first three pages, then pair adjacent later pages |
| Offset \(q\ge0\) | [Item 10](10_odd_hub_blocks.md) | Append disjoint \(p\)-leaf affine square blocks |

The lower bound \(d(K_{p,t})\ge t+\lceil kt/p\rceil\) comes from the odd
degree at each leaf and the maximum \(p\) leaf appearances in a simple
cycle, as recorded in [item 24](24_even_base_residues.md). For an odd
base \(b=p+2j\), this ceiling equals \(k+j\); each cited construction
has \(b\) singleton spokes and \(k+j\) cycles. The even-base counts
are checked in item 24. Appending one \(p\)-leaf block raises both
sides by exactly \(p+k\). The choices of primitive root or trades
may differ between bases; the theorem asserts a partition separately
for each covered \(t\), rather than one nested sequence of partitions.

## One arithmetic appendix for the class statement

The first odd base has a different repair mechanism from all later
ones. Item 55 gives a two-trade criterion on a primitive root \(g\).
Item 57 counts primitive roots passing its quadratic-character test:
the primitive-element indicator and a five-root character-sum bound
give a witness for \(p-1\ge10^7\); its exact [C++ sweep](57_skew_first_base_finite_sweep.cpp)
checks the remaining 166,202 eligible primes \(p\ge29\). The full
eight algebraic exclusions and the count are stated in item 57. This
is the only part of the theorem that must choose a special primitive
root. The paper source for the character-sum lemma is
[Cohen–Sharma–Sharma 2019, Lemma 2.1](https://arxiv.org/pdf/1909.13074).

For all later page-page trades, **any** primitive root works in the
proved range. Put \(a=g^2\), \(\delta=(1-a)/(1+a)\), and let \(\chi\)
be the quadratic character of \(\mathbb F_p\). The two component
tests on the rectangle parameter \(w\) are

\[
F_1(w)=w(w+\delta),\qquad
F_2(w)=(w-1)(w+\delta-1).
\]

The two quadratic sums are \(-1\), and the four-root squarefree
quartic sum has absolute value at most \(3\sqrt p\). Accounting for
the four roots gives these supply bounds, proved in items 60 and 64:

\[
N_{--}\ge(p-3\sqrt p-6)/4,\qquad
N_{+-}\ge(p-3\sqrt p-8)/4.
\]

For consecutive centers, the exact relabel exceptions are two
arithmetic progressions. After removing three parameters already
character-ineligible, at most \(2c-2\) good parameters are lost for
a pair starting at center \(c\ge2\). The exception sets are nested,
so only the last pair matters. At an even prefix \(j=2r\), its start
is \(c=2r-1\) and the sufficient inequality is
\(16r<p-3\sqrt p+10\). At an odd prefix \(j=2r+1\ge5\), its last
paired start is \(c=2r\) and the inequality is
\(16r<p-3\sqrt p+2\). **Both are exactly**
\(8j<p-3\sqrt p+10\). The first three pages are handled by item
64: its \((+,-)\) character supply exceeds the four possible
second-trade exceptions for every \(p\ge53\).

The [full-partition checker](60_skew_adjacent_pairs_full_replay.py)
and [odd-prefix checker](64_skew_odd_prefix_replay.py) replay sample
graphs. The [even-prefix counting scan](60_skew_adjacent_pairs_final_scan.cpp)
checks all 19,622 class primes through one million; an independently
audited [fast existence scan](60_skew_adjacent_pairs_fast_existence_scan.cpp)
checks all 166,203 through ten million. The
[odd-prefix criterion scan](64_skew_odd_prefix_criterion_scan.py)
checks all 42 through 1000. These bounded scans find witnesses
outside this note's initial analytic range at the tested primes. Item 68
supplies a separate uniform proof of all residues for \(p\ge60{,}000{,}000\);
item 69's exact finite criterion scan covers the remaining primes.
