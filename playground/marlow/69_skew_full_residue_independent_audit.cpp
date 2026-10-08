// Independent full-range audit of item 69. Uses a byte primality sieve,
// trial factorization, original w-coordinate progressions, and Euler-only
// character tests. Its first-witness digest must match the primary scan.
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>

static int mod(long long x, int p) {
    int r = int(x % p);
    return r < 0 ? r + p : r;
}
static int powmod(int b, int e, int p) {
    long long a=b, z=1;
    while(e>0) {
        if(e&1) z=z*a%p;
        a=a*a%p; e>>=1;
    }
    return int(z);
}
int main(int argc, char** argv) {
    const int limit=argc>1?std::atoi(argv[1]):59999999;
    if(limit<13 || limit>=60000000) return 2;
    // Independent byte sieve rather than SPF or primality by factorization.
    std::vector<std::uint8_t> prime(limit+1,1);
    prime[0]=prime[1]=0;
    for(int q=2;1LL*q*q<=limit;++q) if(prime[q])
        for(long long x=1LL*q*q;x<=limit;x+=q) prime[int(x)]=0;
    std::vector<int> small;
    for(int q=2;1LL*q*q<=limit;++q) if(prime[q]) small.push_back(q);
    std::uint64_t digest=1469598103934665603ULL;
    int count=0,maxg=0,maxexamined=0,maxexaminedp=0;
    long long totalexamined=0;
    for(int p=13;p<=limit;p+=8) {
        if(!prime[p]) continue;
        ++count;
        // Trial factor p-1 using primes up to sqrt(limit), not SPF.
        int rem=p-1;
        std::vector<int> factors;
        for(int q:small) {
            if(1LL*q*q>rem) break;
            if(rem%q==0) {
                factors.push_back(q);
                do rem/=q; while(rem%q==0);
            }
        }
        if(rem>1) factors.push_back(rem);
        int g=2;
        for(;;++g) {
            bool ok=true;
            for(int q:factors) if(powmod(g,(p-1)/q,p)==1) {ok=false;break;}
            if(ok) break;
        }
        if(g>maxg)maxg=g;
        const int a=int(1LL*g*g%p), D=a+1;
        const int invD=powmod(D,p-2,p), invA=powmod(a,p-2,p);
        const int delta=mod(1LL*(1-a)*invD,p);
        const int c=(p-5)/2;
        int wfound=-1,examined=0;
        for(int w=0;w<p;++w) {
            ++examined;
            // Original item67 w-form excluded progressions:
            // w=(a-q)/D or w=a(1-q)/D, 0<=q<=c.
            const int dw=mod(1LL*D*w,p);
            const int q1=mod(1LL*a-dw,p);
            if(q1<=c)continue;
            const int q2=mod(1LL-1LL*invA*dw,p); // q2 = 1 - a^(-1)Dw
            if(q2<=c)continue;
            const int f1=mod(1LL*w*(w+delta),p);
            if(f1==0 || powmod(f1,(p-1)/2,p)!=p-1)continue;
            const int f2=mod(1LL*(w-1)*(w+delta-1),p);
            if(f2==0 || powmod(f2,(p-1)/2,p)!=p-1)continue;
            wfound=w;break;
        }
        if(wfound<0) {std::cout<<"FAIL p="<<p<<"\n";return 1;}
        totalexamined+=examined;
        if(examined>maxexamined) {maxexamined=examined;maxexaminedp=p;}
        digest ^= (std::uint64_t(p)<<32) | std::uint32_t(wfound);
        digest *= 1099511628211ULL;
        if(p<=1000)std::cout<<p<<' '<<g<<' '<<wfound<<'\n';
    }
    std::cout<<"PASS limit="<<limit<<" primes="<<count<<" max_g="<<maxg
             <<" max_examined="<<maxexamined<<" max_examined_p="<<maxexaminedp
             <<" total_examined="<<totalexamined<<" digest="<<digest<<'\n';
}
