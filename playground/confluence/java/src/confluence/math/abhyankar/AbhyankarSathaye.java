package confluence.math.abhyankar;

import java.math.BigInteger;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

/// Java replication of the computable parts of
/// OAI.AbhyankarSathaye.exists_noncoordinate_polynomial
/// (lean/ComparatorChallenges/AbhyankarSathaye.lean; solution under
/// lean/OAI/AlgebraicGeometry/AbhyankarSathaye/).
///
/// The theorem: for every n >= 4 there is F in C[X_0..X_{n-1}] whose quotient ring C[X]/(F) is
/// isomorphic, as a C-algebra, to a polynomial ring in n-1 variables (the hypersurface F = 0 "is"
/// affine (n-1)-space), but no C-algebra automorphism of C[X] sends a variable to F (F is not a
/// coordinate). Over C this is the negation of the Abhyankar-Sathaye embedding conjecture for
/// hypersurfaces in dimension n >= 4.
///
/// The explicit F lives in Z[h,u,v,w] (degree 17, 69 terms); for n > 4 it is the same polynomial in
/// the first four variables. Everything here is transcribed from the Lean files Identities.lean,
/// Reconstruction.lean, FiberFormulas.lean and CriticalPoint.lean. All formulas are written once,
/// against a tiny `Ring` interface, and run over three rings: exact integer polynomials, exact
/// rationals, and Z/p.
///
/// Checks: (A) the ambient identity shiftX^2 + shiftY^3 = s(1+F) symbolically; (B) F = -1 and all
/// four partials vanish at (2, 0, -1/2, 1/2), exactly; (C) the forward map phi (h,u,v,w -> freeH..
/// freeW) kills F and inverts psi (X,Y,T -> shiftX, shiftY, parameter) at random points mod
/// 2^61-1; (D) over F_7 and F_11, F = 0 has exactly p^3 points and phi is a bijection onto them with
/// inverse psi. Negative controls: a perturbed F, a wrong inverse and a moved critical point must fail.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.abhyankar.AbhyankarSathaye
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Certificate checking instead of trusting a CAS.** The proof is a handful of explicit
///   polynomial maps plus identities between them. A Java system that receives such data (from a
///   solver, a symbolic package, or a model) can check it with code this small: compose, reduce,
///   compare. That is a pattern for any "trust the certificate, not the producer" pipeline.
/// - **One formula, many rings.** Writing the formulas once against a `Ring<E>` interface and running
///   them over exact polynomials, exact rationals and Z/p is a cheap way to get symbolic checks,
///   exact point checks and fast probabilistic (Schwartz-Zippel) checks from the same source,
///   so the three cannot drift apart.
/// - **Randomized identity testing as a unit test.** Expanding phi(F) symbolically is far too large
///   (degrees in the thousands), but evaluating it at random points mod a 61-bit prime is
///   milliseconds. A Java test suite for a polynomial or expression engine can use the same trick
///   to test identities it could never expand.
/// - **Invertible polynomial maps as reversible encodings.** phi and psi are mutually inverse
///   integer-polynomial maps between F_p^3 and the points of F = 0 in F_p^4, so over a finite field
///   they are an explicit bijection with polynomial-time encode and decode. Interesting as a toy;
///   it is NOT a cryptographic primitive and nothing here suggests one.
public class AbhyankarSathaye {

    // ------------------------------------------------------------------ rings
    interface Ring<E> {
        E of(long c);
        E add(E a, E b);
        E sub(E a, E b);
        E mul(E a, E b);
        boolean isZero(E a);
        default E pow(E a, int k) {
            E r = of(1);
            for (int i = 0; i < k; i++) r = mul(r, a);
            return r;
        }
        default E neg(E a) { return sub(of(0), a); }
        default E c(long k, E a) { return mul(of(k), a); }
        default boolean eq(E a, E b) { return isZero(sub(a, b)); }
    }

    /// Sparse polynomial over Z in up to 4 variables; exponent vector packed 16 bits per variable.
    record Poly(Map<Long, BigInteger> t) {
        static long pack(int[] e) {
            long k = 0;
            for (int i = 0; i < 4; i++) k |= ((long) e[i]) << (16 * i);
            return k;
        }
        static int exp(long k, int i) { return (int) ((k >>> (16 * i)) & 0xFFFF); }
        static Poly var(int i) {
            int[] e = new int[4];
            e[i] = 1;
            return new Poly(Map.of(pack(e), BigInteger.ONE));
        }
        int degree() {
            int d = -1;
            for (long k : t.keySet()) d = Math.max(d, exp(k, 0) + exp(k, 1) + exp(k, 2) + exp(k, 3));
            return d;
        }
        Poly pderiv(int i) {
            Map<Long, BigInteger> r = new HashMap<>();
            for (var en : t.entrySet()) {
                int ei = exp(en.getKey(), i);
                if (ei == 0) continue;
                long k = en.getKey() - (1L << (16 * i));
                r.merge(k, en.getValue().multiply(BigInteger.valueOf(ei)), BigInteger::add);
            }
            r.values().removeIf(v -> v.signum() == 0);
            return new Poly(r);
        }
        <E> E eval(Ring<E> R, E[] pt) {
            E tot = R.of(0);
            for (var en : t.entrySet()) {
                E m = R.of(en.getValue().longValueExact());
                for (int i = 0; i < 4; i++) m = R.mul(m, R.pow(pt[i], exp(en.getKey(), i)));
                tot = R.add(tot, m);
            }
            return tot;
        }
    }

    static final Ring<Poly> ZPOLY = new Ring<>() {
        public Poly of(long c) {
            return c == 0 ? new Poly(Map.of()) : new Poly(Map.of(0L, BigInteger.valueOf(c)));
        }
        public Poly add(Poly a, Poly b) {
            Map<Long, BigInteger> r = new HashMap<>(a.t());
            b.t().forEach((k, v) -> r.merge(k, v, BigInteger::add));
            r.values().removeIf(v -> v.signum() == 0);
            return new Poly(r);
        }
        public Poly sub(Poly a, Poly b) {
            Map<Long, BigInteger> r = new HashMap<>(a.t());
            b.t().forEach((k, v) -> r.merge(k, v.negate(), BigInteger::add));
            r.values().removeIf(v -> v.signum() == 0);
            return new Poly(r);
        }
        public Poly mul(Poly a, Poly b) {
            Map<Long, BigInteger> r = new HashMap<>();
            for (var x : a.t().entrySet())
                for (var y : b.t().entrySet())
                    r.merge(x.getKey() + y.getKey(), x.getValue().multiply(y.getValue()), BigInteger::add);
            r.values().removeIf(v -> v.signum() == 0);
            return new Poly(r);
        }
        public boolean isZero(Poly a) { return a.t().isEmpty(); }
    };

    /// Exact rationals.
    record Q(BigInteger n, BigInteger d) {
        static Q of(BigInteger n, BigInteger d) {
            if (d.signum() < 0) { n = n.negate(); d = d.negate(); }
            BigInteger g = n.gcd(d);
            return g.signum() == 0 ? new Q(n, d) : new Q(n.divide(g), d.divide(g));
        }
        @Override public String toString() { return d.equals(BigInteger.ONE) ? n.toString() : n + "/" + d; }
    }

    static final Ring<Q> RAT = new Ring<>() {
        public Q of(long c) { return new Q(BigInteger.valueOf(c), BigInteger.ONE); }
        public Q add(Q a, Q b) { return Q.of(a.n().multiply(b.d()).add(b.n().multiply(a.d())), a.d().multiply(b.d())); }
        public Q sub(Q a, Q b) { return Q.of(a.n().multiply(b.d()).subtract(b.n().multiply(a.d())), a.d().multiply(b.d())); }
        public Q mul(Q a, Q b) { return Q.of(a.n().multiply(b.n()), a.d().multiply(b.d())); }
        public boolean isZero(Q a) { return a.n().signum() == 0; }
    };

    /// Z/p for a prime p, elements as reduced BigIntegers.
    static Ring<BigInteger> modP(BigInteger p) {
        return new Ring<>() {
            public BigInteger of(long c) { return BigInteger.valueOf(c).mod(p); }
            public BigInteger add(BigInteger a, BigInteger b) { return a.add(b).mod(p); }
            public BigInteger sub(BigInteger a, BigInteger b) { return a.subtract(b).mod(p); }
            public BigInteger mul(BigInteger a, BigInteger b) { return a.multiply(b).mod(p); }
            public boolean isZero(BigInteger a) { return a.mod(p).signum() == 0; }
            @Override public BigInteger pow(BigInteger a, int k) { return a.modPow(BigInteger.valueOf(k), p); }
        };
    }

    // ------------------------------------------------------------------ the Lean definitions
    /// S h u v w = 2u^3v + 3u^4w + h(v^2 - 3u^2w^2) + h^2w^3; `c1` is the 2 in front of u^3v
    /// (the negative control changes it to 3).
    static <E> E S(Ring<E> R, E h, E u, E v, E w, long c1) {
        E t1 = R.c(c1, R.mul(R.pow(u, 3), v));
        E t2 = R.c(3, R.mul(R.pow(u, 4), w));
        E t3 = R.mul(h, R.sub(R.pow(v, 2), R.c(3, R.mul(R.pow(u, 2), R.pow(w, 2)))));
        E t4 = R.mul(R.pow(h, 2), R.pow(w, 3));
        return R.add(R.add(t1, t2), R.add(t3, t4));
    }

    static <E> E P(Ring<E> R, E x, E y, E s) {
        return R.add(R.add(R.c(-2, R.mul(R.pow(s, 2), x)), R.c(3, R.mul(s, R.pow(y, 2)))),
            R.c(-3, R.mul(R.pow(s, 3), y)));
    }

    static <E> E alpha(Ring<E> R, E x, E s) {
        return R.add(R.add(R.of(1), R.c(2, R.mul(R.pow(s, 2), x))), R.c(4, R.pow(s, 5)));
    }

    static <E> E beta(Ring<E> R, E x, E y, E s) {
        E a = R.sub(R.c(3, R.pow(s, 3)), R.c(3, R.mul(s, y)));
        E b = R.add(R.of(1), R.c(2, R.mul(R.pow(s, 2), x)));
        return R.sub(R.mul(a, b), R.c(4, R.mul(R.pow(s, 4), R.pow(y, 2))));
    }

    /// x, y, s, F, shiftX, shiftY, fiberParameter (in that order) for a point/polynomials h,u,v,w.
    static <E> List<E> derived(Ring<E> R, E h, E u, E v, E w, long c1) {
        E x = R.add(R.pow(u, 3), R.mul(h, v));
        E y = R.add(R.neg(R.pow(u, 2)), R.mul(h, w));
        E s = S(R, h, u, v, w, c1);
        E F = R.sub(R.sub(h, P(R, x, y, s)), R.of(1));
        E shiftX = R.add(x, R.pow(s, 3));
        E shiftY = R.sub(y, R.pow(s, 2));
        E param = R.add(R.mul(alpha(R, x, s), u), R.mul(beta(R, x, y, s), R.add(v, R.mul(u, w))));
        return List.of(x, y, s, F, shiftX, shiftY, param);
    }

    /// freeH, freeU, freeV, freeW; `c2` is the 2 in front of U*y*G in inverseW (control: 3).
    static <E> List<E> forward(Ring<E> R, E X, E Y, E T, long c2) {
        E fS = R.add(R.pow(X, 2), R.pow(Y, 3));
        E fX = R.sub(X, R.pow(fS, 3));
        E fY = R.add(Y, R.pow(fS, 2));
        E fH = R.add(R.of(1), P(R, fX, fY, fS));
        E fA = alpha(R, fX, fS);
        E fB = beta(R, fX, fY, fS);
        E U = R.sub(R.mul(fH, T), R.mul(fB, fX));                       // inverseU
        E G = R.add(R.mul(fY, T), R.mul(fA, fX));                       // inverseG
        E W = R.add(                                                    // inverseW
            R.mul(R.mul(fA, R.add(R.of(1), R.mul(fB, fY))), R.add(fY, R.pow(U, 2))),
            R.mul(R.pow(fB, 2), R.add(R.sub(fS, R.mul(fH, R.pow(G, 2))), R.c(c2, R.mul(R.mul(U, fY), G)))));
        E V = R.sub(G, R.mul(U, W));                                    // inverseV
        return List.of(fH, U, V, W);
    }

    static int failures = 0;

    static void check(String label, boolean cond) {
        System.out.println((cond ? "PASS " : "FAIL ") + label);
        if (!cond) failures++;
    }

    static void control(String label, boolean held) {
        System.out.println((held ? "CONTROL-HELD (BAD) " : "CONTROL-FAILED-AS-EXPECTED ") + label);
        if (held) failures++;
    }

    public static void main(String[] args) {
        // A. symbolic
        Poly h = Poly.var(0), u = Poly.var(1), v = Poly.var(2), w = Poly.var(3);
        List<Poly> d = derived(ZPOLY, h, u, v, w, 2);
        Poly F = d.get(3);
        System.out.println("F in Z[h,u,v,w]: degree " + F.degree() + ", " + F.t().size() + " terms");
        Poly lhs = ZPOLY.add(ZPOLY.pow(d.get(4), 2), ZPOLY.pow(d.get(5), 3));
        check("[A] ambient  shiftX^2 + shiftY^3 = s*(1+F)", ZPOLY.eq(lhs, ZPOLY.mul(d.get(2), ZPOLY.add(ZPOLY.of(1), F))));
        check("[A] cusp     x^2 + y^3 = h*s",
            ZPOLY.eq(ZPOLY.add(ZPOLY.pow(d.get(0), 2), ZPOLY.pow(d.get(1), 3)), ZPOLY.mul(h, d.get(2))));

        // B. critical point, exact
        Q[] cp = {RAT.of(2), RAT.of(0), Q.of(BigInteger.valueOf(-1), BigInteger.TWO), Q.of(BigInteger.ONE, BigInteger.TWO)};
        Q fv = F.eval(RAT, cp);
        boolean crit = true;
        StringBuilder g = new StringBuilder();
        for (int i = 0; i < 4; i++) {
            Q gi = F.pderiv(i).eval(RAT, cp);
            g.append(gi).append(i < 3 ? ", " : "");
            crit &= RAT.isZero(gi);
        }
        check("[B] F(2,0,-1/2,1/2) = " + fv + " (want -1)", RAT.eq(fv, RAT.of(-1)));
        check("[B] gradient there = (" + g + ")", crit);

        // C. Schwartz-Zippel mod 2^61 - 1
        BigInteger p = BigInteger.ONE.shiftLeft(61).subtract(BigInteger.ONE);
        Ring<BigInteger> Fp = modP(p);
        Random rnd = new Random(20261008);
        boolean all = true;
        int trials = 30;
        for (int i = 0; i < trials; i++) {
            BigInteger X = new BigInteger(61, rnd).mod(p), Y = new BigInteger(61, rnd).mod(p), T = new BigInteger(61, rnd).mod(p);
            List<BigInteger> f = forward(Fp, X, Y, T, 2);
            List<BigInteger> e = derived(Fp, f.get(0), f.get(1), f.get(2), f.get(3), 2);
            all &= Fp.isZero(e.get(3)) && Fp.eq(e.get(4), X) && Fp.eq(e.get(5), Y) && Fp.eq(e.get(6), T);
        }
        check("[C] phi(F)=0, phi(shiftX)=X, phi(shiftY)=Y, phi(param)=T at " + trials + " random points mod 2^61-1", all);

        // D. small fields, full enumeration
        for (int q : new int[] {7, 11}) {
            Ring<BigInteger> Fq = modP(BigInteger.valueOf(q));
            Set<String> zero = new HashSet<>();
            boolean back = true;
            for (int a = 0; a < q; a++) for (int b = 0; b < q; b++) for (int c = 0; c < q; c++) for (int e = 0; e < q; e++) {
                BigInteger[] pt = {BigInteger.valueOf(a), BigInteger.valueOf(b), BigInteger.valueOf(c), BigInteger.valueOf(e)};
                List<BigInteger> dd = derived(Fq, pt[0], pt[1], pt[2], pt[3], 2);
                if (!Fq.isZero(dd.get(3))) continue;
                zero.add(a + "," + b + "," + c + "," + e);
                List<BigInteger> f = forward(Fq, dd.get(4), dd.get(5), dd.get(6), 2);
                for (int i = 0; i < 4; i++) back &= Fq.eq(f.get(i), pt[i]);
            }
            Set<String> image = new HashSet<>();
            for (int a = 0; a < q; a++) for (int b = 0; b < q; b++) for (int c = 0; c < q; c++) {
                List<BigInteger> f = forward(Fq, BigInteger.valueOf(a), BigInteger.valueOf(b), BigInteger.valueOf(c), 2);
                image.add(f.get(0) + "," + f.get(1) + "," + f.get(2) + "," + f.get(3));
            }
            check("[D] p=" + q + ": #V(F) = " + zero.size() + " (p^3 = " + q * q * q + "), psi o phi = id on V(F): "
                + back + ", phi(F_p^3) = V(F): " + image.equals(zero),
                zero.size() == q * q * q && back && image.equals(zero));
        }

        // E. negative controls
        BigInteger X = new BigInteger(61, rnd).mod(p), Y = new BigInteger(61, rnd).mod(p), T = new BigInteger(61, rnd).mod(p);
        List<BigInteger> f = forward(Fp, X, Y, T, 2);
        control("perturbed S (2u^3v -> 3u^3v): phi(F') = 0", Fp.isZero(derived(Fp, f.get(0), f.get(1), f.get(2), f.get(3), 3).get(3)));
        List<BigInteger> f3 = forward(Fp, X, Y, T, 3);
        List<BigInteger> e3 = derived(Fp, f3.get(0), f3.get(1), f3.get(2), f3.get(3), 2);
        control("wrong inverse (2UyG -> 3UyG): phi(F)=0 and phi(shiftY)=Y", Fp.isZero(e3.get(3)) && Fp.eq(e3.get(5), Y));
        Q[] moved = {RAT.of(2), RAT.of(0), Q.of(BigInteger.valueOf(-1), BigInteger.TWO), Q.of(BigInteger.valueOf(3), BigInteger.TWO)};
        Q g0 = F.pderiv(0).eval(RAT, moved);
        control("moved point (2,0,-1/2,3/2): dF/dh = " + g0 + " is zero", RAT.isZero(g0));

        System.out.println(failures == 0 ? "OVERALL: ALL CHECKS PASS, ALL CONTROLS FAIL" : "OVERALL: " + failures + " PROBLEM(S)");
        if (failures != 0) System.exit(1);
    }
}
