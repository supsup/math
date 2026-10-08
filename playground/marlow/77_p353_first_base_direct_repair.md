# A direct repair at the first sixteen-component page

The antipodal [item 53 starter page](53_skew_starter_page.md) for
\(p=353\), primitive root \(g=3\), and \(a=g^{16}\) has sixteen
components. The scaled two-trade template in item 73 does not apply:
for all ten generators \(a\) of the subgroup of order 22,
\(\chi((a+3)(1+3a))=+1\), whereas that template asks for \(-1\).
This is a limitation of that sufficient test, not of the graph
partition formula.

**Fixed-hub computer-assisted result.** A direct rectangle repair
gives

\[
d(K_{353,355})=355+\left\lceil\frac{176\cdot355}{353}\right\rceil
=532.
\]

The [saved 19-trade trace](77_p353_first_base_trace.json) starts
with the affine-square decomposition and one translated antipodal
page. Fifteen page-to-square rectangles each join a pair of current
page components. Eleven leave their touched square cycle connected
immediately; four split that square temporarily and are followed by
one square-to-square rectangle that rejoins it without undoing the
page join. Thus sixteen page components become one using 19 trades.

The [standalone replay](77_p353_first_base_audit.py) rebuilds the
square and starter directly from \(p=353,g=3\), checks every
rectangle's four source and target spokes, validates component counts
after every join and repair, and checks all \(125{,}315\) spokes
exactly once. The final partition has 355 singleton spokes, 176 full
\(706\)-edge cycles, and one \(704\)-edge page cycle, hence 532
parts. The odd-hub parity and cycle-capacity lower bound is the
known bipartite example recorded in
[Bucić–Montgomery, Section 6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf).

Run from the repository root:

```sh
python3 -I playground/marlow/77_p353_first_base_audit.py
```

The [item 10 offset block](10_odd_hub_blocks.md) extends this
fixed-hub equality to \(t=355+353r\), \(r\ge0\). The trace
does not give a uniform result for primes \(p\equiv33\pmod{64}\)
or for other leaf residues. Publication priority is unverified.
