class Answer:

    def __init__(self, b: bool):
        self.b = b

    def __repr__(self):
        return str(self.b)

    def __eq__(self, other):
        if other == self.b:
            return True
        return False