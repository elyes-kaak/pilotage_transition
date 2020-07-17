import numpy as np
from Parametres import *
from sympy import *
import scipy.integrate as integrate

# Cinétique à la ligne de transition (entre t_1 et t_car)

class Cinetique:

    def cinetique_cout(self, t, x, c_init):
        return ((x[0] - c_init) * t / x[2]) + c_init

    def abs_pente_cout(self, x, c_init):
        return abs((x[0] - c_init) / x[2])

    def evol_taxe(self, t, x, c_init, coeff):
        if(t <= x[2]) :
            return self.cinetique_cout(t, x, c_init) - coeff * t - c_init

        return x[0] - coeff * t - c_init

    def cinetique_demande(self, t):
        return demande_ini + alpha * t

    def cinetique_techno(self, t, x):
        x_1 = (self.cinetique_demande(x[2]) - self.cinetique_demande(T_life) + X_2) * (((T_life - t) / (T_life - x[2])) ** (x[1] / x[0])) + (self.cinetique_demande(T_life) - X_2)

        if(self.cinetique_demande(t) - x_1 > X_2) :
            return self.cinetique_demande(t)-X_2

        if(x_1 < 0) :
            return 0

        return x_1

    def chal_latente(self, x):
        return x[0] * integrate.quad(lambda t : self.cinetique_demande(t)-self.cinetique_techno(t, x), x[2], T_life)[0]

    def budget_carbone(self, x):
        return integrate.quad(lambda t : self.cinetique_demande(t), 0, x[2])[0] + integrate.quad(lambda t : self.cinetique_techno(t, x), x[2], t_f)[0]

    def surcout_trajectoire(self, x):
        a1 = integrate.quad(lambda t : self.evol_taxe(t, x, c1i, alpha_c1) * self.cinetique_demande(t), 0, x[2])[0] # taxe dans la phase carbonée
        a2 = integrate.quad(lambda t : self.evol_taxe(t, x, c1i, alpha_c1) * self.cinetique_techno(t, x), x[2], t_f)[0] # taxe sur x1 de t1 à tf
        a3 = integrate.quad(lambda t : self.evol_taxe(t, x, c2i, alpha_c2) * (self.cinetique_demande(t) - self.cinetique_techno(t, x)), x[2], t_f)[0]  # taxe sur x2 de 0 à tf

        surcout = a1 + a2 + a3 - self.chal_latente(x)

        return abs(surcout)

    def eq_evol(self, x):
        temps = [i for i in np.arange(0, T_life + 0.5, 0.5)]
        cout_1, cout_2 = [], []
        for t in temps :
            if(t <= x[2]):
                cout_1.append(self.cinetique_cout(t, x, c1i))
                cout_2.append(self.cinetique_cout(t, x, c2i))
            else :
                cout_1.append(x[0])
                cout_2.append(x[0])

        techno_1, techno_2 = [], []
        for t in temps :
            if(t < x[2]):
                techno_1.append(self.cinetique_demande(t))
                techno_2.append(0)
            else :
                techno_1.append(self.cinetique_techno(t, x))
                techno_2.append(self.cinetique_demande(t) - self.cinetique_techno(t, x))

        taxe_1, taxe_2 = [], []
        for t in temps :
            taxe_1.append(self.evol_taxe(t, x, c1i, alpha_c1))
            taxe_2.append(self.evol_taxe(t, x, c2i, alpha_c2))
        return temps, [cout_1, cout_2], [techno_1, techno_2], [r'carbon\'ee', r'd\'ecarbon\'ee'], [self.cinetique_demande(t) for t in temps], [taxe_1, taxe_2]
