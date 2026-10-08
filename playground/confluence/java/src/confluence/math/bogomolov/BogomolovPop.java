package confluence.math.bogomolov;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/// Finite companion to OAI.BogomolovPop.main_graph_injective
/// (lean/ComparatorChallenges/BogomolovPopInjectivity.lean). The Lean theorem itself is about
/// function fields K|k, L|l of transcendence degree at least 2 over algebraically closed k, l
/// with char != ell, and is not computable: it says that if two isomorphisms of perfect closures
/// (preserving the constant fields) induce the same isomorphism of pro-ell abelianized Galois
/// groups, modulo Z_ell^x scaling, then they agree modulo Frobenius twists. Nothing here proves it.
///
/// What this file checks, as two finite pieces of that mechanism:
///
/// - **Check A** is the Lean lemma `polynomial_power_prime`: (X+1)^n = X^n + 1 in k[X] iff n = 1
///   or n = p^r with p = char k. This dichotomy is where "agree modulo Frobenius" comes from in
///   the proof: an endomorphism acting as an integer power n modulo constants must be x -> x^n
///   and n must be a power of the characteristic.
/// - **Check B** is a finite toy (my construction, not from the paper): K = F_p(x), automorphisms
///   x -> (ax+b)/(cx+d) in PGL2(F_p), acting on the Kummer piece V = sum-zero vectors in
///   (Z/ell)^{P^1(F_p)} (the classes of products of (x - t) modulo constants and ell-th powers).
///   The map "automorphism -> action on V modulo F_ell^x scalars" is checked injective by brute
///   force, and the absolute Frobenius f -> f^p is checked to act on V as the scalar p (so it is
///   invisible modulo scalars, which is why the Galois side is taken modulo units).
/// - **Control C1** must FAIL: restricting to the rank-one piece spanned by (x) (divisor
///   e_0 - e_inf), distinct maps such as x -> 1/x and x -> 1/(2x) give the same data.
///
/// Run (from java/): javac -d out $(find src -name "*.java") && java -cp out confluence.math.bogomolov.BogomolovPop
///
/// ## What this could mean for Java code
///
/// These are possible uses I can defend, not claims from the paper.
///
/// - **Fingerprints modulo a symmetry need the right quotient.** Check B is "is this map
///   recoverable from its action, modulo scalars?". The same question appears when Java code
///   dedupes linear transforms, projective transforms or permutations by a canonical form: the
///   canonical form here (minimum over scalar multiples) is a pattern that can be lifted directly.
/// - **A coarser invariant is a cache key that collides.** C1 shows a rank-one summary that maps
///   distinct transforms to one key. Code that keys a cache by a summary (a hash of one column,
///   a determinant, a sign) should carry a collision test like this one.
/// - **Lucas-style binomial checks are cheap.** Check A is a tiny, exact test for "is n a power of
///   p" via binomial coefficients mod p, usable as a cross-check against a direct implementation
///   in number-theory utilities.
/// - **Mutant instruments.** The toy's honesty rests on the action actually being computed; a
///   version that ignores part of the map (the Python mutant that drops the Galois twist) loses
///   injectivity. Keeping such a mutant beside a checker is a reusable testing habit.
public class BogomolovPop {

    static final int INF = -1;

    // ---------- Check A ----------
    static boolean isPowerOf(int n, int p) { while (n % p == 0) n /= p; return n == 1; }

    static boolean frobIdentity(int n, int p) { // p == 0: characteristic 0
        for (int i = 1; i < n; i++) {
            BigInteger c = binom(n, i);
            if (p == 0 ? c.signum() != 0 : c.mod(BigInteger.valueOf(p)).signum() != 0) return false;
        }
        return true;
    }

    static BigInteger binom(int n, int k) {
        BigInteger r = BigInteger.ONE;
        for (int i = 0; i < k; i++) r = r.multiply(BigInteger.valueOf(n - i)).divide(BigInteger.valueOf(i + 1));
        return r;
    }

    // ---------- Check B (prime q = p) ----------
    static int inv(int a, int p) { return BigInteger.valueOf(a).modInverse(BigInteger.valueOf(p)).intValue(); }

    static int mobius(int[] m, int z, int p) {
        int a = m[0], b = m[1], c = m[2], d = m[3];
        if (z == INF) return c == 0 ? INF : a * inv(c, p) % p;
        int num = (a * z + b) % p, den = (c * z + d) % p;
        return den == 0 ? INF : num * inv(den, p) % p;
    }

    static int[] points(int p) { int[] pts = new int[p + 1]; for (int i = 0; i < p; i++) pts[i] = i; pts[p] = INF; return pts; }

    static int pos(int t, int p) { return t == INF ? p : t; }

    /// PGL2(F_p), one representative per point map.
    static List<int[]> pgl2(int p) {
        List<int[]> out = new ArrayList<>();
        java.util.Set<String> seen = new java.util.HashSet<>();
        for (int a = 0; a < p; a++) for (int b = 0; b < p; b++) for (int c = 0; c < p; c++) for (int d = 0; d < p; d++) {
            if (((a * d - b * c) % p + p) % p == 0) continue;
            int[] m = {a, b, c, d};
            int[] img = new int[p + 1];
            int[] pts = points(p);
            for (int i = 0; i <= p; i++) img[i] = mobius(m, pts[i], p);
            if (seen.add(Arrays.toString(img))) out.add(m);
        }
        return out;
    }

    /// alpha(x - t) = M(x) - t vanishes at M^{-1}(t): the induced point map is M^{-1}.
    static int[] pointAction(int[] m, int p) {
        int[] mi = {m[3], (p - m[1]) % p, (p - m[2]) % p, m[0]};
        int[] pts = points(p), perm = new int[p + 1];
        for (int i = 0; i <= p; i++) perm[i] = pos(mobius(mi, pts[i], p), p);
        return perm;
    }

    /// Matrix on V in basis e_t - e_inf (t finite); columns are images, scaled by `scalar`.
    static int[][] actionOnV(int[] perm, int p, int ell, int scalar) {
        int[][] cols = new int[p][];
        for (int t = 0; t < p; t++) {
            int[] v = new int[p + 1];
            v[perm[t]] += scalar; v[perm[p]] -= scalar;
            cols[t] = new int[p];
            for (int i = 0; i < p; i++) cols[t][i] = Math.floorMod(v[i], ell);
        }
        return cols;
    }

    static String modScalars(int[][] mat, int ell) {
        String best = null;
        for (int lam = 1; lam < ell; lam++) {
            StringBuilder sb = new StringBuilder();
            for (int[] col : mat) for (int x : col) sb.append(lam * x % ell).append(',');
            String s = sb.toString();
            if (best == null || s.compareTo(best) < 0) best = s;
        }
        return best;
    }

    public static void main(String[] args) {
        int failA = 0;
        for (int p : new int[] {0, 2, 3, 5, 7, 11, 13})
            for (int n = 1; n <= 300; n++)
                if (frobIdentity(n, p) != (p == 0 ? n == 1 : isPowerOf(n, p))) failA++;
        System.out.println("Check A (X+1)^n = X^n+1 iff n=1 or a power of char, p in {0,2..13}, n<=300: mismatches=" + failA);

        boolean ok = failA == 0;
        int[][] cases = {{2, 3}, {3, 2}, {5, 2}, {5, 3}, {7, 2}, {7, 3}, {11, 3}};
        for (int[] cs : cases) {
            int p = cs[0], ell = cs[1];
            Map<String, int[]> seen = new HashMap<>();
            int collisions = 0, frobBad = 0;
            List<int[]> g = pgl2(p);
            for (int[] m : g) {
                int[] perm = pointAction(m, p);
                String key = modScalars(actionOnV(perm, p, ell, 1), ell);
                if (seen.putIfAbsent(key, m) != null) collisions++;
                if (!key.equals(modScalars(actionOnV(perm, p, ell, p), ell))) frobBad++;
            }
            boolean inj = collisions == 0;
            ok &= inj && frobBad == 0;
            System.out.printf("Check B q=%d ell=%d: |PGL2|=%d classes=%d injective=%b, Frobenius invisible mod scalars=%b%n",
                p, ell, g.size(), seen.size(), inj, frobBad == 0);
        }

        // Control C1: rank-one piece span(e_0 - e_inf); must collide.
        Map<String, String> ctrl = new LinkedHashMap<>();
        int p = 5, ell = 3;
        String collision = null;
        for (int[] m : pgl2(p)) {
            int[] perm = pointAction(m, p);
            boolean keeps = (perm[0] == 0 && perm[p] == p) || (perm[0] == p && perm[p] == 0);
            if (!keeps) continue;
            int s = perm[0] == 0 ? 1 : ell - 1;
            String key = modScalars(new int[][] {{s}}, ell);
            String prev = ctrl.putIfAbsent(key, Arrays.toString(m));
            if (prev != null && collision == null) collision = prev + " vs " + Arrays.toString(m);
        }
        boolean ctrlFails = collision != null;
        ok &= ctrlFails;
        System.out.println("Control C1 (rank-one piece, q=5 ell=3) collides as required: " + ctrlFails
            + " e.g. (a,b,c,d) " + collision);
        System.out.println(ok ? "ALL EXPECTED" : "UNEXPECTED RESULT");
        if (!ok) System.exit(1);
    }
}
