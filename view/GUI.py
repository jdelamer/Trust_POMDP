from tkinter import *
import numpy as np

from controller.Experiments import Experiments
from controller.Simulator import Simulator
from view.Adversary import Adversary
from view.Agent import Agent
from view.Maze import Maze
from view.MenuBar import MenuBar


class GUI:

    def __init__(self):
        """
        Initializing the class
        """

        self.controller = Simulator()
        self.experiments = None

        """ Initializing the window. """
        self.screen = Tk()
        self.screen.title("Maze")
        self.screen.resizable(0, 0)
        self.menu = MenuBar(self.screen, self)

        self.launch = False

        """ Initializing the Canvas containing the maze. """
        self.maze_canvas = Canvas()

        """ Initializing the agents. """
        self.agents = []
        self.adversaries = []

        """ Initializing the command to slow or accelerate the simulation. """
        self.screen.bind("<Up>", self.accelerate)
        self.screen.bind("<Down>", self.slow)
        self.screen.bind("<space>", self.reset_speed)
        self.simulation_speed = 500

        self.stop = False

        self.run()

    def run(self):
        """
        Run the simulation
        """
        while not self.stop:
            if self.launch:
                self.screen.after(self.simulation_speed, self.controller.run())
                self.update_agents()
                self.update_adversaries()
                self.screen.update()
                if self.controller.launch_replay:
                    if self.controller.replay.index == self.controller.replay.index_max:
                        self.launch = False
            else:
                self.screen.after(self.simulation_speed, self.screen.update())

    def create_scenario(self, maze_size, nb_agents, position_agents, position_goal, nb_adversaries):
        """
        Generate a new maze.
        """
        self.controller.create_scenario(maze_size, nb_agents, position_agents, position_goal, nb_adversaries)
        self.maze_canvas.destroy()
        self.maze_canvas = Maze(self.screen, self.controller.get_maze(), height=500)
        self.maze_canvas.draw()

        """Reset the agents."""
        colors = self.create_random_color(len(self.controller.world.agents) + len(self.controller.world.adversaries))
        i_c = 0
        self.agents = []
        for a in self.controller.world.agents:
            agent = Agent(self.maze_canvas, a.position, colors[i_c])
            self.agents.append(agent)
            i_c += 1
        """ Reset the adversaries """
        self.adversaries = []
        for a in self.controller.world.adversaries:
            adversary = Adversary(self.maze_canvas, a.position, colors[i_c])
            self.adversaries.append(adversary)
            i_c += 1

    def new_scenario(self, nb_agents, position_agents, position_goal, nb_adversaries):
        """
        Generate a new maze.
        """
        self.controller.new_scenario(nb_agents, position_agents, position_goal, nb_adversaries)
        self.maze_canvas.destroy()
        self.maze_canvas = Maze(self.screen, self.controller.get_maze(), height=500)
        self.maze_canvas.draw()
        for i in range(len(self.agents)):
            for j in self.agents[i].estimated_positions:
                self.maze_canvas.delete(j.rectangle)

        colors = self.create_random_color(len(self.controller.world.agents)+len(self.controller.world.adversaries))
        i_c = 0
        self.agents = []
        for a in self.controller.world.agents:
            agent = Agent(self.maze_canvas, a.position, colors[i_c])
            self.agents.append(agent)
            i_c += 1
        """ Reset the adversaries """
        self.adversaries = []
        for a in self.controller.world.adversaries:
            adversary = Adversary(self.maze_canvas, a.position, colors[i_c])
            self.adversaries.append(adversary)
            i_c += 1

    def new_experiments(self, nb_agents, position_agents, position_goal, nb_adversaries, nb_run, coordination):
        """
        Generate a new set of experiments
        """
        self.experiments = Experiments(nb_agents, position_agents, position_goal, nb_adversaries, nb_run, coordination)
        self.experiments.simulator = self.controller
        self.maze_canvas.destroy()
        self.maze_canvas = Maze(self.screen, self.controller.get_maze(), height=500)
        self.maze_canvas.draw()
        for i in range(len(self.agents)):
            for j in self.agents[i].estimated_positions:
                self.maze_canvas.delete(j.rectangle)

        colors = self.create_random_color(len(self.controller.world.agents) + len(self.controller.world.adversaries))
        i_c = 0
        self.agents = []
        for a in self.controller.world.agents:
            agent = Agent(self.maze_canvas, a.position, colors[i_c])
            self.agents.append(agent)
            i_c += 1
        """ Reset the adversaries """
        self.adversaries = []
        for a in self.controller.world.adversaries:
            adversary = Adversary(self.maze_canvas, a.position, colors[i_c])
            self.adversaries.append(adversary)
            i_c += 1


    def update_agents(self):
        """ Update the agents """
        estimated_positions = self.controller.get_estimated_agent_positions()
        for i in range(len(self.agents)):
            self.agents[i].move(self.controller.world.agents[i].position)
            if i in estimated_positions:
                self.agents[i].update_estimated_position(estimated_positions[i])

    def update_adversaries(self):
        """ Update the agents """
        estimated_positions = self.controller.get_estimated_agent_positions()
        for i in range(len(self.adversaries)):
            self.adversaries[i].move(self.controller.world.adversaries[i].position)
            if self.controller.world.adversaries[i].id in estimated_positions:
                self.adversaries[i].update_estimated_position(estimated_positions[self.controller.world.adversaries[i].id])
            else:
                self.adversaries[i].update_estimated_position([])

    def load_maze(self, file_name):
        """
        Load a maze.
        :param file_name: Name of the file
        """
        self.controller.load_maze(file_name)
        self.maze_canvas.destroy()
        self.maze_canvas = Maze(self.screen, self.controller.get_maze(), height=500)
        self.maze_canvas.draw()

    def load_replay(self, file_name):
        """
        Load a replay.
        :param file_name: Name of the file
        """
        self.controller.load_replay(file_name)
        self.controller.launch_replay = True
        self.maze_canvas.destroy()
        self.maze_canvas = Maze(self.screen, self.controller.get_maze(), height=500)
        self.maze_canvas.draw()

        """Reset the agents."""
        colors = self.create_random_color(len(self.controller.world.agents) + len(self.controller.world.adversaries))
        i_c = 0
        self.agents = []
        for a in self.controller.world.agents:
            agent = Agent(self.maze_canvas, a.position, colors[i_c])
            self.agents.append(agent)
            i_c += 1
        """ Reset the adversaries """
        self.adversaries = []
        for a in self.controller.world.adversaries:
            adversary = Adversary(self.maze_canvas, a.position, colors[i_c])
            self.adversaries.append(adversary)
            i_c += 1

    def create_random_color(self, nb_colors):
        """
        Create random colors
        :param nb_colors: number of colors
        :return: colors
        """
        colors = []
        rands = np.random.randint(0, 16777215, nb_colors)
        for i in range(nb_colors):
            colors.append("#" + ("%06x" % rands[i]))
        return colors

    def slow(self, event):
        """Slow the simulation by adding 250 milliseconds before the next simulation step."""
        self.simulation_speed += 250

    def accelerate(self, event):
        """Accelerate the simulation by removing 250 milliseconds before the next simulation step."""
        self.simulation_speed -= 250

    def reset_speed(self, event):
        """Reset to the default time step."""
        self.simulation_speed = 500
