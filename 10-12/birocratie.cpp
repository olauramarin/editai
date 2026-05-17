#include <bits/stdc++.h>
#define INF 1000000001
#define L 1005
using namespace std;
ifstream fin("birocratie.in");
ofstream fout("birocratie.out");

int n;
int m[L][L], dp[L][L], dp0[L][L], dp1[L][L], dp2[L][L];

void board() {
  for (int i = 0; i < n + 2; i++)
    for (int j = 0; j < n + 2; j++)
      m[i][j] = dp[i][j] = dp0[i][j] = dp1[i][j] = dp2[i][j] = -INF;
}

int main() {
  fin >> n;
  board();
  for (int i = 1; i <= n; i++)
    for (int j = 1; j <= n; j++)
      fin >> m[i][j];
  dp[1][1] = dp0[1][1] = dp1[1][1] = dp2[1][1] = m[1][1];
  for (int antidiag = 3; antidiag <= 2 * n; antidiag++) {
    for (int i = 1; i <= n; i++) {
      int j = antidiag - i;
      if (j < 1 || j > n)
        continue;
      dp0[i][j] = max({dp0[i][j], dp[i - 1][j] + m[i][j], dp[i][j - 1] + m[i][j]});
    }
    for (int i = 1; i <= n; i++) {
      int j = antidiag - i;
      if (j < 1 || j > n)
        continue;
      dp1[i][j] = max({dp1[i][j], dp1[i - 1][j + 1] + m[i][j], dp0[i - 1][j + 1] + m[i][j]});
    }
    for (int i = n; i > 0; i--) {
      int j = antidiag - i;
      if (j < 1 || j > n)
        continue;
      dp2[i][j] = max({dp2[i][j], dp2[i + 1][j - 1] + m[i][j], dp0[i + 1][j - 1] + m[i][j]});
    }
    for (int i = 1; i <= n; i++) {
      int j = antidiag - i;
      if (j < 1 || j > n)
        continue;
      dp[i][j] = max({dp[i][j], dp0[i][j], dp1[i][j], dp2[i][j]});
    }
  }
  fout << dp[n][n] << "\n";
  return 0;
}