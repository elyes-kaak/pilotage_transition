from scipy.optimize import minimize

class Optim:
    def __init__(self, objectif, contraintes, bounds, val_init, budget_carb, surcout):
        self.objectif = objectif
        self.contraintes = contraintes
        self.bounds = bounds
        self.val_init = val_init
        self.budget_carb = budget_carb
        self.surcout = surcout

    def sol_optim(self):
        return minimize(self.objectif, self.val_init, method='SLSQP', bounds=self.bounds, constraints=self.contraintes)

    def return_sol_optim(self):

        print('Initial Objective: ' + str(self.objectif(self.val_init)))
        solution = self.sol_optim()
        x = solution.x
        print('Success: ', solution.success)
        print('Message: ', solution.message)
        print('Solution')
        print('c = ' + str(int(x[0])))
        print('k = ' + str(int(x[1])))
        print('t_1 = ' + str(int(x[2])))

        print('Final Objective: ' + str(int(self.objectif(x))))

        print('Emissions de la solution : ', self.budget_carb(x))
        print('Surcout : ', self.surcout(x))

        # print(solution)
        return x
