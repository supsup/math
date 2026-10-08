# A conditional spanning-tree repair for a multi-cycle starter page

The antipodal Mullin–Nemeth page in [item 53](53_skew_starter_page.md)
has more than two components at primes \(p\equiv1\pmod8\).
This note gives a **sufficient**, explicitly checkable way to join them.
It does not prove that the required trades can be packed at every such
prime. The \(p=73\) example below checks the mechanism on a complete
edge partition; [item 62](62_one_mod8_first_base.md) already proves
that fixed first base with a shorter, four-trade certificate.

Write \(p-1=2Aq\), where \(A=2^{v_2(p-1)-1}\ge4\) and odd \(q>1\).
Choose a primitive root \(g\), put \(a=g^A\), and grow one translated
antipodal starter page \(P\) at center \(1\) from the affine square
decomposition of \(K_{p,p}\). The page has \(A\) components indexed by
the cosets of \(\langle a\rangle\) in \(\mathbb F_p^\times\). Let \(C_d\)
denote the full square color of hub difference \(\pm d\), with
\(1\le d\le(p-1)/2\).

Assume the [item 55 two-trade template](55_skew_two_trade_first_step.md)
passes its explicit slot exclusions with this value of \(a\). In its
notation,

\[
Z=\frac{1+3a}{(a-1)^2},\qquad
W=\frac{a(a+3)}{(a-1)^2},\qquad
b=1+Z,\quad v=1+W,\quad
\mu_d=\frac{d(1+a)}{2(a-1)}.
\]

Specifically require \(Z,W\ne0\), \(\chi(W/Z)=-1\), and

\[
\{b-\tfrac12,b+\tfrac12,b+\tfrac32,v+\tfrac12\}
\cap\{1-\mu_1,1+\mu_1\}=\varnothing,
\qquad
\{b-\tfrac12,b+\tfrac32\}
\cap\{1-\mu_3,1+\mu_3\}=\varnothing.
\]

The first trade exchanges \(C_1\) and \(C_3\) spokes

\[
(b,b-\tfrac12),(b+1,b+\tfrac32)
\longleftrightarrow
(b,b+\tfrac32),(b+1,b-\tfrac12);
\]

the second exchanges \(C_1\) and page spokes

\[
(b,b+\tfrac12),(v,v+\tfrac12)
\longleftrightarrow
(b,v+\tfrac12),(v,b+\tfrac12).
\]

Each ordered pair is a (hub, leaf) spoke. The slot exclusions ensure
that the first exchange touches unchanged square slots, preserving both
full cycles. The page spokes in the second exchange are the two crossed
targets. The item 55 local cycle argument then preserves \(C_1\) and
joins the page components containing \(1+Z\) and \(1+W\). It uses the
affine-square hub order and the fact that these page components differ;
it does not require the page to have only two components.

For every nonzero scale \(\lambda\), the affine map
\(T_\lambda(x)=1+\lambda(x-1)\) preserves the page spoke set. Indeed,
the page's hub pairs are \(\{1+x,1+ax\}\) over all
\(x\in\mathbb F_p^\times\), and each old leaf is their midpoint.
On old leaves, the map sends the displayed unchanged spokes in
\(C_1,C_3\) to the corresponding spokes in
\(C_{[\lambda]},C_{[3\lambda]}\), where
\([u]=\min(u\bmod p,-u\bmod p)\). It need not map the
*entire grown square color* to that color: scaling can exchange
which of the two fresh leaf labels replaces a particular square
slot. This does not change the square cycle's topology, because
each fresh leaf still replaces one old leaf at the same two hubs.
The map sends the two joined page components to
\(\lambda Z\langle a\rangle\) and
\(\lambda W\langle a\rangle\).

**Packing lemma.** Suppose \(A-1\) scales are chosen so that:

1. Their quotient edges
   \(\{\lambda Z\langle a\rangle,\lambda W\langle a\rangle\}\)
   form a spanning tree on the \(A\) page components.
2. All \(2(A-1)\) square colors \(C_{[\lambda]}\) and
   \(C_{[3\lambda]}\) are distinct.
3. The two original page spokes targeted by each scaled second trade
   are distinct across all chosen scales.

Then applying the scaled two-trade gadgets in any order gives a
partition of \(K_{p,p+2}\) into \(p+2\) singleton spokes,
\((p-1)/2\) full \(2p\)-edge cycles, and one
\(2(p-1)\)-edge page cycle. In particular,

\[
d(K_{p,p+2})=p+2+
 \left\lceil\frac{(p-1)(p+2)}{2p}\right\rceil
 =\frac{3p+5}{2}.
\]

To prove the lemma, each gadget's square colors are untouched by
earlier gadgets, by condition 2. Its required original page spokes
are still present, by condition 3. The already-used quotient edges
form a forest, so the next tree edge joins two different *current*
page components. The item 55 local move therefore reduces their
count by one, while keeping both square colors connected. Every
rectangle exchanges exactly the same four spokes between colors,
so edge coverage and every vertex support remain exact. After
\(A-1\) gadgets the page is one cycle. The odd-leaf parity and
maximum-cycle-length argument gives the displayed lower bound.

The quotient \(\mathbb F_p^\times/\langle a\rangle\) is cyclic of
power-of-two order \(A\). Since \(\chi(W/Z)=-1\), the quotient
exponent of \(W/Z\) is odd, so it generates the quotient. Thus the
*abstract* candidate edges from all scales already form a connected
cycle.

There is also a simple **greedy packing range**. Fix a spanning tree
by deleting one edge from that quotient cycle. Each of its oriented
edges has exactly \(2q=|\langle a\rangle|\) realizing scales.
One previously chosen gadget excludes at most eight candidate scales
because either of the two candidate square colors might equal either
of its two used square colors, each equality having at most two
signed solutions. It excludes at most four more scales because
either of the two candidate original page spokes might equal either
of its two used page spokes; each such equality fixes \(\lambda\)
uniquely from the nonzero hub offset \(Z\) or \(W\).
After at most \(A-2\) choices, a bucket therefore retains at least
\(2q-12(A-2)\) scales. Consequently

\[
q>6(A-2)
\]

guarantees a compatible packing **whenever the base two-trade
template's algebraic hypotheses hold**. This does not establish
those hypotheses for every prime.

At \(p=73\), take \(g=13\), \(A=4\), \(q=9\), \(a=18\),
\(Z=6\), \(W=20\), and \(W/Z=52\). The scales \(4,7,44\)
give quotient edges \((2,3),(1,2),(3,0)\), a tree. The
[standalone six-trade replay](73_one_mod8_scaled_gadget_p73_audit.py)
constructs the square and page without importing the search code,
checks every source and target spoke, and finds page component
counts \(4\to3\to2\to1\). It verifies all 5,475 spokes exactly
once in 75 singletons, 36 full cycles, and one short cycle:
112 optimal parts. This is a second construction for an already
proved fixed case, illustrating the quotient-tree pattern.

When \(q=1\), \(a=-1\) and the antipodal starter degenerates.
This particular distinct-color packing policy also asks for
\(2(A-1)>A\) square colors when \(A\ge4\), so it cannot handle
those primes. Neither limitation obstructs the graph formula
itself. No uniform theorem for \(p\equiv1\pmod8\) is claimed.
