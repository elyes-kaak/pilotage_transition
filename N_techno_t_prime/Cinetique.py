import scipy.integrate as integrate
from N_techno.Parametres import *
from scipy.optimize import fsolve


# Cinétique à la ligne de transition (entre t_1 et t_car)

class Cinetique:

    def __init__(self):
        self.t_prime = []
        self.index_tra = 0
        self.x_dec = np.zeros(m)
        self.x_car = [p_0[j] * self.cinetique_demande(0) for j in range(n-m)]
        self.t_prime = [0]
        self.t_f = False

    def cinetique_demande(self, t):
        return demande_ini + alpha * t

    def part_car(self, t, x, j):
        return self.cinetique_techno_carb(t, x, j) / self.cinetique_demande(t)

    def trouver_t_prime(self, i, x):
        t_initial_guess = 0
        t_solution, info_dict, ier, mesg = fsolve(lambda t : self.x_decar_ligne(t, x, i) - X_j[i], t_initial_guess, full_output=True)
        print(i)
        print(t_solution, ier, mesg)
        if (ier != 1):
            self.t_f = True
            t_solution = fsolve(lambda t: sum(self.x_car_ligne(t, x, j, i) - X_j[j] for j in range(n-m)), t_initial_guess)
            print(t_solution, ier, mesg)
        if(i == m - 1) :
            self.t_prime.append(t_solution[0])
        else :
            self.t_prime.append(min(x[i+1], t_solution[0]))

    def x_car_ligne(self, t, x, j, i):
        if(t <= T_life[j]):
            x_ini = self.x_car[j]
            return (x_ini - X_jF[j]) * ((T_life[j] - t) / (T_life[j] - x[i])) ** (x[2*m + j - 1] / x[m - 1 + i]) + X_jF[j]

        return X_jF[j]

    def x_decar_ligne(self, t, x, j):
        return self.cinetique_demande(t) - sum(self.x_dec) - sum(self.x_car_ligne(t, x, k, j) for k in range(n-m))

    def cinetique_techno_carb(self, t, x, j):
        if(t < x[0]) :
            self.x_car[j] = p_0[j] * self.cinetique_demande(t)
            return self.x_car[j]

        elif t >= T_life[j] :
            self.x_car[j] = X_jF[j]
            return self.x_car[j]

        else :
            for i in range(m) :
                if(i == m-1) :
                    self.index_tra = m

                elif(t>=x[i] and t<x[i+1]):
                    self.index_tra = i + 1
                    break

            if(len(self.t_prime) <= self.index_tra) :
                self.trouver_t_prime(self.index_tra - 1, x)

            if(t < self.t_prime[-1]) :
                self.x_car[j] = self.x_car_ligne(t, x, j, self.index_tra - 1)
                return self.x_car[j]

            self.x_car[j] = max(X_jF[j], self.part_car(self.t_prime[-1], x, j) * (self.cinetique_demande(t) - sum(self.x_dec)))
            return self.x_car[j]


    def cinetique_techno_decar(self, t, x, i):
        if(t < x[i]) :
            return 0

        elif self.t_prime[-1] > x[i] :
            if(t < self.t_prime[-1]) :
                xi = self.x_decar_ligne(t, x, i)
                self.x_dec[i] = xi
                return xi

            elif self.t_f :
                return (self.x_dec[i] / self.cinetique_demande(self.t_prime[-1])) * self.cinetique_demande(t)

            return self.x_dec[i]

    def tableau_evol(self, x):
        temps = [i for i in np.arange(0, 100, 0.5)]

        techno_dec = [[] for i in range(m)]
        techno_car = [[] for i in range(n-m)]
        for t in temps :
            for j in range(n-m) :
                techno_car[j].append(self.cinetique_techno_carb(t, x, j))
            for j in range(m) :
                techno_dec[j].append(self.cinetique_techno_decar(t, x, j))

        return temps, [techno_dec, techno_car]
