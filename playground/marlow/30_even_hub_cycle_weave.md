# The even-hub parity cliff and an explicit cycle weave

The [even-base note](24_even_base_residues.md) first used Sotteau's general cycle-decomposition theorem. For the particular `K_{2k,2m}` it needs, there is a short explicit construction. It also gives an exact formula with a sharp parity jump:

> For even `h=2k≥2` and `t≥h`, `d(K_{h,t})=t/2` if `t` is even, while `d(K_{h,t})=h+(t−1)/2` if `t` is odd.

This is a concrete corollary of classical even-cycle design theory, not a novelty claim. Here `d(G)` counts simple cycles and singleton edges in an edge partition.

**Cycle weave.** Let `t=2m` with `m≥k`. Name the hubs `H_0,…,H_{2k−1}` and group the leaves as `(A_p,B_p)` for `p∈Z_m`. For every `c∈Z_m`, form a `4k`-edge cycle by taking the hubs in order `H_0,H_1,…,H_{2k−1}` and putting between `H_{2j}` and `H_{2j+1}` the leaf `A_{c+j}`, and between `H_{2j+1}` and `H_{2j+2 mod 2k}` the leaf `B_{c+j}`, for `j=0,…,k−1`. Subscripts on `A,B` are modulo `m`.

Each cycle is simple: its `k` leaf-pair indices are distinct because `m≥k`, and all hubs are distinct. For fixed `A_p`, the `k` cycles `c=p−j` place it between hub pairs `(H_{2j},H_{2j+1})` for all `j`; these pairs partition the `2k` hubs. For fixed `B_p`, the analogous adjacent pairs `(H_{2j+1},H_{2j+2 mod 2k})` also partition the hubs. Thus every hub–leaf spoke appears once and only once, in exactly `m=t/2` cycles. The [checker and four-hub picture](30_even_hub_cycle_weave.py) verify finite instances and show the `K_{4,6}` case.

**Optimality and odd `t`.** A cycle in `K_{h,t}` uses at most `2h` edges. With `s` singleton spokes, the number of parts obeys

`r+s ≥ (ht−s)/(2h)+s = t/2+(1−1/(2h))s`.

For even `t`, this gives `d≥t/2`, attained by the weave. For odd `t`, all `h` hubs have odd degree, so each needs an incident singleton spoke and `s≥h`. The bound then becomes `d≥h+(t−1)/2`. Make all `h` spokes at one leaf singleton parts and apply the weave to the other `t−1` leaves; since `t≥h+1`, the required `m=(t−1)/2≥k`. This attains the bound.

The parity cliff is visible already at four hubs: `d(K_{4,4})=2`, `d(K_{4,5})=6`, and `d(K_{4,6})=3`. Adding the fifth leaf raises the minimum by four parts; adding the sixth lowers it by three. The [diagram](art/even_hub_parity_cliff.svg) gives an explicit three-cycle edge partition of `K_{4,6}` alongside those counts. This is an edge-partition parameter, so it need not be monotone under adding leaves. For odd `h=2k+1`, delete one hub's spokes as singletons and use this weave on `K_{2k,b}`; [item 24](24_even_base_residues.md) records the resulting exact even-base residues.
