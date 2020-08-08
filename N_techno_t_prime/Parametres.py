import numpy as np
from itertools import permutations

# Paramètres globaux
T_life = [60, 60]   # durées de vie des techno carbonées
demande_ini = 200   # demande énergétique
X_j = [150, 200, 200] # productions maximales des techno décarbonées
X_jF = [0, 0] # valeurs finales des techno carbonées

ci_car = [30, 20] # coûts initiaux des techno carbonées
p_0 = [0.7, 0.3] # part des technologies carbonées dans le mix initial
ci_decar = [60, 70, 80] # coûts initiaux des techno décarbonées

alpha = 0   # coefficient d'évolution de la demande

n = 5 # nombre total de technologies (carbonées et décarbonées)
m = 3 # nombre total de technologies décarbonées

# Limites
# b1 = (1, 1000)   # Limites de C
# b2 = (1, 500)    # Limites de K
# b3 = (1, t_f)     # Limites de T_1
# bnds = (b1, b2, b3)

# Valeurs initiales
x0 = np.array([])

x0 = np.append(x0, [10, 30, 40])  # valeur initiale de t_i
x0 = np.append(x0, [10, 20, 5])    # valeur initiale de c_i
x0 = np.append(x0, [100, 220])    # valeur initiale de k_j



# Contraintes
max_budget_carbone = 9000
max_surcout = 100000
max_pente_couts = 5

