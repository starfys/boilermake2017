#!/usr/bin/env python3
import pymongo
from pymongo import MongoClient
import re
import random
from base64 import b64encode, b64decode
b64enc = lambda string: b64encode(string.encode('utf-8')).decode('utf-8')
b64dec = lambda string: b64decode(string.encode('utf-8')).decode('utf-8')

#mongo vars
client = MongoClient('mongodb://localhost:27017')
db = client['boilermake']
collection = db['all_words']

#all words and respective data will live here
masterDict = {}

class MarkovBot(object):
    def __init__(self,hostname='localhost',port=27017):
        self.max_words = 100
        self.client = MongoClient('mongodb://{}:{}'.format(hostname, port))
        self.db = self.client['boilermake']
        self.collection = self.db['all_words']
        self.s = self.db.collection
        self.masterDict = {}


    #InsertToMasterDict: takes a list of tuples into nested dictionaries in self.masterDict.
    def insert_to_master_dict(self,listOfTuples):
        for tup in listOfTuples:
            tup = (b64enc(tup[0]),b64enc(tup[1]))
            if tup[0] not in self.masterDict:
                self.masterDict[tup[0]] = {tup[1]:1}
            else:
                if tup[1] not in self.masterDict[tup[0]]:
                    self.masterDict[tup[0]][tup[1]] = 1
                else:
                    self.masterDict[tup[0]][tup[1]] += 1
            if 'SUM' in self.masterDict[tup[0]]:
                self.masterDict[tup[0]]['SUM'] += 1 
            else:
                self.masterDict[tup[0]]['SUM'] = 1

    #PushToMongo: puts self.masterDict onto database
    def push_to_mongo(self):
        item = self.masterDict
        self.collection.insert_one(item)
    #clear database
    def delete_all_mongo(self):
        self.collection.delete_many({})

    def generate(self):
        generated_sentence = []
        prev_word = b64enc('START_TOKEN')
        for _ in range(self.max_words):
            choice = random.randint(0, self.collection.find_one()[prev_word]['SUM'])
        
            possibilities = self.collection.find_one()[prev_word]
            for new_word, freq in possibilities.items():
                if new_word == 'SUM':
                    continue
                choice -= freq
                if choice <= 0:
                    break
            if new_word == b64enc('END_TOKEN'):
                break
            new_word = b64dec(new_word)
            generated_sentence.append(new_word)
            prev_word = b64enc(new_word)
        return ' '.join(generated_sentence)


if __name__ == '__main__':
    #open data
    import json
    with open('hackathon_desc.json','r') as hj:
        hackathon_desc = json.load(hj)

    m = MarkovBot()
    m.delete_all_mongo()
    m.insert_to_master_dict(hackathon_desc)
    m.push_to_mongo()
    print(m.generate())
