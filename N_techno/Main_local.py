# -*-coding:Latin-1 -*-

from itertools import permutations
from Parametres import *
from Methodes import *
import time
import sys



class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("Results/test-convergence.txt", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

sys.stdout = Logger()


trajectoire_ref = Calcul_trajectoire(x_ref)
budget_ref = trajectoire_ref.budget_carbone_ref()
surcout_ref = trajectoire_ref.surcout_trajectoire_ref()

print('Budget de référence : ', budget_ref)
print('Surcout de référence : ', surcout_ref)
print()

optim = Methodes()
start_time = time.time()
budg, surc, x, res = optim.methode_surcout()
end_time = time.time()

print(res)
print("Temps d'exécution : ", round(end_time - start_time, 2))
print(print_x(x))

trajectoire_sol = Calcul_trajectoire(x)

budget = trajectoire_sol.budget_carbone()
surcout = trajectoire_sol.surcout_trajectoire()
ordre_dec = trajectoire_sol.ordre_dec

print(ordre_dec)
print('La solution du problème a un budget de ', budget, ' et un surcoût de ', surcout)
print("Elle est atteinte pour l'ordre suivant des technos décarbonées : ", ordre_dec)
print_x(x)

'''plot = Plot(x, 'test')
plot.plot()
plt.show()'''



