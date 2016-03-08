from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import json
import string
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

def preprocess(s, lowercase=True): #what does lowercase=True do?
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else ps.stem(token.lower()) for token in tokens]
    return tokens

def normalize_text():
    with open('Tweets.json', 'r') as f:
        for line in f:
            try:
                tweet = json.loads(line) # load it as Python dict
                tokens = preprocess(tweet['text'])
                print([w for w in tokens if not w in stop])
            except BaseException as e:
                continue

normalize_text()
