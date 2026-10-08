"""Independent stdlib replay of all K53 growth and saved checkerboard trades."""
import json
from collections import defaultdict
from pathlib import Path
D=json.loads(Path(__file__).with_name('63_fiftythree_hub_odd_seeds.json').read_text());p=53;k=26;inv2=27
assert D['h']==p
# Hard-coded primitive root 2; the two starter matchings are S and -S.
a=4
half={pow(2,4*i+j,p) for i in range(13) for j in (0,1)}
S={tuple(sorted((x,a*x%p))) for x in half}
NS={tuple(sorted(((-u)%p,(-v)%p))) for u,v in S}
assert len(S)==len(NS)==26 and not S&NS
assert {x for edge in S for x in edge}==set(range(1,p))
assert {min((u-v)%p,(v-u)%p) for u,v in S}==set(range(1,k+1))
assert {((u+v)*inv2)%p for u,v in S|NS}==set(range(1,p))

def edge(u,v):return tuple(sorted((u,v)))

def components(sp):
 adj=defaultdict(set)
 for hub,leaf in sp:adj[(0,hub)].add((1,leaf));adj[(1,leaf)].add((0,hub))
 assert all(len(v)==2 for v in adj.values())
 unseen=set(adj);sizes=[]
 while unseen:
  root=unseen.pop();todo=[root];size=0
  while todo:
   node=todo.pop();size+=node[0]==0
   for z in adj[node]:
    if z in unseen:unseen.remove(z);todo.append(z)
  sizes.append(size)
 return sorted(sizes)

def raw(prefix):
 C=[set() for _ in range(k)];slots={}
 for d in range(1,k+1):
  for u in range(p):
   v=(u+d)%p;m=(u+v)*inv2%p
   pair=edge(u,v);assert pair not in slots
   slots[pair]=(d-1,m);C[d-1].update(((u,m),(v,m)))
 singles={(a,a) for a in range(p)}
 for step in range(prefix):
  center=step+1;page=set();old=[]
  for side,matching in enumerate((S,NS)):
   new=p+2*step+side
   for u,v in matching:
    x,y=(u+center)%p,(v+center)%p
    color,leaf=slots[edge(x,y)]
    assert (x,leaf) in C[color] and (y,leaf) in C[color]
    C[color].difference_update(((x,leaf),(y,leaf)))
    C[color].update(((x,new),(y,new)))
    page.update(((x,leaf),(y,leaf)));old.append(leaf)
    slots[edge(x,y)]=(color,new)
  assert len(old)==len(set(old))==p-1
  C.append(page)
  singles.update(((center,p+2*step),(center,p+2*step+1)))
 return singles,C

total=0
for prefix in range(k):
 t=p+2*prefix;entry=D['odd_base_certificates'][str(t)]
 singles,C=raw(prefix)
 assert singles=={tuple(x) for x in entry['singleton_spokes']}
 assert all(components(c)==[p] for c in C[:k])
 assert all(components(c)==[26,26] for c in C[k:])
 trace=D['repair_traces'][str(t)]
 expected=0 if prefix==0 else 2 if prefix==1 else prefix//2+(prefix%2)
 assert len(trace)==expected,(prefix,len(trace),expected)
 for row in trace:
  target,partner,*spokes=row
  t1,t2,q1,q2=map(tuple,spokes)
  assert 0<=target<len(C) and 0<=partner<len(C) and target!=partner
  assert t1 in C[target] and t2 in C[target]
  assert q1 in C[partner] and q2 in C[partner]
  assert q1==(t1[0],t2[1]) and q2==(t2[0],t1[1])
  oldt,oldp=components(C[target]),components(C[partner])
  C[target].difference_update((t1,t2));C[target].update((q1,q2))
  C[partner].difference_update((q1,q2));C[partner].update((t1,t2))
  newt,newp=components(C[target]),components(C[partner])
  assert len(newt)<=len(oldt) and len(newp)<=len(oldp)
  if len(oldt)==2:assert len(newt)==1
  if len(oldp)==2:assert len(newp)==1
  total+=1
 for i,cycle in enumerate(entry['cycles']):
  hs,ls=cycle['hubs'],cycle['leaves']
  sp={(hub,leaf) for j,hub in enumerate(hs) for leaf in (ls[j],ls[j-1])}
  assert sp==C[i]
  assert components(sp)==[p-(i>=k)]
print('PASS 26 odd/square bases,',total,'saved checkerboard trades replayed; final spoke sets match walks')
