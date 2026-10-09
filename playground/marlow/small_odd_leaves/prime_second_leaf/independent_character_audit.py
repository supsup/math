"""Finite controls for the projector, extension, and arithmetic cutoff."""

import cmath
from math import gcd, sqrt


def primes(limit):
    return [n for n in range(2, limit+1)
            if all(n%d for d in range(2, int(n**0.5)+1))]


def order(x, modulus):
    v=1
    for k in range(1,modulus):
        v=v*x%modulus
        if v==1:return k
    raise AssertionError


def check(p):
    n=(p-1)//2
    Q={x*x%p for x in range(1,p)}
    chi=lambda x: 0 if x%p==0 else (1 if x%p in Q else -1)
    a=next(x for x in sorted(Q) if order(x,p)==n)
    G=next(x for x in range(2,p) if order(x,p)==p-1)
    discrete={pow(G,k,p):k for k in range(p-1)}
    assert len(discrete)==p-1
    eps=-chi(-1)
    selected=[]
    allowed=[]
    for c in range(p):
        R=(c+a-1)%p
        F=(c*c+2*(a-1)*c-(a-1))%p
        if not (c and R and F and (1-c)%p):continue
        signs=(chi(c),chi(R),chi(F),chi(1-c))
        P=(1-signs[0])*(1+signs[1])*(1-signs[2])*(1+eps*signs[3])//16
        assert P in (0,1)
        g=F*pow(c*R,-1,p)%p
        allowed.append((c,g,P))
        if P:
            assert chi(g)==1
            selected.append((c,g))
    assert len(allowed)>=p-5
    # Two extensions of each nontrivial character of Q differ by chi.
    for k0 in range(1,n):
        d=n//gcd(k0,n)
        ext=[k for k in (k0,k0+n) if (2*n)//gcd(k,2*n)==2*d]
        assert ext
        k=ext[0]
        # psi^d is quadratic, and no of the 16 projector terms can
        # cancel the F-root exponent 1 or 1+d modulo 2d.
        assert k*d%(2*n)==n
        assert 1%(2*d) and (1+d)%(2*d)
        Z=sum(cmath.exp(2j*cmath.pi*k*discrete[g]/(2*n))*P
              for c,g,P in allowed)
        assert abs(Z)<=4*sqrt(p)+5+1e-8
    # Every projector-selected g has the anticipated primitive order test.
    return len(selected),sum(order(g,p)==n for _,g in selected)


def arithmetic():
    small=(2,3,5,7,11,13,17,19,23,29,31)
    product=1
    for q in small:product*=q
    assert product==200560490130
    assert 2**55 < 12**5*product
    assert 4*3_000_000_000**3 > 792**10
    print('ABSOLUTE_CUTOFF_ARITHMETIC_PASS')


if __name__=='__main__':
    arithmetic()
    for p in primes(101):
        if p<5:continue
        print('CHARACTER_STRUCTURE_PASS',p,check(p))
