from collections import defaultdict

import networkx as nx
import matplotlib.pyplot as plt
import SimilarityMeasure
import pandas as pd

sim_solution = dict()


def getPubCount(skill_sim_sol, df_a_p_transformed, dict_p_s):  # {solution_authors:{skills}}
    df_a_list = pd.DataFrame(columns=['Author'])
    df_a_pCount = pd.DataFrame(columns=['Author', 'pub_s_Count', 'pub_Count'])
    for aut, sk in skill_sim_sol.items():
        for s in sk:
            for p in df_a_p_transformed.loc[df_a_p_transformed['Author'] == aut]['Publication'].values[0]:
                # if publication has the skill as query_skill, add the author to list
                # number of times author is added = count of their publication
                if p in dict_p_s:
                    if s in dict_p_s.get(p):
                        df_a_list.loc[len(df_a_list)] = aut

        df_a_pCount.loc[len(df_a_pCount)] = aut, \
            len(df_a_list[df_a_list.Author == aut]), \
            len(df_a_p_transformed.loc[df_a_p_transformed['Author'] == aut]['Publication'].values[0])

    print(df_a_pCount)
    return df_a_pCount


def check_skilled_pub_count(best_team, sim_sol_filtered_graph, df_pCount, problem_statement):
    # get authors with max publication
    team = set(df_pCount.query("pub_s_Count == pub_s_Count.max()")["Author"])
    best_team = best_team.union(team)
    best_team, should_process, possible_solution = continue_processing(best_team, sim_sol_filtered_graph,
                                                                       problem_statement)
    if should_process:
        return check_total_pub_count(best_team, possible_solution, sim_sol_filtered_graph,
                                     df_pCount, problem_statement)
    else:
        return best_team


def check_total_pub_count(best_team, possible_solution, sim_sol_filtered_graph, df_pCount, problem_statement):
    # get authors with max publication (1 or more)
    df_pCount = df_pCount[df_pCount['Author'].isin(possible_solution)]
    team = set(df_pCount.query("pub_Count == pub_Count.max()")["Author"])
    best_team = best_team.union(team)
    best_team, should_process, possible_solution = continue_processing(best_team, sim_sol_filtered_graph,
                                                                       problem_statement)
    if should_process:
        best_team = best_team_graph(best_team, possible_solution, sim_sol_filtered_graph, problem_statement)

    return best_team


def best_team_graph(best_team, possible_solution, sim_sol_filtered_graph, problem_statement):
    best_team = check_graph(best_team, possible_solution)
    best_team, should_process, possible_solution = continue_processing(best_team,
                                                                       sim_sol_filtered_graph, problem_statement)
    if should_process:
        return best_team_graph(best_team, possible_solution, sim_sol_filtered_graph, problem_statement)

    return best_team


def check_graph(best_team, possible_solution):
    # reading the graph file
    graph = nx.read_gml("data/dblp.gml")
    minimum = defaultdict()
    min_dist = defaultdict()
    # author_max can be 1 or more
    best_team_copy = best_team.copy()
    for author_max in best_team_copy:
        for autNode in possible_solution:
            dist = nx.shortest_path_length(graph, str(author_max), str(autNode))
            print('distance between', str(author_max), 'and', str(autNode), 'is:',
                  dist, 'path:', nx.astar_path(graph, str(author_max), str(autNode)))
            min_dist[autNode] = dist

        # check if min return list of values, then update
        minimum[min(min_dist, key=min_dist.get)] = min_dist.get(min(min_dist, key=min_dist.get))

    best_team.add(min(minimum, key=minimum.get))  # get the author with minimum distance
    return best_team


def show_mygraph(d_graph):
    pos = nx.spring_layout(d_graph)
    nx.draw_networkx(d_graph, pos)
    labels = nx.get_edge_attributes(d_graph, 'weight')
    nx.draw_networkx_edge_labels(d_graph, pos, edge_labels=labels)
    plt.show()


def filter_skills(best_team, problem_statement):
    skill_solution = set()
    # find their skills
    for aut in best_team:
        for sk in sim_solution[aut]:
            skill_solution.add(sk)

    # filter out skills for which expert isn't yet found
    return set(filter(lambda x: x not in skill_solution, problem_statement))


def continue_processing(best_team, sim_sol_filtered_graph, problem_statement):
    possible_solution = set()
    filtered_skill = filter_skills(best_team, problem_statement)
    if not filtered_skill:
        return best_team, False, possible_solution
    else:
        # find authors having these skills:
        for aut in sim_sol_filtered_graph:
            if (bool(filtered_skill & sim_sol_filtered_graph[aut])) & (aut not in best_team):
                possible_solution.add(aut)

        if len(possible_solution) == 1:
            best_team.union(possible_solution)
            filtered_skill = filter_skills(best_team, problem_statement)

        if not filtered_skill:
            return best_team, False, possible_solution
        else:
            return best_team, True, possible_solution


def adapt_solution(problem_statement, sim_sol, query_skills, df_a_p_transformed, dict_p_s):
    team = set()
    sim_score = []
    global sim_solution
    g = nx.read_gml("data/dblp.gml")
    sim_sol_total = sim_sol.copy()  # as we are removing item, during last iteration step it throws error if all removed
    for aut, sk in sim_sol_total.items():
        # pre-requisite: publication count at-least 2 & author should be part of graph network
        label_to_find = str(aut)
        pCount = len(df_a_p_transformed.loc[df_a_p_transformed['Author'] == aut, 'Publication'].iloc[0])
        if any(n[0] == label_to_find for n in g.nodes(data=True)) and pCount >= 2:
            print(f"A node with label '{label_to_find}' exists in the graph with '{pCount}' publications")
        else:
            print(f"No node with label '{label_to_find}' exists in the graph with at-least 2 publications.")
            sim_sol.pop(aut, None)
            continue

        # >> check similarity of authors':skill wrt to query:skill
        similarity = SimilarityMeasure.calculate_similarity(query_skills, sk)
        sim_score.append(similarity)
    sim_sol_filtered_graph = sim_sol.copy()
    sim_solution = sim_sol.copy()
    if sim_sol_filtered_graph:
        if len(sim_sol_filtered_graph) == 1:
            # if only 1 member is part of solution, add to team.
            return team.add(next(iter(sim_sol_filtered_graph)))
        else:
            best_team = find_best_team(sim_score, sim_sol_filtered_graph, df_a_p_transformed,
                                       dict_p_s, team, problem_statement, query_skills)
            return best_team

    return 'Unable to find team!'


def find_best_team(sim_score, sim_sol_filtered_graph, df_a_p_transformed, dict_p_s,
                   team, problem_statement, query_skills):
    if sim_score.count(sim_score[0]) == len(sim_score):
        # >> if all similarity score is equal:
        print(" >> all authors having same similarity score. ")

        # >> get publication count of respective authors
        df_pCount = getPubCount(sim_sol_filtered_graph, df_a_p_transformed, dict_p_s)

        if df_pCount.pub_s_Count.nunique() != 1:
            # >> if authors' pub count wrt skill are different
            print("Scenario 1:")
            return check_skilled_pub_count(team, sim_sol_filtered_graph, df_pCount, problem_statement)
        else:
            # >>check for alternate method to resolve: count of total publications
            if df_pCount.pub_Count.nunique() != 1:
                print("Scenario 2: ")
                return check_total_pub_count(team, sim_sol_filtered_graph, sim_sol_filtered_graph,
                                             df_pCount, problem_statement)
            else:
                print("Scenario 3: Process graph")
                return best_team_graph(team, sim_sol_filtered_graph, sim_sol_filtered_graph, problem_statement)
    else:
        max_val = max(sim_score)
        max_indices = [i for i, j in enumerate(sim_score) if j == max_val]
        print("max indices: ", max_indices)

        for index_max in max_indices:
            team.add(list(sim_sol_filtered_graph)[index_max])
        sim_score.clear()
        best_team, should_process, possible_solution = continue_processing(team, sim_sol_filtered_graph,
                                                                           problem_statement)
        if should_process:

            sim_sol_reduced = sim_sol_filtered_graph.copy()
            for key in list(sim_sol_filtered_graph):
                if key not in possible_solution:
                    sim_sol_reduced.pop(key)

            for aut, sk in sim_sol_reduced.items():
                # each have only one skill, error if multiple skill, handle it
                similarity = SimilarityMeasure.calculate_similarity(query_skills, sk)
                sim_score.append(similarity)
            best_team = find_best_team(sim_score, sim_sol_reduced, df_a_p_transformed, dict_p_s,
                                       team, problem_statement, query_skills)
            return best_team
        return best_team
