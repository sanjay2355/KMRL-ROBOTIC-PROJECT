import random
with open('wikisent2.txt','r') as source:
    data = [ (random.random(), line) for line in source ]
data.sort()
with open('sample1.txt','w') as target:
    for _, line in data:
        target.write( line )