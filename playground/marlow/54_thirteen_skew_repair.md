# Repairing a split starter page at every thirteen-hub odd base

The [Mullin–Nemeth antipodal page](53_skew_starter_page.md) at \(p=13\) is two disjoint 6-hub cycles. Its translates have perfect one-edge overlap, but the page is not itself a usable short cycle for the two-leaf growth move. Exact support-preserving trades repair this split page at **all five** difficult odd base counts:

| leaf count \(b\) | translated pages | saved trades | final cycles |
| ---: | ---: | ---: | ---: |
| 15 | 1 | 2 | six 26-edge + one 24-edge |
| 17 | 2 | 2 | six 26-edge + two 24-edge |
| 19 | 3 | 2 | six 26-edge + three 24-edge |
| 21 | 4 | 3 | six 26-edge + four 24-edge |
| 23 | 5 | 4 | six 26-edge + five 24-edge |

At each base there are exactly \(b\) singleton spokes, so the part count is \(b+6+j=b+\lceil6b/13\rceil\), where \(b=13+2j\). Combining these odd bases with the even-side weave, the 13-leaf square block, and offset-block lifts gives another proof of \(d(K_{13,t})=t+\lceil6t/13\rceil\) for all \(t\geq12\). The lower bound and base/lift argument are in [item 26](26_thirteen_hub_all_residues.md). The result itself was already known there from finite edge certificates; the new point is a common **starter page and repair mechanism** for all five odd bases.

Take primitive root 2, put \(a=2^2=4\), and use the two alternating matchings

\[
S=\{(1,4),(2,8),(3,12),(5,7),(6,11),(9,10)\},\qquad
-S=\{(1,10),(2,7),(3,4),(5,11),(6,8),(9,12)\},
\]

where each ordered-looking pair denotes an unordered hub edge. These matchings each use one edge of every affine difference color and their twelve midpoints are all nonzero residues. Starting from the affine square, translate this same page by centers \(1,2,\ldots,j\), one for each growth step. The one-edge overlap property from item 53 keeps the displaced leaf labels distinct. The growth operation preserves the old six Hamilton colors, but leaves every new page color in two 6-hub components.

For the first base \(b=15\), a preparatory checkerboard trade exchanges color 0 spokes \((0,6),(1,8)\) with color 2 spokes \((0,8),(1,6)\). Both colors remain connected. A second trade exchanges color 0 spokes \((0,7),(8,2)\) with page-color 6 spokes \((0,2),(8,7)\). This joins the two page components and leaves color 0 connected. The number of cycle components goes \(8\to8\to7\). An exhaustive one-trade scan in this precise checkerboard move class found no direct reduction for the initial \(b=15\) state; the preparatory trade changes the available cross spokes.

The other four prefixes have their own short [saved trade traces](54_thirteen_skew_repair_traces.json). The [deterministic replay](54_thirteen_skew_repair.py) constructs **each prefix afresh** from the square, applies its own trace, checks that total component count never rises, checks every color is a single simple cycle of the required length, and verifies every spoke of \(K_{13,b}\) appears exactly once. A [separate audit](54_thirteen_skew_independent_audit.py) independently enumerates square pairs, replays every intermediate edge partition, and checks supports and connectivity; it found no defect. The repairs can join two split pages in one trade, which explains why some prefixes use fewer trades than pages. This is a fixed-prime finite construction; it does not establish a repair theorem for all \(p\equiv1\pmod4\).
