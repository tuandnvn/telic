'''
Created on Sep 7, 2014

@author: Tuan
'''
from nltk.corpus import wordnet as wn
import json as js
from nltk import FreqDist
import codecs

synset_dict = {}
freqDist = FreqDist()
for t in wn.all_synsets(pos=wn.NOUN):
    if t.lexname() == 'noun.artifact':
        freq = 0
        for lemma in t.lemmas():
            freq += lemma.count()
        synset_dict[t.name()] = freq
        if (freq > 10):
            print t
            print freq
            freqDist[t.name()]= freq

print freqDist.most_common(100)
with codecs.open("artifact.txt", 'w', 'utf-8') as file_handler:
    js.dump( synset_dict, file_handler)

