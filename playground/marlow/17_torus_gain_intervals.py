"""Outward-integer verification of the 16 published S(h) knot bounds.

Run: python3 -I playground/marlow/17_torus_gain_intervals.py
Uses the independently verified rational pi enclosure from item 16.
This checks the explicit algebraic S formula, not its geometric derivation.
"""

from fractions import Fraction as F
from math import isqrt


SCALE = 10 ** 40


def ceil_div(a, b):
    return -((-a) // b)


class Interval:
    def __init__(self, lo, hi):
        assert lo <= hi
        self.lo, self.hi = lo, hi

    @classmethod
    def rational(cls, value):
        q = F(value)
        lo = q.numerator * SCALE // q.denominator
        hi = ceil_div(q.numerator * SCALE, q.denominator)
        return cls(lo, hi)

    def __add__(self, other):
        other = interval(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -interval(other)

    def __rsub__(self, other):
        return interval(other) - self

    def __mul__(self, other):
        other = interval(other)
        products = (self.lo * other.lo, self.lo * other.hi,
                    self.hi * other.lo, self.hi * other.hi)
        return Interval(min(products) // SCALE,
                        ceil_div(max(products), SCALE))

    __rmul__ = __mul__

    def reciprocal(self):
        assert self.lo > 0
        return Interval(SCALE * SCALE // self.hi,
                        ceil_div(SCALE * SCALE, self.lo))

    def __truediv__(self, other):
        return self * interval(other).reciprocal()

    def __rtruediv__(self, other):
        return interval(other) / self

    def __pow__(self, n):
        assert n >= 0 and isinstance(n, int)
        if n == 0:
            return interval(1)
        if n == 1:
            return self
        return self * (self ** (n - 1))

    def sqrt(self):
        assert self.lo >= 0
        lo = isqrt(self.lo * SCALE)
        hi = isqrt(self.hi * SCALE)
        if hi * hi < self.hi * SCALE:
            hi += 1
        return Interval(lo, hi)

    def minimum(self, other):
        other = interval(other)
        return Interval(min(self.lo, other.lo), min(self.hi, other.hi))


def interval(value):
    return value if isinstance(value, Interval) else Interval.rational(value)


PI = Interval(interval('3.14159265358979').lo,
              interval('3.14159265358980').hi)
ELL, DM = interval('.28'), interval('.21')
KNOTS = tuple(map(F, ('1.02 1.06 1.10 1.14 1.18 1.22 1.26 1.30 '
                      '1.34 1.38 1.42 1.46 1.50 1.54 1.58 1.62').split()))
LOWER = (76, 98, 123, 151, 182, 215, 247, 271,
         297, 325, 332, 332, 318, 293, 271, 251)


def gain(h):
    h = interval(h)
    t = 2 * PI / (PI + (PI ** 2 + 4 * PI * h ** 2).sqrt())
    u = (1 - 1 / PI).minimum(interval('.96') / h)
    p = u - 1 + 2 * h * t / PI
    q = 2 / PI * (PI + 2 * h ** 2 * t).sqrt()
    c0 = (interval('.134') * h ** 3).minimum('.36')
    assert p.lo > 0 and q.lo > 0
    critical = 2 * p / (1 + (1 + 6 * c0 * q ** 2 * p / ELL).sqrt())
    assert (p - critical).lo > 0
    uncapped = ELL * ((p - critical) / q) ** 2 + c0 * critical ** 3
    capped = c0 * DM ** 3
    return uncapped.minimum(capped)


def main():
    assert len(KNOTS) == len(LOWER) == 16
    slacks = []
    for h, published in zip(KNOTS, LOWER):
        result = gain(h)
        slack_lo = F(100000 * result.lo, SCALE) - published
        slack_hi = F(100000 * result.hi, SCALE) - published
        assert 1 < slack_lo <= slack_hi < F('1.66'), (h, slack_lo, slack_hi)
        slacks.append(slack_lo)
    print('All 16 published S(h) knot lower bounds pass outward-integer intervals.')
    print('Published slack envelope 1 < 10^5 S(h)-s_h < 1.66 passes.')
    print(f'Smallest lower slack: {float(min(slacks)):.8f}.')


if __name__ == '__main__':
    main()
