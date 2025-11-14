"""
Dijkstra implementation in Python with a simple CLI to read graphs
from stdin, from a file, or run a demo example.

Usage:
  python dijkstra.py --source 0 < graph.txt
  python dijkstra.py --input graph.txt --source 0
  python dijkstra.py --demo
"""

import sys
import heapq
import argparse
from typing import List, Tuple, Iterable


def dijkstra(n: int, edges: List[Tuple[int, int, int]], source: int):
    """Compute shortest paths from source using Dijkstra (min-heap)."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))  # remover esta linha se quiser grafo dirigido

    INF = 10**18
    dist = [INF] * n
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


def load_graph_from_text(text: str):
    data = text.strip().split()
    if len(data) < 3:
        raise ValueError("Entrada insuficiente: esperado n m u v w ...")

    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    edges = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        edges.append((u, v, w))

    rest = list(it)
    s = int(rest[0]) if rest else 0

    return n, m, edges, s


def main(argv: Iterable[str]):
    parser = argparse.ArgumentParser(description="Dijkstra in Python")
    parser.add_argument("--demo", action="store_true", help="Run demo graph")
    parser.add_argument("--source", type=int, default=0, help="Source vertex")
    args = parser.parse_args(list(argv))

    # ----------- MODO DEMO -----------
    if args.demo:
        print("Running Dijkstra demo...")

        n = 5
        edges = [
            (0, 1, 2),
            (0, 2, 4),
            (1, 2, 1),
            (1, 3, 7),
            (2, 4, 3),
            (3, 4, 1),
        ]

        print("Vertices:", n)
        print("Arestas:", edges)

        dist, parent = dijkstra(n, edges, args.source)

        print("Distâncias:", dist)
        print(f"Caminho {args.source}→4:", reconstruct_path(parent, 4))
        return

    # ----------- MODO NORMAL: LER DO STDIN -----------
    data = []
    for line in sys.stdin:
        data.extend(line.strip().split())

    if not data:
        print("Erro: Nenhum dado recebido via stdin.")
        return

    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    edges = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        w = int(next(it))
        edges.append((u, v, w))

    dist, parent = dijkstra(n, edges, args.source)

    print(" ".join(map(str, dist)))


if __name__ == "__main__":
    main(sys.argv[1:])
