class EstimatedPosition:
    """
    Class representing one estimated position.
    """

    def __init__(self, canvas, position, size, color, fill=True):
        self.canvas = canvas
        self.position = position
        self.size = size
        self.color = color
        if fill:
            self.rectangle = self.canvas.create_rectangle(position[0], position[1], position[0]+size[0],
                                                      position[1]+size[1], outline=self.color, fill=self.color)
        else:
            self.rectangle = self.canvas.create_rectangle(position[0], position[1], position[0] + size[0],
                                                          position[1] + size[1], outline=self.color, width=2)
