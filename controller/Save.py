from copy import deepcopy


class Save:

    def __init__(self, maze, mdp):
        self.maze = deepcopy(maze)
        self.mdp = deepcopy(mdp)
        self.process()

    def process(self):
        self.maze.end = []
