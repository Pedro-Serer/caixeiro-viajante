from itertools import permutations

# ----------------------------
# Dados de entrada
# ----------------------------
linhas = [['D', 'A', 2], ['B', 'A', 10], ['E', 'B', 3], ['C', 'B', 9],
          ['D', 'E', 6], ['D', 'B', 10], ['A', 'C', 7], ['E', 'A', 6]]
valores = {'B': 2, 'A': 1, 'E': 3, 'D': 4, 'C': 5}

# ----------------------------
# Funções auxiliares
# ----------------------------
def vizinhos_diff1(u, v):
    return abs(valores[u] - valores[v]) == 1

# Dicionário de adjacência
arestas = {(u, v) for u, v, _ in linhas} | {(v, u) for u, v, _ in linhas}

# ----------------------------
# Gerar janelas
# ----------------------------
v_nomes = list(valores.keys())
k = 4
janelas = [list(permutations(v_nomes[i:i+k])) for i in range(len(v_nomes) - k + 1)]

# ----------------------------
# Construir caminhos Hamiltonianos
# ----------------------------
caminhos = []

for i in range(len(janelas) - 1):
    X = janelas[i]
    Y = janelas[i+1]
    
    for linha_X in X:
        ultimo_X = linha_X[-1]
        for linha_Y in Y:
            primeiro_Y = linha_Y[0]
            if vizinhos_diff1(ultimo_X, primeiro_Y):
                caminho = list(linha_X)
                for v in linha_Y:
                    if v not in caminho:
                        caminho.append(v)
                caminhos.append(caminho)

# Remover duplicados
caminhos_unicos = []
for c in caminhos:
    if c not in caminhos_unicos:
        caminhos_unicos.append(c)

# ----------------------------
# Resultados (Caminhos Hamiltonianos)
# ----------------------------
print("\nCaminhos Hamiltonianos encontrados:")
for i, cam in enumerate(caminhos_unicos, 1):
    print(f"Caminho {i}: {cam}")

if not caminhos_unicos:
    print("Nenhum caminho Hamiltoniano encontrado com os valores atuais.")
