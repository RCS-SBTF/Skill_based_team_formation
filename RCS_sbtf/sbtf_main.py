import algo_sumdistance, algo_processingtime, algo_skillcoverage, algo_diameterdistance, algo, tfs, team_cbr
import networkx as nx
import pandas as pd
import utilities
import max_logit

if __name__ == '__main__':
    choice = input("Enter the selection: 1)Team formation 2)Graph generation")
    print('choice is', choice)
    if choice == '1':
        selected_skills = ['data', 'mining', 'neural', 'networks']
        print('selected_skills', selected_skills)
        selected_ids = utilities.problem_description(selected_skills)
        print('selected_ids', selected_ids)
        # selected_ids = ["4372", "3213", "2273"]
        graph = nx.read_gml("dblp.gml")
        print('Max-Logit algorithm')
        final_team, team_cost = max_logit.max_logit_algo(graph, selected_ids, 100, 0.05)
        
        print('TPLC algorithm')
        team_tpl, leader_cost1 = tfs.tfs(graph, selected_ids, 1, 1)
        team_tpl = str(team_tpl)
        pairs = team_tpl.split(":")
        print('TPLC team', pairs)

        print('TPLR algorithm')
        team_tpr, leader_cost2 = tfs.tfr(graph, selected_ids, 1, 1)
        team_tpr = str(team_tpr)
        pairs1 = team_tpr.split(":")
        print('TPLR team', pairs1)

        print('CBR algorithm')
        final_team_cbr = team_cbr.cbr_master(selected_ids)
        print('Execution completed')
        print('Max-Logit team:', final_team)
        print(utilities.get_author_name_from_label(graph,final_team))
        print('TPLR team:', pairs)
        print(utilities.get_author_name_from_label(graph, pairs))
        print('TPLC team:', pairs1)
        print(utilities.get_author_name_from_label(graph, pairs1))
        print('CBR team:', final_team_cbr)
        print(utilities.get_author_name_from_label(graph, final_team_cbr))
    elif choice == '2':
        print('Processing time')
        algo_processingtime.master()

        print('Sum distance')
        algo_sumdistance.master()

        print('skill coverage')
        algo_skillcoverage.master()

        print('Diameter distance')
        algo_diameterdistance.master()
    else:
        print('Please select 1 or 2')

