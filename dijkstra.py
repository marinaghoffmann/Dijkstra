import sys
import heapq
import argparse
from typing import List, Tuple, Iterable
import math


def dijkstra(n: int, edges: List[Tuple[int, int, int]], source: int, undirected: bool = True):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        if undirected:
            adj[v].append((u, w))

    dist = [math.inf] * n
    parent = [-1] * n
    dist[source] = 0

    pq = [(0, source)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue

        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, parent


def reconstruct_path(parent, target):
    path = []
    while target != -1:
        path.append(target)
        target = parent[target]
    return list(reversed(path))


def parse_graph_stdin():
    data = []
    for line in sys.stdin:
        data.extend(line.strip().split())

    if not data:
        raise ValueError("Erro: nenhum dado recebido via STDIN.")

    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    edges = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        edges.append((u, v, w))

    return n, m, edges


def main(argv: Iterable[str]):
    parser = argparse.ArgumentParser(description="Dijkstra em Python")
    parser.add_argument("--demo", action="store_true", help="Executa exemplo simples")
    parser.add_argument("--source", type=int, default=0, help="Vértice inicial")
    args = parser.parse_args(list(argv))

    if args.demo:
        n = 5
        edges = [
            (0, 1, 2),
            (0, 2, 4),
            (1, 2, 1),
            (1, 3, 7),
            (2, 4, 3),
            (3, 4, 1),
        ]
        dist, parent = dijkstra(n, edges, args.source)
        print("Distâncias:", dist)
        print("Caminho {}→4:".format(args.source), reconstruct_path(parent, 4))
        return

    n, m, edges = parse_graph_stdin()
    dist, _ = dijkstra(n, edges, args.source)
    print(" ".join(map(str, dist)))

def run_dijkstra_py(n, edges, source):
    dist, _ = dijkstra(n, edges, source, undirected=True)
    return dist


if __name__ == "__main__":
    main(sys.argv[1:])
