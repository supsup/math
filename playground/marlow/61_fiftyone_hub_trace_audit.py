"""Independent replay of the K51 square certificate's 32 checkerboard trades."""
import json
from collections import defaultdict
from pathlib import Path
D=json.loads(Path(__file__).with_name('61_fiftyone_hub_square_seed.json').read_text());h=51;inv2=26
C=[]
for d in range(1,26):
 sp=set()
 for a in range(h):
  b=(a+d)%h;m=(a+b)*inv2%h
  sp.update(((a,m),(b,m)))
 C.append(sp)
def nc(sp):
 adj=defaultdict(set)
 for a,b in sp:adj[(0,a)].add((1,b));adj[(1,b)].add((0,a))
 assert all(len(v)==2 for v in adj.values())
 todo=set(adj);n=0
 while todo:
  stack=[todo.pop()];n+=1
  while stack:
   for z in adj[stack.pop()]:
    if z in todo:todo.remove(z);stack.append(z)
 return n
assert [nc(c) for c in C]==[17 if i==16 else 3 if i in (2,5,8,11,14,16,17,20,23) else 1 for i in range(25)]
assert len(D['repair_traces'])==32
for row in D['repair_traces']:
 target,partner,*raw=row;p1,p2,q1,q2=map(tuple,raw)
 assert p1 in C[target] and p2 in C[target]
 assert q1 in C[partner] and q2 in C[partner]
 assert q1==(p1[0],p2[1]) and q2==(p2[0],p1[1])
 before=nc(C[target]);assert before>1 and nc(C[partner])==1
 C[target].difference_update((p1,p2));C[target].update((q1,q2))
 C[partner].difference_update((q1,q2));C[partner].update((p1,p2))
 assert nc(C[target])==before-1 and nc(C[partner])==1
for i,c in enumerate(D['cycles']):
 hs,ls=c['hubs'],c['leaves']
 sp={(a,z) for p,a in enumerate(hs) for z in (ls[p],ls[p-1])}
 assert sp==C[i] and nc(sp)==1
print('PASS all 32 trades replay, component decrease and connected partners, saved walks match')
