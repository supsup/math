"""Exact full-partition replay of several four-component page pairs."""
from collections import defaultdict
from itertools import combinations
from math import isqrt

def components(edges):
    adj=defaultdict(set)
    for h,l in edges:
        adj[('h',h)].add(('l',l));adj[('l',l)].add(('h',h))
    assert adj and all(len(ns)==2 for ns in adj.values())
    unseen=set(adj); out=[]
    while unseen:
        todo=[unseen.pop()]; hubs=set()
        while todo:
            node=todo.pop()
            if node[0]=='h':hubs.add(node[1])
            for nxt in adj[node]:
                if nxt in unseen:unseen.remove(nxt);todo.append(nxt)
        out.append(hubs)
    return out

def factors(n):
    out=[]; d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out

def primitive_root(p):
    return next(g for g in range(2,p) if all(pow(g,(p-1)//r,p)!=1 for r in factors(p-1)))

def is_tree(edges):
    parent=list(range(4))
    def root(x):
        while parent[x]!=x:x=parent[x]
        return x
    for a,b in edges:
        a,b=root(a),root(b)
        if a==b:return False
        parent[a]=b
    return len({root(i) for i in range(4)})==1

def replay(p,j=4,fixed_w=None):
    assert p%16==9 and all(p%d for d in range(2,isqrt(p)+1)) and j%2==0
    k=(p-1)//2; assert 2<=j<=k-1
    g=primitive_root(p);a=pow(g,4,p);q=(p-1)//8
    half={pow(g,8*i+s,p) for i in range(q) for s in range(4)}
    S={frozenset((z,a*z%p)) for z in half}
    T={frozenset((-z%p for z in e)) for e in S}
    assert len(S)==len(T)==k and not S&T
    colors=[set() for _ in range(k)];slots={};inv2=pow(2,-1,p)
    for h1,h2 in combinations(range(p),2):
        d=min((h1-h2)%p,(h2-h1)%p)-1
        leaf=(h1+h2)*inv2%p
        colors[d].update(((h1,leaf),(h2,leaf)))
        slots[h1,h2]=(d,leaf)
    singles={(h,h) for h in range(p)}
    for step in range(j):
        center=step+1;page=set()
        for side,matching in enumerate((S,T)):
            fresh=p+2*step+side
            for edge in matching:
                h1,h2=sorted((z+center)%p for z in edge)
                d,old=slots[h1,h2]
                assert {(h1,old),(h2,old)}<=colors[d]
                colors[d]-={(h1,old),(h2,old)}
                colors[d]|={(h1,fresh),(h2,fresh)}
                page|={(h1,old),(h2,old)}
                slots[h1,h2]=(d,fresh)
        colors.append(page)
        singles|={(center,p+2*step),(center,p+2*step+1)}
    assert all(len(components(page))==1 for page in colors[:k])
    assert all(len(components(page))==4 for page in colors[k:])
    beta=(1+a)*inv2%p;gamma=beta*pow(a,-1,p)%p;delta=(1-a)*pow(1+a,-1,p)%p
    quartic=pow(g,(p-1)//4,p)
    label_map={1:0,quartic:1,p-1:2,(-quartic)%p:3}
    def label(x):
        x%=p
        return None if x==0 else label_map[pow(x,(p-1)//4,p)]
    selected=[]
    for c in range(1,j,2):
        page1,page2=colors[k+c-1],colors[k+c]
        cand=[]
        for w in range(p):
            v=(c+w)%p;u=(v+delta)%p
            x=(c+beta*(u-c))%p;y=(c+gamma*(v-c))%p
            assert x==(c+1+beta*(v-c-1))%p
            assert y==(c+1+gamma*(u-c-1))%p
            old1={(u,x),(v,y)};old2={(u,y),(v,x)}
            if len(old1)!=2 or len(old2)!=2 or not old1<=page1 or not old2<=page2:continue
            l1=(label(u-c),label(v-c));l2=(label(u-c-1),label(v-c-1))
            if None in l1 or None in l2 or l1[0]==l1[1] or l2[0]==l2[1]:continue
            cand.append((w,u,v,tuple(sorted(l1)),tuple(sorted(l2)),old1,old2))
        triple=None
        if fixed_w is not None:
            by_w={row[0]:row for row in cand}
            assert all(w in by_w for w in fixed_w),(p,c,fixed_w)
            triple=tuple(by_w[w] for w in fixed_w)
            assert len({h for row in triple for h in row[1:3]})==6
            assert is_tree([row[3] for row in triple]) and is_tree([row[4] for row in triple])
        else:
            for i,x in enumerate(cand):
                for y in cand[i+1:]:
                    if len({x[1],x[2],y[1],y[2]})!=4:continue
                    if x[3]==y[3] or x[4]==y[4]:continue
                    for z in cand:
                        if len({x[1],x[2],y[1],y[2],z[1],z[2]})!=6:continue
                        if is_tree([x[3],y[3],z[3]]) and is_tree([x[4],y[4],z[4]]):
                            triple=(x,y,z);break
                    if triple:break
                if triple:break
        assert triple is not None,(p,c,len(cand))
        for row in triple:
            before=(len(components(page1)),len(components(page2)))
            assert row[5]<=page1 and row[6]<=page2
            page1-=row[5];page1|=row[6]
            page2-=row[6];page2|=row[5]
            after=(len(components(page1)),len(components(page2)))
            assert after==(before[0]-1,before[1]-1),(p,c,row[0],before,after)
        selected.append((c,tuple(row[0] for row in triple),len(cand)))
    assert all(len(components(page))==1 for page in colors)
    seen=set(singles)
    assert len(seen)==p+2*j
    for page in colors:
        assert not seen&page
        seen|=page
    assert seen=={(h,l) for h in range(p) for l in range(p+2*j)}
    assert len(singles)+len(colors)==p+2*j+k+j
    print('PASS',p,'j',j,'g',g,'selected',selected,'parts',len(singles)+len(colors))

if __name__=='__main__':
    for p,j in [(41,4),(73,4)]:replay(p,j)
    replay(41,18,(9,19,36))
    replay(73,34,(8,17,22))
