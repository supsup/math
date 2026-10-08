# Every large leaf count with forty-one bipartite hubs

Let $d(G)$ be the least number of simple cycles and singleton edges partitioning $E(G)$. An explicit two-cycle affine page, repaired by finite four-edge trades, gives

> **$d(K_{41,t})=t+\left\lceil20t/41\right\rceil$ for every $t\geq40$.**

This is a fixed-hub theorem. The nineteen odd-base repairs are checked separately, with saved ordered walks; no uniform construction for every prime $p\equiv1\pmod4$ is claimed. Publication priority is unverified.

**Lower bound.** Every leaf of $K_{41,t}$ has odd degree, so at least one spoke incident to each leaf must be a singleton. Let there be $s\geq t$ singletons and $r$ cycles. The cycles use $41t-s$ edges, and each simple bipartite cycle uses at most $82$ edges because it has at most 41 distinct hubs. Hence

$$
r+s\geq s+\frac{41t-s}{82}
=t+\frac{20t}{41}+\frac{81}{82}(s-t)
\geq t+\frac{20t}{41}.
$$

Taking the integer ceiling gives the claimed lower bound.

**Even and square bases.** For each even $b=40,42,\ldots,80$, make hub 40's $b$ spokes singleton and apply the [even-side weave](30_even_hub_cycle_weave.md) to $K_{40,b}$. It makes $b/2$ simple 80-edge cycles, and $\lceil20b/41\rceil=b/2$ throughout this range. At $b=41$, use 41 diagonal singleton spokes and twenty 82-edge [offset cycles](10_odd_hub_blocks.md).

**Nineteen odd bases.** For $b=41+2j$, $1\leq j\leq19$, the [growth checker](52_fortyone_hub_two_cycle_growth.py) starts from the square block. Its saved two alternating matchings on the 40 nonzero hubs each contain exactly one edge of every affine difference color $1,\ldots,20$. Across both matchings, their edge midpoints are precisely the 40 nonzero residues. Their union is a two-factor with components of 32 and 8 hubs, so this is deliberately a **two-cycle page**, not a connected growth page.

For each difference color, compare the midpoints of its two page edges. The repeated displacement profile has only one bad magnitude, 1, occurring four times; every other occurring magnitude occurs once. Consequently any two translates with center difference other than $\pm1$ share at most one edge. We use the first $j$ centers of

$$
(1,3,5,7,9,11,13,15,17,19,\;24,26,28,30,32,34,36,38,40).
$$

They avoid $\pm1$. At a growth step, the page selects two edge slots from each old color, replaces their leaf endpoints by the two new leaf labels, makes those two spokes at the center singleton, and puts the displaced spokes in a new page color. The page's midpoint partition and pairwise overlap bound keep its 40 displaced leaf labels distinct. All spokes remain partitioned. Before repair, each old color is one simple 82-edge cycle, while each new page color is split into two cycles with 32 and 8 hubs.

A [support-preserving checkerboard trade](47_support_preserving_switch.md) repairs each split page color. Choose one spoke from each of its two components and the two cross spokes from a connected partner color. Exchange the four spokes. The page components join; the selected partner remains connected. Every hub support, leaf support, singleton spoke, and edge partition remains unchanged. The generator builds **each prefix independently** and checks a deterministic successful sequence of $j$ trades for every $j=1,\ldots,19$. The resulting partition has $b$ singleton spokes, twenty full 82-edge cycles, and $j$ short 80-edge cycles. Thus it has $b+20+j=b+\lceil20b/41\rceil$ parts. The short cycles omit the first $j$ selected centers, one each.

The generator saves the nineteen [odd-base ordered-walk certificates and repair traces](52_fortyone_hub_switch_seeds.json), SHA-256 eed22a0ad539930fcef23b4ec4aecfad5fbe81eda6611777a88f351df29a30ca. The separate [all-residue checker](52_fortyone_hub_all_residues.py) does not import the generator: it reconstructs spoke edges directly from each saved walk, checks connected simple cycles by the walk form, exact spoke coverage, singleton count, cycle count, and the stated hub omissions. It verifies all 41 base residues $40\leq b\leq80$ and eleven added offset blocks per base. The [residue ladder](art/fortyone_hub_residue_ladder.svg) shows the even weave, square, and repaired-page cases.

**Lift.** Every $t\geq40$ is uniquely $b+41q$ with $40\leq b\leq80$ and $q\geq0$. A disjoint 41-leaf offset block adds 41 singleton spokes and twenty Hamilton cycles, or 61 parts. The formula rises by 61 under $t\mapsto t+41$, completing every residue.

The result depends on the explicit 41-hub page and the finite repair trace. The [translation inverse theorem](50_fortyone_center_inverse.md) explains why the displacement profile supports nineteen translates; it does not supply the repairs or a valid connected page on its own. An independent skeptical audit of the saved walks and the construction is requested before any showcase claim.
