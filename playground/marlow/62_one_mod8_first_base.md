# Five first-base repairs with more than two starter-page components

The [Mullin–Nemeth antipodal page](53_skew_starter_page.md) has \(A=2^{v_2(p-1)-1}\) components when \(p-1\) has an odd factor greater than one. For primes \(p\equiv1\pmod8\), \(A\ge4\), so the two-component formula from items [55](55_skew_two_trade_first_step.md) and [57](57_skew_first_base_all_prime_hubs.md) does not apply directly. The [saved support-preserving trade traces](62_one_mod8_first_base_traces.json) repair the first odd base \(K_{p,p+2}\) for five selected primes:

| \(p\) | primitive root \(g\) | initial page components \(A\) | trades | optimal parts |
| ---: | ---: | ---: | ---: | ---: |
| 41 | 6 | 4 | 5 | 64 |
| 73 | 13 | 4 | 4 | 112 |
| 89 | 3 | 4 | 6 | 136 |
| 97 | 5 | 16 | 17 | 148 |
| 113 | 3 | 8 | 9 | 172 |

Each starts from the cyclic-difference affine square on \(K_{p,p}\), grows one translated antipodal page at center 1, and then applies the trace. A trace row gives two colors, two spokes in the first color, and their crossed spokes in the second; exchanging the two pairs keeps every hub and leaf support unchanged. Some preparatory trades leave the total component count level before a later trade reduces it. All traces finish with \(p+2\) singleton spokes, \((p-1)/2\) full \(2p\)-edge cycles, and one \(2(p-1)\)-edge page cycle. Hence each listed prime satisfies

\[
d(K_{p,p+2})=p+2+\left\lceil\frac{(p-1)(p+2)}{2p}\right\rceil
=\frac{3p+5}{2}.
\]

The [independent replay](62_one_mod8_first_base_audit.py) reconstructs the starter and square from \(g\), checks every old and new spoke of each trade, verifies support and nonincreasing component totals, and finally checks all \(p(p+2)\) spokes, connected simple cycles, and the optimum part count. The trace JSON is 1,723 bytes with SHA-256 `ab464df3fb9553742fc82ec4eb355072f532cbfc893b1ce85e66d4b0a37cdfff`. The [\(p\)-leaf offset block](10_odd_hub_blocks.md) extends each certificate to \(t=p+2+pq\), \(q\ge0\).

This is finite evidence that multi-component starter pages can be repaired. It does not prove a uniform \(p\equiv1\pmod8\) result or later odd bases. The \(p=41\) equality is already included in the full fixed-hub theorem of [item 52](52_fortyone_hub_all_residues.md); this page gives a different construction.
