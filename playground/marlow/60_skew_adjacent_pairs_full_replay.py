"""Replay every even growth prefix at six primes with exact edge checks.

Run: python3 -I playground/marlow/60_skew_adjacent_pairs_full_replay.py
"""
import sys
from collections import defaultdict
from itertools import combinations

def primitive(p):
 n=p-1;fs=[];v=n;d=2
 while d*d<=v:
  if v%d==0:
   fs.append(d)
   while v%d==0:v//=d
  d+=1
 if v>1:fs.append(v)
 return next(g for g in range(2,p) if all(pow(g,n//q,p)!=1 for q in fs))

def components(edges):
 adj=defaultdict(set)
 for a,b in edges:
  adj[('h',a)].add(('l',b));adj[('l',b)].add(('h',a))
 assert all(len(v)==2 for v in adj.values())
 unseen=set(adj);hubcomp={};sizes=[]
 while unseen:
  queue=[unseen.pop()];ci=len(sizes);nh=0
  while queue:
   node=queue.pop()
   if node[0]=='h':hubcomp[node[1]]=ci;nh+=1
   for nxt in adj[node]:
    if nxt in unseen:unseen.remove(nxt);queue.append(nxt)
  sizes.append(nh)
 return sorted(sizes),hubcomp

def initial(p):
 k=(p-1)//2;g=primitive(p);a=g*g%p;u=(p-1)//4
 half={pow(g,e,p) for i in range(u) for e in (4*i,4*i+1)}
 first={frozenset((x,a*x%p)) for x in half}
 second={frozenset((-x%p for x in edge)) for edge in first}
 assert len(first)==len(second)==k and not first&second
 C=[set() for _ in range(k)];slots={}
 for x,y in combinations(range(p),2):
  d=min((x-y)%p,(y-x)%p)-1;m=(x+y)*pow(2,-1,p)%p
  C[d].update(((x,m),(y,m)));slots[x,y]=(d,m)
 assert all(components(color)[0]==[p] for color in C)
 return g,(first,second),C,slots,{(a,a) for a in range(p)}

def grow(p,center,step,matchings,C,slots,singles):
 page=set();seen_leaves=[]
 for side,matching in enumerate(matchings):
  fresh=p+2*step+side
  for edge in matching:
   x,y=sorted((z+center)%p for z in edge)
   d,old=slots[x,y]
   assert {(x,old),(y,old)}<=C[d]
   C[d]-={(x,old),(y,old)};C[d]|={(x,fresh),(y,fresh)}
   page|={(x,old),(y,old)};seen_leaves.append(old)
   slots[x,y]=(d,fresh)
 assert len(set(seen_leaves))==p-1
 singles.update(((center,fresh) for fresh in (p+2*step,p+2*step+1)))
 assert components(page)[0]==[(p-1)//2]*2
 C.append(page)

def line_candidates(p,center,g,A,B):
 a=g*g%p;inv=lambda z:pow(z%p,-1,p)
 beta=(1+a)*inv(2)%p;gamma=beta*inv(a)%p
 delta=(1-a)*inv(1+a)%p
 ca=components(A)[1];cb=components(B)[1]
 result=[]
 for v in range(p):
  u=(v+delta)%p
  if u in (center,(center+1)%p) or v in (center,(center+1)%p):continue
  x=(center+beta*(u-center))%p;y=(center+gamma*(v-center))%p
  if x==y:continue
  e1,e2,f1,f2=(u,x),(v,y),(u,y),(v,x)
  if {e1,e2}<=A and {f1,f2}<=B and ca[u]!=ca[v] and cb[u]!=cb[v]:
   result.append((e1,e2,f1,f2))
 return result


def criterion_candidates(p,center,g):
 a=g*g%p;inv=lambda z:pow(z%p,-1,p)
 beta=(1+a)*inv(2)%p;gamma=beta*inv(a)%p
 delta=(1-a)*inv(1+a)%p
 H={(r+a*(center+1))*inv(a+1)%p for r in range(center+1)}
 L={(a*r+center)*inv(a+1)%p for r in range(1,center+2)}
 result=[]
 for v in range(p):
  if v in H or v in L:continue
  u=(v+delta)%p
  if pow((v-center)*(u-center)%p,(p-1)//2,p)!=p-1:continue
  if pow((v-center-1)*(u-center-1)%p,(p-1)//2,p)!=p-1:continue
  x=(center+beta*(u-center))%p;y=(center+gamma*(v-center))%p
  assert x!=y and u!=v
  result.append(((u,x),(v,y),(u,y),(v,x)))
 return result

def check(p,singles,C,prefix):
 k=(p-1)//2;t=p+2*prefix
 assert len(singles)==t and len(C)==k+prefix
 used=set(singles)
 for i,color in enumerate(C):
  assert len(color)==2*(p-(i>=k)) and not used&color
  used.update(color)
  assert components(color)[0]==[p-(i>=k)]
 assert used=={(a,b) for a in range(p) for b in range(t)}
 assert len(singles)+len(C)==t+(k*t+p-1)//p

def run(p):
 g,matchings,C,slots,singles=initial(p);k=(p-1)//2
 out=[]
 for prefix in range(2,k,2):
  center=prefix-1
  grow(p,center,prefix-2,matchings,C,slots,singles)
  grow(p,center+1,prefix-1,matchings,C,slots,singles)
  A,B=C[-2:]
  line=line_candidates(p,center,g,A,B)
  criterion=criterion_candidates(p,center,g)
  assert line==criterion,(p,prefix,len(line),len(criterion))
  move=criterion[0] if criterion else None
  if move is None:
   print('FAIL',p,'prefix',prefix,'line',len(line),flush=True)
   return out,False
  e1,e2,f1,f2=move
  A.difference_update((e1,e2));A.update((f1,f2))
  B.difference_update((f1,f2));B.update((e1,e2))
  check(p,singles,C,prefix)
  out.append({'prefix':prefix,'center':center,'line_count':len(line),'trade':[e1,e2,f1,f2]})
  print('PASS',p,'prefix',prefix,'line',len(line),'move',move,flush=True)
 return out,True

if __name__=='__main__':
 for p in map(int,sys.argv[1:] or (13,29,37,53,61,101)):
  out,ok=run(p)
  assert ok
  print('COMPLETE',p,len(out),'paired prefixes')
