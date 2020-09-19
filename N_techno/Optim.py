from scipy.optimize import minimize, shgo, NonlinearConstraint, differential_evolution
from Parametres import *
import math

Nfeval = 1

class Optim:

    def __init__(self, objectif, contraintes, bounds, x0):
        self.objectif = objectif
        self.contraintes = contraintes
        self.x0 = x0
        self.bnds = bounds


    def callbackF(self, x, convergence = 0):
        global Nfeval
        print(Nfeval, self.objectif(x))
        Nfeval += 1
        return False

    def sol_optim(self):
        return differential_evolution(self.objectif, bnds, maxiter=1000, popsize=30, tol = 0.01, constraints=self.contraintes,
                                              workers = -1, updating = 'deferred', callback=self.callbackF, strategy = 'best1bin',
                                              mutation=0.5, recombination=0.7)
        #return minimize(self.objectif, self.x0, method='COBYLA', constraints=self.contraintes)#, options={'rhobeg': .5, 'maxiter': 10000, 'disp': False, 'catol': 0.000001})



    def return_sol_optim(self):

        solution = self.sol_optim()

        x = solution.x

        res = 'Success: ' + str(solution.success) + '\n'
        res = res + 'Message: ' + str(solution.message) + '\n'

        res = res + 'Final Objective: ' + str(self.objectif(x)) + '\n'
        return x, res, solution.success
