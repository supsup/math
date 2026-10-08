# An antipodal starter page with perfect translation overlap

The two alternating matchings in the 41-hub page of [item 52](52_fortyone_hub_all_residues.md) are strong starters in the additive group of \(\mathbb F_{41}\): each partitions the nonzero hubs into pairs, uses each nonzero difference up to sign once, and has distinct nonzero pair midpoints. This points to the classical [Mullin–Nemeth construction](https://doi.org/10.4153/CMB-1969-063-6). It gives a page with an especially clean property:

> For every prime \(p=2^kt+1\), where \(k\geq1\) and \(t>1\) is odd, there is a two-factor \(P\) on the \(p-1\) nonzero hubs such that each of its two alternating matchings is a strong starter, and \(|P\cap(P+c)|=1\) for every nonzero translation \(c\in\mathbb F_p\).

This statement about the page's overlap is a deduction from the published starter, not a claim that the page is a single cycle. In fact, this particular page has \(2^{k-1}\) components. When \(p\equiv3\pmod4\), it is connected and recovers the page shape behind [item 34](34_prime_two_leaf_growth.md). When \(p\equiv1\pmod4\), it is disconnected, so the translated-page growth move still needs a cycle repair.

**Construction.** Put \(A=2^{k-1}\), choose a primitive root \(g\), set \(a=g^A\), and let

\[
H=\{g^{2iA+j}:0\leq i<t,\ 0\leq j<A\},\qquad
S=\bigl\{\{x,ax\}:x\in H\bigr\},\qquad P=S\cup(-S).
\]

Mullin and Nemeth prove that \(S\) is a strong starter. Their exponent description also shows \(H\) is a *half-set*: \(H\cap(-H)=\varnothing\) and \(H\cup(-H)=\mathbb F_p^*\). Since \(1+a\ne0\), the pair-midpoint set \(M=(1+a)H/2\) is likewise a half-set. Thus the midpoints in \(S\) and \(-S\) partition all nonzero residues. This additional half-set property is often called *skew*; it follows here from the displayed construction.

For each affine difference color, \(S\) has one edge with midpoint \(m\), while \(-S\) has one with midpoint \(-m\). A translated page can meet the original in that color only at shifts \(\pm2m\), once at each sign. Since \(M\) is a half-set, \(\{\pm2m:m\in M\}=\mathbb F_p^*\) with each nonzero shift occurring exactly once. This proves the overlap statement. It improves the *overlap* side of the [translation criterion](49_affine_translation_overlap.md) to the best possible value, but says nothing by itself about connectedness after growth.

For fixed \(j\), the vertices \(g^{j+\ell A}\) for \(0\leq\ell<2t\) form one alternating cycle of \(P\). The \(A\) choices of \(j\) give exactly \(A\) cycles, each of length \(2t\). At \(p=41\), \(k=3,t=5,A=4\): the page has four 10-hub components, compared with the 32- and 8-hub components in item 52's page. The [checker](53_skew_starter_page.py) verifies the starter, midpoint, component, and all-shift overlap assertions for thirteen sample primes, including 41 and 53.

**An antipodal obstruction.** More generally, suppose \(S\) is any starter whose midpoint set is a half-set, and \(p\equiv1\pmod4\). Then \(S\cup(-S)\) cannot be one Hamilton cycle on the nonzero hubs. If it were, negation would be an automorphism of that cycle, free on vertices and edges, swapping its alternating \(S\)- and \(-S\)-edges. The only cycle automorphism free on both vertices and edges is the half-turn. A cycle on \(p-1\equiv0\pmod4\) vertices has an even half-turn displacement, so that automorphism preserves the alternating edge classes, a contradiction. This rules out the **antipodal** single-page shortcut; it does not rule out a connected page made from two different strong starters, nor multi-component pages repaired by trades.

**Next research steps.** [Item 54](54_thirteen_skew_repair.md) now repairs every odd base at 13, and [item 55](55_skew_two_trade_first_step.md) records six two-trade first-step repairs, including 29. The next tests are later prefixes at 29 and multi-component pages at 41, followed by a uniform invariant for a class of primes if the traces support one. A failed bounded search should remain a construction limit, not a counterexample to the decomposition formula. Item 52 answers the repair question for its own two-cycle 41-page, not for this antipodal page or for all primes. No priority claim is made for the overlap identity or parity observation; their relationship to existing starter literature needs further review.
