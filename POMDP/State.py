class State:

    def __init__(self, ax, ay, gx, gy):
        self.ax, self.ay = ax, ay
        self.gx, self.gy = gx, gy

    def goal(self):
        if self.ax == self.gx and self.ay == self.gy:
            return True
        return False

    def __eq__(self, other):
        if self.ax == other.ax and self.ay == other.ay and self.gx == other.gx and self.gy == other.gy:
            return True
        return False

    def __repr__(self):
        return "(" + str(self.ax) + "," + str(self.ay) + "," +str(self.gx) + "," +str(self.gy) + ")"

