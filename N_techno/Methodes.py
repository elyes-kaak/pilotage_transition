from N_techno.Calcul_trajectoire import *
from N_techno.Contraintes import *
from N_techno.Optim import *

from N_techno.Plot import *


class Methodes :

    def methode_surcout(self, description = 'test') :

        # Définition des contraintes : temps et budget
        contraintes = Contraintes()
        contraintes.new_contr_max(lambda x : Calcul_trajectoire(x).budget_carbone(), max_budget_carbone)
        for i in range(m-1) :
            contraintes.new_contr_max(lambda x : x[i] - x[i+1], 0)
            contraintes.new_contr_max(lambda x : x[i], max(T_life))

        # Résolution du problème d'optimisation (fonction objectif correspondant à la minimisation du surcoût sur la trajectoire
        optimisation = Optim(lambda x : Calcul_trajectoire(x).surcout_trajectoire(), contraintes.contr, bnds, x0,
                             lambda x : Calcul_trajectoire(x).budget_carbone(), lambda x : Calcul_trajectoire(x).surcout_trajectoire())

        x = optimisation.return_sol_optim()

        temps, [techno_dec, techno_car], [taxes_decar, taxes_carb], [c_nat_decar, c_nat_carb], demande = Calcul_trajectoire(x).tableau_evol()

        plot = Plot(temps, taxes_decar, taxes_carb, c_nat_decar, c_nat_carb, techno_dec, techno_car, demande, x, description)
        plot.plot()

        print('Emissions de la solution = ' + str(int(Calcul_trajectoire(x).budget_carbone())))
        print('Surcout : ', str(int(Calcul_trajectoire().surcout_trajectoire())))
        plot.plot()

        plt.show()

    def methode_emissions(self, description = 'test', contr_couts = False) :
        # Définition des équations de la cinétique de x_1 à la ligne de transition (entre t_1 et t_car)
        cinetique = Cinetique()

        # Définition des contraintes : temps, budget et surcoût
        contraintes = Contraintes()

        contraintes.new_contr_max(lambda x : Calcul_trajectoire(x).surcout_trajectoire(), max_surcout)
        contraintes.new_contr_min(lambda x : Calcul_trajectoire(x).surcout_trajectoire(), -max_surcout)
        for i in range(m-1) :
            contraintes.new_contr_max(lambda x : x[i] - x[i+1], 0)
            contraintes.new_contr_max(lambda x : x[i], max(T_life))

        # Résolution du problème d'optimisation (fonction objectif correspondant à la minimisation de la valeur finale de x_1
        optimisation = Optim(lambda x : Calcul_trajectoire(x).budget_carbone(), contraintes.contr, bnds, x0,
                             lambda x : Calcul_trajectoire(x).budget_carbone(), lambda x : Calcul_trajectoire(x).surcout_trajectoire())

        x = optimisation.return_sol_optim()

        temps, [techno_dec, techno_car], [taxes_decar, taxes_carb], [c_nat_decar,
                                                                     c_nat_carb], demande = Calcul_trajectoire(
            x).tableau_evol()

        plot = Plot(temps, taxes_decar, taxes_carb, c_nat_decar, c_nat_carb, techno_dec, techno_car, demande, x,
                    description)
        plot.plot()

        print('Emissions de la solution = ' + str(int(Calcul_trajectoire(x).budget_carbone())))
        print('Surcout : ', str(int(Calcul_trajectoire().surcout_trajectoire())))
        plot.plot()

        plt.show()