"""Replay K49 growth and recorded four-spoke trades against saved final walks."""
import json
from collections import defaultdict
from pathlib import Path
D=json.loads(Path(__file__).with_name('59_fortynine_hub_odd_seeds.json').read_text());H=49;K=24;inv2=25
S=[tuple(p) for p in D['starter_matching']]
M=(S,[((-u)%H,(-v)%H) for u,v in S])
centers=D['centers']
def e(a,b):return tuple(sorted((a,b)))
def nc(sp):
 adj=defaultdict(set)
 for a,b in sp:adj[(0,a)].add((1,b));adj[(1,b)].add((0,a))
 assert all(len(v)==2 for v in adj.values())
 unseen=set(adj);count=0
 while unseen:
  stack=[unseen.pop()];count+=1
  while stack:
   for x in adj[stack.pop()]:
    if x in unseen:unseen.remove(x);stack.append(x)
 return count

def raw(j):
 C=[set() for _ in range(K)];slot={}
 for d in range(1,K+1):
  for u in range(H):
   v=(u+d)%H;mid=(u+v)*inv2%H
   assert e(u,v) not in slot
   slot[e(u,v)]=(d-1,mid)
   C[d-1].update(((u,mid),(v,mid)))
 singles={(a,a) for a in range(H)}
 for step,center in enumerate(centers[:j]):
  page=set();old=[]
  for parity,side in enumerate(M):
   z=H+2*step+parity
   for u,v in side:
    a,b=(u+center)%H,(v+center)%H
    c,prior=slot[e(a,b)]
    assert (a,prior) in C[c] and (b,prior) in C[c]
    C[c].difference_update(((a,prior),(b,prior)))
    C[c].update(((a,z),(b,z)))
    page.update(((a,prior),(b,prior)))
    old.append(prior)
    slot[e(a,b)]=(c,z)
  assert len(old)==len(set(old))==H-1
  C.append(page);singles.update(((center,H+2*step),(center,H+2*step+1)))
 return singles,C

assert len(S)==24 and {x for p in S for x in p}==set(range(1,H))
assert {min((v-u)%H,(u-v)%H) for u,v in S}==set(range(1,25))
assert {min((u+v)*inv2%H,(-(u+v)*inv2)%H) for u,v in S}==set(range(1,25))
for j in range(K):
 b=H+2*j;singles,C=raw(j)
 entry=D['odd_base_certificates'][str(b)]
 assert singles=={tuple(x) for x in entry['singleton_spokes']}
 trace=D['repair_traces'][str(b)]
 assert len(trace)==18+j
 for step,row in enumerate(trace,1):
  target,partner,*spokes=row
  t1,t2,p1,p2=map(tuple,spokes)
  assert 0<=target<len(C) and 0<=partner<len(C) and target!=partner
  assert t1 in C[target] and t2 in C[target]
  assert p1 in C[partner] and p2 in C[partner]
  assert p1==(t1[0],t2[1]) and p2==(t2[0],t1[1])
  old_target=nc(C[target]);old_partner=nc(C[partner])
  assert old_target>1 and old_partner==1
  C[target].difference_update((t1,t2));C[target].update((p1,p2))
  C[partner].difference_update((p1,p2));C[partner].update((t1,t2))
  assert nc(C[target])==old_target-1 and nc(C[partner])==1
 for i,cycle in enumerate(entry['cycles']):
  hubs,leaves=cycle['hubs'],cycle['leaves']
  edges={(hub,leaf) for p,hub in enumerate(hubs) for leaf in (leaves[p],leaves[p-1])}
  assert edges==C[i] and nc(edges)==1
print('PASS 24 prefixes, all 708 recorded trades replayed; each reduces target components by one and keeps partner connected; final spokes match saved walks')
