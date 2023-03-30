from collections import defaultdict
import UtilFunctions
import CBRFunctions


def cbr_master(selected_team):
    global df_a_p, df_p_s, df_a_s, df_skill, df_author, \
        query_skills, dict_a_s, case_base

    UtilFunctions.print_header("Load data and transform")
    df_a_p, df_p_s, df_a_s, df_skill, df_author = UtilFunctions.read_data()

    UtilFunctions.print_header("author & publication")
    df_a_p_transformed, dict_p_a = UtilFunctions.transform_data(df_a_p, 'Publication')

    UtilFunctions.print_header("publication & skill")
    UtilFunctions.drop_null_value(df_p_s, 'Skill')
    df_p_s_transformed, dict_p_s = UtilFunctions.transform_data(df_p_s, 'Skill')

    UtilFunctions.print_header("author & skill")
    df_a_s_transformed, dict_a_s = UtilFunctions.transform_data(df_a_s, 'Skill')

    # Case base creation
    UtilFunctions.print_header("Creating knowledge base")
    case_base = CBRFunctions.create_knowledge_base(dict_p_s, dict_p_a)

    # Problem description
    UtilFunctions.print_header("Query skills")

    # task_skills = ['4882', '3379', '2890', '1815']
    # task_skill as set of ID
    query_skills = CBRFunctions.problem_description(selected_team, df_skill)

    # solve above problem
    UtilFunctions.print_header("solving query team skills by CBR")
    final_team = CBRFunctions.solve_problem_cbr(query_skills, case_base, dict_a_s, df_a_p_transformed, dict_p_s, df_author)
    print("Best team:", final_team)
    return final_team







