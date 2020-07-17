import matplotlib.pyplot as plt
from matplotlib import rc

rc('text', usetex=True)

class Plot :

    def __init__(self, t, couts, techno, type_techno, demande, taxes):

        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(nrows = 1, ncols = 3)
        self.t = t
        self.couts = couts
        self.techno = techno
        self.demande = demande
        self.type_techno = type_techno
        self.taxes = taxes

    def plot(self):
        self.ax1.plot(self.t, self.demande, 'r-', label = r'Demande \'energ\'etique')
        for i in range(len(self.techno)) :
            self.ax1.plot(self.t, self.techno[i], label = r'Activit\'e de la technologie ' + self.type_techno[i])

        self.ax1.set_title(r'Evolution de la demande et des activit\'es des diff\'erentes technologies')
        self.ax1.set_ylabel(r'Demande ou activit\'e (MTep)')
        self.ax1.set_xlabel(r'Temps')
        self.ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=2)
        self.ax1.grid(linestyle='--')

        for i in range(len(self.couts)) :
            self.ax2.plot(self.t, self.couts[i], label = r'Co\^ut de la technologie ' + self.type_techno[i])

        self.ax2.set_title(r'Evolution des co\^uts')
        self.ax2.set_ylabel(r'Co\^uts (\$/MTep)')
        self.ax2.set_xlabel(r'Temps')
        self.ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol = 1)
        self.ax2.grid(linestyle = '--')

        for i in range(len(self.taxes)) :
            self.ax3.plot(self.t, self.taxes[i], label = r'Taxe ou subvention sur la technologie ' + self.type_techno[i])

        self.ax3.set_title(r'Evolution des taxes')
        self.ax3.set_ylabel(r'Co\^uts (\$/MTep)')
        self.ax3.set_xlabel(r'Temps')
        self.ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol = 1)
        self.ax3.grid(linestyle = '--')
        self.fig.subplots_adjust(wspace=0.3)



