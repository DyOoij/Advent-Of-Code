input_file = open("input.txt", "r").readlines()

priority = '0abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'




#problem 1
TotalPrio = 0
for i in input_file:
    halfpoint = int(len(i.replace("\n", ""))/2)
    
    for item in i[:halfpoint]:
        if item in i[halfpoint:]:
            #print(item, priority.index(item) + 1)
            TotalPrio += int(priority.index(item) )
            break
            
print(TotalPrio)


#problem 2
TotalPrio2 = 0
cleanlist = []
compoundpacks = []
badgelist = []
for y in input_file:
    cleanlist.append(''.join(set(y.replace("\n", ""))))
    


for j in range(0, len(cleanlist), 3):
    compoundpacks.append(''.join(sorted(''.join(cleanlist[j : j+3]))))
    
for backpack in compoundpacks:
    for badge in backpack:
        location = backpack.index(badge)
        if backpack[location + 1] == badge and backpack[location + 2] == badge:
            badgelist.append(badge)
            break
        
for badgey in badgelist:
    TotalPrio2 += int(priority.index(badgey))
    
print (TotalPrio2)
    
        





    
    
