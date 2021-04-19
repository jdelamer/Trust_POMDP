from tkinter import *

from view.Goal import Goal


class Maze(Canvas):

    def __init__(self, frame, maze, **kw):
        """
        Initializing the class Maze.
        The class inherit of the Class Canvas.
        :param frame: Frame where the canvas will be displayed
        :param maze: Class Maze from package model
        :param kw: Optional arguments
        """
        self.aspect_ratio = maze.nx / maze.ny
        self.padding = 20

        self.height = kw["height"]
        self.width = int(kw["height"] * self.aspect_ratio)

        super().__init__(frame, height=self.height, width=self.width)

        self.maze = maze
        self.maze_img = []
        self.goal = []
        self.configure(background="white")

        # Height and width of the maze image (excluding padding), in pixels
        self.height_maze = kw["height"] - 2 * self.padding
        self.width_maze = int(kw["height"] * self.aspect_ratio) - 2 * self.padding
        self.pack(side=LEFT)

        # Scaling factors mapping maze coordinates to image coordinates
        self.scy, self.scx = self.height_maze / self.maze.ny, self.width_maze / self.maze.nx

    def draw(self):
        """
        Draw the maze
        """
        for x in range(self.maze.nx):
            for y in range(self.maze.ny):
                if self.maze.cell_at(x, y).walls['S']:
                    x1, y1, x2, y2 = self.padding + x * self.scx, self.padding + (y + 1) * self.scy, \
                                     self.padding + (x + 1) * self.scx, self.padding + (y + 1) * self.scy
                    line = self.create_line(x1, y1, x2, y2)
                    self.maze_img.append(line)
                if self.maze.cell_at(x, y).walls['E']:
                    x1, y1, x2, y2 = self.padding + (x + 1) * self.scx, self.padding + y * self.scy, \
                                     self.padding + (x + 1) * self.scx, self.padding + (y + 1) * self.scy
                    line = self.create_line(x1, y1, x2, y2)
                    self.maze_img.append(line)
        self.maze_img.append(self.create_line(self.padding, self.padding, self.width_maze + self.padding, self.padding))
        self.maze_img.append(self.create_line(self.padding, self.padding, self.padding, self.height_maze + self.padding))
        if self.maze.end:
            pos_goal = [int(self.padding + self.maze.end[0] * self.scx),
                        int(self.padding + self.maze.end[1] * self.scy)]
            self.goal = Goal(self, pos_goal, [self.scx, self.scy])
