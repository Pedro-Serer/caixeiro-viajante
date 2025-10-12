from itertools import permutations, combinations

grafo = [
    ['A', {'B', 'C', 'E'}],
    ['B', {'A', 'D'}],
    ['C', {'A'}],
    ['D', {'B', 'E'}],
    ['E', {'A', 'D'}]
]

# --- Map label -> neighbors diretamente ---
adj = {label: viz for label, viz in grafo}

# --- Função: verifica se uma permutação forma caminho válido ---
def caminho_valido(perm):
    """Retorna True se todos os vértices consecutivos em perm são adjacentes."""
    for a, b in zip(perm, perm[1:]):
        if b not in adj[a]:
            return False
    return True

# --- 2. Gera todas as combinações de k vértices ---
k = 3
validas = []

for comb in combinations(adj.keys(), k):
    for perm in permutations(comb):
        if caminho_valido(perm):
            validas.append(perm)

print("=== Permutações válidas ===")
for v in validas:
    print(v)
