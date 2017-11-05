'''
Created on Sep 8, 2014

@author: Tuan
'''
import codecs

from nltk.corpus import wordnet as wn
from nltk.tree import Tree

import json as js
from main.first_pattern import match_first_pattern
from main.second_pattern import match_second_pattern
from main.third_pattern import match_third_pattern


file_to_process = 'parsed_100.data'

with codecs.open(file_to_process, 'r', 'utf-8') as file_handler:
    data = js.load(file_handler)
    counter = 0
    for synset_name in data:
        sent_tokens = data[synset_name]['tokens']
        sent_dependency = data[synset_name]['dependency']
        sent_syntactic_tree = data[synset_name]['tree']
        print '------------------------------------------------------------'
        print data[synset_name]['text']
        for sentence_index in xrange(len(sent_tokens)):
            #for each sentence
            tokens = sent_tokens[sentence_index]
            syntactic_tree = Tree.fromstring(sent_syntactic_tree[sentence_index])
            dependency = sent_dependency[sentence_index]
            print synset_name
            first_result = match_first_pattern(tokens, syntactic_tree, dependency)
            second_result = match_second_pattern(tokens, syntactic_tree, dependency)
            third_result = match_third_pattern(tokens, syntactic_tree, dependency)
            is_telic_found = False
            if first_result != []:
                is_telic_found = True
                print first_result
            if second_result != []:
                is_telic_found = True
                print second_result
            if third_result != []:
                is_telic_found = True
                print third_result
            if (is_telic_found):
                counter += 1
    print 'Number of nouns that has been found a possible telic'
    print counter