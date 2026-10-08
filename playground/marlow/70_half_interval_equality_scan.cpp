// Equality classification backstop for the item 68 overlap theorem.
// Exhaustively scans units at odd moduli n <= 10,000 using exact
// floor-sum counts, independent of the graph constructions.
// Build: c++ -O3 -std=c++17 -Wall -Wextra 70_half_interval_equality_scan.cpp -o scan
// Run:   ./scan
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>

static std::int64_t floor_sum_nonnegative(std::int64_t n, std::int64_t m,
                                          std::int64_t a, std::int64_t b) {
    std::int64_t answer = 0;
    while (true) {
        if (a >= m) {
            answer += (n - 1) * n * (a / m) / 2;
            a %= m;
        }
        if (b >= m) {
            answer += n * (b / m);
            b %= m;
        }
        std::int64_t y = a * n + b;
        if (y < m) break;
        n = y / m;
        b = y % m;
        std::swap(a, m);
    }
    return answer;
}

static std::int64_t floor_sum(std::int64_t n, std::int64_t m,
                              std::int64_t a, std::int64_t b) {
    std::int64_t q = b / m, r = b % m;
    if (r < 0) {
        --q;
        r += m;
    }
    return n * q + floor_sum_nonnegative(n, m, a, r);
}

static int overlap(int n, int a) {
    int k = (n - 1) / 2;
    // Difference counts x=1..k for which ax mod n lies in 1..k.
    return int(floor_sum(k, n, a, a) -
               floor_sum(k, n, a, a - k - 1));
}

int main() {
    std::int64_t units = 0, equalities = 0, noncanonical = 0, divisible3 = 0;
    for (int n = 5; n <= 10000; n += 2) {
        int k = (n - 1) / 2, minimum = (k + 2) / 3;
        int minus3 = n - 3;
        int inverse_minus3 =
            n % 3 == 1 ? (n - 1) / 3 :
            n % 3 == 2 ? (2 * n - 1) / 3 : -1;
        for (int a = 2; a <= n - 2; ++a) {
            if (std::gcd(a, n) != 1) continue;
            ++units;
            int count = overlap(n, a);
            if (count < minimum) {
                std::cout << "BOUND_FAIL n=" << n << " a=" << a << '\n';
                return 1;
            }
            if (count != minimum) continue;
            ++equalities;
            if (n % 3 == 0) {
                ++divisible3;
                std::cout << "DIV3_EQUALITY n=" << n << " a=" << a << '\n';
            } else if (a != minus3 && a != inverse_minus3) {
                ++noncanonical;
                std::cout << "NONCANONICAL n=" << n << " a=" << a << '\n';
            }
        }
    }
    std::cout << "PASS odd_moduli=4998 units=" << units
              << " equalities=" << equalities
              << " noncanonical=" << noncanonical
              << " divisible3_equalities=" << divisible3 << '\n';
}
