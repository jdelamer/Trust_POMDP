class Goal:

    def __init__(self, canvas, position, size):
        self.canvas = canvas
        self.position = position
        self.circle = self.canvas.create_oval(position[0], position[1],
                                              position[0]+size[0], position[1]+size[1], fill="yellow")
