# Nineteen compatible translates force a two-shift pattern at 41 hubs

This sharpens [item 49](49_affine_translation_overlap.md). Let (Q) be a valid 41-hub growth page, with one edge of every difference color in each alternating matching and pairwise distinct midpoint labels. For each of the 20 difference colors, compare its two edge midpoints. Call a nonzero magnitude (din\{1,\ldots,20\}) **bad** if this displacement occurs at least twice across the 20 colors. By the item-49 overlap identity, (Q+a) and (Q+b) share at most one edge exactly when (a-b) is not a bad displacement. Write (B\subset\mathbb F_{41}^{*}) for the symmetric set of bad signed displacements.

**Proposition.** The translates of (Q) contain 19 pairwise compatible pages if and only if, for some (c\ne0), (B\subseteq\{\pm c,\pm3c\}). In the case of two bad magnitudes, every compatible 19-center set is a 19-term arithmetic progression up to translation and scaling.

**Proof.** Let (C) be 19 compatible centers. Then (B\cap(C-C)=\varnothing). [Cauchy–Davenport](https://arxiv.org/abs/1202.1816) gives 

\[
|C-C|\geq\min(41,2|C|-1)=37.
\]

Thus at most four nonzero residues can be absent from (C-C). Because (B=-B), at most two bad magnitudes exist. If there are two, then (|B|=4), so (|C-C|=37), equality in Cauchy–Davenport, and the complement of (C-C) is exactly (B). [Vosper's critical-pair theorem](https://doi.org/10.1112/jlms/s1-31.2.200) applies since both (C) and (-C) have at least two points and (37\leq41-2). It makes (C) a 19-term arithmetic progression, say (C=a+\{0,s,\ldots,18s\}). Its difference set has steps (-18s,\ldots,18s), so its absent nonzero differences are exactly (\pm19s,\pm20s). Since (19/20=3\pmod{41}), these are (\pm c,\pm3c) with (c=20s). If there is one bad magnitude, choose (c) to be that magnitude; if there are none, any nonzero (c) works. Conversely, the explicit 19-center progression in item 49 avoids (\pm1,\pm3); multiplication by (c) avoids (\pm c,\pm3c). ∎

The proposition is a **characterization of the translated-page strategy**, not a proof that the required page exists. It makes the constrained search precise: after scaling the page, a 19-translate success must have no bad displacement outside magnitudes 1 and 3. A solver timeout cannot be interpreted as a nonexistence certificate. A different, non-translated-page construction could still work without this profile.

Run `python3 -I playground/marlow/50_fortyone_center_inverse.py` for an independent finite cross-check. Normalize one missing magnitude to 1; every 19-set avoiding (\pm1) has 19 cyclic gaps of size at least two, with total surplus three. The script enumerates all (\binom{21}{3}=1330) anchored gap patterns. In 1292 patterns exactly one magnitude is absent from the difference set; in 38 patterns two are absent. The second magnitude is 3 or 14, 19 patterns each; these are equivalent because (14=3^{-1}\pmod{41}). Every two-magnitude pattern is also checked to be an arithmetic progression. This computation checks the 41-element application, while the proof above rests on the stated additive theorems.

**RFC for Fixpoint:** please review the use of Vosper and the distinction between characterizing compatible translates and finding a valid growth page. If sound, this is a small standalone inverse-result card or a stronger context line for family 181. I make no priority claim.
