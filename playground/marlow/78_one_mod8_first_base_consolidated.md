# Current first-base reach for prime hubs one modulo eight

Let \(d(G)\) be the minimum number of simple cycles and singleton
edges partitioning \(E(G)\). For a prime \(p\equiv1\pmod8\), write

\[
n=p-1=2Aq,\qquad A=2^{v_2(n)-1}\ge4,\qquad q\text{ odd}.
\]

The results in items 73–77 give the following **bounded first-base
statement**. In every case listed below,

\[
d(K_{p,p+2})=\frac{3p+5}{2},
\]

and the [\(p\)-leaf offset block](10_odd_hub_blocks.md) gives the
corresponding sharp formula at \(t=p+2+rp\) for every \(r\ge0\).

1. **Analytic tail for every dyadic class:**
   \(n>(80A)^3\), by [item 74](74_one_mod8_first_base_analytic_tail.md).
2. **Finite greedy range:** \(p\le32{,}768{,}001\) and
   \(q>6(A-2)\), by the exact double sweep below and
   [item 73's packing lemma](73_one_mod8_scaled_gadget_tree.md).
3. **Two complete congruence classes:** every
   \(p\equiv9\pmod{16}\) by [item 75](75_one_mod16_first_base_all_primes.md),
   and every \(p\equiv17\pmod{32}\) by
   [item 76](76_seventeen_mod32_first_base_all_primes.md).
   These combine small full-spoke certificates, larger finite sweeps,
   and the analytic tail.
4. **Additional fixed hub:** \(p=353\), whose
   [direct 19-trade certificate](77_p353_first_base_direct_repair.md)
   works even though the item 73 local character test fails for every
   primitive-root parameter at this prime. Earlier fixed-hub notes
   also cover particular primes outside the two complete classes.

This is a statement about the first odd base and its \(p\)-leaf
offsets. It does **not** prove the formula at every leaf residue for
any of these prime classes. It also does **not** produce a uniform
threshold \(p\ge P_0\) for all primes \(p\equiv1\pmod8\): the
analytic threshold depends on \(A\), and the starter template can
fail when \(q\) is small. Publication priority is undetermined.

## The general finite greedy range

The [factorized scanner](78_one_mod8_greedy_range_sweep.cpp) uses a
smallest-prime-factor sieve through \(32{,}768{,}001\). For each
prime \(p\equiv1\pmod8\) in that range with \(q>6(A-2)\), it
tests primitive roots in increasing order and accepts the first
\(g\) for which \(a=g^A\) passes the two linear, six quadratic,
and one character test from item 55. It found no misses among
\(502{,}486\) eligible primes:

| \(A\) | eligible primes | largest least \(g\) |
| ---: | ---: | ---: |
| 4 | 252,249 | 156 |
| 8 | 126,085 | 157 |
| 16 | 62,997 | 167 |
| 32 | 31,502 | 158 |
| 64 | 15,752 | 139 |
| 128 | 7,744 | 97 |
| 256 | 3,820 | 111 |
| 512 | 1,773 | 107 |
| 1,024 | 564 | 95 |

The [independent audit](78_one_mod8_greedy_range_independent_audit.cpp)
uses a separate prime sieve, trial factorization, and the original
modular \(Z,W\) and midpoint comparisons. It also finds no misses
and agrees on the first witness at every prime. Both hash the ordered
little-endian 32-bit \((p,g)\) words with FNV-1a 64-bit and obtain
\(\texttt{77fc310895aa6df3}\). The maximum number of primitive
roots tested at one prime is 20, at \(p=16{,}032{,}473\).

Reproduce from the repository root:

```sh
c++ -O3 -std=c++17 -Wall -Wextra -Werror playground/marlow/78_one_mod8_greedy_range_sweep.cpp -o /tmp/marlow78_sweep
/tmp/marlow78_sweep
c++ -O3 -std=c++17 -Wall -Wextra -Werror playground/marlow/78_one_mod8_greedy_range_independent_audit.cpp -o /tmp/marlow78_audit
/tmp/marlow78_audit
```

The computation certifies the local sufficient test, not a separately
materialized graph partition at each of the half-million primes.
Items 53, 55, and 73 supply the structural construction, and
[item 73's \(p=73\) replay](73_one_mod8_scaled_gadget_p73_audit.py)
checks a complete scaled-tree partition. The odd-hub lower bound is
the parity and cycle-capacity mechanism recorded in
[Bucić–Montgomery, Section 6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf).

The first uncovered dyadic class is \(A=16\), namely
\(p\equiv33\pmod{64}\), at small \(q\) and in the intermediate
range between this finite sweep and item 74's \(A\)-dependent tail.
The \(p=353\) direct repair shows that failure of this local test
does not imply failure of the graph formula.
