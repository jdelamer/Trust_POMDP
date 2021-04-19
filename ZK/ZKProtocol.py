import random

import numpy as np


from POMDP.POMDP import POMDP
from ZK.Answer import Answer
from ZK.Question import Question


class ZKProtocol:

    def __init__(self, id_agent: int, pomdp: POMDP):
        self.id_agent = id_agent
        self.pomdp = pomdp
        self.b = 0

    def verifier_send_question(self):
        x = self.random_position(self.pomdp.maze.nx, self.pomdp.maze.ny)
        self.b = random.choice([False, True])
        c = 0
        if self.b:
            c = self.pomdp.mdp.get_policy(x)[self.pomdp.ay0][self.pomdp.ax0]
        else:
            c = np.random.uniform(0, 200, 1)[0]
        return self.b, Question(x, c)

    def verifier_check_answer(self, answer: Answer):
        return self.b == answer.b

    def prover_send_answer(self, question: Question):
        policy = self.pomdp.mdp.get_policy(question.x)
        positions = []
        for j in range(len(policy)):
            for i in range(len(policy[j])):
                if policy[j][i] == question.c:
                    positions.append([i, j])
        if positions:
            return Answer(True), positions
        else:
            return Answer(False), positions

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
