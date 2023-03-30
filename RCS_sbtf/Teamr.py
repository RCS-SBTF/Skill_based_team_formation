class Teamr:

    def __init__(self):
        self.experts = set()
        self.expert_skills = dict()  # dictionary of list of skills representing by an expert to the Team
        self.leader = ""
        self.task = set()
        self.random_experts = set()

    def get_detailed_record(self):
        pass

    def is_formed(self):
        all_skills = set()
        for expert in self.expert_skills:
            all_skills.update(set(self.expert_skills[expert]))
        return len(all_skills) == len(self.task)

    def __str__(self):  # real signature unknown
        """ Return str(self). """
        if len(self.experts) == 0:
            return "Team Not Yet Formed"
        else:
            return ":".join(self.experts)

    def clean_it(self):
        self.experts = set()
        self.expert_skills = dict()  # dictionary of list of skills representing by an expert to the Team
        self.leader = ""
        self.task = set()
        self.random_experts = set()

    def cardinality(self):
        return len(self.experts)

    def get_leader_team_graph(self, l_graph):
        """
        return graph formed by team
        :param l_graph:
        :return:
        """
        nodes = set()
        nodes.add(self.leader)
        import networkx as nx
        for nd1 in self.experts:
            if nd1 != self.leader:
                if nx.has_path(l_graph, nd1, self.leader):
                    for node in nx.dijkstra_path(l_graph, nd1, self.leader):
                        nodes.add(node)
        return l_graph.subgraph(nodes).copy()

    def get_team_graph(self, l_graph):
        """
        return graph formed by team
        :param l_graph:
        :return:
        """
        nodes = set()
        nodes.add(self.leader)
        import networkx as nx
        for nd1 in self.experts:
            for nd2 in self.experts:
                if nd1 != nd2:
                    if nx.has_path(l_graph, nd1, nd2):
                        for node in nx.dijkstra_path(l_graph, nd1, nd2):
                            nodes.add(node)
        return l_graph.subgraph(nodes).copy()

    def diameter(self, l_graph) -> float:
        """
        return diameter of graph formed by team
        diam(X) := max{sp_{X}(u,v) | u,v ∈ X}.
        :param l_graph:
        :return:
        """
        import networkx as nx
        t_graph = self.get_team_graph(l_graph)
        if nx.number_of_nodes(t_graph) < 2:
            return 0
        else:
            sp = dict()
            for nd in t_graph.nodes:
                sp[nd] = nx.single_source_dijkstra_path_length(t_graph, nd)
            e = nx.eccentricity(t_graph, sp=sp)
            return round(nx.diameter(t_graph, e), 2)

    def radius(self, l_graph) -> float:
        """
        return diameter of graph formed by team
        :param l_graph:
        :return:
        """
        import networkx as nx
        import matplotlib.pyplot as plt
        t_graph = self.get_team_graph(l_graph)
        if nx.number_of_nodes(t_graph) < 2:
            return 0
        else:
            shp = dict()
            for nd in t_graph.nodes:
                shp[nd] = nx.single_source_dijkstra_path_length(t_graph, nd)
            try:
                eccent = nx.eccentricity(t_graph, sp=shp)
            except TypeError as eccent:
                nx.draw_circular(t_graph, with_labels=True)
                plt.show()
                msg = "Found infinite path length because the graph is not" " connected"
                raise nx.NetworkXError(msg) from eccent
            return round(nx.radius(t_graph, eccent), 2)

    def sum_distance(self, l_graph, task) -> float:
        """
        returns sum of pair wise skills distance of task
        :param l_graph:
        :param task:
        :return:
        """
        import networkx as nx
        # from Team import Team
        sd = 0
        expert_i = expert_j = ""
        for skill_i in task:
            for skill_j in task:
                if skill_i != skill_j:
                    for member in self.experts:
                        if member in self.expert_skills and skill_i in self.expert_skills[member]:
                            expert_i = member
                        if member in self.expert_skills and skill_j in self.expert_skills[member]:
                            expert_j = member
                    if expert_i in l_graph and expert_j in l_graph and nx.has_path(l_graph, expert_i, expert_j):
                        sd += nx.dijkstra_path_length(l_graph, expert_i, expert_j, weight="cc")
        sd /= 2
        return round(sd, 3)

    def leader_skill_distance(self, l_graph, l_task) -> float:
        """
        return leader skill distance of team i.e. (skills of leader, skill responsible team_member) pairs
        :param l_graph:
        :param l_task:
        :return:
        """
        import networkx as nx
        # from Team import Team
        ld = 0
        if len(self.experts) < 2:
            return 0
        else:
            for skill in l_task:
                for member in self.experts:
                    if member != self.leader and skill in self.expert_skills[member]:
                        if nx.has_path(l_graph, self.leader, member):
                            ld += nx.dijkstra_path_length(l_graph, self.leader, member, weight="cc")
        return round(ld, 3)

    def leader_distance(self, l_graph) -> float:
        """
        return leader distance of team i.e. (leader, team_member) pairs
        :param l_graph:
        :return:
        """
        import networkx as nx
        ld = 0
        if len(self.experts) < 2:
            return 0
        else:
            for member in self.experts:
                if member != self.leader:
                    if nx.has_path(l_graph, self.leader, member):
                        ld += nx.dijkstra_path_length(l_graph, self.leader, member, weight="cc")
        return round(ld, 3)

    def shannon_team_diversity(self, l_graph):
        """
        returns Shannon entropy
        :param l_graph:
        :return:
        """
        import math
        shannon_sum = 0
        tot_skls = set()
        for expert in self.experts:
            tot_skls.update(set(l_graph.nodes[expert]["skills"].split(",")))
        for skill in tot_skls:
            cn = 0
            for expert in self.experts:
                if skill in l_graph.nodes[expert]["skills"].split(","):
                    cn += 1
            prob = cn / len(self.experts)
            shannon_sum += prob * math.log(prob)
        return round(((-1 * shannon_sum) / len(tot_skls)), 5)

    def shannon_task_diversity(self, l_graph):
        """
        returns Shannon entropy
        :param l_graph:
        :return:
        """
        import math
        shannon_sum = 0
        for skill in self.task:
            cn = 0
            for expert in self.experts:
                if skill in l_graph.nodes[expert]["skills"].split(","):
                    cn += 1
            prob = cn / len(self.experts)
            shannon_sum += (prob * math.log(prob))
        return round(((-1 * shannon_sum) / len(self.task)), 5)

    def simpson_task_density(self, l_graph):
        """
        calculates reciprocal simpson diversity
        :return:
        """
        simpson_sum = 0
        for skill in self.task:
            cn = 0
            for expert in self.experts:
                if skill in l_graph.nodes[expert]["skills"].split(","):
                    cn += 1
            prob = cn / len(self.experts)
            simpson_sum += pow(prob, 5)
        return round(simpson_sum / len(self.task), 5)

    def simpson_team_density(self, l_graph):
        """
        calculates reciprocal simpson diversity
        :return:
        """
        simpson_sum = 0
        tot_skls = set()
        for node in self.experts:
            tot_skls.update(set(l_graph.nodes[node]["skills"].split(",")))
        for skill in tot_skls:
            cn = 0
            for expert in self.experts:
                if skill in l_graph.nodes[expert]["skills"].split(","):
                    cn += 1
            prob = cn / len(self.experts)
            simpson_sum += pow(prob, 5)
        return round(simpson_sum / len(tot_skls), 5)

    def simpson_diversity(self, l_graph, bool_team):
        if self.simpson_team_density(l_graph) == 0 or self.simpson_task_density(l_graph) == 0 :
            return 100000  # infinity
        else:
            if bool_team:
                return round(1 / (self.simpson_team_density(l_graph)), 5)
            else:
                return round(1 / (self.simpson_task_density(l_graph)), 5)

    def gini_simpson_diversity(self, l_graph, bool_team):
        if self.simpson_team_density(l_graph) == 0 or self.simpson_task_density(l_graph) == 0 :
            return 100000  # infinity
        else:
            if bool_team:
                return round(1 - (self.simpson_team_density(l_graph)), 5)
            else:
                return round(1 - (self.simpson_task_density(l_graph)), 5)


def similarity_teams():
    year = "2015"
    network = "vldb"
    algori1 = "rfs"
    algori2 = "bsd"
    with open("../dblp-" + year + "/" + network + "-17-tasks-0-" + algori1 + "-teams.txt", "r") as file1, \
            open("../dblp-" + year + "/" + network + "-17-tasks-0-" + algori2 + "-teams.txt", "r") as file2:
        for line1, line2 in zip(file1, file2):
            experts1 = set(line1.strip("\n").split(","))
            experts2 = set(line2.strip("\n").split(","))
            print(",".join(sorted(experts2.intersection(experts1))) + " | " +
                  ",".join(sorted(experts1.difference(experts2))) + " | " +
                  ",".join(sorted(experts2.difference(experts1))))
            print(str(len(experts2.intersection(experts1))) + " | " +
                  str(len(experts1.difference(experts2))) + " | " +
                  str(len(experts2.difference(experts1))))


if __name__ == "__main__":
    year = "2015"
    network = "vldb"
    import networkx as nx

    graph = nx.read_gml("../dblp-" + year + "/" + network + ".gml")
    from Team import Team

    team = Team()
    print(team.get_diameter_nodes(graph))
    # print("memory required in bytes : " + str(team.__sizeof__()))  # sizeof
    # print("memory required in bytes with overhead : " + str(sys.getsizeof(team)))  # sizeof with overhead
    # print("string " + team.__str__())
    # print("cardinality " + str(team.cardinality()))
