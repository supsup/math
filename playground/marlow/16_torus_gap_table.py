"""Exact rational recheck of the final gap table in family 354.

Run: python3 -I playground/marlow/16_torus_gap_table.py
This takes the paper's *earlier knot bounds* as inputs; items 17 and 18
verify those separately. It does not verify the geometric reduction or
the second-derivative bounds used in interpolation.
"""

from fractions import Fraction as F


KNOT_WORDS = ('.64 .74 .84 .92 .98 1.02 1.06 1.10 1.14 1.18 1.22 1.26 '
              '1.30 1.34 1.38 1.42 1.46 1.50 1.54 1.58 1.62 1.70 1.90 2.25')
KNOTS = tuple(map(F, KNOT_WORDS.split()))
B_LOWER = (1744, 1200, 735, 432, 247, 144, 57, -15, -74, -119,
           -153, -178, -196, -211, -226, -247, -275, -260, -193,
           -76, 86, 536, 2275, 6853)
S_LOWER = ((None,) * 5 +
           (76, 98, 123, 151, 182, 215, 247, 271, 297, 325, 332,
            332, 318, 293, 271, 251) + (None,) * 3)
GAP_LOWER = (4416, 2298, 1859, 1313, 967, 1037, 581, 280, 145,
             137, 137, 209, 269, 379, 369, 90, 90, 100, 520,
             1470, 250, 1899, 14266)


def arctan_partial(n, z):
    return sum(((-1) ** j * z ** (2 * j + 1) / (2 * j + 1)
                for j in range(n + 1)), F(0))


def arctan_tail(n, z):
    return z ** (2 * n + 3) / (2 * n + 3)


def check_pi_interval():
    x, y = F(1, 5), F(1, 239)
    lower = 16 * arctan_partial(31, x) - 4 * (
        arctan_partial(9, y) + arctan_tail(9, y))
    upper = 16 * (arctan_partial(31, x) + arctan_tail(31, x)) - 4 * (
        arctan_partial(9, y))
    published_lower = F('3.14159265358979')
    published_upper = F('3.14159265358980')
    assert published_lower < lower < upper < published_upper
    return published_lower


def check_taylor_error():
    """Check the paper's rational inequalities behind E(h) >= Taylor error.

    The differentiation identity is elementary:
    |rho''''(k)| = 15 sqrt(pi) (pi/4)^2 k/(1+(pi/4)k^2)^(7/2).
    Its derivative has the sign of 1-6(pi/4)k^2.
    """
    pi_lower = F('3.14159265358979')
    pi_upper = F('3.14159265358980')
    b_lower = 1 - 1 / pi_lower
    b_upper = 1 - 1 / pi_upper
    assert F('.68') < b_lower < b_upper < F('.69')
    assert 6 * F('3.14') / 4 * F('.68') ** 2 > 1

    # Square positive sides of the published |rho''''(b0)| < 4 bound.
    numerator = (15 * F(11, 14) ** 2 * F('.69')) ** 2 * F(22, 7)
    denominator = (1 + (F('3.14') / 4) * F('.68') ** 2) ** 7
    assert numerator < 16 * denominator

    # Midpoint cubic Taylor remainder, weighted by int_0^D W = .72.
    coefficient = F(4) * F(1, 2) ** 4 / 24 * F('.72')
    assert coefficient == F('.0075') < F('.008')
    assert 49 * F('.989743318611') ** 2 > 48


def check_gap_table(pi_lower):
    assert len(KNOTS) == len(B_LOWER) == len(S_LOWER) == 24
    assert len(GAP_LOWER) == 23
    d_upper = F('.989743318611')
    b_lower = 1 - 1 / pi_lower

    def error(h):
        return F('.008') * max(d_upper / h - b_lower, 0) ** 4

    smallest = None
    for i, (a, b) in enumerate(zip(KNOTS, KNOTS[1:])):
        interior = F('1.02') <= a and b <= F('1.62')
        chi = int(interior)
        curvature = F('2.4') if interior else 2 / a ** 2
        left = F(B_LOWER[i] + chi * (S_LOWER[i] or 0), 100000) - error(a)
        right = F(B_LOWER[i + 1] + chi * (S_LOWER[i + 1] or 0), 100000) - error(b)
        bound = min(left, right) - curvature * (b - a) ** 2 / 8
        assert 1000000 * bound >= GAP_LOWER[i], (a, b)
        smallest = bound if smallest is None else min(smallest, bound)
    assert smallest == F(9, 100000)
    return smallest


def main():
    pi_lower = check_pi_interval()
    check_taylor_error()
    smallest = check_gap_table(pi_lower)
    print('Published rational π enclosure passes Machin-series check.')
    print('Published Taylor-error rational inequalities pass.')
    print('All 23 final gap-table bounds pass exact rational comparison.')
    print(f'Smallest conditional margin: {smallest} = {float(smallest):.8f}.')


if __name__ == '__main__':
    main()
