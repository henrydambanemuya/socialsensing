sc_matrix_file = 'SCMatrix_Test1.txt'
source_claim_matrix = {}    #{source_id : [claim_id]}
source_si_matrix = {}       #{source_id : si}
claim_ztj_matrix = {}       #{claim_id : ztj}
claim_atj_map = {}          #{claim_id : atj}
claim_btj_map = {}          #{claim_id : btj}
source_ai_map = {}          #{source_id : ai}
source_bi_map = {}          #{source_id : bi}
source_num_claims_map = {}  #{source_id : number of claims reported by source}
claims_list = []            #[all claim_ids including duplicates]
distinct_claims_list = []   #[distinct claim ids]
sources_list = []           #[distinct source ids]
d = 0.5                     #probability that a randomly chosen claim is true
n = 0                       #total number of claims

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
                claim_atj_map[a] = 0
                claim_btj_map[a] = 0
                claim_ztj_matrix[a] = 0
                source_num_claims_map[a] = 0
    for claim in claims_list:
        if claim not in distinct_claims_list:
            distinct_claims_list.append(claim)
    global n 
    n = len(distinct_claims_list)
    populate() 
    sc_matrix.close() 

def populate():
    populate_source_claims_list_matrix()
    populate_source_claims_count_map()
    populate_source_si_ai_bi_matrix() 

def populate_source_claims_list_matrix():
    with open(sc_matrix_file, "r") as sc_matrix:
        for line in sc_matrix:
            source_id, claim_id = line.partition(",")[::2]
            a,b = int(source_id),int(claim_id)
            source_claim_matrix[a].append(b)
    sc_matrix.close() 

def populate_source_claims_count_map():
    for key, value in source_claim_matrix.items():
         source_num_claims_map.update({key:len(value)})
        
def populate_source_si_ai_bi_matrix():
    for key, value in source_claim_matrix.items():
        si = source_num_claims_map[key] / n
        source_si_matrix.update({key: si})
        source_ai_map.update({key: si})
        source_bi_map.update({key: 0.5*si})

def calculate_atj():
    for claim_id_atj in distinct_claims_list:
        atj = 1.0 
        for source_id_atj in sources_list:
            ai = source_ai_map[source_id_atj]
            if claim_id_atj in source_claim_matrix[source_id_atj]:
                atj = atj * ai
            else:
                atj = atj * (1 - ai)
        claim_atj_map.update({claim_id_atj:atj})
        
def calculate_btj():       
    for claim_id_btj in distinct_claims_list:
        btj = 1.0 
        for source_id_btj in sources_list:
            bi = source_bi_map[source_id_btj]
            if claim_id_btj in source_claim_matrix[source_id_btj]:
                btj = btj * bi
            else:
                btj = btj * (1 - bi)
        claim_btj_map.update({claim_id_btj:btj})
        
def calculate_ztj():
    for claim_id_ztj in distinct_claims_list:
        atj = claim_atj_map[claim_id_ztj]
        btj = claim_btj_map[claim_id_ztj]
        ztj = atj*d / (atj*d+btj*(1-d))
        claim_ztj_matrix.update({claim_id_ztj:ztj}) 

def recalculate_variables():
    sum_of_ztj_values = 0
    for key, value in claim_ztj_matrix.items():
        sum_of_ztj_values = sum_of_ztj_values + value

    #recalculate ai
    for source_id_of_ai in sources_list:
        sum_of_ztj_values_by_source_for_ai = 0
        for claim_id_of_ai in distinct_claims_list:
            if claim_id_of_ai in source_claim_matrix[source_id_of_ai]:
                sum_of_ztj_values_by_source_for_ai += claim_ztj_matrix[claim_id_of_ai]
        ai = sum_of_ztj_values_by_source_for_ai / sum_of_ztj_values
        source_ai_map.update({source_id_of_ai:ai})
    
    #recalculate bi
    for source_id_of_bi in sources_list:
        sum_of_ztj_values_by_source_for_bi = 0
        k = source_num_claims_map[source_id_of_bi]
        for claim_id_of_bi in distinct_claims_list:
            if claim_id_of_bi in source_claim_matrix[source_id_of_bi]:
                sum_of_ztj_values_by_source_for_bi += claim_ztj_matrix[claim_id_of_bi]
        bi = (k - sum_of_ztj_values_by_source_for_bi) / (n - sum_of_ztj_values)
        source_bi_map.update({source_id_of_bi:bi})

    
    global d #recalculate d
    d = sum_of_ztj_values / n

def e_step():
    calculate_atj()
    calculate_btj()
    calculate_ztj()

def m_step():
    i = 0
    while i < 15:
        recalculate_variables()
        e_step()
        i = i+1
        
def results():
    emlResults = open('emlResults.txt', 'w', encoding='utf-8')
    for key, value in sorted(claim_ztj_matrix.items()):
        if value > 0.5:
            emlResults.write(str(key) + ": " + "1" + "\n")
        else:
            emlResults.write(str(key) + ": " + "0" + "\n")
    emlResults.close()

initialize()
e_step()
m_step()
results()

