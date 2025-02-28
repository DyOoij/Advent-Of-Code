input_file = open("input.txt", "r").readlines()

#problem 1
pairs = []
counter = 0
nonoverlapping = 0

for i in input_file:
    pairs.append(i.replace("\n", ""))

for j in pairs:
    listedvals = []
    rangesL = []
    rangesR = []
    
    
    for k in j.split(","):
        for p in k.split("-"):
            listedvals.append(p)
    
    for rangeL in range(int(listedvals[0]), int(listedvals[1]) + 1):
        rangesL.append(rangeL)
    for rangeR in range(int(listedvals[2]), int(listedvals[3]) + 1):
        rangesR.append(rangeR)
    allvalues = set(rangesL + rangesR)

    if len(rangesL) == len(allvalues) or len(rangesR) == len(allvalues):
        counter += 1
        
    if len(rangesL) + len(rangesR) == len(allvalues):
        nonoverlapping += 1
        
        
print(counter)
print(len(pairs) - nonoverlapping)
        



    
    
