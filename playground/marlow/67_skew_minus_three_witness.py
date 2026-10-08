"""Exact arithmetic certificate for one large conditional late-prefix case.

Run: python3 -I playground/marlow/67_skew_minus_three_witness.py
"""
from fractions import Fraction
from math import factorial, isqrt


def prime(n):
    return n > 1 and all(n % d for d in range(2, isqrt(n) + 1))


def prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.append(n)
    assert all(prime(q) for q in factors)
    return factors


p = 1_000_000_453
assert p % 24 == 13 and prime(p)
k = (p - 1) // 2
factors = prime_factors(k)
assert factors == [2, 3, 11, 17, 445633]
a = p - 3
assert pow(a, k, p) == 1
order_tests = {q: pow(a, k // q, p) for q in factors}
assert all(value != 1 for value in order_tests.values())

# e > 27/10, so p < (27/10)^21 < e^21 and log(p) < 21.
assert sum(Fraction(1, factorial(i)) for i in range(6)) > Fraction(27, 10)
assert 27**21 > p * 10**21
assert p < 31623**2
available = (p + 23) // 6
upper_for_required = 8 * 31623 * 23**2 + 8
assert p + 23 == 6 * available
assert available > upper_for_required

print('p=', p, 'prime=', True, 'k=', k, 'factors=', factors)
print('a=-3 order tests=', order_tests, 'a^k=', pow(a, k, p))
print('available=', available, 'strict_upper_for_required=', upper_for_required)
