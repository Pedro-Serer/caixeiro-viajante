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

# === 1. Matriz 'ordem' do grafo 
ordem = [
    ['A', 0, [2, 3]],   # A(0) conectado a B e C
    ['D', 1, [2, 3]],   # D(1) conectado a B e C
    ['B', 2, [0, 1, 5]],# B(2) conectado a A, D e E
    ['C', 3, [0, 1]],   # C(3) conectado a A e D
    ['F', 4, [5, 6]],   # F(4) conectado a E e G
    ['E', 5, [2, 4, 6]],# E(5) conectado a B, F e G
    ['G', 6, [4, 5]]    # G(6) conectado a F e E
]

# --- Mapas auxiliares para conversão e vizinhança ---
index_to_label = {i: label for label, i, _ in ordem}  # índice → letra
label_to_index = {label: i for label, i, _ in ordem}  # letra → índice
adj = {i: viz for _, i, viz in ordem}                 # vizinhos de cada vértice
n = len(ordem)                                        # número de vértices

# --- Função de verificação de caminho ---
def caminho_valido(perm):
    """
    Retorna True se todos os vértices consecutivos em perm estão conectados no grafo.
    Cada permutação é um possível subcaminho (trinca) do grafo.
    """
    for a, b in zip(perm, perm[1:]):
        if b not in adj[a]:
            return False
    return True

# --- 2. Geração de todas as trincas válidas ---
k = 3
validas = []

for comb in combinations(range(n), k):      # todas as combinações de 3 vértices
    for perm in permutations(comb):         # todas as permutações de cada combinação
        if caminho_valido(perm):           # mantém apenas as trincas válidas
            validas.append(list(perm))

# === 3. Função filtra_saida_v5 ===
def filtra_saida_v5(matriz):
    """
    Reconstrói caminhos completos a partir das trincas válidas.
    Baseado na ideia do Teorema das Trincas de Serer:
    - Cada trinca é uma janela de 3 vértices conectados.
    - Trincas adjacentes compartilham exatamente um vértice extremo.
    - Evita sobreposição de múltiplos vértices para impedir caminhos inválidos.
    """
    caminhos = set()
    tam = len(matriz)

    for i in range(tam):
        base = matriz[i]
        caminho = base.copy()
        usados = {tuple(base)}
        mudou = True

        inicio, fim = caminho[0], caminho[-1]

        while mudou:
            mudou = False
            ultima_trinca = caminho[-3:] if len(caminho) >= 3 else caminho

            for j in range(tam):
                trinca = matriz[j]
                if tuple(trinca) in usados:
                    continue

                # --- Verifica interseção com a última trinca ---
                comuns = set(ultima_trinca) & set(trinca)
                if len(comuns) != 1:  # apenas um vértice em comum permitido
                    continue

                comum = list(comuns)[0]

                # vértice comum deve estar nas extremidades de ambas as trincas
                if not (comum in (ultima_trinca[0], ultima_trinca[-1]) and
                        comum in (trinca[0], trinca[-1])):
                    continue

                # ignora se houver mais de um elemento em comum
                if len(set(ultima_trinca) & set(trinca)) > 1:
                    continue

                # adiciona apenas novos vértices
                novos = [v for v in trinca if v not in caminho]
                if not novos:
                    continue

                # --- Concatena trinca no início ou fim do caminho ---
                if trinca[0] == fim or trinca[-1] == fim:
                    caminho.extend(novos)
                    fim = caminho[-1]
                elif trinca[0] == inicio or trinca[-1] == inicio:
                    caminho = novos + caminho
                    inicio = caminho[0]
                else:
                    continue

                usados.add(tuple(trinca))
                mudou = True
                break

        if len(caminho) > 3:
            caminhos.add(tuple(caminho))

    return caminhos

# --- 4. Executa v5 com as trincas válidas ---
caminhos_indices = filtra_saida_v5(validas)

# --- 5. Converte índices para letras ---
caminhos_letras = []
for caminho in caminhos_indices:
    letras = [index_to_label[i] for i in caminho]
    caminhos_letras.append(letras)

# --- 6. Exibe os caminhos reconstruídos ---
print("=== Caminhos reconstruídos ===")
for c in sorted(caminhos_letras):
    print(c)
