from typing import List

class Question:

    def __init__(self, x: List[int], c: float):
        self.x = x
        self.c = c

    def __repr__(self):
        return "((" + str(self.x[0]) + "," + str(self.x[1]) + "), " + str(self.c) + ")"

    def __str__(self):
        return "((" + str(self.x[0]) + "," + str(self.x[1]) + "), " + str(self.c) + ")"
