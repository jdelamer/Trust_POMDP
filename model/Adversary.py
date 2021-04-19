from ZK.AdvProtocol import AdvProtocol
from controller.AdversaryStrategy import AdversaryStrategy


class Adversary:

    """ Class representing an agent """

    def __init__(self, id, position, pomdp, ranged=True, previous_values=False):
        """
        Initializing the class.
        :param id: id of the agent
        :param position: position of the agent
        """
        self.id = id
        self.position = position
        self.pomdp = pomdp
        self.strategy = AdversaryStrategy(id, pomdp, ranged, previous_values)
        self.zkprotocol = AdvProtocol(pomdp)

    def __repr__(self):
        return "(" + str(self.id) + "," + str(self.position[0]) + "," + str(self.position[1]) + ")"

    def __str__(self):
        return "(" + str(self.id) + "," + str(self.position[0]) + "," + str(self.position[1]) + ")"
