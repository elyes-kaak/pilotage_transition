#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Calcul_trajectoire import *
from Contraintes import *
from Optim import *
from Plot import *
from functools import partial

class Methodes :

    def __init__(self, x0):
        self.x0 = x0

    def f_bnds(self, x, index):
        return x[index]

    def f_surcout(self, x):
        return Calcul_trajectoire(x).surcout_trajectoire()

    def f_derivee(self, x):
        return Calcul_trajectoire(x).derivee()

    def f_ecart_demande(self, x):
        return Calcul_trajectoire(x).ecart_demande()

    def f_budget(self, x):
        return Calcul_trajectoire(x).budget_carbone()

    def methode_surcout(self) :
        # Définition des contraintes : temps, budget et surcoût
        contraintes = Contraintes()

        contraintes.new_contr(partial(self.f_budget), -max_budget_carbone, max_budget_carbone, 'non_lin')

        contraintes.new_contr(partial(self.f_derivee), -np.inf, max_derivee, 'non_lin')

        contraintes.new_contr(partial(self.f_ecart_demande), -np.inf, max_ecart_demande, 'non_lin')

        for i in range(m):
            contraintes.new_contr(partial(self.f_bnds, index=i), min(min(b1)), max(max(b1)), 'non_lin')

        for i in range(m, 2 * m):
            contraintes.new_contr(partial(self.f_bnds, index=i), min(min(b2)), max(max(b2)), 'non_lin')

        for i in range(2 * m, n + m):
            contraintes.new_contr(partial(self.f_bnds, index=i), min(min(b3)), max(max(b3)), 'non_lin')

        # Résolution du problème d'optimisation (fonction objectif correspondant à la minimisation du surcoût sur la trajectoire
        optimisation = Optim(partial(self.f_surcout), contraintes.contr, self.x0)

        x, out, success = optimisation.return_sol_optim()

        #budget = Calcul_trajectoire(x, ci, xj).budget_carbone()
        trajectoire_sol = Calcul_trajectoire(x)
        surcout = trajectoire_sol.surcout_trajectoire()
        budget = trajectoire_sol.budget_carbone()
        res = out + 'Emissions de la solution = ' + str(int(budget)) + '\n'
        res = res + 'Surcout : ' + str(int(surcout)) + '\n'

        return budget, surcout, x, res

    def methode_emissions(self) :

        # Définition des contraintes : temps, budget et surcoût
        contraintes = Contraintes()

        contraintes.new_contr(partial(self.f_surcout), -max_surcout, max_surcout, 'non_lin')

        contraintes.new_contr(partial(self.f_derivee), -np.inf, max_derivee, 'non_lin')

        contraintes.new_contr(partial(self.f_ecart_demande), -np.inf, max_ecart_demande, 'non_lin')

        for i in range(m):
            contraintes.new_contr(partial(self.f_bnds, index=i), min(min(b1)), max(max(b1)), 'non_lin')

        for i in range(m, 2 * m):
            contraintes.new_contr(partial(self.f_bnds, index=i), min(min(b2)), max(max(b2)), 'non_lin')

        for i in range(2 * m, n + m):
            contraintes.new_contr(partial(self.f_bnds, index=i), min(min(b3)), max(max(b3)), 'non_lin')


        # Résolution du problème d'optimisation (fonction objectif correspondant à la minimisation de la valeur finale de x_1
        optimisation = Optim(partial(self.f_budget), contraintes.contr, x0)

        x, out, success = optimisation.return_sol_optim()
        trajectoire_sol = Calcul_trajectoire(x)
        surcout = trajectoire_sol.surcout_trajectoire()
        budget = trajectoire_sol.budget_carbone()
        res = out + 'Emissions de la solution = ' + str(int(budget)) + '\n'
        res = res + 'Surcout : ' + str(int(surcout ** 2))

        return budget, surcout, x, res