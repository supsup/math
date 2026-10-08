"""Is the Collatz bifurcation ratio below the random-tree value? N = 10^6 against 20 Remy trees."""
import random
import statistics
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import strahler as s  # noqa: E402

N = 1_000_000
ch, root = s.collatz_tree(N)
cnt, ln = s.horton(ch, root)
c = s.ratios(cnt)
print(f"COLLATZ N={N:,}: nodes {len(ch):,}, sources {cnt[1]:,}, max order {max(cnt)}")
print("  N_k", [cnt[k] for k in sorted(cnt)])
print("  R_b", c)
print("  mean stream length", [round(ln[k], 2) for k in sorted(ln)])
rng = random.Random(7)
per_k = {}
for t in range(20):
    rc, rr = s.remy_tree(cnt[1], rng)
    r, _ = s.horton(rc, rr)
    for k, v in enumerate(s.ratios(r), start=1):
        per_k.setdefault(k, []).append(v)
print("  CONTROL 20 Remy trees, same sources: k, mean, sd, min, max   | Collatz | z")
for k in range(1, 6):
    xs = per_k[k]
    m, sd = statistics.mean(xs), statistics.stdev(xs)
    z = (c[k - 1] - m) / sd if sd else float("nan")
    print(f"   k={k}: {m:.3f} {sd:.3f} {min(xs):.3f} {max(xs):.3f}   | {c[k - 1]:.3f} | {z:+.1f}")
