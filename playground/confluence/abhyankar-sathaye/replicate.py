"""Independent replication of the computable parts of
OAI.AbhyankarSathaye.exists_noncoordinate_polynomial
(lean/ComparatorChallenges/AbhyankarSathaye.lean; solution OAI/AlgebraicGeometry/AbhyankarSathaye/*).

No CAS is installed here (no sympy), so this file carries its own sparse integer polynomial class.
Every formula below is transcribed from the Lean (Identities.lean, Reconstruction.lean,
FiberFormulas.lean, CriticalPoint.lean). Variables of R = C[h,u,v,w] are X0..X3 in that order.

Checks:
  A. exact symbolic identities in Z[h,u,v,w]: cusp, shift, ambient, Bezout certificate
  B. exact critical point: F(2,0,-1/2,1/2) = -1 and all four partials of the EXPANDED F vanish
     (independent of the Lean's route through the ambient identity)
  C. forward map phi: Z[h,u,v,w] -> Z[X,Y,T] (h,u,v,w -> freeH,freeU,freeV,freeW) kills F and is a
     left inverse of psi (X,Y,T -> shiftX, shiftY, fiberParameter): phi(F) = 0, phi(shiftX) = X,
     phi(shiftY) = Y, phi(param) = T. Too large to expand, so tested by Schwartz-Zippel at random
     points mod the prime 2^61-1 (probabilistic, error <= deg/p per point).
  D. psi o phi = id on the zero fibre: full enumeration of F_p^4 for small p: V(F)(F_p) has exactly
     p^3 points, phi : F_p^3 -> V(F)(F_p) is a bijection with inverse psi. Also prints all fibre sizes.
  E. negative controls, each must FAIL.
"""
import random
import sys
from fractions import Fraction


# ---------------------------------------------------------------- sparse polynomials over Z / Q
class Poly:
    __slots__ = ("t", "n")

    def __init__(self, terms, n):
        self.t = {e: c for e, c in terms.items() if c != 0}
        self.n = n

    @staticmethod
    def const(c, n):
        return Poly({(0,) * n: c}, n)

    @staticmethod
    def var(i, n):
        return Poly({tuple(1 if j == i else 0 for j in range(n)): 1}, n)

    def _co(self, o):
        return o if isinstance(o, Poly) else Poly.const(o, self.n)

    def __add__(self, o):
        o = self._co(o)
        r = dict(self.t)
        for e, c in o.t.items():
            r[e] = r.get(e, 0) + c
        return Poly(r, self.n)

    __radd__ = __add__

    def __neg__(self):
        return Poly({e: -c for e, c in self.t.items()}, self.n)

    def __sub__(self, o):
        return self + (-self._co(o))

    def __rsub__(self, o):
        return self._co(o) - self

    def __mul__(self, o):
        o = self._co(o)
        r = {}
        for e1, c1 in self.t.items():
            for e2, c2 in o.t.items():
                e = tuple(a + b for a, b in zip(e1, e2))
                r[e] = r.get(e, 0) + c1 * c2
        return Poly(r, self.n)

    __rmul__ = __mul__

    def __pow__(self, k):
        r = Poly.const(1, self.n)
        for _ in range(k):
            r = r * self
        return r

    def __eq__(self, o):
        return isinstance(o, Poly) and self.t == o.t

    def is_zero(self):
        return not self.t

    def deg(self):
        return max((sum(e) for e in self.t), default=-1)

    def pderiv(self, i):
        r = {}
        for e, c in self.t.items():
            if e[i]:
                f = list(e)
                f[i] -= 1
                r[tuple(f)] = r.get(tuple(f), 0) + c * e[i]
        return Poly(r, self.n)

    def eval(self, pt):
        tot = 0
        for e, c in self.t.items():
            m = c
            for a, k in zip(pt, e):
                if k:
                    m = m * a ** k
            tot = tot + m
        return tot


class ModP:
    """Element of Z/p with int coercion, so the same formulas run over Z/p."""
    __slots__ = ("v", "p")

    def __init__(self, v, p):
        self.v, self.p = v % p, p

    def _co(self, o):
        return o.v if isinstance(o, ModP) else o

    def __add__(self, o): return ModP(self.v + self._co(o), self.p)
    __radd__ = __add__
    def __sub__(self, o): return ModP(self.v - self._co(o), self.p)
    def __rsub__(self, o): return ModP(self._co(o) - self.v, self.p)
    def __mul__(self, o): return ModP(self.v * self._co(o), self.p)
    __rmul__ = __mul__
    def __neg__(self): return ModP(-self.v, self.p)
    def __pow__(self, k): return ModP(pow(self.v, k, self.p), self.p)
    def __eq__(self, o): return self.v == self._co(o) % self.p
    def __hash__(self): return hash(self.v)



# ---------------------------------------------------------------- univariate root finding mod p
def _trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def _mod(a, b, p):
    a = a[:]
    inv = pow(b[-1], p - 2, p)
    while len(a) >= len(b):
        c = a[-1] * inv % p
        sh = len(a) - len(b)
        for i, bi in enumerate(b):
            a[sh + i] = (a[sh + i] - c * bi) % p
        _trim(a)
    return a


def _mul(a, b, p):
    r = [0] * (len(a) + len(b) - 1) if a and b else []
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] = (r[i + j] + x * y) % p
    return _trim(r)


def _gcd(a, b, p):
    while b:
        a, b = b, _mod(a, b, p)
    return a


def _powmod(base, e, f, p):
    r, b = [1], _mod(base, f, p)
    while e:
        if e & 1:
            r = _mod(_mul(r, b, p), f, p)
        b = _mod(_mul(b, b, p), f, p)
        e >>= 1
    return r


def roots_mod_p(f, p, rng):
    """All roots in F_p of the univariate f (coefficient list, low degree first)."""
    f = _trim([c % p for c in f])
    if len(f) <= 1:
        return []
    xp = _powmod([0, 1], p, f, p)
    g = _gcd(f, _trim([(c - (1 if i == 1 else 0)) % p for i, c in enumerate(xp + [0] * max(0, 2 - len(xp)))]), p)
    out = []

    def split(g):
        if len(g) == 2:
            out.append((-g[0]) * pow(g[1], p - 2, p) % p)
            return
        if len(g) < 2:
            return
        while True:
            a = rng.randrange(p)
            h = _powmod([a, 1], (p - 1) // 2, g, p)
            h = _trim([(c - (1 if i == 0 else 0)) % p for i, c in enumerate(h + [0])])
            d = _gcd(g, h, p)
            if 1 < len(d) < len(g):
                split(d)
                split(_div(g, d, p))
                return

    split(g)
    return out


def _div(a, b, p):
    a = a[:]
    q = [0] * (len(a) - len(b) + 1)
    inv = pow(b[-1], p - 2, p)
    while len(a) >= len(b):
        c = a[-1] * inv % p
        sh = len(a) - len(b)
        q[sh] = c
        for i, bi in enumerate(b):
            a[sh + i] = (a[sh + i] - c * bi) % p
        _trim(a)
    return q


def interpolate(xs, ys, p):
    """Lagrange interpolation mod p -> coefficient list."""
    n = len(xs)
    res = [0] * n
    for i in range(n):
        num, den = [1], 1
        for j in range(n):
            if j != i:
                num = _mul(num, [(-xs[j]) % p, 1], p) or [0]
                den = den * (xs[i] - xs[j]) % p
        c = ys[i] * pow(den, p - 2, p) % p
        for k, a in enumerate(num):
            res[k] = (res[k] + c * a) % p
    return res

# ---------------------------------------------------------------- the Lean definitions, transcribed
def S(h, u, v, w):
    return 2*u**3*v + 3*u**4*w + h*(v**2 - 3*u**2*w**2) + h**2*w**3


def P(x, y, s):
    return -2*s**2*x + 3*s*y**2 - 3*s**3*y


def Alpha(x, s):
    return 1 + 2*s**2*x + 4*s**5


def Beta(x, y, s):
    return (3*s**3 - 3*s*y)*(1 + 2*s**2*x) - 4*s**4*y**2


def inverseU(h, x, beta, T): return h*T - beta*x
def inverseG(x, y, alpha, T): return y*T + alpha*x
def inverseW(h, y, s, alpha, beta, U, G, two=2):
    return alpha*(1 + beta*y)*(y + U**2) + beta**2*(s - h*G**2 + two*U*y*G)
def inverseV(U, G, W): return G - U*W
def parameter(alpha, beta, U, V, W): return alpha*U + beta*(V + U*W)


def derived(h, u, v, w, Sfun=S):
    """x, y, s, p, F, shiftX, shiftY, fiberParameter as in Identities.lean / FiberFormulas.lean."""
    x = u**3 + h*v
    y = -u**2 + h*w
    s = Sfun(h, u, v, w)
    p = P(x, y, s)
    F = h - p - 1
    return dict(x=x, y=y, s=s, p=p, F=F, shiftX=x + s**3, shiftY=y - s**2,
                param=parameter(Alpha(x, s), Beta(x, y, s), u, v, w))


def forward(X, Y, T, two=2):
    """freeH, freeU, freeV, freeW of FiberFormulas.lean (variables ordered X, Y, T)."""
    fS = X**2 + Y**3
    fX = X - fS**3
    fY = Y + fS**2
    fH = 1 + P(fX, fY, fS)
    fA = Alpha(fX, fS)
    fB = Beta(fX, fY, fS)
    fU = inverseU(fH, fX, fB, T)
    fG = inverseG(fX, fY, fA, T)
    fW = inverseW(fH, fY, fS, fA, fB, fU, fG, two=two)
    fV = inverseV(fU, fG, fW)
    return fH, fU, fV, fW


def ok(label, cond):
    print(("PASS " if cond else "FAIL ") + label)
    return cond


def main():
    random.seed(20261008)
    good = True
    n = 4
    h, u, v, w = (Poly.var(i, n) for i in range(n))
    d = derived(h, u, v, w)
    F = d["F"]
    print(f"F in Z[h,u,v,w]: degree {F.deg()}, {len(F.t)} terms; "
          f"max |coeff| {max(abs(c) for c in F.t.values())}")
    print(f"  degree in each variable (h,u,v,w): {[max(e[i] for e in F.t) for i in range(4)]}")

    # A. symbolic identities
    print("\n[A] exact identities in Z[h,u,v,w]")
    good &= ok("cusp     x^2 + y^3 = h*s", d["x"]**2 + d["y"]**3 - h*d["s"] == Poly({}, n))
    good &= ok("shift    shiftX^2 + shiftY^3 = x^2 + y^3 - s*p",
               d["shiftX"]**2 + d["shiftY"]**3 - (d["x"]**2 + d["y"]**3 - d["s"]*d["p"]) == Poly({}, n))
    good &= ok("ambient  shiftX^2 + shiftY^3 = s*(1+F)",
               d["shiftX"]**2 + d["shiftY"]**3 - d["s"]*(1 + F) == Poly({}, n))
    x, y, s = d["x"], d["y"], d["s"]
    lhs = Alpha(x, s)*h + Beta(x, y, s)*y - 1
    rhs = (1 + 2*s**2*x)*(h - 1 - P(x, y, s)) - 4*s**4*(x**2 + y**3 - s*h)
    good &= ok("Bezout   alpha*h + beta*y - 1 = (1+2s^2x)(h-1-P) - 4s^4(x^2+y^3-sh)", lhs == rhs)

    # B. critical point, computed on the EXPANDED polynomial
    print("\n[B] critical point (2, 0, -1/2, 1/2), exact rationals")
    cp = (Fraction(2), Fraction(0), Fraction(-1, 2), Fraction(1, 2))
    Fv = F.eval(cp)
    grads = [F.pderiv(i).eval(cp) for i in range(4)]
    print(f"  F = {Fv}; gradient = {grads}")
    good &= ok("F(cp) = -1", Fv == -1)
    good &= ok("all four partials of F vanish at cp", all(g == 0 for g in grads))
    # extension to n = 5: F does not involve the new variable, gradient at (cp, 0) is (0,...,0)
    print("  (for n > 4, F does not involve X4..; d/dX_k F = 0 identically, so the point (cp,0,...,0) stays critical)")

    # C. forward map, Schwartz-Zippel mod a large prime
    print("\n[C] forward map phi, random points mod p = 2^61 - 1")
    p = (1 << 61) - 1
    trials = 40
    allc = True
    for _ in range(trials):
        X, Y, T = (ModP(random.randrange(p), p) for _ in range(3))
        H, U, V, W = forward(X, Y, T)
        e = derived(H, U, V, W)
        allc &= e["F"] == 0 and e["shiftX"] == X and e["shiftY"] == Y and e["param"] == T
    good &= ok(f"phi(F)=0, phi(shiftX)=X, phi(shiftY)=Y, phi(param)=T at {trials} random points", allc)

    # D. small fields, full enumeration
    print("\n[D] full enumeration over F_p (p small)")
    for q in (2, 3, 5, 7, 11, 13):
        fib = [0] * q
        zero_pts = []
        for a in range(q):
            for b in range(q):
                for c in range(q):
                    for e_ in range(q):
                        Fv = int(derived(*(ModP(t, q) for t in (a, b, c, e_)))["F"].v)
                        fib[Fv] += 1
                        if Fv == 0:
                            zero_pts.append((a, b, c, e_))
        # psi o phi on every zero-fibre point, phi o psi on every point of F_q^3
        back = all(
            tuple(t.v for t in forward(*(lambda dd: (dd["shiftX"], dd["shiftY"], dd["param"]))(
                derived(*(ModP(t, q) for t in pt))))) == pt for pt in zero_pts)
        image = set()
        fwd_ok = True
        for a in range(q):
            for b in range(q):
                for c in range(q):
                    H, U, V, W = forward(ModP(a, q), ModP(b, q), ModP(c, q))
                    dd = derived(H, U, V, W)
                    fwd_ok &= dd["F"] == 0 and (dd["shiftX"].v, dd["shiftY"].v, dd["param"].v) == (a, b, c)
                    image.add((H.v, U.v, V.v, W.v))
        good &= ok(f"p={q}: #V(F)={len(zero_pts)} (= p^3 {q**3}); psi o phi = id on V(F): {back}; "
                   f"phi o psi = id on F_p^3: {fwd_ok}; phi onto V(F): {image == set(zero_pts)}",
                   len(zero_pts) == q**3 and back and fwd_ok and image == set(zero_pts))
        print(f"      fibre sizes #F^-1(c), c = 0..{q-1}: {fib}   (c = -1 is the last entry)")

    # D2. large field: random points ON V(F) (solve F(h,u,v,w)=0 for w), check psi o phi = id there.
    #     This detects any extra component of V(F) that phi misses (a factor of F other than ker phi).
    print("\n[D2] random points of V(F) over F_p, p = 2^61 - 1 (root-find in w)")
    rng = random.Random(7)
    npts, tried = 0, 0
    allb = True
    degw = max(e[3] for e in F.t)
    while npts < 60 and tried < 2000:
        tried += 1
        a, b, c = (rng.randrange(p) for _ in range(3))
        xs = list(range(1, degw + 2))
        ys = [derived(ModP(a, p), ModP(b, p), ModP(c, p), ModP(t, p))["F"].v for t in xs]
        for r in roots_mod_p(interpolate(xs, ys, p), p, rng):
            pt = tuple(ModP(t, p) for t in (a, b, c, r))
            dd = derived(*pt)
            assert dd["F"] == 0
            back = forward(dd["shiftX"], dd["shiftY"], dd["param"])
            allb &= tuple(t.v for t in back) == (a, b, c, r)
            npts += 1
    good &= ok(f"psi o phi = id at {npts} random points of V(F) (found on {tried} random (h,u,v) lines)",
               allb and npts >= 20)

    # D3. no repeated factor: grad F is nonzero at an exact integer point phi(1,0,0) of the image
    H0, U0, V0, W0 = forward(1, 0, 0)
    g0 = [F.pderiv(i).eval((H0, U0, V0, W0)) for i in range(4)]
    good &= ok(f"[D3] phi(1,0,0) = ({H0}, {U0}, {V0}, {W0}) lies on V(F) with gradient {g0} != 0 "
               "(the component phi parametrizes is not a repeated factor of F)",
               F.eval((H0, U0, V0, W0)) == 0 and any(g0))

    # E. negative controls: each MUST fail
    print("\n[E] negative controls (each line should read CONTROL-FAILED-AS-EXPECTED)")

    def S_bad(h, u, v, w):  # coefficient 2 -> 3 in front of u^3 v
        return 3*u**3*v + 3*u**4*w + h*(v**2 - 3*u**2*w**2) + h**2*w**3

    ctrl = []
    X, Y, T = (ModP(random.randrange(p), p) for _ in range(3))
    H, U, V, W = forward(X, Y, T)
    ctrl.append(("perturbed S (2u^3v -> 3u^3v): phi(F') = 0", derived(H, U, V, W, Sfun=S_bad)["F"] == 0))
    H2, U2, V2, W2 = forward(X, Y, T, two=3)
    e2 = derived(H2, U2, V2, W2)
    ctrl.append(("wrong inverse (2UyG -> 3UyG in inverseW): phi(F)=0 and phi(shiftY)=Y",
                 e2["F"] == 0 and e2["shiftY"] == Y))
    cp2 = (Fraction(2), Fraction(0), Fraction(-1, 2), Fraction(3, 2))
    g2 = [F.pderiv(i).eval(cp2) for i in range(4)]
    ctrl.append((f"moved point (2,0,-1/2,3/2): gradient {g2} all zero", all(gg == 0 for gg in g2)))
    q = 7
    cnt = sum(1 for a in range(q) for b in range(q) for c in range(q) for e_ in range(q)
              if derived(*(ModP(t, q) for t in (a, b, c, e_)), Sfun=S_bad)["F"] == 0)
    ctrl.append((f"perturbed F' over F_7: #V(F') = {cnt} equals 343", cnt == q**3))
    # the D2 instrument must be able to see an extra component: G = F * (w - h) has the extra
    # component {w = h}; psi o phi cannot return those points
    rng2 = random.Random(11)
    allg = True
    for _ in range(10):
        a, b, c = (rng2.randrange(p) for _ in range(3))
        xs = list(range(1, degw + 3))
        ys = []
        for t in xs:
            pt = (ModP(a, p), ModP(b, p), ModP(c, p), ModP(t, p))
            ys.append((derived(*pt)["F"] * (pt[3] - pt[0])).v)
        for r in roots_mod_p(interpolate(xs, ys, p), p, rng2):
            dd = derived(*(ModP(t, p) for t in (a, b, c, r)))
            back = forward(dd["shiftX"], dd["shiftY"], dd["param"])
            allg &= tuple(t.v for t in back) == (a, b, c, r)
    ctrl.append(("D2 instrument on G = F*(w-h): psi o phi = id at all its roots", allg))
    for label, held in ctrl:
        print(("CONTROL-HELD (BAD) " if held else "CONTROL-FAILED-AS-EXPECTED ") + label)
        good &= not held

    print("\nOVERALL:", "ALL CHECKS PASS, ALL CONTROLS FAIL" if good else "SOMETHING IS WRONG")
    sys.exit(0 if good else 1)


if __name__ == "__main__":
    main()
