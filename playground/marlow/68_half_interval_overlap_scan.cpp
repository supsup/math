#include <iostream>
#include <algorithm>
#include <cstdlib>
#include <numeric>
using namespace std;

// Count 1 <= x <= (n-1)/2 with ax mod n in the same half interval.
// The difference of floor sums is the indicator of ax mod n > (n-1)/2.
long long fs_nonneg(long long n,long long m,long long a,long long b){
 long long ans=0;
 while(true){
  if(a>=m){ans+=(n-1)*n*(a/m)/2;a%=m;}
  if(b>=m){ans+=n*(b/m);b%=m;}
  long long y=a*n+b;
  if(y<m)break;
  n=y/m;b=y%m;swap(m,a);
 }
 return ans;
}
long long fs(long long n,long long m,long long a,long long b){
 long long q=b/m,r=b%m;if(r<0){--q;r+=m;}
 return n*q+fs_nonneg(n,m,a,r);
}
int countfast(int p,int a){int h=(p-1)/2;return fs(h,p,a,a)-fs(h,p,a,a-h-1);}
int main(int argc,char**argv){int cap=argc>1?atoi(argv[1]):10000;
 long long tested=0;int modulus_count=0;double minratio=1;
 for(int p=3;p<=cap;p+=2){
  ++modulus_count;int h=(p-1)/2;int want=(h+2)/3;int mn=h;
  for(int a=2;a<=p-2;a++)if(std::gcd(a,p)==1){
   int m=countfast(p,a);++tested;
   if(p<=501){
    int direct=0;
    for(int x=1;x<=h;x++) direct+=((a*x)%p<=h);
    if(m!=direct){cout<<"COUNT_MISMATCH "<<p<<" "<<a<<" fast="<<m<<" direct="<<direct<<"\n";return 1;}
   }
   if(m<mn)mn=m;
   if(m<want){cout<<"COUNTEREXAMPLE "<<p<<" "<<a<<" count="<<m<<" want="<<want<<"\n";return 1;}
  }
  minratio=min(minratio,(double)mn/h);
 }
 cout<<"PASS odd_moduli="<<modulus_count<<" unit_multipliers="<<tested<<" cap="<<cap<<" minratio="<<minratio<<"\n";
}
