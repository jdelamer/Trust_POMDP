import random
import numpy as np


from POMDP.POMDP import POMDP
from ZK.Answer import Answer
from ZK.Question import Question

class AdvProtocol:

    def __init__(self, pomdp: POMDP):
        self.pomdp = pomdp
        self.policy_range = []
        self.range_global = [300, 0]

        for j in range(self.pomdp.maze.ny):
            self.policy_range.append([])
            for i in range(self.pomdp.maze.nx):
                self.policy_range[j].append([1000, -1000])

    def verifier_send_question(self):
        x = self.random_position(self.pomdp.maze.nx, self.pomdp.maze.ny)
        range_min = min(self.policy_range[x[0]][x[1]][0], self.range_global[0])
        range_max = max(self.policy_range[x[0]][x[1]][1], self.range_global[1])
        c = np.random.uniform(range_min, range_max)
        return 0, Question(x, c)

    def verifier_check_answer(self, answer: Answer):
        return self.b == answer.b

    def prover_send_answer(self):
        return Answer(random.choice([False, True])), []

    def random_position(self, xmax, ymax):
        """
        Generate a random position
        :param xmax: position maximum in X
        :param ymax: position maximum in Y
        :return: A random position
        """
        x = np.random.randint(xmax)
        y = np.random.randint(ymax)
        return [x, y]