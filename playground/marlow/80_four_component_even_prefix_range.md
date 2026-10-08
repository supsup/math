# Four-component adjacent page pairs: a partial even-prefix theorem

Let `p ≡ 9 (mod 16)` be prime, `k=(p−1)/2`, choose primitive `g`, and put
`a=g⁴`, `D=1+a`, `β=D/2`, `γ=β/a`, `δ=(1−a)/D` in `F_p`. The order of `a`
is `(p−1)/4≥10`, so `a≠0,±1`. Grow antipodal pages centered at
`1,...,j` using the unchanged affine square slots, with even `j=2r` and
`2≤j≤k−1=(p−3)/2`. Since `k` is even, actually `j≤k−2`.

**Claim.** If

    p − 513√p > 1024r + 2048,                              (A)

then the resulting partition can be repaired to attain

    d(K_{p,p+4r}) = p+4r + k + 2r.

The p-leaf offset lift gives the same sharp formula at
`t=p+4r+mp`, `m≥0`. This is a partial range of even growth prefixes,
not a claim about odd prefixes or every residue.

For consecutive pages `P_c,P_{c+1}`, put `w=v−c`, `u=v+δ`,
`x=c+β(u−c)`, and `y=c+γ(v−c)`. The identities
`x=c+1+β(v−c−1)` and `y=c+1+γ(u−c−1)` give the rectangle
`(u,x),(v,y)` in the first page and `(u,y),(v,x)` in the second.
They depend only on `a≠−1`, so [item 60's](60_skew_adjacent_pairs.md)
derivation applies to `a=g⁴`.
For `c≥2`, the **exact** parameters at which one source spoke has a
relabeled slot are

    E_c = c + {(a−q)/D : 0≤q≤c} ∪ c + {a(1−q)/D : 0≤q≤c}.

The two progressions each have `c+1` elements and share at least
`c+a/D`, so `|E_c|≤2c+1`. For `c=1`, `E_1={1+a/D}`.
The translated sets `E_c−c` are nested in `c`.

Write `λ_c(h)=ind_g(h−c) mod 4`. Each page has four components,
indexed by this label. For each `s∈{1,2,3}` seek `w` with

    (λ_c(u),λ_c(v),λ_{c+1}(u),λ_{c+1}(v))=(0,s,0,s).

The four affine arguments `w+δ,w,w+δ−1,w−1` have distinct roots.
[Item 79's](79_four_component_second_base_all_primes.md)
arbitrary-order quartic character count, independent of `c`,
gives at least

    N_s ≥ (p−256−513√p)/256

parameters per pattern. The case `x=y` forces `w=a/D`, hence
`u−c=1/D` and `v−c=a/D`. Their quartic labels are equal because
`a=g⁴`, so this case is excluded by every `s≠0` pattern already.

Choose one rectangle for each `s=1,2,3` at the final pair start
`c=2r−1`. The relabel set costs at most `2c+1` choices. A previously
chosen rectangle has two hubs; each hub forbids at most two line
parameters in a later choice (`u=H` or `v=H`). Thus the third choice
loses at most eight more. Condition (A) is exactly

    N_s > 2c+9 = 4r+7,

because `p−513√p>512c+2560=1024r+2048`.
The three chosen rectangles have disjoint hub sets, and their quotient
edges form the star `0−1,0−2,0−3` in both pages. Their trades
successively reduce both pages from four cycles to one. The same
three `w` values work at every earlier odd pair start because the
exception sets are nested, labels are translation-invariant, and
hub disjointness is unchanged under translation. Page trades leave
square slots unchanged; different page pairs use different colors.

All `k` square colors remain Hamilton cycles. Each of `j` pages is
one short cycle, and there are `p+2j` singleton spokes. The count is
`p+2j+k+j = p+4r+k+2r`. Parity gives at least `p+2j` singles,
and the remaining `2k(p+2j)` edges require at least
`ceil(k(p+2j)/p)=k+j` cycles because `j<p`, proving equality.

The [exact full-spoke checker](80_four_component_even_prefix_replay.py)
constructs the square slots, grows every page, checks each trade's
source edges, verifies component counts `4→3→2→1`, and checks every
spoke exactly once. Run `python3 /tmp/marlow_a4_late_pair_replay.py`.
It passes `p=41,j=4`, `p=73,j=4`, and maximal even prefixes
`p=41,j=18` and `p=73,j=34`. At the final pairs, its witnesses are
`p=41,c=17,w=(9,19,36)` and `p=73,c=33,w=(8,17,22)`.

An [exploratory exact-criterion scan](80_four_component_final_pair_small_scan.py)
finds a double-tree triple surviving the final-pair exceptions for all
151 primes in this class through 10,000, including cases outside (A).
It is finite evidence for a wider range, not part of the uniform proof.

Run from the repository root:

```sh
python3 playground/marlow/80_four_component_even_prefix_replay.py
python3 playground/marlow/80_four_component_final_pair_small_scan.py
```

**Boundary.** The complete-sum count `N_s≈p/256` cannot by itself
handle final pairs `c≈p/2`; the bound (A) reaches only roughly
`r<p/1024` once `p` dominates the `513√p` term. The maximal-prefix
replays are finite examples, not a uniform theorem for that range.
Also, this construction repairs only even `j`; odd `j≥3` still needs
a separate initial three-page repair or another compatible method.
