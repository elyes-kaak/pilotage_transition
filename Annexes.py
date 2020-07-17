from Cinetique import *
import matplotlib.pyplot as plt

def evol_x1_c_cst() :
    c = 100
    temps = [t for t in np.arange(0, T_life, 0.2)]
    cinetique = Cinetique()

    for k in range(25, 501, 25) :
        tab = []
        for t in temps:
            tab.append(cinetique.cinetique_techno(t, 1000, [c, k, 0]))

        plt.plot(temps, tab, label = r'k = ' + str(k))

    plt.xlabel(r'Temps')
    plt.ylabel(r'$x_1$')
    plt.legend()
    plt.title(r'\'Evolution de $x_1$ suivant diff\'erentes valeurs de $k$ pout $c = 100$')
    plt.show()


def evol_x1_k_cst() :
    k = 200
    temps = [t for t in np.arange(0, T_life, 0.2)]
    cinetique = Cinetique()

    for c in range(25, 501, 25):
        tab = []
        for t in temps:
            tab.append(cinetique.cinetique_techno(t, 1000, [c, k, 0]))

        plt.plot(temps, tab, label=r'c = ' + str(c))

    plt.xlabel(r'Temps')
    plt.ylabel(r'$x_1$')
    plt.legend()
    plt.title(r'\'Evolution de $x_1$ suivant diff\'erentes valeurs de $c$ pout $k = 200$')
    plt.show()
