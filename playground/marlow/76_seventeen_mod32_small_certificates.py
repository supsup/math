#!/usr/bin/env python3
"""Full-spoke first-base certificates at p=241,337,401,433.

Run: python3 -I playground/marlow/76_seventeen_mod32_small_certificates.py --verify-four
The default exploratory probe is separate from the four saved certificates.
"""
from collections import Counter, defaultdict
from math import gcd, isqrt
import argparse

LIMIT = 32_768_001

# The order here is the quotient-tree order used by the replay.
FOUR_CERTIFICATES={
    241:(7,(2,5,13,35,1,4,19)),
    337:(10,(5,19,3,7,11,35,2)),
    401:(3,(7,1,15,2,19,4,38)),
    433:(94,(8,2,10,14,4,1,7)),
}

def factors(n):
    out = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d = 3 if d == 2 else d + 2
    if n > 1: out.append(n)
    return out

def isprime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    for d in range(3,isqrt(n)+1,2):
        if n % d == 0: return False
    return True

def primitive_root(p):
    fs=factors(p-1)
    for g in range(2,p):
        if all(pow(g,(p-1)//f,p)!=1 for f in fs): return g
    raise AssertionError(p)

def valid_a(p,a):
    inv=lambda x:pow(x%p,-1,p)
    z=(1+3*a)*inv((a-1)**2)%p
    w=a*(a+3)*inv((a-1)**2)%p
    if not z or not w or pow(w*inv(z)%p,(p-1)//2,p)!=p-1:
        return False,z,w
    b=(1+z)%p;v=(1+w)%p
    half=inv(2)
    mu=lambda d:d*(1+a)*half*inv(a-1)%p
    s1={(b-half)%p,(b+half)%p,(b+3*half)%p,(v+half)%p}
    s3={(b-half)%p,(b+3*half)%p}
    if s1&{(1-mu(1))%p,(1+mu(1))%p}: return False,z,w
    if s3&{(1-mu(3))%p,(1+mu(3))%p}: return False,z,w
    return True,z,w

def cases():
    A=4
    while 6*A+1 <= LIMIT:
        qmax=min(6*(A-2), (LIMIT-1)//(2*A))
        for q in range(3,qmax+1,2):
            p=2*A*q+1
            if isprime(p): yield p,A,q
        A*=2

def analyze():
    rows=[]
    for p,A,q in cases():
        g=primitive_root(p)
        a0=pow(g,A,p)
        good=[]
        for e in range(1,2*q,2):
            if gcd(e,q)>1: continue
            a=pow(a0,e,p)
            yes,z,w=valid_a(p,a)
            if yes: good.append((e,a,z,w))
        rows.append((p,A,q,g,good))
    return rows

def options(p,A,q,g,a,z,w):
    """Group scales by their unordered quotient edge; local templates checked."""
    logs={pow(g,e,p):e%A for e in range(p-1)}
    inv2=pow(2,-1,p)
    b=(1+z)%p;v=(1+w)%p
    page=((b,(v+inv2)%p),(v,(b+inv2)%p))
    buckets=defaultdict(list)
    for lam in range(1,p):
        u=logs[lam*z%p]; t=logs[lam*w%p]
        edge=tuple(sorted((u,t)))
        if edge[0]==edge[1]: raise AssertionError((p,A,q,g,a,z,w))
        colors=frozenset((min(lam,p-lam),min(3*lam%p,-3*lam%p)))
        if len(colors)!=2: continue
        transform=lambda x:(1+lam*(x-1))%p
        spokes=frozenset((transform(h),transform(l)) for h,l in page)
        assert len(spokes)==2
        buckets[edge].append((lam,colors,spokes))
    assert len(buckets)==A
    assert all(len(xs)==2*q for xs in buckets.values())
    return buckets

def find_tree(buckets,A,node_limit=2_000_000):
    """Backtrack over one deleted edge of the A-cycle; return witness or status."""
    edges=sorted(buckets)
    nodes=0
    for deleted in edges:
        todo=[e for e in edges if e!=deleted]
        # A-cycle minus an edge is a spanning tree.
        for ordering in (todo,):
            chosen=[]; used_colors=set();used_spokes=set()
            def dfs(i):
                nonlocal nodes
                nodes+=1
                if nodes>node_limit: raise TimeoutError
                if i==len(ordering): return list(chosen)
                edge=ordering[i]
                for lam,cs,ss in buckets[edge]:
                    if used_colors.isdisjoint(cs) and used_spokes.isdisjoint(ss):
                        chosen.append((edge,lam))
                        used_colors.update(cs);used_spokes.update(ss)
                        ans=dfs(i+1)
                        if ans is not None:return ans
                        chosen.pop();used_colors.difference_update(cs);used_spokes.difference_update(ss)
                return None
            try: result=dfs(0)
            except TimeoutError:return 'node-limit',nodes
            if result is not None:return result,nodes
    return None,nodes

def graph_components(edges):
    adj=defaultdict(set)
    for h,l in edges:
        adj[(0,h)].add((1,l));adj[(1,l)].add((0,h))
    assert all(len(v)==2 for v in adj.values())
    unseen=set(adj); count=0
    while unseen:
        count+=1; stack=[unseen.pop()]
        while stack:
            for v in adj[stack.pop()]:
                if v in unseen:
                    unseen.remove(v);stack.append(v)
    return count,len(adj)//2

def verify_partition(p,A,q,g,witness):
    """Rebuild all K_{p,p+2} spokes and replay every scaled rectangle."""
    assert pow(g,A,p)>1
    a=pow(g,A,p); z=(1+3*a)*pow((a-1)**2,-1,p)%p
    w=a*(a+3)*pow((a-1)**2,-1,p)%p
    assert valid_a(p,a)[0]
    k=(p-1)//2; inv2=pow(2,-1,p)
    half={pow(g,2*A*i+j,p) for i in range(q) for j in range(A)}
    sides=[]
    for sign in (1,-1):
        side={frozenset((sign*x%p,sign*a*x%p)) for x in half}
        assert len(side)==k
        sides.append(side)
    assert not sides[0]&sides[1]
    colors=[set() for _ in range(k)]; slots={}
    for d in range(1,k+1):
        for h in range(p):
            v=(h+d)%p;leaf=(h+v)*inv2%p
            key=frozenset((h,v)); assert key not in slots
            slots[key]=(d-1,leaf)
            colors[d-1].update(((h,leaf),(v,leaf)))
    page=set()
    for i,side in enumerate(sides):
        for edge in side:
            h,v=((x+1)%p for x in edge)
            ci,leaf=slots[frozenset((h,v))]
            original={(h,leaf),(v,leaf)}
            assert original<=colors[ci]
            colors[ci].difference_update(original)
            colors[ci].update(((h,p+i),(v,p+i)))
            page.update(original)
    colors.append(page)
    assert graph_components(page)[0]==A
    b=(1+z)%p;v=(1+w)%p
    prep=((b,(b-inv2)%p),((b+1)%p,(b+3*inv2)%p),
          (b,(b+3*inv2)%p),((b+1)%p,(b-inv2)%p))
    join=((b,(b+inv2)%p),(v,(v+inv2)%p),
          (b,(v+inv2)%p),(v,(b+inv2)%p))
    for j,(edge,lam) in enumerate(witness):
        transform=lambda x:(1+lam*(x-1))%p
        pre=[(transform(h),transform(l)) for h,l in prep]
        joi=[(transform(h),transform(l)) for h,l in join]
        c1=min(lam,p-lam)-1
        c3=min(3*lam%p,-3*lam%p)-1
        for ci,cj,m in ((c1,c3,pre),(c1,k,joi)):
            e1,e2,f1,f2=m
            assert {e1,e2}<=colors[ci] and {f1,f2}<=colors[cj],(p,j,edge,lam,ci,cj,m)
            colors[ci].difference_update((e1,e2));colors[ci].update((f1,f2))
            colors[cj].difference_update((f1,f2));colors[cj].update((e1,e2))
            assert graph_components(colors[ci])[0]==1
            if cj!=k:assert graph_components(colors[cj])[0]==1
        assert graph_components(page)[0]==A-j-1,(p,j,edge,lam)
    assert graph_components(page)==(1,p-1)
    seen={(h,h) for h in range(p)}|{(1,p),(1,p+1)}
    assert len(seen)==p+2
    for ci,C in enumerate(colors):
        assert graph_components(C)==(1,p-(ci==k)),(p,ci)
        assert len(C)==2*(p-(ci==k))
        assert not C&seen,(p,ci)
        seen.update(C)
    assert len(seen)==p*(p+2)
    assert len(colors)+p+2==(3*p+5)//2
    return len(seen),len(colors)+p+2

def verify_four():
    for p,(g,scales) in FOUR_CERTIFICATES.items():
        assert isprime(p)
        n=p-1; A=1<<(n & -n).bit_length()-2
        # These four cases all have p-1=16q, q odd, hence A=8.
        assert A==8 and n%(2*A)==0
        q=n//(2*A)
        assert all(pow(g,n//f,p)!=1 for f in factors(n))
        a=pow(g,A,p)
        ok,z,w=valid_a(p,a);assert ok
        bs=options(p,A,q,g,a,z,w)
        match={lam:edge for edge,xs in bs.items() for lam,_,_ in xs}
        edges=[match[lam] for lam in scales]
        assert len(set(edges))==A-1
        result=verify_partition(p,A,q,g,list(zip(edges,scales)))
        print(f'PASS p={p} g={g} A={A} q={q} scales={scales} '
              f'edges={edges} spokes={result[0]} parts={result[1]}',flush=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--max-p',type=int,default=10000)
    ap.add_argument('--max-a',type=int,default=32)
    ap.add_argument('--node-limit',type=int,default=2_000_000)
    ap.add_argument('--verify-four',action='store_true')
    args=ap.parse_args()
    if args.verify_four:
        verify_four();return
    rows=analyze();print('Total eligible primes',len(rows))
    print('By A', sorted(Counter(A for p,A,q,g,good in rows).items()))
    print('Local pass',sum(bool(good) for p,A,q,g,good in rows))
    print('Local fail',[(p,A,q) for p,A,q,g,good in rows if not good])
    for q0 in (3,5,7):
        subset=[r for r in rows if r[2]==q0 and r[1]>=8]
        print(f'q={q0} A>=8: total={len(subset)}, pass={sum(bool(r[4]) for r in subset)}')
        print(' ',[(p,A,len(good)) for p,A,q,g,good in subset])
    print('Pack probes')
    for p,A,q,g,good in rows:
        if p>args.max_p or A>args.max_a or not good: continue
        witness=None;nodes=0;root=None
        for e,a,z,w in good:
            # g^e is primitive and maps to a.
            ge=pow(g,e,p)
            bs=options(p,A,q,ge,a,z,w)
            ans,n=find_tree(bs,A,args.node_limit)
            nodes+=n
            if ans=='node-limit': witness='node-limit';root=(e,ge,a);break
            if ans is not None:witness=ans;root=(e,ge,a);break
        print((p,A,q),'good_roots',len(good),'result',witness,'root',root,'nodes',nodes,flush=True)

if __name__=='__main__':main()
