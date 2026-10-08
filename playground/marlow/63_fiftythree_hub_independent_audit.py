"""Independent stdlib audit of K53 saved walks, every base and sampled lifts."""
import hashlib,json
from pathlib import Path
raw=Path(__file__).with_name('63_fiftythree_hub_odd_seeds.json').read_bytes();D=json.loads(raw)
h=53;k=26
assert D['h']==h
assert set(D['odd_base_certificates'])=={str(h+2*j) for j in range(k)}

def offset(delta,start):
 return {'hubs':[(-i)%h for i in range(h)],
         'leaves':[start+((-i+delta)%h) for i in range(h)]}

def base(b):
 if b%2:
  entry=D['odd_base_certificates'][str(b)]
  return [tuple(x) for x in entry['singleton_spokes']],entry['cycles']
 half=b//2
 singles=[(h-1,z) for z in range(b)]
 cycles=[{'hubs':list(range(h-1)),
          'leaves':[2*((shift+j)%half)+q for j in range(k) for q in (0,1)]}
          for shift in range(half)]
 return singles,cycles

def audit(b,q):
 t=b+h*q;singles,cycles=base(b)
 singles=list(singles);cycles=list(cycles)
 for block in range(q):
  start=b+h*block
  singles.extend((a,start+a) for a in range(h))
  cycles.extend(offset(delta,start) for delta in range(1,h,2))
 assert len(singles)==t and len(cycles)==(k*t+h-1)//h
 seen=set()
 for a,z in singles:
  assert 0<=a<h and 0<=z<t and (a,z) not in seen
  seen.add((a,z))
 for color in cycles:
  hs,ls=color['hubs'],color['leaves'];n=len(hs)
  assert 2<=n<=h and len(ls)==n
  assert len(set(hs))==len(set(ls))==n
  for i,a in enumerate(hs):
   assert 0<=a<h
   for z in (ls[i],ls[i-1]):
    assert 0<=z<t and (a,z) not in seen,(b,q,a,z)
    seen.add((a,z))
 assert seen=={(a,z) for a in range(h) for z in range(t)}
 assert len(singles)+len(cycles)==t+(k*t+h-1)//h

for b in range(52,105):
 for q in (0,1,11):audit(b,q)
print('PASS 53 bases b=52..104, lifts q=0,1,11: simple cycles, exact spoke coverage, optimum part counts')
print('certificate bytes',len(raw),'sha256',hashlib.sha256(raw).hexdigest())
