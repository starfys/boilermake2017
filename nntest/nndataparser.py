import NeuralNetwork
from collections import OrderedDict
import random

print("###################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#######################")



allUniqueWords = []

with open('test.out', 'r') as f:
	data = f.read()
f.closed

words = data.split(" ")
for word in words:
	word = word.replace(chr(0),'')
	if(not (word in allUniqueWords)):
		allUniqueWords.append(word)
		
	
MAX_VAL = len(allUniqueWords) - 1
MIN_VAL = 0

random.seed(0)	
nn = NeuralNetwork.NeuralNetwork(2,0,1,[],[])

i = 0

while(i < len(words) - 3):
	firstWord = -1
	secondWord = -1
	thirdWord = -1
	
	for wordIndex in range(len(allUniqueWords)):
		if(words[i] == allUniqueWords[wordIndex]):
			firstWord = wordIndex
		if(words[i+1] == allUniqueWords[wordIndex]):
			secondWord = wordIndex
		if(words[i+2] == allUniqueWords[wordIndex]):
			thirdWord = wordIndex
	
	if(firstWord == -1):
		firstWord = random.randint(0,MAX_VAL)
	if(secondWord == -1):
		secondWord = random.randint(0,MAX_VAL)
	if(thirdWord == -1):
		thirdWord = random.randint(0,MAX_VAL)
	
	
	#print(firstWord,secondWord,thirdWord)
	#print("------------------------")
		
	firstWord = nn.normalize(firstWord,0,MAX_VAL,0,1)
	secondWord = nn.normalize(secondWord,0,MAX_VAL,0,1)
	thirdWord = nn.normalize(thirdWord,0,MAX_VAL,0,1)
	#print(firstWord,secondWord,thirdWord)
	#print(firstWord,secondWord,thirdWord)
	nn.train([firstWord,secondWord],[thirdWord],0.1,0.1)
	
	i += 1
	

nn.processInput([0.5718,0.005319])
'''print(allUniqueWords[int(nn.deNormalize(0.5718,0,MAX_VAL))])
print(allUniqueWords[int(nn.deNormalize(0.005319,0,MAX_VAL))])
print(allUniqueWords[int(nn.deNormalize(nn.outNodes[0],0,MAX_VAL))])'''

firstWord = 0.005319
secondWord = nn.outNodes[0]
thirdWord = 0
print(allUniqueWords[int(nn.deNormalize(firstWord,0,MAX_VAL))])
print(allUniqueWords[int(nn.deNormalize(secondWord,0,MAX_VAL))])
for i in range(100):
	#print(firstWord,secondWord,thirdWord)
	#print(allUniqueWords[int(nn.deNormalize(firstWord,0,MAX_VAL))]
	#,allUniqueWords[int(nn.deNormalize(secondWord,0,MAX_VAL))],
	#allUniqueWords[int(nn.deNormalize(thirdWord,0,MAX_VAL))])
	
	nn.processInput([firstWord,secondWord])
	thirdWord = nn.outNodes[0]
	firstWord = secondWord
	secondWord = thirdWord
	
	translatedFirstWord = allUniqueWords[int(nn.deNormalize(firstWord,0,MAX_VAL))]
	translatedSecondWord = allUniqueWords[int(nn.deNormalize(secondWord,0,MAX_VAL))]
	translatedThirdWord = translatedSecondWord
	
	if(translatedFirstWord == translatedSecondWord):
		secondWord = random.uniform(0,1)
	else:
		print(translatedThirdWord)