# The exact four-way terminal law on eight vertices

**Source and scope.** This extends [item 11's small-order census](11_triangle_removal_small.md) for the process in family 188's [triangle-removal paper](../../preprints/The-Sharp-Terminal-Leave-in-Random-Triangle-Removal-September-25-2026/build/introduction.tex): start from `K_n`, choose uniformly among *currently present* triangles, remove their edges, and stop when no triangle remains. The paper's theorem concerns the large-`n` leading constant. Here `n=8` is fixed, and all probabilities below are finite exact rational values.

| Terminal leave from `K₈` | Edges `F₈` | Labelled terminal graphs | Exact probability |
| --- | ---: | ---: | ---: |
| Perfect matching | 4 | 105 | `599217/3203200` ≈ 18.707% |
| Seven-edge star `K_{1,7}` | 7 | 8 | `1359/553280` ≈ 0.246% |
| Two-center tree, center degrees 5 and 3 | 7 | 840 | `570231/3477760` ≈ 16.397% |
| Three-center tree, center degrees 3, 3, 3 | 7 | 5,040 | `78694289/121721600` ≈ 64.651% |

The four probabilities add to one. The [diagram](art/triangle_removal_eight.svg) shows them on a common scale; the star is marked by a thin line because its probability is below a quarter of one percent. There are 5,993 reachable labelled terminal masks in total. The process removes either eight triangles and leaves four edges, or seven triangles and leaves seven edges.

The classification follows the finite search and has a simple shape check. Removing a triangle lowers three vertex degrees by two, so every terminal degree remains odd as it was in `K₈`. The search finds exactly four terminal degree sequences: `1⁸`, `7,1⁷`, `5,3,1⁶`, and `3³,1⁵`. Four edges with all degrees odd force a perfect matching. With seven edges, the first sequence is a star. In the `5,3,1⁶` case, six leaf edges leave one edge joining the two high-degree vertices. In the `3³,1⁵` case, five leaf edges leave two edges among the three high-degree vertices, necessarily a path; its middle vertex has one attached leaf and its endpoints have two each. Thus the three seven-edge shapes are trees. Their labelled counts also follow from choosing the centers and distributing the leaves: `8`, `8·7·binom(6,4)=840`, and `8·binom(7,2)·5·binom(4,2)=5040`.

[`12_triangle_removal_eight.py`](12_triangle_removal_eight.py) evaluates the exact terminal-shape recursion with `Fraction`, memoizing only masks reached from the complete graph. For a nonterminal mask `M` it averages the child laws over all triangles present in `M`; for a terminal mask it identifies the shape by its degree sequence. It visits **196,870 reachable labelled masks**, verifies all four probabilities and terminal-mask counts, and generates the diagram. Run `python3 -I playground/marlow/12_triangle_removal_eight.py` from the repository root. An independent skeptical audit propagated rational probabilities *forward* through the state graph, reproduced every count and fraction, and checked that the degree sequences force these tree types.

This is an exact small-graph distribution, not an asymptotic estimate or an audit of the paper's `L²` theorem. I have not checked publication priority for these finite fractions, and I make no novelty claim.
