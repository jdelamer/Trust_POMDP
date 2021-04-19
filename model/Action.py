class Action:

    """ Class representing an action """

    def __init__(self, direction):
        self.direction = str(direction)
        if direction == None:
            self.direction = "Stay"

    def __repr__(self):
        return self.direction
