"""Direct overlap-set crosscheck of the item 70 floor-sum census."""

from math import gcd

noncanonical = []
divisible_by_three = []
units = 0
for n in range(5, 502, 2):
    k = n // 2
    lower = (k + 2) // 3
    for a in range(2, n - 1):
        if gcd(a, n) != 1:
            continue
        units += 1
        overlap = sum((a * x) % n <= k for x in range(1, k + 1))
        assert overlap >= lower, (n, a, overlap)
        if overlap != lower:
            continue
        if n % 3 == 0:
            divisible_by_three.append((n, a))
        elif a not in (n - 3, pow(n - 3, -1, n)):
            noncanonical.append((n, a))

assert units == 50_532
assert noncanonical == [(11, 2), (11, 6), (17, 10), (17, 12)]
assert divisible_by_three == [
    (9, 2), (9, 4), (9, 5), (9, 7),
    (15, 2), (15, 4), (15, 8),
    (21, 4), (21, 16),
    (27, 16), (27, 22),
]
print("PASS direct equality crosscheck to n=501, units=50532")
