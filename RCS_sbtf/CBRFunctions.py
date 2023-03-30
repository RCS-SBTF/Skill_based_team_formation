from collections import defaultdict

import pandas as pd
import SimilarityMeasure
import UtilFunctions
import ReuseSolution
import ReviseSolution


def create_knowledge_base(d1, d2):
    # The case base is a dictionary that maps problem descriptions to solutions
    case_base = defaultdict(list)
    # Add cases to the case base
    for d in (d1, d2):  # list as many input dicts as you want here, adding the values of same keys
        for key, value in d.items():
            case_base[key].append(value)
    # print(case_base)  # result: {publication: [{problem}, {solution}], publication: [{skill}, {authors}]})
    return case_base


def problem_description(task_skills, df_skill):
    query_skills = set()
    # --convert name of skills to respective ID--
    # for skill in task_skills:
    #     query_skills.add(int(df_skill.loc[df_skill['Skill'] == skill]['sID']))
    # print("Query skill are: ", task_skills, "having id:", query_skills)

    # --convert string of skillID to integer of ID--
    for skill in task_skills:
        query_skills.add(int(skill))

    return query_skills


# Define a function to solve a problem using CBR
def solve_problem_cbr(problem_statement, case_base, dict_a_s, df_a_p_transformed, dict_p_s, df_author):
    final_team = []
    # 1: Retrieve most similar case
    UtilFunctions.print_header("Retrieving similar cases and solution")
    # >>find publications having required skills
    similar_case = SimilarityMeasure.retrieve_similar_case(problem_statement, case_base)
    print("Similar cases: ", similar_case)
    # >>get authors
    sim_case_solution = SimilarityMeasure.similar_case_solution(problem_statement, similar_case, case_base)

    # 2: Reuse the solution from similar cases to solve the current problem [{x,y}]
    UtilFunctions.print_header("Reusing similar cases to solve current problem")
    # >>get skills of suitable authors:  {author: {filtered skills wrt to query}
    skill_sim_sol = ReuseSolution.get_skill_sim_sol(sim_case_solution, problem_statement, dict_a_s)
    print(skill_sim_sol)
    # >>solution 1 - find authors to form team: who have the user specified skills (all)
    solution = ReuseSolution.find_solution(skill_sim_sol, problem_statement)
    # >>if existing authors doesn't satisfy required skills

    # 3: Revise: adapt or modify solution to better fit current problem
    if not solution:
        solution = ReviseSolution.adapt_solution(problem_statement, skill_sim_sol, problem_statement,
                                                 df_a_p_transformed, dict_p_s)

    if solution != "Unable to find team!":
        print(solution)
        for s in solution:
            final_team.append(str(s))
        # solution = UtilFunctions.find_authors_name(solution, df_author)
        # print("Best team: ", solution)
    else:
        print("Team couldn't be formed, as no authors have worked together ever.")
    # 4: Retain: store new case and solution -- not part of RCS implementation

    return final_team
