from ZK.ZKMaze import ZKMaze
from ZK.ZKProtocol import ZKProtocol


class Agent:

    """ Class representing an agent """

    def __init__(self, id, position, pomdp):
        """
        Initializing the class.
        :param id: id of the agent
        :param position: position of the agent
        """
        self.id = id
        self.position = position
        self.pomdp = pomdp
        self.zkmaze = ZKMaze(id, pomdp)
        self.zkprotocol = ZKProtocol(id, pomdp)

    def __repr__(self):
        return "(" + str(self.position[0]) + "," + str(self.position[1]) + ")"

    def __str__(self):
        return "(" + str(self.position[0]) + "," + str(self.position[1]) + ")"
