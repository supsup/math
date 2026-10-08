"""Outward-integer verification of the 24 published tilde-B knot bounds.

Run: python3 -I playground/marlow/18_torus_baseline_intervals.py
Transcribes the source's moment and midpoint-Taylor prescription. This
checks the finite arithmetic, conditional on its analytic error bounds.
"""

from fractions import Fraction as F
from importlib.util import module_from_spec, spec_from_file_location
from math import comb
from pathlib import Path


path = Path(__file__).with_name('17_torus_gain_intervals.py')
spec = spec_from_file_location('torus_intervals', path)
module = module_from_spec(spec)
spec.loader.exec_module(module)
I, PI, SCALE = module.interval, module.PI, module.SCALE

LAMBDA, ELL = I('.98'), I('.28')
D = I(48).sqrt() / 7
A0, B0 = 1 / PI, 1 - 1 / PI
KNOTS = tuple(map(F, ('.64 .74 .84 .92 .98 1.02 1.06 1.10 1.14 1.18 '
                      '1.22 1.26 1.30 1.34 1.38 1.42 1.46 1.50 '
                      '1.54 1.58 1.62 1.70 1.90 2.25').split()))
LOWER = (1744, 1200, 735, 432, 247, 144, 57, -15, -74, -119,
         -153, -178, -196, -211, -226, -247, -275, -260, -193,
         -76, 86, 536, 2275, 6853)


def arcsin(z):
    """Twice-halved positive-coefficient series with rigorous tail."""
    beta = (1 - z ** 2).sqrt()
    half = z / (2 + 2 * beta).sqrt()
    quarter = half / (2 + 2 * (1 - half ** 2).sqrt()).sqrt()
    series = sum((I(F(comb(2 * n, n), 4 ** n * (2 * n + 1)))
                  * quarter ** (2 * n + 1) for n in range(11)), I(0))
    tail = 4 * quarter ** 23 / (1 - quarter ** 2)
    return module.Interval((4 * series).lo, (4 * series + tail).hi)


def moments(z):
    beta = (1 - z ** 2).sqrt()
    ls = [arcsin(z), 1 - beta]
    for n in range(2, 5):
        ls.append(((n - 1) * ls[n - 2] - z ** (n - 1) * beta) / n)
    js = []
    for j in range(4):
        boundary = z ** j / beta - (1 if j == 0 else 0)
        if j:
            boundary -= j * ls[j - 1]
        js.append(LAMBDA * ls[j + 1] - (1 - LAMBDA) * boundary)
    return js


def rho_taylor_coefficients(k):
    sigma = PI / 4
    root_pi = PI.sqrt()
    root = (1 + sigma * k ** 2).sqrt()
    r0 = root_pi * k * root - PI * k ** 2 / 2
    r1 = root_pi * (1 + 2 * sigma * k ** 2) / root - PI * k
    r2 = (root_pi * sigma * k * (3 + 2 * sigma * k ** 2)
          / root ** 3 - PI) / 2
    r3 = root_pi * sigma / (2 * root ** 5)
    return (r0 - k * r1 + k ** 2 * r2 - k ** 3 * r3,
            r1 - 2 * k * r2 + 3 * k ** 2 * r3,
            r2 - 3 * k * r3, r3)


def baseline(h):
    h = I(h)
    t = 2 * PI / (PI + (PI ** 2 + 4 * PI * h ** 2).sqrt())
    x = h * A0
    hb = h * B0
    if hb.hi < D.lo:
        y, curved = hb, True
    else:
        assert hb.lo > D.hi, 'ambiguous branch at published knot'
        y, curved = D, False
    jx, jy, jd = moments(x), moments(y), moments(D)
    result = LAMBDA * h / PI + ELL * t - 1
    result += PI / h ** 2 * jx[2] + (jy[1] - jx[1]) / h
    if curved:
        middle = (B0 + D / h) / 2
        coeffs = rho_taylor_coefficients(middle)
        result += sum((coeffs[j] / h ** j * (jd[j] - jy[j])
                       for j in range(4)), I(0))
    return result


def main():
    assert len(KNOTS) == len(LOWER) == 24
    slacks = []
    for h, published in zip(KNOTS, LOWER):
        result = baseline(h)
        slack_lo = F(100000 * result.lo, SCALE) - published
        slack_hi = F(100000 * result.hi, SCALE) - published
        assert F('1.10') < slack_lo <= slack_hi < F('1.95'), (
            h, float(slack_lo), float(slack_hi))
        slacks.append(slack_lo)
    print('All 24 published tilde-B knot lower bounds pass outward-integer intervals.')
    print('Published slack envelope 1.10 < 10^5 tilde-B(h)-b_h < 1.95 passes.')
    print(f'Smallest lower slack: {float(min(slacks)):.8f}.')


if __name__ == '__main__':
    main()
