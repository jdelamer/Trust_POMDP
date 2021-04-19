import tkinter
from tkinter import Toplevel, filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


class DistancesExperiments(Toplevel):

    """ Class managing the representation of the average distances for a set of experiments. """

    def __init__(self, gui, experiments, **kw):
        """
        Initializing the class and the graph
        :param gui: Class GUI
        :param controller: Class Controller
        """
        super().__init__(**kw)
        self.gui = gui
        self.exp = experiments
        self.fig, ax = plt.subplots()
        width = 0.25
        self.minimum = self.exp.stats.minimum
        self.maximum = self.exp.stats.maximum
        self.average = self.exp.stats.average
        self.std = self.exp.stats.std_average
        self.labels = ["Min.", "Max.", "Avg."]
        self.y = [self.minimum, self.maximum, self.average]
        self.error = [0, 0, self.std]

        menubar = tkinter.Menu(self)
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save PNG", command=self.save)
        filemenu.add_command(label="Save tikz", command=self.save_tikz)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        x = np.arange(len(self.labels))

        ax.set_ylabel('# steps')
        ax.set_title('Number of steps to find the goal.')
        ax.set_xticks(x)
        ax.set_xticklabels(self.labels)

        ax.bar(x, self.y, yerr=self.error, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.yaxis.grid(True)

        canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    def save(self):
        """
        Save the figure
        """
        file_name = filedialog.asksaveasfilename(initialdir="./results/", title="Select file",
                                     filetypes=[("PNG files", "*.png")])
        self.fig.savefig(file_name)

    def save_tikz(self):
        """
        Save the figure as Tikz
        """
        file_name = filedialog.asksaveasfilename(initialdir="./results/", title="Select file",
                                     filetypes=[("Tikz files", "*.tikz")])
        tikz = self.controller.stats.rates_to_tikz()
        with open(file_name, 'w') as handle:
            print(tikz, file=handle)