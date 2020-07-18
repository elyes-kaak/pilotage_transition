import numpy as np

# Paramètres globaux
t_f = 50  # date de fin de transition
T_life = 60   # durée de vie de la technologie x1
demande_ini = 200   # demande énergétique
X_2 = 150  # production maximale de la technologie 2
c1i = 30   # coût initial de la technologie 1
c2i = 60   # coût initial de la technologie 2
seuil = 0.01   # moment où la transition est accomplie
alpha = 0   # coefficient d'évolution de la demande
beta_c1 = 0   # coefficient d'évolution naturelle du coût de la technologie 1
beta_c2 = 0   # coefficient d'évolution naturelle du coût de la technologie 2
crise = 15
gama = 0.9

# Contraintes
max_budget_carbone = 9000
max_surcout = 100000
max_pente_couts = 10

# Limites
b1 = (1, 1000)   # Limites de C
b2 = (1, 320)    # Limites de K
b3 = (1, t_f)     # Limites de T_1
bnds = (b1, b2, b3)

# Valeurs initiales
n = 3
x0 = np.zeros(n)

x0[0] = 10   # valeur initiale de C
x0[1] = 10    # valeur initiale de K
x0[2] = 10    # valeur initiale de t_1