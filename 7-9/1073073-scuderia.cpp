#include <fstream>
#include <iostream>
#include <math.h>
#include <limits.h>

using namespace std;

const int NMAX = 1e6 + 1;
const int OFFSET_MAX = 1e5 + 1;
int a[NMAX + 2 * OFFSET_MAX];
int n, k, p, q, r;

int s(int i, int j)
{
    if (i < 0 || j < 0)
        return 0;
    return a[i * k + j];
}

int getCoords(int x, int y)
{
    return x * k + y;
}

int main()
{
    ifstream fin("scuderia.in");
    ofstream fout("scuderia.out");

    fin >> n >> k >> p >> q >> r;

    if (p > k)
        p = k;

    int offset = k - r, totalSum = 0;

    for (int i = 0; i < n; ++i)
    {
        fin >> a[i + offset];
        totalSum += a[i + offset];
    }

    n += offset;
    int lastLine = n / k + (n % k != 0) - 1;

    for (int i = 0; i <= lastLine; ++i)
        for (int j = 0; j < k; ++j)
        {
            int ind = getCoords(i, j);
            if (i)
                a[ind] += a[getCoords(i - 1, j)];
            if (j)
                a[ind] += a[getCoords(i, j - 1)];

            if (i && j)
                a[ind] -= a[getCoords(i - 1, j - 1)];
        }

    int maxSum = INT_MIN, colGap = k - p;

    for (int i = q; getCoords(i, k - 1) < n; ++i)
    {
        for (int j = p - 1; j < k; ++j)
        {
            int lineSum = s(i, k - 1) - s(i - q, k - 1),
                colSum = s(lastLine, j) - s(lastLine, j - p),
                intersectSum = s(i, j) - s(i - q, j) + s(i - q, j - p) - s(i, j - p);

            if (lineSum + colSum - intersectSum > maxSum)
            {
                maxSum = lineSum + colSum - intersectSum;
            }
        }

        for (int j = colGap; j < k - 1; ++j)
        {
            int hSum = totalSum -
                       (s(lastLine, j) - s(lastLine, j - colGap)) +
                       (s(i, j) - s(i - q, j) - s(i, j - colGap) + s(i - q, j - colGap));

            if (hSum > maxSum)
            {
                maxSum = hSum;
            }
        }
    }

    fout << maxSum << '\n';
    return 0;
}