"""Variations on Confluence at 1, beyond the integers: Gaussian integers, a + b*sqrt(2), and the smooth
complex Collatz map.

1. Gaussian integers a + bi. "Even" means divisible by 1 + i, i.e. a + b even. Every other z leaves
   remainder 1 mod (1 + i), so z -> m*z + 1 is even whenever m is odd. A non-unit odd m has norm >= 5
   while each halving step only halves the norm, so the typical drift is OUTWARD and most starts run
   off; m = 2 - i catches the most nearby starts of the multipliers tried.
2. a + b*sqrt(2). "Even" means divisible by sqrt(2), i.e. a even, and (a + b sqrt2)/sqrt2 = b + (a/2) sqrt2.
   With the UNIT m = sqrt(2) - 1 the odd step does not grow the norm. On |a| <= 60, |b| <= 30 it catches
   3,226 of 7,380 starts (43.7%) in five cycles, against 246 (3.3%) for m = 3: better, not most.
3. The smooth map f(z) = (2 + 7z - (2 + 5z) cos(pi z)) / 4 agrees with n/2 on even n and (3n+1)/2 on odd
   n, but is defined on all of C. Colouring each point by how many steps it takes to escape gives the
   complex Collatz fractal (Chamberland; Letherman, Schleicher and Wood). Written as a PNG with zlib.

Standard library only: python3 -I complex_variations.py
"""
import cmath
import math
import pathlib
import struct
import sys
import zlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))  # -I hides the script dir
import collatz_variations as cv  # noqa: E402


class G:
    """Gaussian integer a + bi."""
    __slots__ = ("a", "b")

    def __init__(self, a, b):
        self.a, self.b = a, b

    def __eq__(self, o):
        return (self.a, self.b) == (o.a, o.b)

    def __hash__(self):
        return hash((self.a, self.b))

    def __str__(self):
        a, b = self.a, self.b
        if b == 0:
            return str(a)
        bi = ("" if abs(b) == 1 else str(abs(b))) + "i"
        if a == 0:
            return ("-" if b < 0 else "") + bi
        return f"{a}{'-' if b < 0 else '+'}{bi}"


def g_norm(z):
    return z.a * z.a + z.b * z.b


def gauss_map(m):
    ma, mb = m

    def f(z):
        if (z.a + z.b) % 2 == 0:
            return G((z.a + z.b) // 2, (z.b - z.a) // 2), True
        return G(ma * z.a - mb * z.b + 1, ma * z.b + mb * z.a), False
    return f


class R2:
    """a + b*sqrt(2)."""
    __slots__ = ("a", "b")

    def __init__(self, a, b):
        self.a, self.b = a, b

    def __eq__(self, o):
        return (self.a, self.b) == (o.a, o.b)

    def __hash__(self):
        return hash((self.a, self.b))

    def __str__(self):
        a, b = self.a, self.b
        if b == 0:
            return str(a)
        s = ("" if abs(b) == 1 else str(abs(b))) + "√2"
        if a == 0:
            return ("-" if b < 0 else "") + s
        return f"{a}{'-' if b < 0 else '+'}{s}"


def r2_size(z):
    # the larger of |z| and |its conjugate|: both embeddings must stay bounded
    r = math.sqrt(2)
    return max(abs(z.a + z.b * r), abs(z.a - z.b * r))


def r2_map(m):
    ma, mb = m

    def f(z):
        if z.a % 2 == 0:
            return R2(z.b, z.a // 2), True
        return R2(ma * z.a + 2 * mb * z.b + 1, ma * z.b + mb * z.a), False
    return f


def png(path, w, h, rows):
    raw = b"".join(b"\x00" + bytes(r) for r in rows)

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def smooth_fractal(path, w=1200, h=420, x0=-0.4, x1=5.6, y_half=1.05, max_it=60):
    """Escape-time picture. Almost every point escapes within 2-3 steps (cos(pi z) grows like
    e^(pi |Im z|)), so a raw step count is nearly flat; colour by a SMOOTH count instead:
    steps plus how far past the escape radius the last step landed, on a log-log scale."""
    def f(z):
        return (2 + 7 * z - (2 + 5 * z) * cmath.cos(math.pi * z)) / 4
    R = 30.0
    rows = []
    escaped = 0
    for j in range(h):
        y = y_half - 2 * y_half * j / (h - 1)
        row = []
        for i in range(w):
            z = complex(x0 + (x1 - x0) * i / (w - 1), y)
            n, big = 0, None
            try:
                while n < max_it:
                    z = f(z)
                    n += 1
                    if abs(z.imag) > R or abs(z) > 1e10:
                        big = abs(z.imag) if abs(z.imag) > R else abs(z)
                        break
            except OverflowError:
                big = 1e300
            if big is None:
                row += [9, 20, 33]                            # never escaped: the dark sea
                continue
            escaped += 1
            nu = n - math.log(max(math.log(big) / math.log(R), 1.0)) / math.log(math.pi)
            t = max(0.0, min(1.0, 1.0 - (nu / 6.0)))          # slow escapers (near the sea) are bright
            ph = 2 * math.pi * nu / 3.0
            band = 0.82 + 0.18 * math.cos(ph)
            r_ = int(255 * band * (0.10 + 0.86 * t ** 0.9))
            g_ = int(255 * band * (0.18 + 0.66 * t ** 1.2))
            b_ = int(255 * band * (0.30 + 0.30 * t ** 2.2))
            row += [min(255, r_), min(255, g_), min(255, b_)]
        rows.append(row)
    png(path, w, h, rows)
    return escaped, w * h


def main():
    out = cv.OUT
    out.mkdir(exist_ok=True)
    gstarts = [G(a, b) for a in range(-30, 31) for b in range(-30, 31) if (a, b) != (0, 0)]
    rstarts = [R2(a, b) for a in range(-60, 61) for b in range(-30, 31) if (a, b) != (0, 0)]
    rows = [
        cv.draw("i_gaussian", "Gaussian integers: z -> (2-i)z + 1", gauss_map((2, -1)), gstarts, 0.13, 0.27,
                ["'even' = divisible by 1+i; starts with |a|, |b| <= 30",
                 "the odd step multiplies the norm by 5: most rivers run off"], g_norm, str),
        cv.draw("j_sqrt2", "a + b√2: z -> (√2-1)z + 1", r2_map((-1, 1)), rstarts, 0.13, 0.27,
                ["'even' = divisible by √2; |a| <= 60, |b| <= 30",
                 "a unit multiplier: 44% find a sea here, against 3% for z -> 3z + 1"], r2_size, str),
    ]
    for r in rows:
        print(*r)
    esc, tot = smooth_fractal(out / "k_complex_fractal.png")
    print("k_complex_fractal.png escaped", esc, "of", tot)
    cards = "".join(f'<img src="{q.name}" alt="{q.stem}">' for q in sorted(out.glob("*.svg")))
    (out / "index.html").write_text(
        "<!doctype html><meta charset=utf-8><title>Confluence variations</title>"
        "<style>body{margin:0;background:#06101a}.g{display:grid;grid-template-columns:repeat(5,240px)}"
        ".g img{width:240px;height:300px;display:block}.f{display:block;width:1200px}</style>"
        f'<div class="g">{cards}</div><img class="f" src="k_complex_fractal.png" alt="complex Collatz fractal">',
        encoding="utf-8")


if __name__ == "__main__":
    main()
