import random
from collections import deque
import time

def robo_limpeza(coln, row, dirt):
    matriz = [['L' for _ in range(coln)] for _ in range(row)] # Cria a matriz
    
    # João espalha lixo
    for _ in range(dirt):
        x = random.randint(0, row -1)
        y = random.randint(0, coln -1)

        matriz[x][y] = 'S'

    x = random.randint(0, row -1)
    y = random.randint(0, coln -1)
    posicao_robo = [x,y] # Posição aleatoria do Robo

    if matriz[posicao_robo[0]][posicao_robo[1]] == 'S':
        # Se o robo comecar em uma posicao de sujeira ele "Limpa" a posicao
        matriz[posicao_robo[0]][posicao_robo[1]] = 'R'
    else:
        matriz[posicao_robo[0]][posicao_robo[1]] = 'R'

    while existe_sujeira(matriz):
        path = bfs_caminho(matriz, tuple(posicao_robo), lambda p: matriz[p[0]][p[1]] == 'S')

        if not path:
            break

        for step in path[1:]:
            matriz[posicao_robo[0]][posicao_robo[1]] = 'L'
            if matriz[step[0]][step[1]] == 'S':
                matriz[step[0]][step[1]] = 'R'
            else:
                matriz[step[0]][step[1]] = 'R'

            posicao_robo = step
            mostrar_matriz(matriz)
            time.sleep(1)
    

def vizinhos(pos, row, coln):
        # Funcao pra tentam mover o Robo e atualizar matriz
        x,y = pos
        for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < row and 0 <= ny < coln:
                yield (nx, ny)


def bfs_caminho(matriz, start, objetivo_cond):
    # BFS para achar o caminho mais curto até uma sujeira
    row, coln = len(matriz), len(matriz[0])
    queue = deque([start])
    parent = {start: None}
    while queue:
        cur = queue.popleft()
        if objetivo_cond(cur):
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path 
        for nb in vizinhos(cur, row, coln):
            if nb not in parent:
                parent[nb] = cur
                queue.append(nb)
    return None    


def existe_sujeira(matriz):
    # Procurar sujeira na matriz
    return any('S' in row for row in matriz)


def mostrar_matriz(matriz):
    # mostrar a matriz
    for linha in matriz:
        print(' '.join(linha))
    print()


def mover_robo(matriz, old_pos, new_pos):
    # Função pra mover o Robo
    ox, oy = old_pos
    nx, ny = new_pos

    matriz[ox][oy] = 'L'

    if matriz[nx][ny] == 'S':
        matriz[nx][ny] = 'L'
    else:
        matriz[nx][ny] = 'R'
    return (nx, ny)

robo_limpeza(4,4,4)