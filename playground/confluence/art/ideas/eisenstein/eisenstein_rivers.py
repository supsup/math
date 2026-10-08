"""Hexagonal rivers: a Collatz-type map on the Eisenstein integers Z[w], w = e^(2 pi i/3), drawn as rivers.

THE ARITHMETIC. z = a + b w with w^2 = -1 - w, norm N(z) = a^2 - ab + b^2. Six units: +-1, +-w, +-w^2.
 * 2 is inert: Z[w]/(2) is the field with four elements {0, 1, w, w^2}. Each NONZERO class holds exactly
   one pair of units +-u, so a "2-odd" z can be made even by adding a unit: z -> m z + u with u = m z mod 2.
 * 1 - w (norm 3) is the ramified prime over 3: Z[w]/(1-w) = F3 = {0, +1, -1}; units are +-1 mod (1-w).

THE SYMMETRY (proved by the argument below, and checked on every start by the script).
For f(z) = m z + c(z) on the odd branch, f(uz) = u f(z) for a unit u iff c(uz) = u c(z).
 * divisor 2, c a FIXED unit per class mod 2: -1 fixes every class mod 2 but c(-z) = -c(z) is then
   impossible, so at most the rotations {1, w, w^2} survive: THREE-fold, never six (the same reason
   3n+1 on -n is 3n-1 on n).
 * divisor 1-w, c = +-1 per class mod (1-w): w fixes every class mod (1-w), so only {+1, -1} survive: TWO-fold.
 * SIX-fold needs c to see both primes. The units are a complete set of residues for the invertible
   classes mod 2(1-w) (that group has order 3 * 2 = 6), so let c(z) = (1-w)^k u, where m z = (1-w)^k y with
   1-w not dividing y, and u is the unit congruent to y mod 2(1-w). Then c(uz) = u c(z) for all six units.
   For this to be a sensible map, m must also be prime to 1-w (else the (1-w)-valuation only grows and
   every start escapes; the script's table shows it). The least such non-unit m is norm 7: m = 2 - w.

THE CHOSEN MAP: z -> z/2 if 2 | z, else (2 - w) z + c(z) with the six-fold c above. It also satisfies
f((1-w) z) = (1-w) f(z) and never changes the power of 1-w in z, so every multiple of 1-w runs as (1-w)
times a start that is prime to 1-w. The drawing therefore shows the starts PRIME TO 1-w in the
unit-symmetric hexagon max(|a|, |b|, |a-b|) <= 20; the |a|, |b| <= 20 box of the brief is NOT unit
symmetric (w * (20 - 20w) = 20 + 40w leaves it), so the table reports both boxes.

Drift: an odd step multiplies |z| by |m| = sqrt 7 = 2.646; a halving step then repeats with chance 1/4, so
on average 4/3 halvings divide |z| by 2^(4/3) = 2.520. A slight OUTWARD drift: most starts that are caught
are caught early, and the escapees (counted, not drawn) are the rule for large starts, heuristically.

Drawing: the river layout of collatz_variations.build, with the mouths placed by symmetry: the mouth
u * r sits at angle arg(u) + offset on a small circle, heading outward, so multiplying by a unit is
literally a rotation of the picture by 60 degrees. A cycle that is itself unit-invariant (the 42-cycle)
is cut at its six rotations into six arms.

Standard library only, deterministic: python3 -I eisenstein_rivers.py  ->  eisenstein_rivers.svg
"""
import math
import pathlib
import sys

ART = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ART))  # -I hides the script dir
import collatz_variations as cv  # noqa: E402

OUT = pathlib.Path(__file__).resolve().with_name("eisenstein_rivers.svg")
BG, INK, DIM, GOLD, PALETTE = cv.BG, cv.INK, cv.DIM, cv.GOLD, cv.PALETTE


class E:
    """Eisenstein integer a + b w."""
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
            return str(a).replace("-", "−")
        bw = ("" if abs(b) == 1 else str(abs(b))) + "ω"
        if a == 0:
            return ("−" if b < 0 else "") + bw
        return f"{a}{'−' if b < 0 else '+'}{bw}".replace("-", "−")

    def __mul__(self, o):
        return E(self.a * o.a - self.b * o.b, self.a * o.b + self.b * o.a - self.b * o.b)

    def __add__(self, o):
        return E(self.a + o.a, self.b + o.b)

    def __neg__(self):
        return E(-self.a, -self.b)

    def c(self):
        return complex(self.a - self.b / 2, self.b * math.sqrt(3) / 2)


def N(z):
    return z.a * z.a - z.a * z.b + z.b * z.b


ONE, W, TWO, PI = E(1, 0), E(0, 1), E(2, 0), E(1, -1)
UNITS = [E(1, 0), E(1, 1), E(0, 1), E(-1, 0), E(-1, -1), E(0, -1)]  # args 0, 60, ..., 300 degrees
ROT3 = [E(1, 0), E(0, 1), E(-1, -1)]                                  # 1, w, w^2


def div2(z):
    return E(z.a // 2, z.b // 2) if z.a % 2 == 0 and z.b % 2 == 0 else None


def divpi(z):  # z / (1 - w) = z (2 + w) / 3
    t = z * E(2, 1)
    return E(t.a // 3, t.b // 3) if t.a % 3 == 0 and t.b % 3 == 0 else None


DIV = {"2": div2, "π": divpi}


def unit_part(z, q):
    """(q^k) * u where z = q^k y, q does not divide y, and u is the unit = y mod 2(1-w)."""
    qd, qv, k = DIV[q], (TWO if q == "2" else PI), ONE
    while (y := qd(z)) is not None:
        z, k = y, k * qv
    for u in UNITS:
        d = z + (-u)
        if div2(d) is not None and divpi(d) is not None:
            return k * u
    raise ValueError(z)


def make(div, m, offset):
    """offset(mz) -> c with div | m z + c."""
    dv = DIV[div]

    def f(z):
        y = dv(z)
        if y is not None:
            return y, True
        r = m * z + offset(m * z)
        assert dv(r) is not None, (str(z), str(r))
        return r, False
    return f


def rep2(sign):  # the unit sign*u, u in {1, w, w^2}, with t + u = 0 mod 2
    return lambda t: next(u for u in ROT3 if div2(t + u) is not None) * E(sign, 0)


def reppi(scale):  # scale * r, r = +-1 with t + r = 0 mod (1-w)
    return lambda t: next(r for r in (ONE, -ONE) if divpi(t + r) is not None) * scale


def six2(sign):  # divisor 2: c = sign * (1-w)^k u
    return lambda t: unit_part(t, "π") * E(sign, 0)


def sixpi(t):  # divisor 1-w: c = -(2^k u), the sign that makes 1-w divide t + c
    return -unit_part(t, "2")


M7, M3, M3b = E(2, -1), E(3, 0), E(1, 2)
EXPLORE = [  # (name, divisor, map); the chosen one first
    ("2: (2−ω)z + c₆   [chosen]", make("2", M7, six2(1))),
    ("2: (2−ω)z − c₆", make("2", M7, six2(-1))),
    ("2: (2−ω)z + u", make("2", M7, rep2(1))),
    ("2: (2−ω)z − u", make("2", M7, rep2(-1))),
    ("2: 3z + u", make("2", M3, rep2(1))),
    ("2: 3z + c₆", make("2", M3, six2(1))),
    ("2: (1−ω)z + u", make("2", PI, rep2(1))),
    ("2: (1−ω)z + c₆", make("2", PI, six2(1))),
    ("2: (1+2ω)z + u", make("2", M3b, rep2(1))),
    ("2: z + c₆", make("2", ONE, six2(1))),
    ("2: ωz + c₆", make("2", W, six2(1))),
    ("2: −ωz + c₆", make("2", E(0, -1), six2(1))),
    ("1−ω: 2z + r", make("π", TWO, reppi(ONE))),
    ("1−ω: 2z + ωr", make("π", TWO, reppi(W))),
    ("1−ω: −2z + r", make("π", -TWO, reppi(ONE))),
    ("1−ω: 2ωz + r", make("π", E(0, 2), reppi(ONE))),
    ("1−ω: (2−ω)z + r", make("π", M7, reppi(ONE))),
    ("1−ω: 2z + c₆", make("π", TWO, sixpi)),
]
SQUARE = [E(a, b) for a in range(-20, 21) for b in range(-20, 21) if (a, b) != (0, 0)]
HEX = [z for z in SQUARE if abs(z.a - z.b) <= 20]


def cycle_of(f, r):
    c, n = [r], f(r)[0]
    while n != r:
        c.append(n)
        n = f(n)[0]
    return c


def survey(f, starts):
    parent, _, _, roots, esc = cv.build(f, starts, N)
    unit_cycles = [r for r in roots if any(N(v) == 1 for v in cycle_of(f, r))]
    to_root = {}
    for s in starts:
        if s in parent:
            v = s
            while parent[v] is not None:
                v = parent[v]
            to_root[s] = v
    to_unit = sum(1 for s in to_root.values() if s in unit_cycles)
    to_zero = sum(1 for s in to_root.values() if s == E(0, 0))
    return len(roots), len(to_root), to_unit, to_zero, esc, sorted(len(cycle_of(f, r)) for r in roots)


def symmetry(f, starts):
    return [u for u in UNITS if all(f(u * z)[0] == u * f(z)[0] for z in starts)]


def table():
    rows = []
    print("| map (divisor: odd step) | units u with f(uz)=u f(z) | box | cycles | caught | to a unit cycle | to 0 | escaped | cycle lengths |")
    print("|---|---|---|---|---|---|---|---|---|")
    for name, f in EXPLORE:
        sym = len(symmetry(f, SQUARE))
        for box, st in (("square", SQUARE), ("hexagon", HEX)):
            k, caught, unit, zero, esc, lens = survey(f, st)
            short = ",".join(f"{L}" for L in sorted(set(lens)))
            print(f"| {name} | {sym} | {box} {len(st)} | {k} | {caught} | {unit} | {zero} | {esc} | {short} |")
            rows.append((name, box, k, caught, esc))
    return rows


def draw(f, even=0.13, odd=0.27, ring=26.0):
    starts = [z for z in HEX if divpi(z) is None]
    parent, divided, flow, roots, escaped = cv.build(f, starts, N)
    # checks the picture relies on
    assert len(symmetry(f, HEX)) == 6
    assert all(f(PI * z)[0] == PI * f(z)[0] for z in HEX)
    assert all((divpi(f(z)[0]) is None) == (divpi(z) is None) for z in HEX)
    assert set(starts) == {u * z for u in UNITS for z in starts}
    # group cycles into unit orbits; pick one representative per orbit and its six rotations as mouths
    cyc = {r: cycle_of(f, r) for r in roots}
    orbits, seen = [], set()
    for r in sorted(roots, key=lambda q: (N(q), str(q))):
        if r in seen:
            continue
        members = [q for q in roots if any(u * r in cyc[q] for u in UNITS)]
        seen |= set(members)
        orbits.append((r, members))
    mouths = []  # (value, angle, orbit index)
    for oi, (r, members) in enumerate(orbits):
        off = math.radians(30) * oi
        for u in UNITS:
            ang = math.atan2((u.c()).imag, (u.c()).real) + off
            mouths.append((u * r, ang, oi))
    for v, _, _ in mouths:
        parent[v] = None
    children = {v: [] for v in parent}
    for v, p in parent.items():
        if p is not None:
            children[p].append(v)
    pos, head = {}, {}
    for r, a, _ in mouths:
        pos[r] = (ring * math.cos(a), ring * math.sin(a))
        head[r] = a
        stack = [r]
        while stack:
            p = stack.pop()
            for c in children[p]:
                if c in pos:
                    continue
                h = head[p] + (even if divided[c] else -odd)
                pos[c] = (pos[p][0] + math.cos(h), pos[p][1] + math.sin(h))
                head[c] = h
                stack.append(c)
    assert len(pos) == len(parent)
    xs = [q[0] for q in pos.values()]
    ys = [q[1] for q in pos.values()]
    span = max(max(abs(x) for x in xs), max(abs(y) for y in ys))  # centred, so rotations stay rotations
    W_, H_, cx, cy_, rad = 480, 600, 240, 252, 190
    sc = rad / span

    def P(v):  # y up, so that multiplying by w turns the picture counter-clockwise
        x, y = pos[v]
        return cx + x * sc, cy_ - y * sc

    basin = {}
    for r, _, oi in mouths:
        stack = [r]
        while stack:
            p = stack.pop()
            basin[p] = oi
            stack.extend(children[p])
    top = math.log(max(flow.values()))
    groups = {}
    for v, p in parent.items():
        if p is None:
            continue
        t = math.log(max(flow[v], 1)) / top
        groups.setdefault((basin[v], min(13, int(t * 14))), []).append(v)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_}" height="{H_}" viewBox="0 0 {W_} {H_}">',
           f'<rect width="{W_}" height="{H_}" fill="{BG}"/>',
           f'<text x="240" y="34" text-anchor="middle" font-family="serif" font-size="21" fill="{INK}">'
           'Hexagonal rivers</text>',
           f'<text x="240" y="52" text-anchor="middle" font-family="serif" font-style="italic" font-size="12" '
           f'fill="{DIM}">a Collatz map on the Eisenstein integers ℤ[ω]</text>']
    cols = [GOLD, PALETTE[1], PALETTE[2], PALETTE[3], PALETTE[4]]
    for (b, lvl), vs in sorted(groups.items(), key=lambda kv: kv[0][1]):
        t = (lvl + 0.5) / 14
        colour = cols[b % len(cols)] if t > 0.5 else f"rgb({int(110 + 134 * t)},{int(196 + 17 * t)},{int(226 - 85 * t)})"
        d = "".join("M%.1f %.1fL%.1f %.1f" % (*P(v), *P(parent[v])) for v in vs)
        out.append(f'<path d="{d}" fill="none" stroke="{colour}" stroke-opacity="{0.3 + 0.7 * t:.2f}" '
                   f'stroke-width="{0.35 + 4.0 * t ** 1.7:.2f}" stroke-linecap="round"/>')
    for v, a, oi in mouths:
        x, y = P(v)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{cols[oi % len(cols)]}"/>')
    # mouth labels, pushed INWARD (the rivers run outward)
    for v, a, oi in mouths:
        x, y = P(v)
        k = 13 if oi == 0 else 30
        lx, ly = x - k * math.cos(a), y + k * math.sin(a) + 3.5
        out.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-family="serif" font-style="italic" '
                   f'font-size="9" fill="{cols[oi % len(cols)]}">{v}</text>')
    # caption: everything below comes from the computation above
    n_all = len(starts)
    caught = sum(1 for s in starts if s in parent)
    per_orbit = []
    for oi, (r, members) in enumerate(orbits):
        n_in = sum(1 for s in starts if s in parent and basin.get(s) == oi)
        per_orbit.append((oi, r, len(members), len(cyc[r]), n_in))
    two = next(o for o in per_orbit if any(N(v) == 1 for v in cyc[o[1]]))
    one_partner = f(ONE)[0]
    to_one = sum(1 for s in starts if s in parent and _root(parent, s) == ONE)
    long_ = [o for o in per_orbit if o is not two]
    k_sq, c_sq, _, _, e_sq, _ = survey(f, SQUARE)
    k_hx, c_hx, _, _, e_hx, _ = survey(f, HEX)
    lines = [
        ("z ↦ z/2 if 2 | z,  else (2−ω)z + c(z)", INK, 12.5),
        ("c(z) = the unit ≡ (2−ω)z mod 2(1−ω), times the power of 1−ω in (2−ω)z", DIM, 10.5),
        (f"{caught:,} of {n_all:,} starts prime to 1−ω, |a|,|b|,|a−b| ≤ 20, reach a cycle; {to_one} reach 1", INK, 11),
        (f"{escaped:,} pass {cv.CAP_VALUE:.0e} or {cv.CAP_STEPS} steps first: not drawn", "#ffb3a7", 10.5),
    ]
    for oi, r, nm, L, n_in in per_orbit:
        if oi == two[0]:
            lines.append((f"gold: {nm} two-cycles 1 ↔ {one_partner} and its rotations, {n_in:,} starts", GOLD, 10.5))
        else:
            j, eps = next((j, u) for j in range(1, L + 1) for u in UNITS[1:] if f_pow(f, r, j) == u * r)
            lines.append((f"rose: one {L}-cycle through {r}; every {j} steps it turns z into {eps}·z; {n_in:,} starts",
                          cols[oi % len(cols)], 10.5))
    lines += [
        ("f(uz) = u·f(z) for all six units u: turning the picture 60° is multiplying by a unit", DIM, 10.5),
        (f"all {len(HEX):,} hexagon starts, multiples of 1−ω too: {k_hx} cycles, {c_hx:,} caught, {e_hx:,} escaped", DIM, 10),
        (f"f((1−ω)z) = (1−ω)f(z), so those are copies of these  ·  turn +{even} dividing, −{odd} multiplying", DIM, 10),
    ]
    y = 463
    for text, colour, size in lines:
        out.append(f'<text x="240" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" '
                   f'fill="{colour}">{text}</text>')
        y += 13.2 if size < 11 else 14.5
    out.append(f'<text x="240" y="592" text-anchor="middle" font-family="sans-serif" font-size="9" fill="{DIM}">'
               'ideas after Confluence at 1 · Confluence</text>')
    out.append("</svg>")
    OUT.write_text("".join(out), encoding="utf-8")
    return dict(starts=n_all, caught=caught, escaped=escaped, to_one=to_one, orbits=per_orbit,
                values=len(parent), square=(k_sq, c_sq, e_sq), hexagon=(k_hx, c_hx, e_hx), size=OUT.stat().st_size)


def _root(parent, v):
    while parent[v] is not None:
        v = parent[v]
    return v


def main():
    table()
    f = EXPLORE[0][1]
    r = cycle_of(f, E(-1, -4))
    print("42-cycle check: f^7(-1-4w) =", f_pow(f, E(-1, -4), 7), " length", len(r))
    print(draw(f))


def f_pow(f, z, k):
    for _ in range(k):
        z = f(z)[0]
    return z


if __name__ == "__main__":
    main()
