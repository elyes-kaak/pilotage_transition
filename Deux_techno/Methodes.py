from Cinetique import *
from Contraintes import *
from Optim import *

from Deux_techno.Plot import *


class Methodes :
    def methode_budget(self, description = 'test', contr_couts = False) :
        # Définition des équations de la cinétique de x_1 à la ligne de transition (entre t_1 et t_car)
        cinetique = Cinetique()

        # Définition des contraintes : temps, budget et surcoût
        contraintes = Contraintes()
        contraintes.new_contr_max(lambda x : cinetique.budget_carbone(x, 1000), max_budget_carbone)
        contraintes.new_contr_max(lambda x : cinetique.surcout_trajectoire(x, 1000), max_surcout)
        contraintes.new_contr_min(lambda x : cinetique.surcout_trajectoire(x, 1000), -max_surcout)
        if(contr_couts) :
            contraintes.new_contr_max(lambda x : cinetique.abs_pente_cout(x, c1i), max_pente_couts)
            contraintes.new_contr_max(lambda x : cinetique.abs_pente_cout(x, c2i), max_pente_couts)

        # Résolution du problème d'optimisation (fonction objectif correspondant à la minimisation de la valeur finale de x_1
        optimisation = Optim(lambda x : cinetique.cinetique_techno(t_f, 1000, x), contraintes.contr, bnds, x0, lambda x : cinetique.budget_carbone(x, 1000), lambda x : cinetique.surcout_trajectoire(x, 1000))

        x = optimisation.return_sol_optim()
        temps, evol_couts, evol_techno, type_techno, demande, evol_taxes = cinetique.eq_evol(x, 1000)
        plot = Plot(temps, evol_couts, evol_techno, type_techno, demande, evol_taxes, x, 1000, description)
        plot.plot()

        temps, evol_couts, evol_techno, type_techno, demande, evol_taxes = cinetique.eq_evol(x, crise)
        plot = Plot(temps, evol_couts, evol_techno, type_techno, demande, evol_taxes, x, crise, description + '_crise')
        print('Emissions de la solution (crise) : ', str(int(cinetique.budget_carbone(x, crise))))
        print('Surcout (crise) : ', str(int(cinetique.surcout_trajectoire(x, crise))))
        plot.plot()

        plt.show()


    def methode_surcout(self, description = 'test', contr_couts = False) :
        # Définition des équations de la cinétique à la ligne de transition (entre t_1 et t_car)
        cinetique = Cinetique()

        # Définition des contraintes : temps et budget
        contraintes = Contraintes()
        contraintes.new_contr_max(lambda x : cinetique.budget_carbone(x, 1000), max_budget_carbone)
        if (contr_couts):
            contraintes.new_contr_max(lambda x : cinetique.abs_pente_cout(x, c1i), max_pente_couts)
            contraintes.new_contr_max(lambda x : cinetique.abs_pente_cout(x, c2i), max_pente_couts)

        # Résolution du problème d'optimisation (fonction objectif correspondant à la minimisation du surcoût sur la trajectoire
        optimisation = Optim(lambda x : cinetique.surcout_trajectoire(x, 1000), contraintes.contr, bnds, x0,
                             lambda x : cinetique.budget_carbone(x, 1000), lambda x : cinetique.surcout_trajectoire(x, 1000))

        x = optimisation.return_sol_optim()

        temps, evol_couts, evol_techno, type_techno, demande, evol_taxes = cinetique.eq_evol(x, 1000)
        plot = Plot(temps, evol_couts, evol_techno, type_techno, demande, evol_taxes, x, 1000, description)
        plot.plot()

        temps, evol_couts, evol_techno, type_techno, demande, evol_taxes = cinetique.eq_evol(x, crise)
        plot = Plot(temps, evol_couts, evol_techno, type_techno, demande, evol_taxes, x, crise, description + '_crise')
        print('Emissions de la solution (crise) : ', str(int((cinetique.budget_carbone(x, crise)))))
        print('Surcout (crise) : ', str(int((cinetique.surcout_trajectoire(x, crise)))))
        plot.plot()

        plt.show()

    def methode_emissions(self, description = 'test', contr_couts = False) :
        # Définition des équations de la cinétique de x_1 à la ligne de transition (entre t_1 et t_car)
        cinetique = Cinetique()

        # Définition des contraintes : temps, budget et surcoût
        contraintes = Contraintes()
        contraintes.new_contr_max(lambda x : cinetique.surcout_trajectoire(x, 1000), max_surcout)
        contraintes.new_contr_min(lambda x : cinetique.surcout_trajectoire(x, 1000), -max_surcout)
        if (contr_couts):
            contraintes.new_contr_max(lambda x: cinetique.abs_pente_cout(x, c1i), max_pente_couts)
            contraintes.new_contr_max(lambda x: cinetique.abs_pente_cout(x, c2i), max_pente_couts)

        # Résolution du problème d'optimisation (fonction objectif correspondant à la minimisation de la valeur finale de x_1
        optimisation = Optim(lambda x : cinetique.budget_carbone(x, 1000), contraintes.contr, bnds, x0, lambda x : cinetique.budget_carbone(x, 1000), lambda x : cinetique.surcout_trajectoire(x, 1000))

        x = optimisation.return_sol_optim()
        temps, evol_couts, evol_techno, type_techno, demande, evol_taxes = cinetique.eq_evol(x, 1000)
        plot = Plot(temps, evol_couts, evol_techno, type_techno, demande, evol_taxes, x, 1000, description)
        plot.plot()

        temps, evol_couts, evol_techno, type_techno, demande, evol_taxes = cinetique.eq_evol(x, crise)
        plot = Plot(temps, evol_couts, evol_techno, type_techno, demande, evol_taxes, x, crise, description + '_crise')
        print('Emissions de la solution (crise) : ', str(int(cinetique.budget_carbone(x, crise))))
        print('Surcout (crise) : ', str(int(cinetique.surcout_trajectoire(x, crise))))
        plot.plot()

        plt.show()