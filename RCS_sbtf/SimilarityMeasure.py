
def calculate_similarity(query, case):
    intersection = len(query.intersection(case))
    union = (len(query) + len(case)) - intersection
    sim = float(intersection) / union
    return sim


# Define a function to retrieve the similar cases from the case base
def retrieve_similar_case(query, case_base):
    similar_cases = set()
    for caseID, case_description in case_base.items():
        # Calculate the similarity between the problem description and the case description
        if calculate_similarity(query, case_description[0]) > 0:
            similar_cases.add(caseID)
    # Return the similar cases
    return similar_cases


# Define a function to adapt the solution of a similar case to the current problem
def similar_case_solution(problem_description, similar_cases, case_base):
    solution = set()
    # Retrieve the solution(Authors) for the similar case(skills)
    for similar_case in similar_cases:
        if len(case_base[similar_case]) > 1: # some case doesn't have authors!!!skip
            for item in case_base[similar_case][1]: # from case base{skill,author} get author as [1]
                solution.add(item)

    print("For the problem(skills): '{}', solution(authors): {}".format(problem_description, solution))
    return solution
