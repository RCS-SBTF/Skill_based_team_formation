import Team
import utilities
import random
import math

def max_logit_algo(graph1, task1, N, tau):
    """
    :param graph1: graph structure passed as input
    :param task1: task contains set of skills required for the team
    :param N: No of iterations
    :param tau: smoothing factor
    :return: best team
    """
    # 1. Randomly  select  candidate  for  each  role  and  generate  a team T, set Tbest←T
    # skill_experts contains skills - set of experts possess that skill
    # example: '1401': ['12824', '9026', '8210']
    skill_experts = utilities.get_skill_experts_dict(graph1)

    # extracting only the required skills for the task
    # '245': ['1757', '2054', '8638', '13623', '5414', '3744', '12551', '8129']
    # '1240': ['11128', '7880', '4728', '13881', '11329', '1247']
    # '1177': ['1432', '7078']
    # '681': ['3748', '2793', '3463', '14144', '11128', '12449', '7880', '13613', '7744', '8294', '3655', '3800', '2041', '2563', '8970', '13623', '2191', '5596', '14912', '4076', '11977', '13457', '5784', '2141', '7115', '165', '54', '9709', '14169', '12220', '10956', '12110', '2740', '10834', '14087', '2635', '8868', '14792', '11635', '7486', '674', '14415', '13049', '6052', '4003', '4854']
    required_skills = {key: skill_experts[key] for key in skill_experts.keys() & task1}

    # form a random team T (comprising random person for each skill)
    # {'245': '12551', '1240': '11128', '1177': '7078', '681': '7744'}
    random_team = {key: random.choice(required_skills[key]) for key in required_skills.keys()}
    print("random team T", random_team)

    # team members
    # ['12551','11128','7078','7744']
    T = list(random_team.values())
    print("random team T members", T)

    # setting the randomly selected team as the best team.
    Tbest = T
    iterations = []
    costs = []
    for i in range(1, N):
        iterations.append(i)
        # 2. calculate the cost of the randomly selected team T
        costT = cost(T, graph1)

        # Randomly select a role, and replace it with a randomly selected alternative candidate, get a new teamT′
        random_skill = random.choice(list(random_team))
        print('picking random skill from Team T', random_skill)
        # find an random person for the random skill
        random_person = random.choice(required_skills[random_skill])
        print('picking random person for the random skill', random_person)

        random_team.update({random_skill: random_person})
        print('New team T"', random_team)
        T_dash = list(random_team.values())
        print('New team T" members', T_dash)

        # 3. calculate the cost of the newly selected team T"
        costTd = cost(T_dash, graph1)

        # calculate the probability
        prob = probability(costT, costTd, tau)
        r = random.uniform(0, 1)

        if r <= prob:
            T = T_dash
            if cost(T, graph1) < cost(Tbest, graph1):
                Tbest = T

        costs.append(cost(Tbest, graph1))

    return Tbest, cost(Tbest, graph1)


def probability(costT, costTd, tau):
    try:
        vt = math.exp(-costT / tau)
    except OverflowError:
        vt = math.inf if costT < 0 else 0
    try:
        vtd = math.exp(-costTd / tau)
    except OverflowError:
        vtd = math.inf if costTd < 0 else 0
    if max(vt, vtd) != 0:
        prob = vtd / max(vt, vtd)
    else:
        prob = 1
    return prob


def cost(team, graph1):
    return Team.diameter(team, graph1)