from N_techno.Annexes import *
from N_techno.Cinetique import *

# test = Methodes()

# test.methode_budget()
# test.methode_emissions()
# test.methode_surcout()

# evol_x1_c_cst()
# evol_x1_k_cst()

test = Cinetique()

temps, [techno_dec, techno_car] = test.tableau_evol(x0)

print([(temps[i], techno_car[0][i], techno_dec[0][i]) for i in range(len(temps))])
print(test.t_prime)