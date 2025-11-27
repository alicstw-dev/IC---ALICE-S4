import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import warnings
import pandas as pd

warnings.filterwarnings("ignore")

peso = ctrl.Antecedent(np.arange(40, 151, 1), 'peso')
altura = ctrl.Antecedent(np.arange(1.5, 2.01, 0.01), 'altura')
imc = ctrl.Consequent(np.arange(15, 46, 1), 'imc', defuzzify_method='centroid')

peso['leve']  = fuzz.trapmf(peso.universe,  [40, 40, 60, 75])
peso['medio'] = fuzz.trimf(peso.universe,   [70, 85, 100])
peso['alto']  = fuzz.trapmf(peso.universe,  [95, 110, 150, 150])

altura['baixa'] = fuzz.trapmf(altura.universe, [1.5, 1.5, 1.6, 1.7])
altura['media'] = fuzz.trimf(altura.universe,  [1.65, 1.75, 1.85])
altura['alta']  = fuzz.trapmf(altura.universe, [1.8, 1.9, 2.0, 2.0])

imc['muito_magro'] = fuzz.trimf(imc.universe, [15, 16, 18.5])
imc['saudavel']    = fuzz.trimf(imc.universe, [18.5, 23, 25])
imc['sobrepeso']   = fuzz.trimf(imc.universe, [25, 28, 30])
imc['obeso']       = fuzz.trapmf(imc.universe, [29, 35, 45, 45])

# Visualizar o universo numérico
# print(peso.universe)
# print(altura.universe)
# print(imc.universe)

# Ver quantidade de pontos
# print(len(peso.universe))
# print(len(altura.universe))
# print(len(imc.universe))

# Ver termos fuzzy disponíveis
# print(peso.terms)
# print(altura.terms)
# print(imc.terms)

# Ver valores numéricos da função de pertinência
# print(peso['leve'].mf)
# print(altura['media'].mf)
# print(imc['obeso'].mf)

# Visualização automática
peso.view()
altura.view()
imc.view()

plt.show()
