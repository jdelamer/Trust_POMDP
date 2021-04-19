from math import sqrt


class Cell:
    """A cell in the maze.

    A maze "Cell" is a point in the grid which may be surrounded by walls to
    the north, east, south or west.

    """
    # A wall separates a pair of cells in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        """
        Initialize the cell at (x,y). At first it is surrounded by walls.
        :param x: Position in x
        :param y: Position in y
        """

        self.x, self.y = x, y
        self.pos = [x, y]
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def wall(self, direction):
        """
        Return if the cell has a wall in a specific direction
        :param direction: direction
        :return: True or False
        """
        return self.walls[direction]

    def has_all_walls(self):
        """ Return if the cell has all its walls """

        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        """ Knock down the wall between cells self and other. """

        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False

    def wall_between(self, other):
        """
        Return if there is a wall between two cells.
        """
        direction = [other.x - self.x, other.y - self.y]
        if direction == [-1, 0]:
            return self.wall('W')
        elif direction == [1, 0]:
            return self.wall('E')
        elif direction == [0, -1]:
            return self.wall('N')
        elif direction == [0, 1]:
            return self.wall('S')
        else:
            return None

    def distance(self, other):
        return abs(sqrt(pow(other.x - self.x, 2) + pow(other.x - self.x, 2)))
