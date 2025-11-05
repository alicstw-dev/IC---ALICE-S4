class Node:
    # O estado é uma tupla (localização_aspirador, estado_A, estado_B).
    # Exemplo: ('A', 'S', 'S')
    def __init__(self, estado, pai=None, acao=None):
        self.estado = estado    # n.ESTADO: O estado do mundo.
        self.pai = pai          # n.PAI: O nó que o gerou.
        self.acao = acao        # n.AÇÃO: A ação que levou a este estado.
    
    def caminho(self):
        """Reconstrói a lista de AÇÕES que levam do início a este nó."""
        caminho_acoes = []
        no_atual = self
        while no_atual.pai is not None:
            caminho_acoes.append(no_atual.acao)
            no_atual = no_atual.pai
        # Inverte a lista para ter a ordem correta (primeira ação -> última ação)
        return caminho_acoes[::-1]
    
def aplicar_acao(estado_atual, acao):
    """
    Função CHILD-NODE: Calcula o novo estado após aplicar uma AÇÃO.
    Estado: (local, estado_A, estado_B)
    """
    local, sala_a, sala_b = estado_atual
    
    if acao == 'Aspirar':
        if local == 'A':
            # Se 'A' estiver suja ('S'), a nova sala 'A' fica 'L'
            novo_estado = (local, 'L', sala_b)
        else: # local == 'B'
            # Se 'B' estiver suja ('S'), a nova sala 'B' fica 'L'
            novo_estado = (local, sala_a, 'L')
            
    elif acao == 'Mover_Direita':
        novo_estado = ('B', sala_a, sala_b)
        
    elif acao == 'Mover_Esquerda':
        novo_estado = ('A', sala_a, sala_b)
        
    else:
        return None # Ação inválida

    # Ação de Aspirar em sala limpa é um self-loop: não altera o estado.
    return novo_estado if novo_estado != estado_atual else None


def teste_objetivo(estado):
    """Verifica se todas as salas estão limpas."""
    # O estado é objetivo se sala_a for 'L' E sala_b for 'L'
    return estado[1] == 'L' and estado[2] == 'L'

from collections import deque

def busca_aspirador_bfs(estado_inicial):
    
    # Lista de todas as ações possíveis no problema
    ACOES = ['Aspirar', 'Mover_Direita', 'Mover_Esquerda']

    # 1. Inicializa o nó raiz e a fronteira (Fila FIFO)
    no_raiz = Node(estado_inicial)
    fronteira = deque([no_raiz])
    
    # 2. Inicializa o conjunto explorado (GRAPH-SEARCH)
    explorados = {estado_inicial}
    
    while fronteira:
        
        # POP (FIFO): Remove o nó mais antigo/primeiro a entrar
        no_atual = fronteira.popleft() 
        
        # 3. Teste de Objetivo
        if teste_objetivo(no_atual.estado):
            print(f"Objetivo alcançado no estado: {no_atual.estado}")
            return no_atual.caminho()
        
        # 4. Expande o nó atual
        for acao in ACOES:
            proximo_estado = aplicar_acao(no_atual.estado, acao)
            
            # Checa se a ação é válida e se o estado não foi explorado
            if proximo_estado and proximo_estado not in explorados:
                
                # Adiciona ao conjunto explorado
                explorados.add(proximo_estado)
                
                # CHILD-NODE: Cria o novo nó filho
                no_filho = Node(estado=proximo_estado, pai=no_atual, acao=acao)
                
                # INSERIR: Adiciona o nó filho ao final da fila (FIFO)
                fronteira.append(no_filho)
                
    return "Falha! Solução não encontrada."

# Estado Inicial: (Local do Aspirador, Estado Sala A, Estado Sala B)
# Exemplo: Aspirador em 'A', Sala A Suja ('S'), Sala B Suja ('S')
ESTADO_INICIAL = ('A', 'S', 'S') 

print(f"Iniciando BFS a partir de {ESTADO_INICIAL}...")

solucao_acoes = busca_aspirador_bfs(ESTADO_INICIAL)

if isinstance(solucao_acoes, list):
    print("\n[Resultado Ótimo Encontrado (BFS)]")
    print(f"Número mínimo de ações: {len(solucao_acoes)}")
    print("Sequência de Ações:")
    for i, acao in enumerate(solucao_acoes):
        print(f"{i+1}. {acao}")
else:
    print(solucao_acoes)

# Saída esperada (óptima):
# 1. Aspirar (A fica Limpa: ('A', 'L', 'S'))
# 2. Mover_Direita (Aspirador em 'B': ('B', 'L', 'S'))
# 3. Aspirar (B fica Limpa: ('B', 'L', 'L') - Objetivo alcançado)