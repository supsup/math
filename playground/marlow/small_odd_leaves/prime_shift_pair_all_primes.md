# Prime-order shift pairs give a one-short cycle for every prime

**Local research finding, independently audited but awaiting Fixpoint's
exact-tip review.** This supplies a uniform shift-pair construction for
every prime hub order, including the previously elusive `p≡1 mod 4`
class. It does not solve composite odd hub orders or every leaf-count base.

## Theorem

Let `p≥5` be prime and `n=(p−1)/2`. The edges of `K_(p,p+1)` can be
partitioned into `n` Hamilton `2p`-cycles, one `2n`-cycle, and `p+1`
singletons. In particular this is the optimal one-short cycle profile at
this base. The same profile with `n(1+t)` Hamilton cycles and
`(1+t)p+1` singletons holds for `K_(p,(1+t)p+1)` for every `t≥0`, by
appending `t` standard square blocks on disjoint sets of `p` leaves.
Each block has diagonal singleton spokes and the `n` Hamilton colors
formed by pairing cyclic shifts `(1,2),(3,4),…,(p−2,p−1)`; each pair
differs by a unit. The resulting cycle count is `n(1+t)+1`. This is
optimal by the [reviewed all-parity lower bound](all_bipartite_parity_bound.md):
the compulsory singleton count is `q=(1+t)p+1`, and
`ceil(q(p−1)/(2p))=n(1+t)+1` cycles are necessary.

## Multiplicative rows

Write `Q` for the nonzero quadratic residues in `F_p`, and `χ` for its
quadratic character. Choose any generator `a` of the cyclic group `Q`.
Choose a nonresidue `b` for which

```text
                         χ(1−b) = −χ(1−a).                 (1)
```

The count below proves that such `b` always exists. Index the `n` rows by
`s∈Q` and put

```text
short hub h_s = a s,       outside hub g_s = b s,
short offset d_s = (1−a)s, outside offset e_s = (1−b)s.   (2)
```

Then `s−h_s=d_s` and `s−g_s=e_s`. Because `a` generates `Q`, the map
`s→h_s` is one `n`-cycle on the selected leaves `Q`. The outside hubs
`bQ` are exactly the distinct nonresidues, so the only unused hub is `0`.
The offset sets `(1−a)Q` and `(1−b)Q` are opposite character cosets by
(1), and therefore partition every nonzero field element exactly once.
Finally `d_s−e_s=(b−a)s` is nonzero: `a` is a residue and `b` is a
nonresidue. In the *additive cyclic group of prime order*, each nonzero
difference generates the entire group. Thus every two-shift square color
is one Hamilton cycle. All conditions of the shift-pair criterion hold.

For completeness, the trade removes from each square color its two edges
at leaf `s` and replaces `s` by the one new leaf. The removed `(h_s,s)`
edges, together with `(s,s)`, make one `2n`-cycle because `s→h_s` is a
cycle. The other removed `(g_s,s)` edges become singletons. The other
old diagonal edges are singleton, as is `(0,new leaf)`. Since the two
offset cosets cover all nonzero offsets and `Q`, `bQ`, `{0}` partition the
hubs, every edge is used exactly once.

## Existence of the outside multiplier

For `t∈{−1,+1}`, define

```text
N_t = #{b∈F_p\{0,1}: χ(b)=−1, χ(1−b)=t}.
```

Expanding the two indicator factors gives

```text
4 N_t = ∑_{b≠0,1}(1−χ(b))(1+tχ(1−b))
      = p−1−t(1−χ(−1)).                                  (3)
```

Here both single-character sums over `b≠0,1` equal `−1`. The product
sum is the elementary Jacobi identity
`∑_b χ(b(1−b))=−χ(−1)`. One direct proof is to count pairs satisfying
`v²=u²−1`: the substitution `(u−v)(u+v)=1` gives exactly `p−1`
pairs, hence `∑_u χ(u²−1)=−1`. Replacing `u` by `2b−1` yields the
Jacobi identity.

If `p≡1 mod 4`, equation (3) gives `N_+=N_-=(p−1)/4≥1`. If
`p≡3 mod 4`, it gives `N_+=(p−3)/4≥1` and `N_-=(p+1)/4≥2` since
`p≥7`. Thus both desired signs occur among nonresidues and (1) can be
met for **every** generator `a`, completing the universal existence
proof. No distribution theorem about primitive roots is needed.

## Small witnesses and exact replay

The first parameter choices found by the self-contained
[`prime_shift_pair_all_primes_check.py`](prime_shift_pair_all_primes_check.py) are:

| `p` | generator `a` of `Q` | nonresidue `b` | short hubs |
|---:|---:|---:|---|
| 5 | 4 | 2 | `1,4` |
| 7 | 2 | 6 | `1,2,4` |
| 11 | 3 | 2 | `1,3,9,5,4` |
| 13 | 4 | 6 | `1,4,3,12,9,10` |

The checker verifies offset partition, single-cycle successor, every
original and transformed cycle's connectedness, every graph edge exactly
once, and two added square blocks on small primes. A separately written
[skeptical audit](prime_shift_pair_all_primes_skeptical_audit.md) and
[independent exact-edge checker](prime_shift_pair_all_primes_independent_check.py)
re-derive the character count and replay the base plus one- and two-block
lifts. These finite checks corroborate the algebraic proof; they are not
its basis. The prime-order hypothesis is
essential to *this argument*: for `p^k` with `k>1`, a nonzero additive
shift has order only `p`, so each two-shift color would split into
several cycles.
