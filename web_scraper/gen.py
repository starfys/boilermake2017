import redis
import random
class MarkovBot(object):
    def __init__(self, hostname='localhost', port=6379):
        self.redis_db = redis.StrictRedis(host=hostname, port=port, db=0)
        self.max_words = 100
    def add_link(self, prev_word, new_word):
            self.redis_db.hincrby(prev_word, new_word, 1)
            self.redis_db.hincrby('FREQUENCY',prev_word, 1)

    def generate(self):
        generated_sentence = []
        prev_word = 'START_TOKEN'
        for _ in range(self.max_words):
            choice = random.randint(0, int(self.redis_db.hget('FREQUENCY', prev_word)))
            possibilities = self.redis_db.hgetall('{}'.format(prev_word))
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
mb = MarkovBot()
print(mb.generate())
