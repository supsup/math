"""Brute-force check of OAI.FiniteCongruence.graph_criterion on small instances.

Both sides are implemented from the challenge DEFINITIONS (lean/ComparatorChallenges/
FiniteCongruenceGraph.lean), not from the proof:

  A_n(L): exists an algebra on Fin n with L ~=o Congruence alg          (Representable, size n)
  B_n(L): exists color : Fin n -> Fin n -> L with IsGraphWitness color (HasGraphWitness, size n)

The theorem says (exists n>0, A_n) <-> (exists n>0, B_n). Both sides are unbounded in n, so we
check the stronger, size-matched statement A_n(L) <-> B_n(L) for every lattice L with |L| <= K
and every n <= N. Agreement for all n <= N implies agreement of the n-bounded criterion.

Usage: python3 -I enumerate.py [K] [N]   (defaults K=6, N=4)
"""
import itertools, sys, time

K = int(sys.argv[1]) if len(sys.argv) > 1 else 6
N = int(sys.argv[2]) if len(sys.argv) > 2 else 4

# ---------------------------------------------------------------- lattices up to iso
def lattice_from_leq(k, leq):
    """Return join table or None if (k, leq) is not a lattice. leq[i][j] means i <= j."""
    join = [[None] * k for _ in range(k)]
    for a in range(k):
        for b in range(k):
            ubs = [c for c in range(k) if leq[a][c] and leq[b][c]]
            least = [c for c in ubs if all(leq[c][d] for d in ubs)]
            if len(least) != 1:
                return None
            join[a][b] = least[0]
    # meets exist automatically for a finite poset with bottom and all joins; check anyway
    for a in range(k):
        for b in range(k):
            lbs = [c for c in range(k) if leq[c][a] and leq[c][b]]
            if len([c for c in lbs if all(leq[d][c] for d in lbs)]) != 1:
                return None
    return join

def canon(k, leq):
    """Canonical form: minimal leq bit-string over all relabelings."""
    best = None
    for perm in itertools.permutations(range(k)):
        s = tuple(leq[perm[i]][perm[j]] for i in range(k) for j in range(k))
        if best is None or s < best:
            best = s
    return best

def canon_fast(k, leq):
    # bottom/top are fixed by any iso; relabel so bottom=0, top=k-1, permute the interior only
    bot = next(i for i in range(k) if all(leq[i][j] for j in range(k)))
    top = next(i for i in range(k) if all(leq[j][i] for j in range(k)))
    interior = [i for i in range(k) if i not in (bot, top)]
    best = None
    for p in itertools.permutations(interior):
        order = [bot] + list(p) + ([top] if k > 1 else [])
        s = tuple(leq[order[i]][order[j]] for i in range(k) for j in range(k))
        if best is None or s < best:
            best = s
    return best

def all_lattices(k):
    """All lattices of size k up to isomorphism, as (leq, join, bot). Linear extensions: i<j
    in the order forces i<j as integers, so only upper-triangular relations are enumerated."""
    if k == 1:
        return {canon_fast(1, [[True]]): ([[True]], [[0]], 0)}
    found = {}
    pairs = [(i, j) for i in range(1, k - 1) for j in range(i + 1, k - 1)]
    for bits in range(1 << len(pairs)):
        leq = [[i == j for j in range(k)] for i in range(k)]
        for i in range(k):
            leq[0][i] = True
            leq[i][k - 1] = True
        for t, (i, j) in enumerate(pairs):
            if bits >> t & 1:
                leq[i][j] = True
        if any(leq[a][b] and leq[b][c] and not leq[a][c]
               for a in range(k) for b in range(k) for c in range(k)):
            continue
        join = lattice_from_leq(k, leq)
        if join is None:
            continue
        c = canon_fast(k, leq)
        if c not in found:
            found[c] = (leq, join, 0)
    return found

# ---------------------------------------------------------------- side A: Representable
def partitions(n):
    """Equivalence relations on range(n) as restricted-growth label tuples."""
    out = []
    def rec(prefix, m):
        if len(prefix) == n:
            out.append(tuple(prefix)); return
        for b in range(m + 1):
            rec(prefix + [b], max(m, b + 1))
    rec([], 0)
    return out

def representable_lattices(n, K):
    """Canonical forms of Congruence(alg) for algebras on Fin n, restricted to size <= K.
    Congruence alg = equivalences compatible with every op. Compatibility with an op of
    arity a is equivalent to compatibility with all its unary translations (fix all but one
    coordinate), because rel is an equivalence (chain the coordinates one at a time). So
    Congruence(alg) = Con(U) for the set U of translations, and conversely every set U of
    self-maps is the op set of a unary algebra. Hence the attainable families are exactly the
    intersections of the families Con(f), f : n -> n (the empty intersection = all of Eq(n),
    the algebra with numOps = 0)."""
    parts = partitions(n)
    P = len(parts)
    def preserves(f, p):
        return all(p[f[x]] == p[f[y]] for x in range(n) for y in range(n) if p[x] == p[y])
    single = set()
    for f in itertools.product(range(n), repeat=n):
        mask = 0
        for i, p in enumerate(parts):
            if preserves(f, p):
                mask |= 1 << i
        single.add(mask)
    full = (1 << P) - 1
    fams = {full}
    frontier = [full]
    while frontier:
        nxt = []
        for a in frontier:
            for s in single:
                c = a & s
                if c not in fams:
                    fams.add(c); nxt.append(c)
        frontier = nxt
    refines = [[all(q[x] == q[y] for x in range(n) for y in range(n) if p[x] == p[y])
                for q in parts] for p in parts]
    result = {}
    sizes = {}
    for m in fams:
        idx = [i for i in range(P) if m >> i & 1]
        sizes[len(idx)] = sizes.get(len(idx), 0) + 1
        if len(idx) > K:
            continue
        leq = [[refines[i][j] for j in idx] for i in idx]
        assert lattice_from_leq(len(idx), leq) is not None   # Con is always a lattice
        result.setdefault(canon_fast(len(idx), leq), m)
    return result, len(fams), sizes

def check_translation_reduction(n, trials, seed=1):
    """Independent check of the reduction used in representable_lattices: for random genuine
    algebras (arities 0..3), compute Congruence(alg) straight from `Compatible` and confirm the
    resulting family is one of the intersection-closure families. Returns #algebras checked."""
    import random
    rng = random.Random(seed)
    parts = partitions(n)
    fams = None
    _, _, _ = None, None, None
    # rebuild the closure family set (all sizes)
    def preserves(f, p):
        return all(p[f[x]] == p[f[y]] for x in range(n) for y in range(n) if p[x] == p[y])
    single = set()
    for f in itertools.product(range(n), repeat=n):
        single.add(sum(1 << i for i, p in enumerate(parts) if preserves(f, p)))
    full = (1 << len(parts)) - 1
    fams = {full}; frontier = [full]
    while frontier:
        nxt = []
        for a in frontier:
            for s in single:
                c = a & s
                if c not in fams:
                    fams.add(c); nxt.append(c)
        frontier = nxt
    for _ in range(trials):
        ops = []
        for _ in range(rng.randint(0, 3)):
            ar = rng.randint(0, 3)
            table = {args: rng.randrange(n) for args in itertools.product(range(n), repeat=ar)}
            ops.append((ar, table))
        mask = 0
        for i, p in enumerate(parts):
            ok = all(p[table[l]] == p[table[r]]
                     for ar, table in ops
                     for l in itertools.product(range(n), repeat=ar)
                     for r in itertools.product(range(n), repeat=ar)
                     if all(p[a] == p[b] for a, b in zip(l, r)))
            if ok:
                mask |= 1 << i
        assert mask in fams, (n, ops)
    return trials

# ---------------------------------------------------------------- side B: HasGraphWitness
class Lat:
    def __init__(self, leq, join, bot):
        self.k = len(leq); self.leq = leq; self.join = join; self.bot = bot

def eqv_closure(n, rel_pairs):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b in rel_pairs:
        parent[find(a)] = find(b)
    return tuple(find(x) for x in range(n))

def witness_conditions(n, L, color, maps, literal_generation=False, drop=None):
    """IsGraphWitness, conjunct by conjunct. `drop` names a conjunct to omit (controls)."""
    leq, join, bot = L.leq, L.join, L.bot
    pts = range(n)
    # 1 symmetric, 2 color = bot <-> equal, 3 triangle
    if drop != 'symm' and any(color[x][y] != color[y][x] for x in pts for y in pts):
        return False
    if drop != 'bot' and any((color[x][y] == bot) != (x == y) for x in pts for y in pts):
        return False
    if drop != 'tri' and any(not leq[color[x][y]][join[color[x][z]][color[z][y]]]
                              for x in pts for y in pts for z in pts):
        return False
    # 4 separation: lower not<= upper -> exists pair with color <= lower, not <= upper
    if drop != 'sep':
        cols = {color[x][y] for x in pts for y in pts}
        for lo in range(L.k):
            for up in range(L.k):
                if not leq[lo][up] and not any(leq[c][lo] and not leq[c][up] for c in cols):
                    return False
    if drop == 'gen':
        return True
    # 5 generation. Admissible placements, read literally: color(p l, p r) <= color(l, r).
    adm = [f for f in maps if all(leq[color[f[x]][f[y]]][color[x][y]] for x in pts for y in pts)]
    ordered = [(x, y) for x in pts for y in pts]
    # images of a single seed under admissible maps = Marked pairs contributed by that seed
    img = {e: {(f[e[0]], f[e[1]]) for f in adm} for e in ordered}
    if literal_generation:
        for r in range(1, len(ordered) + 1):
            for seeds in itertools.combinations(ordered, r):
                sup = bot
                for e in seeds:
                    sup = join[sup][color[e[0]][e[1]]]
                marked = set().union(*(img[e] for e in seeds))
                cls = eqv_closure(n, marked)  # EqvGen of Marked
                if any(leq[color[x][y]][sup] and cls[x] != cls[y] for x in pts for y in pts):
                    return False
        return True
    # Equivalent fast form: the condition depends on seeds only through (sup of colors,
    # union of image sets); enumerate the reachable such pairs by closing singletons under union.
    start = {(color[e[0]][e[1]], frozenset(img[e])) for e in ordered}
    seen = set(start); frontier = list(start)
    while frontier:
        nxt = []
        for (a, A) in frontier:
            for (b, B) in start:
                c = (join[a][b], A | B)
                if c not in seen:
                    seen.add(c); nxt.append(c)
        frontier = nxt
    for sup, marked in seen:
        cls = eqv_closure(n, marked)
        if any(leq[color[x][y]][sup] and cls[x] != cls[y] for x in pts for y in pts):
            return False
    return True

def has_witness(n, L, maps, drop=None, literal_generation=False):
    return find_witness(n, L, maps, drop, literal_generation) is not None

def find_witness(n, L, maps, drop=None, literal_generation=False):
    """Exists color on Fin n. When 'symm'/'bot' are not dropped we only enumerate symmetric
    colorings with bot exactly on the diagonal (any witness has that shape)."""
    pts = range(n)
    if drop in ('symm', 'bot'):
        cells = [(x, y) for x in pts for y in pts]
        for vals in itertools.product(range(L.k), repeat=len(cells)):
            color = [[0] * n for _ in pts]
            for (x, y), v in zip(cells, vals):
                color[x][y] = v
            if witness_conditions(n, L, color, maps, literal_generation, drop):
                return color
        return None
    pairs = [(x, y) for x in pts for y in pts if x < y]
    nonbot = [c for c in range(L.k) if c != L.bot]
    for vals in itertools.product(nonbot, repeat=len(pairs)):
        color = [[L.bot] * n for _ in pts]
        for (x, y), v in zip(pairs, vals):
            color[x][y] = color[y][x] = v
        if witness_conditions(n, L, color, maps, literal_generation, drop):
            return color
    return None

def explain_generation_failure(n, L, color, maps):
    """Smallest seed set (literal Finset semantics) violating conjunct 5, with a bad pair."""
    leq, join, bot = L.leq, L.join, L.bot
    pts = range(n)
    adm = [f for f in maps if all(leq[color[f[x]][f[y]]][color[x][y]] for x in pts for y in pts)]
    ordered = [(x, y) for x in pts for y in pts]
    for r in range(1, len(ordered) + 1):
        for seeds in itertools.combinations(ordered, r):
            sup = bot
            for e in seeds:
                sup = join[sup][color[e[0]][e[1]]]
            marked = {(f[e[0]], f[e[1]]) for f in adm for e in seeds}
            cls = eqv_closure(n, marked)
            for x in pts:
                for y in pts:
                    if leq[color[x][y]][sup] and cls[x] != cls[y]:
                        return seeds, sup, (x, y), len(adm)
    return None

# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    for n in (2, 3, 4):
        print(f"translation reduction: {check_translation_reduction(n, 300)} random algebras on "
              f"Fin {n} (arity 0..3) all land in the unary-closure families")
    lats = {}
    for k in range(1, K + 1):
        ls = all_lattices(k)
        print(f"lattices of size {k}: {len(ls)}")
        for c, (leq, join, bot) in ls.items():
            lats[c] = Lat(leq, join, bot)
    names = {c: f"L{i}(|L|={L.k})" for i, (c, L) in enumerate(lats.items())}
    total = mismatches = 0
    countA = countB = 0
    controls = {'gen': [], 'sep': [], 'tri': []}
    repr_any = {c: False for c in lats}
    for n in range(1, N + 1):
        repA, nfam, sizes = representable_lattices(n, K)
        print(f"n={n}: {nfam} distinct congruence families; size histogram {dict(sorted(sizes.items()))}")
        maps = list(itertools.product(range(n), repeat=n))
        for c, L in lats.items():
            a = c in repA
            b = has_witness(n, L, maps, literal_generation=(n <= 3))
            total += 1; countA += a; countB += b
            repr_any[c] |= a
            if a != b:
                mismatches += 1
                print(f"  MISMATCH n={n} {names[c]}: A={a} B={b}")
            for d in controls:
                if n <= N and not a and has_witness(n, L, maps, drop=d):
                    controls[d].append((n, names[c], c))
        print(f"  n={n}: A true for {sum(1 for c in lats if c in repA)}/{len(lats)} lattices; "
              f"elapsed {time.time()-t0:.1f}s")
    print(f"\n(lattice, n) instances: {total}; A true {countA}; B true {countB}; mismatches {mismatches}")
    print(f"lattices representable at some n<={N}: {sum(repr_any.values())}/{len(lats)}")
    for d, hits in controls.items():
        print(f"control drop-{d}: {len(hits)} instances with weakened-B true but A false")
        for n, nm, c in hits[:6]:
            k = lats[c].k
            rel = [(i, j) for i in range(k) for j in range(k) if i != j and lats[c].leq[i][j]]
            print(f"    n={n} {nm} strict order pairs {rel}")
        if d == 'gen' and hits:
            n, nm, c = hits[0]
            L = lats[c]
            maps = list(itertools.product(range(n), repeat=n))
            color = find_witness(n, L, maps, drop='gen')
            print(f"    explicit: n={n} {nm} color matrix {color}")
            print(f"      full IsGraphWitness on it: {witness_conditions(n, L, color, maps, literal_generation=True)}")
            print(f"      failing (seeds, sup, unconnected pair, #admissible maps): "
                  f"{explain_generation_failure(n, L, color, maps)}")
    sys.exit(1 if mismatches else 0)

if __name__ == "__main__":
    main()
