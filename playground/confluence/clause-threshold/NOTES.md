# FixedClauseThreshold (random proper k-SAT): verification notes

Challenge: `lean/ComparatorChallenges/FixedClauseThreshold.lean`. Theorem `OAI.FixedClauseThreshold.main`.
Solution module `OAI.Probability.RandomSAT.Main`, which has a 15-module cone that needs only Mathlib (4818 lines).
Paper (context only): `preprints/A-Limiting-Satisfiability-Threshold-for-Every-Fixed-Clause-Size-September-25-2026/`.
Checked 2026-10-08.

## Statement in plain words

Fix k >= 3. Take n Boolean variables. A proper clause picks k DISTINCT variables and gives each a sign.
There are C(n,k)·2^k such clauses. A formula of length m is an ordered m-tuple of proper clauses,
drawn uniformly with replacement. `properSATProbability n k m` is the number of satisfiable tuples
divided by (C(n,k)·2^k)^m.

The theorem says there is one real α > 0 with two properties:
- for every density c with 0 <= c < α, P(n, k, ⌊cn⌋) → 1 as n → ∞;
- for every c > α, P(n, k, ⌊cn⌋) → 0.

This is the **satisfiability threshold conjecture** for random k-SAT, in its standard
fixed-density form, for every k >= 3 including k = 3. The rest of this paragraph comes from my memory
and was not checked here. Friedgut (1999) proved a sharp threshold r_k(n) that might depend on n.
Ding, Sly and Sun (2015) proved a constant threshold only for k >= some large k0. As far as I know,
k = 3 was open. So the claim is a major one, and the Lean check is the evidence for it, not this note.

## Definitions audit (traps looked for)

| Item | Finding |
|---|---|
| `ProperClause n k` | Subtype of `Fin n → Option Bool` with exactly k `some`. That is k distinct variables with signs, the standard model (no repeated variables, no tautologies). Card is C(n,k)·2^k (Lean `card_properClause`; my enumeration agrees for n=0..6). |
| `SatisfiesClause` | `∃ i, C i = some (σ i)`, meaning some literal is true. This is correct, and it is not vacuous because absent variables (`none`) never match. |
| `Satisfies`, `Satisfiable` | `∀ j`, then `∃ σ`, with the quantifiers in the correct order. |
| Division by zero | Only when n < k and m > 0 (no clauses exist). Then the value is 0/0 = 0, a finite-n artifact that does not affect the limit. For m = 0 the value is 1/1. The docstring states both. |
| `⌊c·n⌋₊` | ℕ floor. For c >= 0 this is the usual m = ⌊cn⌋. The negative-c case is excluded from the subcritical clause and cannot reach the supercritical one (c > α > 0). |
| Degenerate α | α must be positive and a real number (so finite). Both limit clauses quantify over ALL c on their side. A trivial α cannot work: the first-moment bound forces α <= ln2/(−ln(7/8)) = 5.1909 for k=3 (no satisfying assignments in expectation above it), and at c=2 or 3 P→1 empirically. Nothing is asserted at c = α. |
| sSup/sInf | None in the challenge. The solution's witness is `limsup center`, and it proves convergence (`center_tendsto`) before using the limsup, so the 0-default trap does not apply. |
| Name shadowing | I grepped the solution cone for `namespace`, `notation`, `macro`, `syntax`, `elab`, `instance`, `set_option`. The only namespaces are `OAI` and `FixedClauseThreshold`. Nothing redefines `Filter.Tendsto`, `nhds`, the floor, or `Fintype.card` inside `OAI`. |
| Decidability | `classical` is used inside `properSATProbability`. `Fintype.card` is the same for any instance, so this does not change the value. |

## Lean (Docker, compile + `#print axioms` + textual match)

Log: `../lean-docker/clausethreshold-run.log`. Lean 4.34.1, Mathlib at the repo pin. All 15 modules
built ("Build completed successfully (8939 jobs)").

```
'OAI.FixedClauseThreshold.main' depends on axioms: [propext, Classical.choice, Quot.sound]
Check.lean:6:8: warning: declaration uses `sorry`
'controlWithSorry' depends on axioms: [sorryAx]
```

The theorem's axioms are exactly the three that are permitted, with no `sorryAx`. The sorry control in the
same file is flagged, so the instrument can say NO.

`statement_match.py FixedClauseThreshold` gives 9 challenge declarations. All 9 are identical after
normalization (8 definitions and the theorem statement), 0 differ, 0 are missing, and the solution has 443
extra helpers. The solution's `Model.lean` restates the definitions in the same namespace, and `main`'s type
is built from those definitions.

## Finite replication (Python `check_threshold.py`, Java `confluence.math.clausethreshold.FixedClauseThreshold`)

Both use an exact integer DP over the set of surviving assignments (a bitmask over the 2^n
assignments). Logs: `python-run.log`, `java-run.log`. All checks pass, and the two languages agree to every
printed digit. They share one algorithm, so the closed form below is the check that does not depend on it.

- Card of ProperClause n 3 is 0,0,0,8,32,80,160 for n = 0..6, which equals C(n,3)·8.
- n=2 < k=3: P(m=0)=1 and P(m=1)=0 (Lean's 0/0).
- P = 1 exactly for m < 8, and P < 1 first at m = 8, for n = 3 and n = 4. Each clause kills a 1/8 fraction of
  the assignments, so at least 8 clauses are needed.
- **Closed form:** at n=3, m=8, the formula is unsatisfiable iff the 8 clauses are the 8 distinct sign patterns.
  That gives 8! = 40320 unsatisfiable tuples out of 8^8, so P = 0.9975967. The DP gives exactly 40320.
- Exact P values. n=3: m=12 0.906694, m=16 0.693202, m=20 0.469442. n=4: m=16 0.897625, m=20 0.708149,
  m=32 0.203314.
- Monotone nonincreasing in m (n=3, m<=20; n=4, m<=64).
- First-moment bound P <= 2^n (7/8)^m holds at every computed m.
- The solution's `center 4 3` = (1/n) Σ_{m=1}^{16n} P(4,3,m) = 6.296722. This lies inside the solution's
  eventual bounds [e^-2/16 ≈ 0.00846, 2^3+1 = 9]. Those bounds are "eventually in n", so for n=4 this is only
  a sanity check.

Monte Carlo (DPLL, seeded, Wilson 95% intervals):

| c | Python (seed 20261008, 200 per cell) n=20/40/80 | Java (seed 20261008, 400 per cell) n=40/80/120 |
|---|---|---|
| 2.0 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 (CI lower 0.990) |
| 3.0 | 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 |
| 4.27 | 0.725 / 0.625 / 0.555 | 0.683 / 0.588 / 0.503 |
| 6.0 | 0.020 / 0.005 / 0.000 | 0.000 / 0.000 / 0.000 (CI upper 0.010) |
| 8.0 | 0 / 0 / 0 | (not run) |

These numbers fit a threshold between 3 and 6, with the known finite-size drift near 4.27. They are
evidence about finite n only.

## Negative controls (each must fail, and each did)

1. **Wrong first-moment bound.** P <= 2^n (3/4)^m uses 2-SAT's kill fraction 1/4. The exact counts
   violate it 68 times, first at n=3, m=8, where P = 0.9976 > 0.8009.
2. **Wrong-side claim.** "P(c=6) >= 0.95 at the largest n" is false. The observed value is 0.000 (Python n=80, Java n=120).
3. **Lean sorry control.** `controlWithSorry` reports `sorryAx`.

## LIMITS / could not determine

- No finite computation can confirm a limit statement. The replication checks the model's definitions,
  exact small-n values, and finite-n behaviour on both sides. It does not check the theorem.
- The Lean evidence is compile + `#print axioms` + a TEXTUAL statement match. It is not the official
  Comparator (term comparison, kernel replay, sandbox), and `enable_nanoda` is false in the JSON.
- I did not read the 4818-line proof for mathematical soundness. That is the kernel's job. I did not
  assess whether the argument (hitting-time concentration plus near-additive comparison of the
  center) is new or correct as mathematics, beyond the kernel accepting it.
- The literature status (Friedgut, Ding–Sly–Sun, k=3 open) is from memory and was not re-verified here.
- The theorem gives no value for α. Nothing here confirms that α_3 ≈ 4.27.

## Confluence's recheck

- Read the challenge myself: a clause is a map Fin n -> Option Bool with exactly k signed variables,
  satisfied when some variable matches its sign; formulas are m uniform clause draws with replacement;
  `main` asserts ONE real threshold alpha > 0 for every k >= 3 with probability -> 1 below and -> 0
  above. That is the full satisfiability threshold conjecture (fixed, n-independent alpha), including
  k = 3, not a weaker variant.
- Build log: `Build completed successfully (8939 jobs)`, `main` on [propext, Classical.choice,
  Quot.sound], sorry control on [sorryAx]. statement_match 9/9, re-run by me.
- n = 3, k = 3 by my own reasoning: each of the 8 clauses kills exactly one assignment (checked), so a
  formula is unsatisfiable iff it uses all 8 sign patterns: P(m = 8) = 1 - 8!/8^8 = 0.9975967 and, by
  counting surjections, P(m = 9) = 0.9891853. First-moment bound alpha <= ln 2 / -ln(7/8) = 5.1909.
- Limits stand as written above: finite computation cannot touch a limit, and the claim's weight rests
  on the Lean kernel. Literature status (Ding-Sly-Sun for large k; k = 3 open) is from memory.
