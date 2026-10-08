// Exhaustive exact-line test at the last even prefix for every prime
// p == 5 (mod 8), 13 <= p <= 1,000,000.  By item 60's nested exclusion
// sets, a survivor here works at every earlier even prefix for that p.
// Run: c++ -O3 -std=c++17 playground/marlow/60_skew_adjacent_pairs_final_scan.cpp -o /tmp/marlow_scan && /tmp/marlow_scan
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

constexpr int LIMIT=1000000;

int modpow(int a,int n,int p) {
    std::int64_t x=a,z=1;
    while(n) {
        if(n&1) z=z*x%p;
        x=x*x%p;
        n>>=1;
    }
    return int(z);
}

int residue(std::int64_t x,int p) {
    x%=p;
    return int(x<0?x+p:x);
}

int main() {
    std::vector<int> spf(LIMIT+1);
    for(int i=2;i<=LIMIT;++i) {
        if(spf[i]) continue;
        spf[i]=i;
        if(std::int64_t(i)*i>LIMIT)continue;
        for(int j=i*i;j<=LIMIT;j+=i)if(!spf[j])spf[j]=i;
    }
    int count=0,min_survivors=LIMIT,min_p=0,max_g=0;
    std::int64_t total_survivors=0;
    for(int p=13;p<=LIMIT;p+=8) {
        if(spf[p]!=p)continue;
        ++count;
        int n=p-1,remaining=n;
        std::vector<int> factors;
        while(remaining>1) {
            int q=spf[remaining];factors.push_back(q);
            do{remaining/=q;}while(remaining>1&&remaining%q==0);
        }
        int g=2;
        while(true) {
            bool okay=true;
            for(int q:factors)if(modpow(g,n/q,p)==1){okay=false;break;}
            if(okay)break;
            ++g;
        }
        max_g=std::max(max_g,g);
        int a=int(std::int64_t(g)*g%p),D=a+1;
        int invD=modpow(D,p-2,p);
        int delta=residue(std::int64_t(1-a)*invD,p);
        int c=(p-7)/2;
        std::vector<std::uint8_t> square(p),excluded(p);
        for(int z=1;z<p;++z)square[std::int64_t(z)*z%p]=1;
        for(int r=0;r<=c;++r) {
            excluded[residue((std::int64_t(r)+std::int64_t(a)*(c+1))*invD,p)]=1;
            excluded[residue(std::int64_t(a)*(r+1)+c,p)*std::int64_t(invD)%p]=1;
        }
        int survivors=0;
        for(int v=0;v<p;++v) {
            if(excluded[v])continue;
            int u=(v+delta)%p;
            int f1=residue(std::int64_t(v-c)*(u-c),p);
            int f2=residue(std::int64_t(v-c-1)*(u-c-1),p);
            if(f1&&!square[f1]&&f2&&!square[f2])++survivors;
        }
        if(!survivors) {
            std::cout<<"FAIL p="<<p<<" g="<<g<<" a="<<a<<"\n";
            return 1;
        }
        total_survivors+=survivors;
        if(survivors<min_survivors){min_survivors=survivors;min_p=p;}
        if(p<=1000)std::cout<<p<<' '<<survivors<<'\n';
    }
    std::cout<<"limit="<<LIMIT<<" primes="<<count<<" min="<<min_survivors
             <<" min_p="<<min_p<<" max_g="<<max_g
             <<" total_survivors="<<total_survivors<<'\n';
}
