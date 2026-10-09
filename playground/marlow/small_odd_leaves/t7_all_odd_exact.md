# Seven leaves: exact value for every odd number of hubs at least seven

For edge partitions into singleton edges and simple cycles,

```text
d(K_(p,7)) = p + ceil(3p/7)       for every odd p >= 7.
```

The parity lower bound is proved in [the existing certificate](p12289_t7_odd_block_certificate.md): each hub needs at least one singleton spoke, and each cycle has at most fourteen edges. It remains to construct a partition with exactly `p` singleton spokes and `ceil(3p/7)` cycles.

The existing `K_(6,7)`, `K_(7,7)`, and `K_(11,7)` blocks have respectively `3`, `3`, and `5` cycles, with exactly one singleton spoke at each hub. A new `K_(9,7)` block has three 14-cycles and one 12-cycle. In the table, a row `(H; L)` denotes the alternating cycle `H[0], L[0], H[1], L[1], ..., H[-1], L[-1], H[0]`.

| Hubs in cyclic order | Leaves in cyclic order |
|---|---|
| `0 2 4 3 1 6 5` | `3 0 2 1 4 6 5` |
| `0 8 7 4 5 6 1` | `4 5 6 1 0 3 2` |
| `2 6 7 8 5 4 3` | `2 1 0 3 4 5 6` |
| `0 8 7 3 2 1` | `1 2 3 4 5 6` |

Its nine uncovered edges, used as singleton spokes, are `(0,0), (1,0), (2,1), (3,0), (4,3), (5,2), (6,5), (7,4), (8,6)`. The checker below verifies that every cycle is simple, all cycle edges are distinct, and these are precisely the missing edges.

These seven odd bases cover all odd residues modulo 14. The cycle counts in the last column equal `ceil(3b/7)`.

| Base `b` | Block sizes | Cycles |
|---:|---|---:|
| 7 | `7` | 3 |
| 9 | `9` | 4 |
| 11 | `11` | 5 |
| 13 | `6+7` | 6 |
| 15 | `6+9` | 7 |
| 17 | `6+11` | 8 |
| 19 | `6+6+7` | 9 |

For any odd `p >= 7`, choose the unique base `b` in the table with `p ≡ b (mod 14)`. Then `p=b+14k` for an integer `k>=0`. Use the blocks for `b` plus `2k` disjoint seven-hub blocks, all sharing the same seven leaves. Hubs in different blocks have disjoint edges. The construction has exactly `p` singleton spokes and `ceil(3b/7)+6k = ceil(3p/7)` cycles, proving the claim.

The search also found a `K_(10,7)` block with five 12-cycles, again with one singleton spoke at each hub:

| Hubs in cyclic order | Leaves in cyclic order |
|---|---|
| `0 3 4 1 2 5` | `4 3 1 5 0 6` |
| `1 9 8 6 5 4` | `6 1 0 5 4 2` |
| `0 2 8 3 9 7` | `3 6 5 0 2 1` |
| `2 5 7 4 6 8` | `1 3 0 6 2 4` |
| `0 1 7 9 6 3` | `0 4 5 3 1 2` |

Its singleton complement is `(0,5), (1,3), (2,2), (3,6), (4,5), (5,2), (6,4), (7,6), (8,3), (9,4)`. This block is independently useful, although the odd-`p` proof above does not need it.

Run `python3 t7_all_odd_blocks_check.py`. The self-contained checker audits the old and new finite blocks and the seven base decompositions. Its finite loop through odd `p<1000` is supplementary; the modulo-14 argument proves the unbounded statement.
