import scipy.integrate as integrate
from N_techno.Parametres import *
from scipy.optimize import fsolve


# Cinétique à la ligne de transition (entre t_1 et t_car)

class Cinetique:

    def __init__(self):
        self.t_prime = []
        self.index_tra = 0
        self.index_tra_debut = -1
        self.last_ratio = p_0
        self.last_ratio_dec = [0 for j in range(m)]
        self.x_dec = np.zeros(m)
        self.x_car = [p_0[j] * self.cinetique_demande(0) for j in range(n-m)]
        self.t_f = False

    def cmp(self, a, b):
        return (not(a > b) and not(a < b))

    def cinetique_demande(self, t):
        return demande_ini + alpha * t

    def index_transition(self, t, x):
        debut = -1
        fin = -1
        for i in range(m):
            if (i == m - 1):
                fin = m

            elif (x[i] == x[i + 1] and t >= x[i] and debut == -1):
                debut = i + 1

            if (t >= x[i] and t < x[i + 1]):
                fin = i + 1
                break

        if(debut == -1) :
            debut = fin

        return debut, fin

    def part_car(self, t, x, j):
        return self.cinetique_techno_carb(t, x, j) / self.cinetique_demande(t)

    def x_car_ligne(self, t, x, j, i):
        if(t <= T_life[j]):
            x_ini = self.x_car[j]
            return (x_ini - X_jF[j]) * ((T_life[j] - t) / (T_life[j] - x[i])) ** (x[2*m + j - 1] / x[m - 1 + i]) + X_jF[j]

        return X_jF[j]

    def x_decar_ligne(self, t, x, j):
        return max(0, self.cinetique_demande(t) - sum([self.x_dec[k] for k in range(j)]) - sum(self.x_car[k] for k in range(n-m)))

    def cinetique_techno_carb(self, t, x, j):
        if(t < x[0]) :
            self.x_car[j] = p_0[j] * self.cinetique_demande(t)
            return self.x_car[j]

        elif t >= T_life[j] or self.t_f == True :
            self.x_car[j] = X_jF[j]
            return self.x_car[j]

        else :
            self.index_tra_debut, self.index_tra = self.index_transition(t, x)

            if(self.cmp([self.x_dec[k] for k in range(self.index_tra_debut - 1, self.index_tra)], [X_j[k] for k in range(self.index_tra_debut - 1, self.index_tra)])) :
                self.x_car[j] = self.last_ratio[j] * (self.cinetique_demande(t) - sum([self.x_dec[k] for k in range(m)]))

            else :
                self.x_car[j] = self.x_car_ligne(t, x, j, self.index_tra - 1)
                self.last_ratio[j] = self.x_car[j] / (self.cinetique_demande(t) - sum(self.x_dec))

            return self.x_car[j]

    def cinetique_techno_decar(self, t, x, i):
        if (np.all(np.abs(np.array([self.x_car[k] for k in range(n-m)]) - np.array([X_jF[k] for k in range(n-m)])) <= 0.05 * np.array([X_jF[k] for k in range(n-m)]))):
            self.t_f = True

        if(self.t_f) :
            self.x_dec[i] = (self.cinetique_demande(t) - sum(self.x_car)) * self.last_ratio_dec[i]
            return self.x_dec[i]

        if(t < x[i]) :
            self.x_dec[i] = 0
            return 0

        elif( i < m-1 ) :
            if(t >= x[i] and t < x[i+1] ) :
                self.x_dec[i] = min(self.x_decar_ligne(t, x, i), X_j[i])

            self.last_ratio_dec[i] = self.x_dec[i] / (self.cinetique_demande(t) - sum(self.x_car))
            return self.x_dec[i]

        else :
            if(t >= x[m-1]) :
                self.x_dec[m-1] = min(self.x_decar_ligne(t, x, m-1), X_j[m-1])
            self.last_ratio_dec[m-1] = self.x_dec[m-1] / (self.cinetique_demande(t) - sum(self.x_car))
            return self.x_dec[m-1]


    def tableau_evol(self, x):
        temps = [i for i in np.arange(0, 100, 0.1)]

        techno_dec = [[] for i in range(m)]
        techno_car = [[] for i in range(n-m)]
        for t in temps :
            self.last_demand = self.cinetique_demande(t)
            for j in range(n-m) :
                techno_car[j].append(self.cinetique_techno_carb(t, x, j))
            for j in range(m) :
                techno_dec[j].append(self.cinetique_techno_decar(t, x, j))

        return temps, [techno_dec, techno_car]
