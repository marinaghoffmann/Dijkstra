"""
Benchmark for Dijkstra (Python vs C)

Usage:
  python benchmark_dijkstra.py
  python benchmark_dijkstra.py --include-c
"""

import argparse
import csv
import os
import random
import statistics as stats
import subprocess
import time
from typing import List, Tuple

import matplotlib.pyplot as plt
from dijkstra import dijkstra


def gen_graph(n: int, m: int, seed: int = None):
    if seed is not None:
        random.seed(seed)
    edges = set()
    while len(edges) < m:
        u = random.randrange(n)
        v = random.randrange(n)
        if u != v:
            w = random.randint(1, 20)
            edges.add((u, v, w))
    return list(edges)


def time_python_dijkstra(n, edges, s):
    t0 = time.perf_counter()
    dijkstra(n, edges, s)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0  # ms


def time_c_dijkstra(n, edges, s, exe="./dijkstra_c"):
    text = f"{n} {len(edges)}\n"
    for u, v, w in edges:
        text += f"{u} {v} {w}\n"
    text += f"{s}\n"

    t0 = time.perf_counter()
    subprocess.run([exe], input=text.encode("utf-8"), stdout=subprocess.PIPE)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0  # ms


def plot_curve(xs, ys, title, outpath):
    plt.figure()
    plt.plot(xs, ys, marker="o")
    plt.title(title)
    plt.xlabel("n")
    plt.ylabel("ms")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(outpath, dpi=160)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Benchmark Dijkstra")
    parser.add_argument("--sizes", default="200,400,800,1200,2000")
    parser.add_argument("--density", type=float, default=2.0,
                        help="Edges per node (m ≈ n*density)")
    parser.add_argument("--reps", type=int, default=10)
    parser.add_argument("--include-c", action="store_true")
    args = parser.parse_args()

    sizes = [int(x) for x in args.sizes.split(",")]
    density = args.density
    reps = args.reps
    include_c = args.include_c and os.path.exists("./dijkstra_c")

    results = []

    # ---------------- PYTHON ----------------
    for n in sizes:
        m = int(n * density)

        times = []
        for r in range(reps):
            edges = gen_graph(n, m, seed=r)
            ms = time_python_dijkstra(n, edges, 0)
            times.append(ms)

        mean = stats.mean(times)
        std = stats.pstdev(times)
        results.append(("python", n, mean, std))
        print(f"[PY] n={n} mean={mean:.3f}ms")

    # ------------------ C -------------------
    if include_c:
        for n in sizes:
            m = int(n * density)

            times = []
            for r in range(reps):
                edges = gen_graph(n, m, seed=r)
                ms = time_c_dijkstra(n, edges, 0)
                times.append(ms)

            mean = stats.mean(times)
            std = stats.pstdev(times)
            results.append(("c", n, mean, std))
            print(f"[ C ] n={n} mean={mean:.3f}ms")

    # ------------- salvar CSV ---------------
    with open("results_dijkstra.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["impl", "n", "mean", "std"])
        w.writerows(results)

    # ----------- gráfico Python -------------
    py_ns = [n for impl, n, _, _ in results if impl == "python"]
    py_means = [m for impl, _, m, _ in results if impl == "python"]
    plot_curve(py_ns, py_means, "Dijkstra Python", "plot_python_dijkstra.png")

    # ----------- gráfico Python vs C --------
    if include_c:
        c_ns = [n for impl, n, _, _ in results if impl == "c"]
        c_means = [m for impl, _, m, _ in results if impl == "c"]

        plt.figure()
        plt.plot(py_ns, py_means, marker="o", label="Python")
        plt.plot(c_ns, c_means, marker="s", label="C")
        plt.legend()
        plt.title("Dijkstra Python vs C")
        plt.xlabel("n")
        plt.ylabel("ms")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("plot_python_vs_c_dijkstra.png", dpi=160)
        plt.close()


if __name__ == "__main__":
    main()
