# Every leaf residue for prime hubs 5 modulo 8

**Computer-assisted class theorem.** Let \(p\ge13\) be prime with
\(p\equiv5\pmod8\), and let \(t\ge p-1\) be an integer. Then

\[
d(K_{p,t})=t+\left\lceil\frac{(p-1)t}{2p}\right\rceil.
\]

The proof joins the analytic large-prime tail of
[item 68](68_half_interval_overlap_all_large_primes.md) to an exact
finite enumeration below its \(60{,}000{,}000\) threshold. The
enumeration is deterministic and reproducible from the
[C++ source](69_skew_full_residue_finite_scan.cpp). This is a theorem
conditional on the correctness of that finite computation, not a
uniform symbolic proof for the smaller primes.

## The one condition the finite scan checks

For a prime \(p\equiv5\pmod8\), put \(k=(p-1)/2\), choose a
primitive root \(g\), and set in \(\mathbb F_p\)

\[
a=g^2,\quad D=a+1,\quad
\delta=(1-a)D^{-1},\quad c=k-2,\quad
I=\{0,1,\ldots,c\}.
\]

[Item 67](67_skew_late_prefix_geometry.md) identifies the exact exception set for the last odd page
pair. With \(X=Dw-a\), its complement is

\[
B_c=\{w:X\notin -I\cup-aI\}.
\]

The same page pair has the character-good set

\[
G=\{w:\chi(w(w+\delta))=
          \chi((w-1)(w+\delta-1))=-1\}.
\]

The scan asks whether \(G\cap B_c\) is nonempty. For each
eligible prime below 60 million it factors \(p-1\), chooses the
least primitive root by checking \(g^{(p-1)/q}\ne1\) for every
distinct prime factor \(q\mid p-1\), and searches \(w=0,1,2,\ldots\)
until it finds a survivor. The two exception tests are exactly
\(-X\notin I\) and \(-a^{-1}X\notin I\), so no approximate
exception count is used. A binary Jacobi computation screens the
two quadratic characters; Euler's criterion independently checks
both characters at every accepted witness.

The complete run was:

    c++ -O3 -std=c++17 -Wall -Wextra -pedantic \
      playground/marlow/69_skew_full_residue_finite_scan.cpp \
      -o /tmp/marlow_full_scan
    /tmp/marlow_full_scan 59999999

Its final line was:

    PASS limit=59999999 primes=890703 max_g=62 max_examined=457 max_examined_p=53927101 total_examined=9325372 digest=16172640071437261570

Thus the deterministic search visited every one of the 890,703
eligible primes \(13\le p<60{,}000{,}000\) and found a witness
after examining at most 457 \(w\)-values. The digest folds each
prime and its first witness, allowing later runs to detect a
different enumeration. An independent Python bytearray sieve gave
the same class-prime count. A separate
[literal-set crosscheck](69_skew_full_residue_small_crosscheck.py)
factors \(p-1\) independently, builds both exception progressions
directly in the \(w\)-coordinate, and matches the exact first-witness
digest for all 313 eligible primes through 10,000.

## Why one last-pair witness proves every residue

The exception sets are nested in the pair-start center. Consequently,
one \(w\in G\cap B_{k-2}\) works for every earlier adjacent
pair under the *same* primitive root. [Item 60](60_skew_adjacent_pairs.md) repairs all even
growth prefixes \(j\ge2\). [Item 64](64_skew_third_base_two_trades.md) repairs the first three
pages and then pairs the remaining pages at every odd prefix
\(j\ge3\); its first-three repair is valid for every primitive
root, including the three small primes. The square base
\(j=0\) and \(p\)-leaf offset lift come from [item 10](10_odd_hub_blocks.md); all even
bases come from [item 24](24_even_base_residues.md). [Item 58](58_skew_second_base_one_trade.md) supplies \(j=2\), although the
last-pair witness also covers it. The first odd base \(j=1\)
uses [item 57](57_skew_first_base_all_prime_hubs.md) for \(p\ge29\), possibly with a different
primitive root, and [item 54](54_thirteen_skew_repair.md) supplies the explicit \(p=13\)
case. Separate residue classes may use different partitions and
different roots. Together these are every base leaf count from
\(p-1\) through \(2p-2\); the offset lift covers all
\(t\ge p-1\).

For \(p\ge60{,}000{,}000\), item 68 proves
\(G\cap B_{k-2}\ne\varnothing\) analytically for every
primitive root. Hence the finite and infinite ranges meet without a
gap. Every construction attains the lower bound from item 24.

This is a full formula for this prime class, with a finite
computational component. It does not establish the formula for
composite hubs, for primes \(p\equiv1\pmod8\), or for
\(t<p-1\). Publication priority has not been established.
