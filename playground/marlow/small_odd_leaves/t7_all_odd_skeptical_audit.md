# Skeptical audit: seven leaves and every odd hub count

**Verdict: the stated formula is supported for every odd `p >= 7`.** I independently parsed the literal `K_(9,7)` and `K_(10,7)` rows from [the extension](t7_all_odd_exact.md), the `K_(6,7)` and `K_(11,7)` rows from [the earlier certificate](p12289_t7_odd_block_certificate.md), and generated the `K_(7,7)` rows from its modular formula. [My standalone replay](t7_all_odd_independent_replay.py) imports neither published checker. It checks alternating closed walks, local complements, every claimed residue base as a complete edge partition, and a translated add-14 step for each base; all assertions pass.

For the lower bound, each hub has degree seven. Cycles contribute even degree at each vertex, so every hub needs at least one singleton spoke and `s >= p`. A simple cycle visits at most seven leaves and therefore has at most fourteen edges. Thus `c >= ceil((7p-s)/14)`. The integer function `s + ceil((7p-s)/14)` is nondecreasing in `s`, yielding `s+c >= p+ceil(3p/7)` for every `p` in the claim.

| Local block | Cycle lengths | Distinct cycle edges | Singleton complement |
|---|---|---:|---|
| `K_(6,7)` | `12,12,12` | 36 | six stated pairs, once per hub |
| `K_(7,7)` | `14,14,14` | 42 | diagonal `(h,h)`, once per hub |
| `K_(9,7)` | `14,14,14,12` | 54 | nine stated pairs, once per hub |
| `K_(10,7)` | five `12`-cycles | 60 | ten stated pairs, once per hub |
| `K_(11,7)` | `14,14,14,12,12` | 66 | eleven stated pairs, once per hub |

In each block, every row has distinct hubs and distinct leaves, so its closed alternating walk is a simple cycle. Every consecutive edge, including the closing edge, lies in the block; no cycle edge repeats. The computed missing-edge set equals the claimed singleton set exactly. The ten-hub block checks out but is not needed for the odd-`p` proof.

The seven bases `7,9,11,13,15,17,19` occupy residues `7,9,11,13,1,3,5` modulo 14, respectively. Their block sizes sum to each base, and direct translated-edge replay verifies complete partitions with cycle counts `3,4,5,6,7,8,9`, respectively. These equal `ceil(3b/7)`; there is no overlap even though every block uses the same seven leaf vertices, because its hub interval is disjoint.

Every odd `p >= 7` has exactly one such base `b` with `p = b + 14k`, `k >= 0`. Adding two seven-hub blocks per step adds 14 hubs, 14 singleton spokes, and six 14-cycles. The exact arithmetic is `ceil(3(p+14)/7) = ceil(3p/7)+6`. The blocks' translated edge sets remain disjoint, so the finite base checks and this identity prove the unbounded construction. I found no gap in the all-odd claim.
