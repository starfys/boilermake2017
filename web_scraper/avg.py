import sys

numbers = list(map(lambda line: int(line.rstrip()), sys.stdin.readlines()))
print(sum(numbers)/len(numbers))
print(len(numbers))
