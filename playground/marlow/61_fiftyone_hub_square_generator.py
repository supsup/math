"""Deterministic connected 51-leaf square block; Python stdlib only."""
import json
from collections import defaultdict
from pathlib import Path
H=51;K=25;INV2=26
SPLIT=(2,5,8,11,14,16,17,20,23)

def parts(sp):
 adj=defaultdict(set)
 for a,b in sp:adj[(0,a)].add((1,b));adj[(1,b)].add((0,a))
 assert all(len(v)==2 for v in adj.values())
 unseen=set(adj);out=[]
 while unseen:
  root=min(unseen);unseen.remove(root);stack=[root];p={root}
  while stack:
   for z in sorted(adj[stack.pop()]):
    if z in unseen:unseen.remove(z);p.add(z);stack.append(z)
  out.append(p)
 return sorted(out,key=lambda p:min(a for kind,a in p if kind==0))

def walk(sp):
 bh=defaultdict(set);bl=defaultdict(set)
 for a,b in sp:bh[a].add(b);bl[b].add(a)
 a=min(bh);b=min(bh[a]);hs=[];ls=[]
 while True:
  hs.append(a);ls.append(b)
  nxt=next(z for z in bl[b] if z!=a)
  if nxt==hs[0]:break
  b=next(z for z in bh[nxt] if z!=b);a=nxt
 assert len(hs)==len(ls)==len(bh)==len(bl)
 return {'hubs':hs,'leaves':ls}

C=[]
for d in range(1,K+1):
 sp=set()
 for a in range(H):
  v=(a+d)%H;m=(a+v)*INV2%H
  sp.update(((a,m),(v,m)))
 C.append(sp)
assert [len(parts(c)) for c in C]==[17 if d==16 else 3 if d in SPLIT else 1 for d in range(K)]
trace=[]
for target in SPLIT:
 while len(parts(C[target]))>1:
  ps=parts(C[target]);owners={e:i for i,c in enumerate(C) if i!=target and len(parts(c))==1 for e in c}
  bypart=[sorted(e for e in C[target] if (0,e[0]) in p) for p in ps]
  chosen=None
  for i in range(len(ps)):
   if chosen:break
   for j in range(i+1,len(ps)):
    if chosen:break
    for a,x in bypart[i]:
     if chosen:break
     for b,y in bypart[j]:
      q1,q2=(a,y),(b,x);partner=owners.get(q1)
      if partner is None or owners.get(q2)!=partner:continue
      tn=C[target]-{(a,x),(b,y)}|{q1,q2}
      if len(parts(tn))!=len(ps)-1:continue
      pn=C[partner]-{q1,q2}|{(a,x),(b,y)}
      if len(parts(pn))!=1:continue
      chosen=(partner,(a,x),(b,y),q1,q2,tn,pn);break
  assert chosen is not None,(target,len(ps))
  partner,p1,p2,q1,q2,tn,pn=chosen
  assert {a for a,_ in tn}=={a for a,_ in C[target]}
  assert {b for _,b in tn}=={b for _,b in C[target]}
  assert {a for a,_ in pn}=={a for a,_ in C[partner]}
  assert {b for _,b in pn}=={b for _,b in C[partner]}
  C[target],C[partner]=tn,pn
  trace.append((target,partner,p1,p2,q1,q2))
assert len(trace)==32 and all(len(parts(c))==1 for c in C)
singles={(a,a) for a in range(H)};seen=set(singles)
for c in C:
 assert len(c)==2*H and not seen&c
 seen.update(c)
assert seen=={(a,b) for a in range(H) for b in range(H)}
data={'h':H,'singleton_spokes':sorted(map(list,singles)),'cycles':[walk(c) for c in C],'repair_traces':trace}
out=Path(__file__).with_name('61_fiftyone_hub_square_seed.generated.json');out.write_text(json.dumps(data,separators=(',',':'),sort_keys=True))
print('wrote',out,'32 trades, 51 singletons, 25 simple 102-edge cycles')
