from itertools import permutations

valores = {'A': 1, 'B': 2, 'E': 3, 'C': 4, 'D': 5}

# Cada linha = aresta
linhas = [
    ['A', 'B', 6], ['A', 'E', 5], ['A', 'D', 3], ['B', 'C', 3], ['B', 'D', 4], ['B', 'E', 4],
    ['C', 'A', 3], ['C', 'D', 5], ['C', 'E', 7], ['D', 'E', 4]
]

# Tamanho da janela
k = 4

def vizinhos_diff1(u, v):
    return abs(valores[u] - valores[v]) == 1

distancias = {}
for u, v, d in linhas:
    distancias[(u, v)] = d
    distancias[(v, u)] = d  # bidirecional

janelas = []
for i in range(len(linhas) - k + 1):
    janela = linhas[i:i+k]
    vertices = [v for aresta in janela for v in aresta[:2]]
    vertices = list(dict.fromkeys(vertices))
    perms = list(permutations(vertices))
    janelas.append(perms)

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

caminhos_unicos = []
for c in caminhos:
    if c not in caminhos_unicos:
        caminhos_unicos.append(c)

# Guardar caminhos com detalhes das arestas e soma
caminhos_detalhados = []
for cam in caminhos_unicos:
    detalhe = []
    soma = 0
    for j in range(len(cam) - 1):
        u, v = cam[j], cam[j+1]
        d = distancias.get((u, v), 0)
        detalhe.append(f"{u}-{v}={d}")
        soma += d
    caminhos_detalhados.append((cam, detalhe, soma))

# Encontrar menor soma
menor_caminho = min(caminhos_detalhados, key=lambda x: x[2])

print(f"Total de caminhos Hamiltonianos encontrados: {len(caminhos_unicos)}\n")
for i, (cam, detalhe, soma) in enumerate(caminhos_detalhados, 1):
    print(f"Caminho {i}: {cam} | {' , '.join(detalhe)} | Total: {soma}")

print("\nCaminho de menor soma:")
cam, detalhe, soma = menor_caminho
print(f"{cam} | {' , '.join(detalhe)} | Total: {soma}")
