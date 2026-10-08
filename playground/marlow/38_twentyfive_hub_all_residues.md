# Every large leaf count with twenty-five bipartite hubs

The next composite odd hub count also meets the proposed formula. Write `d(G)` for the minimum number of simple cycles and singleton edges partitioning `E(G)`. Then

> **`d(K_{25,t})=t+ceil(12t/25)` for every `t≥24`.**

This fixed-hub proof uses a parity/cycle-capacity lower bound, the explicit [even-side weave](30_even_hub_cycle_weave.md), the 25-leaf [offset block](10_odd_hub_blocks.md), and eleven saved odd-base edge certificates. It does not give a uniform construction for composite hub counts. Publication priority is unverified.

**Lower bound.** Each leaf has odd degree 25 and at least one singleton spoke. Write the singleton count as `s=t+X`. Cycles then contain `12t−X/2` leaf appearances, at most 25 per simple cycle. Hence `r+s≥t+12t/25+(49/50)X`, and integrality yields `d(K_{25,t})≥t+ceil(12t/25)`. The nonnegative `X` is even because each leaf has an odd number of singleton spokes. If `X≥2`, the real lower bound rises by `49/25>1`; an optimum meeting the displayed bound must have exactly one singleton spoke at each leaf.

**All 25 base residues.** At each even `b=24,26,…,48`, make hub 24's `b` spokes singleton and weave the residual `K_{24,b}` into `b/2` simple 48-edge cycles. Here `ceil(12b/25)=b/2`. At `b=25`, use 25 diagonal singleton spokes and twelve 50-edge offset cycles. The remaining eleven odd bases are `b=27,29,…,47`. For `b=25+2j`, `1≤j≤11`, the saved [JSON walks](38_twentyfive_hub_odd_seeds.json) give 12 full 50-edge cycles and `j` short 48-edge cycles. Their `b+12+j` parts meet the lower bound. Singleton degrees are three at hubs `0,…,j−1` and one elsewhere; each short cycle omits one of those triple-spoke hubs. The omitted leaves follow the [cyclic interval schedule](33_interval_omission_schedule.md). The interval schedule by itself does not assign edges or guarantee simple connected cycles; the saved walks supply those finite witnesses.

The [checker](38_twentyfive_hub_all_residues.py) reconstructs all 25 base partitions, checks exact spoke coverage and cycle simplicity, verifies eleven added 25-leaf blocks for each base, confirms the interval omissions, and draws the [residue ladder](art/twentyfive_hub_residue_ladder.svg). A separate verifier independently checked the eleven raw odd-base walks; I also rebuilt each partition directly from the saved JSON without importing either checker. The JSON SHA-256 is `d6f0be74ff585eaf736b2522caafff778496c124818546c1c78a1fbf3b60b79d`.

**Lift.** Every `t≥24` has a unique expression `b+25q`, `24≤b≤48`, `q≥0`. Appending one disjoint 25-leaf offset block adds 25 singleton spokes and twelve Hamilton cycles, or 37 parts. The lower bound `t+ceil(12t/25)` also rises by 37 under `t→t+25`, so every residue stays exact. [Item 40](40_twentyseven_hub_all_residues.md) covers the next composite case `h=27`; [item 42](42_twentynine_affine_growth.md) covers `h=29`; the first unchecked odd hub count is composite `h=35`.
