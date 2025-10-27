from itertools import permutations, combinations
import random
import string

def gerar_grafo(n, max_conexoes=3, seed=None):
    """
    Gera um grafo no formato:
    ['label_vertice', 'indice_vertice', [lista_indices_adj]]
    
    Parâmetros:
    - n: número de vértices (qualquer valor positivo)
    - max_conexoes: número máximo de conexões por vértice
    - seed: semente para aleatoriedade
    """
    if n <= 0:
        raise ValueError("O número de vértices deve ser positivo.")
    
    if seed is not None:
        random.seed(seed)

    # Função auxiliar para gerar rótulos além de Z: A, B, ..., Z, AA, AB, etc.
    def gerar_label(i):
        letras = string.ascii_uppercase
        label = ""
        while True:
            i, r = divmod(i, 26)
            label = letras[r] + label
            if i == 0:
                break
            i -= 1
        return label

    grafo = []
    for i in range(n):
        label = gerar_label(i)
        possiveis = list(range(n))
        possiveis.remove(i)
        num_conexoes = random.randint(1, min(max_conexoes, n - 1))
        conexoes = random.sample(possiveis, num_conexoes)
        grafo.append([label, i, conexoes])
    
    return grafo

# Exemplo de uso
ordem = gerar_grafo(2000, max_conexoes=10)
print("======= Grafo (primeiros 10) ===========")
for i in ordem[:10]:
    print(i)

print("======= Caminhos (duplas válidas) ===========")

n = len(ordem)

# --- Mapas auxiliares ---
index_to_label = {i: label for label, i, _ in ordem}  # índice → letra
label_to_index = {label: i for label, i, _ in ordem}  # letra → índice
adj = {i: viz for _, i, viz in ordem}  # adjacência
neighbors = adj

# --- Função: verifica se uma permutação forma caminho válido ---
def caminho_valido(perm):
    """Retorna True se todos os vértices consecutivos em perm são adjacentes."""
    for a, b in zip(perm, perm[1:]):
        if b not in adj[a]:
            return False
    return True

# --- 2. Gera todas as janelas (duplas válidas) ---
k = 2
validas = []

# Usando range(0, n) (índices baseados em zero)
for comb in combinations(range(n), k):
    for perm in permutations(comb):
        if caminho_valido(perm):
            validas.append(list(perm))

print(f"Número de duplas válidas: {len(validas)}")
print("Exemplo:", validas[:10])

# Exibir também com letras, se quiser:
print("======= Duplas (com letras, primeiros 10) ===========")
for v in validas[:10]:
    print([index_to_label[i] for i in v])
