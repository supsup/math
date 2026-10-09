# Quasi-Riemann Hypothesis family 003: SiegelZeros build and statement reading

Requested by Fixpoint (undervoice 16467) as the second statement reading plus a kernel build. Reported at 16476.

## Statement (lean/ComparatorChallenges/SiegelZeros.lean): MATCHES (Confluence's reading)
An absolute c > 0 such that for every q >= 3 and every primitive, non-principal, real-valued Dirichlet character chi
mod q, every real zero beta in (0, 1) of L(s, chi) satisfies c <= (1 - beta) log q. That is the strong "no Siegel
zeros" statement. It goes beyond Siegel's theorem (c(eps) q^-eps, ineffective) and beyond Landau-Page (one possible
exceptional character), and it was open as of my June 2026 knowledge. The existential c is not required to be
effective, which is the classical form of the conjecture. It is not vacuous: the quadratic character mod 3 qualifies.
The second declaration is the same statement with the zero conditions bundled into a conjunction.

## Kernel build: PASS
- The cone is 306 modules and needs the external PrimeNumberTheoremAnd package, so the Mathlib-only check.sh refuses it.
  check-pnt.sh and check-pnt-challenge.sh (here) build in a separate volume, confluence-lean-math-pnt.
- Pins: the repo lakefile's lines 73-86, reproduced verbatim (PNT c39a751, leancert, LeanArchitect, PrimeCert, doc-gen4,
  checkdecls, mathlib d13f23b7). All 19 resolved packages match lean/lake-manifest.json (verify-manifest.py: 0 mismatches).
- Patch: lean/patches/PrimeNumberTheoremAnd-lean4341.patch, applied as the lakefile's post_update hook does: HEAD
  pin check, forward apply, then a reverse-check to verify. The patch CREATES PrimeNumberTheoremAnd/SiegelZeros/*,
  including HadamardSupport, the cone's only PNT import. Part of the proof lives in this patch to a third-party
  library. The kernel checked it from source.
- 9,243 jobs built, 318 modules compiled from source (306 OAI and 12 PNT SiegelZeros), 265 s.
- Both theorems depend on [propext, Classical.choice, Quot.sound]. The sorry control gives [sorryAx]. The
  challenge file elaborates. statement_match is 2/2.
- Log: siegelzeros-run.log. Built by a sub-agent; I re-read the axiom lines, the build line and the error count
  from the log myself.

## Not done
DirichletSevenEighths, QuasiRiemannHypothesis and HeckeSevenEighths. Their cones are about 2,924 modules and also
need RellichKondrachov. The method (Proposition thm:ms) was not read.
