from itertools import permutations
from N_techno.Parametres import *
from N_techno.Methodes import *

budget_ref = Calcul_trajectoire(x_ref, ci_decar).budget_carbone()
surcout_ref = Calcul_trajectoire(x_ref, ci_decar).surcout_trajectoire_ref()

print('Budget de référence : ', budget_ref)
print('Surcout de référence : ', surcout_ref)
print()

sigma = list(permutations(range(m)))

bud_surc = []

x_solution = []

optim = Methodes()

ci_decar_bis = ci_decar.copy()

'''   TEST    '''

i = 0
index_min = 0

for k in range(m):
        ci_decar_bis[k] = ci_decar[sigma[i][k]]

'''budg, surc, x = optim.methode_surcout(ci_decar_bis)
bud_surc.append((budg, surc))
x_solution.append(x)

index_min = bud_surc.index(min(bud_surc))
x = x_solution[index_min]'''

x = x0
for k in range(m):
    ci_decar_bis[k] = ci_decar[sigma[index_min][k]]

temps, [techno_dec, techno_car], [taxes_decar, taxes_carb], [c_nat_decar, c_nat_carb], demande = Calcul_trajectoire(x, ci_decar_bis).tableau_evol()
ordre_dec = []
for k in range(m):
    ordre_dec.append(type_dec[sigma[index_min][k]])

plot = Plot(temps, taxes_decar, taxes_carb, c_nat_decar, c_nat_carb, techno_dec, techno_car, demande, x, ci_decar_bis, ordre_dec)

budget = Calcul_trajectoire(x, ci_decar).budget_carbone()
surcout = Calcul_trajectoire(x, ci_decar).surcout_trajectoire()

print('Budget : ', budget)
print('Surcout : ', surcout)
print()

plot.plot()
plt.show()

''' FIN DU TEST   '''

'''
for i in range(len(sigma)) :
    for k in range(m):
        ci_decar_bis[k] = ci_decar[sigma[i][k]]

    budg, surc, x = optim.methode_surcout(ci_decar_bis)
    bud_surc.append((budg, surc))
    x_solution.append(x)

index_min = bud_surc.index(min(bud_surc))
x = x_solution[index_min]
for k in range(m):
    ci_decar_bis[k] = ci_decar[sigma[index_min][k]]

temps, [techno_dec, techno_car], [taxes_decar, taxes_carb], [c_nat_decar, c_nat_carb], demande = Calcul_trajectoire(x, ci_decar_bis).tableau_evol()
ordre_dec = []
for k in range(m):
    ordre_dec.append(type_dec[sigma[index_min][k]])

plot = Plot(temps, taxes_decar, taxes_carb, c_nat_decar, c_nat_carb, techno_dec, techno_car, demande, x, ci_decar_bis, ordre_dec)

plot.plot()
plt.show()

'''