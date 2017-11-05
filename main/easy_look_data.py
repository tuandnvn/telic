'''
Created on Sep 8, 2014

@author: Tuan
'''
import codecs
import json as js
from nltk.tree import Tree

file_to_process = 'parsed_all.data'

data = {}
with codecs.open(file_to_process, 'r', 'utf-8') as file_handler:
    data = js.load(file_handler)
with codecs.open(file_to_process + '.easy', 'w', 'utf-8') as file_handler:
    for synset_name in data:
        tokens = data[synset_name]['tokens']
        dependency = data[synset_name]['dependency']
        tree = data[synset_name]['tree']
        coreference = data[synset_name]['coreference']
        text = data[synset_name]['text']
        file_handler.write('================================\n')
        file_handler.write(synset_name)
        file_handler.write('\n')
        file_handler.write('\n'.join([str(sentence_token) for sentence_token in tokens]))
        file_handler.write('\n')
        file_handler.write('\n'.join([str(sentence_tree) for sentence_tree in tree]))
        file_handler.write('\n')
        file_handler.write('\n'.join([str(Tree.fromstring(sentence_tree)) for sentence_tree in tree]))
        file_handler.write('\n')
        file_handler.write('\n'.join([str(sentence_dependency) for sentence_dependency in dependency]))
        file_handler.write('\n')
        file_handler.write(str(coreference))
        file_handler.write('\n')
        file_handler.write('\n'.join(text))
        file_handler.write('\n')
    