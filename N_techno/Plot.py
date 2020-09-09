import matplotlib.pyplot as plt
from matplotlib import rc
from Calcul_trajectoire import *

rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})

class Plot :

    def __init__(self, x, description = 'test'):

        self.fig, (self.ax1, self.ax2) = plt.subplots(nrows = 1, ncols = 2)
        self.trajectoire = Calcul_trajectoire(x)
        self.t = self.trajectoire.temps
        self.taxes_decar = self.trajectoire.taxes_decar
        self.taxes_carb = self.trajectoire.taxes_carb
        self.demande = self.trajectoire.demande
        self.c_nat_decar = self.trajectoire.c_nat_decar
        self.c_nat_carb = self.trajectoire.c_nat_carb
        self.description = description
        self.techno_dec = self.trajectoire.techno_dec
        self.techno_car = self.trajectoire.techno_car
        self.x = x
        self.ordre_dec = self.trajectoire.ordre_dec
        '''for i in range(len(t)):
            self.demande[i] += sum(xj0)
            for j in range(m):
                self.techno_dec[j][i] += xj0[j]'''

    def plot(self):
        self.fig.set_size_inches((12, 5), forward=False)
        self.ax1.plot(self.t, self.demande, 'r-', label = r'Demande \'energ\'etique')


        for i in range(m):
            self.ax1.plot(self.t, self.techno_dec[i], label=r'Activit\'e de la technologie ' + self.ordre_dec[i])

        for i in range(n - m):
            self.ax1.plot(self.t, self.techno_car[i], label=r'Activit\'e de la technologie ' + type_car[i])

        prod = []
        for i in range(len(self.t)) :
            S = 0
            for j in range(m) :
                S += self.techno_dec[j][i]
            for j in range(n-m):
                S += self.techno_car[j][i]
            prod.append(S)

        self.ax1.plot(self.t, prod, label=r'Production totale')

        self.ax1.set_title(r'\'Evolution de la demande et des activit\'es''\n'r'des diff\'erentes technologies')
        self.ax1.set_ylabel(r'Demande ou activit\'e (TWh)')
        self.ax1.set_xlabel(r'Temps')
        self.ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.01), fancybox=True, shadow=True, ncol=2)
        self.ax1.grid(linestyle='--')

        for i in range(m):
            self.ax2.plot(self.t, np.add(self.c_nat_decar[i], self.taxes_decar[i]), label=r'Co\^ut de la technologie ' + self.ordre_dec[i])

        for i in range(n - m):
            self.ax2.plot(self.t, np.add(self.c_nat_carb[i], self.taxes_carb[i]), label=r'Co\^ut de la technologie ' + type_car[i])

        self.ax2.set_title(r'Evolution des co\^uts')
        self.ax2.set_ylabel(r'Co\^uts (\$/MWh)')
        self.ax2.set_xlabel(r'Temps')
        self.ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.01), fancybox=True, shadow=True, ncol = 2)
        self.ax2.grid(linestyle = '--')

        # for i in range(m) :
        #     self.ax3.plot(self.t, self.taxes_decar[i], label = r'Taxe ou subvention sur la technologie ' + self.ordre_dec[i])
        #
        # for i in range(n - m) :
        #     self.ax3.plot(self.t, self.taxes_carb[i], label = r'Taxe ou subvention sur la technologie ' + type_car[i])
        # self.ax3.set_title(r'Evolution des taxes')
        # self.ax3.set_ylabel(r'Co\^uts (\$/MTep)')
        # self.ax3.set_xlabel(r'Temps')
        # self.ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.01), fancybox=True, shadow=True, ncol = 2)
        # self.ax3.grid(linestyle = '--')
        # self.fig.subplots_adjust(wspace=0.3)

        t_i = ''
        k_i = ''
        c_i = ''
        ordre_techno = ''

        instant_tra = np.array(self.x[0: m])
        cout_tra = np.array(self.x[m: 2 * m])
        k_car = self.x[2 * m: n + m]

        perm = sorted(range(len(instant_tra)), key=lambda k: instant_tra[k])

        self.x = np.around(np.concatenate((instant_tra[perm], cout_tra[perm], k_car)), decimals=2)

        for i in range(m) :
            t_i = t_i + 't_' + str(i) + '= ' + str(int(self.x[i])) + ' '
            c = self.x[m + i]
            for j in range(i + 1, m) :
                if(self.x[j] == self.x[i]) :
                    c = self.x[m + i]
            c_i = c_i + 'c_' + str(i) + '= ' + str(int(c)) + ' '

            ordre_techno = ordre_techno + self.ordre_dec[i] + ' '

        for i in range(n-m) :
            k_i = k_i + 'k_' + str(i) + '= ' + str(int(self.x[2*m + i])) + ' '

        mdata = {'Description': t_i + c_i + k_i
                                + '\n Emissions = ' + str(int(self.trajectoire.budget_carbone()))
                                + ' Surcout = ' + str(int(self.trajectoire.surcout_trajectoire()))
                                + ' max_surcout = ' + str(max_surcout)
                                + ' max_budget = ' + str(max_budget_carbone)
                                + ' Ordre des techno = ' + ordre_techno}

        plt.savefig('Figures/' + self.description + '.png', bbox_inches='tight', dpi=500, metadata=mdata)

