# A partial infinite sequential-pair theorem for antipodal pages

For every prime \(p\equiv5\pmod8\), this note extends the one-trade [second-base repair](58_skew_second_base_one_trade.md) to an initial range of even growth prefixes. If \(r\ge1\), \(2r\le(p-3)/2\), and \(16r<p-3\sqrt p+10\), then

\[
d(K_{p,p+4r})=p+4r+\left\lceil\frac{(p-1)(p+4r)}{2p}\right\rceil
=p+4r+\frac{p-1}{2}+2r.
\]

The same equality holds at \(t=p+4r+pq\), \(q\ge0\), by the [offset lift](10_odd_hub_blocks.md). A [full-partition checker](60_skew_adjacent_pairs_full_replay.py) verifies every even prefix at six primes through 101; an [exact-criterion scan](60_skew_adjacent_pairs_criterion_scan.py) finds witnesses at every even prefix for all 42 primes in this class through 1000. Those finite checks do not extend the proved range for arbitrarily large primes.

Let p>=13 be prime with p≡5 (mod 8), let g be any primitive root,
a=g^2, k=(p-1)/2, D=a+1, beta=D/2, gamma=beta/a, and
delta=(1-a)/D in F_p. The order of a is k>=6, so all denominators used
below are nonzero and delta is not 0, 1, or -1. Start with the affine
midpoint square decomposition of K_{p,p}. Grow pages at centers
1,2,...,j in that order. The antipodal page at center c has underlying
hub edges {c+z,c+az}, z!=0, and its hub h!=c has beta-spoke leaf
c+beta(h-c) and gamma-spoke leaf c+gamma(h-c), unless that edge's
square-color slot was already selected by an earlier page. A selected
slot then has a fresh leaf instead of the original midpoint. Each page
has two components, on the quadratic-residue and nonresidue hub classes
relative to its center; fresh-leaf replacement preserves this shape.

## One line of page-page rectangles

For adjacent page colors P_c and P_{c+1}, choose v in F_p and put

    u=v+delta,
    x=c+beta(u-c),
    y=c+gamma(v-c).

The identities beta*delta=1-beta and gamma*delta=gamma-1 give

    x=c+1+beta(v-c-1),
    y=c+1+gamma(u-c-1).

Therefore the four spokes (u,x),(v,y) in P_c and (u,y),(v,x) in
P_{c+1} form a support-preserving rectangle whenever none of their
four underlying hub edges was selected by an earlier page. Set w=v-c.
The two page-component tests are exactly

    chi(F1(w))=chi(w(w+delta))=-1,
    chi(F2(w))=chi((w-1)(w+delta-1))=-1.

These tests exclude u or v equal to either center. They also exclude
x=y: that equality forces w=a/D, so F1(w)=a/D^2 has character +1.
When both tests hold, each selected pair of spokes is in the two
different components of its page. Exchanging the rectangle joins both
pages into one simple 2(p-1)-edge cycle. This preserves both leaf/hub
supports and all spokes of the partition.

## Exact relabel-exception set for a consecutive prefix

Each hub edge of a translated antipodal page belongs to exactly two
page translates. Indeed, if {z,az}+c={q,aq}+i for i!=c, the
same-orientation identification would force a=1; the reversed
identification determines i uniquely from c and z. Thus, at its
creation, page P_c has one distinct relabeled hub edge from each
earlier center i<c, and no others. A page-page rectangle exchange
never changes a square color or its slot table, so performing prior
pair repairs immediately does not alter this relabel analysis for
later growth pages.

For the pair (c,c+1), let an earlier center i=c-s, s>=1. The shared
edge of P_i and P_c has beta endpoint c-s/D and gamma endpoint
c-a*s/D as viewed from P_c. Its two possible hits by the candidate
source spokes (u,x) [beta] and (v,y) [gamma] are respectively

    v=c+(a-(s+1))/D,       v=c+a(1-(s+1))/D.              (1)

An earlier center i=c+1-s', s'>=1, gives a shared edge of P_i and
P_{c+1} whose beta endpoint is c+1-s'/D and gamma endpoint is
c+1-a*s'/D. Its two possible hits by the candidate cross spokes
(u,y) [gamma] and (v,x) [beta] are respectively

    v=c+a(2-s')/D,         v=c+(a-(s'-1))/D.              (2)

For the consecutive prefix, (1) has s=1,...,c-1 and (2) has
s'=1,...,c. Hence for c>=2 the *exact* set of parameters at which
one of the four candidate spokes uses a relabeled underlying edge is

    E_c=c+{(a-q)/D:0<=q<=c} union
        c+{a(1-q)/D:0<=q<=c}.                            (3)

For c=1 the set is only {c+a/D}; the q=1 terms of (3) do not arise.
For c>=2, each progression has c+1 distinct values. They share at least
c+a/D. This shared point has F1 character +1. Two other distinct
values of E_c are c+(a-1)/D (the F1 root w=-delta) and c (the F1
root w=0). They are also character-ineligible. Therefore at most

    |E_c intersect G_c| <= (2c+1)-3 = 2c-2                (4)

simultaneously character-good parameters are lost to relabeling,
where G_c is the translate of the two-test set above. At c=1, no
character-good parameter is lost. Formula (3), translated by -c,
also shows the exclusions grow monotonically with c; the character
tests in w do not depend on c. A single w surviving at the latest
odd pair-start c=j-1 consequently works for every earlier pair.

## The character count and partial theorem

The roots 0,-delta,1,1-delta of F1 F2 are distinct. The two monic
quadratic character sums equal -1 each. The squarefree quartic sum
has absolute value at most 3*sqrt(p), by the standard Weil bound
(for example, [Cohen--Sharma--Sharma 2019, Lemma 2.1](https://arxiv.org/pdf/1909.13074)). Summing
(1-chi(F1))(1-chi(F2))/4 over F_p, the four roots contribute at most
2 in total, while every nonroot contribution is precisely the
indicator of both characters being -1. Thus the number N of
character-good parameters satisfies

    N >= (p-3*sqrt(p)-6)/4.                                 (5)

Take j=2r with 1<=2r<=(p-3)/2. The latest pair starts at c=2r-1.
For c>=2, (4)--(5) leave a usable parameter whenever

    16r < p-3*sqrt(p)+10.                                  (6)

For r=1, the sole relabel exception is character-ineligible, and
condition (6) also suffices. Under (6), pair P_1 with P_2, P_3 with
P_4, ..., P_{2r-1} with P_{2r}, one rectangle trade per pair. Trades
touch disjoint page colors. They can be performed after all growth
steps or immediately after each pair; in the latter order they do not
change the square-color slots that determine later growth. Every old
square color remains a 2p-edge Hamilton cycle, and each short page
becomes one 2(p-1)-edge cycle. The resulting K_{p,p+4r} partition
has p+4r singletons and k+2r cycles, exactly

    d(K_{p,p+4r})=p+4r+ceil(k(p+4r)/p)=p+4r+k+2r.

Adding q disjoint p-leaf affine square blocks gives the same exact
formula for t=p+4r+pq, q>=0. The proof reaches about r<p/16, or
j=2r<p/8. It does **not** prove every even prefix through
j<=(p-3)/2: at that endpoint the upper bound 2c-2 is about p,
larger than the complete-character-sum lower bound N about p/4.
Finite scans may support that larger claim, but the present estimate
does not establish it.
