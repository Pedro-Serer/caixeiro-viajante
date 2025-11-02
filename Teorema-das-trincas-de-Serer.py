"""
Teorema das Trincas de Serer – Implementação v6

Este código implementa a abordagem descrita no artigo:
"Teorema das trincas de Serer: Um método polinomial de mapear Grafos Arbitrários".

A ideia central é:
- Representar todos os subcaminhos de 3 vértices válidos (trincas) de um grafo.
- Concatenar essas trincas usando janelas deslizantes sobre vértices comuns.
- Reconstruir todos os caminhos possíveis que percorrem os vértices respeitando a conectividade, para isso reduzimos à uma árvore e depois fazemos uma busca de profundidade.
"""

from itertools import permutations, combinations
from collections import deque

# === 1. Matriz 'ordem' ===
ordem = [
    ['A', 1, {2, 3, 4, 8}],
    ['B', 2, {1, 5, 6}],
    ['C', 3, {1, 6, 7}],
    ['D', 4, {1, 5, 11}],
    ['E', 5, {2, 4, 9}],
    ['F', 6, {2, 3, 9, 10}],
    ['G', 7, {3, 8, 10}],
    ['H', 8, {1, 11}],
    ['I', 9, {5, 6, 11}],
    ['J', 10, {6, 7, 11}],
    ['K', 11, {4, 9, 10, 8}]
]

n = len(ordem)

# --- Mapas auxiliares ---
index_to_label = {i: label for label, i, _ in ordem}  # índice → letra
label_to_index = {label: i for label, i, _ in ordem}  # letra → índice
adj = {i: viz for _, i, viz in ordem}  # adjacência
neighbors = adj  # apenas para compatibilidade com o resto do código

# --- Função: verifica se uma permutação forma caminho válido ---
def caminho_valido(perm):
    """Retorna True se todos os vértices consecutivos em perm são adjacentes."""
    for a, b in zip(perm, perm[1:]):
        if b not in adj[a]:
            return False
    return True

# --- 2. Gera todas as janelas (trincas válidas) usando índices ---
k = 3
validas = []

for comb in combinations(range(1, n + 1), k):
    for perm in permutations(comb):
        if caminho_valido(perm):
            validas.append(list(perm))  # já como índices

# --- Construir ADJ entre trincas fornecidas ---
def build_adj(triples):
    adj_triples = {i: [] for i in range(len(triples))}
    for i, t1 in enumerate(triples):
        for j, t2 in enumerate(triples):
            if i == j:
                continue
            # Condição de adjacência: últimos dois de t1 == primeiros dois de t2
            # e último vértice de t2 é vizinho do último de t1
            if t1[1] == t2[0] and t1[2] == t2[1] and t2[2] not in t1:
                if t2[2] in neighbors[t1[2]]:
                    adj_triples[i].append(j)
    return adj_triples

def reduzir_para_arvore(graph, raiz=0):
    visitado = set([raiz])
    fila = deque([raiz])
    arvore = {raiz: []}

    while fila:
        atual = fila.popleft()
        for vizinho in graph.get(atual, []):
            if vizinho not in visitado:
                visitado.add(vizinho)
                fila.append(vizinho)
                arvore[atual].append(vizinho)
                arvore.setdefault(vizinho, [])
    return arvore

def dfs_arvore(arvore, no, caminho=None):
    if caminho is None:
        caminho = []
    caminho.append(no)
    
    filhos = arvore.get(no, [])
    if not filhos:  # folha
        resultados = [caminho.copy()]
    else:
        resultados = []
        for f in filhos:
            resultados.extend(dfs_arvore(arvore, f, caminho))
    
    caminho.pop()
    return resultados

arvore = reduzir_para_arvore(build_adj(validas))

for i in range(len(validas)):
    caminhos = dfs_arvore(arvore, i)
    
    print("Árvore reduzida:", arvore, "\n")
    print("Caminhos DFS:")
    for c in caminhos:
        print(c)
