# Hexagonal rivers: notes

`python3 -I eisenstein_rivers.py` prints the table below and writes `eisenstein_rivers.svg`.

**Notation.** z = a + bω, ω² = −1 − ω. "Divisor 2" maps: z ↦ z/2 if 2 | z, otherwise m·z + c. "Divisor 1−ω" maps: z ↦ z/(1−ω) if (1−ω) | z, otherwise m·z + c.
- **u**: the unit in {1, ω, ω²} with m·z + u ≡ 0 mod 2. **−u** uses the other unit of the same class mod 2.
- **r**: ±1 with m·z + r ≡ 0 mod (1−ω).
- **c₆**: (other prime)^k · (the unit ≡ the prime-free part of m·z mod 2(1−ω)), signed so that the divisor divides.

**Columns.**
- *units*: how many of the six units satisfy f(uz) = u·f(z) on every start in the square box.
- *caught*: the start reaches a cycle within 10^15 in norm or 3000 steps.
- *to a unit cycle*: the start's cycle contains a unit.
- *to 0*: the start falls to the fixed point 0. Several maps degenerate this way.

The square box is the brief's |a|, |b| ≤ 20. The hexagon is max(|a|, |b|, |a−b|) ≤ 20. It is the unit-invariant box, and the square box is not.

| map (divisor: odd step) | units u with f(uz)=u f(z) | box | cycles | caught | to a unit cycle | to 0 | escaped | cycle lengths |
|---|---|---|---|---|---|---|---|---|
| 2: (2−ω)z + c₆   [chosen] | 6 | square 1680 | 40 | 1154 | 450 | 0 | 526 | 2,42 |
| 2: (2−ω)z + c₆   [chosen] | 6 | hexagon 1260 | 39 | 912 | 378 | 0 | 348 | 2,42 |
| 2: (2−ω)z − c₆ | 6 | square 1680 | 0 | 0 | 0 | 0 | 1680 |  |
| 2: (2−ω)z − c₆ | 6 | hexagon 1260 | 0 | 0 | 0 | 0 | 1260 |  |
| 2: (2−ω)z + u | 3 | square 1680 | 4 | 1378 | 1073 | 0 | 302 | 2,180 |
| 2: (2−ω)z + u | 3 | hexagon 1260 | 4 | 1086 | 858 | 0 | 174 | 2,180 |
| 2: (2−ω)z − u | 3 | square 1680 | 4 | 1378 | 1073 | 0 | 302 | 2,180 |
| 2: (2−ω)z − u | 3 | hexagon 1260 | 4 | 1086 | 858 | 0 | 174 | 2,180 |
| 2: 3z + u | 3 | square 1680 | 46 | 508 | 90 | 0 | 1172 | 2,3,5,13,18,31 |
| 2: 3z + u | 3 | hexagon 1260 | 42 | 444 | 90 | 0 | 816 | 2,3,5,13,18,31 |
| 2: 3z + c₆ | 6 | square 1680 | 0 | 0 | 0 | 0 | 1680 |  |
| 2: 3z + c₆ | 6 | hexagon 1260 | 0 | 0 | 0 | 0 | 1260 |  |
| 2: (1−ω)z + u | 3 | square 1680 | 3 | 1680 | 1680 | 0 | 0 | 2 |
| 2: (1−ω)z + u | 3 | hexagon 1260 | 3 | 1260 | 1260 | 0 | 0 | 2 |
| 2: (1−ω)z + c₆ | 6 | square 1680 | 0 | 0 | 0 | 0 | 1680 |  |
| 2: (1−ω)z + c₆ | 6 | hexagon 1260 | 0 | 0 | 0 | 0 | 1260 |  |
| 2: (1+2ω)z + u | 3 | square 1680 | 1 | 1680 | 1680 | 0 | 0 | 6 |
| 2: (1+2ω)z + u | 3 | hexagon 1260 | 1 | 1260 | 1260 | 0 | 0 | 6 |
| 2: z + c₆ | 6 | square 1680 | 36 | 1680 | 1120 | 0 | 0 | 2 |
| 2: z + c₆ | 6 | hexagon 1260 | 36 | 1260 | 840 | 0 | 0 | 2 |
| 2: ωz + c₆ | 6 | square 1680 | 12 | 1680 | 1120 | 0 | 0 | 6 |
| 2: ωz + c₆ | 6 | hexagon 1260 | 12 | 1260 | 840 | 0 | 0 | 6 |
| 2: −ωz + c₆ | 6 | square 1680 | 6 | 1680 | 1120 | 0 | 0 | 12 |
| 2: −ωz + c₆ | 6 | hexagon 1260 | 6 | 1260 | 840 | 0 | 0 | 12 |
| 1−ω: 2z + r | 2 | square 1680 | 6 | 1680 | 1212 | 0 | 0 | 2,43,64 |
| 1−ω: 2z + r | 2 | hexagon 1260 | 6 | 1260 | 940 | 0 | 0 | 2,43,64 |
| 1−ω: 2z + ωr | 2 | square 1680 | 6 | 1680 | 1218 | 0 | 0 | 2,43,64 |
| 1−ω: 2z + ωr | 2 | hexagon 1260 | 6 | 1260 | 940 | 0 | 0 | 2,43,64 |
| 1−ω: −2z + r | 2 | square 1680 | 4 | 1680 | 1212 | 0 | 0 | 4,64,86 |
| 1−ω: −2z + r | 2 | hexagon 1260 | 4 | 1260 | 940 | 0 | 0 | 4,64,86 |
| 1−ω: 2ωz + r | 2 | square 1680 | 7 | 1680 | 876 | 0 | 0 | 4,6,21,36 |
| 1−ω: 2ωz + r | 2 | hexagon 1260 | 7 | 1260 | 676 | 0 | 0 | 4,6,21,36 |
| 1−ω: (2−ω)z + r | 2 | square 1680 | 3 | 322 | 116 | 0 | 1358 | 2,28 |
| 1−ω: (2−ω)z + r | 2 | hexagon 1260 | 3 | 286 | 96 | 0 | 974 | 2,28 |
| 1−ω: 2z + c₆ | 6 | square 1680 | 1 | 1680 | 0 | 1680 | 0 | 1 |
| 1−ω: 2z + c₆ | 6 | hexagon 1260 | 1 | 1260 | 0 | 1260 | 0 | 1 |

## Findings
- **Symmetry: three-fold, two-fold, or six-fold.**
  - Divisor 2 with an offset that depends only on z mod 2 is three-fold at most. Rotation by ω, ω² survives. −1 cannot, because −z ≡ z mod 2 while equivariance needs c(−z) = −c(z).
  - Divisor 1−ω with c = ±r is two-fold. ω ≡ 1 mod (1−ω), so the rotations cannot survive.
  - Six-fold needs the offset to see both primes. The six units are exactly the invertible residues mod 2(1−ω), which gives c₆. Every c₆ row checks all 6 units.
- **c₆ needs m prime to 1−ω as well as to 2.** If m has a factor of 1−ω (m = 1−ω, 3) or of 2 (m = 2), the power of 1−ω or of 2 only grows. Those rows escape completely or collapse to 0.
  - With m a unit, everything is caught in short cycles (2, 6, 12).
  - The smallest non-unit choice is m = 2−ω, of norm 7. It gives the chosen map.
- **The chosen map, 2: (2−ω)z + c₆.**
  - It is six-fold. It also commutes with multiplication by 1−ω and never changes the power of 1−ω in z. So the 40 (square) or 39 (hexagon) cycles are a single six-orbit of 2-cycles 1 ↔ 2 and one 42-cycle through 1+4ω, each scaled by powers of 1−ω.
  - The 42-cycle is itself invariant under all six units: seven steps multiply it by −ω.
  - The drawing uses the 840 hexagon starts prime to 1−ω: 564 caught, 276 escaped, 63 reach 1 itself.
- **Drift.** An odd step multiplies |z| by √7 ≈ 2.646. The halvings divide by 2^(4/3) ≈ 2.520 on average. The drift is slightly outward: expect escapees to dominate in bigger boxes. This is a heuristic, not measured beyond |a|, |b| ≤ 20.
- **Equal rows.** Associate and conjugate multipliers give identical counts: (2−ω)z ± u, and 3+ω (checked in exploration, not tabled).
- **Runner-up: 1−ω: 2z + r.** It catches all 1680 starts in 6 cycles of lengths 2, 43 and 64, but it is only two-fold, so it does not make a hexagonal picture.

## Limits
- **Escapee caps.** The caps are 10^15 in norm and 3000 steps. An escapee is not proven divergent. The caught fraction is a small-box measurement.
- **Picture symmetry.** It is exact by construction: mouths sit at arg(u), the start set is unit-invariant, and the script asserts the equivariance. The turning-walk rivers overlap freely.
