import json
from bs4 import BeautifulSoup as bsoup
import pickle
import re
from os import listdir


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


hackathon_tuples = []
def insert_into_model(prev_word, word):
    hackathon_tuples.append((prev_word, word))

html_parser = 'lxml'

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
        prev_word = 'START_TOKEN'
        for word in words:
            insert_into_model(prev_word, word)
            prev_word = word
        hackathon_tuples.append((word, 'END_TOKEN'))
with open('hackathon_master.pickle','wb') as hackmaster:
    pickle.dump(hackathon_tuples, hackmaster)


