# Skeptical audit of the five-leaf partition claim

**Verdict:** The literal 4-, 5-, 7-, and 9-hub blocks partition their respective
complete bipartite graphs. Together they attain the parity lower bound for
every odd `p>=5`, including `p=12289`. I found no omitted exception.

The separate [replay](odd_t5_skeptical_replay.py) reads the 4-, 7-, and 9-hub
singleton rules and cycle rows directly from
[the claim](odd_t5_exact_blocks.md), and derives the 5-hub rows from its
displayed formula. It imports no data or functions from the claim's checker.
It reconstructs every closed alternating vertex walk, checks vertex
distinctness, and counts each hub-leaf edge. The per-block results are:

| hubs | singleton edges | cycle lengths | cycle edges | total edges |
|---:|---:|---|---:|---:|
| 4 | 4 | 8, 8 | 16 | 20 |
| 5 | 5 | 10, 10 | 20 | 25 |
| 7 | 7 | 10, 10, 8 | 28 | 35 |
| 9 | 9 | 10, 10, 8, 8 | 36 | 45 |

Every edge appears exactly once in each block. Translating disjoint hub
labels preserves this property. In the four-hub block, each hub has singleton
leaf 4; its first cycle supplies leaves `j,j+1 mod 4` and its second supplies
`j+2,j+3 mod 4`. Consequently the `7+4` assembly for `p=11` has 11
singletons and 5 cycles, giving `d(K_(11,5))=16`, while `9+4` for `p=13`
has 13 singletons and 6 cycles, giving `d(K_(13,5))=19`.

The replay checks both the stated
`9+2456*5=12289` assembly and the 5/7-block residue assembly at `p=12289`.
Both have 12289 singletons and 4916 cycles, hence 17205 parts. The first
assembly has `36+2456*20=49156` cycle edges, leaving 12289 singleton edges;
their sum is `5*12289=61445`.

For the lower bound, every hub has degree five. Removing cycles leaves an
odd number of singleton edges at each hub, so their total `s` is at least
`p`. A simple cycle uses at most five distinct leaf vertices and thus at
most ten edges. With `c` cycles, `c>=ceil((5p-s)/10)`. The expression
`s+ceil((5p-s)/10)` is nondecreasing in integral `s`; therefore the number
of parts is at least `p+ceil(2p/5)`. At `p=12289`, this is
`12289+ceil(24578/5)=17205`.

The 5/7-block representation has one residue choice `b` in `0..4`, where
`p=5a+7b`. The smallest eligible odd `p` for each choice is:

| `p mod 10` | `b` | first `p>=15` with `a>=0` |
|---:|---:|---:|
| 5 | 0 | 15 |
| 7 | 1 | 17 |
| 9 | 2 | 19 |
| 1 | 3 | 21 |
| 3 | 4 | 33 |

Increasing `p` by ten increases `a` by two, so these rows cover every odd
`p>=15` except `p=23`. The given `9+7+7` block split covers 23 with
`4+3+3=10=ceil(46/5)` cycles. For the five regular residue choices,
`2a+3b=(2p+b)/5=ceil(2p/5)`. The replay also checks the arithmetic for
each odd `p` from 5 through 103, including the `p=11,13` extension. The
finite check is corroboration; the residue argument plus the small blocks
establishes the unbounded claim.

I ran `python3 -I odd_t5_skeptical_replay.py` and
`python3 -I odd_t5_exception_extension_check.py`; both completed
successfully. The latter is the separately authored
[extension checker](odd_t5_exception_extension_check.py), which I inspected
and ran as an additional cross-check.
