from math import isqrt

def prime(n):return n>1 and all(n%d for d in range(2,isqrt(n)+1))
def root(p):
 for g in range(2,p):
  if len({pow(g,e,p) for e in range(p-1)})==p-1:return g
 raise AssertionError(p)
def page_pair(p,g):
 a=g*g%p;u=(p-1)//4
 half={pow(g,e,p) for i in range(u) for e in (4*i,4*i+1)}
 S=[{frozenset((x,a*x%p)) for x in half}]
 S.append({frozenset((-x%p for x in edge)) for edge in S[0]})
 edge1={frozenset(((x+1)%p for x in edge)):side for side,part in enumerate(S) for edge in part}
 edge2={frozenset(((x+2)%p for x in edge)):side for side,part in enumerate(S) for edge in part}
 assert len(edge1)==len(edge2)==p-1
 common=set(edge1)&set(edge2)
 assert len(common)==1
 inv2=pow(2,-1,p)
 P1={(x,(sum(edge)*inv2)%p) for edge in edge1 for x in edge}
 P2={(x,p+edge1[edge] if edge in common else (sum(edge)*inv2)%p) for edge in edge2 for x in edge}
 assert len(P1)==len(P2)==2*(p-1)
 return P1,P2,common

def scan(p):
 g=root(p);a=g*g%p;iv=lambda z:pow(z%p,-1,p)
 beta=(1+a)*iv(2)%p; gamma=beta*iv(a)%p
 delta=(1-a)*iv(1+a)%p
 P1,P2,common=page_pair(p,g)
 ready=[]
 for v in range(p):
  u=(v+delta)%p
  if u in (1,2) or v in (1,2) or u==v:continue
  x=(1+beta*(u-1))%p;y=(1+gamma*(v-1))%p
  if x==y:continue
  if not {(u,x),(v,y)}<=P1 or not {(u,y),(v,x)}<=P2:continue
  chi=lambda z:pow(z%p,(p-1)//2,p)
  if chi((u-1)*(v-1))!=p-1 or chi((u-2)*(v-2))!=p-1:continue
  ready.append((u,v,x,y))
 return g,a,delta,len(ready),ready[0] if ready else None

if __name__=='__main__':
 results={p:scan(p) for p in range(13,1001,8) if prime(p)}
 print('total',len(results),'positive',sum(row[3]>0 for row in results.values()))
 print('misses',[p for p,row in results.items() if row[3]==0])
 print('first_examples',[(p,results[p]) for p in (13,29,37,53,61,101)])
 print('min_count',min(row[3] for p,row in results.items() if p>=29),'max_count',max(row[3] for row in results.values()))
 print('counts',[(p,row[3]) for p,row in results.items()])
