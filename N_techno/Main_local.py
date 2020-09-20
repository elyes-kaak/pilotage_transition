#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.image as mpimg
from Methodes import *
import time
import sys

nom = 'results-France-Diff-evol-surcout'

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


    optim = Methodes(x0)
    start_time = time.time()
    budget, surcout, x, res = optim.methode_emissions()
    end_time = time.time()

    print(res)
    print("Temps d'exécution : ", round(end_time - start_time, 2))
    print(print_x(x))

    trajectoire_sol = Calcul_trajectoire(x)
    ordre_dec = trajectoire_sol.ordre_dec

    print(ordre_dec)
    print('La solution du problème a un budget de ', budget, ' et un surcoût de ', surcout)
    print("Elle est atteinte pour l'ordre suivant des technos décarbonées : ", ordre_dec)
    print(print_x(x))


def plot_resultat(x) :
    trajectoire = Calcul_trajectoire(x)

    print("Max dérivée : ", trajectoire.derivee())
    print("Ecart demande : ", trajectoire.ecart_demande())
    print("Surcout : ", trajectoire.surcout_trajectoire())
    print("Budget : ", trajectoire.budget_carbone())
    print(trajectoire.ordre_dec)
    print(print_x(x))

    plot = Plot(x, nom)
    plot.plot()
    plt.clf()
    plt.axis('off')
    img = mpimg.imread('Figures/' + nom + '.png')
    plt.imshow(img)
    plt.show()

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
    #test()
    plot_resultat([2.01717240e+00, 8.53585606e+00, 1.67817845e+01, 1.01115031e+00,
     1.59381348e+01, 1.73960776e+02, 1.18786254e+02, 4.46955132e+02,
     3.88572244e+02, 3.20111295e+02, 6.20218827e+01, 7.01697407e+03,
     7.22377380e+03, 6.39986730e+03])