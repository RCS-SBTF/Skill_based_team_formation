import SimilarityMeasure


def is_skill_in_query(skills, query_skills):
    filtered_skill = set()
    for s in skills:
        if s in query_skills:
            filtered_skill.add(s)
    return filtered_skill


def get_skill_sim_sol(sim_case_solution, query_skills, dict_a_s):
    dict_a_s_transformed = {}
    for aut in sim_case_solution:
        dict_a_s_transformed[aut] = is_skill_in_query(dict_a_s[aut], query_skills)
    return dict_a_s_transformed


def find_solution(skill_sim_sol, query_skills):
    # if any user having all query skills
    team = set()
    for aut, sk in skill_sim_sol.items():
        if SimilarityMeasure.calculate_similarity(query_skills, sk) == 1:
            team.add(aut)
    return team



