# Two page-only trades repair the first three antipodal growth pages

Let p>=13 be prime, p≡5 (mod 8). Choose any primitive root g, put
a=g^2, k=(p-1)/2, D=a+1, beta=D/2, gamma=beta/a, and
delta=(1-a)/D in F_p. The antipodal page is the hub-edge set
{{z,az}:z!=0}. It consists of two alternating cycles, on the quadratic
residues and nonresidues. Grow the affine midpoint square at centers
1,2,3, in that order, before doing any repairs. Each old square color
remains Hamiltonian. Each page color P_1,P_2,P_3 has two components.
An edge of a later page that was selected by an earlier page retains
the same two hubs and component, but its leaf is replaced by a fresh
leaf. Distinct page translates share exactly one hub edge, and no hub
edge belongs to three translates.

## Line of rectangles for two centers

For centers c and d=c+s, s!=0, choose z in F_p and set

    v=c+s*z,       u=v+s*delta,
    x=c+beta(u-c), y=c+gamma(v-c).

Because beta*delta=1-beta and gamma*delta=gamma-1,

    x=d+beta(v-d), y=d+gamma(u-d).

Thus the earlier page has source spokes (u,x) [beta], (v,y) [gamma],
and the later page has cross spokes (u,y) [gamma], (v,x) [beta],
unless one of these later-page edges was relabeled by a previous
growth. Define the monic quadratics

    F1(z)=z(z+delta), F2(z)=(z-1)(z+delta-1).

The two selected hubs lie in different components of the first page
exactly when chi(F1)=-1, and in different components of the second
exactly when chi(F2)=-1. The tests also ensure no hub is a page center
and u!=v (since delta!=0).

## First switch, P_1 with P_2

Choose z1 with signs (chi(F1),chi(F2))=(-1,-1). Then the candidate
joins both two-component pages. The only hub edge of P_2 that was
relabelled is its overlap with P_1. Its gamma and beta endpoint hits
coincide on the candidate line at z=a/D. There F1=F2=a/D^2 has
quadratic character +1, so no (-1,-1) candidate is lost. The same
calculation shows x=y only at z=a/D. Consequently *every* (-1,-1)
candidate gives a valid degree/support-preserving switch P_1<->P_2.

## Second switch, P_1 with P_3

Choose z2 with signs (chi(F1),chi(F2))=(+1,-1) on the line c=1,s=2.
The two requested source spokes of P_1 are beta at u and gamma at v,
and lie in the **same original** P_1 component. The P_3 cross spokes
lie in its two **different** components. After the first switch,
P_1 is one cycle. Orient each original P_1 component by multiplication
by a: beta spokes go from hub to leaf; gamma spokes go from leaf to
hub. The first switch cuts one beta spoke from one original component
and one gamma spoke from the other, then joins the two open paths.
In the resulting P_1 cycle one original component is traversed
forward and the other backward. Every untouched beta/gamma pair
within either original component therefore retains opposite
orientations. A crossed two-spoke exchange on a single bipartite
cycle stays one cycle when its removed spokes have opposite
orientations (cut the cycle into two paths; the cross edges join the
paths end-to-end). Hence the second switch leaves P_1 connected
while joining P_3's two components.

There are only two kinds of exceptional (+1,-1) parameters:

* P_3's overlap edge with P_2 was relabelled; it has one beta and one
  gamma endpoint, so it can hit the requested cross spokes for at
  most two z2 values.
* The first switch removed two original P_1 spokes, so at most two z2
  values request an unavailable source spoke.

P_3's other relabelled edge is its overlap with P_1. Its two endpoint
hits coincide at z=a/D, where F1=F2=a/D^2 has character +1, so it
cannot pass (+1,-1). The equality x=y has the same parameter and
is likewise automatically excluded. Thus at most four (+1,-1)
parameters are lost. No earlier switch touches P_3; the second
switch preserves every color's support and every spoke of K_{p,p+6}.

## Supply of the two character patterns

The four roots 0,-delta,1,1-delta of F1F2 are distinct because
a has order k>=6, so delta is not 0,1,-1. Each quadratic character
sum is -1, and the squarefree quartic sum has absolute value at most
3*sqrt(p) by the Weil bound (e.g. Cohen--Sharma--Sharma 2019,
Lemma 2.1, https://arxiv.org/pdf/1909.13074). At each root, either
of the sign-indicator expressions below contributes at most 1/2;
all four roots contribute at most 2. Therefore

    N_-- >= (p-3*sqrt(p)-6)/4,
    N_+- >= (p-3*sqrt(p)-8)/4,

where N_-- and N_+- count nonroot parameters with the indicated
two signs. The first lower bound is positive for every p>=29 in
the class. The second exceeds four for every p>=53 in the class:
p-3*sqrt(p)>24 at p=53 and grows thereafter. Hence the two
switches exist for every such prime, for *any* primitive root g.

The only smaller class primes are 13,29,37. The self-contained
[the self-contained checker](64_skew_odd_prefix_replay.py) constructs their square and
three-page growth, selects the smallest available formula parameters,
applies both switches, and verifies exact full spoke coverage,
all 2-regular supports, connectivity, and the lower-bound count.
It also checks p=53,61,101. An [independent raw-graph audit](64_skew_three_independent_audit.py)
verified all six finite witnesses, and an [all-root audit](64_skew_three_all_roots_audit.py)
verified every primitive root at p=13,29,37. The small
witnesses (g=2) are:

| p | z1 | z2 |
|---:|---:|---:|
| 13 | 3 | 5 |
| 29 | 2 | 3 |
| 37 | 16 | 4 |

Thus for all p>=13 prime with p≡5 (mod 8), the first three pages
can be repaired with two page-only rectangle trades, giving

    d(K_{p,p+6})=(p+6)+k+3.

Adding disjoint p-leaf affine square blocks extends equality to
t=p+6+pq, q>=0.

## Later odd prefixes: a rigorous partial range

Let j=2r+1 with r>=2 and j<=(p-3)/2. First repair pages 1,2,3
by the two trades above. Then pair pages 4,5; 6,7; ...;
2r,2r+1 by one adjacent-page trade per pair. These later trades
touch disjoint page colors and no square color. Performing the first
two trades before or after later growth makes no difference to later
square-color slot selections: page-page trades never change the
square colors or their slot table.

For an adjacent pair starting at center c>=2 in the consecutive
growth prefix, the exact set of scaled character-line parameters
whose requested spokes were relabeled by earlier growth is

    E_c={(a-q)/D:0<=q<=c} union
        {a(1-q)/D:0<=q<=c}.

Each progression has c+1 distinct values. The shared q=0 value
a/D has both character signs +1; the additional distinct values
(a-1)/D and 0 are roots of F1. Thus among the simultaneous
(-1,-1) candidates, at most 2c-2 are lost. The complete-character
sum above gives at least (p-3*sqrt(p)-6)/4 candidates. The E_c
are nested, so the latest pair at c=2r controls every earlier
pair. It has a surviving candidate whenever

    16r < p-3*sqrt(p)+2.

Under this condition all j pages become one short cycle each, giving

    d(K_{p,p+2j})=(p+2j)+k+j.

The same exact equality holds after adding q disjoint p-leaf
square blocks, at t=p+2j+pq for q>=0. The inequality proves
roughly j<p/8, not every allowed odd prefix. The exact arithmetic
scan [for odd prefixes](64_skew_odd_prefix_criterion_scan.py) finds a survivor for
the latest pair in all 42 class primes through 1000, but this finite
observation is not a proof for larger primes. The full-partition
checker [for full partitions](64_skew_odd_prefix_replay.py) accepts `p:j` and
verifies maximal odd prefixes at p=13:j=5, 29:13, 37:17, 53:25,
and 61:29; it checks every spoke and all final cycle supports.
At p=13,j=5 it uses three page-only trades, one fewer than the
earlier four-trade finite trace.

The [orientation-limit note](64_skew_anchor_orientation_limit.md) gives
an exact p=29 counterexample to extending the `(+,−)` sign test by
repeatedly absorbing later pages into the same anchor. It only limits
that particular strategy; the paired-page construction above still
repairs the tested odd prefixes.
