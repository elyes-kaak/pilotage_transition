from Calcul_trajectoire import *
from Contraintes import *
from Optim import *
from Plot import *
from functools import partial

class Methodes :

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

        contraintes.new_contr(partial(self.f_budget), -max_surcout, max_surcout, 'non_lin')

        contraintes.new_contr(partial(self.f_derivee), -np.inf, max_derivee, 'non_lin')

        contraintes.new_contr(partial(self.f_ecart_demande), -np.inf, max_ecart_demande, 'non_lin')

        # Résolution du problème d'optimisation (fonction objectif correspondant à la minimisation du surcoût sur la trajectoire
        optimisation = Optim(partial(self.f_surcout), contraintes.contr)

        x, out, success = optimisation.return_sol_optim()

        #budget = Calcul_trajectoire(x, ci, xj).budget_carbone()
        trajectoire_sol = Calcul_trajectoire(x)
        surcout = trajectoire_sol.surcout_trajectoire()
        budget = trajectoire_sol.budget_carbone()
        res = out + 'Emissions de la solution = ' + str(int(budget)) + '\n'
        res = res + 'Surcout : ' + str(int(surcout)) + '\n'

        return budget, surcout, x, res

    def methode_emissions(self, ci, xj) :

        # Définition des contraintes : temps, budget et surcoût
        contraintes = Contraintes()

        contraintes.new_contr(lambda x : Calcul_trajectoire(x, ci, xj).surcout_trajectoire(), -max_surcout, max_surcout, 'non_lin')

        contraintes.new_contr(lambda x: Calcul_trajectoire(x, ci, xj).derivee(), -np.inf, max_derivee, 'non_lin')

        contraintes.new_contr(lambda x: Calcul_trajectoire(x, ci, xj).ecart_demande(), -np.inf, max_ecart_demande, 'non_lin')

        for i in range(m - 1):
            contraintes.new_contr(partial(self.f_constraint, index=i), -np.inf, 0, 'lin')


        # Résolution du problème d'optimisation (fonction objectif correspondant à la minimisation de la valeur finale de x_1
        optimisation = Optim(lambda x : Calcul_trajectoire(x, ci, xj).budget_carbone(), contraintes.contr, x0)

        x, out, success = optimisation.return_sol_optim()
        budget = Calcul_trajectoire(x, ci, xj).budget_carbone()
        surcout = Calcul_trajectoire(x, ci, xj).surcout_trajectoire()

        res = out + 'Emissions de la solution = ' + str(int(budget)) + '\n'
        res = res + 'Surcout : ' + str(int(surcout)) + '\n'

        if (success == False):
            budget = 1000000000
            surcout = 1000000000

        return budget, surcout, x, res