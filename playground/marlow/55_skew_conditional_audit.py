"""Independent structural audit of the conditional p=5 mod 8 repair.

Checks all 42 eligible primes through 1000, and the three touched colors
at each of the 21 primes meeting the criterion. It does not materialize the
untouched square colors or an entire K_(p,p+2) edge partition.
"""

from collections import defaultdict

def prime(p):return p>1 and all(p%d for d in range(2,int(p**0.5)+1))
def root(p):
 for g in range(2,p):
  if len({pow(g,e,p) for e in range(p-1)})==p-1:return g
 raise AssertionError(p)
def parts(spokes):
 adj=defaultdict(set)
 for a,b in spokes:
  adj[('h',a)].add(('l',b));adj[('l',b)].add(('h',a))
 assert all(len(v)==2 for v in adj.values())
 unseen=set(adj);hub_sizes=[]
 while unseen:
  stack=[unseen.pop()];hubs=leaves=0
  while stack:
   v=stack.pop()
   if v[0]=='h':hubs+=1
   else:leaves+=1
   for w in adj[v]:
    if w in unseen:unseen.remove(w);stack.append(w)
  assert hubs==leaves
  hub_sizes.append(hubs)
 return sorted(hub_sizes)
def swap(A,B,old1,old2,new1,new2):
 assert old1!=old2 and new1!=new2
 assert {old1,old2}<=A and {new1,new2}<=B
 assert new1 not in A and new2 not in A and old1 not in B and old2 not in B
 A.difference_update((old1,old2));A.update((new1,new2))
 B.difference_update((new1,new2));B.update((old1,old2))

counts={};checked=0
for p in range(13,1001,8):
 if not prime(p):continue
 inv=lambda n:pow(n%p,-1,p)
 g=root(p);a=pow(g,2,p);D=(a-1)**2%p
 Z=(1+3*a)*inv(D)%p;W=a*(a+3)*inv(D)%p
 if Z==0 or W==0:label='degenerate'
 elif pow(W*inv(Z)%p,(p-1)//2,p)!=p-1:label='same component'
 else:
  b=(1+Z)%p;v=(1+W)%p;half=inv(2)
  mu=lambda d:d*(1+a)*inv(2*(a-1))%p
  selected=lambda d:{(1+mu(d))%p,(1-mu(d))%p}
  need1={(b-half)%p,(b+half)%p,(b+3*half)%p,(v+half)%p}
  need3={(b-half)%p,(b+3*half)%p}
  label='selected slot' if need1&selected(1) or need3&selected(3) else 'ready'
 counts[label]=counts.get(label,0)+1
 if label not in ('ready','selected slot'):continue
 u=(p-1)//4
 halfset={pow(g,e,p) for i in range(u) for e in (4*i,4*i+1)}
 starter=[{frozenset((x,a*x%p)) for x in halfset}]
 starter.append({frozenset((-x%p for x in pair)) for pair in starter[0]})
 chosen={1:[],3:[]}
 for matching in starter:
  for pair in matching:
   x,y=tuple(pair);d=min((x-y)%p,(y-x)%p)
   if d in chosen:chosen[d].append((1+(x+y)*inv(2))%p)
 for d in chosen:
  assert len(chosen[d])==2 and set(chosen[d])=={(1+mu(d))%p,(1-mu(d))%p},(p,d)
 if label!='ready':continue
 C={d:set() for d in (1,3)}
 for d in C:
  for x in range(p):
   y=(x+d)%p;m=(x+y)*inv(2)%p
   C[d].update(((x,m),(y,m)))
 P=set()
 for side,matching in enumerate(starter):
  fresh=p+side
  for pair in matching:
   x,y=((z+1)%p for z in pair)
   d=min((x-y)%p,(y-x)%p)
   m=(x+y)*inv(2)%p
   if d in C:
    assert {(x,m),(y,m)}<=C[d]
    C[d].difference_update(((x,m),(y,m)))
    C[d].update(((x,fresh),(y,fresh)))
   P.update(((x,m),(y,m)))
 assert parts(C[1])==[p] and parts(C[3])==[p]
 assert parts(P)==[(p-1)//2,(p-1)//2]
 touched_before=C[1]|C[3]|P
 assert (1+a)*Z*inv(2)%p==(W+half)%p
 assert (1+a)*W*inv(2*a)%p==(Z+half)%p
 x1=(b,(b-half)%p);x2=((b+1)%p,(b+3*half)%p)
 y1=(b,(b+3*half)%p);y2=((b+1)%p,(b-half)%p)
 swap(C[1],C[3],x1,x2,y1,y2)
 assert parts(C[1])==[p] and parts(C[3])==[p]
 x1=(b,(b+half)%p);x2=(v,(v+half)%p)
 y1=(b,(v+half)%p);y2=(v,(b+half)%p)
 swap(C[1],P,x1,x2,y1,y2)
 assert parts(C[1])==[p] and parts(P)==[p-1]
 assert C[1]|C[3]|P==touched_before
 assert len(C[1])+len(C[3])+len(P)==len(touched_before)
 checked+=1
 print('ready verified',p,'b',b,'v',v)
print('counts',counts,'connected ready',checked)
