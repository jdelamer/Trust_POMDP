import numpy as np


class ZKMaze:

    def __init__(self, id, pomdp):
        self.id = id
        self.pomdp = pomdp
        self.agents_pos = {}
        self.messages_received_prover = {}
        self.messages_sent_prover = {}
        self.mdp = self.pomdp.mdp
        self.goal_policy = {}

    def prover_send_answer(self, message_received):
        """
        Receive a message from a verifier.
        """
        policy = self.mdp.get_policy(message_received)
        return policy[self.pomdp.ay0][self.pomdp.ax0]

    def verifier_send_question(self, id):
        """ Send a question to a specific agent. """
        pos = self.random_position(self.pomdp.maze.nx, self.pomdp.maze.ny)
        self.messages_sent_prover[id] = pos
        return pos

    def verifier_receive_answer(self, id, message):
        """ Receive the answer to the question. """
        self.messages_received_prover[id] = message

    def estimate_position_agent(self, id):
        """
        Estimate the position of the agent
        :param id: Id of the agent
        """
        positions = self.get_position_possible(self.messages_received_prover[id], self.messages_sent_prover[id])
        if id in self.agents_pos:
            new_positions = self.reduce_position_uncertainty(id, positions)
            self.agents_pos[id] = new_positions
        else:
            self.agents_pos[id] = positions

    def get_position_possible(self, value, goal):
        """
        Get all the positions possible of the agent.
        :param value: Value send by the prover
        :param goal: Goal
        :return: List of positions
        """
        policy = self.mdp.get_policy(goal)
        positions = []
        for j in range(len(policy)):
            for i in range(len(policy[j])):
                if policy[j][i] == value and [i, j] not in positions:
                    positions.append([i, j])
        return positions

    def reduce_position_uncertainty(self, id, new_estimation):
        """
        Reduce the uncertainty on the estimated positions
        :param id: id of the agent
        :param new_estimation: new positions estimated
        :return: List of positions
        """
        positions = []
        previous_estimation = self.agents_pos[id]
        for pe in previous_estimation:
            for ne in new_estimation:
                previous_cell = self.pomdp.maze.cell_at(pe[0], pe[1])
                new_cell = self.pomdp.maze.cell_at(ne[0], ne[1])
                if previous_cell.wall_between(new_cell) is not None:
                    if not previous_cell.wall_between(new_cell) and ne not in positions:
                        positions.append(ne)
                if previous_cell == new_cell:
                    positions.append(ne)
        return positions

    def random_position_avoid(self, xmax, ymax, avoid):
        """
        Generate a random position
        :param xmax: position maximum in X
        :param ymax: position maximum in Y
        :param avoid: Position to avoid
        :return: A random position
        """
        while True:
            x = np.random.randint(xmax)
            y = np.random.randint(ymax)
            if [x, y] != avoid:
                return [x, y]

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
