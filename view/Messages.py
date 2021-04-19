import tkinter
from tkinter import Toplevel, filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class Messages(Toplevel):

    def __init__(self, controller, **kw):
        super().__init__(**kw)
        self.controller = controller

        menubar = tkinter.Menu(self)
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save PNG", command=self.save)
        filemenu.add_command(label="Save tikz", command=self.save_tikz)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        self.fig = plt.figure()
        ax = plt.axes(projection='3d')

        self.x = self.controller.stats.messages_x
        self.y = self.controller.stats.messages_y
        self.z = self.controller.stats.messages_z

        self.x_adv = self.controller.stats.messages_adv_x
        self.y_adv = self.controller.stats.messages_adv_y
        self.z_adv = self.controller.stats.messages_adv_z

        # messages = self.controller.replay.messages
        # for messages_a in messages:
        #     for message in messages_a:
        #         for m in message:
        #             if m:
        #                 if m[1] < len(self.controller.world.agents):
        #                     self.x.append(m[0][0])
        #                     self.y.append(m[0][1])
        #                     self.z.append(m[2])
        #                 else:
        #                     self.x_adv.append(m[0][0])
        #                     self.y_adv.append(m[0][1])
        #                     self.z_adv.append(m[2])

        ax.scatter3D(self.x, self.y, self.z)
        ax.scatter3D(self.x_adv, self.y_adv, self.z_adv, marker='^', color="red")

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
        tikz = self.controller.stats.messages_to_tikz()
        with open(file_name, 'w') as handle:
            print(tikz, file=handle)
