'''
Created on Sep 8, 2014

@author: Tuan
'''
import codecs
from pprint import pprint
import re

from nltk.corpus import wordnet as wn

import json as js
from jsonrpc import RPCTransportError
from stanford_client import StanfordNLP


nlp = StanfordNLP()
def parse_all():
    parsed = {}
    with codecs.open("artifact.txt", 'r', 'utf-8') as file_handler:
        all_list = js.load(file_handler)
   
        for synset in all_list:
            try:
                print '--------------------------------------'
                print synset
                s = wn.synset(synset)
                definition = s.definition()
                definition = str(s.lemma_names()[0]) + " is " + re.sub("\\(.+\\)", "", definition)
                result = nlp.parse(definition)
                parsed[synset] = result
            except RPCTransportError:
                continue
        
    with codecs.open("parsed_all.data", 'w', 'utf-8') as file_handler:
        js.dump(parsed, file_handler)
        
parse_all()
