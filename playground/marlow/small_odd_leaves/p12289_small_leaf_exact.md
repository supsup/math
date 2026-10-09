# Exact small-leaf values and parity bounds

Let `d(K_(p,t))` be the minimum number of parts in an edge partition into singleton edges and simple cycles. The following statements hold for every odd `p>=3` (primality is unnecessary). The cited [small-leaf boundary](odd_hub_small_leaf_boundary.md) established that the large-leaf target formula fails below `p−1`; this note gives exact values at `t=1,2,3` and a sharper bound throughout that range. It makes no claim about a uniform all-residue construction.

**Parity bounds.** If `s` edges are singletons and `c` parts are cycles, then every cycle has at most `2t` edges. Thus `c>=ceil((pt−s)/(2t))`. For even `t`, every leaf has odd degree `p`, so `s>=t`; for odd `t`, every hub has odd degree `t`, so `s>=p`. Since `s+ceil((pt−s)/(2t))` is nondecreasing in `s`,

```text
d(K_(p,t)) >= t+(p−1)/2                 (even t),
d(K_(p,t)) >= p+ceil(p(t−1)/(2t))       (odd t).
```

The odd bound is exact for `t=1` and `t=3`. At `t=1`, all `p` edges are singletons. At `t=3`, write `p=3x+2y` with `x` odd and `y∈{0,1,2}`: take `(x,y)=((p−r)/3,r/2)` for `r=0,2,4` according as `p≡3,5,1 (mod 6)`. Divide the hubs into `x` triples and `y` pairs. In every triple, assign one hub's singleton to each of the three leaves; the six remaining edges form one 6-cycle. In every pair, assign both singleton edges to the same leaf; the four remaining edges form one 4-cycle. These cycles partition all nonsingleton edges, and

```text
d(K_(p,3)) = p+x+y = p+ceil(p/3).
```

For even `2<=t<=p−1`, equality also holds in the even parity bound by an explicit weave. Make the `t` edges at one hub singletons; write `p−1=2M`, `t=2n`, so `1<=n<=M`. Label the residual hubs `E_r,O_r` for `r mod M` and the leaves `L_0,...,L_(2n−1)`. For each `c mod M`, take the cyclic vertex list

```text
L_0, E_c, L_1, O_c, L_2, E_(c+1), L_3, O_(c+1), ...,
L_(2n−2), E_(c+n−1), L_(2n−1), O_(c+n−1), L_0.
```

Hub indices are modulo `M`. The `n` hub pairs in each list are distinct since `n<=M`, so this is a simple `4n=2t` cycle; for `n=1` it is the 4-cycle `L_0,E_c,L_1,O_c,L_0`. As `c` ranges over `Z/M`, each fixed `E_r` is adjacent once to each leaf pair `(L_(2j),L_(2j+1))`, and each fixed `O_r` is adjacent once to `(L_(2j+1),L_(2(j+1 mod n)))`, for `j=0,...,n−1`. Each hub therefore meets every leaf exactly once over the `M` cycles. The cycles partition `K_(p−1,t)` and give `d(K_(p,t))=t+(p−1)/2`.

For `p=12289`, the exact first values are

| `t` | singletons | cycles | `d(K_(12289,t))` |
|---:|---:|---:|---:|
| 1 | 12289 | 0 | 12289 |
| 2 | 2 | 6144 four-cycles | 6146 |
| 3 | 12289 | 4095 six-cycles + 2 four-cycles | 16386 |

The [uniform odd-leaf construction](odd_all_leaves_uniform.md) now attains this lower bound for **every odd `3<=t<=p`**, including `t=5,7,9` previously covered by the companion [five-leaf](odd_t5_exact_blocks.md), [seven-leaf](t7_all_odd_exact.md), and [nine-leaf](t9_all_odd_exact.md) certificates. The even-leaf weave above covers every even `2<=t<=p-1`. These small-leaf results do not verify the separate fixed-prime all-residue packet for `t>=p-1`.
