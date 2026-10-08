"""Check the exact translated-line criterion for all 5 mod 8 primes through 1000.

Run: python3 -I playground/marlow/60_skew_adjacent_pairs_criterion_scan.py
"""
from math import isqrt

def prime(p):return p>1 and all(p%d for d in range(2,isqrt(p)+1))
def root(p):
 n=p-1;factors=[];v=n;d=2
 while d*d<=v:
  if v%d==0:
   factors.append(d)
   while v%d==0:v//=d
  d+=1
 if v>1:factors.append(v)
 return next(g for g in range(2,p) if all(pow(g,n//q,p)!=1 for q in factors))

def scan(p):
 g=root(p);a=g*g%p;inv=pow(a+1,-1,p)
 delta=(1-a)*inv%p;k=(p-1)//2
 residue=[0]*p
 for v in range(1,p):residue[pow(v,2,p)]=1
 best=(10**9,None)
 for c in range(1,k-1,2):
  H={(r+a*(c+1))*inv%p for r in range(c+1)}
  L={(a*r+c)*inv%p for r in range(1,c+2)}
  count=0
  for v in range(p):
   u=(v+delta)%p
   if v in H or v in L:continue
   f1=(v-c)*(u-c)%p;f2=(v-c-1)*(u-c-1)%p
   if f1 and f2 and not residue[f1] and not residue[f2]:count+=1
  if count<best[0]:best=(count,c)
  if count==0:return best
 return best

ps=[p for p in range(13,1001,8) if prime(p)]
for p in ps:
 count,c=scan(p)
 print(p,'min',count,'center',c,flush=True)
 if count==0:print('FIRST FAILURE',p,c,flush=True);break
else:print('ALL',len(ps),'PRIMES POSITIVE')
