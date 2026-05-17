// Stelian Chichirim
// O((N + M) * log*(N + M) + (N + M) * log(N + M))
// Expected: 100p

#include <bits/stdc++.h>

using namespace std;

const int Nmax = 2e5, Mmax = 2e5, Cmax = 1e9, Rmax = 1e9;

struct edge {
    int x, c, pos;
};

struct bridge {
    int x, y, c;
};

int lvl[Nmax + 5], lvlMin[Nmax + 5], comp[Nmax + 5], root[Nmax + 5], cnt[Nmax + 5], where[Nmax + 5], nrcomp;
bool isBridge[Nmax + 5];
long long val[Nmax + 5], ans[Nmax + 5];
vector<edge> g[Nmax + 5];
vector<int> v[Nmax + 5];
vector<bridge> bridges;

void getBridges(int nod, int parent) {
    for (edge& vec : g[nod])
        if (lvl[vec.x] == 0) {
            lvl[vec.x] = lvlMin[vec.x] = lvl[nod] + 1;
            getBridges(vec.x, nod);
            if (lvlMin[vec.x] == lvl[vec.x]) {
                isBridge[vec.pos] = true;
                bridges.push_back({nod, vec.x, vec.c});
            }
            lvlMin[nod] = min(lvlMin[nod], lvlMin[vec.x]);
        }
        else if (vec.x != parent) lvlMin[nod] = min(lvlMin[nod], lvl[vec.x]);
}

void dfs(int nod) {
    comp[nod] = nrcomp;
    cnt[nrcomp]++;
    for (edge& vec : g[nod])
        if (!isBridge[vec.pos] && !comp[vec.x]) dfs(vec.x);
}

int getRoot(int x) {
    int y = x;
    while (y != root[y]) y = root[y];
    while (root[x] != y) {
        int aux = root[x];
        root[x] = y;
        x = aux;
    }
    return y;
}

void unite(int x, int y, int cst) {
    x = getRoot(x);
    y = getRoot(y);
    if (x == y) return;
    if (cnt[x] > cnt[y]) swap(x, y);
    v[y].push_back(x);
    val[y] += 1LL * cst * cnt[x];
    val[x] += 1LL * cst * cnt[y] - val[y];
    root[x] = y;
    cnt[y] += cnt[x];
}

void propagate(int nod, int parent) {
    for (int& vec : v[nod])
        if (vec != parent) {
            val[vec] += val[nod];
            propagate(vec, nod);
        }
}

int main()
{
    ifstream in("regate.in");
    ofstream out("regate.out");
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int N, M, x, y, c;
    in >> N >> M;
    assert(1 <= N && N <= Nmax);
    assert(1 <= M && M <= Mmax);

    for (int i = 1; i <= N; ++i) {
        in >> x;
        assert(1 <= x && x <= Rmax);
        bridges.push_back({-1, i, x});
    }

    for (int i = 1; i <= M; ++i) {
        in >> x >> y >> c;
        assert(1 <= x && x <= N);
        assert(1 <= y && y <= N);
        assert(x != y);
        assert(1 <= c && c <= Cmax);
        g[x].push_back({y, c, i});
        g[y].push_back({x, c, i});
    }

    // find bridges
    lvl[1] = lvlMin[1] = 1;
    getBridges(1, 0);

    // find components
    for (int i = 1; i <= N; ++i)
        if (!comp[i]) {
            nrcomp++;
            cnt[nrcomp] = 0;
            root[nrcomp] = nrcomp;
            dfs(i);
        }

    sort(bridges.begin(), bridges.end(),
         [](const bridge& e1, const bridge& e2) -> bool {
            if (e1.c == e2.c) return e1.x < e2.x;
            return e1.c > e2.c;
         });
    for (bridge& e : bridges) {
        if (e.x == -1) {
            int rt = getRoot(comp[e.y]);
            where[e.y] = rt;
            ans[e.y] = 1LL * e.c * (cnt[rt] - 1) - val[rt];
        }
        else unite(comp[e.x], comp[e.y], e.c);
    }

    propagate(getRoot(1), 0);
    for (int i = 1; i <= N; ++i) {
        ans[i] += val[where[i]];
        out << ans[i] << "\n";
    }
    return 0;
}
