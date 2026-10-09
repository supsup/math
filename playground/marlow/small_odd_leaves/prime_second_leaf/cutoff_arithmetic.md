# Exact arithmetic behind the crude absolute cutoff

This checks only the elementary inequality used in
[`asymptotic_one_cut.md`](asymptotic_one_cut.md). It does not audit the
character-sum or graph arguments there.

The primes less than `32` are

```text
2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
```

with product `P=200560490130`. For each prime `q≥37`,
`2≤q^(1/5)` since `q≥37>32=2^5`. Hence for every positive integer
`n` (extra powers of a prime only increase `n^(1/5)`),

```text
  W(n)=2^ω(n) ≤ (2^11/P^(1/5)) n^(1/5) < 12 n^(1/5).
```

The last strict inequality is equivalent to the exact integer
comparison

```text
  2^55 = 36028797018963968
       < 49905867880028160 = 12^5 · 200560490130.
```

With `n=(p−1)/2`, a sufficient condition for
`sqrt(p)≥66 W(n)` is

```text
  sqrt(p) ≥ 792 (p/2)^(1/5).
```

Raising both positive sides to the tenth power reduces this to
`4p^3≥792^10`. The left side increases with `p`, and at
`p=3,000,000,000` the exact comparison is

```text
  4 p^3 = 108000000000000000000000000000
          > 97107285881285854916272717824 = 792^10.
```

Therefore the numerical cutoff calculation is valid for all real
`p≥3,000,000,000`, and in particular for every prime in that range.
