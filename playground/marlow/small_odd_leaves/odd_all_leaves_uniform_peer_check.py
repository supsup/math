"""Independent literal spoke replay for the proposed all-odd-leaf weave surgery.

Uses no imports, including from a producer or prior checker.
"""


class Counter(dict):
    def __init__(self, items=()):
        super().__init__()
        if isinstance(items, dict):
            self.update(items)
        else:
            for item in items:
                self[item] = self.get(item, 0) + 1

    def __missing__(self, key):
        return 0


class defaultdict(dict):
    def __init__(self, factory):
        super().__init__()
        self.factory = factory

    def __missing__(self, key):
        value = self.factory()
        self[key] = value
        return value


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def selected_pairs(lam, n):
    if n % 2:
        return [(s, s) for s in range(lam)]
    a = n // 2
    sigma = {j: (j + a - 1) % (n - 1) for j in range(n - 1)}
    inverse = {s: j for j, s in sigma.items()}
    require(len(inverse) == n - 1, 'sigma is not injective')
    return [(inverse[s], s) for s in range(lam)]


def check_cycle(edges, p, t, label):
    require(len(edges) >= 4 and len(edges) % 2 == 0, f'{label}: bad length')
    require(len(set(edges)) == len(edges), f'{label}: repeated spoke')
    hubs = {h for h, _ in edges}
    leaves = {l for _, l in edges}
    require(len(hubs) == len(leaves) == len(edges) // 2, f'{label}: repeated vertex or wrong side sizes')
    require(all(0 <= h < p and 0 <= l < t for h, l in edges), f'{label}: bad labels')
    nbr_h = defaultdict(set)
    nbr_l = defaultdict(set)
    for h, l in edges:
        nbr_h[h].add(l)
        nbr_l[l].add(h)
    require(all(len(v) == 2 for v in nbr_h.values()), f'{label}: hub degree')
    require(all(len(v) == 2 for v in nbr_l.values()), f'{label}: leaf degree')
    seen_h = set(); seen_l = set(); stack = [('h', next(iter(hubs)))]
    while stack:
        side, node = stack.pop()
        seen = seen_h if side == 'h' else seen_l
        if node in seen:
            continue
        seen.add(node)
        if side == 'h':
            stack.extend(('l', l) for l in nbr_h[node])
        else:
            stack.extend(('h', h) for h in nbr_l[node])
    require(seen_h == hubs and seen_l == leaves, f'{label}: disconnected')
    return len(hubs)


def check_case(lam, r):
    t = 2*lam + 1
    m = t-1
    n = lam+r
    q = 2*n
    p = q+1
    z = m
    u = q
    pairs = selected_pairs(lam, n)
    require(len(pairs) == lam, 'pair count')
    require(len({j for j, _ in pairs}) == lam, 'repeated row')
    require({s for _, s in pairs} == set(range(lam)), 'column coverage')
    require(len({(j+s) % n for j, s in pairs}) == lam, 'hub-pair collision')
    require(all(0 <= j < n for j, _ in pairs), 'row range')
    chosen = dict(pairs)
    cycle_parts = []
    singleton_parts = Counter((h, z) for h in range(q))
    singleton_parts[(u, z)] += 1
    lengths = Counter()
    for j in range(n):
        H = [(2*j+k) % q for k in range(m)]
        require(len(set(H)) == m, f'case {(lam,r)} row {j} repeats hub')
        edges = {(H[k], k) for k in range(m)} | {(H[(k+1) % m], k) for k in range(m)}
        require(len(edges) == 2*m, 'original weave cycle duplicate')
        if j in chosen:
            s = chosen[j]
            a = 2*s
            b = a+1
            old_a = (H[a], a)
            old_b = (H[b], b)
            require(old_a in edges and old_b in edges, 'cut edge missing')
            edges.remove(old_a)
            edges.remove(old_b)
            singleton_parts[old_a] += 1
            singleton_parts[old_b] += 1
            for spoke in ((H[a], z), (H[b], z)):
                require(singleton_parts[spoke] == 1, 'reused old-hub z singleton')
                singleton_parts[spoke] -= 1
            edges.update(((H[a], z), (H[b], z), (u, a), (u, b)))
        length = check_cycle(edges, p, t, f'lam={lam},r={r},j={j}')
        lengths[length] += 1
        cycle_parts.extend(edges)
    require(lengths == Counter({t:lam, t-1:r}), f'{(lam,r)} lengths {lengths}')
    require(all(v == 1 for v in singleton_parts.values() if v), 'singleton multiplicity')
    all_cycle = Counter(cycle_parts)
    require(all(v == 1 for v in all_cycle.values()), 'cycle spoke multiplicity')
    require(not (set(all_cycle) & {e for e, v in singleton_parts.items() if v}), 'singleton/cycle overlap')
    universe = {(h, l) for h in range(p) for l in range(t)}
    support = set(all_cycle) | {e for e, v in singleton_parts.items() if v}
    require(support == universe, f'{(lam,r)} missing/extra spokes')
    singles = {e for e, v in singleton_parts.items() if v}
    require(Counter(h for h, _ in singles) == Counter({h:1 for h in range(p)}), 'not one singleton/hub')
    require(Counter(l for _, l in singles) == Counter({z:2*r+1, **{l:1 for l in range(m)}}), 'singleton leaves')
    require(n == (lam*p+t-1)//t, 'not sharp cycle count')
    require(p+n == p+(lam*p+t-1)//t, 'not sharp pieces')
    return p, t, n, len(support)


def main():
    cases = 0
    for lam in range(1, 26):
        for r in range(1, 2*lam+1):
            check_case(lam, r)
            cases += 1
    for lam in (32, 64, 128):
        for r in (1, 2, lam, 2*lam-1, 2*lam):
            result = check_case(lam, r)
            print('large',result)
            cases += 1
    print('PASS', cases, 'literal seed cases; all cycles simple and all spokes partitioned')

if __name__ == '__main__':
    main()
