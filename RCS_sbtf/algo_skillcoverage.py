import math
import matplotlib.pyplot as plt
import utilities
import random
import Team
import rarestfirst
from src.RCS_26 import tfs
import UtilFunctions
import CBRFunctions
import numpy as np
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
        final_team, team_cost = max_logit.max_logit_algo(graph, selected_skills, 100, 0.05)

        #team_r, team_cost_r = rarestfirst.rarestfirst(graph, selected_skills)

        team_tfs, leader_cost = tfs.tfs(graph, selected_skills, 1, 1)

        query_skills = CBRFunctions.problem_description(selected_skills, df_skill)
        final_team_cbr = CBRFunctions.solve_problem_cbr(query_skills, case_base, dict_a_s, df_a_p_transformed, dict_p_s,
                                                    df_author)

        return final_team, team_tfs, final_team_cbr

    # A list to store the number of skills
    x_values = []
    # A list to store the execution time of each algorithm
    y_values_max_logit = []
    y_values_tfs = []
    y_values_cbr = []

    # Iterate through the number of skills
    for num_skills in range(4, 12):
        x_values.append(num_skills)
        # Initialize a variable to store the total cost of 50 tasks with this number of skills
        # Perform 50 tasks with this number of skills
        max_logit_coverage = 0
        tfs_coverage = 0
        cbr_coverage = 0
        for i in range(10):
            selected_skills = random.sample(unique_skills, num_skills)
            max_logit_team, tfs_team,cbr_team = calculate_cost(selected_skills)
            print('Selected skills', selected_skills)
            # Max Logit
            print('Max Logit team', max_logit_team)
            max_logit_coverage += UtilFunctions.skill_coverage(selected_skills, max_logit_team)
            # Tfs
            tfs_team = str(tfs_team)
            pairs = tfs_team.split(":")
            print('Tfs team', pairs)
            tfs_coverage += UtilFunctions.skill_coverage(selected_skills, pairs)
            print('cbr team', cbr_team)
            cbr_coverage += UtilFunctions.skill_coverage(selected_skills, cbr_team)

        # Calculate the average cost of the 10 tasks
        print('max_logit_coverage', max_logit_coverage)
        print('tfs_coverage', tfs_coverage)
        print('cbr_coverage', cbr_coverage)
        average_cov_max_logit = max_logit_coverage/10
        average_cov_tfs = tfs_coverage/10
        average_cov_cbr = cbr_coverage/10
        y_values_max_logit.append(average_cov_max_logit )
        y_values_tfs.append(average_cov_tfs)
        y_values_cbr.append(average_cov_cbr)
        print('y_values_max_logit',y_values_max_logit)
        print('y_values_tfs', y_values_tfs)
        print('y_values_cbr',y_values_cbr)
    # Set the width of each bar
    bar_width = 0.2

    # Set the positions of the bars on the x-axis
    r1 = np.arange(len(x_values))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]

    # Create the bars
    plt.bar(r1, y_values_max_logit, width=bar_width, label='Max-Logit algorithm')
    plt.bar(r2, y_values_tfs, width=bar_width, label='TPL closest algorithm')
    plt.bar(r3, y_values_cbr, width=bar_width, label='Case-based reasoning')

    # Add xticks on the middle of the group bars
    plt.xlabel('Number of Skills')
    plt.xticks([r + bar_width for r in range(len(x_values))], x_values)

    # Add y label
    plt.ylabel('Skill coverage')

    # Create legend & Show graphic
    plt.legend()
    plt.show()








