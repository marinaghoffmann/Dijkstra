#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <windows.h>

typedef struct {
    int v;
    int w;
} Edge;

typedef struct {
    Edge* edges;
    int size;
    int capacity;
} AdjList;

void add_edge(AdjList* adj, int u, int v, int w) {
    if (adj[u].size == adj[u].capacity) {
        adj[u].capacity *= 2;
        adj[u].edges = realloc(adj[u].edges, adj[u].capacity * sizeof(Edge));
    }
    adj[u].edges[adj[u].size++] = (Edge){v, w};
}

int extract_min(int* dist, char* visited, int n) {
    int min = INT_MAX, idx = -1;
    for (int i = 0; i < n; i++) {
        if (!visited[i] && dist[i] < min) {
            min = dist[i];
            idx = i;
        }
    }
    return idx;
}

void dijkstra(AdjList* adj, int n, int src) {
    int* dist = malloc(n * sizeof(int));
    char* visited = calloc(n, 1);

    for (int i = 0; i < n; i++) dist[i] = INT_MAX;
    dist[src] = 0;

    for (int i = 0; i < n - 1; i++) {
        int u = extract_min(dist, visited, n);
        if (u == -1) break;
        visited[u] = 1;

        for (int j = 0; j < adj[u].size; j++) {
            int v = adj[u].edges[j].v;
            int w = adj[u].edges[j].w;
            if (!visited[v] && dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
            }
        }
    }

    free(dist);
    free(visited);
}

int main() {
    int n, m;
    scanf("%d %d", &n, &m);

    AdjList* adj = malloc(n * sizeof(AdjList));
    for (int i = 0; i < n; i++) {
        adj[i].size = 0;
        adj[i].capacity = 4;
        adj[i].edges = malloc(4 * sizeof(Edge));
    }

    for (int i = 0; i < m; i++) {
        int u, v, w;
        scanf("%d %d %d", &u, &v, &w);
        add_edge(adj, u, v, w);
    }

    LARGE_INTEGER freq, t1, t2;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&t1);

    dijkstra(adj, n, 0);

    QueryPerformanceCounter(&t2);

    double ms = (double)(t2.QuadPart - t1.QuadPart) * 1000.0 / freq.QuadPart;
    printf("%.6f\n", ms);

    for (int i = 0; i < n; i++) {
        free(adj[i].edges);
    }
    free(adj);
    return 0;
}
