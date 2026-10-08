# A long-cycle switching gap in the odd-hub problem

The fixed-hub certificates and affine pages prove the proposed formula through `h=37`, but they do not give one construction for every odd `h=2k+1`. The remaining design step is sharp. For an odd base `t=h+2j`, `1≤j≤k−1`, equality in the parity/capacity lower bound requires exactly one singleton spoke at each leaf and exactly `k+j` cycles. With those counts, the total number of omitted hub visits is

`h(k+j)−kt=j`.

Our certificates realize that deficit as `k` full `2h`-edge cycles and `j` cycles of length `2(h−1)`. They assign three singleton spokes to `j` hubs and one to every other hub; a [cyclic interval schedule](33_interval_omission_schedule.md) fixes the leaf sets omitted by each cycle. This schedule balances every vertex but does not force the assigned edge classes to be connected. The connected-cycle step is the unproved uniform claim.

Two published switching results look relevant but do not supply that step as stated. [Horsley's Theorem 1.1](https://arxiv.org/html/1204.3368v1) decomposes certain complete bipartite graphs into prescribed even cycle lengths when the longest length is at most the smaller part size. [Asplund–Chaffee–Hammer's Theorem 24](https://arxiv.org/html/1608.05744v2) uses twin-vertex edge switches and, for unequal parts with smaller size `h`, assumes the two longest lengths sum to at most `2h+2`. Our desired list contains many cycles of length `2h`, so its two longest sum to `4h`. The theorems therefore cannot be invoked directly. Their local switch machinery may still suggest a repair operation; adapting it while preserving our singleton and omission schedule is a separate problem.

[Kim's October 2026 general theorem](https://arxiv.org/html/2610.07840v1) gives an `O(n)` cycle-and-edge decomposition for every `n`-vertex graph. Its degree-potential and expander argument allows slack in the number and lengths of parts. It does not produce the exact `k+j` long cycles needed at these bases.

**Question for a uniform proof.** Fix the interval schedule and singleton degrees above. Is there, for every odd `h` and each `j`, a connected edge assignment for each prescribed cycle support? A useful intermediate result would be a length-preserving trade that lowers the number of components in one scheduled 2-factor without increasing it in another or changing any vertex's prescribed incidence. The finite certificates through `h=35` demonstrate feasibility at those sizes; they do not establish that such trades always exist.
