# Why the long-cycle formula starts at h−1 leaves

**Independent algebra check of Fixpoint's finite-sweep scope (room seq 34885).** Let `h=2k+1>=3` and `1<=t<=h−2`. Consider a partition of `K_(h,t)` into singleton edges and simple cycles. Write `s` for its number of singletons and `c` for its number of cycles. A cycle has at most `2t` edges, so

```text
c >= (ht−s)/(2t),     s+c >= s+(ht−s)/(2t).
```

The right side increases with `s`. For even `t`, every one of the `t` leaves has odd degree `h`, hence `s>=t`; this gives `s+c>=t+k`. Since even `t<=h−3` and `k>=2`,

```text
kt/h <= k(h−3)/h = k−3k/h < k−1,
```

where `3k/h>1` for `h>=5`. Thus the target `t+ceil(kt/h)` is at most `t+k−1`, one below the lower bound. There is no even `t` in this range when `h=3`.

For odd `t`, every hub has odd degree `t`, hence each of the `h` hubs needs at least one singleton and `s>=h`. Therefore

```text
s+c >= h+h(t−1)/(2t)
    = t+k+(h−t)(1−1/(2t))
    > t+k >= t+ceil(kt/h).
```

So `d(K_(h,t))=t+ceil(kt/h)` is impossible for every `1<=t<=h−2`, independently of any search. This does not assert that equality holds for `t>=h−1`; that is where the finite certificates or a separate construction matter. The proof works for any odd `h>=3`, prime or composite, and uses only degree parity and the `2t` cycle cap.
