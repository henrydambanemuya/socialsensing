#Python Interface Implementation of Stanford Log-Linear Part-Of-Speech Tagger

import nltk
import numpy
from nltk.corpus import treebank

sentence = "At eight o'clock on Thursday morning, Arthur didn't feel very good"

tokens = nltk.word_tokenize(sentence)

tagged = nltk.pos_tag(tokens)

entities = nltk.chunk.ne_chunk(tagged)

print(entities)

#TODO: Figure out how to implement tree function
##t = treebank.parsed_sents('wsj_0001.mrg')[0]
##
##t.draw()

#Citation: Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.



