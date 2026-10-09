"""A Barnette tour: one unbroken cycle through the truncated octahedron.

The truncated octahedron is the Cayley graph of S_4 on the adjacent transpositions s1 = (01), s2 = (12) and
s3 = (23). It is cubic, bipartite (by the sign of a permutation) and planar and 3-connected (it is a convex
polyhedron), so it is a Barnette graph, and the conjecture (claimed proved in the collection, card 180) says
it has a Hamiltonian cycle. This script:
- builds it, and checks cubic, bipartite and the literal delete-two-vertices 3-connectivity;
- draws it by Tutte's barycentric method: one hexagonal face (the <s1, s2> coset of the identity) is pinned
  on a regular hexagon, and every other vertex sits at the average of its neighbours. For a 3-connected
  planar graph that drawing is guaranteed crossing-free (Tutte 1963), so the planarity is visible;
- finds a Hamiltonian cycle by exhaustive backtracking, verifies it, and draws it as one glowing line;
- colours the vertices by their bipartition class (even and odd permutations).
Run: python3 -I barnette_tour.py  (writes barnette_tour.svg next to itself)
"""
import itertools
import math
import pathlib

perms = list(itertools.permutations(range(4)))
idx = {p: i for i, p in enumerate(perms)}


def swap(p, s):
    q = list(p)
    q[s], q[s + 1] = q[s + 1], q[s]
    return tuple(q)


adj = [[idx[swap(p, s)] for s in range(3)] for p in perms]
n = len(perms)
assert all(len(set(a)) == 3 for a in adj)


def sign(p):
    return sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2


assert all(sign(perms[v]) != sign(perms[w]) for v in range(n) for w in adj[v])  # bipartite


def connected_without(removed):
    alive = [v for v in range(n) if v not in removed]
    seen, stack = {alive[0]}, [alive[0]]
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in removed and w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == len(alive)


assert all(connected_without({a, b}) for a in range(n) for b in range(n))  # 3-connected (a == b covers |S| = 1)

# outer face: the <s1, s2> coset of the identity, in cycle order (alternate s1, s2)
outer, p, s = [], tuple(range(4)), 0
while True:
    outer.append(idx[p])
    p = swap(p, s)
    s = 1 - s
    if idx[p] == outer[0]:
        break
assert len(outer) == 6

W, H = 780, 880
CX, CY, R = W / 2, 440, 330
pos = {v: [CX, CY] for v in range(n)}
for k, v in enumerate(outer):
    a = -math.pi / 2 + 2 * math.pi * k / 6
    pos[v] = [CX + R * math.cos(a), CY + R * math.sin(a)]
inner = [v for v in range(n) if v not in outer]
for _ in range(4000):  # Gauss-Seidel relaxation of the barycentric equations
    for v in inner:
        pos[v] = [sum(pos[w][0] for w in adj[v]) / 3, sum(pos[w][1] for w in adj[v]) / 3]


def segments_cross(a, b, c, d):
    def orient(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    if len({a, b, c, d}) < 4:
        return False
    pa, pb, pc, pd = pos[a], pos[b], pos[c], pos[d]
    return orient(pa, pb, pc) * orient(pa, pb, pd) < 0 and orient(pc, pd, pa) * orient(pc, pd, pb) < 0


edges = sorted({tuple(sorted((v, w))) for v in range(n) for w in adj[v]})
assert len(edges) == 36
assert not any(segments_cross(*e, *f) for e, f in itertools.combinations(edges, 2))  # the drawing is plane


def hamiltonian():
    path, used = [0], {0}

    def go():
        if len(path) == n:
            return path[0] in adj[path[-1]]
        for w in adj[path[-1]]:
            if w not in used:
                path.append(w); used.add(w)
                if go():
                    return True
                path.pop(); used.discard(w)
        return False
    return path if go() else None


cyc = hamiltonian()
assert cyc and len(set(cyc)) == n and all(cyc[(i + 1) % n] in adj[cyc[i]] for i in range(n))

EVEN, ODD = "#f2c14e", "#7aa7ff"
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs><radialGradient id="bg" cx="50%" cy="52%" r="62%"><stop offset="0" stop-color="#1a2032"/>'
         '<stop offset="1" stop-color="#090c14"/></radialGradient>'
         '<linearGradient id="tour" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff9f68"/>'
         '<stop offset="0.5" stop-color="#ff5fa2"/><stop offset="1" stop-color="#8a7dff"/></linearGradient>'
         '<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>'
         '</defs>',
         f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']
for v, w in edges:
    (x1, y1), (x2, y2) = pos[v], pos[w]
    parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#5c6680" '
                 f'stroke-width="1.6" stroke-opacity="0.75"/>')
d = "M" + " L".join(f"{pos[v][0]:.1f},{pos[v][1]:.1f}" for v in cyc) + " Z"
parts.append(f'<path d="{d}" fill="none" stroke="url(#tour)" stroke-width="11" stroke-opacity="0.45" '
             f'stroke-linejoin="round" filter="url(#glow)"/>')
parts.append(f'<path d="{d}" fill="none" stroke="url(#tour)" stroke-width="4" stroke-linejoin="round"/>')
for v in range(n):
    x, y = pos[v]
    col = EVEN if sign(perms[v]) == 0 else ODD
    parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7.5" fill="#090c14" stroke="{col}" stroke-width="2.6"/>')
parts.append(f'<text x="{CX}" y="46" text-anchor="middle" font-family="Georgia, serif" font-size="25" '
             f'fill="#e8ecf4">A Barnette tour</text>')
parts.append(f'<text x="{CX}" y="72" text-anchor="middle" font-family="Georgia, serif" font-size="13.5" '
             f'fill="#a9b2c4">the truncated octahedron (S&#8324; on adjacent swaps), drawn by Tutte&#8217;s barycentric method</text>')
parts.append(f'<text x="{CX}" y="{H - 44}" text-anchor="middle" font-family="Georgia, serif" font-size="13.5" '
             f'fill="#a9b2c4">cubic &#183; bipartite (<tspan fill="{EVEN}">even</tspan> / <tspan fill="{ODD}">odd</tspan> '
             f'permutations) &#183; planar &#183; 3-connected &#8594; one cycle through all 24</text>')
parts.append(f'<text x="{CX}" y="{H - 22}" text-anchor="middle" font-family="Georgia, serif" font-size="12" '
             f'fill="#7f889a">every property asserted by the script that drew it, including that no two edges cross</text>')
parts.append('</svg>')
pathlib.Path(__file__).with_suffix(".svg").write_text("\n".join(parts))
print("wrote", pathlib.Path(__file__).with_suffix(".svg"), "cycle", cyc)
