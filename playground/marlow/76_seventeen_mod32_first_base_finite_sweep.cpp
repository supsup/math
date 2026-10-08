#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>

// Exact finite complement of item 74 for p=17 (mod 32), A=8.
// Build and run commands are in 76_seventeen_mod32_first_base_all_primes.md.
static constexpr int LIMIT = 262144001; // (80*8)^3 + 1
static constexpr int BLOCK = 1 << 20;

static int power(int x, int n, int p) {
    std::int64_t a=x, r=1;
    while (n) { if (n&1) r=r*a%p; a=a*a%p; n>>=1; }
    return int(r);
}

static int mod(std::int64_t x, int p) {
    x%=p;
    return int(x<0 ? x+p : x);
}

static bool ready(int a, int p) {
    std::int64_t x=a;
    int u=mod(1+3*x,p), v=mod(x+3,p);
    if (!u || !v) return false;
    const std::int64_t exclusions[]={
        x*x-4*x-1, x*x+3, x*x+1,
        x*x-2*x-1, x*x+4*x-1, 3*x*x+1
    };
    for (auto f : exclusions) if (!mod(f,p)) return false;
    return power(int(std::int64_t(u)*v%p),(p-1)/2,p)==p-1;
}

static bool direct_check(int a, int p) {
    int ai=power(mod(a-1,p),p-2,p);
    int D=mod(std::int64_t(ai)*ai,p);
    int Z=mod(std::int64_t(mod(1+3LL*a,p))*D,p);
    int W=mod(std::int64_t(a)*mod(a+3,p)%p*D,p);
    if (!Z || !W) return false;
    if (power(mod(std::int64_t(W)*power(Z,p-2,p),p),(p-1)/2,p)!=p-1) return false;
    int b=mod(1+Z,p), v=mod(1+W,p), inv2=(p+1)/2;
    int mu1=mod(std::int64_t(mod(a+1,p))*inv2%p*ai,p);
    int mu3=mod(3LL*mu1,p);
    int targets1[]={mod(2LL*b-1,p),mod(2LL*b+1,p),mod(2LL*b+3,p),mod(2LL*v+1,p)};
    int mids1[]={mod(2LL-2LL*mu1,p),mod(2LL+2LL*mu1,p)};
    int targets3[]={targets1[0],targets1[2]};
    int mids3[]={mod(2LL-2LL*mu3,p),mod(2LL+2LL*mu3,p)};
    for (int t:targets1) for(int m:mids1) if(t==m) return false;
    for (int t:targets3) for(int m:mids3) if(t==m) return false;
    return true;
}

int main() {
    std::vector<int> small;
    std::vector<char> isprime(16385,true);
    for (int i=2;i<(int)isprime.size();++i) {
        if (!isprime[i]) continue;
        small.push_back(i);
        if (i*i<(int)isprime.size()) for(int j=i*i;j<(int)isprime.size();j+=i) isprime[j]=false;
    }
    std::uint64_t digest=14695981039346656037ULL;
    std::uint64_t count=0, witness=0, misses=0, small_count=0;
    int max_g=0,max_tested=0,max_p=0,first_eligible=0,last_eligible=0;
    for (int lo=2;lo<=LIMIT;lo+=BLOCK) {
        int hi=std::min(LIMIT,lo+BLOCK-1);
        std::vector<char> composite(hi-lo+1,false);
        for (int d:small) {
            if (std::int64_t(d)*d>hi) break;
            std::int64_t start=std::max<std::int64_t>(std::int64_t(d)*d,
                ((std::int64_t(lo)+d-1)/d)*d);
            for(std::int64_t j=start;j<=hi;j+=d) composite[j-lo]=true;
        }
        int p=lo+((17-lo)%32+32)%32;
        for(;p<=hi;p+=32) {
            if (composite[p-lo]) continue;
            ++count;
            int q=(p-1)/16;
            if(q<=36) { ++small_count; std::cout << "small p=" << p << " q=" << q << '\n'; continue; }
            if (!first_eligible) first_eligible=p;
            last_eligible=p;
            int n=p-1,left=n;
            std::vector<int> factors;
            for (int d:small) {
                if (std::int64_t(d)*d>left) break;
                if(left%d) continue;
                factors.push_back(d);
                do {left/=d;} while(left%d==0);
            }
            if(left>1) factors.push_back(left);
            bool found=false;
            int primitive_tested=0;
            for(int g=2;g<p;++g) {
                bool primitive=true;
                for(int d:factors) if(power(g,n/d,p)==1) {primitive=false;break;}
                if(!primitive) continue;
                ++primitive_tested;
                int a=power(g,8,p);
                if(!ready(a,p)) continue;
                if(!direct_check(a,p)) {std::cerr << "direct mismatch at p=" << p << " g=" << g << '\n';return 2;}
                found=true;
                ++witness;
                max_g=std::max(max_g,g);
                if(primitive_tested>max_tested) {max_tested=primitive_tested;max_p=p;}
                // FNV-1a over little-endian 32-bit p then g.
                for(std::uint32_t val:{std::uint32_t(p),std::uint32_t(g)})
                    for(int j=0;j<4;++j) {digest^=(val>>(8*j))&255;digest*=1099511628211ULL;}
                break;
            }
            if(!found) {++misses; std::cout << "MISS p=" << p << " q=" << q << '\n';}
        }
    }
    std::cout << "limit=" << LIMIT << " primes_17mod32=" << count
              << " small_q_le36=" << small_count << " q_gt36=" << count-small_count
              << " witnesses=" << witness << " misses=" << misses
              << " max_first_g=" << max_g << " max_primitive_tested=" << max_tested
              << " hardest_p=" << max_p << " first_eligible=" << first_eligible
              << " last_eligible=" << last_eligible << " fnv64=" << digest << '\n';
    return misses ? 1 : 0;
}
