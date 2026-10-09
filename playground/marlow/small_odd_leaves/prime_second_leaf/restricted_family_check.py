"""Finite controls for the asymptotic one-cut specialization.

Scans every prime 17..401 for a witness in b=ac/(c+a-1), and invokes the
existing independent full-edge checker on primes through 101.
"""

import importlib.util
from pathlib import Path


SIBLING = Path(__file__).with_name("multiplicative_splice_finite_check.py")
spec = importlib.util.spec_from_file_location("second_leaf_checker", SIBLING)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


def special_case(p):
    n = (p - 1) // 2
    for a in range(2, p):
        if bridge.chi(a, p) != 1 or bridge.order(a, p) != n:
            continue
        for c in range(1, p):
            R = (c + a - 1) % p
            if not R or bridge.chi(c, p) != -1:
                continue
            if bridge.chi(R, p) != 1:
                continue
            if bridge.chi(1 - c, p) != -bridge.chi(-1, p):
                continue
            b = a * c * pow(R, -1, p) % p
            L = (c + b - 1) % p
            if bridge.chi(L, p) != -1:
                continue
            if bridge.order(L * pow(c, -1, p) % p, p) != n:
                continue
            assert L == (c*c + 2*(a-1)*c - (a-1)) * pow(R, -1, p) % p
            return {"p": p, "a": a, "b": b, "c": c,
                    "U": R, "V": L, "R": R, "L": L,
                    "tau": a, "M": c}
    return None


if __name__ == "__main__":
    checked = 0
    full_replays = 0
    for p in bridge.primes(17, 401):
        case = special_case(p)
        assert case is not None, p
        checked += 1
        if p <= 101:
            bridge.check_case(case)
            full_replays += 1
    assert special_case(5) is None
    assert special_case(13) is None
    print(f"RESTRICTED_FAMILY_PASS primes={checked} exact_edges={full_replays} "
          "range=17..401 exceptions=5,13")
