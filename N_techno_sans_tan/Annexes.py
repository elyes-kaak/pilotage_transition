import matplotlib.pyplot as plt
from matplotlib import rc
from N_techno_sans_tan.Calcul_trajectoire import *

rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})

test = Calcul_trajectoire(x0)

temps, [techno_dec, techno_car], [taxes_decar, taxes_carb], [c_nat_decar, c_nat_carb], demande = test.tableau_evol()

for i in range(m) :
    plt.plot(temps, techno_dec[i], label = r'Activit\'e de la technologie d\'ecarbon\'ee ' + str(i))

for i in range(n-m) :
    plt.plot(temps, techno_car[i], label = r'Activit\'e de la technologie carbon\'ee ' + str(i))

plt.plot(temps, demande, label = r'Demande \'energ\'etique')

S = [0 for t in temps]
for i in range(m) :
    for j in range(len(temps)) :
        S[j] += techno_dec[i][j]

for i in range(n-m) :
    for j in range(len(temps)) :
        S[j] += techno_car[i][j]

for j in range(len(temps)) :
   if (np.abs(S[j] - demande[j]) > 1) :
        print(temps[j], S[j] - demande[j])

plt.legend()
plt.show()

print('Surcout ', test.surcout_trajectoire())
print('Budget ', test.budget_carbone())