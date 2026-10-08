# One trade joins two antipodal pages at the second odd base

The [self-contained checker](58_skew_second_base_one_trade.py) replays six exact partitions, and a [separate line scan](58_skew_second_base_line_scan.py) checks the algebraic candidate through 1000. This theorem starts from the affine square and grows *both* pages before their simultaneous repair; it does not extend an already repaired first-base partition from [item 57](57_skew_first_base_all_prime_hubs.md).

Let `p≥13` be prime, `p≡5 (mod 8)`, choose any primitive root `g`, and write `a=g²`, `k=(p−1)/2`, `β=(1+a)/2`, `γ=β/a`, and `δ=(1−a)/(1+a)` in `F_p`. Since `a` has order `k≥6`, all denominators are nonzero and `δ∉{0,1,−1}`. Start from the affine midpoint square decomposition of `K_{p,p}`. Perform the two-leaf antipodal-starter growth moves at centers 1 and 2, before any connectivity repair. There are `p+4` singleton spokes, `k` full colors, and two short page colors `P_1,P_2`. Every full color is still one Hamilton cycle: each move replaces both spokes of a hub-pair slot by both spokes to one fresh leaf, leaving the cyclic hub order intact and retaining distinct leaf labels. Each short page has two components, the quadratic-residue and nonresidue hub classes relative to its center.

The page at center `c` has hub edges `{c+z,c+az}` for all `z≠0`; at hub `h≠c`, its two spoke leaves before overlap relabeling are `c+β(h−c)` and `c+γ(h−c)`. The center-1 and center-2 hub pages share exactly one edge. To see this, solve `{1+z,1+az}={2+w,2+aw}`. Equal orientation forces `a=1`; reversed orientation gives `z=1/(a+1)`, uniquely. Thus the common edge has hubs `(a+2)/(a+1)` and `(2a+1)/(a+1)`. During the second growth move, the spoke leaf of this one edge in `P_2` is the first move's fresh leaf rather than its old midpoint. All other `P_2` spokes retain the displayed affine formula.

For a parameter `v∈F_p`, set

`u=v+δ`, `x=1+β(u−1)`, `y=1+γ(v−1)`.

The identities `βδ=1−β` and `γδ=γ−1` imply `x=2+β(v−2)` and `y=2+γ(u−2)`. Hence `P_1` contains `(u,x),(v,y)` and `P_2` contains the crossed `(u,y),(v,x)`, except when either selected `P_2` spoke lies on the one relabeled common edge. Excluding all `v` for which `u` or `v` is one of that edge's two hubs costs at most four values. The equality `x=y` is one linear equation in `v` with nonzero slope `β−γ`, so excluding it costs at most one more value. Also `u≠v` automatically because `δ≠0`.

Let `χ` be the quadratic character. The two chosen spokes lie in different components of `P_1` exactly when

`χ(F_1(v))=−1`, where `F_1(v)=(v−1)(v+δ−1)`;

and in different components of `P_2` exactly when

`χ(F_2(v))=−1`, where `F_2(v)=(v−2)(v+δ−2)`.

The four roots `1,1−δ,2,2−δ` are pairwise distinct because `δ∉{0,±1}`. Each monic quadratic with distinct roots has complete character sum `−1`. The squarefree quartic `F_1F_2` has character sum of absolute value at most `3√p` by [Cohen–Sharma–Sharma 2019, Lemma 2.1](https://arxiv.org/pdf/1909.13074). Summing `(1−χ(F_1))(1−χ(F_2))` over the field gives `p+2+Σχ(F_1F_2)`. At the four roots, the summand is at most 2; away from roots it equals 4 exactly when both characters are `−1` and 0 otherwise. Thus the number `N` satisfying both component conditions obeys

`N ≥ (p−3√p−6)/4`.

For `p≥53`, this lower bound is strictly greater than 5. After excluding the at most five exceptional parameters above, at least one `v` yields a genuine rectangle. Exchange its two `P_1` spokes with the two crossed `P_2` spokes. Both old pages have exactly two components, and the two exchanged spokes belong to different components in each page, so the exchange joins each into one simple cycle. It preserves every vertex degree, support, and edge of the overall partition. The resulting `p+4` singletons plus `k+2` cycles meet the usual [parity/capacity lower bound](27_odd_hub_design_question.md) `t+ceil(kt/p)` at `t=p+4` (because `ceil(k(p+4)/p)=k+2`). Thus `d(K_{p,p+4})=(3p+11)/2`. The [p-leaf offset lift](10_odd_hub_blocks.md) gives the same exact formula on `t=p+4+pq`, `q≥0`.

The remaining primes below 53 are `p=13,29,37`. With primitive root `g=2`, explicit line parameters and rectangles are:

| p | δ | v | u | x | y | `P_1` spokes → `P_2` spokes |
|---:|---:|---:|---:|---:|---:|---|
| 13 | 2 | 4 | 6 | 7 | 11 | `(6,7),(4,11)` → `(6,11),(4,7)` |
| 29 | 11 | 0 | 11 | 26 | 4 | `(11,26),(0,4)` → `(11,4),(0,26)` |
| 37 | 29 | 17 | 9 | 21 | 11 | `(9,21),(17,11)` → `(9,11),(17,21)` |

A direct scan using the least primitive root finds a valid line parameter for all 42 primes `p≡5 (mod 8)` through 1000; these examples are numerical checks, not needed beyond the three small certificates for the proof. The theorem concerns the second odd base and its modular lifts, not all residues.
