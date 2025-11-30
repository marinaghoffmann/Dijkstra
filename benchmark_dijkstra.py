#!/usr/bin/env python3
"""
Benchmark Dijkstra (Python vs C) — versão com bandas de erro (±1 std)
- Gera grafos conectados (m = factor * n)
- Executa reps repetições (padrão 30)
- Mede tempo em Python (chamada direta) e em C (lendo tempo impresso pelo executável)
- Salva CSV e gera PNG com bandas de erro e grid quadriculado
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
import numpy as np

# ---- IMPORT: sua função Python Dijkstra ----
# Garantir que dijkstra.py contenha `def run_dijkstra_py(n, edges, source): ...`
from dijkstra import run_dijkstra_py


# -------------------------
# Estilo global dos plots
# -------------------------
def set_plot_style():
    plt.rcParams.update({
        "figure.figsize": (9, 6),
        "font.size": 13,
        "axes.titlesize": 15,
        "axes.labelsize": 13,
        "legend.fontsize": 12,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "lines.linewidth": 1.6,
        "lines.markersize": 6,
    })


# -------------------------
# Geração de grafos
# -------------------------
def gen_connected_graph(n: int, m: int, seed: int = None) -> Tuple[int, int, List[Tuple[int, int, int]], int]:
    """Gera grafo conexo (não-direcionado), devolve (n, m, edges, source)."""
    rnd = random.Random(seed)
    if m < n - 1:
        raise ValueError("m must be >= n-1 to be connected")

    edges = []
    # spanning tree (garante conectividade)
    for v in range(1, n):
        u = rnd.randrange(0, v)
        w = rnd.randint(1, 100)
        edges.append((u, v, w))

    existing = set((min(u, v), max(u, v)) for (u, v, _) in edges)
    attempts = 0
    while len(edges) < m and attempts < 10 * m:
        u = rnd.randrange(0, n)
        v = rnd.randrange(0, n)
        if u == v:
            attempts += 1
            continue
        key = (min(u, v), max(u, v))
        if key in existing:
            attempts += 1
            continue
        edges.append((u, v, rnd.randint(1, 100)))
        existing.add(key)

    # fallback se não conseguiu preencher (raríssimo)
    if len(edges) < m:
        for u in range(n):
            for v in range(u + 1, n):
                key = (u, v)
                if key not in existing:
                    edges.append((u, v, random.randint(1, 100)))
                    existing.add(key)
                if len(edges) >= m:
                    break
            if len(edges) >= m:
                break

    source = 0
    return n, m, edges, source


# -------------------------
# Formatar grafo para stdin (C)
# -------------------------
def graph_to_stdin(n: int, m: int, edges: List[Tuple[int, int, int]], source: int, include_source_in_stdin: bool = True) -> bytes:
    lines = [f"{n} {m}"]
    for u, v, w in edges:
        lines.append(f"{u} {v} {w}")
    if include_source_in_stdin:
        lines.append(str(source))
    return ("\n".join(lines) + "\n").encode("utf-8")


# -------------------------
# Medições
# -------------------------
def time_python_dijkstra(n: int, edges: List[Tuple[int, int, int]], source: int) -> float:
    t0 = time.perf_counter()
    run_dijkstra_py(n, edges, source)
    t1 = time.perf_counter()
    return (t1 - t0) * 1000.0  # ms


def detect_c_executable() -> str:
    if os.name == "nt":
        if os.path.exists("dijkstra_c.exe"):
            return "dijkstra_c.exe"
        if os.path.exists("dijkstra.exe"):
            return "dijkstra.exe"
    else:
        if os.path.exists("./dijkstra_c"):
            return "./dijkstra_c"
        if os.path.exists("./dijkstra"):
            return "./dijkstra"
    return ""


def time_c_dijkstra(n: int, edges: List[Tuple[int, int, int]], source: int, exe: str) -> float:
    """
    Executa o executável C (que deve medir internamente apenas o algoritmo)
    e retorna o valor numérico impresso (ms).
    """
    inp = graph_to_stdin(n, len(edges), edges, source, include_source_in_stdin=True)
    proc = subprocess.run([exe], input=inp, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError("Erro no executável C: " + proc.stderr.decode("utf-8", errors="ignore"))
    out = proc.stdout.decode("utf-8", errors="ignore").strip()
    # extrai primeiro float encontrado
    for token in out.split():
        try:
            return float(token)
        except:
            continue
    raise RuntimeError("Executável C não retornou valor numérico (stdout: {})".format(out))


# -------------------------
# Plots com banda de erro (±1 std)
# -------------------------
def plot_curve_with_band(xs, means, stds, title, xlabel, ylabel, outpath, color="#1f77b4", label=""):
    set_plot_style()
    xs = np.array(xs, dtype=float)
    means = np.array(means, dtype=float)
    stds = np.array(stds, dtype=float)

    plt.figure()
    plt.plot(xs, means, marker="o", color=color, label=label or "média")
    lower = means - stds
    upper = means + stds
    plt.fill_between(xs, lower, upper, color=color, alpha=0.18, linewidth=0.0, edgecolor=None)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


def plot_with_theory_band(xs_nm_pairs, means, stds, title, xlabel, ylabel, outpath, color="#1f77b4"):
    set_plot_style()
    ns = np.array([nm[0] for nm in xs_nm_pairs], dtype=float)
    ms = np.array([nm[1] for nm in xs_nm_pairs], dtype=float)
    means = np.array(means, dtype=float)
    stds = np.array(stds, dtype=float)

    eff = ns + ms
    theory = eff * np.log2(np.maximum(ns, 2.0))

    # escala teoria para coincidir com o primeiro ponto empírico não-nulo
    idx = int(np.argmax(means > 0))
    scale = (means[idx] / theory[idx]) if theory[idx] != 0 else 1.0
    theory_scaled = theory * scale

    plt.figure()
    plt.plot(ns, means, marker="o", color=color, label="Empírico")
    plt.fill_between(ns, means - stds, means + stds, color=color, alpha=0.18)
    plt.plot(ns, theory_scaled, marker="x", linestyle="--", color="#333333", label="(n+m)·log2(n) (normalizado)")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


# -------------------------
# Main
# -------------------------
def main():
    parser = argparse.ArgumentParser(description="Benchmark Dijkstra (Python vs C) — com bandas de erro")
    parser.add_argument("--sizes", type=str, default="200,500,1000,2000,4000",
                        help="Comma-separated list of n")
    parser.add_argument("--factor", type=float, default=4.0, help="m ≈ factor * n")
    parser.add_argument("--reps", type=int, default=30, help="Repetitions per size")
    parser.add_argument("--include-c", action="store_true", help="Include C executable if present")
    parser.add_argument("--seed-base", type=int, default=12345, help="Base seed for reproducibility")
    args = parser.parse_args()

    sizes = [int(x) for x in args.sizes.split(",") if x.strip()]
    factor = float(args.factor)
    reps = int(args.reps)

    exe = detect_c_executable() if args.include_c else ""
    if args.include_c and not exe:
        print("Aviso: executável C não foi encontrado. Compile e nomeie como dijkstra_c.exe (Windows) ou ./dijkstra_c (Unix).")
        return

    results = []  # (impl, n, m, mean_ms, std_ms)

    print("Iniciando benchmark — sizes:", sizes, "factor:", factor, "reps:", reps)
    for n in sizes:
        m = max(n - 1, int(round(factor * n)))
        py_times = []
        c_times = []
        print(f"\n=== n = {n} | m ≈ {m} ===")
        for r in range(reps):
            seed = args.seed_base + r
            n_, m_, edges, source = gen_connected_graph(n, m, seed=seed)

            # Python
            tpy = time_python_dijkstra(n_, edges, source)
            py_times.append(tpy)

            # C (opcional)
            if exe:
                tc = time_c_dijkstra(n_, edges, source, exe=exe)
                c_times.append(tc)

            if (r + 1) % max(1, int(reps / 6)) == 0:
                print(f"  progresso: {r+1}/{reps}")

        py_mean = stats.mean(py_times)
        py_std = stats.pstdev(py_times)
        results.append(("python", n, m, py_mean, py_std))
        print(f"[PY] n={n} mean={py_mean:.4f} ms  std={py_std:.4f} ms")

        if exe:
            c_mean = stats.mean(c_times)
            c_std = stats.pstdev(c_times)
            results.append(("c", n, m, c_mean, c_std))
            print(f"[C ] n={n} mean={c_mean:.6f} ms  std={c_std:.6f} ms")

    # salvar CSV
    out_csv = "results_dijkstra.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["implementation", "n", "m", "mean_ms", "std_ms"])
        for row in results:
            w.writerow(row)
    print("\nCSV salvo em:", out_csv)

    # montar arrays para gráficos
    py_ns = [n for impl, n, m, mean, std in results if impl == "python"]
    py_means = [mean for impl, n, m, mean, std in results if impl == "python"]
    py_stds = [std for impl, n, m, mean, std in results if impl == "python"]

    # Plots Python
    plot_curve_with_band(py_ns, py_means, py_stds,
                        "Dijkstra (Python) — Tempo médio ±1σ", "n (vértices)", "Tempo (ms)",
                        "plot_python_mean_std.png", color="#1f77b4", label="Python")

    plot_with_theory_band([(n, max(n - 1, int(round(factor * n)))) for n in py_ns],
                         py_means, py_stds,
                         "Dijkstra (Python) — Empírico vs Teoria (n+m)·log2(n)",
                         "n (vértices)", "Tempo (ms)",
                         "plot_python_vs_theory.png", color="#1f77b4")

    # Se C presente
    if exe:
        c_ns = [n for impl, n, m, mean, std in results if impl == "c"]
        c_means = [mean for impl, n, m, mean, std in results if impl == "c"]
        c_stds = [std for impl, n, m, mean, std in results if impl == "c"]

        plot_curve_with_band(c_ns, c_means, c_stds,
                            "Dijkstra (C) — Tempo médio ±1σ", "n (vértices)", "Tempo (ms)",
                            "plot_c_mean_std.png", color="#ff7f0e", label="C")

        plot_with_theory_band([(n, max(n - 1, int(round(factor * n)))) for n in c_ns],
                             c_means, c_stds,
                             "Dijkstra (C) — Empírico vs Teoria (n+m)·log2(n)",
                             "n (vértices)", "Tempo (ms)",
                             "plot_c_vs_theory.png", color="#ff7f0e")

        # comparação direta com bandas (plot das médias e bandas sobrepostas)
        set_plot_style()
        plt.figure()
        xs = np.array(py_ns, dtype=float)
        py_means_arr = np.array(py_means, dtype=float)
        py_stds_arr = np.array(py_stds, dtype=float)
        c_means_arr = np.array(c_means, dtype=float)
        c_stds_arr = np.array(c_stds, dtype=float)

        plt.plot(xs, py_means_arr, marker="o", color="#1f77b4", label="Python (média)")
        plt.fill_between(xs, py_means_arr - py_stds_arr, py_means_arr + py_stds_arr, color="#1f77b4", alpha=0.15)

        plt.plot(xs, c_means_arr, marker="s", color="#ff7f0e", label="C (média)")
        plt.fill_between(xs, c_means_arr - c_stds_arr, c_means_arr + c_stds_arr, color="#ff7f0e", alpha=0.15)

        plt.title("Dijkstra — Comparação Python vs C (médias ±1σ)")
        plt.xlabel("n (vértices)")
        plt.ylabel("Tempo (ms)")
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.legend()
        plt.tight_layout()
        plt.savefig("plot_python_vs_c_mean_std.png", dpi=200)
        plt.close()

    print("Plots gerados: plot_python_mean_std.png, plot_python_vs_theory.png",
          "plot_c_mean_std.png (se C), plot_c_vs_theory.png (se C), plot_python_vs_c_mean_std.png (se C)")

    print("Fim.")

if __name__ == "__main__":
    main()
