# Every leaf count at prime hubs three modulo four

Write `d(G)` for the fewest simple cycles and singleton edges partitioning `E(G)`. An affine square seed admits a repeatable two-leaf growth move, giving an infinite-hub result:

> **Theorem.** For every prime `p≥7` with `p≡3 (mod 4)` and every `t≥p−1`, `d(K_{p,t})=t+ceil(((p−1)/2)t/p)`.

This proves the [odd-hub conjecture](27_odd_hub_design_question.md) for these primes, including **all** their difficult odd base residues. It says nothing yet about composite hubs or primes `p≡1 (mod 4)`. Publication priority of this formulation and construction is unverified.

Put `k=(p−1)/2`, which is odd, and label hubs and square-seed leaves by `F_p`.

**Affine square seed.** Declare `(a,a)` a singleton spoke for every `a∈F_p`. For each difference class `{d,−d}`, represented by `d=1,…,k`, use the Hamilton hub cycle `0,d,2d,…,(p−1)d,0`. Replace its edge `{u,u+d}` by the leaf at its midpoint `m=u+d/2`. Every such cycle uses all `p` hub labels and all `p` leaf labels once. For a fixed leaf `m`, the pairs `{m−d/2,m+d/2}` over `d=1,…,k` partition the other `p−1` hubs; with `(m,m)`, this partitions every spoke of `K_{p,p}`.

**Translated growth cycles.** Choose a primitive root `g` modulo `p`. For each center `a`, let `C_a` be the hub cycle

`a+1, a+g, a+g², …, a+g^(p−2), a+1`.

It visits every hub except `a`. Its edge at index `i` has signed difference `(g−1)g^i`, independent of `a`. The same difference class `{d,−d}` occurs at exactly indices `i` and `i+k`, since `g^k=−1`. As `k` is odd, those indices have opposite parity. Thus the even and odd edges of `C_a` are perfect matchings on the hubs other than `a`, **each taking exactly one edge from each affine full-cycle color**.

The original midpoint labels along `C_a` are `a+((1+g)/2)g^i`. Since `g` has order `p−1≥6`, `g≠−1`, so these `p−1` labels are distinct. The key to repetition is that **two differently centered cycles meet in exactly one hub edge**. If an edge `{u,v}` lies in both `C_a` and `C_b`, `a≠b`, its orientations must oppose: the same orientation would imply `(1−g)(a−b)=0`. Solving the opposite orientations yields the unique common edge

`{(g a+b)/(1+g), (a+g b)/(1+g)}`.

Conversely, those two vertices do form an edge of each cycle, so `|E(C_a)∩E(C_b)|=1`. The two orientations of any given hub edge also determine exactly two distinct centers, so the family `{C_a}` is an *orthogonal double cover* of `K_p` by cycles of length `p−1`. [Bey–Hartmann–Leck–Leck (2002)](https://www.math.uni-luebeck.de/mitarbeiter/bey/pub/orthogonal_double_covers_by_super-extendable_cycles__02_BEY_HARTMANN_LECK_LECK.pdf) studies this type of cover. The terminology and general subject are prior art; the use here is the distinct-displaced-leaf induction.

**Inductive two-leaf move.** Begin with the affine square seed. At step `a`, using a center not used before, add leaves `x_a=p+2a` and `y_a=p+2a+1`, with singleton spokes to hub `a`. In each of the `k` full cycles, replace the leaf on its unique even-indexed selected `C_a` edge by `x_a`, and the leaf on its unique odd-indexed selected edge by `y_a`. The displaced old leaves, in `C_a` order, make a new short alternating cycle on the `p−1` hubs other than `a`; its old spokes are precisely the two spokes just removed from each full cycle.

The displaced leaves are distinct at **every** step. Old square-seed labels originally appear at the injective midpoint positions along `C_a`; replacements can only remove some of them from full-cycle slots. A leaf introduced at an earlier center `b` has its remaining full-cycle slots on edges of `C_b`, so it can appear on at most the one edge of `C_a∩C_b`. Labels introduced at different steps are disjoint. Hence the new short cycle is simple. The even and odd matchings give each new leaf exactly one spoke to every hub other than `a`; its singleton gives the remaining spoke. All pre-existing spokes keep their edge coverage. The full cycles remain simple because each loses two distinct leaf labels and gains two fresh labels.

Use centers `a=0,1,…,j−1` for any `0≤j≤k−1`. At `b=p+2j`, the partition has `b` singleton spokes, `k` full `2p`-cycles, and `j` short `2(p−1)`-cycles, hence `b+k+j` parts. The parity/cycle-capacity lower bound gives `d(K_{p,b})≥b+ceil(kb/p)=b+k+j`, since `kb/p=k+j−j/p` and `0≤j<p`. Thus **every difficult odd base is exact**. [Item 24](24_even_base_residues.md) supplies all even bases `p−1,p+1,…,2p−2`, and the [offset block](10_odd_hub_blocks.md) lifts every base by `p` leaves while preserving equality. These `p` base residues cover every `t≥p−1`, proving the theorem.

For `p=7`, `g=3`, the first short cycle has hub order `1,3,2,6,4,5` and displaced leaf order `2,6,4,5,1,3`; even edges have difference classes `2,3,1` and odd edges `1,2,3`. The [diagram](art/prime_two_leaf_growth.svg) shows this first move. The [checker](34_prime_two_leaf_growth.py) constructs **every odd base** at each of the 23 primes `p≡3 (mod 4)` from 7 through 199, checking cycle simplicity, exact spoke coverage, and part counts. An independent read-only audit checked the algebraic square seed, the one-step matching conditions, the translated-cycle intersection, and sequential examples through `p=43`.

**Boundary.** The standard [offset square seed](10_odd_hub_blocks.md) cannot initiate this specific growth move for `p≥5`: all its full cycles have the same hub order, and deleting one hub leaves a path whose only perfect matching would have to serve both new leaves. The affine seed avoids that obstacle. For primes `p≡1 (mod 4)`, the multiplicative cycles above put both appearances of a difference class at the same index parity; that rules out this construction, not the target formula or other growth moves.
