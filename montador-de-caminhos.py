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
graph = gerar_grafo(8000, max_conexoes=1000)
# Transformar lista de grafo em dicionário {indice: [lista_de_adj]}
graph_dict = {v[1]: v[2] for v in graph}

from collections import deque

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
arvore = reduzir_para_arvore(graph_dict, raiz=0)
saida  = dfs_arvore(arvore, 0) 
print(saida)
