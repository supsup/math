#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
int mod(long long x,int p){x%=p;return x<0?x+p:x;}
int mpow(int x,long long e,int p){long long y=1,z=x;while(e){if(e&1)y=y*z%p;z=z*z%p;e>>=1;}return (int)y;}
struct Cand{int v,u;};
bool collides(const Cand &c,const vector<Cand>&picked){for(auto &w:picked)if(c.u==w.u||c.u==w.v||c.v==w.u||c.v==w.v)return true;return false;}
int main(int argc,char**argv){if(argc!=3){cerr<<"usage: scan input.csv output.csv\n";return 2;}ifstream f(argv[1]);ofstream out(argv[2]);string line;getline(f,line);out<<"p,g,a,first1,first2,first3,second1,second2,second3\n";int total=0,passed=0,missing=0,greedyfail=0;while(getline(f,line)){if(line.empty())continue;stringstream ss(line);string s;vector<int> nums;while(getline(ss,s,','))nums.push_back(stoi(s));if(nums.size()<6)continue;int p=nums[0],g=nums[1],a=nums[2];if(p>=300000)break;++total;int ainv=mpow(a+1,p-2,p),beta=mod((long long)(a+1)*mpow(2,p-2,p),p),gamma=mod((long long)beta*mpow(a,p-2,p),p),delta=mod((long long)(1-a)*ainv,p);
vector<int> log4(p,-1);int z=1;for(int i=0;i<p-1;i++){log4[z]=i%4;z=(long long)z*g%p;}if(z!=1){cerr<<"root failure "<<p<<"\n";return 1;}
auto shared=[&](int c,int d){int e=d-c;return array<int,2>{mod(c+(long long)e*ainv,p),mod(c+(long long)e*a*ainv,p)};};auto h12=shared(1,2),h13=shared(1,3),h23=shared(2,3);
array<vector<Cand>,4> first,second;
for(int v=0;v<p;v++){
int u=mod(v+delta,p),x=mod(1+(long long)beta*(u-1),p),y=mod(1+(long long)gamma*(v-1),p);
if(x!=y&&u!=h12[0]&&u!=h12[1]&&v!=h12[0]&&v!=h12[1]){
int l1=log4[mod(u-1,p)],l2=log4[mod(v-1,p)],l3=log4[mod(u-2,p)],l4=log4[mod(v-2,p)];
if(l1==0&&l3==0&&l2==l4&&l2>=1&&l2<=3)first[l2].push_back({v,u});}
int uu=mod(v+2LL*delta,p),xx=mod(1+(long long)beta*(uu-1),p),yy=mod(1+(long long)gamma*(v-1),p);
if(xx!=yy&&uu!=h13[0]&&uu!=h13[1]&&v!=h13[0]&&v!=h13[1]&&uu!=h23[0]&&uu!=h23[1]&&v!=h23[0]&&v!=h23[1]){
int l1=log4[mod(uu-1,p)],l2=log4[mod(v-1,p)],l3=log4[mod(uu-3,p)],l4=log4[mod(v-3,p)];
if(l1==l2&&l1>=1&&l1<=3&&l3==0&&l4==l1)second[l1].push_back({v,uu});}
}
bool hasall=true;for(int j=1;j<=3;j++)if(first[j].empty()||second[j].empty())hasall=false;
if(!hasall){++missing;cout<<"missing p="<<p<<" first="<<first[1].size()<<","<<first[2].size()<<","<<first[3].size()<<" second="<<second[1].size()<<","<<second[2].size()<<","<<second[3].size()<<"\n";continue;}
vector<Cand> picked;array<int,6> vs;bool ok=true;
for(int t=0;t<6;t++){auto &list=(t<3?first[t+1]:second[t-2]);bool found=false;for(auto c:list){if(!collides(c,picked)){picked.push_back(c);vs[t]=c.v;found=true;break;}}if(!found){ok=false;break;}}
if(!ok){++greedyfail;cout<<"greedyfail p="<<p<<" counts="<<first[1].size()<<","<<first[2].size()<<","<<first[3].size()<<","<<second[1].size()<<","<<second[2].size()<<","<<second[3].size()<<"\n";continue;}
++passed;out<<p<<","<<g<<","<<a;for(int v:vs)out<<","<<v;out<<"\n";
}
cout<<"TOTAL="<<total<<" PASS="<<passed<<" MISSING="<<missing<<" GREEDYFAIL="<<greedyfail<<"\n";}
