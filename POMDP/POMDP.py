import math

from POMDP.Action import Action

class POMDP:

    def __init__(self, maze, init_pos, mdp):
        self.maze = maze
        self.ax0, self.ay0 = init_pos[0], init_pos[1]
        self.mdp = mdp
        self.states = []
        self.b0 = []
        self.actions = [Action("N"), Action("S"), Action("W"), Action("E")]
        self.goals = []
        self.no_goals = []

        self.__init_states()
        self.__init_belief()
        self.policy = {}
        self.heuristic_search()

    def __init_states(self):
        self.states = [[x, y] for x in range(self.maze.nx) for y in range(self.maze.ny)]

    def __init_belief(self):
        self.b0 = []
        for s in self.states:
            if s == [self.ax0, self.ay0]:
                self.b0.append(0)
            else:
                self.b0.append(1)

    def belief_state_update(self, position):
        for i in range(len(self.b0)):
            if position == self.maze.end:
                if self.states[i] == position:
                    self.b0[i] = 1
                else:
                    self.b0[i] = 0
            else:
                if self.states[i] == position:
                    self.b0[i] = 0
                if position in self.goals:
                    self.goals.remove(position)

    def available_action(self, position):
        a_available = []
        cell = self.maze.cell_at(position[0], position[1])
        for a in self.actions:
            if cell.wall(a.direction):
                a_available.append(a)
        return a_available

    def heuristic_search(self):
        if self.goals:
            min_val = math.inf
            min_policy = None
            for i in range(len(self.goals)):
                if self.goals[i]:
                    val = self.mdp.policies[(self.goals[i][0], self.goals[i][1])][1][self.ay0][self.ax0]
                    if val < min_val:
                        min_val = val
                        min_policy = self.mdp.policies[(self.goals[i][0], self.goals[i][1])][0]
            self.policy = min_policy
        else:
            min_val = math.inf
            min_policy = None
            for i in range(len(self.b0)):
                if self.b0[i]:
                    val = self.mdp.policies[(self.states[i][0], self.states[i][1])][1][self.ay0][self.ax0]
                    if val < min_val:
                        min_val = val
                        min_policy = self.mdp.policies[(self.states[i][0], self.states[i][1])][0]
            self.policy = min_policy

    def deduce_goal(self, goals, no_goals):
        for i in range(len(self.b0)):
            for j in range(len(goals)):
                if self.states[i] == goals[j]:
                    if goals[j] not in self.goals and goals[j] not in self.no_goals:
                        self.goals.append(goals[j])
            for j in range(len(no_goals)):
                if self.states[i] == no_goals[j] and self.b0[i]:
                    if no_goals[j] not in self.no_goals:
                        self.b0[i] = 0
                        self.no_goals.append(no_goals[j])
                        if no_goals[j] in self.goals:
                            self.goals.remove(no_goals[j])

    def get_best_action(self):
        return Action(self.policy[self.ay0][self.ax0])

    def execute_action(self, action):
        cell = self.maze.cell_at(self.ax0, self.ay0)
        if action.direction == "Stay":
            return [self.ax0, self.ay0]
        if cell.wall(action.direction):
            return [self.ax0, self.ay0]
        else:
            new_ax, new_ay = self.ax0, self.ay0
            if action.direction == "S":
                new_ay += 1
            elif action.direction == "N":
                new_ay -= 1
            elif action.direction == "E":
                new_ax += 1
            elif action.direction == "W":
                new_ax -= 1
            self.belief_state_update([new_ax, new_ay])
            self.ax0, self.ay0 = new_ax, new_ay
        return [self.ax0, self.ay0]
