import math
import numpy as np

class StatisticsExperiments:

    def __init__(self):
        self.minimum = []
        self.std_minimum = 0

        self.maximum = []
        self.std_maximum = 0

        self.average = []
        self.std_average = 0

    def add_stats_distances(self, distances, nb_agents):
        minimum = math.inf
        maximum = 0
        average = 0
        for d in distances:
            if d < nb_agents:
                goal = distances[d].index(0.0)
                if goal < minimum:
                    minimum = goal
                if goal > maximum:
                    maximum = goal
                average += goal
        self.minimum.append(minimum)
        self.maximum.append(maximum)
        self.average.append(average/nb_agents)

    def calculate_distances(self):
        self.std_average = np.std(self.average)
        self.maximum = max(self.minimum)
        self.average = np.average(self.average)
        self.minimum = min(self.minimum)

    def print_distances(self):
        print("Best case: ", self.minimum)
        # print("Std Best case: ", self.std_minimum)
        print("Worst case: ", self.maximum)
        # print("Std Worst case: ", self.std_maximum)
        print("Average: ", self.average)
        print("Std Average: ", self.std_average)

