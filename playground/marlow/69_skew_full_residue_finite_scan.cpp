// Exact maximal-odd-prefix existence scan for p == 5 (mod 8).
// For each eligible prime, use its least primitive root and seek one
// w in G \ B_exception at c=(p-5)/2. Nested exceptions then cover
// every adjacent page pair. This checks the finite range below item 68.
//
// Build: c++ -O3 -std=c++17 -Wall -Wextra 69_skew_full_residue_finite_scan.cpp -o scan
// Run:   ./scan 59999999
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <vector>

static int residue(std::int64_t x, int p) {
    x %= p;
    return int(x < 0 ? x + p : x);
}

static int power_mod(int a, int n, int p) {
    std::int64_t x = a, z = 1;
    while (n) {
        if (n & 1) z = z * x % p;
        x = x * x % p;
        n >>= 1;
    }
    return int(z);
}

// For prime p, Jacobi(x,p) is the quadratic character of x mod p.
static int jacobi(std::int64_t x, int p) {
    int a = residue(x, p), n = p, sign = 1;
    while (a) {
        while (!(a & 1)) {
            a >>= 1;
            if ((n & 7) == 3 || (n & 7) == 5) sign = -sign;
        }
        std::swap(a, n);
        if ((a & 3) == 3 && (n & 3) == 3) sign = -sign;
        a %= n;
    }
    return n == 1 ? sign : 0;
}

int main(int argc, char** argv) {
    int limit = argc > 1 ? std::atoi(argv[1]) : 59999999;
    if (limit < 13 || limit >= 60000000) {
        std::cerr << "limit must be in [13,60000000)\n";
        return 2;
    }
    std::vector<int> spf(limit + 1);
    for (int i = 2; i <= limit; ++i) {
        if (spf[i]) continue;
        spf[i] = i;
        if (std::int64_t(i) * i > limit) continue;
        for (int j = i * i; j <= limit; j += i)
            if (!spf[j]) spf[j] = i;
    }

    int count = 0, max_g = 0, max_examined = 0, max_examined_p = 0;
    std::int64_t total_examined = 0;
    std::uint64_t digest = 1469598103934665603ULL;
    for (int p = 13; p <= limit; p += 8) {
        if (spf[p] != p) continue;
        ++count;
        int n = p - 1, remaining = n;
        std::vector<int> factors;
        while (remaining > 1) {
            int q = spf[remaining];
            factors.push_back(q);
            do { remaining /= q; } while (remaining > 1 && remaining % q == 0);
        }
        int g = 2;
        for (;; ++g) {
            bool primitive = true;
            for (int q : factors)
                if (power_mod(g, n / q, p) == 1) {
                    primitive = false;
                    break;
                }
            if (primitive) break;
        }
        max_g = std::max(max_g, g);
        int a = int(std::int64_t(g) * g % p);
        int D = a + 1;
        int invD = power_mod(D, p - 2, p);
        int invA = power_mod(a, p - 2, p);
        int delta = residue(std::int64_t(1 - a) * invD, p);
        int c = (p - 5) / 2;
        int examined = 0, witness = -1;
        for (int w = 0; w < p; ++w) {
            ++examined;
            int X = residue(std::int64_t(D) * w - a, p);
            if (residue(-X, p) <= c) continue;
            if (residue(-std::int64_t(invA) * X, p) <= c) continue;
            int F1 = residue(std::int64_t(w) * (w + delta), p);
            if (jacobi(F1, p) != -1) continue;
            int F2 = residue(std::int64_t(w - 1) * (w + delta - 1), p);
            if (jacobi(F2, p) != -1) continue;
            // Independent Euler checks guard against Jacobi implementation errors.
            if (power_mod(F1, n / 2, p) != p - 1 ||
                power_mod(F2, n / 2, p) != p - 1) {
                std::cout << "CHARACTER_MISMATCH p=" << p << " w=" << w << '\n';
                return 1;
            }
            witness = w;
            break;
        }
        if (witness < 0) {
            std::cout << "FAIL p=" << p << " g=" << g << '\n';
            return 1;
        }
        total_examined += examined;
        if (examined > max_examined) {
            max_examined = examined;
            max_examined_p = p;
        }
        digest ^= std::uint64_t(p) << 32 | std::uint32_t(witness);
        digest *= 1099511628211ULL;
        if (p <= 1000) std::cout << p << ' ' << g << ' ' << witness << '\n';
        if (count % 10000 == 0)
            std::cerr << "done=" << count << " p=" << p << '\n';
    }
    std::cout << "PASS limit=" << limit << " primes=" << count
              << " max_g=" << max_g
              << " max_examined=" << max_examined
              << " max_examined_p=" << max_examined_p
              << " total_examined=" << total_examined
              << " digest=" << digest << '\n';
}
