from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import bigrams
from collections import Counter
import string
import operator
import json
import re


ps = PorterStemmer()

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', '#rt', '#follow', 'via', 'donald', 'trump', '…', "trump's",
                                                   'new']
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=True): #what does "lowercase=True" do?
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else ps.stem(token.lower()) for token in tokens]
    return tokens

def summarize():
    fname = 'Tweets.json'
    with open(fname, 'r') as f:
        count_all = Counter()
        count_hash = Counter()
        count_mention = Counter()
        count_bigram = Counter()
        for line in f:
            try:
                tweet = json.loads(line)
                # Create a list with all the terms
                terms_stop = [term for term in preprocess(tweet['text']) if term not in stop and not term.startswith(('#', '@'))]                # Create a list with all hashtags
                # Create a list with all hashtags
                terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#') and term not in stop]
                # Create a list with all mentions
                terms_mention = [term for term in preprocess(tweet['text']) if term.startswith('@') and term not in stop]
                #Create a list of term sequences. Depth = 2
                terms_bigram = bigrams(terms_stop)
                # Update counters
                count_all.update(terms_stop)
                count_hash.update(terms_hash)
                count_mention.update(terms_mention)
                count_bigram.update(terms_bigram)
                
            except BaseException as e:
                continue
            
        # Print the 12 most frequent words
        print("Frequent Terms:")
        print(count_all.most_common(12))
        print("\n Frequent Hashtags:")
        print(count_hash.most_common(12))
        print(" \n Frequent Mentions:")
        print(count_mention.most_common(12))
        print(" \n Frequent Bigrams:")
        print(count_bigram.most_common(12))
            
summarize()
        
            
