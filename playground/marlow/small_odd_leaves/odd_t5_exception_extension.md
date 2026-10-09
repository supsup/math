# Four-hub extension for the remaining five-leaf cases

**Status, 2026-10-09:** The explicit certificate and separate checker below
cover `p=11,13`. The [skeptical audit](odd_t5_skeptical_audit.md) has since
independently replayed the four-hub block and both assemblies.

The lower bound for odd \(p\) is \(d(K_{p,5})\ge p+\lceil 2p/5\rceil\). Indeed, each of the \(p\) hubs has odd degree, so its incident edge partition contains an odd positive number of singleton edges. If there are \(s\ge p\) singleton edges and \(c\) simple cycles, then \(5p-s\le 10c\). Hence \(s+c\ge s+\lceil(5p-s)/10\rceil\ge p+\lceil2p/5\rceil\).

Here is a four-hub block that attains this bound. Let hubs be \(0,1,2,3\) and leaves be \(0,1,2,3,4\). Make \((j,4)\) a singleton for every hub \(j\). The other sixteen edges split into the two simple 8-cycles below. In a row \((L;H)\), the cycle runs through \(l_0,h_0,l_1,h_1,\ldots,l_{r-1},h_{r-1},l_0\).

| leaves \(L\) | hubs \(H\) |
|---|---|
| \(0,1,2,3\) | \(0,1,2,3\) |
| \(2,3,0,1\) | \(0,1,2,3\) |

At hub \(j\), the first row uses leaves \(j,j+1\pmod4\), and the second uses \(j+2,j+3\pmod4\). Thus the two rows cover each of the four nonsingleton edges at every hub exactly once. Both rows visit each hub and each of leaves \(0,1,2,3\) exactly once, so they are simple cycles.

Use this block with disjoint hub sets and the common five leaves:

* \(p=11\): the seven-hub block from [the main note](odd_t5_exact_blocks.md) and this four-hub block give eleven singletons and \(3+2=5=\lceil22/5\rceil\) cycles. Hence \(d(K_{11,5})=16\).
* \(p=13\): the nine-hub block from [the main note](odd_t5_exact_blocks.md) and this four-hub block give thirteen singletons and \(4+2=6=\lceil26/5\rceil\) cycles. Hence \(d(K_{13,5})=19\).

The [companion checker](odd_t5_exception_extension_check.py) independently checks every cycle's simplicity, every edge exactly once, and the part counts. It uses only Python's standard library and copies the seven- and nine-hub certificate data directly rather than importing project code. Run `python3 -I odd_t5_exception_extension_check.py`.
