import tkinter
from tkinter import Toplevel, filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


class AcceptationRate(Toplevel):

    """ Class managing the representation of the acceptation rate in a graph. """

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
        width = 0.25
        self.accepted = []
        self.rejected = []
        self.accepted_rate = []
        self.rejected_rate = []
        self.labels = []

        menubar = tkinter.Menu(self)
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save PNG", command=self.save)
        filemenu.add_command(label="Save tikz", command=self.save_tikz)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        for i in range(len(self.controller.world.agents)):
            self.accepted.append(0)
            self.rejected.append(0)
            self.accepted_rate.append(0)
            self.rejected_rate.append(0)
            self.labels.append("Ag. " + str(i))
        for i in range(len(self.controller.world.adversaries)):
            self.accepted.append(0)
            self.rejected.append(0)
            self.accepted_rate.append(0)
            self.rejected_rate.append(0)
            self.labels.append("Adv. " + str(i))
        x = np.arange(len(self.labels))

        # Getting all the messages exchanged.
        messages = self.controller.replay.messages

        # While each steps of the simulation has not been processed.
        # self.index = 0
        # while self.index < self.controller.replay.index_max:
        #     # Processing the messages sent by each agent at this step
        #     for i in range(len(self.controller.world.agents)):
        #         verifier = self.controller.world.agents[i]
        #         for j in range(len(messages[i][self.index])):
        #             if messages[i][self.index][j]:
        #                 id = messages[i][self.index][j][1]
        #                 goal = messages[i][self.index][j][0]
        #                 value = messages[i][self.index][j][2]
        #                 position_possible = verifier.zkmaze.get_position_possible(value, goal)
        #                 if id < len(self.accepted):
        #                     if position_possible:
        #                         self.accepted[id] += 1
        #                     else:
        #                         self.rejected[id] += 1
        #                 else:
        #                     if position_possible:
        #                         self.accepted[id-100+len(self.controller.world.agents)] += 1
        #                     else:
        #                         self.rejected[id-100+len(self.controller.world.agents)] += 1
        #     self.index += 1

        self.accepted = self.controller.stats.accepted
        self.rejected = self.controller.stats.rejected

        for i in range(len(self.accepted)):
            if self.accepted[i] > 0:
                self.accepted_rate[i] = self.accepted[i]/(self.accepted[i]+self.rejected[i])
            if self.rejected[i] > 0:
                self.rejected_rate[i] = self.rejected[i]/(self.accepted[i]+self.rejected[i])
        print(self.accepted, self.rejected)
        print(self.accepted_rate, self.rejected_rate)
        rects1 = ax.bar(x - width / 2, self.accepted_rate, width, label='Accepted')
        rects2 = ax.bar(x + width / 2, self.rejected_rate, width, label='rejected')
        ax.set_ylabel('%')
        ax.set_title('Accepting rates by agents')
        ax.set_xticks(x)
        ax.set_xticklabels(self.labels)
        ax.legend()

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