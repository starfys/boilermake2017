#!/usr/bin/env python3
import pymongo
from pymongo import MongoClient
import re
import random

client = MongoClient('mongodb://localhost:27017')
db = client['boilermake']
collection = db['all_words']
s = db.collection

max_words = 100

def generate():
    generated_sentence = []
    prev_word = 'START_TOKEN'
    for _ in range(max_words):
        choice = random.randint(0, s.find_one()[prev_word]['SUM'])
        
        possibilities = s.find_one()[prev_word]
        for new_word, freq in possibilities.items():
            if new_word == 'SUM':
                continue
            choice -= freq
            if choice <= 0:
                break
        if new_word == 'END_TOKEN':
            break
        generated_sentence.append(new_word)
        prev_word = new_word
    return ' '.join(generated_sentence)

print(generate())
