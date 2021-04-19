import random

from POMDP.Action import Action
from model.Transition import execute_action


class MDP:

    def __init__(self, maze):
        self.maze = maze
        self.actions = [Action("E"), Action("W"), Action("N"), Action("S")]
        self.policies = {}

    def cost_function(self, position, new_position, rng):
        if position == new_position:
            return 1000
        else:
            return 2+rng

    def compute_all_policies(self, gamma):
        self.policies = {}
        goals = [[x, y] for x in range(self.maze.nx) for y in range(self.maze.ny)]
        for g in goals:
            self.policies[(g[0], g[1])] = self.value_iteration(gamma, g)
        return self.policies

    def available_action(self, position):
        a_available = []
        cell = self.maze.cell_at(position[0], position[1])
        for a in self.actions:
            if not cell.wall(a.direction):
                a_available.append(a)
        return a_available

    def value_iteration(self, gamma, goal, val=None):
        """
        Performs value iteration on a given grid of objects.
        """

        is_value_changed = True
        policy = [[0 for i in range(self.maze.nx)] for j in range(self.maze.ny)]
        values = [[1000 for i in range(self.maze.nx)] for j in range(self.maze.ny)]
        # iterate values until convergence
        if val!=None:
            rng=0
        else:
            rng = random.random()
        while is_value_changed:
            is_value_changed = False
            for i in range(self.maze.nx):
                for j in range(self.maze.ny):
                    if [i, j] != goal:
                        q = 0
                        for a in self.available_action([i, j]):
                            neighbor = execute_action(self.maze, [i, j], a)
                            cost = self.cost_function([i, j], neighbor.pos, rng)
                            q = cost + gamma * values[neighbor.y][neighbor.x]
                            if q < values[j][i]:
                                values[j][i] = q
                                policy[j][i] = a
                                is_value_changed = True
                    else:
                        values[j][i] = 0
                        policy[j][i] = "Stay"
        return policy, values

    def get_policy(self, position):
        return self.policies[(position[0], position[1])][1]
