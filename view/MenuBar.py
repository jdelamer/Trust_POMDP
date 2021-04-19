from tkinter import *
from tkinter import filedialog

from view.AcceptationRate import AcceptationRate
from view.Distances import Distances
from view.DistancesExperiments import DistancesExperiments
from view.Experiments import Experiments
from view.Scenario import Scenario
from view.Messages import Messages
from view.Uncertainty import Uncertainty


class MenuBar:
    """
    Class representing the MenuBar.
    """
    def __init__(self, window, viewer):
        """
        Initializing the menu
        :param window: The window where the menu bar will be
        :param viewer: the class Viewer
        """
        self.window = window
        self.menu = Menu(self.window)
        self.viewer = viewer

        """ Initializing the menu file """
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Generate", command=self.new_maze)
        self.file_menu.add_command(label="New scenario", command=self.new_scenario)
        self.file_menu.add_command(label="Save maze", command=self.save_maze)
        self.file_menu.add_command(label="Load maze", command=self.load_maze)
        self.file_menu.add_command(label="Quit", command=self.quit)

        """ Initializing the replay menu """
        self.replay_menu = Menu(self.menu, tearoff=0)
        self.replay_menu.add_command(label="Save replay", command=self.save_replay)
        self.replay_menu.add_command(label="Load replay", command=self.load_replay)

        """ Initializing the command menu """
        self.command_menu = Menu(self.menu, tearoff=0)
        self.command_menu.add_command(label="Start", command=self.start)
        self.command_menu.add_command(label="Stop", command=self.stop)

        """ Initializing the statistics menu """
        self.statistic_menu = Menu(self.menu, tearoff=0)
        self.statistic_menu.add_command(label="Messages", command=self.messages)
        self.statistic_menu.add_command(label="Uncertainty", command=self.uncertainty)
        self.statistic_menu.add_command(label="Acceptations", command=self.acceptation)
        self.statistic_menu.add_command(label="Distances", command=self.distances)

        """ Initializing the experiments menu """
        self.experiments_menu = Menu(self.menu, tearoff=0)
        self.experiments_menu.add_command(label="New experiments", command=self.new_experiments)
        self.experiments_menu.add_command(label="Start experiments", command=self.startExp)
        self.experiments_menu.add_command(label="Distances", command=self.distancesExp)

        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.menu.add_cascade(label="Replay", menu=self.replay_menu)
        self.menu.add_cascade(label="Command", menu=self.command_menu)
        self.menu.add_cascade(label="Stats", menu=self.statistic_menu)
        self.menu.add_cascade(label="Experiments", menu=self.experiments_menu)

        self.window.config(menu=self.menu)

    def new_maze(self):
        """
        Generate a new maze
        """
        Scenario(self.viewer)

    def save_maze(self):
        """
        Save the maze
        """
        maze_name_file = filedialog.asksaveasfilename(initialdir="./mazes/", title="Select file",
                                                filetypes=[("Pickle files", "*.pickle")])
        if maze_name_file:
            self.viewer.controller.save_maze(maze_name_file)

    def load_maze(self):
        """
        Load a maze
        """
        maze_name_file = filedialog.askopenfilename(initialdir="./mazes/", title="Select file",
                                                filetypes=[("Pickle files", "*.pickle")])
        if maze_name_file:
            self.viewer.load_maze(maze_name_file)

    def save_replay(self):
        """
        Save the replay
        """
        replay_name_file = filedialog.asksaveasfilename(initialdir="./replays/", title="Select file",
                                                filetypes=[("Pickle files", "*.pickle")])
        if replay_name_file:
            self.viewer.controller.save_replay(replay_name_file)

    def load_replay(self):
        """
        Load the replay
        """
        replay_name_file = filedialog.askopenfilename(initialdir="./replays/", title="Select file",
                                                filetypes=[("Pickle files", "*.pickle")])
        if replay_name_file:
            self.viewer.load_replay(replay_name_file)

    def messages(self):
        Messages(self.viewer.controller)

    def uncertainty(self):
        Uncertainty(self.viewer, self.viewer.controller)

    def acceptation(self):
        AcceptationRate(self.viewer, self.viewer.controller)

    def distances(self):
        Distances(self.viewer, self.viewer.controller)

    def new_scenario(self):
        """
        New scenario
        """
        Scenario(self.viewer, False)

    def new_experiments(self):
        """
        New experiments
        """
        Experiments(self.viewer, False)

    def quit(self):
        """
        Quit the simulation
        """
        self.viewer.stop = True

    def start(self):
        """
        Start the simulation
        """
        self.viewer.launch = True

    def stop(self):
        """
        Stop the simulation
        """
        self.viewer.launch = False

    def startExp(self):
        """
        Start the experimentation
        """
        self.viewer.experiments.run()

    def distancesExp(self):
        DistancesExperiments(self.viewer, self.viewer.experiments)