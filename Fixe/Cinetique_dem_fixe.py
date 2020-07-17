import numpy as np
from Parametres import *
import scipy.integrate as integrate

# Cinétique à la ligne de transition (entre t_1 et t_car)

class Cinetique:
    def cinetique_cout(self, t, x, c_init):
        return ((x[0] - c_init) * t / x[2]) + c_init

    def abs_pente_cout(self, x, c_init):
        return abs((x[0] - c_init) / x[2])

    def cinetique_evolution(self, t, x):
        return X_2 * (((T_life - t) / (T_life - x[2])) ** (x[1] / x[0])) + (demande_ini - X_2)

    def t_car(self, x):
        return T_life - (T_life - x[2]) * (seuil ** (x[0] / x[1]))

    def chal_latente(self, x):
        return x[0] * integrate.quad(lambda t : demande_ini - self.cinetique_evolution(t, x), x[2], T_life)[0]

    def budget_carbone(self, x):
        return integrate.quad(lambda t : demande_ini, 0, x[2])[0] + integrate.quad(lambda t : self.cinetique_evolution(t, x), x[2], t_f)[0]

    def surcout_trajectoire(self, x):
        a1 = demande_ini * x[2] * (x[0] - c1i) / 2  # taxe sur x1 de 0 à t1'''
        a2 = (x[0] - c1i) * integrate.quad(lambda t : self.cinetique_evolution(t, x), x[2], t_f)[0] # taxe sur x1 de t1 à tf
        a3 = (x[0] - c2i) * integrate.quad(lambda t : demande_ini - self.cinetique_evolution(t, x), x[2], t_f)[0]  # taxe sur x2 de 0 à tf
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
                techno_1.append(demande_ini)
                techno_2.append(0)
            else :
                techno_1.append(self.cinetique_evolution(t, x))
                techno_2.append(demande_ini - self.cinetique_evolution(t, x))

        taxe_1, taxe_2 = [], []
        for t in temps:
            taxe_1.append(self.cinetique_cout(t, x, c1i) - c1i)
            taxe_2.append(self.cinetique_cout(t, x, c2i) - c2i)

        return temps, [cout_1, cout_2], [techno_1, techno_2], [r'carbon\'ee', r'd\'ecarbon\'ee'], [demande_ini for i in np.arange(0, T_life + 0.5, 0.5)], [taxe_1, taxe_2]