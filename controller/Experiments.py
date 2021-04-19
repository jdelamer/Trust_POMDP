from controller.Simulator import Simulator
from controller.StatisticsExperiments import StatisticsExperiments


class Experiments:
    """
    Class allowing the user to run multiple experiments with the same configuration.
    """

    def __init__(self, nb_agents, position_agents, position_goal, nb_adversaries, nb_run, coordination):
        """
        Initializing the experiments
        """
        self.simulator = Simulator()
        self.nb_agents = nb_agents
        self.position_agents = position_agents
        self.position_goal = position_goal
        self.nb_adversaries = nb_adversaries
        self.nb_run = nb_run
        self.coordination = coordination
        self.stats = StatisticsExperiments()

    def run(self):
        print("Experiments started.")
        for i in range(self.nb_run):
            print("Simulation ", i)
            self.simulator.new_scenario(self.nb_agents, self.position_agents, self.position_goal, self.nb_adversaries,
                                        self.coordination)
            while not self.simulator.end:
                self.simulator.run()
            self.stats.add_stats_distances(self.simulator.stats.distances, self.nb_agents)
            self.simulator.end = False
        self.stats.calculate_distances()
        print("Experiments finished.")
        self.stats.print_distances()



