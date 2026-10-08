# Issue / PR candidates for supsup/math (for Charles to walk through before anything is pushed)

Charles, 2026-10-08: "if you think there might be things worth opening an issue or PR on ... for now tho only commit
to here locally i would want to walk over it with you before we push to remote". Nothing here has been pushed or
opened. The local clone's only remote is `origin` = openai/math; the fork is NOT added as a remote.

## Short answer

**No defect found** in anything I checked. Every result I verified held: the Truffet counterexample (Python, Java and
the Lean proof in a container), the four-row permanent inequality (Lean proof, plus a numerical check of its exponent),
and the Sidorenko pattern graph's stated structure. So there is no bug report to file. What follows are
improvement-shaped candidates, ranked by how much I'd stand behind them.

## 1. PR (best candidate): a light way to check ONE Mathlib-only challenge

- **The gap:** `lean/README.md` warns that compiling the whole library may fail and recommends "compiling only small
  portions at a time", and the Comparator README's recipe (`lake update`, `lake exe cache get`, `comparator`) resolves
  the full manifest, about 10 external packages (Carleson, sphere eversion, strong PNT, ...) that most results never
  import.
- **What I measured:** 390 of the 416 challenges need nothing beyond Mathlib (`lean-cones/cones.py`). For those, a
  project that requires ONLY Mathlib at the pinned rev, holding just the solution's own dependency cone, builds in
  seconds once the Mathlib cache is present: Truffet (2 modules) and FourRowPermanent (5 modules) each compiled in
  under 30 s in a clean Debian container, with `#print axioms` matching the permitted axioms.
- **The PR would add:** a small script (generalized from `lean-docker/check.sh` + `cones.py`, without my local paths)
  that takes a challenge name, computes the cone, refuses cones needing a non-Mathlib package, and builds just that.
- **Honest limits:** it is not Comparator (it does `#print axioms` and a textual statement match, not a compiled-term
  comparison), so it would be offered as a quick pre-check, not a replacement. Upstream may simply prefer their
  existing flow; this is the kind of PR worth asking about in an issue first.

## 2. Issue (low priority, possibly not worth filing): FourRowPermanent's stated range for p₀ is loose

- The theorem states `∃ p₀, 4/3 < p₀ ∧ p₀ < 2 ∧ ...`. At the uniform law the inequality fails for every
  p < 4·ln 4 / ln 24 ≈ 1.7448 (a permutation matrix violates it; closed form 4^{4/p}/24, see `permanent/NOTES.md`), so
  any valid p₀ is at least about 1.7448. The proof uses p₀ = 2 − 10⁻⁵, so nothing is wrong.
- This is a TRUE statement with a loose advertised bound, not an error. It might interest the authors as a sharper
  statement, but it does not need fixing. I would lean toward not filing, or mentioning it only if (1) opens a
  conversation.

## 3. Not issues (recorded so we don't re-examine them)

- Truffet: all 13 conjuncts and the proof check out; the one "for all α, exists w" conjunct I only sampled is proved in
  Lean.
- Sidorenko: H's structure matches the paper's table exactly; my tiny-kernel search found no violation, which is
  consistent with the paper (it needs a large construction) and is not evidence against it. Not formalized in Lean.
- The 2026-10-08 pull (adc7f12 -> fd4aeeb) changed none of the inputs to the above.

## If we do push something

My suggestion: add the fork as a separate remote (for example `fork`), keep `origin` = openai/math untouched, and push
only a branch, never `main`. My playground is on the local branch `confluence/playground`, with `main` left as a clean
mirror of upstream.
