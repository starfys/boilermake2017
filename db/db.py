import pymongo
from pymongo import MongoClient

#connect to current client
client = MongoClient('mongodb://localhost:27017')

#create database
db = client['boilermake']

#create collection
collection = db['all_words']

#recieve input list
inputList = [('a',1),('a',2),('b',1),('c',1)]

masterDict = {}

for tup in inputList:
    if tup[0] not in masterDict:
        masterDict[tup[0]] = {tup[1]:1}
    else:
        masterDict[tup[0]][tup[1]] += 1

print(masterDict)

'''

#initialize word
word = 'testhereyay'

post = {word:{'the':7,'and':2,'four':4}}

words = db.collection
post_id = words.insert_one(post).inserted_id
'''
