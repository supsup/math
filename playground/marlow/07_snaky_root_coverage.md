# Where Snaky's 32 root branches overlap

**Source and scope.** Family 187's [21-move Snaky certificate](../../preprints/Snaky-in-21-Maker-moves-September-25-2026/verification/certificate.txt) ends with a card whose required Maker set is empty, whose clean envelope has 251 cells in a `17×17` box, and whose height is 21. Its root move is `(8,8)`, after which it offers 32 transformed child conditions. The paper supplies the soundness argument and its [checker](../../preprints/Snaky-in-21-Maker-moves-September-25-2026/verification/verify_certificate.py) validates the finite set identities; this note asks a smaller descriptive question: **how many child envelopes contain each board cell?**

[`07_snaky_root_coverage.py`](07_snaky_root_coverage.py) reconstructs all 728 certificate cards from the source bytes, checks the pinned certificate hash and root invariants, and counts membership in the final card's 32 child envelopes. The [heatmap](art/snaky_root_coverage.svg) covers the `17×17` box. The exact results are:

| Quantity | Count |
| --- | ---: |
| Distinct cells in the union of child envelopes | 251 |
| Total cell–child memberships | 4,420 |
| Cells in every child envelope | 1: the Maker pivot `(8,8)` |
| Other cells lying in 31 of 32 child envelopes | **43** |
| Other cells lying in only one child envelope | 3 |
| Cells of the `17×17` box outside the union | 38 |

The 43 high-overlap cells are a sharp illustration of why the root's *intersection* condition matters. After Maker claims `(8,8)`, if Breaker's next cell is one of those 43, it lies in 31 child envelopes; just one child's **sufficient clean-envelope precondition** survives. If Breaker plays outside the 251-cell union, all 32 survive. The certificate establishes at least one surviving child for any legal Breaker reply because the only common envelope cell is the Maker-owned pivot. A failed precondition does **not** show that its child strategy is impossible; this is a coverage count of a proof certificate, not a game-theoretic count of winning branches or probabilities.

The script's independent parser can fail visibly if the pinned file hash changes, a reference points forward, the final card is not `(required=∅, support=251, height=21)`, or its counted overlap disagrees with the assertions. A separate skeptical audit instrumented the paper's original checker in memory and reproduced the 4,420 memberships and all overlap counts without using my parser. The paper's own checker separately prints `PASS` for the 728-card, height-21 certificate. I have not built the [Lean formalization](../../lean/docs/187.md), and the heatmap does not simulate Maker or Breaker. I found this measurement useful because it exposes how tight a multi-branch certificate can be even with 32 alternatives. I do not claim the overlap counts are a new theorem or that they improve the 21-move strategy.
