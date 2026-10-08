"""Independent stdlib replay of saved K49 ordered walks, all 49 bases and 0/1/11 lifts."""
import json,hashlib
from pathlib import Path
h=49;k=24
p=Path(__file__).with_name('59_fortynine_hub_odd_seeds.json')
raw=p.read_bytes(); data=json.loads(raw)
assert data['h']==h
assert len(data['odd_base_certificates'])==24

def offset_cycle(delta,start):
 return {'hubs':[(-i)%h for i in range(h)],'leaves':[start+((-i+delta)%h) for i in range(h)]}

def base(b):
 if b%2:
  entry=data['odd_base_certificates'][str(b)]
  return [tuple(x) for x in entry['singleton_spokes']],entry['cycles']
 half=b//2
 singles=[(h-1,z) for z in range(b)]
 cycles=[{'hubs':list(range(h-1)),'leaves':[2*((shift+j)%half)+q for j in range(k) for q in (0,1)]} for shift in range(half)]
 return singles,cycles

def audit(b,q):
 t=b+h*q; singles,cycles=base(b)
 singles=list(singles);cycles=list(cycles)
 for block in range(q):
  start=b+h*block
  singles.extend((a,start+a) for a in range(h))
  cycles.extend(offset_cycle(delta,start) for delta in range(1,h,2))
 assert len(singles)==t
 assert len(cycles)==(k*t+h-1)//h
 seen=set()
 for a,z in singles:
  assert 0<=a<h and 0<=z<t
  assert (a,z) not in seen
  seen.add((a,z))
 for c in cycles:
  hs,ls=c['hubs'],c['leaves']
  n=len(hs)
  assert 2<=n<=h and len(ls)==n
  assert len(set(hs))==len(set(ls))==n
  for i,a in enumerate(hs):
   assert 0<=a<h
   for z in (ls[i],ls[i-1]):
    assert 0<=z<t and (a,z) not in seen,(b,q,a,z)
    seen.add((a,z))
 assert len(seen)==h*t
 assert seen=={(a,z) for a in range(h) for z in range(t)}
 assert len(singles)+len(cycles)==t+(k*t+h-1)//h
 return len(cycles)

for b in range(48,97):
 for q in (0,1,11):audit(b,q)
print('PASS all 49 base residues b=48..96, lifts q=0,1,11: simple cycles, exact edge partition, optimum part count')
print('certificate bytes',len(raw),'sha256',hashlib.sha256(raw).hexdigest())
print('odd-base cycle counts',[(b,audit(b,0)) for b in range(49,96,2)])
