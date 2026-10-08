# Three standard shapes in a rectangular three-torus

**Candidate comparison only.** The cubic [three-shape calculation](15_torus_candidate_phases.md) extends cleanly to a rectangular flat three-torus of unit volume. Write its side lengths as `a≤b≤c` with `abc=1`, and put `v=min(V,1−V)`. Among round balls, circular tubes around closed geodesics, and pairs of parallel flat tori, the cheapest candidate area is

> `F(v)=min{(36π)^(1/3)v^(2/3), 2√(π a v), 2/c}`.

This is **not** a claim that these standard shapes beat every possible region in a noncubic torus. The cubic global classification is the separate family-354 preprint claim audited in [item 16](16_torus_source_audit.md). [Milman's 2025 paper, §1.2](https://onlinelibrary.wiley.com/doi/10.1002/cpa.70020) already gives the candidate switches for the one-parameter rectangular family with side ratio `(β,1,1)` and discusses partial global-minimality results. The formulas here are an elementary extension of the *candidate comparison* to arbitrary ordered rectangular side lengths, with no novelty or priority claim.

The ball area depends only on `v` because `abc=1`. A tube with circular cross-section around a closed geodesic of length `ℓ` has `v=πr²ℓ` and boundary area `2πrℓ=2√(πℓ v)`. The shortest nonzero lattice vector has length `a`, so the cheapest tube family uses a shortest-axis direction (with ties if short sides coincide). A pair of parallel flat tori with primitive integer normal `m` has one-sheet area `√((m₁/a)²+(m₂/b)²+(m₃/c)²)`, at least `1/c`; equality uses coordinate planes orthogonal to a longest side. Hence the cheapest slab area is `2/c`.

The active crossings are

| switch | volume `v` | area | curvature/slope before → after |
| --- | ---: | ---: | ---: |
| ball → shortest tube | `v₁=4πa³/81` | `4πa²/9` | `6/a → 9/(2a)` |
| shortest tube → thinnest-wall slab | `v₂=b/(πc)` | `2/c` | `π/b → 0` |

They always occur in this order within the half-volume range. Indeed

`v₁/v₂=(4π²/81)(a/b)²<1`, and `v₂=b/(πc)≤1/π<1/2`.

For the side ratio `(β,1,1)` in Milman's convention, unit-volume rescaling gives `a=β^(2/3)` and `b=c=β^(−1/3)`. The formulas reduce to his candidate thresholds `4πβ²/81` and `1/π`.

The ratio `v₂/v₁=(81/(4π²))(b/a)²` quantifies how unequal short and middle sides widen the tube phase. The **formal area-curve** equality of ball and slab is at `v₀=√(2/(9π))c^(−3/2)`, strictly between `v₁` and `v₂`; the tube is cheaper there. For a strongly stretched torus, a ball of that formal volume may no longer embed, so this is not generally a tie between actual regions. The candidate envelope has two downward slope jumps, as expected for a concave profile.

All three *active* candidates are embedded. At `v₁`, the ball radius is `a/3<a/2`, so it fits inside the shortest period. At `v₂`, the tube radius is `b/π<b/2`, below its smaller transverse half-period. A slab orthogonal to side `c` has width `vc≤c/2` throughout `v≤1/2`. These observations justify the entire lower envelope as an attainable standard-candidate comparison, including each tie, and complements give the other half of the torus volume.

For example, `(a,b,c)=(1/2,1,2)` moves the switches from the cube's `4π/81,1/π` to `π/162,1/(2π)`. Its formal hidden ball–slab crossing is `1/(6√π)`, and its tube-phase volume ratio is `81/π²` rather than the cube's `81/(4π²)`. [The generated figure](art/rectangular_torus_candidates.svg) compares the two cases on a square-root volume axis. Run [`21_rectangular_torus_candidates.py`](21_rectangular_torus_candidates.py) to recheck these identities and regenerate it.
