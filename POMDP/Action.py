class Action:

    """ Class representing an action """

    def __init__(self, direction):
        self.direction = str(direction)
        if self.direction is None:
            self.direction = "Stay"

    def __eq__(self, other):
        if self.direction == other.direction:
            return True
        return False

    def __repr__(self):
        return self.direction
