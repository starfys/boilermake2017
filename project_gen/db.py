import pymongo
from pymongo import MongoClient
import pprint

from base64 import b64encode, b64decode
b64enc = lambda string: b64encode(string.encode('utf-8')).decode('utf-8')
b64dec = lambda string: b64decode(string.encode('utf-8')).decode('utf-8')

#connect to current client
client = MongoClient('mongodb://localhost:27017')

#create database
db = client['boilermake']

#create collection
collection = db['all_words']

#all words and respective data will live here
masterDict = {}

def ShowValues():
    pprint.pprint(db.collection.find_one())

#InsertToMasterDict: takes a list of tuples into nested dictionaries in masterDict.
def InsertToMasterDict(listOfTuples):
    for tup in listOfTuples:
        tup = (b64enc(tup[0]),b64enc(tup[1]))
        if tup[0] not in masterDict:
            masterDict[tup[0]] = {tup[1]:1}
        else:
            if tup[1] not in masterDict[tup[0]]:
                masterDict[tup[0]][tup[1]] = 1
            else:
                masterDict[tup[0]][tup[1]] += 1
        if 'SUM' in masterDict[tup[0]]:
            masterDict[tup[0]]['SUM'] += 1 
        else:
            masterDict[tup[0]]['SUM'] = 1

#PushToMongo: puts masterDict onto database
def PushToMongo():
    item = masterDict
    db.collection.insert_one(item)

def DeleteAllMongo():
    db.collection.delete_many({})

#open data
import json
with open('hackathon_desc.json','r') as hj:
    hackathon_desc = json.load(hj)

#reset server
DeleteAllMongo()

#data to server
InsertToMasterDict(hackathon_desc)
PushToMongo()

#ShowValues()
