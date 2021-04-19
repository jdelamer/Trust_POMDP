import numpy as np

class AdversaryStrategy:
    """
    Class representing the adversary strategy
    """
    def __init__(self, id, pomdp, ranged=True, previous_values=False):
        """
        Initializing the class
        :param id: Id of the adversary
        :param pomdp: POMDP
        :param ranged: Strategy ranged
        :param previous_values: Strategy previous values
        """
        self.id = id
        self.pomdp = pomdp
        self.ranged = ranged
        self.previous_values = previous_values
        self.policy_range = []
        self.policy_values = []
        self.messages_received_prover = {}
        self.messages_sent_prover = {}
        self.range_global = [300, 0]
        self.all_values = [0]

        for j in range(self.pomdp.maze.ny):
            self.policy_range.append([])
            for i in range(self.pomdp.maze.nx):
                self.policy_range[j].append([1000, -1000])
        for j in range(self.pomdp.maze.ny):
            self.policy_values.append([])
            for i in range(self.pomdp.maze.nx):
                self.policy_values[j].append([])

    def prover_send_answer(self, message_received):
        """
        Receive a message from a verifier.
        """
        x, y = message_received[0], message_received[1]
        value = 0
        if self.ranged:
            range_min = min(self.policy_range[y][x][0], self.range_global[0])
            range_max = max(self.policy_range[y][x][1], self.range_global[1])
            value = np.random.uniform(range_min, range_max)
        if self.previous_values:
            if self.policy_values[y][x]:
                value = np.random.choice(self.policy_values[y][x])
            else:
                value = np.random.choice(self.all_values)
        return value

    def verifier_send_question(self, id):
        """ Send a question to a specific agent. """
        pos = self.random_position(self.pomdp.maze.nx, self.pomdp.maze.ny)
        self.messages_sent_prover[id] = pos
        return pos

    def verifier_receive_answer(self, id, message):
        """ Receive the answer to the question. """
        self.messages_received_prover[id] = message
        self.update_range(self.messages_sent_prover[id], message)
        self.update_values(self.messages_sent_prover[id], message)

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

    def update_range(self, position, value):
        """
        Update the range of possible values
        :param position: position of the cell
        :param value: new value
        """
        if value < self.policy_range[position[0]][position[1]][0]:
            self.policy_range[position[0]][position[1]][0] = value
        if value > self.policy_range[position[0]][position[1]][1]:
            self.policy_range[position[0]][position[1]][1] = value
        if value < self.range_global[0]:
            self.range_global[0] = value
        if value > self.range_global[1]:
            self.range_global[1] = value

    def update_values(self, position, value):
        """
        Update the values
        :param position: position of the cell
        :param value: new value
        """
        if value not in self.policy_values[position[0]][position[1]]:
            self.policy_values[position[0]][position[1]].append(value)
        if value not in self.all_values:
            self.all_values.append(value)
