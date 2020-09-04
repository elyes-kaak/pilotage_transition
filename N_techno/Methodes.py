from N_techno.Calcul_trajectoire import *
from N_techno.Contraintes import *
from N_techno.Optim import *
from N_techno.Plot import *

class Methodes :

    def methode_surcout(self, ci) :

        # Définition des contraintes : temps et budget
        contraintes = Contraintes()

        contraintes.new_contr_max(lambda x : Calcul_trajectoire(x, ci).budget_carbone(), max_budget_carbone)

        contraintes.new_contr_max(lambda x: x[0] - x[1], 0)
        contraintes.new_contr_max(lambda x: x[1] - x[2], 0)

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

        x = x_to_bnds(x)
        print_x(x)
        x = x_to_r(x)
        return budget, surcout, x

    def methode_emissions(self, ci) :

        # Définition des contraintes : temps, budget et surcoût
        contraintes = Contraintes()

        contraintes.new_contr_max(lambda x : Calcul_trajectoire(x, ci).surcout_trajectoire(), max_surcout)
        contraintes.new_contr_min(lambda x : Calcul_trajectoire(x, ci).surcout_trajectoire(), -max_surcout)

        contraintes.new_contr_max(lambda x: x[0] - x[1], 0)
        contraintes.new_contr_max(lambda x: x[1] - x[2], 0)


        # Résolution du problème d'optimisation (fonction objectif correspondant à la minimisation de la valeur finale de x_1
        optimisation = Optim(lambda x : Calcul_trajectoire(x, ci).budget_carbone(), contraintes.contr, x0,
                            lambda x : Calcul_trajectoire(x, ci).budget_carbone(), lambda x : Calcul_trajectoire(x, ci).surcout_trajectoire())


        x = optimisation.return_sol_optim()

        budget = Calcul_trajectoire(x, ci).budget_carbone()
        surcout = Calcul_trajectoire(x, ci).surcout_trajectoire()

        print('Emissions de la solution = ' + str(int(budget)))
        print('Surcout : ', str(int(surcout)))

        x = x_to_bnds(x)
        print_x(x)
        x = x_to_r(x)

        return budget, surcout, x