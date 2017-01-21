import json
from bs4 import BeautifulSoup as bsoup
import pickle
import re

with open('hackathon_data.pickle','rb') as hackathon_data_file:
    hackathon_data = pickle.load(hackathon_data_file)


headers = {
        'inspiration':'INSPIRATION',
        'motivation':'MOTIVATION',
        'what it does':'WHAT_IT_DOES',
        'how we built it':'HOW_WE_BUILT_IT',
        'challenges we ran into':'CHALLENGES_WE_RAN_INTO',
        'accomplishments that we\'re proud of':'ACCOMPLISHMENTS',
        'what we learned':'WHAT_WE_LEARNED',
        'what\'s next for':'WHATS_NEXT_FOR',
        'built with':'BUILT_WITH',
        'try it out':'TRY_IT_OUT'
}


"""
import re
import redis
import random
class MarkovBot(object):
    def __init__(self, hostname='localhost', port=6379):
        self.redis_db = redis.StrictRedis(host=hostname, port=port, db=0)
        self.max_words = 100

    def add(self, sentence):
        sentence.append('END_TOKEN')
        prev_word = 'START_TOKEN'
        for new_word in sentence:
            #Add new_word as a new subentry of user_id_prev_word
            self.redis_db.hincrby(prev_word, new_word, 1)
            self.redis_db.incrby("{}_FREQUENCY".format(prev_word), 1)
            prev_word = new_word

    def generate(self):
        generated_sentence = []
        prev_word = 'START_TOKEN'
        for _ in range(self.max_words):
            choice = random.randint(0, int(self.redis_db.get('{}_FREQUENCY'.format(prev_word))))
            possibilities = self.redis_db.hgetall(prev_word)
            for new_word, value in possibilities.items():
                choice -= int(value.decode('utf-8'))
                if choice <= 0:
                    break
            new_word = new_word.decode('utf-8')
            if new_word == 'END_TOKEN':
                break
            generated_sentence.append(new_word)
            prev_word = new_word
        return ' '.join(generated_sentence)

markov_bot = MarkovBot()
"""
hackathon_tuples = []
def insert_into_model(prev_word, word):
    hackathon_tuples.append((prev_word, word))
html_parser = 'lxml'
for url, hackathon in list(hackathon_data.items()):
    for project in hackathon:
        description = bsoup(re.sub(r'</span>', '    </span>',project[1]), html_parser).text.lower()
        for key, replacement in headers.items():
            description = description.replace(key, replacement) 
        words = re.split(r'[ \n\t]+', description)[1:]
        prev_word = 'START_TOKEN'
        for word in words:
            insert_into_model(prev_word, word)
            prev_word = word
        hackathon_tuples.append((word, 'END_TOKEN'))

"""
for _ in range(20):
    print('========='*20)
    print(markov_bot.generate())
"""
