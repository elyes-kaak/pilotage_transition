from N_techno.Cinetique import *
from scipy.integrate import trapz

class calcul_trajectoire :
    def __init__(self, x):
        self.test = 0
        self.x = x
        self.cinetique = Cinetique()
