#include <bits/stdc++.h>
using namespace std;
 
int main()
{
    
    ifstream cin("esm.in");
    ofstream cout("esm.out");
    
    int c, n, v[100001], fr[100001] = {0}, fr2[100001] = {0};
    cin >> c >> n;
    
    for(int i = 1; i <= n; i++)
        cin >> v[i];
    
    if(c == 1)
    {
        int ans = 0;
        for(int i = 1; i + 2 <= n; i++)
            if(1LL * v[i] * v[i+1] == 1LL * v[i+2])
                ans++;
        cout << ans << '\n';
    }
    
    if(c == 2)
    {
        for(int i = 1; i < n; i++)
        {
            fr2[v[i]] = fr[v[i]];
            fr[v[i]] = i;
        }
        int maxi = 0;
        for(int i = 1; i * i <= v[n]; i++)
            if(v[n] % i == 0)
            {
                if(i != v[n]/i && fr[i] && fr[v[n]/i])
                    maxi = max(maxi, min(fr[i], fr[v[n]/i]));
                if(i == v[n]/i && fr2[i])
                    maxi = max(maxi, fr2[i]);
            }
        
        cout << maxi << '\n';
    }
    
    if(c == 3)
    {
        long long ans = 0;
        for(int x = 1; x <= n; x++)
        {
            int maxi = 0;
            for(int i = 1; i * i <= v[x]; i++)
                if(v[x] % i == 0)
                {
                    if(i != v[x]/i && fr[i] && fr[v[x]/i])
                        maxi = max(maxi, min(fr[i], fr[v[x]/i]));
                    if(i == v[x]/i && fr2[i])
                        maxi = max(maxi, fr2[i]);
                }
            ans += maxi;
            fr2[v[x]] = fr[v[x]];
            fr[v[x]] = x;
        }
        cout << ans << '\n';
    }
    return 0;
}