from N_techno.Cinetique import *
from scipy.integrate import trapz

class Calcul_trajectoire :
    def __init__(self, x, ci, xj):
        self.x = x
        self.cinetique = Cinetique(ci, xj)

    def tableau_evol(self):
        temps = [i for i in np.arange(0, max_temps, pas_temps)]

        techno_dec = [[] for i in range(m)]
        techno_car = [[] for i in range(n - m)]
        taxes_decar = [[] for i in range(m)]
        taxes_carb = [[] for i in range(n - m)]
        c_nat_decar = [[] for i in range(m)]
        c_nat_carb = [[] for i in range(n - m)]
        demande = []
        for t in temps:

            demande.append(self.cinetique.cinetique_demande(t))
            self.cinetique.mix_instant_t(t, self.x)
            self.cinetique.last_demand = self.cinetique.cinetique_demande(t)
            for j in range(n - m):
                techno_car[j].append(self.cinetique.cinetique_techno_carb(t, self.x, j))
                taxes_carb[j].append(self.cinetique.taxes_car(t, self.x, j))
                c_nat_carb[j].append(self.cinetique.cout_car_nat(t, j))
            for j in range(m):
                techno_dec[j].append(self.cinetique.cinetique_techno_decar(t, self.x, j))
                taxes_decar[j].append(self.cinetique.taxes_dec(t, self.x, j))
                c_nat_decar[j].append(self.cinetique.cout_dec_nat(t, j))

        return temps, [techno_dec, techno_car], [taxes_decar, taxes_carb], [c_nat_decar, c_nat_carb], demande


    def budget_carbone(self):
        temps, [techno_dec, techno_car], [taxes_decar, taxes_carb], [c_nat_decar, c_nat_carb], demande = self.tableau_evol()
        t_f = self.cinetique.t_f
        return sum([trapz(techno_car[j], temps) for j in range(n-m)])

    def budget_carbone_ref(self):
        temps, [techno_dec, techno_car], [taxes_decar, taxes_carb], [c_nat_decar, c_nat_carb], demande = self.tableau_evol()

        return sum([trapz(techno_car[j], temps) for j in range(n-m)])

    def surcout_trajectoire(self):

        temps, [techno_dec, techno_car], [taxes_decar, taxes_carb], [c_nat_decar, c_nat_carb], demande = self.tableau_evol()

        S = 0
        surc_taxe_carb = np.multiply(taxes_carb, taxes_carb)
        surc_taxe_dec = np.multiply(taxes_decar, taxes_decar)
        integrand_chal_lat = np.multiply(c_nat_carb, np.subtract([np.multiply(p_0[j], demande) for j in range(n-m)], techno_car))
        S += sum([trapz(surc_taxe_carb[j], temps) for j in range(n-m)])
        S += sum([trapz(surc_taxe_dec[j], temps) for j in range(m)])
        S += sum([trapz(integrand_chal_lat[j], temps) for j in range(n-m)])
        t_f = self.cinetique.t_f
        return S


    def surcout_trajectoire_ref(self):
        temps, [techno_dec, techno_car], [taxes_decar, taxes_carb], [c_nat_decar, c_nat_carb], demande = self.tableau_evol()
        S = 0
        integrand_chal_lat = np.multiply(c_nat_carb, np.subtract([np.multiply(p_0[j], demande) for j in range(n-m)], techno_car))
        S += sum([trapz(integrand_chal_lat[j], temps) for j in range(n-m)])

        return S

    def val_finale_car(self, j):
        temps, [techno_dec, techno_car], [taxes_decar, taxes_carb], [c_nat_decar,
                                                                     c_nat_carb], demande = self.tableau_evol()

        return techno_car[j][-1]
