input_file = open("input.txt", "r").readlines()

refracdata = []
crateset = []
cratedict = {}
secondset = {}
instructions = []


for i in input_file:
    refracdata.append(i.replace("\n",""))
    
for j in refracdata:
    if j == "":
        break
    else:
        crateset.append(j)
                
for k in crateset[-1]:
    stack = []
    if k != " ":
        rowloc = crateset[-1].index(k)
        
        for lineofcrates in crateset[:-1]:
            if lineofcrates[rowloc] != " ":
                stack.append(lineofcrates[rowloc])
        stack.append(crateset[-1][rowloc])
        stack.reverse()
        
        cratedict[stack[0]] = stack[1:]
        secondset[stack[0]] = stack[1:]

for t in refracdata:
    if len(t) > 0:
        if t[0] == 'm':
            instructions.append(t)



#problem 1
for y in instructions:
    amount = int(y.split(" ")[1])
    locfrom = y.split(" ")[3]
    locto = y.split(" ")[5]
    
    for cycle in range(amount):
        collectcrate = cratedict[locfrom][-1]
        del cratedict[locfrom][-1]
        cratedict[locto].append(collectcrate)
        

for i in cratedict:
    print(cratedict[i][-1], end = "")
print()



#problem 2

for q in instructions:
    amount = int(q.split(" ")[1])
    locfrom = q.split(" ")[3]
    locto = q.split(" ")[5]
    


    
    collectedcrates = secondset[locfrom][-amount:]

    del secondset[locfrom][-amount:]
    secondset[locto] += collectedcrates
    
for h in secondset:
    print(secondset[h][-1], end = "")
print()    

       




        
        
        



    
    
