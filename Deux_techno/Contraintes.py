class Contraintes:
    def __init__(self):
        self.contr = []

    def new_contr_max(self, fonction, maxi, type = 'eq'):
        def fonc_contrainte(x):
            if(maxi < fonction(x)) :
                return -1

            return 0

        self.contr.append({'type' : type, 'fun' : fonc_contrainte})

    def new_contr_min(self, fonction, mini, type = 'eq'):
        def fonc_contrainte(x):
            if(fonction(x) < mini) :
                return -1

            return 0

        self.contr.append({'type' : type, 'fun' : fonc_contrainte})
