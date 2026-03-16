import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tree.build_tree import build_tree
from algorithms.dfs import dfs
from algorithms.bfs import bfs


def medir(func, root, repeticoes=3):
    resultado = None
    total = 0.0
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        resultado = func(root)
        total += time.perf_counter() - inicio
    return resultado, (total / repeticoes) * 1000


def imprimir_tabela(dados):
    sep = "-" * 72
    print("\n" + sep)
    print(f"{'Comparação: DFS vs BFS':^72}")
    print(sep)
    print(f"{'Algoritmo':<14} {'Itens retornados':>16} {'Tempo médio (ms)':>18}")
    print(sep)
    for d in dados:
        print(f"{d['nome']:<14} {d['nos']:>16} {d['tempo']:>17.4f}")
    print(sep + "\n")


def responder_perguntas(dados):
    dfs_d = next(d for d in dados if d["nome"] == "DFS")
    mais_rapido = "DFS" if dfs_d["tempo"] <= next(d for d in dados if d["nome"] == "BFS")["tempo"] else "BFS"

    print("=" * 72)
    print("Respostas — Parte 5 do trabalho")
    print("=" * 72)
    print(f"""
1. Qual algoritmo encontra resposta mais rápido em árvores profundas?
   → DFS — segue um caminho até a folha sem explorar outros ramos antes.
     (No teste desta árvore o mais rápido foi: {mais_rapido})

2. Qual algoritmo consome mais memória?
   → BFS — a fila pode armazenar todos os nós de um nível inteiro ao mesmo tempo.

3. Em que tipo de problema BFS seria preferível?
   → Quando a resposta está próxima da raiz ou quando precisa do menor caminho.
     Exemplo: redes sociais, rotas em grafos.

4. Em que tipo de problema DFS seria preferível?
   → Quando a árvore é profunda e a resposta está em uma folha distante.
     Exatamente o caso deste jogo de adivinhação.
""")
    print("=" * 72)


def main():
    csv_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "data", "zoo.csv"))

    print(f"\nCarregando árvore de '{csv_path}'...")
    avl = build_tree(csv_path)
    root = avl.get_root()

    if root is None:
        print("erro: árvore vazia. Verifique o caminho do zoo.csv.")
        return

    print(f"Árvore construída. Raiz: {root}\n")

    visita_dfs, tempo_dfs = medir(dfs, root)
    visita_bfs, tempo_bfs = medir(bfs, root)

    dados = [
        {"nome": "DFS", "visita": visita_dfs, "nos": len(visita_dfs), "tempo": tempo_dfs},
        {"nome": "BFS", "visita": visita_bfs, "nos": len(visita_bfs), "tempo": tempo_bfs},
    ]

    imprimir_tabela(dados)
    responder_perguntas(dados)


if __name__ == "__main__":
    main()
