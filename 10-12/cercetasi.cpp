#include <bits/stdc++.h>
#define ll long long
using namespace std;

const int NMAX=100008;
const ll mod=1000000007;

int n,r,st,dr;
ll fact[NMAX],ifact[NMAX],inv[NMAX];

void pre(int en)
{
    fact[0]=fact[1]=1LL;
    ifact[0]=ifact[1]=1LL;
    inv[0]=inv[1]=1LL;
    for(ll i=2; i<=en; i++){
        fact[i]=(fact[i-1]*i)%mod;
        inv[i]=(inv[mod%i]*(mod-mod/i))%mod;
        ifact[i]=(ifact[i-1]*inv[i])%mod;
    }
}

ll comb(int n,int k)
{
    if(n<0 || k<0 || k>n)
        return 0;
    return (((fact[n]*ifact[k])%mod)*ifact[n-k])%mod;
}

ll pw(ll baza, ll expo)
{
    ll ans=1LL;
    while(expo){
        if(expo&1)
            ans=(ans*baza)%mod;
        expo>>=1;
        baza=(baza*baza)%mod;
    }
    return ans;
}

ll get_stir(ll n, ll k)
{
    if(n==0 && k==0)
        return 1LL;
    if(n==k)    
        return 1LL;
    if(k>n || n==0 || k==0)
        return 0;

    ll ans=0;
    for(int i=0; i<=k; i++){
        ll add=(comb(k,i)*pw(i,n))%mod;
        if((k-i)%2==0){
            ans=(ans+add)%mod;
        }
        else 
            ans=(ans-add+mod)%mod;
    }
    return (ans*ifact[k])%mod;
}

ll pref[NMAX];

void solve(string file)
{
    ifstream fin(file+".in");
    ofstream fout(file+".out");

    fin >> n >> r >> st >> dr;
    pre(n);

    n-=r;
    n++;
    st-=r;
    st++;
    dr-=r;
    dr++;

    pref[0]=1LL;
    for(ll i=1; i<=dr; i++){
        if(i&1){
            pref[i]=(pref[i-1]-ifact[i]+mod)%mod;
        }
        else {
            pref[i]=(pref[i-1]+ifact[i])%mod;
        }
    }

    ll ans=0;
    for(ll i=0; i<=dr; i++){
        ll pp=(pw(i,n)*ifact[i])%mod,add;
        if(st-i-1>=0)
            add=(pref[dr-i]-pref[st-i-1]+mod)%mod;
        else 
            add=pref[dr-i];

        add=(add*pp)%mod;
        ans=(ans+add)%mod;
    }
    fout << ans << "\n";
    fin.close();
    fout.close();
}

int main() 
{
    solve("cercetasi");
    return 0;   
}