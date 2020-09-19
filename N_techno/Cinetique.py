#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Parametres_Allemagne import *

# Cinétique à la ligne de transition (entre t_1 et t_car)

class Cinetique:

    def __init__(self, x):
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
        self.instant_f = -1
        instant_tra = np.array(x[0: m])
        cout_tra = np.array(x[m: 2 * m])
        k_car = x[2 * m: n + m]

        perm = sorted(range(len(instant_tra)), key=lambda k: instant_tra[k])

        self.x = np.around(np.concatenate((instant_tra[perm], cout_tra[perm], k_car)), decimals=2)
        self.ordre_dec = np.array(type_dec.copy())[perm]
        self.xj = np.array(X_j.copy())[perm]
        self.ci_dec = np.array(ci_decar.copy())[perm]

    def cmp(self, a, b):
        return (not(a > b) and not(a < b))

    def cinetique_demande(self, t):
        if (t <= 34):
            return demande_ini - 0.0016 * t ** 4 + 0.1097 * t ** 3 - 1.9561 * t ** 2 + 5.9101 * t
        else:
            return self.cinetique_demande(34)

    def index_transition(self, t):
        debut = -1
        fin = -1
        for i in range(m):
            if (i == m - 1):
                fin = m

            if (t >= self.x[i] and t < self.x[i + 1]):
                fin = i + 1
                break
        for i in range(m):
            if(self.x[i] == self.x[fin - 1]) :
                debut = i + 1
                break

        return debut, fin

    def mix_instant_t(self, t):

        T_life_atteint = [t > T_life[j] for j in range(n-m)]

        if t >= self.x[0] :
            self.index_tra_debut, self.index_tra = self.index_transition(t)

        if(self.instant_actuel < self.x[self.index_tra - 1] and t >= self.x[self.index_tra - 1]) :
            self.x_car_ini = [elem for elem in self.x_car]

        for i in range(self.index_tra_debut - 1) :
            if(self.t_prime[i] == -1) :
                self.t_prime[i] = self.instant_actuel

        self.instant_actuel = t

        if (np.all(np.abs(np.array([self.x_car[k] for k in range(n-m)]) - np.array([X_jF[k] for k in range(n-m)])) <= 0.05 * np.array([max(1, X_jF[k]) for k in range(n-m)]))):

            self.t_f = True
            if(self.instant_f == -1) :
                self.instant_f = t

            for i in range(m) :
                if(self.t_prime[i] == -1) :
                    self.t_prime[i] = t

        if (t <= self.x[0]):
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

            X_j_atteint = []
            limites_dec_respectees = False

            total_dec = self.cinetique_demande(t) - sum(self.x_car)

            while (limites_dec_respectees == False):
                limites_dec_respectees = True
                for j in range(m):
                    if j in X_j_atteint:
                        self.x_dec[j] = self.xj[j]
                        self.last_ratio_dec[j] = self.xj[j] / total_dec
                    else:
                        self.x_dec[j] = max(0, (self.cinetique_demande(t) - sum(self.x_car)) *
                                                            self.last_ratio_dec[j])
                        if (self.x_dec[j] > self.xj[j]):
                            X_j_atteint.append(j)
                            ecart_ratio = self.last_ratio_dec[j] - self.xj[j] / total_dec
                            for l in range(m) :
                                if(not l in X_j_atteint) :
                                    self.last_ratio_dec[l] += ecart_ratio / (m - len(X_j_atteint))
                            limites_dec_respectees = False

        else :
            if (self.cmp([self.x_dec[k] for k in range(self.index_tra_debut - 1, self.index_tra)],
                         [self.xj[k] for k in range(self.index_tra_debut - 1, self.index_tra)])):

                for j in range(n-m) :
                    if (T_life_atteint[j]):
                        self.x_car[j] = X_jF[j]
                    else:
                        self.x_car[j] = max(X_jF[j], self.last_ratio[j] * (self.cinetique_demande(t) - sum([self.x_dec[k] for k in range(m)])))

            else :
                for j in range(n-m) :
                    self.x_car[j] = self.x_car_ligne(t, j, self.index_tra - 1)

                X_j_atteint = []
                limites_dec_respectees = False
                while (limites_dec_respectees == False):
                    limites_dec_respectees = True
                    for j in range(self.index_tra_debut - 1, self.index_tra):
                        if j in X_j_atteint :
                            self.x_dec[j] = self.xj[j]
                        else :
                            self.x_dec[j] = max(0,
                                                1 / (len(range(self.index_tra_debut - 1, self.index_tra)) - len(X_j_atteint)) * (
                                                    self.cinetique_demande(t) -
                                                    sum([self.x_dec[k] for k in range(self.index_tra_debut - 1)]) -
                                                    sum([self.xj[k] for k in X_j_atteint]) -
                                                    sum(self.x_car[k] for k in range(n - m))))
                            if(self.x_dec[j] > self.xj[j]):
                                X_j_atteint.append(j)
                                if (self.t_prime[j] == -1):
                                    self.t_prime[j] = t
                                limites_dec_respectees = False


                if(sum(self.x_dec) > (self.cinetique_demande(t) - sum(X_jF))) :
                    self.t_f = True
                    for j in range(n-m) :
                        self.x_car[j] = X_jF[j]
                    for j in range(m) :
                        self.x_dec[j] = (self.cinetique_demande(t) - sum(self.x_car)) * self.last_ratio_dec[j]

                if (self.cmp([self.x_dec[k] for k in range(self.index_tra_debut - 1, self.index_tra)],
                             [self.xj[k] for k in range(self.index_tra_debut - 1, self.index_tra)])):
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

    def x_car_ligne(self, t, j, i):
        if(t <= T_life[j]):
            x_ini = self.x_car_ini[j]
            if(self.x[i] >= T_life[j]) :
                self.x[i] = T_life[j] - 0.01

            return (x_ini - X_jF[j]) * ((T_life[j] - t) / (T_life[j] - self.x[i])) ** (self.x[2*m + j] / self.x[m + i]) + X_jF[j]


        return X_jF[j]

    def cinetique_techno_carb(self, t, j):
        if (self.instant_actuel != t):
            self.mix_instant_t(t)
        return self.x_car[j]

    def cinetique_techno_decar(self, t, i):
        if(self.instant_actuel != t) :
            self.mix_instant_t(t)
        return self.x_dec[i]

    def cout_dec(self, t, j):
        _ , i_trans = self.index_transition(self.x[j])

        cout_transition = self.x[m + i_trans - 1]
        if self.instant_f > -1 and t > self.instant_f:
            return beta_decar[j] * (t - self.instant_f) + self.cout_dec(self.instant_f, j)

        elif(t < self.x[j]) :
            return ((cout_transition - self.ci_dec[j]) / self.x[j]) * t + self.ci_dec[j]

        elif(t > self.t_prime[j] and self.t_prime[j] > -1) :
            return beta_decar[j] * (t - self.t_prime[j]) + cout_transition

        return cout_transition

    def cout_car(self, t, j):

        if(t < self.x[0]) :
            _, i_trans = self.index_transition(self.x[0])
            cout_transition = self.x[m + i_trans - 1]
            return ((cout_transition - ci_car[j]) / self.x[0]) * t + ci_car[j]

        elif self.instant_f > -1 and t > self.instant_f :
            return beta_car[j] * (t - self.instant_f) + self.cout_car(self.instant_f, j)

        else :
            i_trans_debut, i_trans = self.index_transition(t)
            cout_transition = self.x[m + i_trans - 1]
            for k in range(i_trans_debut - 1, i_trans) :
                if(self.t_prime[k] == -1) :
                    return cout_transition

            if(i_trans == m) :
                return beta_car[j] * (t - max([self.t_prime[k] for k in range(i_trans_debut - 1, i_trans)])) + cout_transition

            return ((self.x[m + i_trans] - cout_transition) / (self.x[i_trans] - max([self.t_prime[k] for k in range(i_trans_debut - 1, i_trans)])) * (t - max([self.t_prime[k] for k in range(i_trans_debut - 1, i_trans)])) + cout_transition)

    def cout_car_nat(self, t, j):
        return beta_car[j] * t + ci_car[j]

    def cout_dec_nat(self,t, j):
        return beta_decar[j] * t + self.ci_dec[j]

    def taxes_car(self, t, j):
        return self.cout_car(t, j) - self.cout_car_nat(t, j)

    def taxes_dec(self, t, j):
        return self.cout_dec(t, j) - self.cout_dec_nat(t, j)