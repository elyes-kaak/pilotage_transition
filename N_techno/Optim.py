from scipy.optimize import minimize, shgo, NonlinearConstraint, differential_evolution
from Parametres import *
import math
Nfeval = 1

class Optim:

    def __init__(self, objectif, contraintes, val_init, budget_carb, surcout):
        self.objectif = objectif
        self.contraintes = contraintes
        self.val_init = val_init
        self.budget_carb = budget_carb
        self.surcout = surcout

    def callbackF(self, x):
        global Nfeval
        print(Nfeval, x, self.objectif(x))
        Nfeval += 1

    def sol_optim(self):
        #return minimize(self.objectif, self.val_init, method='SLSQP', constraints=self.contraintes,
        #                tol=None, callback=self.callbackF)
        return minimize(self.objectif, self.val_init, method='COBYLA', constraints=self.contraintes,
                        tol=None, options={'rhobeg': .5, 'maxiter': 10000, 'disp': False, 'catol': 0.000001})

    def return_sol_optim(self):

        res = 'Initial Objective: ' + str(self.objectif(self.val_init)) + '\n'

        solution = self.sol_optim()

        x = solution.x

        res = res + 'Success: ' + str(solution.success) + '\n'
        res = res + 'Message: ' + str(solution.message) + '\n'

        res = res + 'Final Objective: ' + str(self.objectif(x)) + '\n'
        return x, res, solution.success
