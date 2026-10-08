"""Exact finite character/relabel criterion for latest odd prefix per prime."""
from math import isqrt

def prime(p):
    return p>1 and all(p%d for d in range(2,isqrt(p)+1))

def root(p):
    factors={q for q in range(2,p) if (p-1)%q==0 and prime(q)}
    return next(g for g in range(2,p)
                if all(pow(g,(p-1)//q,p)!=1 for q in factors))

def chi(p,x):
    x%=p
    return 0 if not x else (1 if pow(x,(p-1)//2,p)==1 else -1)

def scan(p):
    g=root(p);a=g*g%p;D=a+1;inv=pow(D,-1,p)
    delta=(1-a)*inv%p
    good={w for w in range(p) if chi(p,w*(w+delta))==-1
          and chi(p,(w-1)*(w+delta-1))==-1}
    c=(p-5)//2  # latest even pair start in maximal odd prefix
    excluded={(a-q)*inv%p for q in range(c+1)}
    excluded|={a*(1-q)*inv%p for q in range(c+1)}
    survivors=good-excluded
    return g,c,len(good),len(excluded),len(survivors),min(survivors) if survivors else None

if __name__=='__main__':
    rows=[(p,*scan(p)) for p in range(13,1001,8) if prime(p)]
    assert len(rows)==42
    assert all(row[5]>0 for row in rows)
    print('primes',len(rows),'all_latest_odd_prefixes_ready',True,
          'minimum_survivors',min(row[5] for row in rows))
    print('examples',rows[:6],rows[-3:])
