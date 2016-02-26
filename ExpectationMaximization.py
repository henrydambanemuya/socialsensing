from bisect import bisect
from random import randint
import json

sc_matrix_file = 'SCMatrix.txt'
source_claim_matrix = {}         #source_id : [claim_id] pair values
source_si_matrix = {}       #source_id : si pair values
claim_ztj_matrix = {}       #claim_id : ztj pair values
claims_list = []            #list of all claim_ids including duplicates
distinct_claims_list = []   #list of distinct claim ids
sources_list = []           #list of distinct source ids

ai = [] #probability that source reports claim to be true when claim is true
bi = [] #probability that source reports claim to be true when claim is false
d = 0.5 #probability that a randomly chosen claim is true
c = 0   #convergence indicator: 0 when ai, bi, and d do not converge. 1 = converge.
atj = 1
btj = 1
ztj = 0

def initialize():
    with open(sc_matrix_file, "r") as sc_matrix:
        for line in sc_matrix:
            source_id, claim_id = line.partition(",")[::2]
            a,b = int(source_id),int(claim_id)
            #data.insert(bisect(data, (a,1000)), (a,b))
            claims_list.append(b)
            if a not in sources_list:
                sources_list.append(a)
                source_claim_matrix[a] = []
                source_si_matrix[a] = []

def populate_source_claim_matrix():
    with open(sc_matrix_file, "r") as sc_matrix:
        for line in sc_matrix:
            source_id, claim_id = line.partition(",")[::2]
            a,b = int(source_id),int(claim_id)
            sensing_matrix[a].append(b)

def populate_source_si_matrix():
    total_claims = len(claims_list)
    for key, value in sensing_matrix.items():
        claims_by_source = len(value)
        probability_source_reports_claim = claims_by_source / total_claims
        source_si_matrix[key].append(probability_source_reports_claim)
        ai.append(probability_source_reports_claim)
        bi.append(0.5*probability_source_reports_claim)

def populate_distinct_claims_matrix():
    #populate distinct_claims_list
    for claim in claims_list:
        if claim not in distinct_claims_list:
            distinct_claims.append(claim)
    
def calculate sicj():
    for claim in distinct_claims_list():
        

#TODO: Implement Method
def calculate_sicj():
    for claim in distinct_claims_list:
        for key value in source_claim_matrix:
            
            if claim in value:
                
        1 = 1        

def calculate_atj():
    atj = 1
    for value in ai:
        if sicj == 1:
            atj *= value
        else:
            atj *= 1-value

def calculate_btj():
    btj = 1
    for value in bi:
        if sicj == 1:
            btj *= value
        else:
            btj *= 1-value

def calculate_ztj():
    for claim in distinct_claims_list:
        calculate_atj()
        calculate_btj()
        ztj = atj*d / ((atj*d) + btj * (1-d)) #calculate ztj value for claim
        claim_ztj_matrix[claim] = ztj #assign ztj value to claim in claim_ztj_matrix

def recalculate_variables():
    sum_of_ztj_values = 0
    for key value in claim_ztj_matrix.items():
        sum_of_ztj_values += value
    for value in ai:
        #update values
    for value in bi:
        #update values
    d = sum_of_ztj_values / len(distinct_claims_list)
    

def results():
    for key, value in claim_ztj_matrix.items():
        print(str(key) + ": " + str(value) + "\n")

def initial_run():
    initialize()
    populate_source_claim_matrix()
    populate_source_si_matrix()
    populate_distinct_claims_matrix()
    #results()

def iteration():
    #TODO: Implement Method
    1 = 1

initial_run()

