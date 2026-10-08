"""Check the antipodal strong-starter page and its translation overlaps.

Run: python3 -I playground/marlow/53_skew_starter_page.py
The construction is Mullin--Nemeth's for prime p=2**k*t+1 with odd t>1.
"""

def primitive_root(p):
    factors = {q for q in range(2, p) if (p-1) % q == 0 and
               all(q % d for d in range(2, int(q**0.5)+1))}
    for g in range(2, p):
        if all(pow(g, (p-1)//q, p) != 1 for q in factors):
            return g
    raise ValueError(p)


def page(p):
    assert p > 5 and all(p % d for d in range(2, int(p**0.5)+1))
    n = p-1
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    t = n
    assert t > 1
    A = 2**(k-1)
    g = primitive_root(p)
    a = pow(g, A, p)
    H = {pow(g, 2*i*A+j, p) for i in range(t) for j in range(A)}
    S = {frozenset((x, a*x % p)) for x in H}
    minus_S = {frozenset((-x % p for x in e)) for e in S}
    assert len(S) == len(minus_S) == (p-1)//2
    assert S.isdisjoint(minus_S)
    E = S | minus_S
    assert len(E) == p-1
    assert set().union(*E) == set(range(1, p))
    assert {min((x-y) % p, (y-x) % p) for x,y in map(tuple,S)} == set(range(1,(p+1)//2))
    M = {(sum(e)*pow(2,-1,p)) % p for e in S}
    assert len(M) == len(S) and 0 not in M
    assert M.isdisjoint({-m % p for m in M})
    assert M | {-m % p for m in M} == set(range(1,p))
    neighbors = {x:set() for x in range(1,p)}
    for e in E:
        x,y = tuple(e)
        neighbors[x].add(y)
        neighbors[y].add(x)
    assert all(len(v)==2 for v in neighbors.values())
    unseen = set(neighbors)
    sizes = []
    while unseen:
        seed = min(unseen)
        stack = [seed]
        component = set()
        while stack:
            x = stack.pop()
            if x in component:
                continue
            component.add(x)
            stack.extend(neighbors[x]-component)
        unseen -= component
        sizes.append(len(component))
    assert sorted(sizes) == [2*t]*A
    for shift in range(1,p):
        moved = {frozenset((x+shift)%p for x in e) for e in E}
        assert len(E & moved) == 1, (p, shift)
    return {'p':p,'g':g,'k':k,'t':t,'components':sorted(sizes)}


if __name__ == '__main__':
    for p in (7, 11, 13, 19, 23, 29, 31, 37, 41, 43, 53, 73, 97):
        print(page(p))
