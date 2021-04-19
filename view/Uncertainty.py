import tkinter
from tkinter import Toplevel, filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
import csv


class Uncertainty(Toplevel):

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
        self.estimated_position = {}
        self.average_size = []
        self.average_manhattan = []
        self.std_size = []
        self.std_manhattan = []
        self.x = []

        menubar = tkinter.Menu(self)
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save PNG", command=self.save)
        filemenu.add_command(label="Save tikz", command=self.save_tikz)
        filemenu.add_command(label="Save csv", command=self.save_csv)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)
        self.estimated_position = self.controller.stats.estimated_position

        # for i in range(len(self.controller.world.agents)):
        #     x = []
        #     y = []
        #     for j in range(len(self.estimated_position[i])):
        #         x.append(j)
        #         y.append(len(self.estimated_position[i][j]))
        #     ax.plot(x[10:], y[10:], c=self.gui.agents[i].color)
        for i in range(len(self.estimated_position[0])):
            self.x.append(i)
            values = []
            for j in range(len(self.controller.world.agents)):
                values.append(len(self.estimated_position[j][i]))
            mean = np.mean(values)
            std = np.std(values)
            self.average_size.append(mean)
            self.std_size.append(std)

        for i in range(len(self.estimated_position[0])):
            averages = []
            for j in range(len(self.controller.world.agents)):
                real_position = self.controller.replay.agents_positions[j][i]
                distances = []
                for k in self.estimated_position[j][i]:
                    distances.append(distance.cityblock(real_position, k))
                averages.append(np.average(distances))
            self.average_manhattan.append(np.average(averages))
            self.std_manhattan.append(np.std(averages))


        ax.plot(self.x[10:], self.average_size[10:])
        plt.fill_between(self.x[10:], np.array(self.average_size[10:]) - np.array(self.std_size[10:]),
                         np.array(self.average_size[10:]) + np.array(self.std_size[10:]),
                         color='gray', alpha=0.2)

        plt.xlabel('Steps')
        plt.ylabel('Nb of estimated positions')


        canvas = FigureCanvasTkAgg(self.fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


    def reduce_position_uncertainty(self, id, new_estimation):
        """
        Reduce the uncertainty on the estimated positions
        :param id: id of the agent
        :param new_estimation: new positions estimated
        :return: List of positions
        """
        positions = []
        previous_estimation = self.estimated_position[id][self.index-1]
        for pe in previous_estimation:
            for ne in new_estimation:
                previous_cell = self.controller.world.agents[0].pomdp.maze.cell_at(pe[0], pe[1])
                new_cell = self.controller.world.agents[0].pomdp.maze.cell_at(ne[0], ne[1])
                if previous_cell.wall_between(new_cell) is not None:
                    if not previous_cell.wall_between(new_cell) and ne not in positions:
                        positions.append(ne)
                if previous_cell == new_cell:
                    positions.append(ne)
        return positions

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
        tikz = self.controller.stats.uncertainty_to_tikz()
        with open(file_name, 'w') as handle:
            print(tikz, file=handle)

    def save_csv(self):
        file_name = filedialog.asksaveasfilename(initialdir="./results/", title="Select file",
                                                 filetypes=[("CSV files", "*.csv")])
        with open(file_name, mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            csv_writer.writerow(['Average size', 'Std size', 'Average distance', 'Std distance'])
            csv_writer.writerow([np.average(self.average_size), np.average(self.std_size),
                                 np.average(self.average_manhattan), np.average(self.std_manhattan)])


