import pymongo
from pymongo import MongoClient
import pprint

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


#for testing
l = [('START_TOKEN','word'),('START_TOKEN','word2'),('START_TOKEN','the'),('START_TOKEN','and'),('START_TOKEN','seven'),('and','word'),('the','and'),('seven','word'),('seven','the'),('seven','word2'),('word','the'),('word2','the'),('word','and'),('word','and'),('word','seven'),('word','seven'),('word','seven'),('word','seven'),('word','seven'),('word','seven'),('word','seven'),('word','seven'),('word','seven')]

DeleteAllMongo()

InsertToMasterDict(l)
PushToMongo()

ShowValues()
