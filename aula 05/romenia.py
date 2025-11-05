from collections import deque 
# Importamos 'deque' (double-ended queue), que é a forma mais eficiente 
# em Python para lidar com filas (FIFO) e pilhas (LIFO) em ambas as pontas.
# O Grafo de Estados: Representação do mapa da Romênia.
# A chave (string) é o estado (cidade).
# O valor (lista) são as ações possíveis/estados adjacentes.
ROMENIA = {
    'Arad': ['Zerind', 'Timisoara', 'Sibiu'],
    'Zerind': ['Arad', 'Oradea'],
    'Oradea': ['Zerind', 'Sibiu'],
    'Sibiu': ['Arad', 'Oradea', 'Fagaras', 'Rimnicu Vilcea'],
    'Timisoara': ['Arad', 'Lugoj'],
    'Lugoj': ['Timisoara', 'Mehadia'],
    'Mehadia': ['Lugoj', 'Drobeta'],
    'Drobeta': ['Mehadia', 'Craiova'],
    'Craiova': ['Drobeta', 'Rimnicu Vilcea', 'Pitesti'],
    'Rimnicu Vilcea': ['Sibiu', 'Craiova', 'Pitesti'],
    'Fagaras': ['Sibiu', 'Bucareste'],
    'Pitesti': ['Rimnicu Vilcea', 'Craiova', 'Bucareste'],
    'Bucareste': ['Fagaras', 'Pitesti', 'Giurgiu', 'Urziceni'],
    'Giurgiu': ['Bucareste'],
    'Urziceni': ['Bucareste', 'Hirsova', 'Vaslui'],
    'Hirsova': ['Urziceni', 'Eforie'],
    'Eforie': ['Hirsova'],
    'Vaslui': ['Urziceni', 'Iasi'],
    'Iasi': ['Vaslui', 'Neamt'],
    'Neamt': ['Iasi']
}

class Node:
    """Estrutura de dados que armazena as informações de rastreamento (histórico) de um estado."""
    
    def __init__(self, estado, pai=None, acao=None, custo_caminho=0):
        # O construtor cria uma nova instância de Nó.
        self.estado = estado            # n.ESTADO: O nome da cidade que o nó representa.
        self.pai = pai                  # n.PAI: A referência ao nó anterior que levou a este (para rastreamento).
        self.acao = acao                # n.AÇÃO: A estrada usada para chegar a este estado.
        self.custo_caminho = custo_caminho # n.CUSTO-DO-CAMINHO: Custo total acumulado do início até aqui.
        
    def __repr__(self):
        # Método especial para exibir o objeto de forma legível (útil para debug).
        return f"<Node: {self.estado}>"

    def caminho(self):
        """Método que reconstrói e retorna o caminho completo percorrido."""
        caminho = []
        no_atual = self
        
        # Percorre a árvore de busca para trás, usando os ponteiros n.PAI.
        while no_atual:
            caminho.append(no_atual.estado)
            no_atual = no_atual.pai # Vai para o nó pai
            
        return caminho[::-1] # Retorna a lista invertida para ter a ordem correta (Início -> Objetivo).
    
def busca_em_largura_bfs(problema_grafo, estado_inicial, estado_objetivo):
    """
    Algoritmo BFS (Busca em Largura), que usa uma estratégia FIFO (Primeiro a Entrar, Primeiro a Sair).
    Ele explora o grafo em 'camadas' antes de ir mais fundo.
    """
    
    no_raiz = Node(estado_inicial)
    fronteira = deque([no_raiz]) # FRONTEIRA: Fila (FIFO). O 'deque' é essencial para isso.
    explorados = {estado_inicial} # CONJUNTO EXPLORADO: Armazena estados já visitados (GRAPH-SEARCH).
    
    while fronteira: # Repete enquanto a fronteira não estiver VAZIA?
        
        # OPERAÇÃO CRÍTICA (FIFO): Pega o nó mais ANTIGO da fila (o nó mais à esquerda).
        no_atual = fronteira.popleft() 
        
        # Teste de Objetivo
        if no_atual.estado == estado_objetivo:
            return no_atual.caminho()
        
        # Expande o nó
        for proximo_estado in problema_grafo.get(no_atual.estado, []):
            
            # Checa se o estado já foi explorado para evitar caminhos redundantes
            if proximo_estado not in explorados:
                explorados.add(proximo_estado) # Adiciona ao conjunto explorado
                
                # CHILD-NODE: Cria o novo nó filho
                no_filho = Node(estado=proximo_estado, pai=no_atual, acao=f"Ir para {proximo_estado}")
                
                # INSERIR: Adiciona o nó filho ao FINAL da fila (FIFO)
                fronteira.append(no_filho)
                
    return "Falha! Objetivo não alcançável (BFS)."

def busca_em_profundidade_dfs(problema_grafo, estado_inicial, estado_objetivo):
    """
    Algoritmo DFS (Busca em Profundidade), que usa uma estratégia LIFO (Último a Entrar, Primeiro a Sair).
    Ele explora um caminho até o fim antes de retroceder.
    """
    
    no_raiz = Node(estado_inicial)
    fronteira = [no_raiz]        # FRONTEIRA: Pilha (LIFO). Uma lista padrão pode ser usada como Pilha.
    explorados = {estado_inicial}
    
    while fronteira: # Repete enquanto a pilha não estiver vazia
        
        # OPERAÇÃO CRÍTICA (LIFO): Pega o nó mais NOVO (o último a entrar / topo da pilha).
        no_atual = fronteira.pop() 
        
        if no_atual.estado == estado_objetivo:
            return no_atual.caminho()
        
        # Expande o nó
        # [::-1] é usado para inverter a ordem de iteração, garantindo que
        # o DFS explore os vizinhos na ordem alfabética inversa (se essa for a preferência).
        for proximo_estado in problema_grafo.get(no_atual.estado, [])[::-1]: 
            if proximo_estado not in explorados:
                explorados.add(proximo_estado)
                
                # CHILD-NODE: Cria o novo nó filho
                no_filho = Node(estado=proximo_estado, pai=no_atual, acao=f"Ir para {proximo_estado}")
                
                # INSERIR: Adiciona o novo nó ao topo da Pilha (LIFO)
                fronteira.append(no_filho)
                
    return "Falha! Objetivo não alcançável (DFS)."

# ==============================================================================
# 5. EXECUÇÃO DAS BUSCAS
# ==============================================================================
if __name__ == '__main__':
    
    CIDADE_INICIAL = 'Arad'
    CIDADE_OBJETIVO = 'Bucareste'

    print("--- INICIANDO EXECUÇÕES ---")
    print(f"Objetivo: Encontrar caminho de {CIDADE_INICIAL} para {CIDADE_OBJETIVO}")
    print("-----------------------------\n")

    # --- EXECUÇÃO 1: BFS (FIFO) ---
    caminho_bfs = busca_em_largura_bfs(ROMENIA, CIDADE_INICIAL, CIDADE_OBJETIVO)
    
    print(">>> RESULTADO BUSCA EM LARGURA (BFS / FIFO):")
    if isinstance(caminho_bfs, list):
        print(f"Caminho: {' -> '.join(caminho_bfs)}")
        print(f"Comprimento (número de passos): {len(caminho_bfs) - 1}")
    else:
        print(caminho_bfs)
        
    print("\n" + "="*30 + "\n")

    # --- EXECUÇÃO 2: DFS (LIFO) ---
    caminho_dfs = busca_em_profundidade_dfs(ROMENIA, CIDADE_INICIAL, CIDADE_OBJETIVO)
    
    print(">>> RESULTADO BUSCA EM PROFUNDIDADE (DFS / LIFO):")
    if isinstance(caminho_dfs, list):
        print(f"Caminho: {' -> '.join(caminho_dfs)}")
        print(f"Comprimento (número de passos): {len(caminho_dfs) - 1}")
    else:
        print(caminho_dfs)

    print("\n--- FIM DAS EXECUÇÕES ---")