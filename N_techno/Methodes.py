from Calcul_trajectoire import *
from Contraintes import *
from Optim import *
from Plot import *
from functools import partial

class Methodes :

    def f_constraint(self, x, index):
        return x[index] - x[index + 1]

    def f_bnds(self, x, index):
        return x[index]

    def limite_car(self, x, ci, xj, index):
        return Calcul_trajectoire(x, ci, xj).val_finale_car(index)

    def methode_surcout(self, ci, xj) :

        # Définition des contraintes : temps et budget
        contraintes = Contraintes()

        contraintes.new_contr_max(lambda x : Calcul_trajectoire(x, ci, xj).budget_carbone(), max_budget_carbone)
        for j in range(n - m) :
            contraintes.new_contr_max(partial(self.limite_car, index=j, ci = ci, xj = xj), X_jF[j])

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
        optimisation = Optim(lambda x : Calcul_trajectoire(x, ci, xj).surcout_trajectoire(), contraintes.contr, x0,
                             lambda x : Calcul_trajectoire(x, ci, xj).budget_carbone(), lambda x : Calcul_trajectoire(x, ci, xj).surcout_trajectoire())

        x, out = optimisation.return_sol_optim()

        budget = Calcul_trajectoire(x, ci, xj).budget_carbone()
        surcout = Calcul_trajectoire(x, ci, xj).surcout_trajectoire()

        res = out + 'Emissions de la solution = ' + str(int(budget)) + '\n'
        res = res + 'Surcout : ' + str(int(surcout)) + '\n'

        if(contraintes.check_contr(x) == False) :
            budget = 1000000000
            surcout = 1000000000
            res = res + 'Contraintes non respectées \n'

        else :
            res = res + 'Contraintes respectées \n'

        return budget, surcout, x, res

    def methode_emissions(self, ci, xj) :

        # Définition des contraintes : temps, budget et surcoût
        contraintes = Contraintes()

        contraintes.new_contr_max(lambda x : Calcul_trajectoire(x, ci, xj).surcout_trajectoire(), max_surcout)

        contraintes.new_contr_min(lambda x : Calcul_trajectoire(x, ci, xj).surcout_trajectoire(), -max_surcout)

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
        optimisation = Optim(lambda x : Calcul_trajectoire(x, ci, xj).budget_carbone(), contraintes.contr, x0,
                            lambda x : Calcul_trajectoire(x, ci, xj).budget_carbone(), lambda x : Calcul_trajectoire(x, ci, xj).surcout_trajectoire())


        x, out = optimisation.return_sol_optim()
        budget = Calcul_trajectoire(x, ci, xj).budget_carbone()
        surcout = Calcul_trajectoire(x, ci, xj).surcout_trajectoire()

        res = out + 'Emissions de la solution = ' + str(int(budget)) + '\n'
        res = res + 'Surcout : ' + str(int(surcout)) + '\n'

        if (contraintes.check_contr(x) == False):
            budget = 1000000000
            surcout = 1000000000
            res = res + 'Contraintes non respectées \n'

        else:
            res = res + 'Contraintes respectées \n'

        return budget, surcout, x, res