# Lean in Docker (no Lean on the host)

Charles OK'd Docker for isolated replication (2026-10-08). `run-truffet.sh` starts one throwaway
container (`debian:bookworm-slim`, labelled `owner=confluence`, removed on exit) with:

- `coderefs/math/lean` mounted READ-ONLY at `/src` (nothing is written into the repo)
- a named volume `confluence-lean-math` at `/work` holding elan, the Lean toolchain, the Mathlib cache
  and build output, kept so later checks reuse the ~9k-file Mathlib cache

`truffet-check.sh` (runs inside) installs elan at the repo's pinned toolchain (`leanprover/lean4:v4.34.1`),
makes a minimal Lake project requiring ONLY Mathlib at the repo's pinned rev `d13f23b7`, copies in the 2
solution modules, runs `lake exe cache get`, builds, and prints the theorem's axioms next to a `sorry`
control.

## Result: Truffet (2026-10-08 12:23Z, `truffet-run.log`)

```
'OAI.TruffetV4Counterexample.finite_execution_not_optimal' depends on axioms: [propext, Classical.choice, Quot.sound]
'controlWithSorry' depends on axioms: [sorryAx]
```

- Both modules compile against the pinned Mathlib (TruffetModel 6.7 s, TruffetCounterexample 4.0 s).
- The theorem uses exactly the three axioms the challenge permits, and no `sorryAx`.
- The control in the same file shows `sorryAx`, so the instrument CAN report an unproved theorem.
- `statement_match.py`: all 31 challenge declarations (defs and the theorem statement) are textually identical
  in the solution after whitespace normalization; 12 extra helper declarations in the solution. Its negative
  control (one coefficient of `better` changed in a copy) is caught as exactly 1 differing declaration.

What this is NOT: the official Comparator check (`leanprover/comparator` compares compiled terms and runs the
kernel export under a sandbox). Mine is compile + `#print axioms` + a textual statement comparison. Together
they say: the solution's theorem, which states the same thing as the challenge, is proved without `sorry`
or extra axioms.

## Generic check: `./check.sh <ChallengeName>`

Reads the challenge JSON, computes the solution's cone with `../lean-cones/cones.py`, REFUSES cones needing a
non-Mathlib package, copies just those modules into a project under the volume, builds, and prints `#print axioms`
for the challenge's theorem names next to a sorry control. Pair it with `python3 -I statement_match.py <Name>`.

| Challenge | Modules | Axioms | Statement match | Log |
|---|---|---|---|---|
| TruffetCounterexample | 2 | propext, Classical.choice, Quot.sound | 31/31 | truffet-run.log |
| FourRowPermanent | 5 | propext, Classical.choice, Quot.sound | 10/10 | fourrow-run.log |

## Mistakes on the way (kept, they cost three runs)

1. `roots := #[...TruffetCounterexample]` made Lake skip `TruffetModel` (not part of any lib), so the
   import failed (`truffet-run-1-failed.log`).
2. `globs := #[.andSubmodules OAI]` also asks for a module named `OAI` itself; no `OAI.lean` exists in my
   copy (`truffet-run-2-failed.log`, though both real modules built). `.submodules` is right.
3. A side control run in a fresh container without `git` made `lake env` try to re-clone Mathlib, which
   wiped the populated package dir; the next run then found no Mathlib `.olean` files. Fixed by putting the
   control INSIDE the main script, which always reinstalls git and runs `lake exe cache get` first.
