from itertools import permutations
from Parametres import *
from Methodes import *
import time
import multiprocessing as mp
import sys

fn = "Results/test2.txt"
sigma = list(permutations(range(m)))
optim = Methodes()

def listener(q):
    '''listens for messages on the q, writes to file. '''

    with open(fn, 'a') as f:
        while 1:
            m = q.get()
            if m == 'kill':
                f.write('killed' + '\n')
                break
            f.write(str(m) + '\n')
            f.flush()

def worker(arg, q, bud_surcout_xsol):
    ordre_dec = []
    ci_decar_worker = ci_decar.copy()
    X_j_worker = X_j.copy()
    res = ''
    for k in range(m):
        ci_decar_worker[k] = ci_decar[sigma[arg][k]]
        X_j_worker[k] = X_j[sigma[arg][k]]
        ordre_dec.append(type_dec[sigma[arg][k]])

    res = res + "L'ordre des technos décarbonées est le suivant : " + str(ordre_dec) + '\n'
    res = res + "sigma[i] = " + str(sigma[arg]) + '\n'
    start_time = time.time()
    budg, surc, x, out = optim.methode_surcout(ci_decar_worker, X_j_worker)
    end_time = time.time()
    res = res + "x = " + ','.join(map(str, x)) + '\n'
    res = res + out
    res = res + "Temps d'exécution : " + str(round(end_time - start_time, 2)) + '\n'
    res = res + print_x(x)

    bud_surcout_xsol.append((surc, budg, x))
    q.put(res)
    return res

def main() :
    start_time = time.time()

    budget_ref = Calcul_trajectoire(x_ref, ci_decar, X_j).budget_carbone_ref()
    surcout_ref = Calcul_trajectoire(x_ref, ci_decar, X_j).surcout_trajectoire_ref()
    with open(fn, 'w') as f:
        f.write('Budget de référence : ' + str(budget_ref) + '\n')
        f.write('Surcout de référence : '+ str(surcout_ref) + '\n')
        f.flush()

    manager = mp.Manager()
    q = manager.Queue()

    bud_surc_xsol = manager.list()

    pool = mp.Pool(mp.cpu_count() + 2)

    # put listener to work first
    watcher = pool.apply_async(listener, (q,))

    jobs = []

    #for i in range(len(sigma)) :
    for i in range(5) :
        job = pool.apply_async(worker, (i, q, bud_surc_xsol))
        jobs.append(job)

    for job in jobs:
        job.get()


    bud_surc_xsol = list(bud_surc_xsol)
    q.put('kill')

    pool.close()
    pool.join()

    end_time = time.time()

    print("Temps d'exécution : " + str(round(end_time - start_time, 2)) + '\n')

    bud_surc = [(elem[0], elem[1]) for elem in bud_surc_xsol]

    index_min = bud_surc.index(min(bud_surc))

    x = bud_surc_xsol[index_min][2]

    ci_decar_bis = ci_decar.copy()
    X_jbis = X_j.copy()
    X_j0bis = X_j_0.copy()
    ordre_dec = []

    for k in range(m):
        ci_decar_bis[k] = ci_decar[sigma[index_min][k]]
        X_jbis[k] = X_j[sigma[index_min][k]]
        X_j0bis[k] = X_j_0[sigma[index_min][k]]
        ordre_dec.append(type_dec[sigma[index_min][k]])


    temps, [techno_dec, techno_car], [taxes_decar, taxes_carb], [c_nat_decar, c_nat_carb], demande = Calcul_trajectoire(x, ci_decar_bis, X_jbis).tableau_evol()

    res = 'La solution du problème a un budget de ' + str(bud_surc[index_min][1]) + ' et un surcoût de ' + str(bud_surc[index_min][0]) + '\n'
    res = res + "Elle est atteinte pour l'ordre suivant des technos décarbonées : " + str(ordre_dec) + '\n'
    res = res + "sigma[index_min] = " + str(sigma[index_min]) + '\n'
    res = res + "x = " + ','.join(map(str, x)) + '\n'
    res = res + print_x(x)

    with open(fn, 'a') as f:
        f.write(res)
        f.flush()

    plot = Plot(temps, taxes_decar, taxes_carb, c_nat_decar, c_nat_carb, techno_dec, techno_car, demande, x, ci_decar_bis, ordre_dec, X_jbis, X_j0bis, 'test2')
    plot.plot()
    plt.show()

def plot_resultat(perm, x) :
    ci_decar_bis = ci_decar.copy()
    X_jbis = X_j.copy()
    X_j0bis = X_j_0.copy()
    ordre_dec = []

    for k in range(m):
        ci_decar_bis[k] = ci_decar[perm[k]]
        X_jbis[k] = X_j[perm[k]]
        X_j0bis[k] = X_j_0[perm[k]]
        ordre_dec.append(type_dec[perm[k]])

    temps, [techno_dec, techno_car], [taxes_decar, taxes_carb], [c_nat_decar, c_nat_carb], demande = Calcul_trajectoire(
        x, ci_decar_bis, X_jbis).tableau_evol()

    print("Max dérivée : ", Calcul_trajectoire(x, ci_decar_bis, X_jbis).derivee())
    print("Ecart demande : ", Calcul_trajectoire(x, ci_decar_bis, X_jbis).ecart_demande())

    plot = Plot(temps, taxes_decar, taxes_carb, c_nat_decar, c_nat_carb, techno_dec, techno_car, demande, x,
                ci_decar_bis, ordre_dec, X_jbis, X_j0bis, 'test-bis')
    plot.plot()
    plt.show()

if __name__ == '__main__':
    main()

    #plot_resultat([0, 1, 3, 4, 2], [3.19,3.28,6.17,6.33,6.33,11.48,12.06,9.73,9.24,15.44,99.11,99.23,100.12])