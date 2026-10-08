#include <algorithm>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <vector>

constexpr int LIMIT = 32768001;
using i64 = std::int64_t;

int power(int x, int e, int p) {
    i64 y = 1, z = x;
    while (e) {
        if (e & 1) y = y * z % p;
        z = z * z % p;
        e >>= 1;
    }
    return static_cast<int>(y);
}

int norm(i64 x, int p) {
    x %= p;
    return static_cast<int>(x < 0 ? x + p : x);
}

bool direct_ready(int a, int p) {
    int den = norm(i64(a - 1) * (a - 1), p);
    if (!den) return false;
    int inv_den = power(den, p - 2, p);
    int z = norm(i64(1 + 3 * a) * inv_den, p);
    int w = norm(i64(norm(i64(a) * (a + 3), p)) * inv_den, p);
    if (!z || !w) return false;
    if (power(norm(i64(z) * w, p), (p - 1) / 2, p) != p - 1) return false;
    int half = (p + 1) / 2;
    int inv_slot = power(norm(2LL * (a - 1), p), p - 2, p);
    int mu1 = norm(i64(a + 1) * inv_slot, p);
    int mu3 = norm(3LL * mu1, p);
    int b = norm(1LL + z, p);
    int v = norm(1LL + w, p);
    int f1[] = {norm(1LL - mu1, p), norm(1LL + mu1, p)};
    int f3[] = {norm(1LL - mu3, p), norm(1LL + mu3, p)};
    int t1[] = {norm(i64(b) - half, p), norm(i64(b) + half, p),
                norm(i64(b) + 3LL * half, p), norm(i64(v) + half, p)};
    int t3[] = {t1[0], t1[2]};
    for (int x : t1) for (int y : f1) if (x == y) return false;
    for (int x : t3) for (int y : f3) if (x == y) return false;
    return true;
}

void hash32(std::uint64_t &h, std::uint32_t x) {
    for (int i = 0; i < 4; ++i) {
        h ^= (x >> (8 * i)) & 255u;
        h *= 1099511628211ULL;
    }
}

int main() {
    std::vector<unsigned char> composite(LIMIT + 1);
    for (i64 d = 2; d * d <= LIMIT; ++d) {
        if (composite[d]) continue;
        for (i64 j = d * d; j <= LIMIT; j += d) composite[j] = 1;
    }
    std::vector<int> trial;
    for (int d = 2; i64(d) * d <= LIMIT; ++d)
        if (!composite[d]) trial.push_back(d);
    int count = 0, max_g = 0, max_g_p = 0, max_tests = 0, hardest = 0;
    int by_a[11] = {};
    std::uint64_t digest = 14695981039346656037ULL;
    std::vector<int> failures;
    for (int p = 17; p <= LIMIT; p += 8) {
        if (composite[p]) continue;
        int n = p - 1;
        int lowbit = n & -n;
        int A = lowbit / 2;
        int q = n / lowbit;
        if (q <= 6 * (A - 2)) continue;
        ++count;
        int rem = n;
        std::vector<int> divisors;
        for (int d : trial) {
            if (i64(d) * d > rem) break;
            if (rem % d) continue;
            divisors.push_back(d);
            while (rem % d == 0) rem /= d;
        }
        if (rem > 1) divisors.push_back(rem);
        int witness = 0, tested = 0;
        for (int g = 2; g < p; ++g) {
            bool primitive = true;
            for (int d : divisors)
                if (power(g, n / d, p) == 1) { primitive = false; break; }
            if (!primitive) continue;
            ++tested;
            if (direct_ready(power(g, A, p), p)) { witness = g; break; }
        }
        if (!witness) failures.push_back(p);
        else {
            int ai = 0;
            for (int x=A;x>1;x>>=1) ++ai;
            ++by_a[ai];
            if (witness > max_g) { max_g = witness; max_g_p = p; }
            if (tested > max_tests) { max_tests = tested; hardest = p; }
        }
        hash32(digest, static_cast<std::uint32_t>(p));
        hash32(digest, static_cast<std::uint32_t>(witness));
    }
    std::cout << "limit=" << LIMIT << " primes=" << count << " max_g=" << max_g << " max_g_p=" << max_g_p
              << " max_generators_tested=" << max_tests << " hardest=" << hardest
              << " fnv1a64_p_g_le=" << std::hex << std::setw(16) << std::setfill('0') << digest << std::dec << " failures=";
    for (int p : failures) std::cout << p << ',';
    std::cout << '\n';
    for (int i=0;i<11;++i) if (by_a[i])
        std::cout << "A=" << (1<<i) << " count=" << by_a[i] << '\n';
    return failures.empty() ? 0 : 1;
}
