import random
import re

from textblob import TextBlob

def read_text(filename):
    with open(filename) as f:
        lines = f.readlines()
        return ' '.join(lines)

def replaceIC(word, sentence):
    insensitive_hippo = re.compile(re.escape(word), re.IGNORECASE)
    return insensitive_hippo.sub('__________________', sentence)

def removeWord(sentence, poss):
    words = None
    if 'NNP' in poss:
        words = poss['NNP']
    elif 'NN' in poss:
        words = poss['NN']
    else:
        print("NN and NNP not found")
        return (None, sentence, None)
    if len(words) > 0:
        word = random.choice(words)
        replaced = replaceIC(word, sentence)
        return (word, sentence, replaced)
    else:
        print("words are empty")
        return (None, sentence, None)

text = read_text('ww2.txt')
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

for sentence in sposs.keys():
    poss = sposs[sentence]
    (word, osentence, replaced) = removeWord(sentence, poss)
    if replaced is None:
        print ("Founded none for ")
        print(sentence)
    else:
        print(replaced)
        print ("\n===============")
        print(word)
        print ("===============")
        print("\n")