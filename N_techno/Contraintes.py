from scipy.optimize import NonlinearConstraint, LinearConstraint

class Contraintes:
    def __init__(self):
        self.contr = ()

    def new_contr(self, fonction, mini, maxi, type):
        if(type == "non_lin"):
            nlc = NonlinearConstraint(fonction, mini, maxi)
        else :
            nlc = LinearConstraint(fonction, mini, maxi)

        self.contr = self.contr + (nlc,)

