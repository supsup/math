"""Independent bounded line-parameter scan for p=9 (mod 16), p<300000.

The program examines v=0..min(p,80)-1; if it finds 3 compatible
page-to-page rectangles at every eligible prime, that bounded search
itself is a finite certificate. It does not import repository code.
"""
from math import isqrt

LIMIT=300000

def is_prime(p):
    return p>1 and all(p%d for d in range(2,isqrt(p)+1))

def prime_factors(n):
    out=[];d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out

def primitive_root(p):
    n=p-1;fs=prime_factors(n)
    for g in range(2,p):
        if all(pow(g,n//r,p)!=1 for r in fs):return g
    raise AssertionError(p)

def connected(edges):
    parent=list(range(4))
    def root(x):
        while parent[x]!=x:x=parent[x]
        return x
    for a,b in edges:
        x,y=root(a),root(b)
        if x==y:return False
        parent[x]=y
    return len({root(x) for x in range(4)})==1

def find(p,cap=80):
    g=primitive_root(p);a=pow(g,4,p)
    inv=lambda x:pow(x%p,-1,p)
    beta=(1+a)*inv(2)%p;gamma=beta*inv(a)%p
    delta=(1-a)*inv(1+a)%p
    overlap={(a+2)*inv(1+a)%p,(2*a+1)*inv(1+a)%p}
    i=pow(g,(p-1)//4,p)
    chars={1:0,i:1,p-1:2,(-i)%p:3}
    def label(x):
        x%=p
        return None if x==0 else chars[pow(x,(p-1)//4,p)]
    candidates=[]
    for v in range(min(p,cap)):
        u=(v+delta)%p
        if u in overlap or v in overlap:continue
        x=(1+beta*(u-1))%p
        y=(1+gamma*(v-1))%p
        assert x==(2+beta*(v-2))%p
        assert y==(2+gamma*(u-2))%p
        if u==v or x==y:continue
        c1=label(u-1),label(v-1)
        c2=label(u-2),label(v-2)
        if None in c1 or None in c2 or c1[0]==c1[1] or c2[0]==c2[1]:continue
        candidates.append((v,u,tuple(sorted(c1)),tuple(sorted(c2))))
    # The first 80 values usually yield many choices. Search all triples
    # adaptively and stop at the first pair of quotient spanning trees.
    def forest_ok(edges):
        parent=list(range(4))
        def root(x):
            while parent[x]!=x:x=parent[x]
            return x
        for a,b in edges:
            x,y=root(a),root(b)
            if x==y:return False
            parent[x]=y
        return True
    for i,c in enumerate(candidates):
        e1=[c[2]];e2=[c[3]]
        used={c[1],(c[0])}
        for d in candidates[i+1:]:
            if d[0] in used or d[1] in used or not forest_ok(e1+[d[2]]) or not forest_ok(e2+[d[3]]):continue
            used2=used|{d[0],d[1]}
            for e in candidates:
                if e[0] in used2 or e[1] in used2:continue
                if connected(e1+[d[2],e[2]]) and connected(e2+[d[3],e[3]]):
                    return g,[c,d,e]
    return g,None

if __name__=='__main__':
    count=0;miss=[];maxv=0
    digest=14695981039346656037
    def hash32(value):
        global digest
        for byte in value.to_bytes(4,'little'):
            digest^=byte
            digest=(digest*1099511628211)&((1<<64)-1)
    for p in range(9,LIMIT,16):
        if not is_prime(p):continue
        count+=1
        g,rows=find(p)
        if rows is None:miss.append(p)
        else:
            maxv=max(maxv,max(r[0] for r in rows))
            for value in (p,g,*(r[0] for r in rows)):hash32(value)
        if count%500==0:print('progress',count,p,'misses',len(miss),flush=True)
    print('primes',count,'misses',miss,'max_v',maxv,'fnv64',f'{digest:016x}')
