#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

static constexpr int LIMIT = 10000000;

// All products below are below 3*LIMIT^2, so signed 64-bit arithmetic suffices.

static int mod_pow(int base, int exponent, int p) {
    std::int64_t x = base, result = 1;
    while (exponent > 0) {
        if (exponent & 1) result = result * x % p;
        x = x * x % p;
        exponent >>= 1;
    }
    return int(result);
}

static bool ready(int a, int p) {
    const std::int64_t x = a;
    auto residue = [p](std::int64_t z) {
        z %= p;
        return int(z < 0 ? z + p : z);
    };
    const int linear1 = residue(1 + 3*x);
    const int linear2 = residue(x + 3);
    if (linear1 == 0 || linear2 == 0) return false;
    const std::int64_t q[] = {
        // The six nontrivial midpoint exclusions in item 55's repair lemma.
        x*x - 4*x - 1,
        x*x + 3,
        x*x + 1,
        x*x - 2*x - 1,
        x*x + 4*x - 1,
        3*x*x + 1,
    };
    for (auto z : q) if (residue(z) == 0) return false;
    const int character_argument = int(std::int64_t(linear1)*linear2 % p);
    // Since a=g^2, this is chi(W/Z)=-1 in the lemma.
    return mod_pow(character_argument, (p-1)/2, p) == p-1;
}

int main() {
    std::vector<int> spf(LIMIT+1, 0);
    for (int i=2; i<=LIMIT; ++i) {
        if (spf[i]) continue;
        spf[i]=i;
        if (std::int64_t(i)*i>LIMIT) continue;
        for (int j=i*i; j<=LIMIT; j+=i) if (!spf[j]) spf[j]=i;
    }
    int primes=0, witnesses=0, max_g=0, max_tests=0, hardest_p=0;
    for (int p=13; p<=LIMIT; p+=8) {
        if (spf[p]!=p) continue;
        ++primes;
        int n=p-1, left=n;
        std::vector<int> factors;
        while (left>1) {
            int q=spf[left];
            factors.push_back(q);
            do { left/=q; } while (left>1 && left%q==0);
        }
        bool found=false;
        int tested=0;
        for (int g=2; g<p; ++g) {
            bool primitive=true;
            // In the cyclic group F_p^*, g is primitive exactly when none
            // of these prime-index subgroup tests returns 1.
            for (int q : factors) {
                if (mod_pow(g,n/q,p)==1) { primitive=false; break; }
            }
            if (!primitive) continue;
            ++tested;
            int a=int(std::int64_t(g)*g%p);
            if (!ready(a,p)) continue;
            if (p==13) {
                std::cerr << "Unexpected p=13 ready witness\n";
                return 2;
            }
            found=true;
            ++witnesses;
            max_g=std::max(max_g,g);
            if (tested>max_tests) { max_tests=tested; hardest_p=p; }
            break;
        }
        if (p==13) {
            if (found) return 3;
            continue;
        }
        if (!found) {
            std::cerr << "No ready generator at p=" << p << "\n";
            return 1;
        }
    }
    std::cout << "limit=" << LIMIT << " primes_5mod8=" << primes
              << " witnesses_p_ge29=" << witnesses
              << " max_first_g=" << max_g
              << " max_generators_tested=" << max_tests
              << " hardest_p=" << hardest_p << '\n';
    return 0;
}
