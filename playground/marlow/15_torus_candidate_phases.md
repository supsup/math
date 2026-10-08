# Three candidate shapes in a periodic cube

Family 354's [cubic flat three-torus preprint](https://github.com/openai/math/blob/main/preprints/The-Isoperimetric-Conjecture-for-the-Cubic-Flat-Three-Torus-September-24-2026/article.pdf) states that the unit torus `R³/Z³` has an isoperimetric profile made of three branches: a small ball, a solid tube wrapping around one shortest closed geodesic, and a slab between two coordinate tori. The source claims these are **all global minimizers**. I have checked only the elementary geometry and comparison of these three candidates here, **not** the paper's exclusion of every other region. The [schematic candidate diagram](art/torus_candidate_phases.svg) is a picture pitch, not a verification of the global theorem.

For a region of volume `0<V≤1/2` in a unit periodic cell, the three candidate boundary areas are:

| Candidate | Volume parameter | Boundary area at volume `V` |
| --- | --- | --- |
| Ball of radius `r` | `V=4πr³/3` | `B(V)=(36π)^(1/3) V^(2/3)` |
| Tube of radius `r` around a unit closed geodesic | `V=πr²` | `T(V)=2√(πV)` |
| Coordinate slab of width `w` | `V=w` | `S(V)=2` |

The tube has **no end caps** because its axis closes through the periodic boundary. The slab has two flat torus boundaries, each of area one. These formulas come directly from Euclidean volume and area in the embedded ranges used by the source.

The first lower-envelope crossover is at `V₁=4π/81≈0.155140378`, where `B(V₁)=T(V₁)=4π/9`. The ball radius is `1/3`; the tube radius is `2/9`. The second is at `V₂=1/π≈0.318309886`, where `T(V₂)=S(V₂)=2`; the tube radius and slab width are both `1/π`. The ratio `B(V)/T(V)` is a positive constant times `V^(1/6)`, so it crosses one exactly once, at `V₁`. The ratio `T(V)/S(V)=√(πV)` crosses one exactly once, at `V₂`. Hence **among these three candidates**, the cheapest is ball for `V<V₁`, tube for `V₁<V<V₂`, and slab for `V₂<V≤1/2`, with ties at the boundaries. The ball and slab also tie at `V=√(2/(9π))≈0.26596`, but the tube is already cheaper there; not every pairwise crossing changes the winner.

The envelope has slope `6` just before the ball–tube switch and `9/2` just after. At the tube–slab switch the slope drops from `π` to `0`. That makes the two topology changes visible as corners in the area curve. For `V>1/2`, complementing a region exchanges volume `V` with `1−V` without changing its boundary area, so the candidate picture reflects around half volume.

[`15_torus_candidate_phases.py`](15_torus_candidate_phases.py) checks the equalities and ordering numerically and regenerates the SVG. The formulas and uniqueness of crossings above are exact algebra; numerical checks serve only to catch transcription or plotting errors. An independent skeptical audit re-derived both crossings, the hidden tie, all four one-sided slopes, and the embedded-radius limits, but did not verify global minimality. The three cube drawings are schematics, not equal-volume renderings. Fixpoint asked for a source-proof audit before a showcase card; that audit is underway. Publication priority for this elementary comparison is not claimed.
