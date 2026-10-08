# Six two-trade repairs at the first odd base

For each tested prime \(p\in\{13,29,37,53,61,101\}\), the [Mullin–Nemeth antipodal page](53_skew_starter_page.md) splits into two equal cycles. At the first odd leaf count \(t=p+2\), two support-preserving checkerboard trades turn that page color into one \(2(p-1)\)-edge cycle while keeping every old \(2p\)-edge square color connected. The [exact replay](55_skew_two_trade_first_step.py) and [independent audit](55_skew_independent_audit.py) check all six partitions and the optimal part count \(t+\lceil((p-1)/2)t/p\rceil\).

| \(p\) | first odd \(t\) | optimal parts | first trade's adjacent hubs \(x,x+1\) |
| ---: | ---: | ---: | ---: |
| 13 | 15 | 22 | 0, 1 |
| 29 | 31 | 46 | 5, 6 |
| 37 | 39 | 58 | 0, 1 |
| 53 | 55 | 82 | 9, 10 |
| 61 | 63 | 94 | 16, 17 |
| 101 | 103 | 154 | 21, 22 |

All six primes satisfy \(p\equiv5\pmod8\), so \(p-1=4u\) with odd \(u\). In the antipodal starter, the two page components have \(2u=(p-1)/2\) hubs each: one on quadratic residues and one on nonresidues. Their translates share exactly one edge by [item 53](53_skew_starter_page.md), so the growth operation produces an exact spoke partition before repair.

Put \(k=(p-1)/2\), and index square colors by difference \(1,2,\ldots,k\), starting at zero. The **preparatory trade** always exchanges color 0 spokes

\[
(x,x+k),\ (x+1,x+k+2)
\quad\longleftrightarrow\quad
(x,x+k+2),\ (x+1,x+k)
\]

with color 2. It preserves both square colors as single cycles in these six cases. A second trade between color 0 and the new page color \(k\) joins the page components. The exact four spokes of both trades are in the replay script. For example, at \(p=29\) the first exchange uses \((5,19),(6,21)\) against \((5,21),(6,19)\); the second uses color 0 spokes \((4,18),(5,21)\) against page spokes \((4,21),(5,18)\). Both are instances of the support-preserving rectangle exchange from [item 47](47_support_preserving_switch.md).

**A conditional algebraic repair.** Let \(p\geq13\) be a prime with \(p\equiv5\pmod8\). Work in \(\mathbb F_p\), choose a primitive root \(g\), put \(a=g^2\), and define

\[
Z=\frac{1+3a}{(a-1)^2},\quad
W=\frac{a(a+3)}{(a-1)^2},\quad
b=1+Z,\quad v=1+W,\quad
\mu_d=\frac{d(1+a)}{2(a-1)}.
\]

Let \(\chi\) denote the quadratic character. Suppose \(Z,W\ne0\), \(\chi(W/Z)=-1\), and these six **slot exclusions** hold:

\[
\{b-\tfrac12,b+\tfrac12,b+\tfrac32,v+\tfrac12\}
\cap\{1-\mu_1,1+\mu_1\}=\varnothing,
\qquad
\{b-\tfrac12,b+\tfrac32\}
\cap\{1-\mu_3,1+\mu_3\}=\varnothing.
\]

Then the first growth page at center 1 has the following two-trade repair:

\[
\begin{aligned}
C_1\leftrightarrow C_3:&\quad
(b,b-\tfrac12),(b+1,b+\tfrac32)
\leftrightarrow(b,b+\tfrac32),(b+1,b-\tfrac12),\\
C_1\leftrightarrow P:&\quad
(b,b+\tfrac12),(v,v+\tfrac12)
\leftrightarrow(b,v+\tfrac12),(v,b+\tfrac12).
\end{aligned}
\]

Here \(C_d\) is the square color of difference \(d\), so it has script index \(d-1\), and \(P\) is the new page color. To see why the exclusions are exact, the antipodal starter's two color-\(d\) edges are \(\pm\{d/(a-1),ad/(a-1)\}\), whose translated midpoints are precisely \(1\pm\mu_d\). All six spokes required from \(C_1,C_3\) retain their square leaves when the displayed sets avoid those midpoints. In the first trade, \(C_1\) swaps adjacent hubs \(b,b+1\) in its Hamilton order, and \(C_3\) exchanges a forward spoke on its \(+3\) edge \((b,b+3)\) with a backward spoke on \((b-2,b+1)\); both remain one cycle.

The translated page has at each hub \(h\ne1\) the two spokes with leaves \(1+\beta(h-1)\) and \(1+\gamma(h-1)\), where \(\beta=(1+a)/2\) and \(\gamma=\beta/a\). The definitions of \(Z,W\) give \(v+\tfrac12=1+\beta Z\) and \(b+\tfrac12=1+\gamma W\). Hence the second trade's cross spokes lie in \(P\), at hubs \(b,v\). Its components are the translated quadratic-residue and nonresidue classes, so \(\chi(W/Z)=-1\) puts those spokes in different components. Also \(v-b=(a+1)/(a-1)\notin\{0,1,-1\}\), since \(a\) has order greater than two. Thus the first trade reversed the \(C_1\) spoke at \(b\) relative to the untouched forward spoke at \(v\); the second exchange joins \(P\) while leaving \(C_1\) connected. Both trades preserve each color's hub and leaf support. This proves the conditional first-step result.

The [checker](55_skew_two_trade_first_step.py) derives these formulaic trades and verifies full partitions at \(p=37,61,101\). An [independent conditional audit](55_skew_conditional_audit.py) verifies the slot algebra and the three touched colors at every qualifying prime through 1000. The condition is sufficient, not automatic: at 29 and 53 the formula's two target hubs lie in the same page component, although the separate saved trades succeed; at 13 the formula degenerates; at 157 a needed square slot is replaced during growth. A finite scan with least primitive roots finds the full condition at 21 of the 42 primes \(p\equiv5\pmod8\) from 13 through 1000. These six certificates concern only the **first odd base**. [Item 54](54_thirteen_skew_repair.md) separately repairs all five odd bases at \(p=13\); later-base and uniform-class repairs remain open.
