from itertools import permutations
from Parametres import *
from Methodes import *
import time
import sys

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("Results/test.txt", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

sys.stdout = Logger()

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()


budget_ref = Calcul_trajectoire(x_ref, ci_decar, X_j).budget_carbone_ref()
surcout_ref = Calcul_trajectoire(x_ref, ci_decar, X_j).surcout_trajectoire_ref()

print('Budget de référence : ', budget_ref)
print('Surcout de référence : ', surcout_ref)
print()

sigma = list(permutations(range(m)))

bud_surc = []

x_solution = []

optim = Methodes()

ci_decar_bis = ci_decar.copy()
X_jbis = X_j.copy()

printProgressBar(0, len(sigma), prefix = 'Progress:', suffix = 'Complete', length = 50)

for i in range(len(sigma)) :
    ordre_dec = []
    for k in range(m):
        ci_decar_bis[k] = ci_decar[sigma[i][k]]
        X_jbis[k] = X_j[sigma[i][k]]
        ordre_dec.append(type_dec[sigma[i][k]])

    print("L'ordre des technos décarbonées est le suivant : ", ordre_dec)
    start_time = time.time()
    budg, surc, x, res = optim.methode_surcout(ci_decar_bis, X_jbis)
    end_time = time.time()
    print(res)
    print("Temps d'exécution : ", round(end_time - start_time, 2))
    print(print_x(x))

    bud_surc.append((surc, budg))
    x_solution.append(x)

    printProgressBar(i + 1, len(sigma), prefix='Progress:', suffix='Complete', length=50)

    print()

X_j0bis = X_j_0.copy()

index_min = bud_surc.index(min(bud_surc))
x = x_solution[index_min]

for k in range(m):
    ci_decar_bis[k] = ci_decar[sigma[index_min][k]]
    X_jbis[k] = X_j[sigma[index_min][k]]
    X_j0bis[k] = X_j_0[sigma[index_min][k]]


temps, [techno_dec, techno_car], [taxes_decar, taxes_carb], [c_nat_decar, c_nat_carb], demande = Calcul_trajectoire(x, ci_decar_bis, X_jbis).tableau_evol()

ordre_dec = []
for k in range(m):
    ordre_dec.append(type_dec[sigma[index_min][k]])

print(ordre_dec)
print('La solution du problème a un budget de ', bud_surc[index_min][1], ' et un surcoût de ', bud_surc[index_min][0])
print("Elle est atteinte pour l'ordre suivant des technos décarbonées : ", ordre_dec)
print_x(x)

plot = Plot(temps, taxes_decar, taxes_carb, c_nat_decar, c_nat_carb, techno_dec, techno_car, demande, x, ci_decar_bis, ordre_dec, X_jbis, X_j0bis, 'test')
plot.plot()
plt.show()
