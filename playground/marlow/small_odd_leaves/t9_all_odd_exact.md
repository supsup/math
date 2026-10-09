# Nine leaves: an exact partition for every odd number of hubs

Let `d(K_(p,9))` be the minimum number of singleton edges and simple cycles in an edge partition of the complete bipartite graph with `p` hubs and nine leaves. Then

```text
d(K_(p,9)) = p + ceil(4p/9)       for every odd p >= 9.
```

Each hub has odd degree nine, so any such partition has at least one singleton spoke at each hub. If there are `s >= p` singleton edges and `c` cycles, then `18c >= 9p-s`, since a simple cycle has at most nine hubs and nine leaves. Thus `s+c >= s+ceil((9p-s)/18) >= p+ceil(4p/9)`. The last inequality follows because increasing `s` by one can reduce the ceiling term by at most one.

The literal finite certificates are in [t9_odd_base_cycles.json](t9_odd_base_cycles.json). For each listed odd `m`, a row `[H,L]` describes the alternating simple cycle `H[0],L[0],H[1],L[1],...,H[-1],L[-1],H[0]`. Its two edges at leaf `L[i]` are `(H[i],L[i])` and `(H[(i+1) mod |H|],L[i])`. The uncovered edges are the singleton spokes. The [independent checker](t9_odd_base_check.py) verifies each row is a simple cycle, no cycle edge repeats, the complement has exactly one edge at each hub, and the cycles plus singleton edges partition all `9m` edges.

| Base hubs `m` | Cycles | Cycle lengths | Singleton leaves |
| ---: | ---: | --- | --- |
| 9 | 4 | four 18 | one at each leaf |
| 11 | 5 | four 18, one 16 | three at leaf 0; one elsewhere |
| 13 | 6 | four 18, two 16 | three at leaves 0–1; one elsewhere |
| 15 | 7 | four 18, three 16 | three at leaves 0–2; one elsewhere |
| 17 | 8 | four 18, four 16 | three at leaves 0–3; one elsewhere |
| 19 | 9 | four 18, five 16 | three at leaves 0–4; one elsewhere |
| 21 | 10 | four 18, six 16 | three at leaves 0–5; one elsewhere |
| 23 | 11 | four 18, seven 16 | three at leaves 0–6; one elsewhere |
| 25 | 12 | four 18, eight 16 | three at leaves 0–7; one elsewhere |

These nine bases represent every odd residue modulo 18. For any odd `p >= 9`, let `b` be the base with `p ≡ b (mod 18)`; necessarily `p=b+18r` with `r>=0`. Place the `b`-hub certificate and `2r` copies of the nine-hub certificate on disjoint sets of hubs, all using the same nine leaves. Edges from different hub blocks are disjoint. The resulting cycle count is `ceil(4b/9)+8r = ceil(4p/9)` and there is one singleton at every hub. This reaches the lower bound.

The nine-hub certificate also has a direct formula. Number hubs and leaves modulo nine. For each `a` in `1,3,5,7`, take `H[i]=-i mod 9`, `L[i]=a-i mod 9` for `i=0,...,8`. That cycle uses spoke differences `a` and `a+1`; the four cycles use all nonzero differences once, leaving `(h,h)` as the nine singletons.

Provenance: this addition is stacked on the frozen parent tip `b19f78c`, which proves the exact `t=1,3,5,7` cases. The `m=11,...,25` cycle rows were found on 2026-10-09 by a local OR-Tools CP-SAT search. It fixed singleton `(h,h)` for `0<=h<9` and assigned each extra hub pair `(9+2j,10+2j)` singleton leaf `j`. The degree constraints required each hub to occur in four cycles, each present leaf to have degree two in its cycle, four nine-leaf cycles, and one eight-leaf cycle omitting each `j`; disconnected cycle candidates were excluded by iterative component cuts. The JSON stores the concrete output. The [recovered search script and fresh replay](t9_odd_base_search_provenance.md) document how comparable blocks were found; the original search stdout was not saved, and exact byte-for-byte reproduction of the JSON is not claimed. The separate standard-library checker reads only that JSON, independently rebuilds the edge sets, and needs no solver. The finite certificates plus the written modulo-18 argument prove the unbounded claim; the checker's finite sample loop is supplemental.

Run from this directory:

```sh
python3 -I t9_odd_base_check.py
```

The checker also assembles and audits every edge of `K_(12289,9)`: 12,289 singletons and 5,462 cycles, for `d(K_(12289,9))=17,751`.
