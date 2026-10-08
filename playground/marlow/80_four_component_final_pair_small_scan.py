"""Finite exploratory scan of the maximal pair criterion, p=9 mod16."""
from math import isqrt

def prime(p):return p>1 and all(p%d for d in range(2,isqrt(p)+1))
def factors(n):
    out=[];d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out
def root(p):
    return next(g for g in range(2,p) if all(pow(g,(p-1)//q,p)!=1 for q in factors(p-1)))
def tree(edges):
    parent=list(range(4))
    def find(x):
        while parent[x]!=x:x=parent[x]
        return x
    for u,v in edges:
        u,v=find(u),find(v)
        if u==v:return False
        parent[u]=v
    return len({find(i) for i in range(4)})==1
def run(p):
    g=root(p);a=pow(g,4,p);D=(a+1)%p;invD=pow(D,-1,p)
    delta=(1-a)*invD%p;beta=D*pow(2,-1,p)%p;gamma=beta*pow(a,-1,p)%p
    k=(p-1)//2;c=k-2
    E={((a-q)*invD)%p for q in range(c+1)}|{(a*(1-q)*invD)%p for q in range(c+1)}
    i=pow(g,(p-1)//4,p);chars={1:0,i:1,p-1:2,(-i)%p:3}
    def label(x):
        x%=p
        return None if x==0 else chars[pow(x,(p-1)//4,p)]
    cand=[]
    for w in range(p):
        if w in E:continue
        u=(w+delta)%p;v=w
        x=beta*u%p;y=gamma*v%p
        if x==y:continue
        l1=(label(u),label(v));l2=(label(u-1),label(v-1))
        if None in l1 or None in l2 or l1[0]==l1[1] or l2[0]==l2[1]:continue
        cand.append((w,u,v,tuple(sorted(l1)),tuple(sorted(l2))))
    for i,x in enumerate(cand):
        for y in cand[i+1:]:
            if len({x[1],x[2],y[1],y[2]})!=4 or x[3]==y[3] or x[4]==y[4]:continue
            for z in cand:
                if len({x[1],x[2],y[1],y[2],z[1],z[2]})!=6:continue
                if tree([x[3],y[3],z[3]]) and tree([x[4],y[4],z[4]]):
                    return g,len(cand),(x[0],y[0],z[0])
    return g,len(cand),None

if __name__=='__main__':
    count=0;miss=[];least=10**9
    for p in range(9,10001,16):
        if not prime(p):continue
        count+=1;g,n,w=run(p);least=min(least,n)
        if w is None:miss.append((p,n))
        print(p,'g',g,'candidates',n,'triple',w)
    print('SUMMARY',count,'miss',miss,'least_candidates',least)
