from markov import MarkovBot
import random

with open('devpost_project.htm','r') as devpost_temp_file:
    template = devpost_temp_file.read()
mb = MarkovBot()
desc = mb.generate_project()
title = mb.generate_title()
with open('myproject.html','w') as output_file:
    output_file.write(template.replace('INSERT_TITLE_HERE',title).replace('INSERT_DESCRIPTION_HERE',desc).replace('INSERT_LIKES_HERE',str(random.randint(1,100))))
