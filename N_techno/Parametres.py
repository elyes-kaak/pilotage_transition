import numpy as np

# Paramètres globaux
T_life = [20, 30, 30]#, 60]   # durées de vie des techno carbonées
demande_ini = 440   # demande énergétique
X_j = [1000, 20, 50, 1000, 100] # productions maximales des techno décarbonées
X_jF = [240, 0, 0] # valeurs finales des techno carbonées

X_j_0 = [17, 62, 0, 6, 2] # productions initiales des technos décarbonées
ci_car = [56.42, 65.18, 85.77] # coûts initiaux (variables) des techno carbonées

p_0 = [0.9451, 0.0184, 0.0365] # part des technologies carbonées dans le mix initial
p_1 = [0.9451, 0.0184, 0.0365] # part des technologies carbonées dans le mix initial

ci_decar = [116.945, 75, 79.67, 286.62, 120] # coûts initiaux des techno décarbonées

type_dec = ['Eolien', 'Hydro', 'Biogaz', 'Solaire', 'Biomasse']
type_car = ['Nucleaire', 'Charbon', 'Gaz']

beta_car = [0, 0, 0]
beta_decar = [0, 0, 0, 0, 0]

n = len(type_dec) + len(type_car) # nombre total de technologies (carbonées et décarbonées)
m = len(type_dec) # nombre total de technologies décarbonées

t_f = 30 # instant de fin de transition

# Limites
b2 = ((1, 500),)   # Limites de C
b3 = ((1, 10000),)    # Limites de K
b1 = ((1, t_f),)    # Limites de T_i
bnds = list(m * b1 + m * b2 + (n-m) * b3)


# Valeurs initiales
x0 = np.array([])

x0 = np.append(x0, [1, 10, 15, 20, 25])  # valeur initiale de t_i
x0 = np.append(x0, [10, 10, 10, 10, 10])    # valeur initiale de c_i
x0 = np.append(x0, [100, 100, 100])    # valeur initiale de k_j


x_ref = np.array([])

x_ref = np.append(x_ref, [min(T_life) for i in range(m)])  # valeur initiale de t_i
x_ref = np.append(x_ref, [70, 60, 55, 50, 45])    # valeur initiale de c_i
x_ref = np.append(x_ref, [100, 220, 250])    # valeur initiale de k_j

# Contraintes
max_budget_carbone = 13000
max_surcout = 10000000
max_derivee = 250
max_ecart_demande = 0.1

pas_temps = 0.1
max_temps = 30.1

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

    return c_i + '\n' + t_i + '\n' + k_i + '\n'