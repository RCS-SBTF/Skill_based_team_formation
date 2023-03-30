import pandas as pd
import numpy as np
import CBRFunctions
import SimilarityMeasure
import ReuseSolution


def skill_coverage(task_skills, solution):
    df_aut_skill = load_data('data/dblp-author-skills.txt', 'Author', 'Skill')
    df_author = load_data('data/dblp-authors.txt', 'aID', 'autName')
    df_skill = load_data('data/dblp-skills.txt', 'sID', 'Skill')
    df_a_s_transformed, dict_a_s = transform_data(df_aut_skill, 'Skill')
    task_skills_id = CBRFunctions.problem_description(task_skills, df_skill)
    # solution_id = find_authors_id(solution, df_author)
    solution_id = set()
    for s in solution:
        solution_id.add(int(s))
    skill_sim_sol = ReuseSolution.get_skill_sim_sol(solution_id, task_skills_id, dict_a_s)
    solution_skills = set()
    for k, v in skill_sim_sol.items():
        for s in v:
            solution_skills.add(s)
    sim_score = SimilarityMeasure.calculate_similarity(solution_skills, task_skills_id)

    return sim_score


def read_data():
    return load_data('data/dblp-author-publications.txt', 'Author', 'Publication'), \
        load_data('data/dblp-pubs-skills.txt', 'Publication', 'Skill'), \
        load_data('data/dblp-author-skills.txt', 'Author', 'Skill'), \
        load_data('data/dblp-skills.txt', 'sID', 'Skill'), \
        load_data('data/dblp-authors.txt', 'aID', 'autName')


def load_data(fileName, col1, col2):
    data = pd.read_csv(fileName, sep='\t', header=None, names=[col1, col2])
    return pd.DataFrame(data)


# converts the integer values to list and performs explode functionality
def to_list(df, col):
    for ind in df.index:
        cellVal = df[col][ind]
        if "," not in cellVal:
            cellVal += "," + cellVal
        df.at[ind, col] = list(map(int, cellVal.split(",")))
    return df


def explode_list(df, col):
    df_list = to_list(df, col)
    return df_list.explode(col, ignore_index=True)


def transform_data(df, col):
    print("original data:", "\n", df.head(3))
    print("\n")
    df_transform = df.copy()
    df_transform = to_list(df_transform, col)
    df_transform[col] = df_transform[col].apply(set)
    print("transformed data:", "\n", df_transform.head(3))
    print("\n")
    if {'Publication', 'Author'}.issubset(df.columns):
        dict_set = explode_list(df, col).groupby([col])['Author'].apply(
            lambda grp: set(grp.value_counts().index)).to_dict()
    elif {'Publication', 'Skill'}.issubset(df.columns):
        dict_set = df_transform.set_index('Publication')[col].to_dict()
    elif {'Author', 'Skill'}.issubset(df.columns):
        dict_set = df_transform.set_index('Author')[col].to_dict()

    return df_transform, dict_set


def print_header(title):
    print("\n")
    print("---", title, "---")
    print("\n")


def drop_null_value(df, col):
    # str(df.isnull().sum().sum()), str(df.isna().sum().sum())
    df[col].replace('', np.nan, inplace=True)
    df.dropna(subset=[col], inplace=True)


def find_authors_name(author_id, df_author):
    aut_solution = set()
    for aut in author_id:
        aut_solution.add(df_author.loc[df_author["aID"] == aut]["autName"].values[0])
    return aut_solution


def find_authors_id(authors_name, df_author):
    aut_solution = set()
    for aut in authors_name:
        aut_solution.add(df_author.loc[df_author["autName"] == aut]["aID"].values[0])
    return aut_solution
