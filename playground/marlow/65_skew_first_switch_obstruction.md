# One-switch obstruction for the antipodal first page

Let `p` be prime, `p ≡ 1 (mod 4)`, and write `p−1 = 2 A q`, where
`A = 2^(v₂(p−1)−1) ≥ 2` and `q > 1` is odd. Choose a primitive root `g` and
put `a = g^A`, so `ord(a) = 2q` and `−1 = a^q`. Use the strong-starter matching
`S = {{x,ax}: log_g(x) mod 2A ∈ {0,…,A−1}}` and its antipode `−S`. Grow at
center `1` with new leaves `p,p+1`, moving the two spokes of each translated
matching edge out of the old affine-square color and into a new page color `P`.
This is precisely the first-base starter used in items 53/55/62. The
assumption `q>1` matters: for `q=1`, `a=−1` and `S=−S`, so these two pages
are not disjoint.

**Claim.** No single support-preserving checkerboard rectangle trade between
two current colors can strictly decrease the total number of cycle
components. This applies to all such `p ≡ 1 (mod 4)`, including the
`p ≡ 5 (mod 8)` two-component page and the `p ≡ 1 (mod 8)` multi-component
page. It does not obstruct zero-gain setup trades followed by a gain, or
other starter constructions.

Because multiplication by `−1 = a^q` exchanges the two exponent halves
modulo `2A`, the edge union `S ∪ (−S)` is exactly
`{{x,ax}: x∈F_p^×}`. Put `β=(1+a)/2` and `γ=β/a`. The page therefore has,
for each old hub `h=1+x` with `x ≠ 0`, exactly the two edges
`(h,1+βx)` and `(h,1+γx)`. Hub `1` is absent from `P`, and the page's hub
components are the cosets of `<a>`: two hubs `1+x,1+y` are in the same
component exactly when `y/x∈<a>`. In particular `P` has `A` cycles. This
follows since a shared leaf gives `βx=γy`, hence `y=ax`, and these are all
hub transitions.

For square color `C_d`, `1≤d≤(p−1)/2`, put `s=d/2` in `F_p`. Its old edges
are `(h,h+s)` and `(h,h−s)`. For each difference class `±d`, the edges of
`S∪(−S)` are represented by `x` and `−x` in `{{x,ax}}`; their translated
midpoints are `1±βx`, distinct because `β≠0`. These two starter slots are
replaced individually by `p` and `p+1`, so `C_d` remains a
Hamilton cycle with the cyclic order of its remaining old edges unchanged.
Along this cycle, old edges of slope `+s` have one traversal orientation,
and old edges of slope `−s` have the other. A checkerboard switch on two old
edges of **equal** slope splits `C_d` into two cycles; with **opposite**
slopes it leaves `C_d` connected. This is the standard cut-and-rejoin fact
for two edges of a simple cycle. The page has only old-leaf edges, so every
square/page rectangle necessarily uses old square edges.

Consider a rectangle with square edges `(u,u+εs)` and `(v,v−εs)`,
`ε∈{±1}`, whose crossed edges lie in `P`. Write `u=1+U`, `v=1+V` and let
`B,C∈{β,γ}` be the two page slopes. The crossed-edge equations are

```
V−εs = B U,       U+εs = C V.
```

Eliminating `s` gives `(C−1)V=(1−B)U`. Neither `U,V` nor `C−1` is zero.
For the four choices of `(B,C)`, this yields

```
V/U ∈ {−1, a, a^−1} ⊂ <a>.
```

Thus the page edges belong to the *same* page component for opposite
square slopes. A switch there cannot merge page components, while `C_d`
stays connected. For equal square slopes, `C_d` splits, while a switch can
merge at most two page components, so again the total component count cannot
decrease. A switch between two square colors cannot decrease it either:
both square colors already have one component. That proves the claim.

The exact starter hypotheses and the ``q>1`` qualifier should accompany
the statement. Independent enumeration at `p=13,29,37,41,53,61,73,89,97,101,113`
found no improving first rectangle, consistent with the proof. The five
`p ≡ 1 (mod 8)` saved traces begin with zero-gain setup trades; their
component-drop sequences are respectively `[0,1,1,0,1]`, `[0,1,1,1]`,
`[0,1,0,1,0,1]`, `[0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1]`, and
`[0,1,1,1,0,1,1,1,1]`.

Independent finite replay: [first-switch trace audit](65_skew_first_switch_trace_audit.py).
