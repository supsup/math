# Every large leaf count with forty-nine bipartite hubs

Let \(d(G)\) be the minimum number of simple cycles and singleton edges partitioning \(E(G)\). The saved finite certificates prove

> \(d(K_{49,t})=t+\lceil24t/49\rceil\) for every \(t\geq48\).

This is a fixed-hub result. The [saved ordered-walk certificates and repair traces](59_fortynine_hub_odd_seeds.json) are solver-free; the [deterministic generator](59_fortynine_hub_generator.py), [trace replay](59_fortynine_hub_trace_audit.py), and [independent all-residue audit](59_fortynine_hub_independent_audit.py) provide separate ways to check them. Publication priority and external peer review remain unverified.

**Lower bound.** Each leaf has odd degree 49 and hence needs a singleton incident edge. If \(s\geq t\) singleton spokes and \(r\) cycles are used, each cycle has at most 98 edges. Thus
\[
  s+r\geq s+(49t-s)/98
  =t+24t/49+(97/98)(s-t)
  \geq t+24t/49.
\]
Taking ceilings gives the lower bound.

**Even bases and square base.** Every \(t\geq48\) is uniquely \(b+49q\) with \(48\leq b\leq96\). For even \(b\), make hub 48's \(b\) spokes singleton and use the even-side weave on \(K_{48,b}\), giving \(b/2=\lceil24b/49\rceil\) simple cycles. For the odd square base and its growth, start with diagonal singleton spokes and the 24 cyclic-difference colors of \(K_{49}\). Differences 7, 14 and 21 each initially yield seven disjoint 7-hub cycles, while all other differences yield a Hamilton cycle. Eighteen explicit support-preserving checkerboard trades join those three split colors, keeping each partner connected. The resulting 49-base has 49 singletons and 24 simple 98-edge cycles.

**Odd growth.** A saved 24-edge matching \(S\) on the nonzero residues modulo 49 uses each undirected difference magnitude 1 through 24 and one midpoint from each antipodal midpoint pair. Let \(E=S\cup(-S)\). Its two alternating matchings each cover the 48 nonzero hubs, all 48 edge midpoints are distinct, and its union has two 24-hub components. For every nonzero shift \(a\), \(|E\cap(E+a)|=1\): for each difference color its two edge midpoints are \(m,-m\), so an overlap shift must be \(\pm2m\), and the 24 antipodal midpoint classes enumerate each nonzero shift exactly once.

At odd base \(b=49+2j\), \(0\leq j\leq23\), translate this page by centers \(1,2,\ldots,j\). Each step replaces its selected old spokes with spokes to two new leaves, places the displaced spokes in a new short color, and adds two singleton spokes at its center. The original page midpoint labels are distinct. A later page intersects any earlier translated page in at most one edge, so at most one selected edge at a step can inherit either fresh leaf from any particular earlier step. The 48 displaced leaf labels are therefore distinct. The three square colors retain seven components each; each new color has two 24-hub components. Eighteen trades join the square colors, then one trade joins each of the \(j\) page colors. Every trade preserves the hubs, leaves and degree-two support of both colors and reduces the split target's component count by one while keeping its partner connected. The result has \(b\) singleton spokes, 24 full 98-edge cycles and \(j\) short 96-edge cycles. Since \(\lceil24(49+2j)/49\rceil=24+j\), it reaches the lower bound.

**Lift and evidence.** Adding a disjoint 49-leaf [offset block](10_odd_hub_blocks.md) supplies 49 singleton spokes and 24 simple 98-edge cycles, raising both the construction and the formula by 73 parts. The certificate JSON contains ordered cycle walks and all 708 four-edge trade rows across the 24 odd bases; its SHA-256 is `2d16b57b5d28308913358be498268850d19ece921e8e58fcf8c1a36a8f749954`. The self-contained standard-library generator reproduces that file byte-for-byte. The separate trace checker replays every trade and matches the saved walks. Another checker independently audits every spoke, cycle simplicity and exact optimum part count for all 49 bases and lifts by 0, 1 and 11 blocks. These are finite computation checks; no Lean formalization or external mathematical peer review is claimed.
