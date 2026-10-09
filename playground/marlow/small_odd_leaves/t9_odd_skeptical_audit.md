# Independent skeptical audit: nine leaves, all odd hub counts

**Verdict: the saved certificates and lift support the claimed theorem.** I found no edge, cycle, parity, count, or residue gap. This verdict concerns the theorem and the concrete JSON currently saved here; it does not independently reproduce the CP-SAT search that found the rows.

## Sources and replay

I read `t9_all_odd_exact.md`, `t9_odd_base_cycles.json`, and `t9_odd_base_check.py`, then wrote `t9_odd_independent_replay.py` without importing or calling the author's checker or search code. The JSON's SHA-256 is `c32b8e293db66719d72e256a8c809989550b36e6baf02d3c279dac686ca47e95`. Run the independent replay from this directory:

```sh
python3 -I t9_odd_independent_replay.py t9_odd_base_cycles.json
```

The replay parses each `[H,L]` row as the alternating closed walk in the theorem. It checks valid, distinct hubs and leaves in every row, so every row is a simple 16- or 18-edge cycle. It builds a `Counter` of the actual spokes used by all cycles, rejects multiplicity greater than one, and compares against the full `m × 9` universe. In every base, the complement has exactly one spoke at each hub and the stated singleton-leaf distribution. It also checks that the saved nine-hub rows match the displayed modular formula, cycle by cycle.

| Base `m` | 18-edge cycles | 16-edge cycles | Singletons | Total pieces |
| ---: | ---: | ---: | ---: | ---: |
| 9 | 4 | 0 | 9 | 13 |
| 11 | 4 | 1 | 11 | 16 |
| 13 | 4 | 2 | 13 | 19 |
| 15 | 4 | 3 | 15 | 22 |
| 17 | 4 | 4 | 17 | 25 |
| 19 | 4 | 5 | 19 | 28 |
| 21 | 4 | 6 | 21 | 31 |
| 23 | 4 | 7 | 23 | 34 |
| 25 | 4 | 8 | 25 | 37 |

## Unbounded step and lower bound

The bases are the nine distinct odd residues modulo 18. For odd `p >= 9`, its representative `b` in `{9,11,...,25}` satisfies `p=b+18r` for an integer `r>=0`; in particular no base exceeds its target `p`. One base block and `2r` disjoint nine-hub blocks use the same leaves but disjoint hub sets, so their spoke sets cannot overlap. Each block contributes one singleton per hub. The cycle count is

```text
ceil(4b/9) + 2r·4 = ceil(4b/9 + 8r) = ceil(4p/9).
```

The independent replay checks the algebra for every residue and also materializes the entire `p=12289` partition. It finds 12,289 singleton spokes, 5,462 simple cycles, 17,751 total pieces, and all 110,601 graph edges exactly once.

For the lower bound, each hub has odd degree 9 while every cycle contributes even degree, forcing an odd positive number of singletons at each hub, hence `s>=p`. A simple cycle visits at most nine leaves, so covers at most 18 edges. Thus `c >= ceil((9p-s)/18)`. The function `s+ceil((9p-s)/18)` is nondecreasing on integral `s`, giving `s+c >= p+ceil(4p/9)`. The construction attains it.

## Provenance limit

At the time of this skeptical audit, the packet did not include the search program, version, seed, or log. A [subsequent provenance note](t9_odd_base_search_provenance.md) now includes the recovered program and a fresh replay; the original stdout and wall-time trace were not saved, and I do not claim exact byte-for-byte reproduction of the JSON. This is a provenance limit, not a proof gap: the literal JSON is a complete finite certificate, and the standard-library replay validates it without OR-Tools or any solver dependency. The author's checker likewise only imports the Python standard library. Its checks rely on `assert`, so its documented `python3 -I` invocation must be run without Python optimization; the independent replay uses explicit exceptions instead.
