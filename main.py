from itertools import permutations, combinations

ordem = [
    ['A', 1, {2, 3, 5}],
    ['C', 2, {1}],
    ['B', 3, {1, 4}],
    ['E', 4, {3, 5}],
    ['D', 5, {1, 4}]
]

# --- Mapas auxiliares ---
index_to_label = {i: label for label, i, _ in ordem}
adj = {i: viz for _, i, viz in ordem}
n = len(ordem)

# --- Função: verifica se uma permutação forma caminho válido ---
def caminho_valido(perm):
    """Retorna True se todos os vértices consecutivos em perm são adjacentes."""
    for a, b in zip(perm, perm[1:]):
        if b not in adj[a]:
            return False
    return True

# --- 2. Gera todas as janelas (combinações de k vértices) ---
k = 3
validas = []

for comb in combinations(range(1, n+1), k):
    for perm in permutations(comb):
        if caminho_valido(perm):
            validas.append(perm)

print("=== Permutações válidas ===")
for v in validas:
    print([index_to_label[i] for i in v])

# --- 3. Cria transições entre janelas (verificação O(1)) ---
transicoes = {u: [] for u in validas}
for u in validas:
    ultimo_u = u[-1]
    for v in validas:
        primeiro_v = v[0]
        if primeiro_v in adj[ultimo_u]: 
            transicoes[u].append(v)

print("\n=== Transições entre janelas ===")
for u, vs in transicoes.items():
    print(f"{[index_to_label[i] for i in u]} -> {[ [index_to_label[i] for i in v] for v in vs ]}")

# --- 4. Concatenação de janelas para formar candidatos ---
candidatos = []
for u in validas:
    for v in transicoes[u]:
        # Concatena sem repetir o último vértice de u
        caminho = list(u) + list(v[1:])
        candidatos.append([index_to_label[i] for i in caminho])

print("\n=== Candidatos finais (junção de janelas) ===")
for c in candidatos:
    print(c)

