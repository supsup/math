# An FPRAS for common bases of two matroids: what the Lean statement says, and what I checked

Lean: challenge `lean/ComparatorChallenges/CommonBasesFPRAS.lean` (131 lines), theorem
`OAI.common_bases_fpras`; solution `lean/OAI/Combinatorics/MatroidCounting/CommonBases.lean`
(ONE module, 26 126 lines, `import Mathlib` only). Paper:
`preprints/Approximate-counting-of-common-bases-of-two-matroids-September-23-2026/` (read for context:
abstract, intro, Section 2). Python: `common_bases.py` here. Java:
`../java/src/confluence/math/commonbases/CommonBases.java`.

## The statement in plain words

There is ONE fixed program P (for a machine with k+8 bit-stacks and s+1 control states) and constants
C > 0, d such that, for every n, r, every pair of matroids M₁, M₂ on Fin n of rank r, every exact
independence oracle O for them, and every rational ε, δ in (0,1), with B = C·(1 + n + ℓ + ⌈1/ε⌉ +
⌈log₂⌈1/δ⌉⌉)^d (ℓ = bit length of n, r, ε, δ):

1. on EVERY random tape, after B machine steps the program has halted, made ≤ B oracle calls and
   ≤ B charged bit operations, output a rational z ≥ 0, and z = 0 whenever there is no common base;
2. of the 2^B tapes of length B, at least (1-δ)·2^B give an output z with
   (1-ε)Z ≤ z ≤ (1+ε)Z, where Z is the number of common bases.

## Audit verdict: (a), the open problem as usually posed (oracle model), and slightly stronger

Nothing I found makes the statement weaker than its name. Evidence, from the challenge file:

- **A real computational model, fixed before the input.** `∃ (k s : ℕ) (P : Program k s) (C d : ℕ), 0 < C ∧
  ∀ (n r : ℕ) (M₁ M₂ …) (O …) (ε δ : ℚ), …` (lines 109-111). The program, C and d are chosen
  before n, the matroids, the oracle, ε and δ, so the witness cannot depend on the input. `Program k s :=
  Fin (s + 1) → Instruction k s`, with instructions `push`, `pop`, `coin`, `query`, `halt` (lines 18-25).
  Each step does O(1) stack work, so the model is no stronger than a RAM; a polynomial bound here is a
  polynomial bound in the usual sense.
- **The matroids are reachable only through the oracle.** `machineStep` takes `O : IndependenceOracle
  n` and nothing else about M₁, M₂. `ExactOracles` (lines 9-12) pins O exactly:
  `O which A = true ↔ (if which then M₂ else M₁).Indep {i | A i = true}`. A query costs
  `length + n + 1` bit operations and needs an n-bit register (lines 76-86).
- **Running time is the machine's own step count, bounded on every tape.** `∀ bits : ℕ → Bool, let out
  := execution P O (initialConfig k s n r ε δ) bits B; out.output.isSome ∧ out.oracleCalls ≤ B ∧
  out.bitOperations ≤ B ∧ …` (lines 117-120). `execution … B` runs exactly B steps, and a halted machine
  is frozen (`if c.output.isSome then c else …`, line 55), so "halted within B steps" is forced.
- **B is polynomial in the right quantities:** `resourceBound C d n r ε δ := C * (1 + n + inputLength n r
  ε δ + ⌈ε⁻¹⌉₊ + Nat.clog 2 ⌈δ⁻¹⌉₊) ^ d` (line 106). n appears in unary (as it must: queries are n bits),
  ε⁻¹ polynomially, δ only through log. That is the FPRAS shape exactly.
- **Randomness is a genuine uniform probability.** Step t reads `bits t` (line 97); success is counted as
  `Nat.card {bits : Fin B → Bool // ∃ z, (execution … (finiteBits bits) B).output = some z ∧
  relativeAccuracy ε Z z}` against `(1 - δ) * 2^B` (lines 121-124). Since only bits 0..B-1 are ever read,
  this is the probability over independent fair coins. Success probability 1-δ for every δ ∈ (0,1) is
  stronger than the usual 3/4 (which is equivalent anyway by the median trick).
- **The accuracy is the standard one:** `relativeAccuracy ε Z z := (1-ε)*Z ≤ z ∧ z ≤ (1+ε)*Z` (line 103).
- **All pairs of matroids.** The only hypotheses are `M₁.E = Set.univ`, `M₂.E = Set.univ`,
  `M₁.eRank = r`, `M₂.eRank = r`, exact oracles, and 0 < ε, δ < 1 (lines 112-114). Equal rank is not a
  restriction: with different ranks there is no common base, and the rank is computable greedily in n
  queries. No representability, regularity, partition or bounded-rank hypothesis. Hypotheses are
  satisfiable (e.g. free matroids), so nothing is vacuous.
- **Definitions are Mathlib's.** `commonBaseCount M₁ M₂ := Nat.card {A : Finset (Fin n) // M₁.IsBase A ∧
  M₂.IsBase A}` (lines 14-16), Mathlib `Matroid`, `IsBase`, `Indep`, `eRank`. The ground set is finite, so
  `Nat.card` is the honest count.
- **Traps I looked for and did not find.** x/0 = 0: the halt output is `reg6 / reg7` (line 89), so a zero
  denominator gives output 0, which is just a legal output, not a loophole. No sSup/sInf. A malformed query
  halts with output 0 (line 85), again a legal output. The extra clause `Z = 0 → z = 0` on every tape is a
  STRENGTHENING (deciding Z > 0 is matroid intersection, which is deterministic polynomial).

So the formal theorem is the statement Liu's dissertation records as open (paper, intro: "explicitly
recorded in Liu's dissertation, Section 13.2, Problem 1"): an FPRAS for the common bases of two arbitrary
independence-oracle matroids. To my knowledge (cutoff mid-2026) no published resolution existed; known
cases were bipartite perfect matchings (two partition matroids, Jerrum-Sinclair-Vigoda), one matroid
(Anari-Liu-Oveis Gharan-Vinzant), and 2^O(r)-factor or r = O(log n) results (Anari-Oveis Gharan-Vinzant).
That is a labelled recollection, not a literature search.

What it is NOT: it says nothing about the degree d or constant C (they are existential; the proof sets
`d := p.degree`, `C := p.coefficient*2^p.degree+1` for a polynomial `p := totalResourcePoly fp fq` that the
statement does not fix), so it is a complexity-class statement, not a practical algorithm claim.

## Solution vs challenge (my own diff, before statement_match)

`diff` of the challenge against the first 135 lines of the solution: identical definitions, the solution
only wraps them in an unnamed `section` and continues the file. The final theorem
`common_bases_fpras : CommonBasesFPRAS.MainTheorem` (solution, near the end) instantiates
`⟨1, fprasBlock.size, fprasBlock.code, p.coefficient*2^p.degree+1, p.degree, …⟩`, i.e. it exhibits an
explicit program, `fprasBlock := pipeline (compile preambleCode) (compile postambleCode)`, compiled from an
internal expression language. Grep of the solution for `sorry`, `axiom`, `native_decide`, `implemented_by`,
`extern`, `unsafe`, `ofReduceBool`: no hits.

## Lean check (Docker)

Log: `../lean-docker/commonbases-run.log` (2026-10-08, 18:08-18:10Z, Lean 4.34.1, pinned Mathlib cache).

- Cone: 1 module. `✔ Built OAI.Combinatorics.MatroidCounting.CommonBases (102s)`, build successful.
- `'OAI.common_bases_fpras' depends on axioms: [propext, Classical.choice, Quot.sound]`, exactly the
  permitted set. The sorry control in the same check file shows `[sorryAx]`, so the axiom report can
  report a sorry.
- `statement_match.py CommonBasesFPRAS`: 15/15 challenge declarations identical in the solution, 0 differ,
  0 missing; 3026 solution-only helpers. Nothing to judge.

So, as far as the Lean kernel is concerned, the formal statement above is PROVED. Combined with the audit,
this is a machine-checked proof of what I believe was an open problem; that is the reason to want
independent re-checking of the Lean environment, not a reason to doubt the audit.

## Computations (`python3 -I common_bases.py`, exit 0, about 7 s)

Every instance is checked to satisfy the basis-exchange axiom first. Counts by two independent channels:

- **direct**: the Lean definition, #{A : base of M₁ and of M₂};
- **paired reduction** (paper Section 2): K = M₁ ⊕ M₂* built as an explicit basis family on 2n elements
  (dual bases = complements), count transversals S(A) that are bases of K.

| instance | direct | paired | independent value |
|---|---|---|---|
| graphic K4 vs itself | 16 | 16 | 16 (Cayley 4²) |
| two partition matroids of K3,3 | 6 | 6 | 6 (= 3! perfect matchings) |
| U(3,6) vs itself | 20 | 20 | 20 = C(6,3) |
| C4+chord vs relabelled C4+chord | 6 | 6 | - |
| U(2,5) vs U(3,5) | 0 | 0 | 0 |
| partition {0,1},{2} vs {3,4},{2} | 0 | 0 | 0 |
| 4 random bipartite graphs (no isolated vertex) | 2, 4, 2, 5 | same | Ryser permanent, same |
| 6 random binary (GF(2)) rank-3 pairs on 6 elements | 1, 11, 4, 6, 3, 6 | same | - |

I also checked, for every A on every equal-rank instance, that the defect of the transversal is
d(S(A)) = n - rank_K(S(A)) = (|A| - r₁(A)) + (r - r₂(A)) (my derivation from the dual-rank formula; it
is zero exactly on common bases). Brute force over K agrees everywhere.

**My estimator, not theirs.** `anneal_estimate` telescopes c₀(q) = Σ_transversals q^d(S) from c₀(1) = 2ⁿ
down to q ≤ ε/2^(n+2), where Z ≤ c₀(q) ≤ Z + 2ⁿq, estimating each ratio by sampling from π_q ∝ q^d with
an EXACT sampler (enumerating all 2ⁿ transversals), and returns 0 when no transversal has d = 0. With
ε = δ = 1/4 it landed in (1±ε)Z in 40/40 runs on each of the 13 equal-rank instances with n ≤ 9.

**Observation (why the paper needs defect states):** a single-pair-flip Metropolis chain on transversals
at q = 10⁻⁶, started at a common base of U(3,6) with itself, visited 1 of the 20 common bases in 20 000
steps. Common bases are separated by states of defect ≥ 1, so the naive chain freezes; the paper adds
"one empty pair, one full pair" states with learned multipliers (JSV-style) to cross them.

## Negative controls (all must fail, all did)

- Reduction with M₂ instead of M₂*: disagrees with brute force (e.g. K4: 12 vs 16; K3,3: 0 vs 6).
  Note it AGREES on U(3,6) vs itself (20 = 20), since U(3,6)* = U(3,6): a control on that instance
  alone would have been blind.
- Claimed count 17 for K4: rejected.
- Estimator stopped early at q = 1/2: fails the (1±ε) test, so the accuracy test can fail.
- Java (`CommonBases.java`, JDK 25): same two-channel counts and the first two controls; prints ALL OK.

## LIMITS / could not determine

- I did NOT run the Lean program `fprasBlock.code`. It is compiled inside Lean from an expression
  language; extracting and simulating it was out of scope, and its step budget B has an unstated degree.
  So no empirical check touches THEIR algorithm, only the reduction it starts from and the generic
  telescoping layer, with an exact sampler that sidesteps the mixing question, which is the whole content
  of the paper.
- I did not read the 26k-line proof. The Lean kernel check (above) is the evidence for correctness; the
  paper's mixing / transport argument is unreviewed by me.
- "Open problem" status is from memory and the paper's own framing, not a literature search.
- The model charges a query `length + n + 1` and halting the output's bit length; I judged these
  reasonable, not equivalent to any named textbook model.

## Confluence's recheck

- Read `MainTheorem` myself (challenge lines 100-130): `∃ (k s) (P : Program k s) (C d), 0 < C ∧ ∀ n r M₁ M₂ O ε δ, ...`
  fixes ONE program and constants before the input; the machine is a register/stack program whose only access to
  the matroids is the oracle `O`, pinned by `ExactOracles` to Mathlib's `Indep`; on EVERY tape it halts within
  B = C(1 + n + input length + ⌈1/ε⌉ + log₂⌈1/δ⌉)^d steps with at most B oracle calls; and at least (1-δ)·2^B of
  the 2^B tapes give (1 ± ε) accuracy. That is an FPRAS for common bases of arbitrary matroid pairs.
- Build log: `common_bases_fpras` on [propext, Classical.choice, Quot.sound]; sorry control on [sorryAx].
- statement_match 15/15 (after today's matcher fixes).
- Worth keeping from the report: the dual-swap control (M₂ in place of M₂*) passes on U(3,6) because U(3,6) is
  self-dual, so a control run on that instance alone would have been blind; it fails on K4 (12 vs 16) and K3,3.
- Not settled here: the degree d and constant C are existential and unknown, and the Markov chain's mixing (the
  paper's real content) is checked only by the kernel.
