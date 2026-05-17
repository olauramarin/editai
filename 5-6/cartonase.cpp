#include <fstream> 

#define DIM 100010 
using namespace std; 
int n, c, i, poz, maxim, maxim1, maxim2, nr, f[DIM], v[DIM]; 
int main () { 
    ifstream fin ("cartonase.in"); 
    ofstream fout("cartonase.out"); 
    fin>>c>>n; 
    for (i=1;i<=n;i++) { 
        fin>>v[i]; 
        f[v[i]]++; 
    } 
    if (c == 1) { 
        fin>>poz; 
        for (i=1;i<=poz;i++) 
            if (v[i] >= v[poz]) 
                break; 
        fout<<i-1<<"\n"; 
        return 0; 
    } 
  
    if (c == 2) { 
        maxim = 0; 
        nr = 0; 
        for (i=1;i<=n;i++) { 
            if (v[i] > maxim) 
                maxim = v[i]; 
            if (maxim == i) { 
                nr++; 
                if (nr != 1) 
                    fout<<" "; 
                fout<<i; 
            } 
        } 
        fout<<"\n"; 
        return 0; 
    } 
    if (c == 3) { 
        maxim1 = 0; 
        maxim2 = 0; 
        nr = 0; 
        for (i=1;i<=n;i++) { 
            if (v[i] > maxim1) { 
                maxim2 = maxim1; 
                maxim1 = v[i]; 
            } else
                if (v[i] > maxim2) 
                    maxim2 = v[i]; 
            if (maxim1 > i && maxim2 <= i) { 
                nr++; 
                if (nr!=1) 
                    fout<<" "; 
                fout<<i; 
            } 
        } 
        fout<<"\n"; 
    } 
    return 0; 
}