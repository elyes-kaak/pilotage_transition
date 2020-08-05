from Deux_techno.Cinetique import *
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

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


def evol_x_multi_techno() :
    p = [0.7, 0.3]
    T_life = [50, 60]
    t_tr = [3, 30]
    X_ren = [700, 300]
    k = [200, 150]
    c = [70, 50]
    E = 500
    x_f = [0, 0]
    x1f1 = p[0] * E
    x2f1 = p[1] * E

    x_1 = []
    x_2 = []

    x_dec_1 = []
    x_dec_2 = []
    def x1(t) :
        if(t < T_life[0]):
            return (x1f1 - x_f[0]) * ((T_life[0] - t) / (T_life[0] - t_tr[0]))**(k[0]/c[0]) + x_f[0]
        return x_f[0]

    def x2(t) :
        if(t < T_life[1]):
            return (x2f1 - x_f[1]) * ((T_life[1] - t) / (T_life[1] - t_tr[0]))**(k[1] / c[0]) + x_f[1]
        return x_f[1]

    xdec = lambda t: E - x1(t) - x2(t) - X_ren[0]

    t_initial_guess = np.array([5])
    t_solution, info_dict, ier, mesg = fsolve(xdec, t_initial_guess,full_output=True)
    if (ier != 1):
        t_solution = fsolve(lambda t: x1(t) + x2(t) - x_f[0] - x_f[1], t_initial_guess)

    x1f = x1(min(t_solution, t_tr[1]))
    x2f = x2(min(t_solution, t_tr[1]))
    def x12(t) :
        if(t < T_life[0]):
            return ((x1f - x_f[0]) * ((T_life[0] - t) / (T_life[0] - t_tr[1])) ** (k[0] / c[1])) + x_f[0]
        return x_f[0]

    def x22(t) :
        if(t < T_life[1]):
            return ((x2f - x_f[1]) * ((T_life[1] - t) / (T_life[1] - t_tr[1])) ** (k[1] / c[1])) + x_f[1]
        return x_f[1]

    xdec2 = lambda t: E - x12(t) - x22(t) - X_ren[0] - X_ren[1]

    t_solution_2, info_dict, ier, mesg = fsolve(xdec2, t_initial_guess, full_output=True)
    if (ier != 1):
        t_solution_2 = fsolve(lambda t: x12(t) + x22(t) - x_f[0] - x_f[1], t_initial_guess)

    temps = [t for t in np.arange(0, 60.2, 0.2)]
    i = 0
    for t in temps :
        if(t < t_tr[0]) :
            x_1.append(p[0] * E)
            x_2.append(p[1] * E)
            x_dec_1.append(0)
            x_dec_2.append(0)

        if(t>= t_tr[0] and t<=t_tr[1]) :

            if(t <= t_solution[0]) :
                xd1 = E - x1(t) - x2(t)
                x_1.append(x1(t))
                x_2.append(x2(t))
                x_dec_1.append(xd1)
                x_dec_2.append(0)
            else :
                #xd1 = x_dec_1[-1]
                xd1 = E - x1(t_solution[0]) - x2(t_solution[0])
                x_1.append(x1(t_solution[0]))
                x_2.append(x2(t_solution[0]))
                x_dec_1.append(xd1)
                x_dec_2.append(0)

        if (t > t_tr[1]):
            xd1 = x_dec_1[-1]
            xd2 = E - x12(t) - x22(t) - xd1
            if(t <= t_solution_2[0]) :
                x_1.append(x12(t))
                x_2.append(x22(t))
                x_dec_1.append(xd1)
                x_dec_2.append(xd2)
            else :
                x_1.append(x_1[-1])
                x_2.append(x_2[-1])
                x_dec_1.append(xd1)
                x_dec_2.append(x_dec_2[-1])

    plt.plot(temps, x_1, label=r'$x_3^{car}$')
    plt.plot(temps, x_2, label=r'$x_4^{car}$')
    plt.plot(temps, x_dec_1, label=r'$x^{decar}_1$')
    plt.plot(temps, x_dec_2, label=r'$x^{decar}_2$')

    plt.plot(temps, [E for t in temps], label=r'Demande \'energ\'etique')

    plt.axvline(x = t_tr[0], linestyle = 'dashed', linewidth = 0.5, color='k')
    plt.text(s=r'$t_1$', x=t_tr[0] + 0.5, y=E+20)

    plt.axvline(x=t_tr[1], linestyle='dashed', linewidth=0.5, color='k')
    plt.text(s=r'$t_2$', x=t_tr[1] + 0.5, y=E + 20)

    plt.axvline(x=t_solution, linestyle='dashed', linewidth=0.5, color='k')
    plt.text(s=r'$t_1^\prime$', x=t_solution - 0.8, y=E + 20)

    plt.axvline(x=t_solution_2, linestyle='dashed', linewidth=0.5, color='k')
    plt.text(s=r'$t_2^\prime$', x=t_solution_2 + 0.5, y=E + 20)

    plt.hlines(x_f[0], 0, 60, linestyles='dashed', linewidth = 0.5)
    plt.text(s=r'$X_3^f$', x = -1.5, y=x_f[0]-22)

    plt.hlines(x_f[1], 0, 60, linestyles='dashed', linewidth=0.5)
    plt.text(s=r'$X_4^f$', x=-1.5, y=x_f[1] + 8)

    plt.hlines(X_ren[0], 0, 60, linestyles='dashed', linewidth=0.5)
    plt.text(s=r'$X_1$', x=-1.5, y=X_ren[0] - 8)

    plt.hlines(X_ren[1], 0, 60, linestyles='dashed', linewidth=0.5)
    plt.text(s=r'$X_2$', x=-1.5, y=X_ren[1] - 8)

    plt.xlabel(r'Temps')
    plt.ylabel(r'$x(t)$')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol = 5)
    plt.title(r'\'Evolution des activit\'es des technologies carbon\'ees et d\'ecarbon\'ees')
    plt.show()