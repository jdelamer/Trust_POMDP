from copy import deepcopy

from POMDP.POMDP import POMDP
from model.Agent import Agent
from model.Maze import Maze

import numpy as np


class World:
    """
    Class representing the world
    """
    def __init__(self):
        self.size = [0, 0]
        self.maze = []
        self.agents = []
        self.adversaries = []

    def create_agents(self, nb_agents, mdp):
        """
        Create a number of agents
        :param nb_agents: Number of agents
        :param mdp: MDP
        """
        for i in range(nb_agents):
            x, y = np.random.randint(self.maze.nx, size=2)
            pomdp = POMDP(self.maze, [x, y], deepcopy(mdp))
            a = Agent(i, [x, y], pomdp)
            self.agents.append(a)

    def create_random_goal(self):
        """ Create a random goal """
        x = np.random.randint(self.maze.nx)
        y = np.random.randint(self.maze.ny)
        self.maze.end = [x, y]

    def get_end(self):
        """
        Return the position of the end
        :return: The end position
        """
        return self.maze.end

    def get_agents_position(self):
        """
        Return the position of the agents
        :return: The list of position
        """
        agents_position = []
        for a in self.agents:
            agents_position.append(a.position)
        return agents_position

    def get_adversary_position(self):
        """
        Return the position of the adversaries
        :return: The list of position
        """
        adversaries_position = []
        for a in self.adversaries:
            adversaries_position.append(a.position)
        return adversaries_position

    def reset(self):
        """
        Reset the world
        """
        self.maze = Maze(self.size[0], self.size[1])
        self.agents = []
