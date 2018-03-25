# -*- coding: utf-8 -*-
"""
Generates fill in the blank questions based on NLTK.
"""

import random
import re
from textblob import TextBlob

def read_text(filename):
    with open(filename) as f:
        lines = f.readlines()
        return ' '.join(lines)

def replaceIC(word, sentence):
    if len(word) > 3:
        insensitive_hippo = re.compile(re.escape(word), re.IGNORECASE)
        return insensitive_hippo.sub('__________________', sentence)
    else:
        pass

def removeWord(sentence, poss):
    words = None
    if 'NNP' in poss:
        words = poss['NNP']
    elif 'NN' in poss:
        words = poss['NN']
    else:
        return (None, sentence, None)
    if len(words) > 0:
        word = random.choice(words)
        replaced = replaceIC(word, sentence)
        return (word, sentence, replaced)
    else:
        return (None, sentence, None)

text = read_text('input.txt')
text_blob = TextBlob(text)
sposs = {}

for sentence in text_blob.sentences:
    poss = {}
    sposs[sentence.string] = poss;
    for t in sentence.tags:
        tag = t[1]
        if tag not in poss:
            poss[tag] = []
        poss[tag].append(t[0])


QandA = []
for sentence in sposs.keys():
    poss = sposs[sentence]
    (word, osentence, replaced) = removeWord(sentence, poss)
    if replaced is None:
        pass
    else:
        QandA.append([replaced, word])

if len(QandA) >= 5:    
    final = random.sample(QandA, 5)
else:
    final = random.sample(QandA, len(QandA))
    
for item in final:
    for thing in item:
        print(thing)  
        