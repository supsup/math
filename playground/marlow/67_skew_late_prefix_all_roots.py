from math import isqrt

def prime(p):return p>1 and all(p%d for d in range(2,isqrt(p)+1))
def factors(n):
 out=[];d=2
 while d*d<=n:
  if n%d==0:
   out.append(d)
   while n%d==0:n//=d
  d+=1
 if n>1:out.append(n)
 return out

def root_count(p,a,sq):
 D=(a+1)%p;ivD=pow(D,-1,p);d=(1-a)*ivD%p;k=(p-1)//2;c=k-2
 good={z for z in range(p) if z*(z+d)%p not in sq and z*(z+d)%p!=0 and (z-1)*(z+d-1)%p not in sq and (z-1)*(z+d-1)%p!=0}
 E={(a-q)*ivD%p for q in range(c+1)}|{a*(1-q)*ivD%p for q in range(c+1)}
 return len(good-E),len(good),p-len(E),len(E)

rows=[]
for p in range(13,2001,8):
 if not prime(p):continue
 fs=factors(p-1);vals=[];sq={x*x%p for x in range(1,p)};seen=set()
 for g in range(2,p):
  if all(pow(g,(p-1)//q,p)!=1 for q in fs):
   a=g*g%p
   if a not in seen:vals.append((root_count(p,a,sq),g,a));seen.add(a)
 x=min(vals)
 rows.append((p,len(vals),x))
 if x[0][0]==0:print('FAIL',p,x,flush=True);break
 print('row',p,len(vals),'min',x,flush=True)
else:print('ALL_PASS',len(rows),'min_survivors',min((r[2][0][0],r[0],r[2][1],r[2][2]) for r in rows))
