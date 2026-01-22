import random
import numpy as np

# REPRESENTAÇÃO
# Cromossomo: lista de tamanho N
# índice = coluna, valor = linha

def criar_individuo(n):
    return [random.randint(0, n - 1) for _ in range(n)]


def criar_populacao(tamanho, n):
    return [criar_individuo(n) for _ in range(tamanho)]

# FUNÇÃO DE APTIDÃO
def fitness_n_rainhas(individuo):
    conflitos = 0
    n = len(individuo)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(individuo[i] - individuo[j]) == abs(i - j):
                conflitos += 1
    return -conflitos  # maximização

# SELEÇÃO

def selecao_torneio(populacao, fitness, k=3):
    selecionados = random.sample(populacao, k)
    return max(selecionados, key=fitness)

# CRUZAMENTO
def cruzamento_um_ponto(pai1, pai2):
    ponto = random.randint(1, len(pai1) - 2)
    return (
        pai1[:ponto] + pai2[ponto:],
        pai2[:ponto] + pai1[ponto:]
    )

# MUTAÇÃO
def mutacao(individuo, taxa, n):
    if random.random() < taxa:
        coluna = random.randint(0, n - 1)
        individuo[coluna] = random.randint(0, n - 1)
    return individuo

# ALGORITMO GENÉTICO
def ga_n_rainhas(
    n,
    tamanho_pop=100,
    geracoes=500,
    taxa_cruz=0.8,
    taxa_mut=0.05,
    seed=None
):
    if seed is not None:
        random.seed(seed)

    pop = criar_populacao(tamanho_pop, n)

    for _ in range(geracoes):
        nova_pop = []

        while len(nova_pop) < tamanho_pop:
            p1 = selecao_torneio(pop, fitness_n_rainhas)
            p2 = selecao_torneio(pop, fitness_n_rainhas)

            if random.random() < taxa_cruz:
                f1, f2 = cruzamento_um_ponto(p1, p2)
            else:
                f1, f2 = p1[:], p2[:]

            nova_pop.append(mutacao(f1, taxa_mut, n))
            nova_pop.append(mutacao(f2, taxa_mut, n))

        pop = nova_pop[:tamanho_pop]

    melhor = max(pop, key=fitness_n_rainhas)
    return melhor, fitness_n_rainhas(melhor)

for s in [1, 2, 3, 5, 11]:
    sol, fit = ga_n_rainhas(n=8, seed=s)
    print(f"Seed {s} | Fitness: {fit} | Solução: {sol}")