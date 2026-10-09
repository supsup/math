# Provenance of the nine-leaf finite blocks

The literal proof certificate is [t9_odd_base_cycles.json](t9_odd_base_cycles.json), checked without a solver by [t9_odd_base_check.py](t9_odd_base_check.py) and a separate skeptical replay. The original exploratory [search script](t9_odd_base_search.py) survived in `/tmp/t9_search.py` and was copied here byte for byte on 2026-10-09. Its source SHA-256 is recorded in the [fresh replay log](t9_odd_base_search_replay_20261009.log).

The original search ran under Python 3.9.6 with OR-Tools 9.6.2534. It used CP-SAT with eight workers, base random seed `1`, seed `1+r` at subtour-cut round `r`, and a 60-second wall-time limit per base. The script fixes one singleton per hub and all cycle degree and length constraints, solves, finds disconnected cycle components, adds cuts excluding them, and repeats until every selected component is a single cycle. It was called for `m=11,13,...,25`; the `m=9` rows in the JSON come from the direct modular formula in [the proof](t9_all_odd_exact.md).

To run the preserved script as written, install the same package into its historical temporary import path and then run a base:

```sh
python3 -m pip install --target /tmp/t9_ortools ortools==9.6.2534
python3 t9_odd_base_search.py 11 60
```

The JSON was produced by a second local batch run of the same `solve(m, limit=60, seed=1)` function for all eight nontrivial bases. The batch parsed the printed cycle rows into JSON. Its original stdout and wall-time trace were not saved; the JSON itself preserves every selected cycle. The linked replay log is a **new** run, made after preserving the script, with the same version, seeds, workers, and time limit. Its eight sets of rows differ from the original JSON because parallel CP-SAT search can choose different feasible solutions. Each replay block was parsed and passed the same independent edge/cycle checker. Exact byte-for-byte regeneration of the original JSON is therefore not claimed; both the original and replay rows are directly checkable finite certificates.
