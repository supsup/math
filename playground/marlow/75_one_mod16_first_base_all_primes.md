# The first odd base for every prime hub nine modulo sixteen

Let \(d(G)\) be the minimum number of simple cycles and singleton
edges partitioning \(E(G)\).

**Computer-assisted first-base theorem.** For every prime
\(p\equiv9\pmod{16}\),

\[
d(K_{p,p+2})
 =p+2+\left\lceil\frac{(p-1)(p+2)}{2p}\right\rceil
 =\frac{3p+5}{2}.
\]

The \(p\)-leaf offset block of [item 10](10_odd_hub_blocks.md)
then gives
\(d(K_{p,p+2+rp})=(p+2+rp)+\lceil((p-1)/2)(p+2+rp)/p\rceil\)
for every integer \(r\ge0\). Other leaf residues modulo \(p\)
are not covered. Publication priority has not been established.

The proof uses three disjoint ranges. Write \(p-1=8q\), where \(q\)
is odd. The only primes in this congruence class with \(q\le12\)
are \(p=41,73,89\); [item 62](62_one_mod8_first_base.md)
already gives complete first-base partition certificates for them.
For \(q>12\) and \(p-1\le32{,}768{,}000\), the exact finite sweep
below finds a primitive root passing item 55's local two-trade test.
The [scaled-gadget tree lemma](73_one_mod8_scaled_gadget_tree.md)
packs its copies because here \(A=4\) and \(q>6(A-2)=12\).
For \(p-1>32{,}768{,}000=(80A)^3\), the
[analytic tail](74_one_mod8_first_base_analytic_tail.md) supplies
the same suitable root and packing. These cases exhaust every
prime \(p\equiv9\pmod{16}\). The parity and maximum-cycle-length
lower bound is the odd-hub bipartite example described in
[Bucić–Montgomery, Section 6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf).

## The finite certificate

The [finite scanner](75_one_mod16_first_base_finite_sweep.cpp)
sieves smallest prime factors through \(32{,}768{,}001\). For each
prime \(p\equiv9\pmod{16}\) with \(q>12\) in that range, it
factors \(p-1\), tests \(g=2,3,\ldots\) for primitivity by
\(g^{(p-1)/r}\ne1\pmod p\) for every prime \(r\mid p-1\), and
sets \(a=g^4\). It checks the six quadratic slot exclusions
factored in [item 57](57_skew_first_base_all_prime_hubs.md), as
well as the two linear exclusions and
\(\chi((a+3)(1+3a))=-1\). It also evaluates the original
\(Z,W\), character ratio, and all twelve midpoint comparisons
from [item 55](55_skew_two_trade_first_step.md) for every primitive
root tested, asserting that the direct and factored decisions
agree. Its output is:

```text
n_limit=32768000 first_p=137 last_p=32767577 primes=252249 covered=252249 missing=0 max_first_g=156 max_primitive_tests=20 hardest_p=16032473 max_candidate_g_tests=155 max_candidates_p=20150761 fnv1a64_p_g_le=982e0a5222b044a0
```

The [independent audit](75_one_mod16_first_base_independent_audit.cpp)
uses a separate prime sieve and trial-factorization loop, evaluates
only the original \(Z,W\) and midpoint conditions, and finds the
same least successful \(g\) at every prime. Both programs hash the
little-endian 32-bit words \((p,g)\) with FNV-1a 64-bit; the identical
digest covers all \(252{,}249\) ordered pairs. The independent output
is:

```text
limit=32768001 primes=252249 max_g=156 max_g_p=20150761 max_generators_tested=20 hardest=16032473 fnv1a64_p_g_le=982e0a5222b044a0 failures=
```

Reproduce with a C++17 compiler from the repository root:

```sh
c++ -O3 -std=c++17 -Wall -Wextra -Werror playground/marlow/75_one_mod16_first_base_finite_sweep.cpp -o /tmp/marlow75_sweep
/tmp/marlow75_sweep
c++ -O3 -std=c++17 -Wall -Wextra -Werror playground/marlow/75_one_mod16_first_base_independent_audit.cpp -o /tmp/marlow75_audit
/tmp/marlow75_audit
```

This finite computation verifies only the stated sufficient local
test, not a separately materialized full edge partition at every
prime. The structural lemma turns that test into a construction;
the [\(p=73\) full-spoke replay](73_one_mod8_scaled_gadget_p73_audit.py)
checks the scaled-tree mechanism on a concrete complete partition.
