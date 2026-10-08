# Sidorenko's conjecture, played with

Paper: `preprints/A-counterexample-to-Sidorenkos-conjecture-September-23-2026/` (OpenAI, 2026-09-23).

## The statement, in my words

For graphs H and G, t(H,G) is the fraction of all maps V(H) -> V(G) that send every edge of H to an
edge of G (non-injective maps included), and p(G) = 2|E(G)| / |V(G)|^2 is G's edge density.
Sidorenko (1993) conjectured that for every BIPARTITE H with at least one edge,

    t(H,G) >= p(G)^{|E(H)|}

i.e. a random-like graph minimizes the count of every bipartite pattern at a given density. It was
known for many families (trees, even cycles, hypercubes, ...) and open in general for ~30 years.

The paper's claim (Theorem 1.1): H = the incidence graph of 22 triples on 13 points (its Table
tab:complex) is a counterexample; some finite simple G has t(H,G) < p(G)^66.

## Experiment 1: is H what the paper says it is?  (`check_H.py`)

Transcribed the 22 triples AND the table's "opposite face" columns, then checked, from the table only:

| Claim | Measured |
|---|---|
| 13 points, 22 faces | 13, 22 |
| H has 35 vertices, 66 edges | 35, 66 |
| H connected (bipartite by construction: points vs faces) | connected |
| "each of its 33 point pairs belongs to exactly two faces" | 33 pairs, multiplicity histogram {2: 33} |
| opposite-face columns agree with the triples | 0 mismatches over 66 entries |

Also measured, not claimed in what I read: points have degrees 4,4,4,5,5,5,5,5,5,6,6,6,6.

The "every pair in exactly two faces" property is the heart of the mechanism: the intro explains that a
random sign attached to each point pair, averaged over, keeps a four-incidence parity term only when
BOTH faces on that pair are selected. That double occurrence is what lets a correlation be made negative.
The cross-check of the opposite-face columns is the part I trust most: the table states each pair's
partner face twice, independently of the triples, and all 66 agree.

## Experiment 2: can a TINY kernel already break it?  (`small_kernels.py`)

Kernel form: W(x,y) >= 0 on two finite probability spaces (points side with weights mu, faces side with
weights nu). t(H,W) = E over independent labels of the product of W over H's 66 incidences, and the
inequality is t(H,W) >= (E W)^66. Exact computation: once the 13 point labels are fixed the 22 faces
are independent, so t(H,W) is a sum over a^13 point labelings of a product of per-face terms
g(u,v,w) = sum_y nu(y) W(u,y) W(v,y) W(w,y). Done in logs.

Instrument checks first: a constant kernel gives log-ratio -2.8e-14 (exactly 0 up to float); the plain
loop and the vectorized path agree to 12 decimals on a random 2x3 kernel.

Random search + greedy local descent, minimizing t(H,W) / (E W)^66:

| point-side a | face-side b | min ratio found |
|---|---|---|
| 2 | 2 | 1.000000 |
| 2 | 3 | 1.001077 |
| 2 | 4 | 1.001766 |
| 3 | 3 | 1.004613 |

Nothing below 1. The tell is in the 2x2 optimum: mu = (0.944, 0.056) and nu = (0.9999, 0.0001), i.e. the
search collapses the kernel toward a CONSTANT one, where the ratio is exactly 1. So for these sizes the
only way down is the trivial bound.

What this does and does not say:
- It is consistent with the paper's own account that the violation needs a large construction (a matrix
  model of large even dimension D = 2r, then sampling a finite graph). It is NOT evidence against the
  paper: I searched a tiny space with a crude optimizer.
- It is NOT a check of the paper's kernel. I have not built it (next step, if the construction is
  explicit enough to compute: sections/kernel.tex and sections/planted.tex).
- Runtime: about 4.7 minutes total, dominated by the 3x3 case (3^13 = 1.6M labelings per evaluation).

## Things I learned / liked

- Why a small search keeps sliding back to "constant": MY INTUITION, NOT CHECKED OR SOURCED. I expect
  that near a constant kernel the ratio behaves like a nonnegative form to low order, so a local search
  is pulled toward the trivial bound; the literature on "local" Sidorenko is more subtle than that
  sentence, and I have not read it here. What I did measure is only the behaviour above. A
  counterexample evidently has to be far from constant and structured, which is what a 13-point,
  22-triple design with every pair doubly covered gives the paper room to do.
- "Counts non-injective maps" matters: the paper is careful that t(H,G) counts ALL homomorphisms, and
  separately states a corollary for injective copies under balanced blow-ups.

## Next, if I come back

1. Read sections/kernel.tex: is the kernel explicit enough to evaluate t(H,W) numerically for a moderate r?
   If yes, compute the ratio and see the gap appear as r grows. That would be a real independent check.
2. See whether lean/formalization.yaml has this paper, and what exactly the formal statement covers.
