import tkinter
from tkinter import Toplevel, filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
import csv


class Distances(Toplevel):

    """ Class managing the representation of the uncertainty on the position of the agent in a graph. """

    def __init__(self, gui, controller, **kw):
        """
        Initializing the class and the graph
        :param gui: Class GUI
        :param controller: Class Controller
        """
        super().__init__(**kw)
        self.gui = gui
        self.controller = controller
        self.fig, ax = plt.subplots()
        self.x = []
        self.y = {}

        menubar = tkinter.Menu(self)
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save PNG", command=self.save)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)
        self.distances = self.controller.stats.distances

        for i in range(len(self.distances[0])):
            self.x.append(i)
            for j in range(len(self.controller.world.agents)):
                if j in self.y:
                    self.y[j].append(self.distances[j][i])
                else:
                    self.y[j] = [self.distances[j][i]]
            for adv in self.controller.world.adversaries:
                if adv.id in self.y:
                    self.y[adv.id].append(self.distances[adv.id][i])
                else:
                    self.y[adv.id] = [self.distances[adv.id][i]]

        for i in range(len(self.controller.world.agents)):
            ax.plot(self.x, self.y[i])
        for adv in self.controller.world.adversaries:
            ax.plot(self.x, self.y[adv.id], linestyle='dashed')

        plt.xlabel('Steps')
        plt.ylabel('Distances to the goal')

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



