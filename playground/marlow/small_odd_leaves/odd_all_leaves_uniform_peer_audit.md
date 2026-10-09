# Skeptical audit of the proposed uniform odd-small-leaf construction

**Verdict: the proposed construction is valid as stated.** For every odd `t=2λ+1>=3` and odd `p>=t`, it proves

```text
d(K_(p,t)) = p + ceil(pλ/t),       λ=(t-1)/2.
```

I independently checked the row/column selector, the original weave's full edge coverage, the surgery's cycle connectivity and resource disjointness, the singleton count, and the unbounded lift. The standalone [literal checker](odd_all_leaves_uniform_peer_check.py) has no imports or solver dependency. It reconstructed every spoke for 665 seed cases, including every `1<=r<=2λ` for `1<=λ<=25` and five boundary choices each at `λ=32,64,128`; all passed. This is a mathematical and finite replay verdict on the stated construction, not a claim about publication priority. No reviewed branch or RFC was changed.

## Lower bound and base seed

Every hub has odd degree `t`, so if `s` singleton edges occur, `s=p+2k` for some `k>=0`. A simple cycle has at most `2t` spokes, hence its count `c` satisfies

```text
c >= ceil((pt-s)/(2t)) = ceil((pλ-k)/t) >= ceil(pλ/t)-k.
```

Thus `s+c >= p+ceil(pλ/t)+k`. Equality requires one singleton per hub.

At `p=t`, label both sides by `Z/t`, use `(h,h)` as singleton, and for `j=0,...,λ-1` use the directed leaf arcs `(h+2j+1) -> (h+2j+2)` labeled by `h`, arithmetic modulo `t`. Each color is a Hamilton cycle on the `t` leaves, and shifts `1,...,2λ` use every off-diagonal spoke once. This is the sharp `t`-hub seed with `λ` cycles.

## The even-hub weave at `p=t+2r`

Fix `1<=r<t`, put `n=λ+r`, `q=2n=p-1`, and `m=t-1=2λ`. Label old hubs by `Z/q`, old leaves by `L_0,...,L_(m-1)`, and let `z=L_m` be the extra leaf. For `j` in `Z/n`, define `H_(j,k)=2j+k mod q` and the original cycle

```text
H_(j,0), L_0, H_(j,1), L_1, ..., H_(j,m-1), L_(m-1), H_(j,0).
```

The `m` hubs in a row are distinct because `m<=q`. At each old leaf `L_k`, the two incident hubs from row `j` are `H_(j,k)` and `H_(j,k+1 mod m)`. Their offsets have opposite parity: for `k<m-1` they differ by one, while for `k=m-1` the offsets are `m-1` and `0`, again opposite since `m` is even. As `j` runs through `Z/n`, each parity class of `Z/q` occurs once. Hence the `n` cycles partition all spokes of `K_(q,m)`. Initially make every old hub's `z` spoke a singleton.

## The selector really is a noncollision matching

We need `λ` pairs `(j,s)` with distinct rows `j`, columns `s=0,...,λ-1`, and values `j+s mod n`.

If `n` is odd, choose `j=s`. Rows are distinct because `λ<n` and the values `2s mod n` are distinct because multiplication by two is invertible modulo odd `n`.

If `n=2a` is even, define `σ(j)=(j+a-1) mod (2a-1)` for `0<=j<=2a-2`. This permutes the columns `0,...,n-2`, which include `0,...,λ-1` since `n=λ+r` and `r>=1`. Choose the unique inverse row `j=σ^(-1)(s)` for each required column. To check that `j+σ(j) mod n` is injective, split the row range:

```text
0<=j<=a-1:       σ(j)=j+a-1,   j+σ(j)=2j+a-1 mod 2a;
a<=j<=2a-2:      σ(j)=j-a,     j+σ(j)=2j-a mod 2a.
```

Within each range the values differ by two and remain distinct modulo `2a`; the two ranges have opposite parity. Thus all `n-1` displayed sums are distinct, and the selected subset is valid. This also covers `n=2`, where the second range is empty.

## Why each cut gives one simple longer cycle

Write `a=2s`, `b=a+1`, and abbreviate `H_k=H_(j,k)`. In the selected row, cut `H_a-L_a` and `H_b-L_b`. The remaining cycle edges form two paths: the short path `L_a-H_b` and the other path from `L_b` around the rest of the old cycle to `H_a`. Introduce the new hub `u=q`, remove old singleton spokes `H_a-z` and `H_b-z`, and insert

```text
H_a-z, H_b-z, u-L_a, u-L_b
```

as cycle edges. They join the two paths into the single cycle

```text
H_a - z - H_b - L_a - u - L_b - (rest of old row) - H_a.
```

Every old vertex appears once, and `u,z` are new to the row, so the cycle is simple. This remains true for `m=2`: the long path is just `L_b-H_a`. The two deleted old spokes become singleton edges. The surgery replaces two cycle spokes by four and raises the cycle length from `2(t-1)` to `2t`.

The chosen columns are all distinct, so the new hub's `u-L_a,u-L_b` cycle spokes cover each old leaf once; `u-z` remains its singleton. Also,

```text
H_a = 2(j+s) mod q,       H_b = 2(j+s)+1 mod q.
```

Distinct selector sums modulo `n` reserve disjoint pairs of old hubs. Thus no `H-z` spoke is reused in two surgeries. Each selected old hub trades its original `H-z` singleton for exactly one deleted old spoke singleton; each unselected old hub keeps `H-z`. There is exactly one singleton at every hub. On the leaf side, each old leaf gets one singleton and `z` gets `2r+1`.

Exactly `λ` rows are modified and `n-λ=r` remain. There are therefore `λ` cycles of length `2t` and `r` cycles of length `2(t-1)`, with no missing or repeated spoke. Their count is `n=λ+r=ceil(λ(t+2r)/t)`, since `λ(t+2r)/t=λ+r-r/t` and `0<r<t`. This attains the lower bound for each seed `p=t+2r`.

## All odd hub counts

Every odd `p>=t` is uniquely `p=t+2r+2tm` with `0<=r<t` and `m>=0`. Take the corresponding seed, then add `2m` disjoint copies of the sharp `t`-hub block on the same leaf set. Each copy contributes `t` new singleton spokes and `λ` new cycles; disjoint hub sets keep their spokes disjoint. The cycle count rises by `2mλ`, exactly the increase in `ceil(pλ/t)`. This proves the displayed formula for all allowed `p`.

The checker reconstructs the original weave, applies each cut literally, tests every resulting part is one connected simple cycle, tests all singleton and cycle spoke multiplicities, and compares their union to the complete `p*t` universe. Its finite range is corroboration of the symbolic proof, not the reason the theorem extends to all `t,p`.
