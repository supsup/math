# Bounded two-ring second-leaf splice controls, primes 17 through 101

**Finite, method-specific evidence only.** The sufficient multiplicative
two-ring condition in [the bridge note](bridge.md) has a witness for each
of the **20 primes** in the closed interval `17≤p≤101`. This is not an
all-prime `K_(p,p+2)` theorem, an asymptotic existence proof, or an
obstruction at untested primes. The endpoints `p=5,13` already require
more flexible bridges than this particular one-cut splice.

The deterministic [checker](multiplicative_splice_finite_check.py)
selects the first admissible `(a,b,c)` in increasing integer order,
then chooses the first matching `τ∈{1,a}` and `M∈{c,L}`. For each
candidate it verifies the base character condition, the distinct
second-leaf spokes, the generator order of `L/c`, and `bR=Mτ`.
It constructs the two internal cycles, removes the two splice edges,
adds the two cross edges, and checks the resulting `2(p−1)`-cycle.
It then rebuilds all `(p−1)/2` transformed full cycles, checks each
cycle's connectivity, and counts **every** edge of `K_(p,p+2)` exactly
once with `p+2` singleton spokes. The
[JSON certificate](multiplicative_splice_finite_cert.json) holds the
exact parameters for all 20 primes and **literal short-cycle walks**
for `p=17,19,23` (32, 36, and 44 vertices respectively). Ordinary
checker execution regenerates and compares all parameters, reads the
literal walks, and independently replays the full graph at every prime.

| `p` | `a` | `b` | `c` | `R` | `L` | `τ` | `M` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 17 | 2 | 6 | 7 | 8 | 12 | 2 | 7 |
| 19 | 4 | 2 | 13 | 16 | 14 | 1 | 13 |
| 23 | 2 | 11 | 19 | 6 | 20 | 1 | 20 |
| 29 | 4 | 8 | 10 | 13 | 17 | 1 | 17 |
| 31 | 7 | 3 | 22 | 28 | 24 | 1 | 22 |
| 37 | 3 | 13 | 22 | 34 | 24 | 3 | 24 |
| 41 | 2 | 7 | 34 | 40 | 35 | 1 | 34 |
| 43 | 9 | 2 | 27 | 35 | 28 | 1 | 27 |
| 47 | 2 | 11 | 13 | 14 | 23 | 1 | 13 |
| 53 | 4 | 2 | 48 | 49 | 51 | 4 | 51 |
| 59 | 3 | 2 | 55 | 57 | 56 | 1 | 55 |
| 61 | 4 | 7 | 51 | 57 | 54 | 4 | 54 |
| 67 | 4 | 7 | 27 | 33 | 30 | 1 | 30 |
| 71 | 2 | 22 | 22 | 43 | 23 | 1 | 23 |
| 73 | 6 | 5 | 13 | 18 | 17 | 1 | 17 |
| 79 | 2 | 7 | 59 | 65 | 60 | 1 | 60 |
| 83 | 3 | 2 | 79 | 81 | 80 | 1 | 79 |
| 89 | 5 | 27 | 62 | 88 | 66 | 1 | 62 |
| 97 | 2 | 21 | 63 | 64 | 83 | 1 | 83 |
| 101 | 4 | 10 | 86 | 95 | 89 | 4 | 86 |

Run `python3 -I multiplicative_splice_finite_check.py` from this
directory. It prints one `SPLICE_PASS` line per prime and finishes
`SPLICE_RANGE_PASS primes=20 first=17 last=101`.
