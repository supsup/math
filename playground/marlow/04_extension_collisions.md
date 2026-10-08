# How many forbidden copies appear at the cycle–triangle boundary?

**Scope.** This is a conditional one-vertex extension count, not the unrestricted Ramsey multiplicity of all colorings at `K_{2m−1}`. Start from either of the two `R(C_m,K_3)`-critical colorings of `K_{2m−2}` classified by [Radziszowski and Jin (1994), Theorem 3](https://www.cs.rit.edu/~spr/PUBL/paper30.pdf): two red `K_{m−1}`s with zero or one red bridge. Add a new vertex and color every new edge arbitrarily. Count each red `C_m` once by its undirected edge set, and each blue `K_3` once by its vertex set. All forbidden copies must use the new vertex because the starting coloring is safe.

**Finding.** For every `m≥6`, every such extension has at least **`(m−2)^2`** forbidden copies in total. This is sharp for *both* critical types. My exhaustive small-case counts are:

| `m` | no bridge: minimum | one bridge: minimum | attachments per type |
| ---: | ---: | ---: | ---: |
| 4 | 3 | 2 | 64 |
| 5 | 8 | 9 | 256 |
| 6 | 16 | 16 | 1024 |

The `m=4,5` values are finite enumerations, not consequences of the `m≥6` formula. These are counts of forbidden *subgraphs*, not just the statement that at least one appears. I have not established whether this exact extension minimum was previously known; the underlying critical coloring classification certainly was.

## Proof for `m≥6`

Put `k=m−1≥5` and `q=(k−2)!`. Let the new vertex have `a` red neighbors in the first red `K_k` and `b` in the second. With **no bridge**, the number of new red `C_{k+1}`s is

`q [binom(a,2)+binom(b,2)]`.

Indeed, any such cycle lies in one block plus the new vertex, uses all `k` vertices of that block, chooses its two endpoints among the new red neighbors, and orders the other `k−2` clique vertices. The number of new blue triangles is `(k−a)(k−b)`, since each needs one blue neighbor of the new vertex from each block. Thus the total is

`F(a,b)=q [binom(a,2)+binom(b,2)] + (k−a)(k−b)`.

For `k≥5`, `q>k`. Holding `b` fixed, the difference `F(a+1,b)−F(a,b)=qa−(k−b)` is negative from `a=0` to `1` unless `b=k`, and strictly positive for every `a≥1`. The same holds with `a,b` exchanged. Moving each coordinate to `1` never raises `F`; the only possible tie in the first move when the other coordinate is `k` disappears when that coordinate is moved to `1`. Therefore the unique minimum occurs at `a=b=1`, and equals `(k−1)^2=(m−2)^2`. It is attained by choosing one red neighbor in each block; then no red `C_m` appears and exactly `(k−1)^2` blue triangles appear.

With **one bridge** `x–y`, where `x` lies in the first block and `y` in the second, the red within-block cycles above remain. The bridge deletes at most one of the blue triangles counted by `F`, namely the triangle using the new vertex and `x,y`; denote that possible subtraction by `I∈{0,1}`. Other new red cycles can only add to the total. When `(a,b)≠(1,1)`, `F(a,b)` is an integer strictly above `(k−1)^2`, so even subtracting one cannot go below the claimed bound. When `(a,b)=(1,1)` and `I=1`, the new red neighbors `u,w` are distinct from `x,y`, respectively. There is a red `C_m` following

`new → u → x → [a y–w path on k−2 vertices of the second clique] → new`.

That extra red cycle compensates for the one deleted blue triangle. When `I=0`, `F` alone gives the bound. Sharpness for the bridge type comes from making `x` and `y` the new vertex's only red neighbors: the red cross structure then forms only a triangle, while the remaining `(k−1)^2` blue cross pairs give that many blue triangles.

## Reproduction and limits

Run `python3 -I playground/marlow/04_extension_collisions.py` from the repo root. For `m=4,5,6`, it generates every undirected `C_m` edge mask and every triangle mask on `K_{2m−1}`, tries every new-vertex attachment for both critical types, counts forbidden copies, asserts the minima in the table, and regenerates [the chart](art/extension_collisions.svg). This check could fail by finding a smaller total in any of the 2,688 tested attachments, or by disagreeing with the analytic `m=6` bound; neither happened. A separate skeptical audit used an adjacency-based depth-first cycle search and reproduced all six minima; it also found no gap in the general proof. The proof uses the published critical-type classification as input and the elementary count above. It says nothing about arbitrary colorings of `K_{2m−1}` whose `K_{2m−2}` restriction was already noncritical.

**Possible use.** A lower bound on the number of violations can help quantify how abruptly a finite Ramsey constraint becomes unsatisfiable when a vertex is added to a tight witness. A SAT or graph-search implementation could use the count to check explanations or rank near-solutions, but no speedup is measured. Prior art on threshold Ramsey multiplicity exists for other settings; I have not found this exact conditional count in the sources checked, so novelty remains unverified.
