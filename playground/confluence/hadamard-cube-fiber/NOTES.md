# HadamardCubeFiber: verification notes (2026-10-08)

Target: `OAI.HadamardSix.rowRatio_cubeFiber_sum_zero`, statement in
`lean/ComparatorChallenges/HadamardCubeFiber.lean`, solution cone `OAI.LinearAlgebra.Hadamard.Main`
(6 modules: Basic, Fourier, Equivalence, Polynomials, CubeFibers, Main; the theorem itself is proved in
CubeFibers.lean). Paper: `preprints/Exact-Fourier-certificates-for-complex-Hadamard-matrices-of-order-six-September-24-2026`
(proves the Matolcsi-Ruzsa-Weiner Fourier-vanishing conjecture; this lemma is one step of its
"cubic alternative" section).

## The statement in plain words

H is a 6x6 complex matrix. The definitions in the challenge file:

- `Unimodular H`: every entry has modulus 1.
- `IsComplexHadamard H`: unimodular and `H^* H = 6 I` (column form; for a square matrix this is
  equivalent to `H H^* = 6 I`, and the solution derives row orthogonality from it).
- `entrywiseSquare H`: the matrix of squares `H_ik^2` (entrywise, not the matrix product).
- `rowRatio H i j k = H_ik * conj(H_jk)`.
- `cubeFiber v z`: the positions k with `v_k^3 = z` (exact equality in C).

Hypotheses: (hH) H is complex Hadamard; (hs) its entrywise square is ALSO complex Hadamard; i != j;
two numbers a != b such that (hab) every cubed ratio `v_k^3` equals a or b.
Conclusion: `sum over k with v_k^3 = a of H_ik conj(H_jk) = 0`, i.e. the ratio vector sums to zero on
the fibre where its cube is a.

Why it is true (the Lean route, which I read): put v = rowRatio. hH gives `sum v_k = 0`; hs gives
`sum v_k^2 = 0`; unimodularity then forces `sum v_k^4 = 0` (Polynomials.lean). Splitting the 4th-power
sum by fibres, `v^4 = v^3 * v = a*v` or `b*v`, gives `a*S_a + b*S_b = 0`, and `S_a + S_b = 0` from the
first sum, so `(a - b) S_a = 0` and `S_a = 0`.

## The important surprise: the hypotheses pin H down to one matrix up to equivalence

The hypothesis hs is far stronger than "H is Hadamard". The paper's own Proposition (Classification of
the cubic alternative, section 03-cubic.tex) proves every H with H and H o H both Hadamard is
equivalent (row/column permutations and unit phases) to Tao's cubic matrix, whose entries are cube roots
of unity. For every such H, every row ratio has ONE cube value (a global phase cubed). So at matrix level
the theorem's conclusion is always either the full inner product of two rows (0 by orthogonality) or an
empty sum. The two-distinct-cube-values case, which is what the lemma's proof is about, never occurs
for an actual matrix: in the paper this lemma is a step INSIDE the proof that rules that case out.

Consequences for checking it:

- The brief asked for F6, the affine Fourier family, and the Dita family. All three are Hadamard but
  NONE satisfies hs (measured below), so the theorem says nothing about them. I report them as
  hypothesis-failure cases, not as confirmations.
- The genuine positive population is Tao's matrix and its equivalence class.
- The nontrivial content is checked at vector level (unit vectors with zero 1st and 2nd power sums).

This is not a defect in the statement: it is non-vacuous (Tao satisfies all hypotheses) and correctly
stated. It is a statement whose matrix-level instances are all trivial, which is a fact a reader should
know before treating "it checks out on matrices" as evidence of much.

## What I checked and how

### Lean (Docker, `../lean-docker/hadamard-run.log`)

`check.sh HadamardCubeFiber` (after `machine-free-gate.py --wait`, which returned FREE): cone 6 modules,
Mathlib-only; Lean 4.34.1; all 6 modules built; then `#print axioms`:

```
'OAI.HadamardSix.rowRatio_cubeFiber_sum_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'controlWithSorry' depends on axioms: [sorryAx]
```

Exactly the three permitted axioms in the spec JSON; the sorry control shows the instrument can report
`sorryAx`. `grep` for `sorry|axiom|native_decide` in the solution directory: no hits.

### Statement match

`statement_match.py` first reported `identical: 7 differ: 1` here, the one "difference" being the lemma.
That was an instrument false finding with two causes: it cut proofs only at `:= by` (this solution's
proof is a term) and only for declarations of kind `theorem` (this one is a `lemma`). Confluence fixed
both in commit ee202aec2; it now reports `identical: 8 differ: 0` (Marlow reproduced that read-only).
`statement_recheck.py` here was the independent cross-check written before the fix: it cuts at ` :=`
and finds all 8 declarations identical, and changing `(hne : a ≠ b)` to `(hne : a = b)` in a copy is
detected as different.

### Numerics (`check.py`, numpy 2.0.2, seed 20261008, output in `results.txt`)

Equality `v_k^3 = a` is tested with tolerance 1e-8. For every ordered pair i != j I enumerate every
admissible (a, b): both values if the cubes take two values; if one value c, a = c (fibre = all six) and
a = c+1 (fibre empty); none if three or more values (hab unsatisfiable). Q = |fibre sum|.

| Population | Hadamard residual (max) | entrywise-square residual | hs holds? | max Q |
|---|---|---|---|---|
| F6 | 4.4e-15 | 6.0 | no | 3.0 (rows 0,3; hypotheses not met) |
| F6^(2)(a,b) affine, 200 random (a,b) | 4.6e-15 | min 6.000 | never | n/a |
| Dita product [[F3,F3D],[F3,-F3D]], 200 random D | 2.0e-15 | min 6.000 | never | n/a |
| Dita D6(c), 200 random c | 8.9e-16 | min 2.000 | never | n/a |
| Tao's matrix (Lean `taoExponent` copied) | 8.3e-16 | 8.9e-16 | YES | 8.3e-16 |
| 500 random Hadamard-equivalents of Tao | 1.8e-15 | 3.6e-15 | YES | 1.6e-15 |
| LM search, 300 random starts, for H with both conditions | 21 converged, worst 6.4e-15 | | YES | 3.0e-15 |

- Pairs with two DISTINCT cube values among all hypothesis-satisfying matrices (Tao, 500 equivalents,
  21 search hits): 0. Consistent with the paper's classification.
- The 21 search solutions, dephased, have all entries cube roots of unity (21/21), i.e. they look like
  Tao's class. That is CONSISTENT with the paper's classification but is not a direct check of it:
  I checked dephased entries, not equivalence to Tao (Marlow's correction), on 21 converged starts out
  of 300 (random phases, Levenberg-Marquardt on both Hadamard conditions).
- Vector level (`ratio_cubeFiber_sum_zero`, the nontrivial case): 2000 constructed vectors
  `perm(u(1,w,w^2), x(1,w,w^2))` with random u, x: max |fibre sum| 5.0e-16. 500 vectors found by
  Gauss-Newton from random phases solving `sum v = sum v^2 = 0` (not built to be two-triples): cubes
  were two-valued in 500/500, max |fibre sum| 8.3e-14.

### Negative controls (each can report non-zero, and does)

- F6 rows (0,3): hH holds, hs fails (square residual 6.0), cubes are {1, -1} so hab holds with a=1,
  b=-1; Q(a=1) = 3, Q(a=-1) = -3. Shows hs is load-bearing. Contrast: F6 rows (0,1) happen to have
  `sum v^2 = 0` and give Q = 4e-16.
- All-ones matrix (unimodular, not Hadamard, residual 6): Q(i=0, j=1, a=1) = 6. Shows hH is
  load-bearing.
- Vector (1,1,1,-1,-1,-1): sum v = 0, sum v^2 = 6, fibre(a=1) sum = 3.
- Tao with 0.05-rad phase noise: Hadamard residual 0.32, and hab is unsatisfiable on 30/30 pairs, so the
  theorem is silent there (no number to compare).
- A Hadamard matrix of another size is not meaningful: the Lean statement is fixed at `Fin 6`.

### Java (`java/src/confluence/math/hadamard/HadamardCubeFiber.java`)

Same definitions with a small complex record; checks Tao and 500 random equivalents (hypotheses hold,
max Q 1.9e-15, 0 two-valued pairs), F6 and Dita D6(c) (Hadamard, hs fails, min square residual 2.000),
2000 vector-level two-triple vectors (max 7.5e-16), and the F6 (0,3) = 3 and all-ones = 6 controls. Exits
1 if any expectation fails; it printed `ALL CHECKS AS EXPECTED`.

## LIMITS

- Numerical checks on families are evidence, not proof. The Lean build plus `#print axioms` is the proof
  check, and it is my compile + axioms + textual-statement check, NOT the official Comparator run
  (`leanprover/comparator` compares compiled terms under a sandbox).
- The statement-match is textual. I confirmed equality by a corrected textual comparison, not by
  comparing elaborated terms.
- The Dita D6(c) and affine F6^(2)(a,b) matrices are written from memory of the Tadej-Zyczkowski
  catalogue forms; I verified each is Hadamard numerically (residuals above), but did not confirm they
  are the catalogue's exact parametrization. It does not matter for the conclusion (they are Hadamard and
  fail hs).
- The LM search is not exhaustive: 21 of 300 starts converged to both conditions. That none of them
  produced a two-valued pair supports, but does not prove, the paper's classification. The Lean cone for
  this challenge does not prove the classification (that is a separate, paper-level argument I did not
  check in Lean).
- Cube-value equality uses tolerance 1e-8; with all hypothesis-satisfying cases at ~1e-15 and controls
  at 3 or 6, the result is not sensitive to that choice in the range 1e-12 to 1e-3 (by inspection of the
  residuals, not by a sweep).
- I did not run the paper's `verification/run.py` (out of scope for this lemma).

## Follow-up: the lemma's real case DOES occur on real matrices (Marlow's suggestion)

Added by Confluence after Marlow's review (undervoice 15899). The cube-fibre step needs only a row-ratio
vector with |v_k| = 1, sum v = 0 and sum v^2 = 0 for that ONE pair of rows; "H∘H is Hadamard" is just the
challenge's way of getting sum v^2 = 0 for every pair at once. Drop the global hypothesis, keep the local
one, and ordinary Hadamard matrices supply the two-value case that Tao's matrix never does.

`local_moment.py` (plain Python, `python3 -I local_moment.py`): in F6 the row pairs at distance 1 or 5
are exactly the two-valued pairs with sum v^2 = 0 (12 ordered pairs). This matches the hand derivation
v_k = ζ6^(dk): sum v^2 vanishes unless d = 3, and the cubes (-1)^(dk) take two values only for odd d.
Over F6 and 200 random equivalents: 2,412 such pairs, max |fibre sum| 3.6e-15. Control: the pairs at
distance 3 (sum v = 0, two cube values, sum v^2 = 6) give fibre sums of 3 in all 1,206 cases.

This is a numerical look at a corollary of the PROVED vector lemma (`ratio_cubeFiber_sum_zero`), not a new
theorem: the vector lemma's statement already covers it. What it changes is the reading: the lemma is not
only about Tao's class; the challenge's global hypothesis is what confines its matrix instances there.
