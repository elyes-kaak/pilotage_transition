import scipy.integrate as integrate
from N_techno.Parametres import *
from scipy.optimize import fsolve


# Cinétique à la ligne de transition (entre t_1 et t_car)

class Cinetique:

    def __init__(self):
        self.t_prime = []
        self.index_tra = 0
        self.index_tra_debut = 0
        self.last_ratio = p_0
        self.instant_actuel = 0
        self.last_ratio_dec = [0 for j in range(m)]
        self.x_dec = np.zeros(m)
        self.x_car = [p_0[j] * self.cinetique_demande(0) for j in range(n-m)]
        self.x_car_ini = [p_0[j] * self.cinetique_demande(0) for j in range(n - m)]
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

            if (t >= x[i] and t < x[i + 1]):
                fin = i + 1
                break
        for i in range(m):
            if(x[i] == x[fin - 1]) :
                debut = i + 1
                break

        return debut, fin

    def mix_instant_t(self, t, x):
        self.index_tra_debut, self.index_tra = self.index_transition(t, x)

        if(self.instant_actuel < x[self.index_tra - 1] and t >= x[self.index_tra - 1]) :
            self.x_car_ini = [elem for elem in self.x_car]

        self.instant_actuel = t

        if (np.all(np.abs(np.array([self.x_car[k] for k in range(n-m)]) - np.array([X_jF[k] for k in range(n-m)])) <= 0.05 * np.array([X_jF[k] for k in range(n-m)]))):
            self.t_f = True

        if (t <= x[0]):
            for j in  range(n-m) :
               self.x_car[j] = p_0[j] * self.cinetique_demande(t)

            for j in range(m) :
                self.x_dec[j] = 0

        elif(self.t_f == True) :
            for j in range(n - m):
                self.x_car[j] = X_jF[j]

            for j in range(m):
                self.x_dec[j] = (self.cinetique_demande(t) - sum(self.x_car)) * self.last_ratio_dec[j]

        else :
            if (self.cmp([self.x_dec[k] for k in range(self.index_tra_debut - 1, self.index_tra)],
                         [X_j[k] for k in range(self.index_tra_debut - 1, self.index_tra)])):

                for j in range(n-m) :
                    self.x_car[j] = max(X_jF[j], self.last_ratio[j] * (self.cinetique_demande(t) - sum([self.x_dec[k] for k in range(m)])))

            else :
                for j in range(n-m) :
                    self.x_car[j] = self.x_car_ligne(t, x, j, self.index_tra - 1)

                X_j_atteint = []
                for j in range(self.index_tra_debut - 1, self.index_tra) :
                    self.x_dec[j] = max(0, (1/len(range(self.index_tra_debut - 1, self.index_tra))) * (self.cinetique_demande(t) - sum([self.x_dec[k] for k in range(self.index_tra_debut - 1)]) - sum(self.x_car[k] for k in range(n-m))))
                    if(self.x_dec[j] > X_j[j]) :
                        X_j_atteint.append(j)

                if (len(X_j_atteint) > 0):
                    for j in range(self.index_tra_debut - 1, self.index_tra):
                        if j in X_j_atteint :
                            self.x_dec[j] = X_j[j]
                        else :
                            self.x_dec[j] = max(0,
                                1 / (len(range(self.index_tra_debut - 1, self.index_tra)) - len(X_j_atteint)) * (
                                                self.cinetique_demande(t) -
                                                sum([self.x_dec[k] for k in range(self.index_tra_debut - 1)]) -
                                                sum([X_j[k] for k in X_j_atteint]) -
                                                sum(self.x_car[k] for k in range(n - m))))

                if(sum(self.x_dec) > (self.cinetique_demande(t) - sum(X_jF))) :
                    self.t_f = True
                    for j in range(n-m) :
                        self.x_car[j] = X_jF[j]
                    for j in range(m) :
                        self.x_dec[j] = (self.cinetique_demande(t) - sum(self.x_car)) * self.last_ratio_dec[j]

                for j in range(m) :
                    self.last_ratio_dec[j] = self.x_dec[j] / sum(self.x_dec)

                for j in range(n-m) :
                    self.last_ratio[j] = self.x_car[j] / sum(self.x_car)

                if (self.cmp([self.x_dec[k] for k in range(self.index_tra_debut - 1, self.index_tra)],
                             [X_j[k] for k in range(self.index_tra_debut - 1, self.index_tra)])):
                    for j in range(n - m):
                        self.x_car[j] = max(X_jF[j], self.last_ratio[j] * (
                        self.cinetique_demande(t) - sum([self.x_dec[k] for k in range(m)])))

    def x_car_ligne(self, t, x, j, i):
        if(t <= T_life[j]):
            x_ini = self.x_car_ini[j]
            return (x_ini - X_jF[j]) * ((T_life[j] - t) / (T_life[j] - x[i])) ** (x[2*m + j - 1] / x[m - 1 + i]) + X_jF[j]

        return X_jF[j]

    def cinetique_techno_carb(self, t, x, j):
        if (self.instant_actuel != t):
            self.mix_instant_t(t, x)
        return self.x_car[j]

    def cinetique_techno_decar(self, t, x, i):
        if(self.instant_actuel != t) :
            self.mix_instant_t(t, x)
        return self.x_dec[i]


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
