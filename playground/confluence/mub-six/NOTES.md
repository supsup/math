# Mutually unbiased bases in C^6 (Comparator: MUBSix, family 266)

## Statement (read by Confluence)

`OAI.MUB6.fourier_and_family_bound` has two conjuncts:
1. For every order-6 complex Hadamard matrix H (unimodular entries, H*H = 6I) NOT equivalent to Tao's matrix (full
   equivalence: row and column permutations and unit phases on both sides), and every coordinate permutation pi,
   the normalised character sum g H (alpha . pi) is 0, with alpha = (1, 1, 1, -1, -1, -1).
2. `Attainable n -> n <= 5`: there are no 6 mutually unbiased orthonormal bases of C^6. `IsMUBFamily` is the plain
   definition (|<b, b'>|^2 = 1/6 for vectors of different bases); `Basis` is Mathlib's OrthonormalBasis of
   EuclideanSpace C (Fin 6). No restricted model.

## Relation to the paper and to the open problem

- docs/266: the paper claims at most THREE; "the selected statement does not establish the paper's upper bound of
  three or its computer-assisted exclusion of four arbitrary bases". So the row is NARROWER than the paper.
- But conjunct 2 is strong on its own: six MUBs in dimension d force a complete set of d + 1 (a known result, from
  my knowledge, not re-checked here), so "at most 5" rules out a complete set of 7 in C^6, which was (as of my
  knowledge, before August 2026) a famous open question. Same cutoff caveat as the Crouzeix correction: the novelty
  framing needs a source check before it goes on a public card.

## Lean check (Docker, my own run)

- Cone: 3,381 modules, Mathlib only (`lean-cones/cones.py`). Build ran about two and a half hours.
- `Build completed successfully (12305 jobs)`.
- `'OAI.MUB6.fourier_and_family_bound' depends on axioms: [propext, Classical.choice, Quot.sound]`; sorry control
  `[sorryAx]`. No `Lean.ofReduceBool`, so no `native_decide`: the case analysis was checked by the kernel itself.
- statement_match 17/17.
- Log: `../lean-docker/mubsix-run.log`.

## Limits

- One reading (mine); the trust card needs a second.
- Not the official Comparator run; the match is textual.
- The proof's mathematics (and whatever computation the 3,381 modules encode) is the kernel's word only.
