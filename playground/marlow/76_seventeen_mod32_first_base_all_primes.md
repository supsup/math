# The first odd base for every prime hub seventeen modulo thirty-two

Let \(d(G)\) be the minimum number of simple cycles and singleton
edges partitioning \(E(G)\).

**Computer-assisted first-base theorem.** For every prime
\(p\equiv17\pmod{32}\),

\[
d(K_{p,p+2})
 =p+2+\left\lceil\frac{(p-1)(p+2)}{2p}\right\rceil
 =\frac{3p+5}{2}.
\]

The [\(p\)-leaf offset block](10_odd_hub_blocks.md) gives
\(d(K_{p,p+2+rp})=(p+2+rp)+\lceil((p-1)/2)(p+2+rp)/p\rceil\)
for every integer \(r\ge0\). Other leaf residues modulo \(p\)
are not settled here. Publication priority has not been established.

Write \(p-1=16q\), with \(q\) odd, so item 73's parameter is
\(A=8\). The six primes in this class with \(q\le36\) are
\(17,113,241,337,401,433\). [Item 31](31_seventeen_hub_all_residues.md)
gives the full fixed-hub formula at 17, while
[item 62](62_one_mod8_first_base.md) certifies the first base at 113.
The [four saved certificates](76_seventeen_mod32_small_certificates.py)
cover the other four: they use seven scaled two-trade gadgets to join
the eight starter-page components. The replay rebuilds
the square and page, checks each source and target spoke, preserves
cycle connectivity after every trade, and verifies all
\(p(p+2)\) spokes exactly once. The witnesses are:

| \(p\) | primitive \(g\) | seven scales | quotient-tree edges | spokes / parts |
| ---: | ---: | --- | --- | ---: |
| 241 | 7 | 2, 5, 13, 35, 1, 4, 19 | (0,5), (1,4), (1,6), (2,5), (2,7), (3,6), (4,7) | 58,563 / 364 |
| 337 | 10 | 5, 19, 3, 7, 11, 35, 2 | (0,5), (1,4), (1,6), (2,5), (2,7), (3,6), (4,7) | 114,243 / 508 |
| 401 | 3 | 7, 1, 15, 2, 19, 4, 38 | (0,7), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7) | 161,603 / 604 |
| 433 | 94 | 8, 2, 10, 14, 4, 1, 7 | (0,5), (1,4), (1,6), (2,5), (2,7), (3,6), (4,7) | 188,355 / 652 |

For \(q>36\) and \(p-1\le262{,}144{,}000\), an exact
[segmented finite sweep](76_seventeen_mod32_first_base_finite_sweep.cpp)
finds a primitive root \(g\) satisfying item 55's algebraic
two-trade test at every eligible prime. It sieves one-megabyte
blocks, factors \(p-1\) by trial primes, and checks both the
factored exclusions and the original \(Z,W\), character and
midpoint conditions at each accepted witness. There are 894,227
eligible primes, from \(p=593\) through \(262{,}143{,}793\),
and no failures. The greatest least witness is \(g=181\);
at most 20 primitive roots were tested for one prime.
An [independent full-range audit](76_seventeen_mod32_first_base_independent_audit.cpp)
uses a bit-packed sieve and separate direct-condition logic.
Both return the same FNV-1a 64-bit digest of the ordered
little-endian \((p,g)\) witness pairs:

```text
b584f964dd718afc
```

Here \(q>36=6(A-2)\), so the [scaled-gadget tree lemma](73_one_mod8_scaled_gadget_tree.md)
turns every passing test into an optimal partition. For
\(p-1>262{,}144{,}000=(80A)^3\), the
[analytic first-base tail](74_one_mod8_first_base_analytic_tail.md)
supplies both the parameter and the packing. The small cases,
finite sweep, and analytic tail exhaust \(p\equiv17\pmod{32}\).
The known odd-hub parity and cycle-capacity lower bound is recorded
in [Bucić–Montgomery, Section 6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf).

Reproduce the finite and small certificates from the repository root:

```sh
c++ -O3 -std=c++17 -Wall -Wextra -Werror playground/marlow/76_seventeen_mod32_first_base_finite_sweep.cpp -o /tmp/marlow76_sweep
/tmp/marlow76_sweep
c++ -O3 -std=c++17 -Wall -Wextra -Werror playground/marlow/76_seventeen_mod32_first_base_independent_audit.cpp -o /tmp/marlow76_audit
/tmp/marlow76_audit
python3 -I playground/marlow/76_seventeen_mod32_small_certificates.py --verify-four
```

The full-spoke replays are finite certificates at four hubs; the
large sweep checks the sufficient local test rather than explicitly
materializing nearly a million full graph partitions. Item 73 supplies
the uniform structural implication from that test to the partition.
