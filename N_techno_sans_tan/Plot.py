import matplotlib.pyplot as plt
from matplotlib import rc
from N_techno_sans_tan.Calcul_trajectoire import *

rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})

class Plot :

    def __init__(self, t, taxes_decar, taxes_carb, c_nat_decar, c_nat_carb, techno_dec, techno_car, demande, x, ci, ordre_dec, description = 'test'):

        self.fig, (self.ax1, self.ax2) = plt.subplots(nrows = 1, ncols = 2)
        self.t = t
        self.taxes_decar = taxes_decar
        self.taxes_carb = taxes_carb
        self.demande = demande
        self.c_nat_decar = c_nat_decar
        self.c_nat_carb = c_nat_carb
        self.description = description
        self.techno_dec = techno_dec
        self.techno_car = techno_car
        self.x = x
        self.ci = ci
        self.ordre_dec = ordre_dec

    def plot(self):
        self.fig.set_size_inches((12, 5), forward=False)
        self.ax1.plot(self.t, self.demande, 'r-', label = r'Demande \'energ\'etique')

        for i in range(m):
            self.ax1.plot(self.t, self.techno_dec[i], label=r'Activit\'e de la technologie d\'ecarbon\'ee ' + self.ordre_dec[i])

        for i in range(n - m):
            self.ax1.plot(self.t, self.techno_car[i], label=r'Activit\'e de la technologie carbon\'ee ' + type_car[i])

        self.ax1.set_title(r'\'Evolution de la demande et des activit\'es''\n'r'des diff\'erentes technologies')
        self.ax1.set_ylabel(r'Demande ou activit\'e (MTep)')
        self.ax1.set_xlabel(r'Temps')
        self.ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.01), fancybox=True, shadow=True, ncol=2)
        self.ax1.grid(linestyle='--')

        for i in range(m):
            self.ax2.plot(self.t, np.add(self.c_nat_decar[i], self.taxes_decar[i]), label=r'Co\^ut de la technologie d\'ecarbon\'ee ' + self.ordre_dec[i])

        for i in range(n - m):
            self.ax2.plot(self.t, np.add(self.c_nat_carb[i], self.taxes_carb[i]), label=r'Co\^ut de la technologie carbon\'ee ' + type_car[i])

        self.ax2.set_title(r'Evolution des co\^uts')
        self.ax2.set_ylabel(r'Co\^uts (\$/MTep)')
        self.ax2.set_xlabel(r'Temps')
        self.ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.01), fancybox=True, shadow=True, ncol = 2)
        self.ax2.grid(linestyle = '--')

        '''for i in range(m) :
            self.ax3.plot(self.t, self.taxes_decar[i], label = r'Taxe ou subvention sur la technologie d\'ecarbon\'ee ' + self.ordre_dec[i])

        for i in range(n - m) :
            self.ax3.plot(self.t, self.taxes_carb[i], label = r'Taxe ou subvention sur la technologie carbon\'ee ' + type_car[i])
        self.ax3.set_title(r'Evolution des taxes')
        self.ax3.set_ylabel(r'Co\^uts (\$/MTep)')
        self.ax3.set_xlabel(r'Temps')
        self.ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.01), fancybox=True, shadow=True, ncol = 2)
        self.ax3.grid(linestyle = '--')
        self.fig.subplots_adjust(wspace=0.3)'''

        t_i = ''
        k_i = ''
        c_i = ''
        ordre_techno = ''

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
                                + '\n Emissions = ' + str(int(Calcul_trajectoire(self.x, self.ci).budget_carbone()))
                                + ' Surcout = ' + str(int(Calcul_trajectoire(self.x, self.ci).surcout_trajectoire()))
                                + ' max_surcout = ' + str(max_surcout)
                                + ' max_budget = ' + str(max_budget_carbone)
                                + ' Ordre des techno = ' + ordre_techno}

        plt.savefig('Figures/' + self.description + '.png', bbox_inches='tight', dpi=500, metadata=mdata)

