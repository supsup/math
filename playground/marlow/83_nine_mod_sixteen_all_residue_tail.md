# Every leaf residue for large prime hubs nine modulo sixteen

**Analytic prime-class tail.** If \(p\ge10^{14}\) is prime
with \(p\equiv9\pmod{16}\), then for every integer \(t\ge p-1\),

\[
d(K_{p,t})=t+\left\lceil\frac{(p-1)t}{2p}\right\rceil.
\]

The lower bound is the standard odd-hub parity and cycle-capacity
argument: each of the \(t\) degree-\(p\) leaves requires a singleton
edge, and a simple cycle uses at most \(2p\) edges. The constructions
below attain it. The \(10^{14}\) cutoff is deliberately conservative;
this note does **not** assert the formula for every prime in this
congruence class or for other one-mod-eight prime classes. Publication
priority has not been investigated.

Write \(k=(p-1)/2\). Every \(t\ge p-1\) is obtained from one base
\(b\in[p-1,2p-2]\) by adding nonnegative multiples of \(p\). The
[\(p\)-leaf offset block](10_odd_hub_blocks.md) preserves equality,
so it suffices to cover that base interval.

* [Item 24](24_even_base_residues.md) supplies every even base.
* The affine midpoint square supplies \(b=p\). [Item 75](75_one_mod16_first_base_all_primes.md)
  supplies the first odd base \(b=p+2\) for every prime in this class.
* [Item 81](81_four_component_third_base_all_primes.md) supplies the
  three-page base \(b=p+6\) for every prime in this class.
* [Item 82](82_four_component_late_pair_fourier_tail.md) proves that
  one triple of hub-disjoint four-component rectangle trades survives
  every adjacent page pair at all eligible \(p\ge10^{14}\).
  For even page-growth counts \(j\ge2\), pair the pages
  \((1,2),(3,4),\ldots,(j-1,j)\). For odd \(j\ge3\), first use
  item 81's repair of pages \(1,2,3\), then pair
  \((4,5),(6,7),\ldots,(j-1,j)\). A page trade does not alter a
  square-color slot, so these repairs remain compatible with later
  growth. The nested relabel-exception sets in item 82 guarantee the
  same witness parameters at every pair start.

For \(p\equiv9\pmod{16}\), \(k\) is even. The allowed growth counts
\(0\le j\le k-1=(p-3)/2\) give every odd base
\(b=p+2j\) from \(p\) through \(2p-3\). Together with the even
bases, these are all bases in \([p-1,2p-2]\). At each odd base,
the repaired partition has \(p+2j\) singleton spokes,
\(k\) full Hamilton cycles, and \(j\) short cycles:

\[
d(K_{p,p+2j})=p+2j+k+j
             =p+2j+\left\lceil\frac{k(p+2j)}p\right\rceil,
\]

because \(j<p\). The even-base count is established in item 24.
This proves the formula at every base and hence at every larger
leaf count.

This tail uses the analytic portions of items 75 and 81, whose
thresholds are much smaller than \(10^{14}\), plus item 82's
analytic final-pair bound. The finite-prime scans in those notes
extend their individual base theorems downward but are not needed
for the formula stated here. The
[combined full-spoke replay](83_nine_mod_sixteen_odd_prefix_replay.py)
checks the stitching of item 81 and later page pairs at the maximal
odd prefixes for \(p=41\) and \(73\); these are structural sanity
checks, not assumptions of the large-prime proof.

Run the combined checker from the repository root with
`python3 playground/marlow/83_nine_mod_sixteen_odd_prefix_replay.py`.
