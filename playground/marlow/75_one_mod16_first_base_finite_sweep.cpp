#include <algorithm>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <vector>

static constexpr int N_LIMIT = 32768000;
static constexpr int P_LIMIT = N_LIMIT + 1;

static int power_mod(int base, int exponent, int p) {
    std::int64_t x = base, out = 1;
    while (exponent) {
        if (exponent & 1) out = out * x % p;
        x = x * x % p;
        exponent >>= 1;
    }
    return static_cast<int>(out);
}

static int mod(std::int64_t v, int p) {
    v %= p;
    return static_cast<int>(v < 0 ? v + p : v);
}

static bool slot_and_character_test(int a, int p) {
    const std::int64_t x = a;
    const int f1 = mod(1 + 3*x, p);
    const int f2 = mod(x + 3, p);
    if (f1 == 0 || f2 == 0) return false;
    // Six factorized midpoint collision equations from item 55.
    const std::int64_t bad[6] = {
        x*x - 4*x - 1,
        x*x + 3,
        x*x + 1,
        x*x - 2*x - 1,
        x*x + 4*x - 1,
        3*x*x + 1,
    };
    for (std::int64_t v : bad) if (mod(v, p) == 0) return false;
    // a = g^4 is square, so chi(W/Z) = chi((a+3)(1+3a)).
    const int f = static_cast<int>(std::int64_t(f1) * f2 % p);
    return power_mod(f, (p-1)/2, p) == p-1;
}

static bool direct_template_test(int a, int p) {
    const int den = mod(a-1, p);
    if (den == 0) return false;
    const int inv_den = power_mod(den, p-2, p);
    const int inv_den2 = static_cast<int>(std::int64_t(inv_den)*inv_den % p);
    const int inv2 = (p+1)/2;
    const int Z = static_cast<int>(std::int64_t(mod(1 + 3LL*a, p))*inv_den2 % p);
    const int W = static_cast<int>(std::int64_t(a)*mod(a+3, p)%p*inv_den2%p);
    if (Z == 0 || W == 0) return false;
    const int ratio = static_cast<int>(std::int64_t(W)*power_mod(Z,p-2,p)%p);
    if (power_mod(ratio, (p-1)/2, p) != p-1) return false;
    const int b = mod(1LL+Z,p), v=mod(1LL+W,p);
    const int mu1 = static_cast<int>(std::int64_t(mod(1LL+a,p))*inv2%p*inv_den%p);
    const int mu3 = mod(3LL*mu1,p);
    const int first[4] = {mod(b-inv2,p),mod(b+inv2,p),mod(b+3LL*inv2,p),mod(v+inv2,p)};
    const int second[2] = {mod(b-inv2,p),mod(b+3LL*inv2,p)};
    const int first_slots[2] = {mod(1LL-mu1,p),mod(1LL+mu1,p)};
    const int second_slots[2] = {mod(1LL-mu3,p),mod(1LL+mu3,p)};
    for (int x : first) for (int y : first_slots) if (x == y) return false;
    for (int x : second) for (int y : second_slots) if (x == y) return false;
    return true;
}

static void hash32(std::uint64_t& h, std::uint32_t value) {
    for (int i = 0; i < 4; ++i) {
        h ^= (value >> (8*i)) & 0xffu;
        h *= 1099511628211ull;
    }
}

int main() {
    std::vector<int> spf(P_LIMIT + 1, 0);
    for (int i = 2; i <= P_LIMIT; ++i) {
        if (spf[i]) continue;
        spf[i] = i;
        if (std::int64_t(i)*i > P_LIMIT) continue;
        for (int j = i*i; j <= P_LIMIT; j += i) if (!spf[j]) spf[j] = i;
    }

    std::uint64_t digest = 14695981039346656037ull;
    int primes = 0, covered = 0, missing = 0;
    int max_g = 0, max_primitive_tests = 0, hardest_p = 0;
    int max_candidates = 0, max_candidates_p = 0;
    int first_p = 0, last_p = 0;
    for (int p = 105; p <= P_LIMIT; p += 16) {
        if (spf[p] != p) continue;
        const int q = (p-1)/8;
        if (q <= 12 || (q & 1) == 0) { std::cerr << "Bad range invariant at p=" << p << '\n'; return 2; }
        if (first_p == 0) first_p = p;
        last_p = p;
        ++primes;
        int left = p-1;
        std::vector<int> factors;
        while (left > 1) {
            int f = spf[left];
            factors.push_back(f);
            do { left /= f; } while (left > 1 && left % f == 0);
        }
        int found_g = 0, primitive_tests = 0, candidates = 0;
        for (int g = 2; g < p; ++g) {
            ++candidates;
            bool primitive = true;
            for (int f : factors) {
                if (power_mod(g, (p-1)/f, p) == 1) { primitive = false; break; }
            }
            if (!primitive) continue;
            ++primitive_tests;
            const int a = static_cast<int>(std::int64_t(g)*g%p*g%p*g%p);
            const bool fast = slot_and_character_test(a, p);
            const bool direct = direct_template_test(a, p);
            if (fast != direct) { std::cerr << "filter mismatch p=" << p << " g=" << g << " a=" << a << "\n"; return 3; }
            if (!fast) continue;
            found_g = g;
            break;
        }
        if (!found_g) {
            ++missing;
            std::cout << "missing p=" << p << "\n";
        } else {
            ++covered;
            max_g = std::max(max_g, found_g);
            if (primitive_tests > max_primitive_tests) { max_primitive_tests = primitive_tests; hardest_p = p; }
            if (candidates > max_candidates) { max_candidates = candidates; max_candidates_p = p; }
        }
        hash32(digest, static_cast<std::uint32_t>(p));
        hash32(digest, static_cast<std::uint32_t>(found_g));
        if (primes % 50000 == 0) std::cerr << "progress primes=" << primes << " p=" << p << '\n';
    }
    std::cout << "n_limit=" << N_LIMIT << " first_p=" << first_p << " last_p=" << last_p
              << " primes=" << primes << " covered=" << covered << " missing=" << missing
              << " max_first_g=" << max_g
              << " max_primitive_tests=" << max_primitive_tests << " hardest_p=" << hardest_p
              << " max_candidate_g_tests=" << max_candidates << " max_candidates_p=" << max_candidates_p
              << " fnv1a64_p_g_le=" << std::hex << std::setw(16) << std::setfill('0') << digest << std::dec << '\n';
    return missing ? 1 : 0;
}
