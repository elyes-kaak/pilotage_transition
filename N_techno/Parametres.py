import numpy as np
from itertools import permutations
import math

# Paramètres globaux
T_life = [60, 60, 60, 60]   # durées de vie des techno carbonées
demande_ini = 440   # demande énergétique
X_j = [1000, 1000, 500, 1000, 1000, 50] # productions maximales des techno décarbonées
X_jF = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01] # valeurs finales des techno carbonées

ci_car = [20, 30, 40, 30] # coûts initiaux des techno carbonées

p_0 = [0.9451, 0.0184, 0.0048, 0.0316] # part des technologies carbonées dans le mix initial
p_1 = [0.9451, 0.0184, 0.0048, 0.0316] # part des technologies carbonées dans le mix initial

ci_decar = [100, 100, 100, 100, 100, 100] # coûts initiaux des techno décarbonées

type_dec = ['Hydro', 'Biomasse', 'Geothermie', 'Solaire', 'Eolien', 'Dechets']
type_car = ['Nucleaire', 'Charbon', 'Petrole', 'Gaz']

beta_car = [-0.1, -0.2, -0.1, -0.2]
beta_decar = [-0.2, -0.6, -0.1, -0.8, -0.8, -0.1]

n = len(type_dec) + len(type_car) # nombre total de technologies (carbonées et décarbonées)
m = len(type_dec) # nombre total de technologies décarbonées

# Limites
b2 = ((1, 10000),)   # Limites de C
b3 = ((1, 10000),)    # Limites de K
b1 = ((1, min(T_life)),)     # Limites de T_i
bnds = m * b1 + m * b2 + (n-m) * b3

# Valeurs initiales
x0 = np.array([])

x0 = np.append(x0, [5, 15, 25, 30, 35, 45])  # valeur initiale de t_i
x0 = np.append(x0, [70, 60, 55, 50, 45, 40])    # valeur initiale de c_i
x0 = np.append(x0, [100, 220, 250, 150])    # valeur initiale de k_j


x_ref = np.array([])

x_ref = np.append(x_ref, [min(T_life) for i in range(m)])  # valeur initiale de t_i
x_ref = np.append(x_ref, [70, 60, 55, 50, 45, 40])    # valeur initiale de c_i
x_ref = np.append(x_ref, [100, 220, 250, 150])    # valeur initiale de k_j

# Contraintes
max_budget_carbone = 9000
max_surcout = 10000000
max_pente_couts = 5


def x_to_bnds(x):
    x_new = np.zeros(len(x))

    for i in range(len(x)):
        x_new[i] = ((bnds[i][1] - bnds[i][0]) / math.pi) * (math.atan(x[i]) + math.pi / 2) + bnds[i][0]
        if i < m:
            x_new[i] = int(10 * x_new[i]) / 10
    return x_new


def x_to_r(x):
    x_new = np.zeros(len(x))

    for i in range(len(x)):
        x_new[i] = math.tan((math.pi * (x[i] - bnds[i][0]) / (bnds[i][1] - bnds[i][0])) - math.pi / 2)

    return x_new

def print_x(x):
    t_i = ''
    k_i = ''
    c_i = ''

    for i in range(0, m):
        t_i = t_i + 't_' + str(i) + '= ' + str(round(x[i], 2)) + ' '
        c = x[m + i]
        for j in range(i + 1, m):
            if (x[j] == x[i]):
                c = x[m + j]
        c_i = c_i + 'c_' + str(i) + '= ' + str(round(c, 2)) + ' '

    for i in range(n - m):
        k_i = k_i + 'k_' + str(i) + '= ' + str(round(x[2 * m + i], 2)) + ' '

    print(c_i)
    print(t_i)
    print(k_i)
    print()

x0 = x_to_r(x0)
x_ref = x_to_r(x_ref)