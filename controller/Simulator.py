import pickle

from algorithm.MDP import MDP
from controller.Replay import Replay
from controller.Save import Save
from controller.Scenario import Scenario
from controller.Statistics import Statistics
from model.World import World


class Simulator:

    """
    Class representing the Simulator.
    """

    def __init__(self):
        """
        Initializing the Simulator
        """
        self.world = World()
        self.mdp = []
        self.replay = Replay(self.world.maze, self.world.agents, self.world.get_agents_position())
        self.launch_replay = False
        self.stats = Statistics(len(self.world.agents), len(self.world.adversaries))
        self.distances = []
        self.end = False
        self.coordination = True

    def get_maze(self):
        """
        Return the class Maze contained in the class World
        :return: Return the maze
        """
        return self.world.maze

    def generate_maze(self, size):
        """
        Generate a maze.
        """
        self.world.maze.make_maze(size)
        self.world.create_random_goal()

    def init_simulator(self):
        """
        Initialize the simulator and create the mdp and the agents
        """
        self.generate_maze([15, 15])
        self.mdp = self.calculate_policies()
        self.world.create_agents(2, self.mdp)

    def calculate_policies(self):
        """
        Create the MDP and calculate all the policies
        :return:
        """
        print(" Computing policies... ")
        mdp = MDP(self.world.maze)
        mdp.compute_all_policies(0.99)
        print(" Done. ")
        return mdp

    def create_scenario(self, maze_size, nb_agents, position_agents, position_goal, nb_adveraries):
        """
        Create a new scenario
        :param maze_size: the size of the maze to generate
        :param nb_agents: the number of agents
        :param position_agents: the positions of the agents
        :param position_goal: the position of the goal
        """
        scenario = Scenario(maze_size, nb_agents, position_agents, position_goal)
        scenario.create_maze()
        self.world.maze = scenario.maze
        self.mdp = self.calculate_policies()
        scenario.create_agents(self.mdp)
        scenario.random_adversaries(nb_adveraries, self.mdp)
        self.world.agents = scenario.agents
        self.world.adversaries = scenario.adversaries
        self.replay = Replay(self.world.maze, self.world.agents, self.world.get_agents_position(), self.world.adversaries, self.world.get_adversary_position())
        self.stats = Statistics(len(self.world.agents), len(self.world.adversaries))
        self.distances = self.mdp.value_iteration(1, self.world.maze.end)[1]

    def new_scenario(self, nb_agents, position_agents, position_goal, nb_adveraries, coordination=True):
        """
        Create a new scenario without changing the map
        :param nb_agents: the number of agents
        :param position_agents: the positions of the agents
        :param position_goal: the position of the goal
        """
        scenario = Scenario([self.world.maze.nx, self.world.maze.ny], nb_agents, position_agents, position_goal)
        scenario.nb_agents = nb_agents
        scenario.maze = self.world.maze
        scenario.create_agents(self.mdp)
        scenario.random_adversaries(nb_adveraries, self.mdp)
        self.world.agents = scenario.agents
        self.world.adversaries = scenario.adversaries
        self.world.maze.end = position_goal
        self.replay = Replay(self.world.maze, self.world.agents, self.world.get_agents_position(), self.world.adversaries, self.world.get_adversary_position())
        self.stats = Statistics(len(self.world.agents), len(self.world.adversaries))
        self.distances = self.mdp.value_iteration(1, self.world.maze.end)[1]
        self.coordination = coordination

    def reset(self):
        """
        Reset the simulation
        :return the new world
        """
        self.world.reset()
        self.init_simulator()
        return self.world

    def run(self):
        """
        Run the problem
        """
        if self.launch_replay:
            self.run_replay()
        else:
            positions = []
            positions_adv = []
            for a in self.world.agents:
                if a.position != self.world.get_end():
                    self.run_agent(a)
                positions.append(a.position)
                self.stats.update_distances(a.id, self.distances[a.position[1]][a.position[0]]/2)
            for adv in self.world.adversaries:
                if adv.position != self.world.get_end():
                    self.run_adversary(adv)
                positions_adv.append(adv.position)
                self.stats.update_distances(adv.id, self.distances[adv.position[1]][adv.position[0]]/2)
            self.replay.update_positions(positions)
            self.replay.update_positions_adversary(positions_adv)
            messages = self.exchanging_message()
            self.replay.update_messages(messages)
            self.stats.update_messages(self.world, messages)
            goals_possible, no_goals = self.deduce_goal()
            for a in self.world.agents:
                if self.coordination:
                    a.pomdp.deduce_goal(goals_possible, no_goals)
                else:
                    a.pomdp.deduce_goal([], [])
        self.checkEnd()

    def run_replay(self):
        if self.replay.index < self.replay.index_max:
            positions = self.replay.get_positions()
            positions_adv = self.replay.get_positions_adversaries()
            messages = self.replay.get_messages()
            self.replay.index += 1
            for i in range(len(self.world.agents)):
                self.world.agents[i].position = positions[i]
                self.stats.update_distances(self.world.agents[i].id, self.distances[self.world.agents[i].position[1]][self.world.agents[i].position[0]] / 2)
            for i in range(len(self.world.adversaries)):
                self.world.adversaries[i].position = positions_adv[i]
                self.stats.update_distances(self.world.adversaries[i].id, self.distances[self.world.adversaries[i].position[1]][
                    self.world.adversaries[i].position[0]] / 2)
            self.stats.update_messages(self.world, messages)


    def run_agent(self, agent):
        """
        Run the process for each agent
        :param agent: agent
        """
        # Get the best action following the current policy
        action = agent.pomdp.get_best_action()
        # Execute the action
        new_position = agent.pomdp.execute_action(action)
        # Update the position of the agent
        agent.position = new_position
        # Search with an heuristic the best policy to execute
        agent.pomdp.heuristic_search()

    def run_adversary(self, adversary):
        """
        Run the process for each adversary
        :param adversary: adversary
        """
        # Get the best action following the current policy
        action = adversary.pomdp.get_best_action()
        # Execute the action
        new_position = adversary.pomdp.execute_action(action)
        # Update the position of the agent
        adversary.position = new_position
        # Search with an heuristic the best policy to execute
        adversary.pomdp.heuristic_search()

    def exchanging_message(self):
        """
        Exchange messages between agents.
        """
        messages = []
        for i in range(len(self.world.agents)):
            verifier = self.world.agents[i]
            messages_a = []
            for j in range(len(self.world.agents)):
                if j != i:
                    prover = self.world.agents[j]
                    question = verifier.zkmaze.verifier_send_question(prover.id)
                    answer = prover.zkmaze.prover_send_answer(question)
                    verifier.zkmaze.verifier_receive_answer(prover.id, answer)
                    verifier.zkmaze.estimate_position_agent(prover.id)
                    messages_a.append([question, prover.id, answer])
                else:
                    messages_a.append([])
            for adv in range(len(self.world.adversaries)):
                prover = self.world.adversaries[adv]
                question = verifier.zkmaze.verifier_send_question(prover.id)
                answer = prover.strategy.prover_send_answer(question)
                verifier.zkmaze.verifier_receive_answer(prover.id, answer)
                verifier.zkmaze.estimate_position_agent(prover.id)
                messages_a.append([question, prover.id, answer])
            messages.append(messages_a)
        for i in range(len(self.world.adversaries)):
            verifier = self.world.adversaries[i]
            messages_a = []
            for j in range(len(self.world.agents)):
                prover = self.world.agents[j]
                question = verifier.strategy.verifier_send_question(prover.id)
                answer = prover.zkmaze.prover_send_answer(question)
                verifier.strategy.verifier_receive_answer(prover.id, answer)
                messages_a.append([question, prover.id, answer])
            messages.append(messages_a)
        return messages

    def estimate_position_agent(self, id, positions):
        """
        Estimate the position of the agent
        :param id: Id of the agent
        """
        if id in self.estimated_positions:
            new_positions = self.reduce_position_uncertainty(id, positions)
            self.estimated_positions[id] = new_positions
        else:
            self.estimated_positions[id] = positions

    def reduce_position_uncertainty(self, id, new_estimation):
        """
        Reduce the uncertainty on the estimated positions
        :param id: id of the agent
        :param new_estimation: new positions estimated
        :return: List of positions
        """
        positions = []
        previous_estimation = self.estimated_positions[id]
        for pe in previous_estimation:
            for ne in new_estimation:
                previous_cell = self.world.maze.cell_at(pe[0], pe[1])
                new_cell = self.world.maze.cell_at(ne[0], ne[1])
                if previous_cell.wall_between(new_cell) is not None:
                    if not previous_cell.wall_between(new_cell) and ne not in positions:
                        positions.append(ne)
                if previous_cell == new_cell:
                    positions.append(ne)
        return positions

    def get_estimated_agent_positions(self):
        """
        Return all the expected positions for every agent
        :return: list of expected positions
        """
        expected_positions = {}
        for a in self.world.agents:
            if a.id in self.stats.estimated_position:
                expected_positions[a.id] = self.stats.estimated_position[a.id][self.stats.index-1]
        return expected_positions

    def deduce_goal(self):
        goals = []
        no_goals = []
        for a in self.world.agents:
            if self.stats.index > 1:
                if self.stats.estimated_position[a.id][self.stats.index-1] == self.stats.estimated_position[a.id][self.stats.index-2]:
                    goals += self.stats.estimated_position[a.id][self.stats.index-1]
                    break
                else:
                  if len(self.stats.estimated_position[a.id][self.stats.index-2]) == 1:
                    no_goals += self.stats.estimated_position[a.id][self.stats.index-2]
        return goals, no_goals

    def save_maze(self, file_name):
        """
        Save the maze in a Pickle file
        :param file_name: name of the file
        """
        save = Save(self.world.maze, self.mdp)
        with open(file_name, 'wb') as handle:
            pickle.dump(save, handle)

    def load_maze(self, file_name):
        """
        Load a maze from a Pickle file
        :param file_name: name of the file
        """
        with open(file_name, "rb") as handle:
            save = pickle.load(handle)
            maze = save.maze
            mdp = save.mdp
        self.world.maze = maze
        self.mdp = mdp

    def save_replay(self, file_name):
        """
        Save the replay in a Pickle file
        :param file_name: name of the file
        """
        with open(file_name, 'wb') as handle:
            pickle.dump(self.replay, handle)

    def load_replay(self, file_name):
        """
        Load a maze from a Pickle file
        :param file_name: name of the file
        """
        with open(file_name, "rb") as handle:
            self.replay = pickle.load(handle)
        self.world.maze = self.replay.maze
        self.world.agents = self.replay.agents
        self.world.adversaries = self.replay.adversaries
        self.stats = Statistics(len(self.world.agents), len(self.world.adversaries))
        self.mdp = self.calculate_policies()
        self.distances = self.mdp.value_iteration(1, self.world.maze.end)[1]

    def checkEnd(self):
        end = True
        for a in self.world.agents:
            if a.position != self.world.get_end():
                end = False
        self.end = end