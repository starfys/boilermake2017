import redis
import json
from bs4 import BeautifulSoup as bsoup
import pickle
import re
from os import listdir
import random
html_parser='lxml'
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


def clean_header(header):
    header = ' '.join(map(lambda s: s.capitalize, header.split('_')))
class MarkovBot(object):
    def __init__(self, hostname='localhost', port=6379):
        self.redis_db = redis.StrictRedis(host=hostname, port=port, db=0)
        self.max_words = 1000
    def add_link(self, prev_word, new_word):
            self.redis_db.hincrby(prev_word, new_word, 1)
            self.redis_db.hincrby('FREQUENCY',prev_word, 1)

    def generate(self, prev_word = 'START_TOKEN', length=100):
        self.max_words=length
        generated_sentence = []
        prev_word = 'START_TOKEN'
        for _ in range(self.max_words):
            try:
                choice = random.randint(0, int(self.redis_db.hget('FREQUENCY', prev_word)))
            except:
                prev_word = 'START_TOKEN'
                continue
            possibilities = self.redis_db.hgetall('{}'.format(prev_word))
            for new_word, value in possibilities.items():
                choice -= int(value.decode('utf-8'))
                if choice <= 0:
                    break
            new_word = new_word.decode('utf-8')
            if new_word in headers.values():
                prev_word = 'START_TOKEN'
                continue
            if new_word == 'END_TOKEN':
                break
            generated_sentence.append(new_word)
            prev_word = new_word
        return ' '.join(generated_sentence)
    def reset(self):
        self.redis_db.flushall()
    def reset_title(self):
        for title_key in self.redis_db.keys('TITLE_*'):
            self.redis_db.delete(title_key)
    def train_model(self):
        for i, json_file in enumerate(listdir('data')):
            print(i)
            try:
                hackathon = json.load(open('data/'+json_file,'r'))
            except:
                print('failed to open')
                continue
            for project in hackathon:
                description = bsoup(re.sub(r'</span>', '    </span>',project[1]), html_parser).text.lower()
                for key, replacement in headers.items():
                    description = description.replace(key, replacement) 
                words = re.split(r'[ \n\t]+', description)[1:]
                for word in words:
                    self.add_link(prev_word,word)
                    prev_word = word
    def generate_project(self):
        desc = ''
        for header in ['INSPIRATION', 'MOTIVATION', 'WHAT_IT_DOES', 'HOW_WE_BUILT_IT', 'CHALLENGES_WE_RAN_INTO', 'ACCOMPLISHMENTS', 'WHAT_WE_LEARNED','WHATS_NEXT_FOR']:
            desc += "<h2>{}</h2>\n<p>{}</p>\n".format(header, self.generate(header))
        return desc
    def generate_title(self, max_letters=20):
        generated_title = ''
        prev_letter = 'TITLE_START'
        for i in range(max_letters):
            try:
                choice = random.randint(0, int(self.redis_db.hget('FREQUENCY', prev_letter)))
            except:
                prev_letter = 'TITLE_START'
                continue
            possibilities = self.redis_db.hgetall(prev_letter)
            for new_letter, value in possibilities.items():
                choice -= int(value.decode('utf-8'))
                if choice <= 0:
                    break
            new_letter = new_letter.decode('utf-8')
            if new_letter == 'TITLE_END':
                if i < 10:
                    new_letter = 'TITLE_ '
                else:
                    break
            generated_title += new_letter.split('_')[1]
            prev_letter = new_letter
        if generated_title.rstrip() == '':
            generated_title = self.generate_title()
        return generated_title
    def train_title(self):
        for i, json_file in enumerate(listdir('data')):
            print(i)
            try:
                hackathon = json.load(open('data/'+json_file,'r'))
            except:
                print('failed to open')
                continue
            for project in hackathon:
                title = project[0]
                prev_letter = 'TITLE_START'
                for letter in [title[i:i+2] for i in range(0,len(title),2)]:
                    letter = 'TITLE_{}'.format(letter)
                    self.add_link(prev_letter,letter)
                    prev_letter = letter
                self.add_link(prev_letter, 'TITLE_END')
