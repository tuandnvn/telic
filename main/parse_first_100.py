'''
Created on Sep 7, 2014

@author: Tuan
'''
import codecs
import re

from nltk.corpus import wordnet as wn

import json as js
from stanford_client import StanfordNLP


nlp = StanfordNLP()
def try_first_100():
    first_100_list = [(u'house.n.01', 157), (u'room.n.01', 116), (u'door.n.01', 98), (u'road.n.01', 96), (u'surface.n.01', 90), (u'car.n.01', 89), (u'street.n.01', 86), (u'wall.n.01', 82), (u'work.n.02', 76), (u'rifle.n.01', 75), (u'window.n.01', 72), (u'gun.n.01', 72), (u'cell.n.01', 71), (u'plant.n.01', 68), (u'anode.n.01', 66), (u'office.n.01', 62), (u'dwelling.n.01', 61), (u'church.n.02', 59), (u'shelter.n.01', 56), (u'merchandise.n.01', 56), (u'bed.n.01', 51), (u'building.n.01', 50), (u'art.n.01', 49), (u'farm.n.01', 49), (u'ship.n.01', 49), (u'equipment.n.01', 48), (u'doorway.n.01', 48), (u'apparel.n.01', 44), (u'kitchen.n.01', 43), (u'system.n.01', 43), (u'stairs.n.01', 42), (u'fabric.n.01', 41), (u'hotel.n.01', 39), (u'floor.n.01', 39), (u'bullet.n.01', 39), (u'facility.n.01', 38), (u'painting.n.01', 37), (u'device.n.01', 36), (u'thing.n.04', 36), (u'ball.n.01', 35), (u'chair.n.01', 35), (u'phonograph_record.n.01', 34), (u'shop.n.01', 34), (u'weapon.n.01', 34), (u'fence.n.01', 34), (u'roof.n.01', 34), (u'picture.n.01', 33), (u'machine.n.01', 33), (u'artillery.n.01', 33), (u'apartment.n.01', 32), (u'product.n.02', 31), (u'telephone.n.01', 31), (u'flag.n.01', 31), (u'hallway.n.01', 30), (u'drug.n.01', 30), (u'tube.n.01', 30), (u'hat.n.01', 30), (u'coat.n.01', 29), (u'block.n.01', 29), (u'part.n.02', 28), (u'bottle.n.01', 28), (u'basement.n.01', 27), (u'shoe.n.01', 27), (u'blanket.n.01', 27), (u'thing.n.08', 26), (u'hospital.n.01', 26), (u'airplane.n.01', 26), (u'box.n.01', 25), (u'table.n.02', 25), (u'structure.n.01', 25), (u'train.n.01', 25), (u'desk.n.01', 24), (u'wagon.n.01', 24), (u'apparatus.n.01', 24), (u'station.n.01', 23), (u'floor.n.02', 23), (u'holder.n.01', 23), (u'instrument.n.01', 23), (u'light.n.02', 23), (u'piece.n.01', 23), (u'anteroom.n.01', 22), (u'bedroom.n.01', 22), (u'barn.n.01', 22), (u'factory.n.01', 22), (u'pocket.n.01', 21), (u'component.n.03', 21), (u'lab.n.01', 21), (u'porch.n.01', 21), (u'camp.n.01', 20), (u'shot.n.02', 20), (u'truck.n.01', 20), (u'photograph.n.01', 20), (u'living_room.n.01', 19), (u'camera.n.01', 18), (u'book.n.02', 18), (u'gate.n.01', 18), (u'uniform.n.01', 18), (u'sketch.n.01', 17), (u'yard.n.02', 17), (u'tent.n.01', 17)]
    parsed = {}
    for synset in first_100_list:
        print '--------------------------------------'
        print synset[0]
        s = wn.synset(synset[0])
        definition = s.definition()
        definition = str(s.lemma_names()[0]) + " is " + re.sub("\\(.+\\)", "", definition)
        result = nlp.parse(definition)
        parsed[synset[0]] = result
    
    with codecs.open("parsed_100.data", 'w', 'utf-8') as file_handler:
        js.dump(parsed, file_handler)
        
try_first_100()
