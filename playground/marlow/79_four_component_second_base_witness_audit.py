"""Independent exact-arithmetic replay of the finite witness table."""
import csv
from hashlib import sha256
from pathlib import Path

P = Path(__file__).with_name('79_four_component_second_base_witnesses.csv')
rows = list(csv.DictReader(P.open()))
assert len(rows) == 6123

def prime(n):
    if n < 2: return False
    d=2
    while d*d<=n:
        if n%d==0: return False
        d+=1
    return True

def comp(p,g,z):
    assert z%p
    omega=pow(g,(p-1)//4,p)
    tag=pow(z%p,(p-1)//4,p)
    return next(j for j in range(4) if pow(omega,j,p)==tag)

def tree(edges):
    par=list(range(4))
    def find(a):
        while par[a]!=a: a=par[a]
        return a
    for a,b in edges:
        a,b=find(a),find(b)
        if a==b: return False
        par[a]=b
    return len({find(j) for j in range(4)})==1

for row in rows:
    p,g,a=(int(row[k]) for k in ('p','g','a'))
    assert p%16==9 and p<600000 and prime(p)
    assert pow(g,4,p)==a
    # Quartic-character image of a primitive root is enough for these labels;
    # independently check primitivity via distinct prime factors of p-1.
    n=p-1; fs=[]; d=2
    while d*d<=n:
        if n%d==0:
            fs.append(d)
            while n%d==0: n//=d
        d+=1
    if n>1:fs.append(n)
    assert all(pow(g,(p-1)//d,p)!=1 for d in fs)
    beta=(1+a)*pow(2,-1,p)%p
    gamma=beta*pow(a,-1,p)%p
    delta=(1-a)*pow(1+a,-1,p)%p
    common={(a+2)*pow(a+1,-1,p)%p,(2*a+1)*pow(a+1,-1,p)%p}
    triples=[]
    hubs=set()
    for key in ('v1','v2','v3'):
        v=int(row[key]);assert 0<=v<p
        u=(v+delta)%p
        x=(1+beta*(u-1))%p
        y=(1+gamma*(v-1))%p
        assert x==(2+beta*(v-2))%p
        assert y==(2+gamma*(u-2))%p
        assert u!=v and x!=y
        assert u not in common and v not in common
        assert u not in (1,2) and v not in (1,2)
        assert {u,v}.isdisjoint(hubs)
        hubs.update((u,v))
        e1=(comp(p,g,u-1),comp(p,g,v-1))
        e2=(comp(p,g,u-2),comp(p,g,v-2))
        assert e1[0]!=e1[1] and e2[0]!=e2[1]
        triples.append((e1,e2))
    assert tree([e[0] for e in triples])
    assert tree([e[1] for e in triples])

assert [int(r['p']) for r in rows]==[p for p in range(41,600000,16) if prime(p)]
print('PASS rows',len(rows),'sha256',sha256(P.read_bytes()).hexdigest())
print('first',[(r['p'],r['g'],r['v1'],r['v2'],r['v3']) for r in rows[:5]])
print('last',[(r['p'],r['g'],r['v1'],r['v2'],r['v3']) for r in rows[-3:]])
