# Exact value at seven leaves for 12,289 hubs

For an edge partition into singleton edges and simple cycles,

```text
d(K_(12289,7)) = 12289 + ceil(3·12289/7) = 17556.
```

The lower bound is the odd-leaf parity bound in [the small-leaf note](p12289_small_leaf_exact.md): every one of the 12,289 hubs has odd degree seven, so at least one incident edge must be a singleton. If there are `s` singleton edges and `c` cycles, each cycle has at most fourteen edges, giving `c >= ceil((7p-s)/14)`. The resulting bound `s+c` is nondecreasing for `s>=p`, and at `s=p` it is `p+ceil(3p/7)`.

Here are three finite blocks, with hubs labelled `H_0,...,H_(m−1)` and the common leaves `L_0,...,L_6`. Each table row `(h_0 ... h_(r−1); l_0 ... l_(r−1))` is the simple cycle

```text
H_(h_0), L_(l_0), H_(h_1), L_(l_1), ..., H_(h_(r−1)), L_(l_(r−1)), H_(h_0).
```

The `K_(7,7)` block has seven singleton edges `(H_i,L_i)`. For each `a` in `{1,3,5}`, take a 14-cycle with hub sequence `h_k = −k (mod 7)` and leaf sequence `l_k = h_k+a (mod 7)`, for `k=0,...,6`. Its edges have offsets `a` and `a+1`; the three cycles therefore cover all six nonzero offsets exactly once.

An auxiliary `K_(6,7)` block has three 12-cycles:

| Hubs in cyclic order | Leaves in cyclic order |
|---|---|
| `2 4 5 1 3 0` | `2 6 3 5 1 4` |
| `1 2 3 4 0 5` | `6 3 4 0 5 2` |
| `1 5 2 4 0 3` | `4 1 5 3 6 0` |

Their 36 edges are distinct. The six unused singleton edges are `(0,2), (1,1), (2,0), (3,2), (4,1), (5,0)`, where `(h,l)` means `H_h L_l`. Thus three leaves receive two singleton spokes each, preserving even residual degree there. This block is a valid local gadget, although it is not needed for `p=12289`.

The needed `K_(11,7)` block has three 14-cycles followed by two 12-cycles:

| Hubs in cyclic order | Leaves in cyclic order |
|---|---|
| `8 10 3 4 9 5 0` | `2 1 0 5 3 6 4` |
| `1 5 9 0 6 4 10` | `1 4 0 3 2 6 5` |
| `6 0 5 10 1 2 7` | `1 2 0 3 6 4 5` |
| `3 6 1 2 8 7` | `6 4 0 1 3 2` |
| `4 2 9 7 8 3` | `3 2 1 0 5 4` |

Their 66 edges are distinct. The eleven unused singleton edges are

```text
(0,5), (1,2), (2,5), (3,3), (4,1), (5,5),
(6,0), (7,6), (8,6), (9,6), (10,4).
```

Partition the 12,289 hubs into 1,754 disjoint groups of seven and one group of eleven, since `12289 = 1754·7+11`. Apply the seven-hub construction to every seven-hub group and the eleven-hub certificate to the last group, always using the same seven leaves. Different groups have disjoint edge sets. This produces `1754·7+11 = 12289` singleton edges and `1754·3+5 = 5267` cycles, attaining the lower bound. Every part is a singleton or a simple cycle, and every edge is used once.

Run [the finite checker](p12289_t7_odd_block_check.py) with `python3 p12289_t7_odd_block_check.py`. It audits every listed local edge, the singleton complements, and the full 86,023-edge partition.
