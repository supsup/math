#include <cstdint>
#include <iostream>
#include <map>
#include <vector>
using i64 = std::int64_t;
constexpr int LIM = 32768001;
int pw(int x,int e,int p){i64 y=1,z=x;while(e){if(e&1)y=y*z%p;z=z*z%p;e>>=1;}return int(y);}
int md(i64 x,int p){x%=p;return int(x<0?x+p:x);}
bool ready(int a,int p){
  i64 x=a;
  int l=md(1+3*x,p),r=md(x+3,p);
  if(!l||!r)return false;
  i64 bad[]={x*x-4*x-1,x*x+3,x*x+1,x*x-2*x-1,x*x+4*x-1,3*x*x+1};
  for(auto y:bad)if(!md(y,p))return false;
  return pw(md(i64(l)*r,p),(p-1)/2,p)==p-1;
}
void hash32(std::uint64_t &h, std::uint32_t x){for(int i=0;i<4;++i){h^=(x>>(8*i))&255u;h*=1099511628211ULL;}}
int main(){
 std::vector<int> spf(LIM+1);
 for(int d=2;d<=LIM;++d){if(spf[d])continue;spf[d]=d;if(i64(d)*d>LIM)continue;for(int j=d*d;j<=LIM;j+=d)if(!spf[j])spf[j]=d;}
 std::map<int,int> counts,misses,maxg;std::vector<int> miss_p;
 std::uint64_t digest=14695981039346656037ULL;
 for(int p=17;p<=LIM;p+=8){if(spf[p]!=p)continue;
  int n=p-1,k=0;for(int m=n;!(m&1);m>>=1)++k;int A=1<<(k-1),q=n/(2*A);
  if(q<=6*(A-2))continue;
  ++counts[A];std::vector<int> ds;for(int rem=n;rem>1;){int d=spf[rem];ds.push_back(d);do{rem/=d;}while(rem>1&&rem%d==0);}
  int found=0;for(int g=2;g<p;++g){bool primitive=true;for(int d:ds)if(pw(g,n/d,p)==1){primitive=false;break;}if(!primitive)continue;
    if(ready(pw(g,A,p),p)){found=g;break;}}
  if(!found){++misses[A];miss_p.push_back(p);}else if(found>maxg[A])maxg[A]=found;
  hash32(digest,p);hash32(digest,found);
 }
 for(auto [a,c]:counts)std::cout<<"A="<<a<<" count="<<c<<" misses="<<misses[a]<<" max_g="<<maxg[a]<<'\n';
 std::cout<<"missing primes=";for(int p:miss_p)std::cout<<p<<',';std::cout<<'\n';
 std::cout<<"digest="<<digest<<'\n';
}
