from bisect import bisect
from random import randint
import json

sc_matrix_file = 'SCMatrix.txt'
sensing_matrix = {}
si_values = {}
claims_list = []
sources_list = []

def initialize():
    with open(sc_matrix_file, "r") as sc_matrix:
        for line in sc_matrix:
            source_id, claim_id = line.partition(",")[::2]
            a,b = int(source_id),int(claim_id)
            #data.insert(bisect(data, (a,1000)), (a,b))
            claims_list.append(b)
            if a not in sources_list:
                sources_list.append(a)
                sensing_matrix[a] = []
                si_values[a] = []

def populate_sensing_matrix():
    with open(sc_matrix_file, "r") as sc_matrix:
        for line in sc_matrix:
            source_id, claim_id = line.partition(",")[::2]
            a,b = int(source_id),int(claim_id)
            sensing_matrix[a].append(b)

def populate_si_values():
    total_claims = len(claims_list)
    print(total_claims)
    for key, value in sensing_matrix.items():
        claims_by_source = len(value)
        probability_source_reports_claim = claims_by_source / total_claims
        si_values[key].append(probability_source_reports_claim)    

def populate_lists():
    populate_sensing_matrix()
    populate_si_values()

def results():
    for key, value in si_values.items():
        print(str(key) + ": " + str(value) + "\n")    

initialize()
populate_lists()
#results()
