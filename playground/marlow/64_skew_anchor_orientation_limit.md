# Orientation condition for repeated page absorption

Suppose a connected bipartite page color A is a simple cycle. Let
e=(u,x), f=(v,y) be two spokes with distinct hubs and distinct leaves,
and suppose a different color owns the crossed spokes (u,y),(v,x).
Orient A arbitrarily. The support-preserving rectangle exchange

    (u,x),(v,y)  <->  (u,y),(v,x)

leaves A connected **if and only if** e and f have opposite directed
types on that cycle (one hub-to-leaf and one leaf-to-hub). To prove
this, cut the oriented cycle at the two spokes. If their types are
opposite, the crossed edges reconnect the two open paths end-to-end
as one cycle. If their types are the same, each path closes on
itself, yielding two cycles. The other color's connectivity is a
separate question; when its two selected spokes are in different
components, the same exchange joins those components.

For an antipodal original page, orient each quadratic-character
component by multiplication by a=g^2. Its beta spokes are
hub-to-leaf and gamma spokes leaf-to-hub. After the first switch
joining two original components, one entire component is traversed
backward, so an untouched beta/gamma pair from the **same** original
component remains opposite on the merged cycle. This is the
orientation fact used for the first (+,-) absorption in item 64.

After a second absorption, the connected anchor's current direction
need not be uniform on each original component. Define sigma(e)=+1
if an untouched original spoke e is traversed in its original
component's direction and -1 otherwise. A future beta/gamma pair
from one original component has opposite current types exactly when
its two sigma values agree. Equivalently, the anchor-preservation
condition is an exact, checkable **reversal-parity equality**.
The character signs (+,-) only say that its hubs lie in the same
original anchor component and different new-page components; they
do not determine this parity equality after two absorptions.

An exact counterexample to blindly repeating the item-64 sign rule
occurs at p=29, primitive root g=2. Grow pages at centers 1,2,3,4.
Switch P1 with P2 at formula parameter z=2, then P1 with P3 at z=3.
All three page colors are connected. A third P1/P4 formula candidate
at z=21 has the prescribed signs (+,-) and all four required spokes:

    P1: (10,9),(6,15) ; P4: (10,15),(6,9).

The two P1 spokes lie in its original quadratic-residue component,
but on the current P1 cycle they are **both** directed leaf-to-hub.
The switch joins P4 into one 28-hub cycle and splits P1 into 8- and
20-hub cycles. The self-contained exact replay is

    python3 -I playground/marlow/64_skew_odd_prefix_replay.py --anchor-counterexample

It checks the character signs, all spoke memberships, every color's
degree-two condition, and exact global spoke coverage. This is a
counterexample to a proposed reusable *sign-only* anchor lemma,
not to the existence of an optimal K_{29,37} decomposition. The
triple-plus-adjacent-pairs construction repairs later pages there.

A greedy strategy that keeps using the same anchor can also stall,
despite the successful triple-plus-pairs certificates. This only
shows that the chosen strategy cannot establish the full odd-prefix
range. A uniform theorem beyond the current roughly p/8 range would
need either a bound on the reversal-parity-qualified candidates or a
more flexible page matching argument.

The p=29 stall has a sharper exact certificate. After absorbing
P2,P3,P4 into P1 with z=2,3,5, respectively, the six (+,-)
candidate parameters for P1/P5 are z=3,5,8,13,15,21.
The spokes at z=13,15 are unavailable. Each of the other four
joins P5 but splits P1, into hub-size pairs [7,21], [9,19],
[10,18], and [5,23], respectively. Replay with
`python3 -I playground/marlow/64_skew_odd_prefix_replay.py --anchor-stall`.
This exhausts only the displayed affine (+,-) line in that chosen
anchor state; it says nothing about other rectangles or earlier
switch choices.
