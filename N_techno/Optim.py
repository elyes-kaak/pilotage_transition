from scipy.optimize import minimize
from N_techno.Parametres import *

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

        t_i = ''
        k_i = ''
        c_i = ''
        for i in range(m - 1, -1, -1):
            t_i = t_i + 't_' + str(i) + '= ' + str(int(self.x[i])) + ' '
            c = x[m + i]
            for j in range(i + 1, m):
                if (x[j] == x[i]):
                    c = x[m + i]
            c_i = c_i + 'c_' + str(i) + '= ' + str(int(c)) + ' '

        for i in range(n - m):
            k_i = x[2 * m + i]
        print(c_i)
        print(t_i)
        print(k_i)

        print('Final Objective: ' + str(int(self.objectif(x))))

        print('Emissions de la solution : ', str(int(self.budget_carb(x))))
        print('Surcout : ', str(int(self.surcout(x))))

        # print(solution)
        return x
