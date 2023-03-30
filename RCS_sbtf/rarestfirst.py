def rarestfirst(l_graph, l_task):
    """
    returns team of experts with minimum diameter distance
    :param l_graph:
    :param l_task:
    :return tuple(set, dictionary, string):
    """
    from Teamr import Teamr
    import networkx as nx
    from tqdm import tqdm
    import utilities
    l_skill_expert = utilities.get_skill_experts_dict(l_graph)
    rare_skills_support = [min([(len(l_skill_expert[l_skill]), l_skill) for l_skill in l_task], key=lambda x: x[0])]
    # print(rare_skills_support)    # print rarest skill support and skill
    rare_skills = [l_skill for count, l_skill in rare_skills_support]
    min_dd = 100  # minimum diameter distance
    best_team = Teamr()
    for rare_skill in tqdm(rare_skills, total=len(rare_skills)):
        for candidate in tqdm(l_skill_expert[rare_skill], total=len(l_skill_expert[rare_skill])):
            team = Teamr()
            for skill in l_task:
                team.task.add(skill)
            team.leader = candidate
            team.experts.add(candidate)
            if candidate not in team.expert_skills:
                team.expert_skills[candidate] = list()
                team.expert_skills[candidate].append(rare_skill)
            else:
                team.expert_skills[candidate].append(rare_skill)
            for l_skill in l_task:
                if l_skill != rare_skill:
                    closest_expert = ""
                    min_distance = 100
                    for expert in l_skill_expert[l_skill]:
                        if expert in l_graph and candidate in l_graph and nx.has_path(l_graph, candidate, expert):
                            distance = nx.dijkstra_path_length(l_graph, candidate, expert, weight="cc")
                            if min_distance > distance:
                                min_distance = distance
                                closest_expert = (expert + ".")[:-1]
                    if len(closest_expert) > 0:
                        team.experts.add(closest_expert)
                        if closest_expert in team.expert_skills:
                            team.expert_skills[closest_expert].append(l_skill)
                        else:
                            team.expert_skills[closest_expert] = list()
                            team.expert_skills[closest_expert].append(l_skill)
            # print(team)
            if team.is_formed():
                dd = team.diameter(l_graph)
                if dd is not None:
                    if min_dd > dd:
                        min_dd = dd
                        best_team = team
    return best_team, min_dd
