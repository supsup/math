# Third odd base for every prime p ≡ 9 (mod 16)

For every prime \(p\equiv9\pmod{16}\),

\[
d(K_{p,p+6})=\frac{3p+17}{2}.
\]

The [\(p\)-leaf offset block](10_odd_hub_blocks.md) extends equality to
\(t=p+6+rp\), \(r\ge0\). This is a third-base theorem, not yet a formula
for every leaf residue. Its finite component is a deterministic
certificate computation. Publication priority has not been investigated.

## Six page-to-page rectangles

Choose a primitive root \(g\), put \(a=g^4\),
\(\beta=(1+a)/2\), \(\gamma=\beta/a\), and
\(\delta=(1-a)/(1+a)\) in \(\mathbb F_p\). Grow the affine midpoint square
at centers 1, 2, and 3 using the translated antipodal matchings of
[item 79](79_four_component_second_base_all_primes.md). Each page
\(P_c\) has four components indexed at hub \(h\) by
\(\lambda_c(h)=\operatorname{ind}_g(h-c)\bmod4\). Growth changes square
slots, while subsequent page trades do not, so the third growth may
equivalently be done before or after repairing the first two pages.

For centers \(c,d=c+s\), let \(u=v+s\delta\),
\(x=c+\beta(u-c)\), and \(y=c+\gamma(v-c)\). The identities
\(x=d+\beta(v-d)\), \(y=d+\gamma(u-d)\) give a potential rectangle:
\(P_c\) has \((u,x),(v,y)\) and \(P_d\) has \((u,y),(v,x)\).
The two translated pages share one hub edge, whose hubs are
\(c+s/(1+a)\) and \(c+sa/(1+a)\). A later page's two spokes on this
edge may have been relabeled by earlier growth. We exclude those
hubs, and exclude \(x=y\).

First choose three pairwise hub-disjoint \(P_1\)–\(P_2\) rectangles
with label patterns

\[
(\lambda_1(u),\lambda_1(v),\lambda_2(u),\lambda_2(v))
       =(0,j,0,j),\qquad j=1,2,3.
\]

As in item 79, their quotient edges form a star in both pages;
three trades make \(P_1,P_2\) each one cycle. Next use \(s=2\)
and choose one \(P_1\)–\(P_3\) rectangle for each pattern

\[
(\lambda_1(u),\lambda_1(v),\lambda_3(u),\lambda_3(v))
       =(j,j,0,j),\qquad j=1,2,3.
\]

These edges join \(P_3\)'s four components in a star. They also
preserve connectivity of \(P_1\). After the first three trades,
each original noncentral component \(j\) of \(P_1\) had exactly one
spoke cut, so its untouched spokes form an intact path in the new
single cycle. The \(P_1\) source spokes of the \(j\)-th later
rectangle are a beta spoke and a gamma spoke of that path. They
have opposite orientations along the cycle, even if the path as a
whole is traversed backward. Crossing two spokes of opposite
orientation on one bipartite cycle leaves one cycle. Each
noncentral path is used only once, so earlier later-stage trades
do not disturb the next path.

## Analytic supply for p ≥ 300,000

Each prescribed pattern tests four distinct affine roots:
\(v+\delta-1,v-1,v+\delta-2,v-2\) for the first stage, or
\(v+2\delta-1,v-1,v+2\delta-3,v-3\) for the second. Distinctness
uses \(\delta\notin\{0,1,-1\}\). The arbitrary-order quartic
character-sum calculation in item 79 gives at least

\[
N\ge\frac{p-256-513\sqrt p}{256}>73\qquad(p\ge300{,}000)
\]

parameters for **each** pattern. In the first stage, at most four
values touch the shared hub edge, one has \(x=y\), and eight more
can reuse hubs of the two earlier rectangles: at most 13 exclusions.
In the second stage, excluding hubs of \(P_3\)'s two shared edges
costs at most eight values, \(x=y\) costs one, and the six hubs
used by the first stage forbid at most 12 values. Two earlier
second-stage rectangles forbid at most eight more: at most 29
exclusions. Thus all six trades exist for every eligible prime at
least 300,000.

## Finite certificates below 300,000

The [strict-star scanner](81_four_component_third_base_star_scan.cpp)
checks all 3,230 primes \(p\equiv9\pmod{16}\) below 300,000 using
the primitive roots in [item 79's independently audited table](79_four_component_second_base_witnesses.csv).
It finds six hub-disjoint prescribed rectangles for 3,220 primes.
The other ten primes are exactly
\(41,73,89,137,233,281,313,457,617,937\). There were zero
greedy-selection failures after all six prescribed pattern sets
were nonempty. The [3,220-row witness table](81_four_component_third_base_star_witnesses.csv)
has SHA-256 `1e6146ef6be9e44f7ae0b646d3da44504bebcf677c1bfea3d06ba989b2f44083`.
The [independent arithmetic audit](81_four_component_third_base_star_audit.cpp)
checks the entire prime universe, primitive roots, both affine
identities, all labels, shared-edge exclusions, and hub disjointness
at every row.

For the ten exceptions, the [separate table](81_four_component_third_base_exceptions.csv)
records three initial item 79 double-tree trades and three further
\(P_1\)–\(P_3\) trades. Its SHA-256 is
`8fac6a6b08144ab899c5f36133c0d9fb578ea05b0ae338c30a15af1634c57c98`.
The [full graph replay](81_four_component_third_base_full_replay.py)
verifies all ten exceptions and seven strict-star sample primes:
each growth slot, every source spoke, the resulting component
counts, exact coverage of all \(p(p+6)\) spokes, and the final part
count. The finite exceptions rely on these explicit graph checks;
they need not obey the strict-star pattern.

After six trades, there are \(p+6\) singleton spokes,
\((p-1)/2\) full Hamilton cycles, and three short cycles, totaling
\((3p+17)/2\) parts. The odd-hub parity and capacity lower bound is
\(p+6+\lceil((p-1)/2)(p+6)/p\rceil=(3p+17)/2\).

Reproduce from the repository root:

```sh
c++ -O3 -std=c++17 -Wall -Wextra -Werror playground/marlow/81_four_component_third_base_star_scan.cpp -o /tmp/marlow81_scan
/tmp/marlow81_scan playground/marlow/79_four_component_second_base_witnesses.csv /tmp/marlow81_witnesses.csv
shasum -a 256 /tmp/marlow81_witnesses.csv playground/marlow/81_four_component_third_base_star_witnesses.csv
c++ -O3 -std=c++17 -Wall -Wextra -Werror playground/marlow/81_four_component_third_base_star_audit.cpp -o /tmp/marlow81_audit
/tmp/marlow81_audit playground/marlow/81_four_component_third_base_star_witnesses.csv
python3 playground/marlow/81_four_component_third_base_full_replay.py
```
