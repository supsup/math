// Independent arithmetic audit of the third-base strict-star witness table.
#include <array>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
static int md(long long n,int p){n%=p;return n<0?n+p:(int)n;}
static int power(int a,int n,int p){long long x=1,y=a;while(n){if(n&1)x=x*y%p;y=y*y%p;n>>=1;}return (int)x;}
static vector<int> fields(const string& s){stringstream in(s);string cell;vector<int> v;while(getline(in,cell,','))v.push_back(stoi(cell));return v;}
static vector<bool> sieve(int n){vector<bool> b(n,true);b[0]=b[1]=false;for(int i=2;i*i<n;i++)if(b[i])for(int j=i*i;j<n;j+=i)b[j]=false;return b;}
static bool primitive(int g,int p){int n=p-1;for(int d=2;d*d<=n;d++)if(n%d==0){if(power(g,(p-1)/d,p)==1)return false;while(n%d==0)n/=d;}return n==1||power(g,(p-1)/n,p)!=1;}
int main(int argc,char**argv){if(argc!=2){cerr<<"usage: audit witnesses.csv\n";return 2;}auto prime=sieve(300000);set<int> expected;for(int p=2;p<300000;p++)if(prime[p]&&p%16==9)expected.insert(p);set<int> exceptions={41,73,89,137,233,281,313,457,617,937};ifstream in(argv[1]);if(!in)throw runtime_error("no input");string line;getline(in,line);if(line!="p,g,a,first1,first2,first3,second1,second2,second3")throw runtime_error("bad header");set<int> actual;int rows=0;while(getline(in,line)){if(line.empty())continue;auto w=fields(line);if(w.size()!=9)throw runtime_error("bad row");int p=w[0],g=w[1],a=w[2];if(p>=300000||!prime[p]||p%16!=9||!actual.insert(p).second||!primitive(g,p)||power(g,4,p)!=a)throw runtime_error("prime/root row");int inv2=power(2,p-2,p), invA=power(a,p-2,p),invD=power(a+1,p-2,p);int beta=md((long long)(a+1)*inv2,p),gamma=md((long long)beta*invA,p),delta=md((long long)(1-a)*invD,p);vector<int> label(p,-1);int z=1;for(int e=0;e<p-1;e++){if(label[z]!=-1)throw runtime_error("repeated power");label[z]=e%4;z=md((long long)z*g,p);}if(z!=1)throw runtime_error("not primitive");auto overlap=[&](int c,int d){int s=d-c;return array<int,2>{md(c+(long long)s*invD,p),md(c+(long long)s*a*invD,p)};};auto edge12=overlap(1,2),edge13=overlap(1,3),edge23=overlap(2,3);set<int> used;
for(int t=0;t<6;t++){int j=t%3+1,s=t<3?1:2,d=1+s,v=w[3+t],u=md(v+(long long)s*delta,p);if(v<0||v>=p)throw runtime_error("v range");int x=md(1+(long long)beta*(u-1),p),y=md(1+(long long)gamma*(v-1),p);if(x==y||x!=md(d+(long long)beta*(v-d),p)||y!=md(d+(long long)gamma*(u-d),p))throw runtime_error("rectangle identity");if(used.count(u)||used.count(v)||u==v)throw runtime_error("hub collision");used.insert(u);used.insert(v);if(t<3){if(u==edge12[0]||u==edge12[1]||v==edge12[0]||v==edge12[1])throw runtime_error("first overlap");if(label[md(u-1,p)]!=0||label[md(v-1,p)]!=j||label[md(u-2,p)]!=0||label[md(v-2,p)]!=j)throw runtime_error("first labels");}else{for(auto h:{u,v})if(h==edge13[0]||h==edge13[1]||h==edge23[0]||h==edge23[1])throw runtime_error("second overlap");if(label[md(u-1,p)]!=j||label[md(v-1,p)]!=j||label[md(u-3,p)]!=0||label[md(v-3,p)]!=j)throw runtime_error("second labels");}}
++rows;}
for(int p:exceptions)expected.erase(p);if(actual!=expected||rows!=3220)throw runtime_error("incomplete prime universe");cout<<"PASS independent arithmetic audit: "<<rows<<" strict-star rows, exactly 10 declared exceptions, all prime/root/identities/labels/overlaps/hubs\n";}
