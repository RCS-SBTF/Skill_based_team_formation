import math
import matplotlib.pyplot as plt
import utilities
import random
import Team
import rarestfirst
from src.RCS_26 import tfs
import UtilFunctions
import CBRFunctions
import max_logit


def master():
    import networkx as nx

    # reading the graph file
    graph = nx.read_gml("dblp.gml")
    print(graph)
    # case based reasoning
    global df_a_p, df_p_s, df_a_s, df_skill, df_author, \
        query_skills, dict_a_s, case_base

    #UtilFunctions.print_header("Load data and transform")
    df_a_p, df_p_s, df_a_s, df_skill, df_author = UtilFunctions.read_data()

    #UtilFunctions.print_header("author & publication")
    df_a_p_transformed, dict_p_a = UtilFunctions.transform_data(df_a_p, 'Publication')

    #UtilFunctions.print_header("publication & skill")
    UtilFunctions.drop_null_value(df_p_s, 'Skill')
    df_p_s_transformed, dict_p_s = UtilFunctions.transform_data(df_p_s, 'Skill')

    #UtilFunctions.print_header("author & skill")
    df_a_s_transformed, dict_a_s = UtilFunctions.transform_data(df_a_s, 'Skill')

    # Case base creation
    #UtilFunctions.print_header("Creating knowledge base")
    case_base = CBRFunctions.create_knowledge_base(dict_p_s, dict_p_a)


    # Initialize an empty set to store the unique skills
    skills_set = set()

    # Iterate through the nodes in the graph
    for node in graph.nodes():
        # Check if the node has a 'skills' attribute
        if 'skills' in graph.nodes[node]:
            # Split the skills string into a list of individual skills
            skills = graph.nodes[node]['skills'].split(',')
            # Add the skills to the skills set
            skills_set.update(skills)

    # Convert the set to a list
    unique_skills = list(skills_set)
    print(unique_skills)
    # 2493
    print(len(unique_skills))

    import random
    import matplotlib.pyplot as plt
    import time

    # A function that takes the number of skills and returns the cost using the max-logit algorithm
    def calculate_cost(selected_skills):
        # max-logit algorithm goes here
        final_team, team_cost = max_logit.max_logit_algo(graph, selected_skills, 200, 0.05)

        #team_r, team_cost_r = rarestfirst.rarestfirst(graph, selected_skills)

        team_tfs, leader_cost = tfs.tfs(graph, selected_skills, 1, 1)

        query_skills = CBRFunctions.problem_description(selected_skills, df_skill)
        final_team_cbr = CBRFunctions.solve_problem_cbr(query_skills, case_base, dict_a_s, df_a_p_transformed, dict_p_s,
                                                    df_author)

        return final_team, team_tfs,final_team_cbr

    # A list to store the number of skills
    x_values = []

    y_values_max_logit = []
    y_values_tfs = []
    y_values_cbr = []

    # Iterate through the number of skills
    for num_skills in range(4, 12):
        x_values.append(num_skills)
        # Initialize a variable to store the total cost of 50 tasks with this number of skills
        # Perform 50 tasks with this number of skills
        total_max = 0
        total_tfs = 0
        total_cbr = 0

        for i in range(10):
            selected_skills = random.sample(unique_skills, num_skills)
            max_logit_team, tfs_team,cbr_team = calculate_cost(selected_skills)

            # Max Logit
            print('Max logit team', max_logit_team)
            total_max += Team.sum_distance(max_logit_team, graph,selected_skills)
            # Tfs
            tfs_team = str(tfs_team)
            pairs = tfs_team.split(":")
            print('Tfs team', pairs)
            total_tfs += Team.sum_distance(pairs, graph, selected_skills)
            print('cbr team', cbr_team)
            total_cbr += Team.sum_distance(cbr_team, graph, selected_skills)

        # Calculate the average cost of the 10 tasks
        average_max_logit = total_max/10
        average_tfs = total_tfs/10
        average_cbr = total_cbr/10
        y_values_max_logit.append(average_max_logit)
        y_values_tfs.append(average_tfs)
        y_values_cbr.append(average_cbr)
    plt.plot(x_values, y_values_max_logit, '-o', label='Max-Logit algorithm')
    plt.plot(x_values, y_values_tfs, '-o', label='TPL closest algorithm')
    plt.plot(x_values, y_values_cbr, '-o', label='Case-based reasoning')
    # Plot the graph
    plt.xlabel('Number of Skills')
    plt.ylabel('Sum Distance of Team formed')
    plt.legend()
    plt.show()


