# Prime second-leaf one-cut packet

The [asymptotic theorem](asymptotic_one_cut.md) gives an optimal one-short
edge partition of `K_(p,p+2)` for every prime `p≥3,000,000,000` (more
generally when `sqrt(p)≥66·2^ω((p−1)/2)`). It has `(p−1)/2` Hamiltonian
`2p`-cycles, one `2(p−1)`-cycle, and `p+2` singleton edges. The claim is
only for prime hub order and these stated ranges; primes `401<p<3B`
remain outside this packet's existence proof.

The proof specializes the [exact second-leaf bridge criterion](bridge.md)
to `b=ac/(c+a−1)` and counts admissible `c` with a character sieve and
the five-root Weil bound. The [exact cutoff arithmetic](cutoff_arithmetic.md),
[skeptical theorem audit](asymptotic_one_cut_skeptical_audit.md), and
[independent bridge audit](bridge_skeptical_audit.md) accompany it.
Fixpoint's formal review is pending; no showcase claim has been made.

Bounded controls replay full edges at `p=5,7,11,13` and the `20`
restricted-family primes `17≤p≤101`. The parameter checker finds a
splice triple at all `73` primes `17≤p≤401`, which gives pages there
by the proved graph lemma; it does not literally replay their edges
above `101`. This finite evidence does not close the gap above `401`.
From this directory run:

```sh
python3 -I exact_bridge_check.py
python3 -I independent_bridge_check.py
python3 -I multiplicative_splice_finite_check.py
python3 -I restricted_family_check.py
python3 -I independent_one_cut_check.py
python3 -I independent_character_audit.py
```

The first three controls document the bridge and earlier finite
two-ring cases. The last three independently check the restricted
asymptotic family's algebra and finite full-edge pages.
