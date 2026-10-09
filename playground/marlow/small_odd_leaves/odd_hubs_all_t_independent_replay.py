"""Independent bounded full-partition replay for the odd-hub all-t corollary."""
from collections import Counter, defaultdict


def edges_of_walk(hubs, leaves):
    n=len(hubs)
    assert n==len(leaves)>=2
    assert len(set(hubs))==n and len(set(leaves))==n
    return [(hubs[i],leaves[i]) for i in range(n)]+[(hubs[(i+1)%n],leaves[i]) for i in range(n)]


def square(t):
    singles=[(h,h) for h in range(t)]
    cycles=[]
    for a in range((t-1)//2):
        hubs=[(-i)%t for i in range(t)]
        leaves=[(2*a+1-i)%t for i in range(t)]
        cycles.append(edges_of_walk(hubs,leaves))
    return singles,cycles


def seed(t,r):
    if r==0:return square(t)
    lam=(t-1)//2;n=lam+r;q=2*n;m=t-1;z=m;u=q
    if n%2:
        rows={s:s for s in range(lam)}
    else:
        a=n//2
        inv={(j+a-1)%(n-1):j for j in range(n-1)}
        rows={inv[s]:s for s in range(lam)}
    selected=[];cycles=[]
    for j in range(n):
        hubs=[(2*j+i)%q for i in range(m)]
        c=edges_of_walk(hubs,list(range(m)))
        if j in rows:
            s=rows[j]
            for k in (2*s,2*s+1):
                h=hubs[k]
                c.remove((h,k))
                c.extend(((h,z),(u,k)))
                selected.append((h,k))
        cycles.append(c)
    sel_hubs={h for h,k in selected}
    assert len(sel_hubs)==m
    singles=selected+[(h,z) for h in range(q) if h not in sel_hubs]+[(u,z)]
    return singles,cycles


def odd_big(P,T):
    assert P>=T>=3 and P%2 and T%2
    delta=(P-T)//2
    blocks, r=divmod(delta,T)
    singles,cycles=seed(T,r)
    offset=T+2*r
    for unused in range(2*blocks):
        ss,cc=square(T)
        singles.extend((h+offset,l) for h,l in ss)
        cycles.extend([[(h+offset,l) for h,l in c] for c in cc])
        offset+=T
    assert offset==P
    return singles,cycles


def even_small(p,t):
    M=(p-1)//2;n=t//2
    assert 1<=n<=M
    singles=[(0,l) for l in range(t)]
    cycles=[]
    for c in range(M):
        edge_list=[]
        for j in range(n):
            e=1+(c+j)%M
            o=1+M+(c+j)%M
            edge_list.extend(((e,2*j),(e,2*j+1),(o,2*j+1),(o,2*((j+1)%n))))
        cycles.append(edge_list)
    return singles,cycles


def even_large_base(p,t):
    assert p%2 and t%2==0 and p-1<=t<=2*p-2
    k=(p-1)//2; a=t//2
    singles=[(0,l) for l in range(t)]
    cycles=[]
    for j in range(a):
        hubs=[1+i for i in range(2*k)]
        leaves=[(2*j+i)%t for i in range(2*k)]
        cycles.append(edges_of_walk(hubs,leaves))
    return singles,cycles


def large_odd(p,t):
    ss,cc=odd_big(t,p)
    return [(l,h) for h,l in ss],[[(l,h) for h,l in c] for c in cc]


def build(p,t):
    assert p>=1 and p%2 and t>=1
    if p==1:return [(0,l) for l in range(t)],[]
    if t==1:return [(h,0) for h in range(p)],[]
    if t%2:
        return odd_big(p,t) if t<=p else large_odd(p,t)
    if t<p-1:
        return even_small(p,t)
    if t<=2*p-2:
        return even_large_base(p,t)
    t0=t-p
    ss,cc=large_odd(p,t0)
    add_s,add_c=square(p)
    ss.extend((h,l+t0) for h,l in add_s)
    cc.extend([[(h,l+t0) for h,l in c] for c in add_c])
    return ss,cc


def sharp_count(p,t):
    if p==1:return t
    k=(p-1)//2
    if t%2 and t<p:return p+(p*(t-1)//(2*t)+(p*(t-1)%(2*t)!=0))
    if t%2==0 and t<p-1:return t+k
    return t+(k*t+p-1)//p


def check(p,t):
    singles,cycles=build(p,t)
    assert len(singles)+len(cycles)==sharp_count(p,t),(p,t,'count',len(singles),len(cycles),sharp_count(p,t))
    used=Counter(singles)
    for ci,c in enumerate(cycles):
        assert len(c)%2==0 and len(c)>=4
        adj=defaultdict(set)
        for h,l in c:
            assert 0<=h<p and 0<=l<t
            adj[('h',h)].add(('l',l));adj[('l',l)].add(('h',h))
            used[h,l]+=1
        assert len(adj)==len(c) and all(len(v)==2 for v in adj.values()),(p,t,ci,'degree')
        stack=[next(iter(adj))];visited=set()
        while stack:
            v=stack.pop()
            if v in visited:continue
            visited.add(v);stack.extend(adj[v]-visited)
        assert len(visited)==len(adj),(p,t,ci,'connectivity')
    assert used==Counter((h,l) for h in range(p) for l in range(t)),(p,t,'edge partition')


if __name__=='__main__':
    cases=0
    for p in range(1,32,2):
        for t in range(1,4*p+1):
            check(p,t);cases+=1
    print('PASS',cases,'full odd-hub partitions: odd p=1..31, all t=1..4p')
