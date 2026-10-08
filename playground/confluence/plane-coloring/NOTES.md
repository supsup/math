# PlaneColoring: a proper 7-colouring of the plane, replicated twice and checked in Lean

Lean: `lean/ComparatorChallenges/PlaneColoring.lean` (statement, proof `sorry`), spec
`PlaneColoring.json` (permitted axioms `propext`, `Quot.sound`, `Classical.choice`). The solution root is
`OAI.Geometry.PlaneColoring.Main`. Its dependency cone is 9 modules: Main, Seven, Assembly, Lattice,
Metric, Covering, MeasurableAssembly, MeasurableProper and Basic. The folder holds 46 files, and the
other 37 are not imported by this theorem.

## The statement, in plain words

`ProperColoring k` says there is a function `c : Plane → Fin k` with `dist x y = 1 → c x ≠ c y`, where
`Plane = EuclideanSpace ℝ (Fin 2)` (the Euclidean metric). Only distance EXACTLY 1 is constrained.
`properColoring_seven : ProperColoring 7` says 7 colours are enough. This is the classical upper bound
for the Hadwiger–Nelson problem.

## What the proof actually builds (read from the Lean, not from memory)

The proof does not build hexagons directly. It uses disks around lattice points.

- Centres: `triangularLattice a b = (4/5)·(a + b/2, (√3/2)·b)`. This is a triangular lattice whose
  nearest neighbours are 4/5 apart (Metric.lean).
- Colours: `colorFin a b = (a + 3b) mod 7` (Lattice.lean).
- Cells: every point lies within r = 7/15 of some centre. Covering.lean proves "within √(1/3) of the
  unit lattice", and Seven.lean rescales that by 4/5, giving (4/5)/√3 ≈ 0.4619 ≤ 7/15 ≈ 0.4667.
  `Assembly.exists_unit_distance_coloring_of_center_cover` then picks one such centre per point with
  `choose`, and the point takes that centre's colour.
- Why it is proper: if x and y pick the same centre, `dist x y ≤ 2r = 14/15 < 1`. If they pick
  different centres of the same colour, then 7 divides (a−c) + 3(b−d), so (a−c)² + (a−c)(b−d) + (b−d)²
  ≥ 7. That puts the centres at least (4/5)√7 ≈ 2.117 > 2 apart, and the triangle inequality gives
  `dist x y > 2 − 2r > 1`.

**Boundary convention:** Lean has none. Points within 7/15 of two or three centres belong to all of
them, and that happens for about 23% of random points. Lean's `choose` (Classical.choice) picks one
opaquely, and the proof holds for EVERY choice. So "which tile owns a boundary" is not defined by the
Lean. The only concrete rule in the source is the witness inside the proof of
`triangular_lattice_cover`: `n = ⌊2y/√3⌋`, `m = ⌊x − n/2⌋`, and then the comparisons `u ≤ 1/2`,
`√3·v ≤ 1−u` and `√3·v ≤ u`. I checked it numerically: on all 200,000 sampled points this witness was a NEAREST centre (a sample, not a proof). It is
the hexagonal Voronoi tiling, with regular hexagons of circumradius (= side) 4/(5√3) ≈ 0.4619 and
diameter ≈ 0.9238, and ties go to the lower or left centre through the floors and `≤`. But
`choose` is not required to return that witness, so the witness is one valid selector, not "the Lean
colouring". `exists_measurable_proper_seven` in the same file is a different theorem. It does fix a
rule: the first centre in a countable enumeration.

## What I checked, and how

`replicate.py` (Python with numpy, run as `python3 replicate.py`; it needs the user site, so not `-I`)
and `../java/src/confluence/math/planecoloring/PlaneColoring.java` (Java 25). Both are written from the
Lean definitions and are independent of each other. Both use seed 20261008.

The main instrument is the **admissible colour set**: for each point, the set of colours of ALL centres
within 7/15. A unit pair fails if its two endpoints share any admissible colour. Zero failures means
every possible selector is proper on that sample, Lean's included. I also ran two concrete selectors:
nearest centre (hexagons) and the floor witness.

| check | Python | Java |
|---|---|---|
| exact side conditions: 16/75 ≤ (7/15)², 14/15 < 1, (16/25)·7 > (29/15)², min normSq of same-colour offsets (|a|,|b| ≤ 30) = 7 | all OK (Fractions) | all OK (long) |
| (a) 1,000,000 random unit pairs in [−50,50]²: admissible-set conflicts | 0 | 0 |
| (a) same pairs, nearest-centre conflicts | 0 | 0 |
| (a) endpoints with more than 1 admissible centre or colour | 467,693 / 2,000,000 | 468,926 / 2,000,000 |
| (b) 400,000 boundary pairs (endpoint within 1e-9 of a hexagon vertex, edge or r-circle; directions aimed at other boundary points, random, or along the 12 lattice angles): admissible / nearest conflicts | 0 / 0 | 0 / 0 |
| (b) endpoints with more than 1 admissible centre | 415,942 / 800,000 | 415,624 / 800,000 |
| floor-witness selector: max distance to its centre | 0.461880215351702 (200k points incl. 100k boundary) | 0.461880215351671 |
| floor witness is a nearest centre (to 1e-9) | 200,000 / 200,000 | not checked |
| floor-witness colouring conflicts | 0 / 200,000 random pairs | 0 / 200,000 (half boundary) |

Scale window (Python, polygon distance): with nearest-centre hexagons and (a+3b) mod 7, the tiling is
proper exactly for spacing d in (√(3/7), √3/2) = (0.6547, 0.8660). The lower end is where the gap
between same-colour hexagons reaches 1, and the upper end is where the hexagon diameter reaches 1.
Lean's disk argument with r = 7/15 needs the narrower range d in (0.7307, 0.8083), and d = 0.8 lies in
it. The cover inequality has only a small margin (0.4619 against 0.4667). The separation inequality
has a large one (2.117 against 1.933).

## Negative controls (every one must fire, with an explicit pair)

| control | Python violations / 200k | Java violations / 200k | example violating pair (Python) |
|---|---|---|---|
| spacing 1.0 (hexagon diameter 1.155 > 1) | 2,598 | 2,515 | p=(−8.575113987545, −12.331542428786), q=(−9.439289462627, −11.828351860248), both colour 5 |
| spacing 0.6 (same-colour hexagons 0.917 apart) | 1,139 | 1,134 | p=(−20.124526551091, −48.994658921495), q=(−19.160427650023, −49.260202343479), both colour 4 |
| rule (a+b) mod 7 | 47,085 | 47,190 | p=(36.022168036695, −18.059318471626), q=(35.642267518077, −17.134291122865), both colour 4 |
| 6 colours, (a+3b) mod 6 | 6,144 | 6,072 | p=(48.417418872025, −16.896802756859), q=(49.041225050428, −16.115223681022), both colour 4 |
| admissible instrument, r = 0.55 (2r > 1) | 11,088 | 11,027 | p=(5.265759110319, −13.686116234981), q=(5.157987754626, −12.691940528734) |
| admissible instrument, r = 7/15 with rule a+b | 62,693 | 62,773 | p=(−19.824059064207, −2.777950700471), q=(−20.115936121776, −1.821494855560) |

The Python violating pairs are not floating-point artefacts. Each endpoint is at least 0.043 closer to
its own centre than to the next one (the "tie margins" the script prints), and |p − q| − 1 is about
1e-15.

## Lean, in Docker (2026-10-08, log `../lean-docker/planecoloring-run.log`)

- The 9-module cone builds against the pinned Mathlib (Lean 4.34.1): "Build completed successfully".
- `'OAI.Problem160.properColoring_seven' depends on axioms: [propext, Classical.choice, Quot.sound]`.
  These are exactly the permitted set, with no `sorryAx`.
- Sorry control in the same file: `'controlWithSorry' depends on axioms: [sorryAx]`. So the instrument
  can report `sorryAx`.
- `statement_match.py PlaneColoring`: `Plane` and `ProperColoring` are textually identical to the
  challenge. `properColoring_seven` is reported as DIFFERS, and that is a FALSE ALARM of the
  instrument. Its `statement_only` cuts at `:= by`, and the solution's proof is a term
  (`:= properColoring_seven_of_normalized_cover triangular_lattice_cover`), so the whole body is
  compared, including the next docstring. The statement part, `theorem properColoring_seven :
  ProperColoring 7`, is identical on both sides, and both sit in `OAI.Problem160`. This is a textual
  check, not the Comparator's term-level check.

## Limits

- The random and boundary tests are evidence, not proof. The Lean proof is the proof. My tests sample
  10^6 + 4·10^5 pairs out of a continuum, and they run in `double`.
- The admissible-set instrument checks every selector only on the sampled points. Neither language
  can run Lean's actual `choose`, which is noncomputable.
- The exact check "min normSq ≥ 7" covers only offsets with |a|, |b| ≤ 30. The general fact is the
  Lean lemma `seven_dvd_normSq` (identity a² + ab + b² = (a+3b)(a−2b) + 7b²), which I read but did not
  re-prove.
- The Lean run builds with `lake build` and prints only the last 12 lines. A warning in an earlier line
  would not be visible, but the axioms line rules out `sorry` in this theorem's dependencies.
- I did not run the Comparator itself, and `enable_nanoda` is false in the spec.

## What surprised me

- The proof does not prove that hexagons work. It proves that closed disks of radius 7/15, which
  overlap, work under any assignment of the overlaps. About 23% of the plane is in an overlap. That
  argument is more robust than the textbook hexagon picture, and boundary conventions become
  irrelevant by construction.
- The concrete witness in `triangular_lattice_cover` turns out to be exactly the Voronoi (hexagon)
  assignment, although nothing in the Lean says "nearest".
- The repository's own `statement_match.py` mislabels any theorem whose solution proof is a term
  rather than a `by` block.
