# -*- coding: utf-8 -*-
"""
Generates true or false questions.
"""

import random

# Finds a word with a defined antonym and switches in the sentence.
def make_false(oldsent):
    sent=oldsent[:]
    global words
    for word in sent:
        if word in words or word in special:
            if word in special:
                spec_index = sent.index(word)
                if spec_index +1 == len(sent) or sent[spec_index + 1] != 'not':
                    replace = word + ' not'
                else:
                    replace = word
                    del sent[spec_index + 1]
                sent[spec_index] = replace
                return sent
                break                    
            else:
                index_sentence = sent.index(word)
                index_words = words.index(word)
                replace =''
                if index_words%2 == 0:
                    replace = words[index_words+1]
                else:
                    replace = words[index_words-1]
                sent[index_sentence] = replace
                return sent
                break
        else:
            pass
    return ''

# Lists with special words (add not) and other anytonyms.
special = ['will', 'is', 'are', 'am', 'do', 'was', 'were', 'could', 'would', 'should', 'may' 'might', 'shall', 'did', 'does', 'must']
words = ['less', 'more', 'least', 'most',
         'lower', 'higher', 'lowest', 'highest',
         'smaller', 'bigger', 'smallest', 'biggest',
         'increase', 'decrease', 'increased', 'decreased', 'increases', 'decreases',
         'positive', 'negative', 'can', 'cannot', 'all', 'some', 'true', 'false',  
         'equal', 'unequal', 'best', 'worst', 'bad', 'good', 'with', 'without']

text = open('input.txt', 'r')
questions = []
answers = []
right_answer = []

# Determines whether a T/F question should be generated.
for line in text:
    sentence = (line.split(' '))
    sentence[-1] = sentence[-1].replace('\n', '')
    sentence_false = make_false(sentence)
    if random.choice([True, False]) == False and sentence != '':     
        if sentence_false == '':
            pass
        else:
            right_answer.append(sentence)
            questions.append(sentence_false)
            answers.append(False)
    else:
        if sentence_false =='':
            pass
        else:
            questions.append(sentence)
            answers.append(True)
            right_answer.append('')

squestions = []
sright = []

# Merges list of individual words in the question
for item in questions:
    string = ' '
    for w in item:
        string += str(w) + ' '
    string = string.strip()
    squestions.append(string)

# Merges list of individual words in the answer
for item in right_answer:
    string = ' '
    for w in item:
        string += str(w) + ' '
    string = string.strip()
    sright.append(string)

# Randomally selects questions from the given data
lsv1 = []
i = 0
while i < len(squestions):
    lsv1.append([squestions[i], answers[i], sright[i]])
    i += 1

if len(lsv1) >= 5:    
    final = random.sample(lsv1, 5)
else:
    final = random.sample(lsv1, len(lsv1))
    
for item in final:
    for thing in item:
        print(thing)    