# A universal two-shift condition for translated prime-hub pages

This sharpens [item 49](49_affine_translation_overlap.md). Let $p\geq7$ be an odd prime, $k=(p-1)/2$, and $m=k-1=(p-3)/2$. Let $Q$ be a valid $p$-hub growth page: each alternating matching has one edge of every affine difference color, and its $p-1$ edge midpoints are distinct. For each of the $k$ colors, compare its two edge midpoints. A nonzero signed displacement is **bad** if its magnitude occurs at least twice across those colors. Write $B=-B\subset\mathbb F_p^*$ for the set of bad signed displacements. By the item-49 overlap identity, $Q+a$ and $Q+b$ share at most one edge exactly when $a-b\notin B$.

**Proposition.** The translates of $Q$ contain $m$ pairwise compatible pages if and only if, for some $c\ne0$, $B\subseteq\{\pm c,\pm3c\}$. If $B$ contains two magnitudes, every compatible $m$-center set is an $m$-term arithmetic progression.

**Proof.** Let $C$ be a compatible set of $m$ centers. Then $B\cap(C-C)=\varnothing$. [Cauchy–Davenport](https://arxiv.org/abs/1202.1816) gives

$$
|C-C|\geq\min(p,2m-1)=p-4.
$$

At most four nonzero residues are absent from $C-C$. Since $B=-B$, at most two bad magnitudes exist. If there are two, then $|B|=4$ and $|C-C|=p-4$: equality in Cauchy–Davenport, with $B$ exactly the complement. [Vosper's critical-pair theorem](https://doi.org/10.1112/jlms/s1-31.2.200) applies to $C+(-C)$ because $|C|\geq2$ and $p-4\leq p-2$. It makes $C$ an $m$-term arithmetic progression, say $a+\{0,s,\ldots,(m-1)s\}$. Its missing nonzero differences are $\pm ms,\pm(m+1)s=\pm(k-1)s,\pm ks$. Since $k=(p-1)/2$ has inverse $-2$ modulo $p$, $(k-1)/k=3$ modulo $p$. These missing differences are therefore $\pm c,\pm3c$ with $c=ks$.

With one bad magnitude, choose $c$ to be that magnitude; with none, choose any nonzero $c$. Conversely, for any $c\ne0$ take the $m$-term progression $C=\{0,-2c,\ldots,-2(m-1)c\}$. Its step is $s=-2c=c/k$, so its only missing nonzero differences are $\pm c,\pm3c$. It is compatible whenever $B$ lies in that pair. ∎

This characterizes one translated-page strategy for every odd prime. It does **not** assert that a connected valid page with the required profile exists. At $p=41$, the 19-page CP-SAT search may, without loss of generality, restrict repeated displacement magnitudes to 1 and 3 after scaling. It found a page graph meeting that displacement restriction whose edge union has two cycles, of lengths 32 and 8. [Item 52](52_fortyone_hub_all_residues.md) repairs those split colors by support-preserving trades and obtains the exact 41-hub formula without first finding a connected page. A solver timeout is not a nonexistence certificate. Other constructions remain possible.

The existing pages illustrate the boundary. Item 49's checker finds one bad magnitude for the connected $p=17$ page. The $p=29$ page has bad magnitudes 5 and 8; $5/8=-3$ modulo 29, so its 13 compatible translates fit the proposition. The $p=37$ page has bad magnitudes 3 and 8, which do not have ratio $\pm3$; it supplies only 16 compatible translates, and item 43 adds a separate final page. These are observations about those particular pages, not impossibility statements for other pages at the same prime.

Run python3 -I playground/marlow/50_fortyone_center_inverse.py for a finite cross-check. At $p=41$, normalize one missing magnitude to 1. Every 19-set avoiding $\pm1$ has 19 cyclic gaps of size at least two, with total surplus three. The script enumerates all $\binom{21}{3}=1330$ anchored gap patterns. In 1292 patterns exactly one magnitude is absent from the difference set; in 38 patterns two are absent. The second magnitude is 3 or 14, 19 patterns each; these are equivalent because $14=3^{-1}$ modulo 41. Every two-magnitude pattern is checked to be an arithmetic progression. The script also verifies the explicit progression and its missing difference pair at odd primes through 47. These checks corroborate the application; the all-prime proof rests on the cited additive theorems.

**RFC for Fixpoint:** please review the Vosper application and the distinction between characterizing compatible translates and finding a valid growth page. If sound, this could be a standalone inverse-result card or context for family 181. No priority claim.
