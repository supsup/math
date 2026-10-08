"""Small-prime every-primitive-root check using independent raw growth."""
import importlib.util
from pathlib import Path

audit_path = Path(__file__).with_name("64_skew_three_independent_audit.py")
spec = importlib.util.spec_from_file_location("skew_three_audit", audit_path)
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)


def prime_factors(n):
    out=[];d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out


def chi(p,z):
    z%=p
    return 0 if z==0 else (1 if pow(z,(p-1)//2,p)==1 else -1)


for p in (13,29,37):
    roots=[g for g in range(2,p)
           if all(pow(g,(p-1)//q,p)!=1 for q in prime_factors(p-1))]
    solutions=[]
    for g in roots:
        a=g*g%p
        delta=(1-a)*pow(1+a,-1,p)%p
        first=[z for z in range(p)
               if chi(p,z*(z+delta))==-1
               and chi(p,(z-1)*(z+delta-1))==-1]
        second=[z for z in range(p)
                if chi(p,z*(z+delta))==1
                and chi(p,(z-1)*(z+delta-1))==-1]
        found=None
        for z1 in first:
            for z2 in second:
                colors,singletons=G.raw_growth(p,g)
                k=(p-1)//2
                try:
                    G.switch(colors[k],colors[k+1],G.rect(p,g,1,1,z1))
                    G.switch(colors[k],colors[k+2],G.rect(p,g,1,2,z2))
                    assert all(len(G.cycles(C))==1 for C in colors)
                    seen=set(singletons)
                    for C in colors:
                        assert not seen&C
                        seen.update(C)
                    assert seen=={(h,l) for h in range(p) for l in range(p+6)}
                    found=(z1,z2)
                    break
                except AssertionError:
                    pass
            if found:break
        assert found is not None,(p,g)
        solutions.append((g,*found))
    print(p,len(roots),'/',len(solutions),'primitive roots solved',solutions)
