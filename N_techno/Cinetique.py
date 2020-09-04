import scipy.integrate as integrate
from N_techno.Parametres import *
from scipy.optimize import fsolve
import math


# Cinétique à la ligne de transition (entre t_1 et t_car)

class Cinetique:

    def __init__(self, ci):
        self.t_prime = [-1 for i in range(m)]
        self.index_tra = 0
        self.index_tra_debut = 0
        self.last_ratio = p_1
        self.instant_actuel = 0
        self.last_ratio_dec = [0 for j in range(m)]
        self.x_dec = np.zeros(m)
        self.x_car = [p_0[j] * self.cinetique_demande(0) for j in range(n-m)]
        self.x_car_ini = [p_0[j] * self.cinetique_demande(0) for j in range(n - m)]
        self.t_f = False
        self.ci_dec = ci

    def cmp(self, a, b):
        return (not(a > b) and not(a < b))

    def cinetique_demande(self, t):
        if(t <= 34) :
            return demande_ini - 0.0016 * t**4 + 0.1097 * t**3 - 1.9561 * t**2 + 5.9101 * t
        else :
            return self.cinetique_demande(34)

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
        x = x_to_bnds(x)

        T_life_atteint = [t > T_life[j] for j in range(n-m)]

        if t >= x[0] :
            self.index_tra_debut, self.index_tra = self.index_transition(t, x)

        if(self.instant_actuel < x[self.index_tra - 1] and t >= x[self.index_tra - 1]) :
            self.x_car_ini = [elem for elem in self.x_car]

        for i in range(self.index_tra_debut - 1) :
            if(self.t_prime[i] == -1) :
                self.t_prime[i] = self.instant_actuel

        self.instant_actuel = t

        if (np.all(np.abs(np.array([self.x_car[k] for k in range(n-m)]) - np.array([X_jF[k] for k in range(n-m)])) <= 0.05 * np.array([X_jF[k] for k in range(n-m)]))):
            self.t_f = True
            for i in range(m) :
                if(self.t_prime[i] == -1) :
                    self.t_prime[i] = t

        if (t <= x[0]):
            for j in range(n-m) :
                if(T_life_atteint[j]) :
                    self.x_car[j] = X_jF[j]
                else :
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
                    if (T_life_atteint[j]):
                        self.x_car[j] = X_jF[j]
                    else:
                        self.x_car[j] = max(X_jF[j], self.last_ratio[j] * (self.cinetique_demande(t) - sum([self.x_dec[k] for k in range(m)])))

            else :
                for j in range(n-m) :
                    self.x_car[j] = self.x_car_ligne(t, x, j, self.index_tra - 1)

                X_j_atteint = []
                for j in range(self.index_tra_debut - 1, self.index_tra) :
                    self.x_dec[j] = max(0, (1/len(range(self.index_tra_debut - 1, self.index_tra))) *
                                        (self.cinetique_demande(t) -
                                         sum([self.x_dec[k] for k in range(self.index_tra_debut - 1)]) -
                                         sum(self.x_car[k] for k in range(n-m))))

                    if(self.x_dec[j] > X_j[j]) :
                        X_j_atteint.append(j)
                        if(self.t_prime[j] == -1):
                            self.t_prime[j] = t

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

                if (self.cmp([self.x_dec[k] for k in range(self.index_tra_debut - 1, self.index_tra)],
                             [X_j[k] for k in range(self.index_tra_debut - 1, self.index_tra)])):
                    for j in range(n - m):
                        if (T_life_atteint[j]):
                            self.x_car[j] = X_jF[j]
                        else:
                            self.x_car[j] = max(X_jF[j], self.last_ratio[j] * (
                            self.cinetique_demande(t) - sum([self.x_dec[k] for k in range(m)])))

                S_dec = sum(self.x_dec)
                S_car = sum(self.x_car)
                for j in range(m) :
                    if(S_dec == 0) :
                        self.last_ratio_dec[j] = 0
                    else :
                        self.last_ratio_dec[j] = self.x_dec[j] / S_dec

                for j in range(n-m) :
                    if(S_car == 0) :
                        self.last_ratio[j] = 0

                    else :
                        self.last_ratio[j] = self.x_car[j] / S_car

    def x_car_ligne(self, t, x, j, i):
        if(t <= T_life[j]):
            x_ini = self.x_car_ini[j]
            return (x_ini - X_jF[j]) * ((T_life[j] - t) / (T_life[j] - x[i])) ** (x[2*m + j] / x[m + i]) + X_jF[j]

        return X_jF[j]

    def cinetique_techno_carb(self, t, x, j):
        if (self.instant_actuel != t):
            self.mix_instant_t(t, x)
        return self.x_car[j]

    def cinetique_techno_decar(self, t, x, i):
        if(self.instant_actuel != t) :
            self.mix_instant_t(t, x)
        return self.x_dec[i]

    def cout_dec(self, t, x, j):
        x = x_to_bnds(x)

        _ , i_trans = self.index_transition(x[j], x)

        cout_transition = x[m + i_trans - 1]
        if(t < x[j]) :
            return ((cout_transition - self.ci_dec[j]) / x[j]) * t + self.ci_dec[j]

        elif(t > self.t_prime[j] and self.t_prime[j] > -1) :
            return beta_decar[j] * (t - self.t_prime[j]) + cout_transition

        return cout_transition

    def cout_car(self, t, x, j):

        x = x_to_bnds(x)

        if(t < x[0]) :
            _, i_trans = self.index_transition(x[0], x)
            cout_transition = x[m + i_trans - 1]
            return ((cout_transition - ci_car[j]) / x[0]) * t + ci_car[j]

        else :
            i_trans_debut, i_trans = self.index_transition(t, x)
            cout_transition = x[m + i_trans - 1]
            for k in range(i_trans_debut - 1, i_trans) :
                if(self.t_prime[k] == -1) :
                    return cout_transition

            if(i_trans == m) :
                return beta_car[j] * (t - max([self.t_prime[k] for k in range(i_trans_debut - 1, i_trans)])) + cout_transition

            return ((x[m + i_trans] - cout_transition) / (x[i_trans] - max([self.t_prime[k] for k in range(i_trans_debut - 1, i_trans)])) * (t - max([self.t_prime[k] for k in range(i_trans_debut - 1, i_trans)])) + cout_transition)

    def cout_car_nat(self, t, j):
        return beta_car[j] * t + ci_car[j]

    def cout_dec_nat(self,t, j):
        return beta_decar[j] * t + self.ci_dec[j]

    def taxes_car(self, t, x, j):
        return self.cout_car(t, x, j) - self.cout_car_nat(t, j)

    def taxes_dec(self, t, x, j):
        return self.cout_dec(t, x, j) - self.cout_dec_nat(t, j)