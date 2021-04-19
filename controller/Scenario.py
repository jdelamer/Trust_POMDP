from copy import deepcopy

from POMDP.POMDP import POMDP
from model.Adversary import Adversary
from model.Agent import Agent
from model.Maze import Maze

import numpy as np


class Scenario:
    """
    Class representing a scenario
    """

    def __init__(self, maze_size, nb_agents, position_agents, position_goal):
        """
        Initializing the class
        :param maze_size: size of the maze
        :param nb_agents: number of agents
        :param position_agents: agents position
        :param position_goal: goal position
        """
        self.maze_size = maze_size
        self.nb_agents = nb_agents
        self.position_agents = position_agents
        self.position_goal = position_goal

        self.maze = []
        self.agents = []
        self. adversaries = []

    def create_maze(self):
        """
        Create a maze
        """
        self.maze = Maze(self.maze_size[0], self.maze_size[1], self.position_goal)
        self.maze.make_maze()

    def create_agents(self, mdp):
        """
        Create a number of agents with a defined position
        :param mdp: MDP
        """
        if self.position_agents:
            for i in range(self.nb_agents):
                pomdp = POMDP(self.maze, self.position_agents[i], deepcopy(mdp))
                a = Agent(i, self.position_agents[i], pomdp)
                self.agents.append(a)
        else:
            self.random_agents(mdp)

    def random_agents(self, mdp):
        """
        Generate a number of agents
        :param mdp: MDP
        """
        for i in range(self.nb_agents):
            x, y = np.random.randint(self.maze_size[0], size=1)[0],  np.random.randint(self.maze_size[1], size=1)[0]
            pomdp = POMDP(self.maze, [x, y], deepcopy(mdp))
            a = Agent(i, [x, y], pomdp)
            self.agents.append(a)

    def random_adversaries(self, nb_adversaries, mdp):
        """
        Generate random adversaries
        :param nb_adversaries: Number of adversaries
        :param mdp: MDP
        """
        for i in range(nb_adversaries):
            x, y = np.random.randint(self.maze_size[0], size=1)[0],  np.random.randint(self.maze_size[1], size=1)[0]
            pomdp = POMDP(self.maze, [x, y], deepcopy(mdp))
            a = Adversary(100+i, [x, y], pomdp)
            self.adversaries.append(a)
