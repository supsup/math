"""Check the stated properties of the pattern graph H in
'A counterexample to Sidorenko's conjecture' (OpenAI, 2026-09-23), from its Table tab:complex.

Claims checked (introduction + complex section):
  - 13 points, 22 triple faces
  - incidence graph H: 35 vertices, 66 edges, bipartite (points | faces), connected
  - "Each of its 33 point pairs belongs to exactly two faces"
  - the table's own "opposite face" columns agree with the triples
Nothing here is taken from the prose except the claims themselves.
"""
from itertools import combinations
from collections import defaultdict

# Face j: (points i1,i2,i3), (opposite faces j12, j13, j23), bits -- transcribed from the table.
TABLE = [
    (0,  (0, 1, 3),   (1, 2, 4),    "000"),
    (1,  (0, 1, 9),   (0, 3, 7),    "010"),
    (2,  (0, 2, 3),   (3, 0, 8),    "001"),
    (3,  (0, 2, 9),   (2, 1, 9),    "110"),
    (4,  (1, 3, 10),  (0, 5, 11),   "001"),
    (5,  (1, 7, 10),  (6, 4, 16),   "000"),
    (6,  (1, 7, 12),  (5, 7, 18),   "100"),
    (7,  (1, 9, 12),  (1, 6, 21),   "110"),
    (8,  (2, 3, 4),   (2, 9, 10),   "101"),
    (9,  (2, 4, 9),   (8, 3, 12),   "100"),
    (10, (3, 4, 11),  (8, 11, 13),  "111"),
    (11, (3, 10, 11), (4, 10, 17),  "101"),
    (12, (4, 8, 9),   (13, 9, 21),  "101"),
    (13, (4, 8, 11),  (12, 10, 19), "011"),
    (14, (5, 6, 7),   (15, 16, 18), "000"),
    (15, (5, 6, 11),  (14, 17, 19), "110"),
    (16, (5, 7, 10),  (14, 17, 5),  "010"),
    (17, (5, 10, 11), (16, 15, 11), "111"),
    (18, (6, 7, 12),  (14, 20, 6),  "001"),
    (19, (6, 8, 11),  (20, 15, 13), "010"),
    (20, (6, 8, 12),  (19, 18, 21), "011"),
    (21, (8, 9, 12),  (12, 20, 7),  "111"),
]

FACES = [pts for _, pts, _, _ in TABLE]


def main():
    points = sorted({p for f in FACES for p in f})
    assert [j for j, *_ in TABLE] == list(range(22)), "face indices are 0..21 in order"
    print(f"points: {len(points)} (claim 13)  faces: {len(FACES)} (claim 22)")

    # incidence graph H: vertex ("p", i) for points, ("f", j) for faces
    edges = [(("p", i), ("f", j)) for j, f in enumerate(FACES) for i in f]
    vertices = {v for e in edges for v in e}
    print(f"H vertices: {len(vertices)} (claim 35)  edges: {len(edges)} (claim 66)")
    assert len(set(edges)) == len(edges), "no repeated incidence"

    # bipartite by construction (edges only join a point to a face); connected?
    adj = defaultdict(set)
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    seen, stack = set(), [next(iter(vertices))]
    while stack:
        v = stack.pop()
        if v in seen:
            continue
        seen.add(v)
        stack.extend(adj[v] - seen)
    print(f"connected: {len(seen) == len(vertices)}")

    # pair multiplicities
    pair_faces = defaultdict(list)
    for j, f in enumerate(FACES):
        for a, b in combinations(sorted(f), 2):
            pair_faces[(a, b)].append(j)
    mult = defaultdict(int)
    for faces in pair_faces.values():
        mult[len(faces)] += 1
    print(f"distinct point pairs covered: {len(pair_faces)} (claim 33); multiplicity histogram: {dict(mult)}")

    # the table's opposite-face columns must agree with the triples
    bad = []
    for j, (i1, i2, i3), (j12, j13, j23), _ in TABLE:
        for (a, b), claimed in (((i1, i2), j12), ((i1, i3), j13), ((i2, i3), j23)):
            others = [k for k in pair_faces[tuple(sorted((a, b)))] if k != j]
            if others != [claimed]:
                bad.append((j, (a, b), claimed, others))
    print(f"opposite-face column mismatches: {len(bad)}" + (f" {bad}" if bad else ""))

    degrees = sorted(len(adj[("p", i)]) for i in points)
    print(f"point degrees (faces per point): {degrees}")


if __name__ == "__main__":
    main()
