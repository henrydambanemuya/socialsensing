from __future__ import division

sc_matrix_file = 'SCMatrix.txt'
source_claim_matrix = {}    #source_id : [claim_id] pair values
source_si_matrix = {}       #source_id : si pair values
claim_ztj_matrix = {}       #claim_id : ztj pair values
source_ai_map = {}          #source_id : probability that source reports claim to be true when claim is true
source_bi_map = {}          #source_id : probability that source reports claim to be true when claim is false
source_num_claims_map = {}  #source_id : number of claims made by source
claims_list = []            #list of all claim_ids including duplicates
distinct_claims_list = []   #list of distinct claim ids
sources_list = []           #list of distinct source ids
i = 0                       #iteration count
d = 0.5                     #probability that a randomly chosen claim is true
atj = 1.0
btj = float(1)
ztj = float(0)

def initialize():
    with open(sc_matrix_file, "r") as sc_matrix:
        for line in sc_matrix:
            source_id, claim_id = line.partition(",")[::2]
            a,b = int(source_id),int(claim_id)
            claims_list.append(b)
            if a not in sources_list:
                sources_list.append(a)
                source_claim_matrix[a] = []
                source_si_matrix[a] = []
                source_ai_map[a] = 0
                source_bi_map[a] = 0
                source_num_claims_map[a] = 0

def populate():
    populate_source_claim_matrix()
    populate_distinct_claims_matrix()
    populate_source_num_claims_map()
    populate_source_si_matrix()
    
    
def populate_source_claim_matrix():
    with open(sc_matrix_file, "r") as sc_matrix:
        for line in sc_matrix:
            source_id, claim_id = line.partition(",")[::2]
            a,b = int(source_id),int(claim_id)
            source_claim_matrix[a].append(b)
            
def populate_distinct_claims_matrix():
    #populate distinct_claims_list
    for claim in claims_list:
        if claim not in distinct_claims_list:
            distinct_claims_list.append(claim)
    n = len(distinct_claims_list)

def populate_source_num_claims_map():
    for key, value in source_claim_matrix.items():
        source_num_claims_map.update({key:len(value)})
        
def populate_source_si_matrix():
    total_claims = len(distinct_claims_list)
    for key, value in source_claim_matrix.items():
        probability_source_reports_claim = source_num_claims_map[key] / total_claims
        source_si_matrix.update({key: probability_source_reports_claim})
        source_ai_map.update({key:probability_source_reports_claim})
        source_bi_map.update({key:0.5*probability_source_reports_claim})

#TODO: Debug function - currently dividing by zero. Possible infinite loop
def calculate_ztj():
    #calculate atj
    atj = 1.0
    for claim_id in distinct_claims_list:
        for source_id in sources_list:
            if claim_id in source_claim_matrix[source_id]:
                atj = atj * source_ai_map[source_id]
            else:
                atj = atj * (1 - source_ai_map[source_id])
          
    #calculate btj
    btj = 1.0
    for claim_id in distinct_claims_list:
        for source_id in sources_list:
            if claim_id in source_claim_matrix[source_id]:
                btj = btj*source_bi_map[source_id]
            else:
                btj = btj*(1 - source_bi_map[source_id])

    #calculate ztj
    for claim in distinct_claims_list:      
        ztj = atj*d / ((atj*d) + btj * (1-d)) #calculate ztj value for claim
        claim_ztj_matrix.update({claim:ztj}) #assign ztj value to claim in claim_ztj_matrix

def recalculate_variables():
    #calculate sum of ztj values
    sum_of_ztj_values = 0
    for key, value in claim_ztj_matrix.items():
        sum_of_ztj_values += value

    #recalculate ai
    for source_id_of_ai in sources_list:
        sum_of_ztj_values_by_source_for_ai = 0
        for claim_id_of_ai in distinct_claims_list:
            if claim_id_of_ai in source_claim_matrix[source_id_of_ai]:
                sum_of_ztj_values_by_source_for_ai += claim_ztj_matrix[claim_id]
        ai = sum_of_ztj_values_by_source_for_ai / sum_of_ztj_values
        source_ai_map.update({source_id_of_ai:ai})
    
    #recalculate bi
    for source_id_of_bi in sources_list:
        sum_of_ztj_values_by_source_for_bi = 0
        for claim_id_of_bi in distinct_claims_list:
            if claim_id_of_bi in source_claim_matrix[source_id_of_bi]:
                sum_of_ztj_values_by_source_for_bi += claim_ztj_matrix[claim_id]
        bi = (source_num_claims_map[source_id_of_bi] - sum_of_ztj_values_by_source_for_bi) / sum_of_ztj_values
        source_bi_map.update({source_id_of_bi:bi})

    #recalculate d   
    d = sum_of_ztj_values / len(distinct_claims_list)

def e_step():
    initialize()
    populate()
    calculate_ztj()

def m_step():
    while i < 15:
        recalculate_variables()
        calculate_ztj()
        i = i+1

def results():
    for key, value in claim_ztj_matrix.items():
        print(str(key) + ": " + str(value) + "\n")


initialize()
populate()
e_step()
m_step()
results()

