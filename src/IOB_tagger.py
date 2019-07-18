from __future__ import unicode_literals
from hazm import *
import pycrfsuite
import sys
IOB_MODEL_ADDRESS = 'resources/30BILLNER.model'
POS_MODEL_ADDRESS = 'resources/postagger.model'
def pos_tag_correct(sent):
    data = sent
    for i in range(len(sent)):
        if ("_" in sent[i][0]):
            words = sent[i][0].split('_')
            tag = sent[i][1]
            data.pop(i)
            for j in range(len(words)):
                data.insert(i+j, (words[j],tag))
    return data

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    features = [
        'bias',
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag,
        'postag[:2]=' + postag[:2],
    ]
    if i > 0:
        word_before = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.extend( [
        'bias',
        '-1:word[-3:]=' + word_before[-3:],
        '-1:word[-2:]=' + word_before[-2:],
        '-1:word.istitle=%s' % word_before.istitle(),
        '-1:word.isdigit=%s' % word_before.isdigit(),
        '-1:postag=' + postag1,
        '-1:postag[:2]=' + postag1[:2],
    ])
        
    else :
        features.append('BOS')
    
    if i < len(sent) - 1 :
        word_after = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.extend( [
        'bias',
        '+1:word[-3:]=' + word_after[-3:],
        '+1:word[-2:]=' + word_after[-2:],
        '+1:word.istitle=%s' % word_after.istitle(),
        '+1:word.isdigit=%s' % word_after.isdigit(),
        '+1:postag=' + postag1,
        '+1:postag[:2]=' + postag1[:2],
    ])
        
    else :
        features.append('EOS')
    
    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2tokens(sent):
    tokens = []
    for i in range(len(sent)) :
        tokens.append(sent[i][0])
    return tokens
jomle = ""
print(sys.argv)
for arg in sys.argv[1:]:
    jomle += arg + " "
def IOB_tagger(jomle):
    iob_tagger = pycrfsuite.Tagger()
    iob_tagger.open(IOB_MODEL_ADDRESS)
    pos_tagger = POSTagger(model=POS_MODEL_ADDRESS)
    sent = pos_tag_correct(pos_tagger.tag(word_tokenize(jomle)))
    IOB_tags = iob_tagger.tag(sent2features(sent))
    tokens = sent2tokens(sent)

    for i in range(len(tokens)):
        print( tokens[i]+ " : "+ IOB_tags[i])
