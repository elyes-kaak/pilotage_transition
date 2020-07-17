from sympy import *
import numpy as np
from Parametres import *
from Optim import *
from Contraintes import *
from Demande_variable.Cinetique_dem_var import *
from Plot import *

def methode_budget() :
    # Définition des équations de la cinétique de x_1 à la ligne de transition (entre t_1 et t_car)
    cinetique = Cinetique()

    # Définition des contraintes : temps, budget et surcoût
    contraintes = Contraintes()
    contraintes.new_contr_max(cinetique.budget_carbone, max_budget_carbone)
    contraintes.new_contr_max(cinetique.surcout_trajectoire, max_surcout)
    contraintes.new_contr_max(lambda x : cinetique.abs_pente_cout(x, c1i), max_pente_couts)
    contraintes.new_contr_max(lambda x : cinetique.abs_pente_cout(x, c2i), max_pente_couts)

    # Résolution du problème d'optimisation (fonction objectif correspondant à la minimisation de la valeur finale de x_1
    optimisation = Optim(lambda x : cinetique.cinetique_techno(t_f, x), contraintes.contr, bnds, x0, cinetique.budget_carbone, cinetique.surcout_trajectoire)

    x = optimisation.return_sol_optim()
    temps, evol_couts, evol_techno, type_techno, demande, evol_taxes = cinetique.eq_evol(x)
    plot = Plot(temps, evol_couts, evol_techno, type_techno, demande, evol_taxes)
    plot.plot()


def methode_surcout() :
    # Définition des équations de la cinétique à la ligne de transition (entre t_1 et t_car)
    cinetique = Cinetique()

    # Définition des contraintes : temps et budget
    contraintes = Contraintes()
    contraintes.new_contr_max(cinetique.budget_carbone, max_budget_carbone)
    contraintes.new_contr_max(lambda x : cinetique.abs_pente_cout(x, c1i), max_pente_couts)
    contraintes.new_contr_max(lambda x : cinetique.abs_pente_cout(x, c2i), max_pente_couts)

    # Résolution du problème d'optimisation (fonction objectif correspondant à la minimisation du surcoût sur la trajectoire
    optimisation = Optim(cinetique.surcout_trajectoire, contraintes.contr, bnds, x0, cinetique.budget_carbone, cinetique.surcout_trajectoire)

    x = optimisation.return_sol_optim()

    temps, evol_couts, evol_techno, type_techno, demande, evol_taxes = cinetique.eq_evol(x)
    plot = Plot(temps, evol_couts, evol_techno, type_techno, demande, evol_taxes)
    plot.plot()


methode_surcout()
