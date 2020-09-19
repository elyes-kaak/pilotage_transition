#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.image as mpimg
from Methodes import *
import time
import sys

nom = 'results-COBYLA-France-multiple-x0-2'

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("Results/" + nom + ".txt", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

#sys.stdout = Logger()

def main():
    trajectoire_ref = Calcul_trajectoire(x_ref)
    budget_ref = trajectoire_ref.budget_carbone_ref()
    surcout_ref = trajectoire_ref.surcout_trajectoire_ref()

    print('Budget de référence : ', budget_ref)
    print('Surcout de référence : ', surcout_ref)
    print()

    for i in range(50) :
        # Valeurs initiales
        x0 = np.array([])
        
        t_i = np.random.uniform(min(min(b1)), max(max(b1)), m)
        c_i = np.random.uniform(min(min(b2)), max(max(b2)), m)
        k_j = np.random.uniform(min(min(b3)), max(max(b3)), n-m)
        x0 = np.append(x0, t_i)  # valeur initiale de t_i
        x0 = np.append(x0, c_i)    # valeur initiale de c_i
        x0 = np.append(x0, k_j)    # valeur initiale de k_j

        optim = Methodes(x0)
        start_time = time.time()
        budget, surcout, x, res = optim.methode_surcout()
        end_time = time.time()

        print(res)
        print("Temps d'exécution : ", round(end_time - start_time, 2))
        print(print_x(x))

        trajectoire_sol = Calcul_trajectoire(x)
        ordre_dec = trajectoire_sol.ordre_dec

        print(ordre_dec)
        print('La solution du problème a un budget de ', budget, ' et un surcoût de ', surcout)
        print("Elle est atteinte pour l'ordre suivant des technos décarbonées : ", ordre_dec)
        print_x(x)


def plot_resultat(x) :
    trajectoire = Calcul_trajectoire(x)

    print("Max dérivée : ", trajectoire.derivee())
    print("Ecart demande : ", trajectoire.ecart_demande())
    print("Surcout : ", trajectoire.surcout_trajectoire())
    print("Budget : ", trajectoire.budget_carbone())
    print(trajectoire.ordre_dec)

    plot = Plot(x, nom)
    plot.plot()
    plt.clf()
    plt.axis('off')
    img = mpimg.imread('Figures/' + nom + '.png')
    plt.imshow(img)

def test():
    fichier = open('Results/' + nom + '.txt', 'r')
    Lines = fichier.readlines()
    surcout = []
    messages = []
    for line in Lines :
        if(line[0:16] == 'Final Objective:') :
            surcout.append(float(line[17:]))
        if(line[0:8] == 'Message:') :
            messages.append(line[9:])

    surcout_bis = []
    i = 0
    for (a, b) in zip(surcout, messages) :
        if(b == 'Optimization terminated successfully.\n'):
            i+=1
            surcout_bis.append(a)
    print(i)
    print(min(surcout_bis), max(surcout_bis), np.average(surcout_bis))


if __name__ == '__main__':
    #main()
    test()
    #plot_resultat([2.0440549764252647,17.399640781622505,17.471669320151832,26.05450024631681,18.513977531514968,23.964985824834454,294.8150427621593,498.85285885363743,63.94052511386734,247.36455447812565,2982.531304046623,229.79900711194455,3230.2954682351374])

