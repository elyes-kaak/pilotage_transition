#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Cinetique import *
from scipy.integrate import trapz
from numpy import diff

class Calcul_trajectoire :
    def __init__(self, x):
        self.x = x
        self.cinetique = Cinetique(self.x)
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
            self.cinetique.mix_instant_t(t)
            self.cinetique.last_demand = self.cinetique.cinetique_demande(t)
            for j in range(n - m):
                techno_car[j].append(self.cinetique.cinetique_techno_carb(t, j))
                taxes_carb[j].append(self.cinetique.taxes_car(t, j))
                c_nat_carb[j].append(self.cinetique.cout_car_nat(t, j))
            for j in range(m):
                techno_dec[j].append(self.cinetique.cinetique_techno_decar(t, j))
                taxes_decar[j].append(self.cinetique.taxes_dec(t, j))
                c_nat_decar[j].append(self.cinetique.cout_dec_nat(t, j))

        self.temps = temps 
        self.techno_dec = techno_dec 
        self.techno_car = techno_car
        self.taxes_decar = taxes_decar
        self.taxes_carb = taxes_carb
        self.c_nat_decar = c_nat_decar
        self.c_nat_carb = c_nat_carb
        self.demande = demande
        self.ordre_dec = self.cinetique.ordre_dec

    def budget_carbone(self):
        return sum([trapz(self.techno_car[j], self.temps) for j in range(1, n-m)])

    def budget_carbone_ref(self):
        return sum([trapz(self.techno_car[j], self.temps) for j in range(1, n-m)])

    def surcout_trajectoire(self):
        S = 0
        surc_taxe_carb = np.multiply(self.taxes_carb, self.techno_car)
        surc_taxe_dec = np.multiply(self.taxes_decar, self.techno_dec)
        integrand_chal_lat = np.multiply(self.c_nat_carb, np.subtract([np.multiply(p_0[j], self.demande) for j in range(n-m)], self.techno_car))
        S += sum([trapz(surc_taxe_carb[j], self.temps) for j in range(n-m)])
        S += sum([trapz(surc_taxe_dec[j], self.temps) for j in range(m)])
        S += sum([trapz(integrand_chal_lat[j], self.temps) for j in range(n-m)])
        return abs(S)


    def surcout_trajectoire_ref(self):
        S = 0
        integrand_chal_lat = np.multiply(self.c_nat_carb, np.subtract([np.multiply(p_0[j], self.demande) for j in range(n-m)], self.techno_car))
        S += sum([trapz(integrand_chal_lat[j], self.temps) for j in range(n-m)])

        return S

    def val_finale_car(self, j):
        return self.techno_car[j][-1]

    def ecart_demande(self):
        ecart = []
        for i in range(len(self.temps)):
            S = 0
            for j in range(m):
                S += self.techno_dec[j][i]
            for j in range(n - m):
                S += self.techno_car[j][i]
            ecart.append(abs(self.demande[i] - S))

        return max(ecart)

    def derivee(self):
        maxi = -100000
        for elem in self.techno_car :
            maxi = max(maxi, max(np.abs(diff(elem)/diff(self.temps))))
        for elem in self.techno_dec :
            maxi = max(maxi, max(np.abs(diff(elem) / diff(self.temps))))

        return maxi
