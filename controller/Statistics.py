from model.World import World

from ZK.Cycle import Cycle


class Statistics:
    """
    Class containing all the statistics on a scenario.
    """
    def __init__(self, nb_agents, nb_adversaries):
        """
        Initializing the class
        """
        self.nb_agents = nb_agents
        self.nb_adversaries = nb_adversaries

        # Messages statistics
        self.messages_x = []
        self.messages_y = []
        self.messages_z = []

        self.messages_adv_x = []
        self.messages_adv_y = []
        self.messages_adv_z = []

        # Uncertainty statistics
        self.index = 0
        self.estimated_position = {}

        # Acceptation rates
        self.accepted = []
        self.rejected = []

        # Distances
        self.distances = {}

    def update_messages(self, world, messages):
        for i in range(len(messages)):
            for m in messages[i]:
                if m:
                    self.update_statistic(world, m)
                    self.update_uncertainty(world, m)
                    self.update_accepted_rates(world, m)
        # for m in messages:
        #     self.update_statistic(world, m)
        #     self.update_uncertainty(world, m)
        #     self.update_accepted_rates(world, m)
        self.index += 1

    def update_statistic(self, world: World, m: Cycle):
        if m[1] < len(world.agents):
            self.messages_x.append(m[0][0])
            self.messages_y.append(m[0][1])
            self.messages_z.append(m[2])
        else:
            self.messages_adv_x.append(m[0][0])
            self.messages_adv_y.append(m[0][1])
            self.messages_adv_z.append(m[2])
        # if m.id_agent < len(world.agents):
        #     self.messages_x.append(m.question.x[0])
        #     self.messages_y.append(m.question.x[1])
        #     self.messages_z.append(m.question.c)
        # else:
        #     self.messages_adv_x.append(m.question.x[0])
        #     self.messages_adv_y.append(m.question.x[1])
        #     self.messages_adv_z.append(m.question.c)

    def update_uncertainty(self, world: World, m):
        id = m[1]
        if id in self.estimated_position:
            if len(self.estimated_position[id]) < self.index+1:
                self.estimated_position[id].append([])
        else:
            self.estimated_position[id] = [[]]
        verifier = world.agents[0]
        position_possible = verifier.zkmaze.get_position_possible(m[2], m[0])
        if self.index == 0:
            self.estimated_position[id][self.index] += position_possible
        else:
            estimated_positions = self.reduce_position_uncertainty(world, id, position_possible)
            for ep in estimated_positions:
                if ep not in self.estimated_position[id][self.index]:
                    self.estimated_position[id][self.index] += [ep]
        # if m.id_agent > self.nb_agents:
        #     return
        # verifier = world.agents[m.id_agent]
        # position_possible = []
        # policy = verifier.pomdp.mdp.get_policy(m.question.x)
        # if m.id_agent in self.estimated_position:
        #     if len(self.estimated_position[m.id_agent]) < self.index + 1:
        #         self.estimated_position[m.id_agent].append([])
        # else:
        #     self.estimated_position[m.id_agent] = [[]]
        #     for j in range(len(policy)):
        #         for i in range(len(policy[j])):
        #             self.estimated_position[m.id_agent][self.index].append([i, j])
        # if m.b:
        #     policy = verifier.pomdp.mdp.get_policy(m.question.x)
        #     for j in range(len(policy)):
        #         for i in range(len(policy[j])):
        #             if policy[j][i] == m.question.c:
        #                 position_possible.append([i, j])
        # else:
        #     position_possible = []
        #     for j in range(len(policy)):
        #         for i in range(len(policy[j])):
        #             position_possible.append([i, j])
        # position_possible = self.reduce_position_uncertainty(world, m.id_agent, position_possible)
        # for ep in position_possible:
        #     if ep not in self.estimated_position[m.id_agent][self.index]:
        #         self.estimated_position[m.id_agent][self.index] += [ep]

    def update_accepted_rates(self, world: World, m):
        if len(self.accepted) < len(world.agents)+len(world.adversaries):
            for i in range(len(world.agents)):
                self.accepted.append(0)
                self.rejected.append(0)
            for i in range(len(world.adversaries)):
                self.accepted.append(0)
                self.rejected.append(0)
        id = m[1]
        verifier = world.agents[0]
        position_possible = verifier.zkmaze.get_position_possible(m[2], m[0])
        if id < len(self.accepted):
            if position_possible:
                self.accepted[id] += 1
            else:
                self.rejected[id] += 1
        else:
            if position_possible:
                self.accepted[id - 100 + len(world.agents)] += 1
            else:
                self.rejected[id - 100 + len(world.agents)] += 1
        # if len(self.accepted) < (self.nb_agents+self.nb_adversaries):
        #     for i in range(self.nb_agents+self.nb_adversaries):
        #         self.accepted.append(0)
        #         self.rejected.append(0)
        # for id_agent in m.answer.keys():
        #     if id_agent < len(self.accepted):
        #         if m.b == m.answer[id_agent].b:
        #             self.accepted[id_agent] += 1
        #         else:
        #             self.rejected[id_agent] += 1
        #     else:
        #         if m.b == m.answer[id_agent].b:
        #             self.accepted[id_agent - 100 + self.nb_agents] += 1
        #         else:
        #             self.rejected[id_agent - 100 + self.nb_agents] += 1

    def update_distances(self, agent, distance):
        """
        Update the distances fron the goal
        :param agent: agent to update
        :param distance: distance
        """
        if agent in self.distances:
            self.distances[agent].append(distance)
        else:
            self.distances[agent] = [distance]

    def reduce_position_uncertainty(self, world, id, new_estimation):
        """
        Reduce the uncertainty on the estimated positions
        :param id: id of the agent
        :param new_estimation: new positions estimated
        :return: List of positions
        """
        positions = []
        previous_estimation = self.estimated_position[id][self.index-1]
        for pe in previous_estimation:
            for ne in new_estimation:
                previous_cell = world.agents[0].pomdp.maze.cell_at(pe[0], pe[1])
                new_cell = world.agents[0].pomdp.maze.cell_at(ne[0], ne[1])
                if previous_cell.wall_between(new_cell) is not None:
                    if not previous_cell.wall_between(new_cell) and ne not in positions:
                        positions.append(ne)
                if previous_cell == new_cell:
                    positions.append(ne)
        # if self.index == 1:
        #     return new_estimation
        return positions