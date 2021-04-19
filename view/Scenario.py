from tkinter import *
from tkinter import ttk


class Scenario(Toplevel):

    def __init__(self, gui, new=True, **kw):
        super().__init__(**kw)
        self.title = "New scenario"
        self.gui = gui
        self.new = new

        """ Init spinbox for size of the maze """
        Label(self, text="Size of the maze").grid(row=0, column=0, columnspan=4)
        Label(self, text="x").grid(row=1, column=0)
        Label(self, text="y").grid(row=1, column=2)
        if new:
            self.x_spinbox = Spinbox(self, from_=15, to_=100, width=3)
            self.x_spinbox.grid(row=1, column=1)
            self.y_spinbox = Spinbox(self, from_=15, to_=100, width=3)
            self.y_spinbox.grid(row=1, column=3)
        else:
            self.x_spinbox = Spinbox(self, from_=15, to_=100, width=3, state=DISABLED,
                                     textvariable=self.gui.controller.world.maze.nx)
            self.x_spinbox.grid(row=1, column=1)
            self.y_spinbox = Spinbox(self, from_=15, to_=100, width=3, state=DISABLED,
                                     textvariable=self.gui.controller.world.maze.ny)
            self.y_spinbox.grid(row=1, column=3)

        """ Init the number of agents """
        Label(self, text="Select the number of agents").grid(row=2, column=0, columnspan=4)
        self.agent_spinbox = Spinbox(self, from_=2, to_=10, width=3)
        self.agent_spinbox.grid(row=3, column=0, columnspan=2)
        self.agent_spinbox_pos = []
        Button(self, text="Define positions", command=self.generate_agents).grid(row=3, column=2, columnspan=2)

        """ Init the number of adversaries """
        Label(self, text="Select the number of adversaries").grid(row=20, column=0, columnspan=4)
        Label(self, text="Nb").grid(row=21, column=0, columnspan=2)
        self.adv_spinbox = Spinbox(self, from_=0, to_=2, width=3)
        self.adv_spinbox.grid(row=21, column=2, columnspan=2)
        self.adv_spinbox_pos = []

        """ Define goal """
        Label(self, text="Select the positions of the goals").grid(row=30, column=0, columnspan=4)
        self.goal_x_spinbox = Spinbox(self, from_=0, to_=self.x_spinbox.get(), width=3)
        self.goal_x_spinbox.grid(row=31, column=1)
        self.goal_y_spinbox = Spinbox(self, from_=0, to_=self.y_spinbox.get(), width=3)
        self.goal_y_spinbox.grid(row=31, column=3)

        """ Define validation button """
        Button(self, text="Validate", command=self.validate).grid(row=22, column=0, columnspan=4)

    def generate_agents(self):
        self.agent_spinbox_pos = []
        nb_agents = int(self.agent_spinbox.get())
        Label(self, text="Define agents positions").grid(row=2, column=0, columnspan=4)
        for i in range(nb_agents):
            Label(self, text="x").grid(row=4+i, column=0)
            Label(self, text="y").grid(row=4+i, column=2)
            x_spinbox = Spinbox(self, from_=0, to_=self.x_spinbox.get(), width=3)
            x_spinbox.grid(row=4+i, column=1)
            y_spinbox = Spinbox(self, from_=0, to_=self.y_spinbox.get(), width=3)
            y_spinbox.grid(row=4+i, column=3)
            self.agent_spinbox_pos.append([x_spinbox, y_spinbox])

    def validate(self):
        maze_size = [int(self.x_spinbox.get()), int(self.y_spinbox.get())]
        position_goal = [int(self.goal_x_spinbox.get()), int(self.goal_y_spinbox.get())]
        positions_agents = []
        for p in self.agent_spinbox_pos:
            positions_agents.append([int(p[0].get()), int(p[1].get())])
        if self.new:
            self.gui.create_scenario(maze_size, int(self.agent_spinbox.get()), positions_agents, position_goal,
                                     int(self.adv_spinbox.get()))
        else:
            self.gui.new_scenario(int(self.agent_spinbox.get()), positions_agents, position_goal,
                                  int(self.adv_spinbox.get()))
        self.gui.maze = True
        self.destroy()
