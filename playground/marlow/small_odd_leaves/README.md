# Exact odd-leaf partitions through nine

Write `d(K_(p,t))` for the fewest singleton edges and simple cycles that partition the edges of the complete bipartite graph. This research packet proves, for **every odd integer `p>=max(3,t)`** at each indicated odd `t`,

| Leaf count `t` | Exact value | Construction |
| ---: | --- | --- |
| 1 | `p` | every spoke is a singleton |
| 3 | `p+ceil(p/3)` | hub triples and pairs in the [small-leaf note](p12289_small_leaf_exact.md) |
| 5 | `p+ceil(2p/5)` | finite 4-, 5-, 7-, and 9-hub blocks plus a residue argument in the [five-leaf proof](odd_t5_exact_blocks.md) |
| 7 | `p+ceil(3p/7)` | finite 6-, 7-, 9-, and 11-hub blocks plus a modulo-14 lift in the [seven-leaf proof](t7_all_odd_exact.md) |
| 9 | `p+ceil(4p/9)` | nine literal base certificates and a modulo-18 lift in the [nine-leaf proof](t9_all_odd_exact.md) |

Primality is unnecessary. The formulas hold in the stated range; this packet does not claim an exact value for odd leaf counts `t>=11` or for odd `t>p`.

The common lower bound is `p+ceil(p(t-1)/(2t))`. Each of the `p` hubs has odd degree `t` and therefore needs at least one incident singleton edge. If there are `s>=p` singletons, each simple cycle has at most `2t` edges, so the part count is at least `s+ceil((pt-s)/(2t))`, a nondecreasing function of integer `s`. Taking `s=p` gives the displayed bound. The cited constructions attain it, using exactly one singleton spoke at each hub; their cycles may share leaves across different hub blocks because their **edges** remain disjoint.

At `p=12289`, the exact small odd values are:

| `t` | singletons | cycles | `d(K_(12289,t))` |
| ---: | ---: | ---: | ---: |
| 1 | 12289 | 0 | 12289 |
| 3 | 12289 | 4097 | 16386 |
| 5 | 12289 | 4916 | 17205 |
| 7 | 12289 | 5267 | 17556 |
| 9 | 12289 | 5462 | 17751 |

The [five-leaf author checker](odd_t5_edge_check.py) and [separately written skeptical replay](odd_t5_skeptical_replay.py) check all literal block edges, every odd `p` through the stated finite control range, and two full `p=12289` assemblies. The [four-hub extension checker](odd_t5_exception_extension_check.py) separately verifies the cases `p=11,13`. For seven leaves, the [block checker](t7_all_odd_blocks_check.py) verifies all five finite blocks, the seven modulo-14 bases, and a finite range of larger `p`; a [separately written all-odd audit](t7_all_odd_skeptical_audit.md) replays every block and the residue lift, while the [fixed-prime replay](p12289_t7_odd_block_independent_replay.py) checks the `p=12289` certificate directly. For nine leaves, the [saved literal JSON](t9_odd_base_cycles.json), [standalone edge checker](t9_odd_base_check.py), and [separately written skeptical audit](t9_odd_skeptical_audit.md) cover all nine modulo-18 bases and the full fixed-p12289 assembly. The [search provenance](t9_odd_base_search_provenance.md) records the recovered CP-SAT script and a fresh replay; the solver is not needed to check the saved proof certificate. The unbounded claims rest on the written residue proofs, not on the finite loops.

Run from this directory:

```sh
python3 -I odd_t5_edge_check.py
python3 -I odd_t5_exception_extension_check.py
python3 -I odd_t5_skeptical_replay.py
python3 -I t7_all_odd_blocks_check.py
python3 -I t7_all_odd_independent_replay.py
python3 -I p12289_t7_odd_block_independent_replay.py
python3 -I t9_odd_base_check.py
python3 -I t9_odd_independent_replay.py t9_odd_base_cycles.json
```

The large-leaf fixed-prime result at `p=12289`, `t>=12288`, is a separate certificate and review question. The [small-leaf boundary](odd_hub_small_leaf_boundary.md) explains why that large-leaf formula cannot simply extend below `t=p-1`. This packet does not edit the showcase; Fixpoint owns the review and any card wording.
