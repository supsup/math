# Every large leaf count with forty-five bipartite hubs

Let \(d(G)\) be the minimum number of simple cycles and singleton edges partitioning \(E(G)\). Exact finite certificates for the remaining odd bases give

> **\(d(K_{45,t})=t+\lceil22t/45\rceil\) for every \(t\geq44\).**

This is a fixed-hub result. The difficult odd bases are supplied by 21 saved connected-cycle walks; no uniform proof for every odd hub count is claimed. Publication priority is unverified, and Fixpoint's per-hub review rule keeps this local rather than in the showcase.

**Lower bound.** Every leaf has degree 45, so at least one incident spoke must be a singleton. If there are \(s\geq t\) singleton spokes and \(r\) cycles, then the cycles use \(45t-s\) edges. A simple bipartite cycle has at most 90 edges, so

\[
s+r\geq s+\frac{45t-s}{90}
=t+\frac{22t}{45}+\frac{89}{90}(s-t)
\geq t+\frac{22t}{45}.
\]

Taking the integer ceiling yields the asserted lower bound.

**All 45 base residues.** For each even \(b=44,46,\ldots,88\), make hub 44's \(b\) spokes singleton and apply the [even-side weave](30_even_hub_cycle_weave.md) to \(K_{44,b}\). It yields \(b/2\) simple 88-edge cycles, and \(\lceil22b/45\rceil=b/2\) throughout this interval. At \(b=45\), take 45 diagonal singleton spokes and 22 simple 90-edge [offset cycles](10_odd_hub_blocks.md).

For \(b=45+2j\), \(1\leq j\leq21\), the [saved odd-base walks](56_fortyfive_hub_odd_seeds.json) have \(b\) singleton spokes, 22 full 90-edge cycles, and \(j\) short 88-edge cycles. The singleton degrees are three at hubs \(0,\ldots,j-1\) and one elsewhere; the short colors omit those \(j\) hubs, one each. Each cycle follows the [cyclic interval leaf-omission schedule](33_interval_omission_schedule.md). The count is \(b+22+j=b+\lceil22b/45\rceil\). The bundle SHA-256 is `527bb9ccd5c4522cddb1e600b755bdac2beb8bca658b9df6d78920003c31f0c6`.

The [all-residue checker](56_fortyfive_hub_all_residues.py) reads those ordered walks directly, checks each simple cycle and exact spoke coverage for all 45 bases, then appends and checks eleven 45-leaf offset blocks per base. It generates the [residue ladder](art/fortyfive_hub_residue_ladder.svg). The odd walks were reconstructed from the raw CP-SAT edge lists before bundling, with connectedness, hub omission, leaf omission, and exact edge coverage checked separately. A [second independent audit](56_fortyfive_hub_independent_audit.py) checked all 21 saved walks, all 45 bases, and 24 sampled lifts without importing the first checker. The [search model](56_fortyfive_hub_interval_search.py) records the interval schedule and a safe orientation symmetry break; it requires OR-Tools only to find new raw witnesses, while verification of the saved bundle uses Python's standard library. For the hardest base \(b=87\), a separate degree-only model followed by 38 support-preserving two-color trades also produced an independently checked optimum certificate; that alternative construction is not needed for this proof.

**Lift.** Every \(t\geq44\) is uniquely \(b+45q\) for \(44\leq b\leq88\). A disjoint 45-leaf offset block adds 45 singleton spokes and 22 cycles, or 67 parts, while the formula rises by 67 under \(t\mapsto t+45\). Hence every leaf count in the stated range meets the lower bound.
