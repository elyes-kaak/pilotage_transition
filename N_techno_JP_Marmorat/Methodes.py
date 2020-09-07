from N_techno_JP_Marmorat.Calcul_trajectoire import *
from N_techno_JP_Marmorat.Contraintes import *
from N_techno_JP_Marmorat.Optim import *
from N_techno_JP_Marmorat.Plot import *
from functools import partial

class Methodes :

    def f_constraint(self, x, index):
        return x[index] - x[index + 1]

    def f_bnds(self, x, index):
        return x[index]

    def methode_surcout(self, ci) :

        # Définition des contraintes : temps et budget
        contraintes = Contraintes()

        contraintes.new_contr_max(lambda x : Calcul_trajectoire(x, ci).budget_carbone(), max_budget_carbone)

        for i in range(m - 1):
            contraintes.new_contr_max(partial(self.f_constraint, index=i), 0)

        for i in range(m):
            contraintes.new_contr_max(partial(self.f_bnds, index=i), max(b1))
            contraintes.new_contr_min(partial(self.f_bnds, index=i), min(b1))

        for i in range(m, 2 * m):
            contraintes.new_contr_max(partial(self.f_bnds, index=i), max(b2))
            contraintes.new_contr_min(partial(self.f_bnds, index=i), min(b2))

        for i in range(2 * m, n + m):
            contraintes.new_contr_max(partial(self.f_bnds, index=i), max(b3))
            contraintes.new_contr_min(partial(self.f_bnds, index=i), min(b3))

        # Résolution du problème d'optimisation (fonction objectif correspondant à la minimisation du surcoût sur la trajectoire
        optimisation = Optim(lambda x : Calcul_trajectoire(x, ci).surcout_trajectoire(), contraintes.contr, x0,
                             lambda x : Calcul_trajectoire(x, ci).budget_carbone(), lambda x : Calcul_trajectoire(x, ci).surcout_trajectoire())

        x = optimisation.return_sol_optim()

        budget = Calcul_trajectoire(x, ci).budget_carbone()
        surcout = Calcul_trajectoire(x, ci).surcout_trajectoire()
        print()
        print('Emissions de la solution = ' + str(int(budget)))
        print('Surcout : ', str(int(surcout)))
        print()

        return budget, surcout, x

    def methode_emissions(self, ci) :

        # Définition des contraintes : temps, budget et surcoût
        contraintes = Contraintes()

        contraintes.new_contr_max(lambda x : Calcul_trajectoire(x, ci).surcout_trajectoire(), max_surcout)

        contraintes.new_contr_min(lambda x : Calcul_trajectoire(x, ci).surcout_trajectoire(), -max_surcout)

        for i in range(m-1) :
            contraintes.new_contr_max(partial(self.f_constraint, index=i), 0)

        for i in range(m) :
            contraintes.new_contr_max(partial(self.f_bnds, index=i), max(b1))
            contraintes.new_contr_min(partial(self.f_bnds, index=i), min(b1))

        for i in range(m, 2*m) :
            contraintes.new_contr_max(partial(self.f_bnds, index=i), max(b2))
            contraintes.new_contr_min(partial(self.f_bnds, index=i), min(b2))

        for i in range(2*m, n + m) :
            contraintes.new_contr_max(partial(self.f_bnds, index=i), max(b3))
            contraintes.new_contr_min(partial(self.f_bnds, index=i), min(b3))

        # Résolution du problème d'optimisation (fonction objectif correspondant à la minimisation de la valeur finale de x_1
        optimisation = Optim(lambda x : Calcul_trajectoire(x, ci).budget_carbone(), contraintes.contr, x0,
                            lambda x : Calcul_trajectoire(x, ci).budget_carbone(), lambda x : Calcul_trajectoire(x, ci).surcout_trajectoire())


        x = optimisation.return_sol_optim()

        budget = Calcul_trajectoire(x, ci).budget_carbone()
        surcout = Calcul_trajectoire(x, ci).surcout_trajectoire()

        print('Emissions de la solution = ' + str(int(budget)))
        print('Surcout : ', str(int(surcout)))

        return budget, surcout, x