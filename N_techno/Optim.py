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
        return minimize(self.objectif, self.val_init, method='SLSQP', constraints=self.contraintes)

    def return_sol_optim(self):

        print('Initial Objective: ' + str(self.objectif(self.val_init)))

        solution = self.sol_optim()

        x = solution.x

        print('Success: ', solution.success)
        print('Message: ', solution.message)
        print('Solution')
        print('Final Objective: ' + str(self.objectif(x)))
        return x
