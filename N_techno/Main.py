import matplotlib.pyplot as plt
from matplotlib import rc
from N_techno.Annexes import *
from N_techno.Cinetique import *

rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
# test = Methodes()

# test.methode_budget()
# test.methode_emissions()
# test.methode_surcout()

# evol_x1_c_cst()
# evol_x1_k_cst()

test = Cinetique()

temps, [techno_dec, techno_car] = test.tableau_evol(x0)


for i in range(m) :
    plt.plot(temps, techno_dec[i], label = r'Activit\'e de la technologie d\'ecarbon\'ee ' + str(i))

for i in range(n-m) :
    plt.plot(temps, techno_car[i], label = r'Activit\'e de la technologie carbon\'ee ' + str(i))

plt.plot(temps, [test.cinetique_demande(t) for t in temps], label = r'Demande \'energ\'etique')

S = [0 for t in temps]
for i in range(m) :
    for j in range(len(temps)) :
        S[j] += techno_dec[i][j]

for i in range(n-m) :
    for j in range(len(temps)) :
        S[j] += techno_car[i][j]

for j in range(len(temps)) :
    if (abs(S[j] - test.cinetique_demande(temps[j])) > 0.1) :
        print(temps[j], S[j] - test.cinetique_demande(temps[j]))
plt.legend()
plt.show()