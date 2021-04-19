from copy import deepcopy


class Replay:
    """
    Class representing a replay
    """

    def __init__(self, maze, agents, agents_positions, adversaries=[], adversaries_position=[]):
        """
        Initializing the replay
        :param maze: The maze
        :param agents: List of agents
        :param agents_positions: List of agents position
        :param adversaries: List of adversaries
        :param adversaries_position: List of adversaries position
        """
        self.maze = maze
        self.agents = deepcopy(agents)
        self.agents_positions = []
        self.adversaries = deepcopy(adversaries)
        self.adversaries_position = []
        self.messages = []
        self.index = 0
        self.index_max = 0
        for i in range(len(agents_positions)):
            self.agents_positions.append([agents_positions[i]])
        for i in range(len(adversaries_position)):
            self.adversaries_position.append([adversaries_position[i]])
        for i in range(len(agents_positions)+len(adversaries)):
            self.messages.append([])

    def update_positions(self, positions):
        """
        Update the positions of the agents
        :param positions: List of positions
        """
        for i in range(len(positions)):
            self.agents_positions[i].append(positions[i])
        self.index_max += 1

    def update_positions_adversary(self, positions):
        """
        Update the position of the adversaries
        :param positions: List of positions
        """
        for i in range(len(positions)):
            self.adversaries_position[i].append(positions[i])

    def update_messages(self, messages):
        """
        Updates the messages sent
        :param messages: List of messages
        """
        for i in range(len(messages)):
            self.messages[i].append(messages[i])

    def get_positions(self):
        """
        Get the positions of the agents at one step
        :return: List of positions
        """
        positions = []
        for i in range(len(self.agents)):
            positions.append(self.agents_positions[i][self.index+1])
        return positions

    def get_positions_adversaries(self):
        """
        Get the position of the adversaries
        :return: List of positions
        """
        positions = []
        for i in range(len(self.adversaries)):
            positions.append(self.adversaries_position[i][self.index + 1])
        return positions

    def get_messages(self):
        """
        Get the messages sent at this time step
        :return: List of messages
        """
        messages = []
        for i in range(len(self.messages)):
            messages.append(self.messages[i][self.index])
        return messages
