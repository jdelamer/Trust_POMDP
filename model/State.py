class State:

    def __init__(self, position, explored):
        self.position = position
        self.explored = explored

    def __eq__(self, other):
        if self.position != other.position:
            return False
        elif self.explored != other.explored:
            return False
        return True