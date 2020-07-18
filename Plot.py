import matplotlib.pyplot as plt
from matplotlib import rc
from Cinetique import *

rc('text', usetex=True)
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})

class Plot :

    def __init__(self, t, couts, techno, type_techno, demande, taxes, x, t_crise, description = 'test'):

        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(nrows = 1, ncols = 3)
        self.t = t
        self.couts = couts
        self.techno = techno
        self.demande = demande
        self.type_techno = type_techno
        self.taxes = taxes
        self.description = description
        self.x = x
        self.t_crise = t_crise

    def plot(self):
        self.fig.set_size_inches((12, 5), forward=False)
        self.ax1.plot(self.t, self.demande, 'r-', label = r'Demande \'energ\'etique')
        for i in range(len(self.techno)) :
            self.ax1.plot(self.t, self.techno[i], label = r'Activit\'e de la technologie ' + self.type_techno[i])

        self.ax1.set_title(r'\'Evolution de la demande et des activit\'es''\n'r'des diff\'erentes technologies')
        self.ax1.set_ylabel(r'Demande ou activit\'e (MTep)')
        self.ax1.set_xlabel(r'Temps')
        self.ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=1)
        self.ax1.grid(linestyle='--')

        for i in range(len(self.couts)) :
            self.ax2.plot(self.t, self.couts[i], label = r'Co\^ut de la technologie ' + self.type_techno[i])

        self.ax2.set_title(r'Evolution des co\^uts')
        self.ax2.set_ylabel(r'Co\^uts (\$/MTep)')
        self.ax2.set_xlabel(r'Temps')
        self.ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol = 1)
        self.ax2.grid(linestyle = '--')

        for i in range(len(self.taxes)) :
            self.ax3.plot(self.t, self.taxes[i], label = r'Taxe ou subvention sur la technologie ' + self.type_techno[i])

        self.ax3.set_title(r'Evolution des taxes')
        self.ax3.set_ylabel(r'Co\^uts (\$/MTep)')
        self.ax3.set_xlabel(r'Temps')
        self.ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol = 1)
        self.ax3.grid(linestyle = '--')
        self.fig.subplots_adjust(wspace=0.3)

        cinetique = Cinetique()
        mdata = {'Description': 'c = ' + str(int(self.x[0])) + ' k = ' + str(int(self.x[1])) + ' t_1 = ' + str(int(self.x[2]))
                                + '\n Emissions = ' + str(int(cinetique.budget_carbone(self.x, self.t_crise)))
                                + ' Surcout = ' + str(int(cinetique.surcout_trajectoire(self.x, self.t_crise)))
                                + '\n t_f = ' + str(t_f) + ' alpha = ' + str(alpha) + ' beta_1 = ' + str(beta_c1) + ' beta_2 = ' + str(beta_c2)
                                + '\n k_max = ' + str(b2[1]) + ' max_surcout = ' + str(max_surcout)
                                + ' max_budget = ' + str(max_budget_carbone) + ' max_pente_couts = ' + str(max_pente_couts)}

        plt.savefig('Figures/' + self.description + '.png', bbox_inches='tight', dpi=500, metadata=mdata)

