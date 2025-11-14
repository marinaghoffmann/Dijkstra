# 🚀 Análise Completa do Algoritmo de Dijkstra — Python e C

Implementações e estudo experimental do algoritmo de **Dijkstra** (caminho mínimo em grafos com arestas de peso não-negativo).  
Inclui: implementações em **Python e C**, scripts de benchmark, geração de CSVs, criação de gráficos e documentação.

---

## 📌 Conteúdo do Repositório

- `dijkstra.py` — implementação em Python com suporte a `--demo`, `--source` e leitura via stdin.  
- `dijkstra.c` — implementação em C usando min-heap simples, também com `--demo` e leitura via stdin.  
- `benchmark_dijkstra.py` — gera grafos aleatórios, executa benchmarks, salva resultados em CSV e cria gráficos comparativos (Python vs C).  
- `results_dijkstra.csv` — (gerado pelo benchmark) resultados de performance.  
- `plot_python_dijkstra.png`, `plot_python_vs_c_dijkstra.png` — imagens geradas pelo benchmark.  
- `README.md` — este arquivo.

---

# 1. Descrição do Problema e do Algoritmo

### 🎯 Problema
Calcular as menores distâncias entre um vértice fonte `s` e todos os outros vértices de um grafo com pesos não-negativos.

### 💡 Ideia Geral do Dijkstra
Utiliza uma *fila de prioridade* (min-heap) para sempre escolher o próximo vértice de menor distância conhecida e atualizar (relaxar) os vizinhos.

### 📌 Pseudocódigo
Dijkstra(G, source):
para cada v em V:
dist[v] = +∞
parent[v] = NIL
dist[source] = 0

heap = min-priority-queue
heap.push((0, source))

enquanto heap não estiver vazia:
(d, u) = heap.pop_min()
se d > dist[u]: continue
 para cada (u, v, w) em adj[u]:
    se dist[u] + w < dist[v]:
       dist[v] = dist[u] + w
       parent[v] = u
       heap.push((dist[v], v))
retorne dist, parent


---

# 2. Classificação Assintótica

Assumindo um **heap binário**:

| Operação | Custo |
|---------|-------|
| Inserção / extração | \(O(\log n)\) |
| Relaxamento total | \(O(m \log n)\) |
| **Complexidade final** | **O((n + m) log n)** |

Para heap de Fibonacci → \(O(m + n \log n)\).

---

# 3. Quando Usar Dijkstra

📌 **Use quando:**
- Pesos são **não-negativos**.  
- Você precisa de caminho mínimo *single-source*.  
- Grafos médios e grandes (até milhões de arestas) com boa performance.

❌ **Não use quando:**
- Existem pesos negativos → **Bellman-Ford**.  
- Quer caminho mínimo entre *todos os pares* → Floyd-Warshall.  
- O problema envolve caminho mais longo → NP-hard.

---

# 4. Formato de Entrada (stdin)

n m
u1 v1 w1
u2 v2 w2
...
u_m v_m w_m
s

- `n` → vértices (0 até n-1)  
- `m` → número de arestas  
- `u v w` → aresta com peso  
- `s` → fonte (pode ser sobrescrita por `--source`)

### Exemplo (`graph.txt`)
5 6
0 1 2
0 2 4
1 2 1
1 3 7
2 4 3
3 4 1
0


---

# 5. Como Executar o Projeto

## ✔ Python
```bash
python dijkstra.py --demo
python dijkstra.py < graph.txt
python dijkstra.py --source 0 < graph.txt

C
gcc -O2 -o dijkstra_c dijkstra.c
./dijkstra_c --demo
./dijkstra_c < graph.txt

Benchmark
python benchmark_dijkstra.py
python benchmark_dijkstra.py --include-c
(Certifique-se de usar um virtualenv com matplotlib instalado.)