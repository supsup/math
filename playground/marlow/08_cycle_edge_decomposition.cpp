// Exact small-order cycle-and-edge partition census for family 181.
// Run from the repo root:
// c++ -O3 -std=c++17 -o /tmp/marlow_cycle_decomp playground/marlow/08_cycle_edge_decomposition.cpp
// /tmp/marlow_cycle_decomp
// A cycle is simple and has at least three edges. Vertices are labelled 0..n-1.

#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <set>
#include <utility>
#include <vector>

using namespace std;

struct Census {
  int n;
  int edge_count;
  vector<pair<int, int>> edges;
  vector<int> cycles;
  vector<vector<int>> cycles_at_edge;
  vector<uint8_t> optimum;
  vector<int> extremal_masks;

  explicit Census(int order) : n(order), edge_count(order * (order - 1) / 2) {
    int index[7][7]{};
    for (int u = 0; u < n; ++u) {
      for (int v = u + 1; v < n; ++v) {
        index[u][v] = index[v][u] = int(edges.size());
        edges.emplace_back(u, v);
      }
    }
    for (int first = 0; first < n; ++first) {
      vector<int> path{first};
      auto extend = [&](auto&& self, int used, int edge_mask) -> void {
        if (path.size() >= 3 && path[1] < path.back()) {
          cycles.push_back(edge_mask | (1 << index[path.back()][first]));
        }
        for (int next = first + 1; next < n; ++next) {
          if (used & (1 << next)) continue;
          int last = path.back();
          path.push_back(next);
          self(self, used | (1 << next), edge_mask | (1 << index[last][next]));
          path.pop_back();
        }
      };
      extend(extend, 1 << first, 0);
    }
    set<int> distinct(cycles.begin(), cycles.end());
    assert(distinct.size() == cycles.size());
    constexpr int expected_cycles[] = {0, 0, 0, 1, 7, 37, 197, 1172};
    assert(int(cycles.size()) == expected_cycles[n]);
    cycles_at_edge.resize(edge_count);
    for (int cycle : cycles) {
      for (int edge = 0; edge < edge_count; ++edge) {
        if (cycle & (1 << edge)) cycles_at_edge[edge].push_back(cycle);
      }
    }
    optimum.resize(1 << edge_count);
  }

  int split_mask(int hub_bits) const {
    int mask = 0;
    for (int i = 0; i < edge_count; ++i) {
      auto [u, v] = edges[i];
      if ((hub_bits & (1 << u)) || (hub_bits & (1 << v))) mask |= 1 << i;
    }
    return mask;
  }

  void run() {
    array<int, 8> histogram{};
    histogram[0] = 1;
    int maximum = 0;
    for (int mask = 1; mask < int(optimum.size()); ++mask) {
      int pivot_bit = mask & -mask;
      int pivot = __builtin_ctz(static_cast<unsigned>(pivot_bit));
      int best = 1 + optimum[mask ^ pivot_bit];
      for (int cycle : cycles_at_edge[pivot]) {
        if ((mask & cycle) == cycle) {
          best = min(best, 1 + int(optimum[mask ^ cycle]));
        }
      }
      assert(best < int(histogram.size()));
      optimum[mask] = static_cast<uint8_t>(best);
      ++histogram[best];
      if (best > maximum) {
        maximum = best;
        extremal_masks.clear();
      }
      if (best == maximum) extremal_masks.push_back(mask);
    }
    constexpr int expected_maximum[] = {0, 0, 1, 2, 3, 4, 5, 7};
    constexpr int expected_extremal_count[] = {0, 0, 1, 3, 17, 170, 2664, 35};
    assert(maximum == expected_maximum[n]);
    assert(int(extremal_masks.size()) == expected_extremal_count[n]);
    if (n == 7) {
      set<int> expected;
      for (int hubs = 0; hubs < (1 << n); ++hubs) {
        if (__builtin_popcount(static_cast<unsigned>(hubs)) == 3) {
          expected.insert(split_mask(hubs));
        }
      }
      assert(expected.size() == 35);
      assert(expected == set<int>(extremal_masks.begin(), extremal_masks.end()));
      // Explicit 7-part partition of K_3 joined to an independent 4-set:
      // triangle 0-1-2; four-cycles 0-3-1-4 and 0-5-1-6;
      // singleton edges 2-3, 2-4, 2-5, 2-6.
      int witness = 0;
      const vector<vector<int>> walks{{0, 1, 2}, {0, 3, 1, 4}, {0, 5, 1, 6}};
      for (const auto& walk : walks) {
        int cycle = 0;
        for (size_t j = 0; j < walk.size(); ++j) {
          auto e = minmax(walk[j], walk[(j + 1) % walk.size()]);
          auto it = find(edges.begin(), edges.end(), e);
          assert(it != edges.end());
          cycle |= 1 << (it - edges.begin());
        }
        assert((witness & cycle) == 0);
        witness |= cycle;
      }
      for (int leaf = 3; leaf < 7; ++leaf) {
        auto it = find(edges.begin(), edges.end(), make_pair(2, leaf));
        assert(it != edges.end());
        int bit = 1 << (it - edges.begin());
        assert((witness & bit) == 0);
        witness |= bit;
      }
      assert(witness == split_mask(0b0000111));
      assert(optimum[witness] == 7);
    }
    cout << "n=" << n << " graphs=" << optimum.size() << " cycles=" << cycles.size()
         << " max=" << maximum << " labelled_extrema=" << extremal_masks.size()
         << " histogram=";
    for (int i = 0; i <= maximum; ++i) cout << (i ? "," : "") << histogram[i];
    cout << '\n';
  }
};

int main() {
  for (int n = 2; n <= 7; ++n) Census(n).run();
}
