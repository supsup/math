# An analytic first-base tail for prime hubs one modulo eight

Let \(d(G)\) be the minimum number of simple cycles and singleton
edges partitioning \(E(G)\).

**First-base theorem.** Let \(p\equiv1\pmod8\) be prime, put
\(n=p-1=2Aq\), where \(A=2^{v_2(n)-1}\ge4\) and \(q\) is odd.
If

\[
n>(80A)^3,
\]

then

\[
d(K_{p,p+2})
 =p+2+\left\lceil\frac{(p-1)(p+2)}{2p}\right\rceil
 =\frac{3p+5}{2}.
\]

Appending disjoint \(p\)-leaf offset blocks from
[item 10](10_odd_hub_blocks.md) gives the same formula
\(d(K_{p,t})=t+\lceil((p-1)/2)t/p\rceil\) at
\(t=p+2+rp\) for every integer \(r\ge0\).
This theorem does **not** cover the other leaf residues modulo \(p\) or all
primes one modulo eight. For the progression \(p\equiv9\pmod{16}\),
where \(A=4\), the explicit condition is \(p-1>32{,}768{,}000\).

The proof combines the [conditional scaled-gadget tree](73_one_mod8_scaled_gadget_tree.md)
with the primitive-root character sieve used at
[item 57](57_skew_first_base_all_prime_hubs.md). The
[Mullin–Nemeth starter](53_skew_starter_page.md) supplies a page with
\(A\) components; its construction is classical. The parity and
maximum-cycle-length lower bound is the odd-hub bipartite example
recorded by [Bucić and Montgomery, Section 6](https://rhmontgomery.warwick.ac.uk/papers/28cyclepacking.pdf).
The new claim here is the attaining first-base construction in this
explicit tail. Publication priority has not been established.

## A primitive root passes the local two-trade test

Write \(\theta=\varphi(n)/n\) and \(V(n)=2^{\omega(n)}\).
For a primitive root \(g\), put \(a=g^A\) and

\[
F(X)=(X^A+3)(3X^A+1).
\]

Since \(A\) is even, \(a\) is a square. The item 55 ratio
\(W/Z=a(a+3)/(1+3a)\) therefore satisfies

\[
\chi(W/Z)=\chi(F(g))
\]

whenever its numerator and denominator are nonzero.
The two factors of \(F\) have disjoint, nonzero, simple roots
over the algebraic closure: their defining values \(-3\) and
\(-1/3\) differ for odd \(p\), and \(p\nmid A\).
Thus \(F\) has exactly \(2A\) distinct roots there and at most
\(2A\) roots in \(\mathbb F_p\).

Consider

\[
T=\sum_{\substack{g\in\mathbb F_p^\times\\g\ {\rm primitive}}}
       \chi(F(g)).
\]

The standard primitive-element indicator has coefficient
\(\ell^1\)-mass \(\theta V(n)\); see
[Cohen–Sharma–Sharma (2019), Section 2](https://arxiv.org/pdf/1909.13074).
For any one of its multiplicative-character terms \(\psi(g)\),
the order \(d\) of \(\psi\) is squarefree.
Let \(m=\operatorname{lcm}(d,2)\), choose a character \(\eta\) of
order \(m\), and write the product as
\(\eta(g^jF(g)^{m/2})\) for a suitable exponent \(j\).
Every root of \(F\) then has exponent \(m/2\), so the polynomial
is not an \(m\)-th power. It has at most \(2A+1\) distinct
roots, counting \(0\). [Lemma 2.1 of the same source](https://arxiv.org/pdf/1909.13074)
gives a bound of \(2A\sqrt p\) for the complete sum.
For the trivial \(\psi\), omitting \(g=0\) costs at most one,
which is absorbed by the same bound. Hence

\[
|T|\le2A\theta V(n)\sqrt p.                         \tag{1}
\]

At most \(2A\) primitive roots give \(F(g)=0\).
The eight algebraic exclusions of item 55 consist of two
linear and six quadratic equations in \(a\), forbidding at
most \(14\) values of \(a\), hence at most \(14A\) values
of \(g\). Thus the number of primitive roots with
\(\chi(F(g))=-1\) and none of those exclusions is positive
whenever

\[
\frac{\theta n-2A-2A\theta V(n)\sqrt p}{2}>14A.
\]

Because \(\theta\ge1/V(n)\), a sufficient condition is

\[
n>A V(n)(2\sqrt p+30).                             \tag{2}
\]

For such a root, \(a=g^A\) has order \(2q>2\), and item 55's
slot-and-cycle argument applies to the \(A\)-component page
as explained in item 73.

## The numerical tail and the packing

[Cohen–Sharma–Sharma, Lemma 3.2](https://arxiv.org/pdf/1909.13074)
gives \(V(n)<37.469\,n^{1/6}\).
Our hypothesis implies \(n>(80\cdot4)^3>96{,}100\).
Consequently

\[
2\sqrt{n+1}+30<2.1\sqrt n,\qquad
A V(n)(2\sqrt p+30)
 <(37.469)(2.1)A n^{2/3}
 <80A n^{2/3}<n.
\]

This proves (2) without a finite prime sweep. Also
\[
q=\frac{n}{2A}>256{,}000A^2>6(A-2).
\]
The greedy packing argument in item 73 therefore selects
\(A-1\) compatible scaled gadgets along a quotient spanning
tree. Each performs two support-preserving trades, keeps
every full square color connected, and joins one page-component
pair. The final page is one cycle, giving the stated upper
bound. The published odd-hub lower bound matches it exactly.

The threshold is deliberately conservative. Below it,
failure of this estimate says nothing about the partition
formula; [item 62](62_one_mod8_first_base.md) already certifies
several smaller first bases by explicit trades. A proof at all
prime hubs one modulo eight would also need the other
leaf residues modulo \(p\).
