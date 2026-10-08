// Exact final-even-prefix existence test for p == 5 (mod 8), p <= 10,000,000.
// The two relabel-exception progressions are tested by inverting their
// affine maps, so no O(p)-sized excluded set or square table is needed.
// A final-prefix witness works at every earlier even prefix (item 60).
// Run: c++ -O3 -std=c++17 playground/marlow/60_skew_adjacent_pairs_fast_existence_scan.cpp -o /tmp/marlow_fast_scan && /tmp/marlow_fast_scan
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

constexpr int LIMIT=10000000;

int modpow(int a,int n,int p) {
    std::int64_t x=a,z=1;
    while(n) {
        if(n&1)z=z*x%p;
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
        if(spf[i])continue;
        spf[i]=i;
        if(std::int64_t(i)*i>LIMIT)continue;
        for(int j=i*i;j<=LIMIT;j+=i)if(!spf[j])spf[j]=i;
    }
    int count=0,max_g=0,max_examined=0,max_examined_p=0;
    std::int64_t total_examined=0;
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
        for(;;++g) {
            bool primitive=true;
            for(int q:factors)if(modpow(g,n/q,p)==1){primitive=false;break;}
            if(primitive)break;
        }
        max_g=std::max(max_g,g);
        int a=int(std::int64_t(g)*g%p),D=a+1;
        int invD=modpow(D,p-2,p),invA=modpow(a,p-2,p);
        int delta=residue(std::int64_t(1-a)*invD,p);
        int c=(p-7)/2;
        int examined=0,witness=-1;
        for(int v=0;v<p;++v) {
            ++examined;
            int H=residue(std::int64_t(D)*v-std::int64_t(a)*(c+1),p);
            if(H<=c)continue;
            int L=residue(std::int64_t(D)*v-c,p);
            L=residue(std::int64_t(L)*invA,p);
            if(1<=L&&L<=c+1)continue;
            int u=(v+delta)%p;
            int F1=residue(std::int64_t(v-c)*(u-c),p);
            if(!F1||modpow(F1,(p-1)/2,p)!=p-1)continue;
            int F2=residue(std::int64_t(v-c-1)*(u-c-1),p);
            if(!F2||modpow(F2,(p-1)/2,p)!=p-1)continue;
            witness=v;
            break;
        }
        if(witness<0){std::cout<<"FAIL p="<<p<<" g="<<g<<"\n";return 1;}
        total_examined+=examined;
        if(examined>max_examined){max_examined=examined;max_examined_p=p;}
        if(p<=1000)std::cout<<p<<' '<<witness<<'\n';
        if(count%10000==0)std::cerr<<"done="<<count<<" p="<<p<<'\n';
    }
    std::cout<<"limit="<<LIMIT<<" primes="<<count<<" max_g="<<max_g
             <<" max_examined="<<max_examined<<" max_examined_p="<<max_examined_p
             <<" total_examined="<<total_examined<<'\n';
}
