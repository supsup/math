"""Independent stdlib audit of saved K51 square block, even bases and sampled lifts."""
import json,hashlib
from pathlib import Path
raw=Path(__file__).with_name('61_fiftyone_hub_square_seed.json').read_bytes();D=json.loads(raw)
h=51;k=25
assert D['h']==h and len(D['cycles'])==k and len(D['singleton_spokes'])==h

def offset(delta,start):
 return {'hubs':[(-i)%h for i in range(h)],'leaves':[start+((-i+delta)%h) for i in range(h)]}

def base(b):
 if b==h:return [tuple(x) for x in D['singleton_spokes']],D['cycles']
 assert 50<=b<=100 and b%2==0
 m=b//2
 singles=[(h-1,z) for z in range(b)]
 cycles=[{'hubs':list(range(h-1)),
          'leaves':[2*((shift+j)%m)+q for j in range(k) for q in (0,1)]}
          for shift in range(m)]
 return singles,cycles

def audit(b,q):
 singles,cycles=base(b);singles=list(singles);cycles=list(cycles)
 for block in range(q):
  start=b+h*block
  singles.extend((a,start+a) for a in range(h))
  cycles.extend(offset(delta,start) for delta in range(1,h,2))
 t=b+h*q;seen=set()
 assert len(singles)==t and len(cycles)==(k*t+h-1)//h
 for a,z in singles:
  assert 0<=a<h and 0<=z<t and (a,z) not in seen
  seen.add((a,z))
 for color in cycles:
  hs,ls=color['hubs'],color['leaves'];n=len(hs)
  assert 2<=n<=h and len(ls)==n and len(set(hs))==len(set(ls))==n
  for i,a in enumerate(hs):
   assert 0<=a<h
   for z in (ls[i],ls[i-1]):
    assert 0<=z<t and (a,z) not in seen
    seen.add((a,z))
 assert seen=={(a,z) for a in range(h) for z in range(t)}
 assert len(singles)+len(cycles)==t+(k*t+h-1)//h

for b in [51,*range(50,101,2)]:
 for q in (0,1,11):audit(b,q)
print('PASS square b=51 and 26 even b=50..100, q=0,1,11; exact spoke partition and optimum count')
print('sha256',hashlib.sha256(raw).hexdigest())
