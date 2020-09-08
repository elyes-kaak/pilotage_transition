class Contraintes:
    def __init__(self):
        self.contr = []

    def new_contr_max(self, fonction, maxi, type = 'ineq'):
        def fonc_contrainte(x):
            return maxi - fonction(x)

        self.contr.append({'type' : type, 'fun' : fonc_contrainte})

    def new_contr_min(self, fonction, mini, type = 'ineq'):
        def fonc_contrainte(x):
            return fonction(x) - mini

        self.contr.append({'type' : type, 'fun' : fonc_contrainte})


    def check_contr(self, x):
        for elem in self.contr :
            if(elem['fun'](x) < 0):
                return False

        return True

