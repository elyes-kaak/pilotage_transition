#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.image as mpimg
from Methodes import *
import time
import multiprocessing as mp
from tqdm import tqdm, trange

nom = 'results-Diff-France-multiple-x0'
fn = "Results/" + nom + ".txt"

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
    res = ''
    start_time = time.time()
    # Valeurs initiales
    optim = Methodes(arg)
    budg, surc, x, out = optim.methode_surcout()
    end_time = time.time()
    res = res + "x0 = " + ','.join(map(str, arg)) + '\n'
    res = res + "x = " + ','.join(map(str, x)) + '\n'
    res = res + out
    res = res + "Temps d'exécution : " + str(round(end_time - start_time, 2)) + '\n'
    res = res + print_x(x)

    bud_surcout_xsol.append((surc, budg, x))
    q.put(res)
    return res

def main() :
    start_time = time.time()

    budget_ref = Calcul_trajectoire(x_ref).budget_carbone_ref()
    surcout_ref = Calcul_trajectoire(x_ref).surcout_trajectoire_ref()
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
    for i in range(50) :
        x0 = np.array([])
        t_i = np.random.uniform(min(min(b1)), max(max(b1)), m)
        c_i = np.random.uniform(min(min(b2)), max(max(b2)), m)
        k_j = np.random.uniform(min(min(b3)), max(max(b3)), n - m)
        x0 = np.append(x0, t_i)  # valeur initiale de t_i
        x0 = np.append(x0, c_i)  # valeur initiale de c_i
        x0 = np.append(x0, k_j)  # valeur initiale de k_j

        job = pool.apply_async(worker, (x0.copy(), q, bud_surc_xsol))
        jobs.append(job)


    for job in tqdm(jobs):
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

    trajectoire_sol = Calcul_trajectoire(x)

    budget = trajectoire_sol.budget_carbone()
    surcout = trajectoire_sol.surcout_trajectoire()
    ordre_dec = trajectoire_sol.ordre_dec

    res = 'La solution du problème a un budget de ' + str(budget) + ' et un surcoût de ' + str(surcout) + '\n'
    res = res + "Elle est atteinte pour l'ordre suivant des technos décarbonées : " + str(ordre_dec) + '\n'
    res = res + "x = " + ','.join(map(str, x)) + '\n'
    res = res + print_x(x)

    with open(fn, 'a') as f:
        f.write(res)
        f.flush()

    plot = Plot(x, nom)
    plot.plot()
    plt.clf()
    plt.axis('off')
    img = mpimg.imread('Figures/' + nom + '.png')
    plt.imshow(img)
    plt.show()

if __name__ == '__main__':
    main()