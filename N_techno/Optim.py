from scipy.optimize import minimize, shgo, NonlinearConstraint, differential_evolution
from Parametres import *
import math

Nfeval = 1

class Optim:

    def __init__(self, objectif, contraintes):
        self.objectif = objectif
        self.contraintes = contraintes


    def callbackF(self, x, convergence = 0):
        global Nfeval
        print(Nfeval, self.objectif(x))
        Nfeval += 1
        return False

    def sol_optim(self):
        #return minimize(self.objectif, x0, method='SLSQP', constraints=self.contraintes, bounds=bnds,
        #                tol=None, callback=self.callbackF)
        #return minimize(self.objectif, x0, method='COBYLA', constraints=self.contraintes,
        #                callback=self.callbackF)#, options={'rhobeg': .5, 'maxiter': 10000, 'disp': False, 'catol': 0.000001})

        return differential_evolution(self.objectif, bnds, maxiter=1000, popsize=10*(n+m), tol = 0.001,
                                      workers = -1, updating = 'deferred', callback=self.callbackF, strategy = 'best1bin',
                                      mutation=0.8, recombination=0.9)#

    def return_sol_optim(self):

        solution = self.sol_optim()

        x = solution.x

        res = 'Success: ' + str(solution.success) + '\n'
        res = res + 'Message: ' + str(solution.message) + '\n'

        res = res + 'Final Objective: ' + str(self.objectif(x)) + '\n'
        return x, res, solution.success
