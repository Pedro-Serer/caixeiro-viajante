from itertools import permutations, combinations

# === Estrutura do grafo ===
ordem = [
    ['A', 1, {2, 3, 5}],
    ['C', 2, {1}],
    ['B', 3, {1, 4}],
    ['E', 4, {3, 5}],
    ['D', 5, {1, 4}]
]

# Mapas auxiliares
index_to_label = {i: label for label, i, _ in ordem}
label_to_index = {label: i for label, i, _ in ordem}
adj = {i: viz for _, i, viz in ordem}
n = len(ordem)

# --- Função: verifica se uma permutação forma um caminho válido ---
def caminho_valido(perm):
    """Retorna True se todos os vértices consecutivos em perm são adjacentes."""
    for a, b in zip(perm, perm[1:]):
        if b not in adj[a]:
            return False
    return True

# --- Gera todas as janelas (combinações de 3 vértices) ---
k = 3
validas = []

for comb in combinations(range(1, n+1), k):
    for perm in permutations(comb):
        if caminho_valido(perm):
            validas.append(perm)

print("=== Permutações válidas ===")
for v in validas:
    print([index_to_label[i] for i in v])

# --- Cria transições entre janelas ---
transicoes = {}
for u in validas:
    transicoes[u] = []
    for v in validas:
        # se o final de u conecta ao início de v
        if u[-1] in adj[v[0]]:
            transicoes[u].append(v)

# --- Busca caminhos completos via DFS ---
resultados = []

def dfs(caminho, visitados):
    ultimo = caminho[-1]
    if len(visitados) == n:
        resultados.append([index_to_label[i] for i in caminho])
        return
    for prox in range(1, n+1):
        if prox not in visitados and prox in adj[ultimo]:
            dfs(caminho + [prox], visitados | {prox})

# Inicia a busca a partir de cada vértice
for v in range(1, n+1):
    dfs([v], {v})

print("\n=== Candidatos finais (Hamiltonianos) ===")
for r in resultados:
    print(r)
