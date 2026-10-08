# Every large leaf count with fifty-three bipartite hubs

The [saved odd-base walks and trades](63_fiftythree_hub_odd_seeds.json) can be rebuilt by a [deterministic standard-library generator](63_fiftythree_hub_generator.py). A separate [trade replay](63_fiftythree_hub_trace_audit.py) checks the raw growth moves and all recorded switches, while an [independent all-residue audit](63_fiftythree_hub_independent_audit.py) checks final cycles and lifts.

Let \(d(G)\) be the least number of simple cycles and singleton edges partitioning \(E(G)\). Finite certificates establish

> **\(d(K_{53,t})=t+\lceil26t/53\rceil\) for every \(t\geq52\).**

This is a fixed-hub result, not a uniform all-primes theorem. Publication priority and external peer review are unverified.

**Lower bound.** Each leaf has odd degree 53, so at least one incident spoke is singleton. If \(s\geq t\) singleton spokes and \(r\) cycles are used, a simple bipartite cycle has at most 106 edges. Thus
\[
s+r\geq s+(53t-s)/106
=t+26t/53+(105/106)(s-t)
\geq t+26t/53.
\]
The integer bound follows by taking ceilings.

**All 53 base residues.** Every \(t\geq52\) is uniquely \(b+53q\), \(52\leq b\leq104\). At each even \(b=52,54,\ldots,104\), make hub 52's \(b\) spokes singleton and use the even-side weave on \(K_{52,b}\). It gives \(b/2=\lceil26b/53\rceil\) simple 104-edge cycles. At \(b=53\), diagonal singleton spokes and the 26 cyclic-difference colors give 26 simple 106-edge cycles, because every difference 1 through 26 is coprime to 53.

For \(b=53+2j\), \(1\leq j\leq25\), use the [Mullin–Nemeth antipodal starter](53_skew_starter_page.md) at primitive root \(g=2\). Translate its two-matching page successively through centers \(1,2,\ldots,j\), replacing selected square slots with spokes to two new leaves and collecting displaced spokes as a new short page color. Each raw page has two 26-hub components, while the 26 old colors stay Hamiltonian. At every even prefix, pair adjacent pages \((1,2),(3,4),\ldots\) with the [item-60](60_skew_adjacent_pairs.md) support-preserving rectangle. At odd prefix \(j=1\), use the two-trade first-page repair from [item 55](55_skew_two_trade_first_step.md); the first trade prepares two connected square colors and the second joins the page. For each later odd prefix \(j=3,5,\ldots,25\), repair the preceding pairs and join the final unpaired page with one additional rectangle against a connected partner. The saved trace specifies that partner and all four spokes at every prefix. Every color is then a single simple cycle: 26 full 106-edge cycles and \(j\) short 104-edge cycles. The partition has \(b\) singleton spokes and \(26+j=\lceil26b/53\rceil\) cycles.

Appending a disjoint 53-leaf offset block adds 53 singleton spokes and 26 simple 106-edge cycles, raising both the construction and formula by 79 parts. This proves every residue class.

**Finite evidence and scope.** The standard-library generator saves ordered walks and all 170 four-spoke trade rows across the 26 odd/square bases. The generated certificate JSON is 345,029 bytes with SHA-256 `d2e0fb314f44aa167f46a5ba10c0d7dcac60fa8ec85cb2905081bbd936596a51`; regenerating it needs no solver. A separate standard-library trace audit reconstructs the raw pages and replays every trade, checking connected components and agreement with saved walks. Another independent certificate audit checks all 53 base residues and lifts by 0, 1 and 11 blocks directly from the saved walks: simple cycles, exact spoke coverage and optimum part counts. These finite checks support the fixed-53 theorem; they are not Lean formalization or external peer review. The item-60 character-sum theorem only proves an initial range of paired prefixes uniformly across primes; this fixed-53 result relies on the saved finite prefix certificates.
