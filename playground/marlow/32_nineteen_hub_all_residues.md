# Every large leaf count with nineteen bipartite hubs

Write `d(G)` for the fewest simple cycles and singleton edges partitioning `E(G)`. The finite-hub result is

> **`d(K_{19,t})=t+ceil(9t/19)` for every `t≥18`.**

This follows from a parity/cycle-capacity lower bound, the explicit [even-side weave](30_even_hub_cycle_weave.md), the nineteen-leaf [offset block](10_odd_hub_blocks.md), and eight saved odd-base edge certificates. It does not prove the analogous conjecture for arbitrary odd hub count. Publication priority is unverified.

**Lower bound.** Each of the `t` leaves has odd degree 19, so at least one incident edge must be a singleton part. If there are `s=t+X` singleton spokes, cycles use `9t−X/2` leaf appearances, at most 19 in each simple cycle. Thus

`r+s ≥ t+9t/19+(37/38)X ≥ t+9t/19`,

and integrality gives `d(K_{19,t})≥t+ceil(9t/19)`. Here `X` is a nonnegative even integer because each leaf has an odd number of singleton spokes. If `X≥2`, the real lower bound increases by at least `37/19>1`, so an optimum meeting the stated value has exactly one singleton spoke per leaf.

**All nineteen base residues.** Take one base `b∈{18,…,36}` for each residue modulo 19. If `b` is even, declare all `b` spokes at hub 18 singleton, then use the item-30 weave to partition `K_{18,b}` into `b/2` simple 36-edge cycles. Since `ceil(9b/19)=b/2` on this range, this is optimal. At `b=19`, use 19 diagonal singletons and nine 38-edge offset cycles. At the eight odd bases `b=21,23,…,35`, the saved [JSON walks](32_nineteen_hub_odd_seeds.json) specify every singleton and every alternating simple cycle. For `b=19+2j`, `1≤j≤8`, each certificate has nine full 38-edge cycles and `j` short 36-edge cycles; singleton degrees are three at `j` hubs and one at the other hubs, and the short cycles omit those `j` triple-spoke hubs one apiece. There are `9+j` cycles and `b+9+j` parts, equal to `b+ceil(9b/19)`.

The [checker](32_nineteen_hub_all_residues.py) reconstructs all 19 base partitions and eleven lifted copies per base, confirms every spoke appears exactly once, checks cycle simplicity and part counts, and draws the [residue ladder](art/nineteen_hub_residue_ladder.svg). An independent checker rebuilt all eight saved odd certificates and 95 base/lift partitions without importing this checker. The saved JSON SHA-256 is `b5d816e3ad377e610faceccaacc3fe6fb77eedf2bd34eb6b7a5cb6e07ee07719`.

**Lift.** Every `t≥18` is uniquely `b+19q` for `18≤b≤36`, `q≥0`. Append `q` disjoint nineteen-leaf offset blocks, each with 19 diagonal singleton spokes and nine Hamilton cycles. Each adds 28 parts, exactly the change in `t+ceil(9t/19)` under `t→t+19`. Hence every residue meets the lower bound. The first unchecked odd hub count is composite `h=27`, beginning with `t=29`; [items 37 and 38](README.md) handle `h=21,25`, and [item 34](34_prime_two_leaf_growth.md) covers every prime hub `3 (mod 4)`.

The certificates were found with a [cyclic interval omission schedule](33_interval_omission_schedule.md). Its degree balance is uniform in odd `h`, but finding simple connected cycles from that schedule remains an open construction step here.
