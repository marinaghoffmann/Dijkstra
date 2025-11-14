#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

typedef struct {
    int v, w;
} Edge;

typedef struct {
    int v;
    long long dist;
} HeapNode;

typedef struct {
    HeapNode *a;
    int size, capacity;
} MinHeap;

MinHeap* heap_create(int cap) {
    MinHeap *h = malloc(sizeof(MinHeap));
    h->a = malloc(sizeof(HeapNode) * cap);
    h->size = 0;
    h->capacity = cap;
    return h;
}

void heap_swap(HeapNode *x, HeapNode *y) {
    HeapNode tmp = *x;
    *x = *y;
    *y = tmp;
}

void heap_push(MinHeap *h, int v, long long d) {
    int i = h->size++;
    h->a[i].v = v;
    h->a[i].dist = d;

    while (i > 0) {
        int p = (i - 1) / 2;
        if (h->a[p].dist <= h->a[i].dist) break;
        heap_swap(&h->a[p], &h->a[i]);
        i = p;
    }
}

HeapNode heap_pop(MinHeap *h) {
    HeapNode root = h->a[0];
    h->a[0] = h->a[--h->size];

    int i = 0;
    while (1) {
        int l = 2*i + 1, r = 2*i + 2, m = i;
        if (l < h->size && h->a[l].dist < h->a[m].dist) m = l;
        if (r < h->size && h->a[r].dist < h->a[m].dist) m = r;
        if (m == i) break;
        heap_swap(&h->a[i], &h->a[m]);
        i = m;
    }
    return root;
}

int main(int argc, char **argv) {
    int demo = 0;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--demo")) demo = 1;
    }

    if (demo) {
        printf("Running Dijkstra demo...\n");
        int n = 5;
        int m = 6;
        int edges_arr[6][3] = {
            {0,1,2}, {0,2,4}, {1,2,1}, {1,3,7}, {2,4,3}, {3,4,1}
        };
        int s = 0;

        long long INF = LLONG_MAX/4;
        long long *dist = malloc(sizeof(long long)*n);
        int *parent = malloc(sizeof(int)*n);

        for (int i=0; i<n; i++){ dist[i] = INF; parent[i] = -1; }

        int *deg = calloc(n, sizeof(int));
        for (int i=0;i<m;i++){
            deg[edges_arr[i][0]]++;
            deg[edges_arr[i][1]]++;
        }

        Edge **adj = malloc(sizeof(Edge*) * n);
        for (int i=0;i<n;i++){
            adj[i] = malloc(sizeof(Edge) * deg[i]);
            deg[i] = 0;
        }

        for (int i=0;i<m;i++){
            int u = edges_arr[i][0];
            int v = edges_arr[i][1];
            int w = edges_arr[i][2];
            adj[u][deg[u]].v = v; adj[u][deg[u]].w = w; deg[u]++;
            adj[v][deg[v]].v = u; adj[v][deg[v]].w = w; deg[v]++;
        }

        dist[s] = 0;
        MinHeap *hp = heap_create(n*4);
        heap_push(hp, s, 0);

        while (hp->size) {
            HeapNode h = heap_pop(hp);
            int u = h.v;
            long long d = h.dist;
            if (d > dist[u]) continue;

            for (int i=0;i<deg[u];i++){
                int v = adj[u][i].v;
                int w = adj[u][i].w;
                long long nd = d + w;
                if (nd < dist[v]){
                    dist[v] = nd;
                    parent[v] = u;
                    heap_push(hp, v, nd);
                }
            }
        }

        printf("Distances: ");
        for (int i=0;i<n;i++) printf("%lld ", dist[i]);
        printf("\n");
        return 0;
    }

    int n, m;
    scanf("%d %d", &n, &m);

    int (*edges)[3] = malloc(sizeof(int)*3*m);

    for (int i=0;i<m;i++)
        scanf("%d %d %d", &edges[i][0], &edges[i][1], &edges[i][2]);

    int source;
    scanf("%d", &source);

    long long INF = LLONG_MAX/4;
    long long *dist = malloc(sizeof(long long)*n);

    int *deg = calloc(n, sizeof(int));
    for (int i=0;i<m;i++){
        deg[edges[i][0]]++;
        deg[edges[i][1]]++;
    }

    Edge **adj = malloc(sizeof(Edge*) * n);
    for (int i=0;i<n;i++){
        adj[i] = malloc(sizeof(Edge) * deg[i]);
        deg[i] = 0;
    }

    for (int i=0;i<m;i++){
        int u = edges[i][0];
        int v = edges[i][1];
        int w = edges[i][2];
        adj[u][deg[u]].v = v; adj[u][deg[u]].w = w; deg[u]++;
        adj[v][deg[v]].v = u; adj[v][deg[v]].w = w; deg[v]++;
    }

    for (int i=0;i<n;i++) dist[i] = INF;
    dist[source] = 0;

    MinHeap *hp = heap_create(n*4);
    heap_push(hp, source, 0);

    while (hp->size) {
        HeapNode h = heap_pop(hp);
        int u = h.v;
        long long d = h.dist;
        if (d > dist[u]) continue;

        for (int i=0;i<deg[u];i++){
            int v = adj[u][i].v;
            int w = adj[u][i].w;
            long long nd = d + w;
            if (nd < dist[v]){
                dist[v] = nd;
                heap_push(hp, v, nd);
            }
        }
    }

    for (int i=0;i<n;i++) printf("%lld ", dist[i]);
    printf("\n");

    return 0;
}
