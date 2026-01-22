import math
import random
import numpy as np

# REPRESENTAÇÃO
# Cromossomo: permutação das cidades

def criar_individuo_tsp(n):
    individuo = list(range(n))
    random.shuffle(individuo)
    return individuo


def criar_populacao_tsp(tamanho, n):
    return [criar_individuo_tsp(n) for _ in range(tamanho)]

# FUNÇÃO DE APTIDÃO
def distancia(c1, c2):
    return math.dist(c1, c2)

def fitness_tsp(individuo, cidades):
    total = 0
    for i in range(len(individuo)):
        c1 = cidades[individuo[i]]
        c2 = cidades[individuo[(i + 1) % len(individuo)]]
        total += distancia(c1, c2)
    return 1 / total

# SELEÇÃO
def selecao_roleta(populacao, fitness, cidades):
    soma = sum(fitness(ind, cidades) for ind in populacao)
    r = random.uniform(0, soma)
    acumulado = 0
    for ind in populacao:
        acumulado += fitness(ind, cidades)
        if acumulado >= r:
            return ind

# CRUZAMENTO (OX)
def crossover_ox(p1, p2):
    a, b = sorted(random.sample(range(len(p1)), 2))
    filho = [-1] * len(p1)
    filho[a:b] = p1[a:b]

    pos = b
    for gene in p2:
        if gene not in filho:
            if pos >= len(p1):
                pos = 0
            filho[pos] = gene
            pos += 1

    return filho

# MUTAÇÃO
def mutacao_swap(individuo, taxa):
    if random.random() < taxa:
        i, j = random.sample(range(len(individuo)), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo

# ALGORITMO GENÉTICO
def ga_tsp(
    cidades,
    tamanho_pop=100,
    geracoes=500,
    taxa_cruz=0.9,
    taxa_mut=0.02,
    seed=None
):
    if seed is not None:
        random.seed(seed)

    n = len(cidades)
    pop = criar_populacao_tsp(tamanho_pop, n)

    for _ in range(geracoes):
        nova_pop = []

        while len(nova_pop) < tamanho_pop:
            p1 = selecao_roleta(pop, fitness_tsp, cidades)
            p2 = selecao_roleta(pop, fitness_tsp, cidades)

            if random.random() < taxa_cruz:
                filho = crossover_ox(p1, p2)
            else:
                filho = p1[:]

            nova_pop.append(mutacao_swap(filho, taxa_mut))

        pop = nova_pop

    melhor = max(pop, key=lambda ind: fitness_tsp(ind, cidades))
    return melhor, fitness_tsp(melhor, cidades)

cidades = [(random.random(), random.random()) for _ in range(10)]
for s in [10, 20, 30]:
    sol, fit = ga_tsp(cidades, seed=s)
    print(f"Seed {s} | Fitness: {fit}")