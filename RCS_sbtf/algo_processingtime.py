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
        start_time = time.time()
        final_team, team_cost = max_logit.max_logit_algo(graph, selected_skills, 100, 0.05)
        end_time = time.time()
        max_logit_time = end_time - start_time


        start_time = time.time()
        team_tfs, leader_cost = tfs.tfs(graph, selected_skills, 1, 1)
        end_time = time.time()
        tfs_time = end_time - start_time

        start_time = time.time()
        query_skills = CBRFunctions.problem_description(selected_skills, df_skill)
        final_team_cbr = CBRFunctions.solve_problem_cbr(query_skills, case_base, dict_a_s, df_a_p_transformed, dict_p_s,
                                                    df_author)
        print('cbr',final_team_cbr)
        end_time = time.time()
        cbr_time = end_time - start_time

        return max_logit_time, tfs_time, cbr_time

    # A list to store the number of skills
    x_values = []

    y_values_max_logit = []
    y_values_tfs = []
    y_values_cbr = []

    # Iterate through the number of skills
    for num_skills in range(4, 12):
        x_values.append(num_skills)
        # Initialize a variable to store the total cost of 50 tasks with this number of skills
        total_time_max_logit = 0
        total_time_tfs = 0
        total_time_cbr = 0
        # Perform 50 tasks with this number of skills
        for i in range(10):
            selected_skills = random.sample(unique_skills, num_skills)
            max_logit_time, tfs_time,cbr_time = calculate_cost(selected_skills)
            total_time_max_logit += max_logit_time
            total_time_tfs += tfs_time
            total_time_cbr += cbr_time
        # Calculate the average cost of the 10 tasks
        average_time_max_logit = total_time_max_logit / 10
        average_time_tfs = total_time_tfs / 10
        average_time_cbr = total_time_cbr / 10
        y_values_max_logit.append(average_time_max_logit)
        y_values_tfs.append(average_time_tfs)
        y_values_cbr.append(average_time_cbr)
    plt.plot(x_values, y_values_max_logit, '-o', label='Max-Logit algorithm')
    plt.plot(x_values, y_values_tfs, '-o', label='TPL closest algorithm')
    plt.plot(x_values, y_values_cbr, '-o', label='Case-based reasoning')
    # Plot the graph
    plt.xlabel('Number of Skills')
    plt.ylabel('Processing time')
    plt.legend()
    plt.show()


