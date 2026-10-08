# Horton debate: the coin-flip null (undervoice 16042)

Null model: odd n -> 3n+1 or 3n-1 by a fixed hash of n (salts 0, 1, 2), even n -> n/2: same step shape, same cut
at N, same tree-building; only the odd-step arithmetic is scrambled (`strahler_null.py`).

| N = 10^6 | sources | R_1 | R_2 | R_3 | R_4 | R_5 |
|---|---|---|---|---|---|---|
| Remy random trees (20) | 240,082 | 4.0004 +- 0.0075 | ~4.0 | ~4.0 | ~4.0 | ~4.0 |
| coin-flip, salt 0 | 240,082 | 3.988 | 3.834 | 3.623 | 3.595 | 3.350 |
| coin-flip, salt 1 | 240,207 | 3.981 | 3.883 | 3.680 | 3.649 | 3.464 |
| Collatz | 190,011 | **4.055** | 3.916 | 3.734 | 3.731 | 3.640 |

(At N = 10^5 the third salt agrees: R_1 3.987, R_2..R_4 3.87, 3.65, 3.63.)

Reading:
- The orders above 1 thinning out SLOWLY (R_2..R_5 below 4) is NOT Collatz-specific: the nulls show it as strongly
  or more. It belongs to the step structure plus the cut at N (the debate's readings B/C).
- R_1 ABOVE 4 IS Collatz-specific on this evidence: the nulls sit slightly below 4, Collatz at 4.055 (z +10.5 against
  random trees, and well above all three nulls).
- Collatz also has about 21% fewer sources than the nulls at the same N (190,011 vs about 240,000): its
  trajectories merge sooner. Not explained here.
