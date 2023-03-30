import UtilFunctions
from statistics import mean

task_skills = [['2770', '4481'], ['2770', '4481']]
solution = [['3430', '17016'], ['3344', '4826', '12893']]
similarity = []
for t, s in zip(task_skills, solution):
    similarity.append(UtilFunctions.skill_coverage(t, s))

print(mean(similarity))
