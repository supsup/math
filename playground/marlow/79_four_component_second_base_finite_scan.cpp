#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;
struct Cand { int v,u,x,y,e1,e2; };
int modpow(int a,int e,int p){ long long z=1,b=a; while(e){if(e&1)z=z*b%p;b=b*b%p;e>>=1;}return (int)z;}
int inv(int a,int p){return modpow(a,p-2,p);}
int red(long long x,int p){x%=p;if(x<0)x+=p;return (int)x;}
vector<int> factors(int n){vector<int> r;for(int d=2;(long long)d*d<=n;++d)if(n%d==0){r.push_back(d);while(n%d==0)n/=d;}if(n>1)r.push_back(n);return r;}
int root(int p){auto f=factors(p-1);for(int g=2;g<p;++g){bool yes=true;for(int d:f)if(modpow(g,(p-1)/d,p)==1){yes=false;break;}if(yes)return g;}return -1;}
int edge(int a,int b){if(a>b)swap(a,b);static const int lookup[4][4]={{-1,0,1,2},{0,-1,3,4},{1,3,-1,5},{2,4,5,-1}};return lookup[a][b];}
bool tree(int e0,int e1,int e2){static const int U[6]={0,0,0,1,1,2},V[6]={1,2,3,2,3,3};int par[4]={0,1,2,3};auto find=[&](int x){while(par[x]!=x)x=par[x];return x;};for(int e:{e0,e1,e2}){int a=find(U[e]),b=find(V[e]);if(a==b)return false;par[a]=b;}return true;}
bool disjoint(const Cand &a,const Cand &b){return a.u!=b.u&&a.u!=b.v&&a.v!=b.u&&a.v!=b.v;}
int main(int argc,char**argv){int limit=argc>1?atoi(argv[1]):600000; vector<bool> prime(limit+1,true);prime[0]=prime[1]=false;for(int d=2;(long long)d*d<=limit;++d)if(prime[d])for(int n=d*d;n<=limit;n+=d)prime[n]=false;
ofstream out(argc>2?argv[2]:"/tmp/marlow79_witnesses.csv");out<<"p,g,a,v1,v2,v3,scanned,valid_count\n";
uint64_t digest=1469598103934665603ULL;auto mix=[&](uint64_t x){digest^=x;digest*=1099511628211ULL;};
int total=0,positive=0,miss=0;long long scanned_sum=0;vector<int> misses;array<int,36> bins;
for(int p=41;p<limit;p+=16){if(!prime[p])continue;++total;int g=root(p),a=modpow(g,4,p);int beta=red((1LL+a)*inv(2,p),p),gamma=red(1LL*beta*inv(a,p),p),delta=red(1LL*(1-a)*inv(1+a,p),p);int h1=red(1LL*(a+2)*inv(a+1,p),p),h2=red(1LL*(2LL*a+1)*inv(a+1,p),p);
vector<int8_t> label(p,-1);int z=1;for(int e=0;e<p-1;++e){label[z]=e&3;z=red(1LL*z*g,p);}if(z!=1){cerr<<"bad root "<<p<<"\n";return 2;}
array<vector<Cand>,36> bucket; bins.fill(0);int full=0,scanned=0,valid_count=0;
for(int v=0;v<p;++v){++scanned;int u=red(v+delta,p);if(u==1||u==2||v==1||v==2||u==h1||u==h2||v==h1||v==h2)continue;int x=red(1LL+1LL*beta*red(u-1,p),p),y=red(1LL+1LL*gamma*red(v-1,p),p);if(x==y)continue;int e1=edge(label[red(u-1,p)],label[red(v-1,p)]),e2=edge(label[red(u-2,p)],label[red(v-2,p)]);if(e1<0||e2<0)continue;++valid_count;int type=e1*6+e2;if((int)bucket[type].size()<9){bucket[type].push_back({v,u,x,y,e1,e2});if(++bins[type]==9)++full;}if(full==36)break;}
scanned_sum+=scanned;bool found=false;Cand ca{},cb{},cc{};
for(int t0=0;t0<36&&!found;++t0)if(!bucket[t0].empty())for(int t1=t0+1;t1<36&&!found;++t1)if(!bucket[t1].empty())for(int t2=t1+1;t2<36&&!found;++t2)if(!bucket[t2].empty()){
if(!tree(t0/6,t1/6,t2/6)||!tree(t0%6,t1%6,t2%6))continue;
for(auto &a0:bucket[t0]){for(auto &a1:bucket[t1])if(disjoint(a0,a1)){for(auto &a2:bucket[t2])if(disjoint(a0,a2)&&disjoint(a1,a2)){ca=a0;cb=a1;cc=a2;found=true;break;}if(found)break;}if(found)break;}}
if(found){++positive;out<<p<<","<<g<<","<<a<<","<<ca.v<<","<<cb.v<<","<<cc.v<<","<<scanned<<","<<valid_count<<"\n";mix(p);mix(g);mix(a);mix(ca.v);mix(cb.v);mix(cc.v);}else{++miss;misses.push_back(p);out<<p<<","<<g<<","<<a<<",-1,-1,-1,"<<scanned<<","<<valid_count<<"\n";mix(p);mix(g);mix(a);mix(0xffffffffULL);}if(total%1000==0)cerr<<"done="<<total<<" p="<<p<<" positive="<<positive<<" miss="<<miss<<"\n";
}
out.close();cout<<"limit="<<limit<<" total="<<total<<" positive="<<positive<<" miss="<<miss<<" scanned_sum="<<scanned_sum<<" digest="<<digest<<"\n";cout<<"misses:";for(int x:misses)cout<<" "<<x;cout<<"\n";
}
