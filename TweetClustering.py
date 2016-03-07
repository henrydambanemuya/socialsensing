import json
import re
import random
from math import*

tweets_filename = 'Tweets.json'
vector_dictionary = {}      #{claim_id : claim}
vector_centroid_map = {}    #{centroid: [claim_id]
indicator = 0               

centroids = [323906397735641088,323906483584655360,323906657333682176,323907258301939713,323909308188344320,323913403460636673,324067437886713856,324117950774775809,324138055772561408,324219503401644033,324320247018573824,
324346553835868161,324372750330363904,324408472441585664,324422817565257728,324448013999304704,324785120085176320, 325059351209443329,325060324992643072,325162944931438592,325253327048822784,325337623910559745,325409910642835456,
325701934273134594,325946633986641920]

def jaccard_distance(a,b):
    intersection_cardinality = len(set.intersection(*[set(a), set(b)]))
    union_cardinality = len(set.union(*[set(a), set(b)]))
    return 1- (intersection_cardinality/float(union_cardinality))

def populate_vector_dictionary():
    with open(tweets_filename, "r") as tweets_file:
        for line in tweets_file:
            tweet = json.loads(line.strip()) 
            text = tweet['text']
            value = (re.sub(r"http\S+", "", text))
            key = tweet['id']
            vector_dictionary.update({key:value})
            
def recalculate_centroid():
    for key, value in vector_centroid_map.items():
        i = 0
        var_distance = 251
        min_centroid = 0
        
        for item in value:
            sum_distance = 0
            while i < len(value)-1:
                j_distance = jaccard_distance(vector_dictionary.get(item),vector_dictionary.get(value[i+1]))
                sum_distance += j_distance
                i = i+1
            if sum_distance < var_distance:
                var_distance = sum_distance
                min_centroid = key
        if min_centroid != key:
            key = min_centroid
            indicator = 1
            
def check_indicator():
    if indicator == 1:
        for key, value in vector_centroid_map.items():
            vector_centroid_map[key] = []
        tweet_clustering()
        recalculate_centroid()
        check_indicator()
    

def tweet_clustering():
    with open(tweets_filename, "r") as tweets_file:
        for line in tweets_file:
            j_distance = 0
            var_distance = 1.1
            min_centroid = 0
            tweet = json.loads(line.strip()) 
            if 'text' in tweet:
                text = tweet['text']
                vector = (re.sub(r"http\S+", "", text)) 
                vectorId = tweet['id']

            for key, value in vector_centroid_map.items():
                j_distance = jaccard_distance(vector_dictionary.get(key), vector)
                if j_distance < var_distance:
                    var_distance = j_distance
                    min_centroid = key
            vector_centroid_map[min_centroid].append(vectorId)
            
def initialize_v_c_map():
    for centroid in centroids:
        vector_centroid_map[centroid] = []
        

def results():
    for key, value in vector_centroid_map.items():
        print(str(key) + ": " + str(value) + "\n")
        
initialize_v_c_map()                
populate_vector_dictionary()
tweet_clustering()
recalculate_centroid()
check_indicator()
results()
