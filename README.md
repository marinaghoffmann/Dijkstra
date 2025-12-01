 # 🧭 DIJKSTRA — ANÁLISE DE COMPLEXIDADE E BENCHMARK EM PYTHON E C

Este repositório contém implementações completas do algoritmo de **Dijkstra** em **Python** e **C**, além de um estudo experimental detalhado sobre sua complexidade, desempenho prático, geração de gráficos e relatório de benchmarking.

---

# 📌 1. SOBRE O PROJETO

Este projeto foi desenvolvido para a disciplina de **Teoria da Computação**, com os objetivos de:

* Implementar o algoritmo **Dijkstra** em Python e C.
* Comparar o desempenho entre as duas linguagens.
* Gerar dados experimentais com entradas sintéticas.
* Confirmar empiricamente a complexidade teórica.
* Produzir gráficos, tabelas e relatórios.
* Analisar melhor caso, pior caso e caso médio.

---

# ⚙️ 2. DESCRIÇÃO DO DIJKSTRA

O **algoritmo de Dijkstra** resolve o problema do **caminho mínimo** em grafos ponderados e sem arestas negativas.

**Lógica geral:**

1. Inicialize a distância do nó inicial como 0 e de todos os outros como infinito.
2. Marque todos os nós como não visitados.
3. Enquanto houver nós não visitados:

   * Escolha o nó não visitado com a menor distância.
   * Atualize as distâncias de seus vizinhos.
   * Marque o nó como visitado.

**Pseudocódigo resumido:**

```
dijkstra(grafo, origem):
    dist[origem] = 0
    conjunto_vazio = {}
    enquanto houver nós não visitados:
        u = nó com menor dist[u]
        para cada vizinho v de u:
            se dist[u] + peso(u,v) < dist[v]:
                dist[v] = dist[u] + peso(u,v)
        marcar u como visitado
```

---

# 📈 3. COMPLEXIDADE ASSINTÓTICA

| CASO            | COMPLEXIDADE | DETALHES |   |   |     |   |   |                                     |
| --------------- | ------------ | -------- | - | - | --- | - | - | ----------------------------------- |
| **Melhor Caso** | O(           | E        | + | V | log | V | ) | Grafo com poucas atualizações       |
| **Caso Médio**  | Θ(           | E        | + | V | log | V | ) | Grafos aleatórios densos            |
| **Pior Caso**   | O(           | E        | + | V | log | V | ) | Grafos densos com todos os caminhos |

### SÍNTESE:

* **Big-O:** O(|E| + |V| log |V|)
* **Big-Ω:** Ω(|E| + |V| log |V|)
* **Big-Θ:** Θ(|E| + |V| log |V|)

O desempenho depende da estrutura usada para a fila de prioridade (ex: heap binário).

---

# 🏗️ 4. COMO REPRODUZIR O PROJETO

## 0️⃣ Clonar o repositório:

```
git clone https://github.com/marinaghoffmann/Dijkstra
cd Dijkstra
```

## 1️⃣ Criar e ativar ambiente virtual (Windows PowerShell):

```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 2️⃣ Instalar pacotes necessários:

```
pip install matplotlib numpy
```

## 3️⃣ Compilar implementação em C:

```
gcc -O2 -o dijkstra_c.exe dijkstra.c
```

## 4️⃣ Rodar benchmarking:

* Python + C:

```
python benchmark_dijkstra.py --include-c
```

* Somente Python:

```
python benchmark_dijkstra.py
```

* Alterar número de repetições (ex: 30):

```
python benchmark_dijkstra.py --reps 30 --include-c
```

---

# 🧮 5. IMPLEMENTAÇÕES

## ✔️ Python — `dijkstra.py`

### Executar demo:

```bash
python dijkstra.py --demo
```

### Executar com arquivo de entrada:

```bash
python dijkstra.py --input grafo.txt
```

## ⚡ C — `dijkstra.c`

Implementação otimizada para desempenho máximo.

### Compilar:

```bash
gcc -O2 -o dijkstra_c.exe dijkstra.c
```

### Executar demo:

```bash
./dijkstra_c.exe --demo
```

---

# 🚀 6. BENCHMARKING — `benchmark_dijkstra.py`

O script gera:

* Entradas aleatórias de diferentes tamanhos.
* 15 a 30 execuções por tamanho.
* Média e desvio-padrão dos tempos.
* CSV com resultados.
* Gráficos PNG comparativos.

### Executar benchmarking:

```bash
python benchmark_dijkstra.py
```

### Incluir implementação em C:

```bash
python benchmark_dijkstra.py --include-c
```

---

# 📊 7. GRÁFICOS E RESULTADOS

Arquivos gerados automaticamente:

* `plot_c_mean_std.png` → Tempo médio + desvio do C
* `plot_c_vs_theory.png` → Comparação com curva teórica
* `plot_python_mean_std.png` → Tempo médio + desvio do Python
* `plot_python_vs_c_mean_std.png` → Comparação Python x C
* `plot_python_vs_theory.png` → Comparação Python com complexidade teórica
* `results_dijkstra.csv` → Todos os resultados tabulados
