from itertools import permutations
from N_techno.Parametres import *
from N_techno.Methodes import *
import time
import multiprocessing as mp
import sys

fn = "Results/test.txt"
sigma = list(permutations(range(m)))
optim = Methodes()
ci_decar_bis = ci_decar.copy()
X_jbis = X_j.copy()

def listener(q):
    '''listens for messages on the q, writes to file. '''

    with open(fn, 'w') as f:
        while 1:
            m = q.get()
            if m == 'kill':
                f.write('killed' + '\n')
                break
            f.write(str(m) + '\n')
            f.flush()

def worker(arg, q, bud_surcout, x_solution):
    ordre_dec = []
    ci_decar_worker = ci_decar.copy()
    X_j_worker = X_j.copy()
    res = ''
    for k in range(m):
        ci_decar_worker[k] = ci_decar[sigma[arg][k]]
        X_j_worker[k] = X_j[sigma[arg][k]]
        ordre_dec.append(type_dec[sigma[arg][k]])

    res = res + "L'ordre des technos décarbonées est le suivant : " + str(ordre_dec) + '\n'
    start_time = time.time()
    budg, surc, x, out = optim.methode_surcout(ci_decar_worker, X_j_worker)
    end_time = time.time()
    res = res + out
    res = res + "Temps d'exécution : " + str(round(end_time - start_time, 2)) + '\n'
    res = res + print_x(x)

    bud_surcout.append((surc, budg))
    x_solution.append(x)
    q.put(res)
    return res

def main() :
    budget_ref = Calcul_trajectoire(x_ref, ci_decar, X_j).budget_carbone_ref()
    surcout_ref = Calcul_trajectoire(x_ref, ci_decar, X_j).surcout_trajectoire_ref()
    with open(fn, 'w') as f:
        f.write('Budget de référence : ' + str(budget_ref) + '\n')
        f.write('Surcout de référence : '+ str(surcout_ref) + '\n')
        f.flush()

    manager = mp.Manager()
    q = manager.Queue()

    bud_surc = manager.list()
    x_solution = manager.list()

    pool = mp.Pool(mp.cpu_count() + 2)

    # put listener to work first
    watcher = pool.apply_async(listener, (q,))

    jobs = []

    for i in range(len(sigma)) :
        job = pool.apply_async(worker, (i, q, bud_surc, x_solution))
        jobs.append(job)

    for job in jobs:
        job.get()

    bud_surc = list(bud_surc)
    x_solution = list(x_solution)
    q.put('kill')

    pool.close()
    pool.join()

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

    res = 'La solution du problème a un budget de ' + str(bud_surc[index_min][1]) + ' et un surcoût de ' + str(bud_surc[index_min][0]) + '\n'
    res = res + "Elle est atteinte pour l'ordre suivant des technos décarbonées : " + str(ordre_dec) + '\n'
    res = res + print_x(x)

    with open(fn, 'a') as f:
        f.write(res)
        f.flush()

    plot = Plot(temps, taxes_decar, taxes_carb, c_nat_decar, c_nat_carb, techno_dec, techno_car, demande, x, ci_decar_bis, ordre_dec, X_jbis, X_j0bis, 'test')
    plot.plot()
    plt.show()


if __name__ == '__main__':
    main()