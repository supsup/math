# Exact cycle partitions of complete bipartite graphs

Write `d(K_(p,t))` for the fewest singleton edges and simple cycles that partition the edges of the complete bipartite graph. The [all-parity theorem](all_bipartite_parity_bound.md) now gives an exact formula for every positive `p,t`:

```text
m=min(p,t), s0=max(p if t is odd else 0, t if p is odd else 0)
d(K_(p,t))=s0+ceil((p*t-s0)/(2*m)).
```

The construction uses the [uniform odd-leaf proof](odd_all_leaves_uniform.md) for **every odd `p>=t>=3`**,

```text
d(K_(p,t)) = p + ceil(p(t-1)/(2t)).
```

At `t=1`, all `p` spokes are singletons, so the same formula gives `d(K_(p,1))=p`. Primality is unnecessary. The proof uses an explicit cyclic weave, a two-edge switch, and a `2t`-hub lift; it needs no solver or existence theorem. The [large-leaf corollary](odd_hubs_large_leaves_uniform.md) supplies the remaining odd-hub cases, including even `t>p`, and the all-parity theorem applies the symmetric cases and an even-even weave.

Each hub has odd degree `t`, so it needs at least one incident singleton edge. With `s>=p` singletons, each simple cycle has at most `2t` edges, giving at least `s+ceil((pt-s)/(2t))` parts. This is nondecreasing in integer `s`; at `s=p` it gives the displayed lower bound. The uniform construction supplies exactly one singleton per hub and the required number of simple cycles. Its seed blocks are formulaic for every odd `t`, including odd composite hub counts.

The [prime-order shift-pair theorem](prime_shift_pair_all_primes.md) gives a sharper cycle profile for `K_(p,p+1+tp)` at every prime `p>=5` and integer `t>=0`: one `p-1`-cycle and all remaining cycles Hamiltonian. Its [independent skeptical audit](prime_shift_pair_all_primes_skeptical_audit.md), [producer checker](prime_shift_pair_all_primes_check.py), and [separate exact-edge checker](prime_shift_pair_all_primes_independent_check.py) accompany the proof. Fixpoint's exact-tip review is pending; this branch makes no showcase edit.

The earlier finite packets remain useful independent controls and show how the result emerged:

| Odd leaves `t` | Exact value for odd `p>=t` | Earlier construction |
| ---: | --- | --- |
| 1 | `p` | every spoke is a singleton |
| 3 | `p+ceil(p/3)` | hub triples and pairs in the [small-leaf note](p12289_small_leaf_exact.md) |
| 5 | `p+ceil(2p/5)` | finite 4-, 5-, 7-, and 9-hub blocks in the [five-leaf proof](odd_t5_exact_blocks.md) |
| 7 | `p+ceil(3p/7)` | finite blocks and a modulo-14 lift in the [seven-leaf proof](t7_all_odd_exact.md) |
| 9 | `p+ceil(4p/9)` | nine literal bases and a modulo-18 lift in the [nine-leaf proof](t9_all_odd_exact.md) |

At `p=12289`, the formula gives the following sample values:

| `t` | singletons | cycles | `d(K_(12289,t))` |
| ---: | ---: | ---: | ---: |
| 1 | 12289 | 0 | 12289 |
| 3 | 12289 | 4097 | 16386 |
| 5 | 12289 | 4916 | 17205 |
| 7 | 12289 | 5267 | 17556 |
| 9 | 12289 | 5462 | 17751 |
| 11 | 12289 | 5586 | 17875 |

The [uniform checker](odd_all_leaves_uniform_check.py) rebuilds every spoke and every cycle for all 650 nonzero seed blocks at odd `t=3,...,51`. A [separately written edge-multiset replay](odd_all_leaves_uniform_independent_replay.py) checks all 2,550 nonzero seeds through odd `t=101`, while the [skeptical audit](odd_all_leaves_uniform_skeptical_audit.md) re-derives the row assignment, switch connectivity, lower bound, and unbounded lift. A second [adversarial proof audit](odd_all_leaves_uniform_peer_audit.md) and [independent checker](odd_all_leaves_uniform_peer_check.py) cover 665 cases, including large-leaf boundary seeds. The finite checks corroborate the written proof; they do not set its range. The earlier five-, seven-, and nine-leaf certificates and independent replays remain intact at the parent reviewed tip.

Run from this directory:

```sh
python3 -I odd_all_leaves_uniform_check.py
python3 -I odd_all_leaves_uniform_independent_replay.py
python3 -I odd_all_leaves_uniform_peer_check.py
python3 -I odd_hubs_large_leaves_uniform_check.py
python3 -I odd_hubs_all_t_independent_replay.py
python3 -I all_bipartite_parity_bound_check.py
python3 -I prime_shift_pair_all_primes_check.py
python3 -I prime_shift_pair_all_primes_independent_check.py
python3 -I odd_t5_edge_check.py
python3 -I odd_t5_skeptical_replay.py
python3 -I t7_all_odd_blocks_check.py
python3 -I t7_all_odd_independent_replay.py
python3 -I t9_odd_base_check.py
python3 -I t9_odd_independent_replay.py t9_odd_base_cycles.json
```

The fixed-prime result for `p=12289` and `t>=12288` remains a separate structured certificate. The [small-leaf boundary](odd_hub_small_leaf_boundary.md) explains why its large-leaf formula cannot extend below `t=p-1`. This branch makes no showcase edit; Fixpoint owns the independent review and card wording.
