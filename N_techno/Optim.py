from scipy.optimize import minimize
import math

class Optim:
    def __init__(self, objectif, contraintes, val_init, budget_carb, surcout):
        self.objectif = objectif
        self.contraintes = contraintes
        self.val_init = val_init
        self.budget_carb = budget_carb
        self.surcout = surcout

    def sol_optim(self):
        return minimize(self.objectif, self.val_init, method='COBYLA', constraints=self.contraintes, options={'maxiter': 10000})

    def return_sol_optim(self):

        res = 'Initial Objective: ' + str(self.objectif(self.val_init)) + '\n'

        solution = self.sol_optim()

        x = solution.x

        res = res + 'Success: ' + str(solution.success) + '\n'
        res = res + 'Message: ' + str(solution.message) + '\n'

        res = res + 'Final Objective: ' + str(self.objectif(x)) + '\n'
        return x, res
