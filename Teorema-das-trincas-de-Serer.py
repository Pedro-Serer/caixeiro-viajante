"""
Teorema das Trincas de Serer – Implementação v5

Este código implementa a abordagem descrita no artigo:
"Teorema das trincas de Serer: Um método polinomial de mapear Grafos Arbitrários".

A ideia central é:
- Representar todos os subcaminhos de 3 vértices válidos (trincas) de um grafo.
- Concatenar essas trincas usando janelas deslizantes sobre vértices comuns.
- Reconstruir todos os caminhos possíveis que percorrem os vértices respeitando a conectividade.
"""

from itertools import permutations, combinations

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

# --- Construir caminhos usando apenas trincas fornecidas ---
def build_paths(triples):
    adj_triples = build_adj(triples)
    paths = []
    seen_paths = set()  # para evitar duplicatas

    for start_idx in range(len(triples)):
        path = triples[start_idx].copy()
        current_idx = start_idx

        while True:
            extended = False
            for next_idx in adj_triples[current_idx]:
                next_triple = triples[next_idx]
                next_vertex = next_triple[2]
                if next_vertex not in path:  # não repetir vértices
                    path.append(next_vertex)
                    current_idx = next_idx
                    extended = True
                    break
            if not extended:
                break

        # Converter para tupla para usar em set e evitar duplicatas
        path_tuple = tuple(path)
        if path_tuple not in seen_paths:
            seen_paths.add(path_tuple)
            paths.append(path)

    return paths

# --- Executar ---
paths = build_paths(validas)

# Exibir caminhos com nomes dos vértices
for p in paths:
    print([index_to_label[i] for i in p])
