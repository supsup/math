# Skeptical audit: multiplicative shift pairs at every prime

**Independent audit verdict: sound for every prime `p≥5`.** I checked the argument in [`prime_shift_pair_all_primes.md`](prime_shift_pair_all_primes.md) against the stated shift-pair conditions, derived the character count independently, and built a separate exact-edge checker. The construction proves the one-short optimum at `q=p+1+tp` for every `t≥0`; it does not settle composite hub orders or the other square-window leaf counts.

For a generator `a` of the nonzero quadratic residues `S`, `a≠1` because `|S|=(p−1)/2≥2`; hence `χ(1−a)∈{±1}`. For either target sign `t`, let `N_t` count nonresidues `b` with `χ(1−b)=t`. The indicator sum over `b≠0,1` is

```text
4N_t = ∑(1−χ(b))(1+tχ(1−b))
     = p−1−t(1−χ(−1)).
```

The two linear character sums are each `−1`; the product sum is `−χ(−1)`, as follows from counting `(u,v)` with `v²=u²−1`. For `p≡1 mod 4`, both signs occur `(p−1)/4` times. For `p≡3 mod 4`, `N_+=(p−3)/4≥1` and `N_-=(p+1)/4≥2`. The endpoint `p=5` works: `S={1,4}`, `a=4`, `b=2`, giving rows `(d,e,s,h,g)=(2,4,1,4,2)` and `(3,1,4,1,3)`. The excluded prime `p=3` has `|S|=1`, so `a=1` and zero short offset; the theorem correctly starts at five.

Given `b` with `χ(1−b)=−χ(1−a)`, the offsets `(1−a)S` and `(1−b)S` are opposite nonzero character cosets, so they partition all `p−1` nonzero shifts exactly once. The map `s↦as` is one cycle on `S`; `s↦bs` bijects `S` onto the nonresidues; the remaining hub is zero. The paired shifts differ by `(b−a)s≠0`, which is an additive generator because the field has prime order. Moreover `s−as=(1−a)s` and `s−bs=(1−b)s`, so each row removes precisely the two required spokes from one Hamilton square cycle. These facts meet every hypothesis of the shift-pair criterion, including distinct selected leaves, disjoint new-leaf hub roles, and connectedness of the short cycle.

My independent [standard-library checker](prime_shift_pair_all_primes_independent_check.py) enumerates **every generator** and verifies the exact character-count formula and nonempty candidate set for all 44 primes `5≤p≤199`. It constructs a witness from the first generator, checks that each original and transformed two-shift row is one simple `2p`-cycle, the transferred row is one simple `p−1`-cycle, and all `p(p+1)` spokes occur once in exactly `(p−1)/2` full cycles, one short cycle, and `p+1` singleton parts. It independently appends one and two `p`-leaf offset blocks and checks complete edge coverage and the part-count formula. The producer's separate [`prime_shift_pair_all_primes_check.py`](prime_shift_pair_all_primes_check.py) also passes all 44 base graphs through `p=199`. The finite checks corroborate the unbounded algebraic argument; they do not replace it.

**Overlap and boundary.** Locally, the result subsumes the previous first-even-base `q=p+1+tp` results for primes `p≡3 mod 4`, `p≡5 mod 8`, and size-qualified later two-adic classes; those used different Kotzig/direct-swap constructions and remain valid. It says nothing about `q=p+2+tp`, other square-window bases, or composite odd `m`. The prior finite shift-pair witnesses through `m=39` are compatible with this theorem at prime orders. I have not assessed historical publication priority; this is a mathematical and local-repository overlap audit.
