"""Independent literal-set crosscheck of the item 69 C++ criterion scan."""

from math import isqrt

LIMIT = 10_000
MASK = (1 << 64) - 1


def prime(p):
    return p >= 2 and all(p % q for q in range(2, isqrt(p) + 1))


def factors(n):
    out = []
    q = 2
    while q * q <= n:
        if n % q == 0:
            out.append(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        out.append(n)
    return out


count = total = max_examined = 0
max_examined_p = 0
digest = 1469598103934665603
for p in range(13, LIMIT + 1, 8):
    if not prime(p):
        continue
    count += 1
    divisors = factors(p - 1)
    g = next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in divisors))
    a = g * g % p
    inv_d = pow(a + 1, -1, p)
    delta = (1 - a) * inv_d % p
    c = (p - 5) // 2
    excluded = {
        (a - q) * inv_d % p for q in range(c + 1)
    } | {
        a * (1 - q) * inv_d % p for q in range(c + 1)
    }
    for w in range(p):
        if w in excluded:
            continue
        f1 = w * (w + delta) % p
        f2 = (w - 1) * (w + delta - 1) % p
        if pow(f1, (p - 1) // 2, p) == p - 1 and pow(f2, (p - 1) // 2, p) == p - 1:
            break
    else:
        raise AssertionError(f"no witness at p={p}")
    examined = w + 1
    total += examined
    if examined > max_examined:
        max_examined, max_examined_p = examined, p
    digest ^= (p << 32) | w
    digest = digest * 1099511628211 & MASK

observed = (count, max_examined, max_examined_p, total, digest)
expected = (313, 65, 6301, 3487, 5327093834099845491)
assert observed == expected, (observed, expected)
print("PASS direct-set crosscheck limit=10000", observed)
