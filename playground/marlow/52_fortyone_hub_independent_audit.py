"""Independent direct audit of item 52 walks, growth, and all 190 trades.

Run: python3 -I playground/marlow/52_fortyone_hub_independent_audit.py
"""

import json, collections, pathlib, hashlib
P=pathlib.Path(__file__).resolve().parent
raw=(P/'52_fortyone_hub_switch_seeds.json').read_bytes(); D=json.loads(raw)
H=41; K=20; universe=lambda t:{(h,l) for h in range(H) for l in range(t)}
match=[D['matchings'][x] for x in ('even','odd')]
def E(a,b): return tuple(sorted((a,b)))
def spokes(c):
 h,l=c['hubs'],c['leaves']; assert len(h)==len(l)>=2 and len(set(h))==len(h) and len(set(l))==len(l)
 return [(u,v) for i,u in enumerate(h) for v in (l[i],l[i-1])]
def parts(S):
 adj=collections.defaultdict(set)
 for a,b in S: adj[('h',a)].add(('l',b)); adj[('l',b)].add(('h',a))
 assert all(len(ns)==2 for ns in adj.values())
 todo=set(adj); cs=[]
 while todo:
  st=[todo.pop()]; c=set(st)
  while st:
   for v in adj[st.pop()]:
    if v in todo: todo.remove(v);c.add(v);st.append(v)
  cs.append(c)
 return sorted(len(c)//2 for c in cs)
def check(singles,cycles,t):
 seen=set(); lengths=[]
 for e in singles:
  e=tuple(e);assert 0<=e[0]<H and 0<=e[1]<t and e not in seen;seen.add(e)
 for c in cycles:
  es=spokes(c);assert len(set(es))==len(es)
  for e in es: assert 0<=e[0]<H and 0<=e[1]<t and e not in seen;seen.add(e)
  lengths.append(len(c['hubs']))
 assert seen==universe(t), (t,len(seen))
 assert len(singles)==t and len(cycles)==(20*t+40)//41
 return collections.Counter(lengths)
# Independently validate matching page
mids=set(); es=set(); disps=[]; page=set()
for side in match:
 assert len(side)==20
 verts=[]
 for d,(a,b) in enumerate(side,1):
  assert {a,b}<=set(range(1,H)) and min((a-b)%H,(b-a)%H)==d
  q=E(a,b);assert q not in es;es.add(q);verts.extend((a,b))
  mid=(a+b)*21%H;assert mid and mid not in mids;mids.add(mid)
  page.update([(a,mid),(b,mid)])
 assert set(verts)==set(range(1,H))
assert mids==set(range(1,H)) and parts(page)==[8,32]
for (a,b),(c,d) in zip(*match):
 s=((c+d)-(a+b))*21%H;disps.append(min(s,H-s))
profile=collections.Counter(disps)
for s in range(1,H):
 trans={E((a+s)%H,(b+s)%H) for a,b in es}
 assert len(es&trans)==profile[min(s,H-s)]
centers=D['centers']; assert len(centers)==len(set(centers))==19
for a in centers:
 for b in centers:
  if a!=b: assert profile[min((a-b)%H,(b-a)%H)]<=1
# Independently validate saved base walks, parity, and per-prefix omitted hubs.
assert set(D['seeds'])=={str(t) for t in range(43,80,2)}
odd=[]
for t in range(43,80,2):
 seed=D['seeds'][str(t)];counts=check(seed['singleton_spokes'],seed['cycles'],t)
 j=(t-41)//2;assert counts=={41:20,40:j}
 assert {h for c in seed['cycles'] if len(c['hubs'])==40 for h in set(range(41))-set(c['hubs'])}==set(centers[:j])
 odd.append(t)
# Replay all trace switches independently against affine square and matching translation.
trace_counts=[]
for t in odd:
 j=(t-41)//2
 C=[set() for _ in range(20)];slots={}
 for d in range(1,21):
  for a in range(41):
   b=(a+d)%41;m=(a+b)*21%41;slots[E(a,b)]=(d-1,m)
   C[d-1].update(((a,m),(b,m)))
 assert all(parts(c)==[41] for c in C)
 for step,z in enumerate(centers[:j]):
  page=set();oldmid=[]
  for p,side in enumerate(match):
   newleaf=41+2*step+p
   for a,b in side:
    x,y=(a+z)%41,(b+z)%41; color,mid=slots[E(x,y)]
    old={(x,mid),(y,mid)};assert old<=C[color]
    C[color]-=old;C[color].update(((x,newleaf),(y,newleaf)))
    page|=old;oldmid.append(mid);slots[E(x,y)]=(color,newleaf)
  assert len(set(oldmid))==40 and parts(page)==[8,32]
  C.append(page)
 for rec in D['traces'][str(t)]:
  p,q=rec['page_color'],rec['partner_color']
  a,b=map(tuple,rec['page_old_spokes']);x,y=map(tuple,rec['partner_old_spokes'])
  assert p>=20 and p<len(C) and q!=p
  assert {a,b}<=C[p] and {x,y}<=C[q]
  assert len({a[0],b[0]})==len({a[1],b[1]})==2
  assert {x,y}=={(a[0],b[1]),(b[0],a[1])}
  assert parts(C[p])==[8,32] and parts(C[q]) in ([41],[40])
  C[p]-={a,b};C[p]|={x,y};C[q]-={x,y};C[q]|={a,b}
  assert len(parts(C[p]))==len(parts(C[q]))==1
 assert len(D['traces'][str(t)])==j and all(len(parts(c))==1 for c in C)
 actual=[set(spokes(c)) for c in D['seeds'][str(t)]['cycles']]
 assert C==actual, ('trace mismatch',t)
 trace_counts.append(j)
# Independent even-base and lift checks.
def base(t):
 if t%2==0:
  m=t//2
  s=[(40,l) for l in range(t)]
  c=[{'hubs':list(range(40)),'leaves':[2*((a+j)%m)+p for j in range(20) for p in range(2)]} for a in range(m)]
 elif t==41:
  s=[(h,h) for h in range(41)];c=offset(0)
 else:
  z=D['seeds'][str(t)];s=z['singleton_spokes'];c=z['cycles']
 return s,c
def offset(start):
 return [{'hubs':[(-i)%41 for i in range(41)],'leaves':[start+((-i+a)%41) for i in range(41)]} for a in range(1,41,2)]
for t in range(40,81):
 s,c=base(t);check(s,c,t)
 for n in range(1,12):
  ss=list(s);cc=list(c)
  for k in range(n):
   st=t+41*k;ss += [(h,st+h) for h in range(41)];cc += offset(st)
  check(ss,cc,t+41*n)
print('json_sha256',hashlib.sha256(raw).hexdigest())
print('profile',sorted(profile.items()),'centers',centers)
print('odd bases',len(odd),'traces',sum(trace_counts),'walks',sum(len(D['seeds'][str(t)]['cycles']) for t in odd))
print('all 41 bases and all 11 offset lifts: exact edge partitions, valid simple cycles, correct counts')
