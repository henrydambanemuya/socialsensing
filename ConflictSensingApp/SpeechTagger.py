from nltk.tokenize import word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import state_union
import nltk
import json
import re

train_text = state_union.raw('2005-GWBush.txt')
inputFile = 'data.json'
outputFile = 'sample_text.txt'

custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
tokenized = custom_sent_tokenizer.tokenize(outputFile)

def createInput():
    
    with open(inputFile, 'r') as i:
        with open(outputFile, 'w') as o:
            for line in i:
                try:
                    tweet = json.loads(line)
                    text = tweet['text']
                    o.write(' '.join(re.sub("(RT)|(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split()))
                    #o.write('\n')
                except BaseException as e:
                    continue

def tagInput():
    try:
        with open(outputFile, 'r') as f:
            for line in f:
                words = nltk.word_tokenize(line)
                tagged = nltk.pos_tag(words)
                print(tagged)
    except Exception as e:
        print(str(e))

createInput()
tagInput()
        
            
