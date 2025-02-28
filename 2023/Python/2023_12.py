from datetime import datetime
from collections import Counter


print("Start of script: ", str(datetime.now()).split(" ")[1][:-7])

input_file = open("input.txt", "r").readlines()

clean_data = []

for i in input_file:
    j = i.replace('\n','').split(' ')
    clean_data.append([j[0],j[1]])



def CreateAllVariations(Line): #clean_data > [ i[0] ]
    #Create all the possible variations of the line
    Variations = Line
    VariReturn = []
    

    for Variation_Line in Variations:
        ItemsInVar = len(Variations)
        for char_i in range(len(Variation_Line)):
            if Variation_Line[char_i] == '?':
                #Look, buddy, pal, friendo, friend
                #This is not pretty, it's not efficient, it's just not your best work
                #But here's the thing
                #It works
                #You have the computing power and it works
                #So go to sleep
                LineToUpdate1, LineToUpdate2 = list(Variation_Line).copy(), list(Variation_Line).copy()
                LineToUpdate1[char_i], LineToUpdate2[char_i] = '#', '.'
                for UpdatedLine in [LineToUpdate1, LineToUpdate2]:
                    Variations.append(UpdatedLine)
                break
    
 
    for Var_i in range(len(Variations)):
        #This cleans up the list and removes all non-complete sequences
        #It's hackey as fuck, and you could optimise by removing updated sequences from the initial list
        #But again, you have enough RAM, let it sweat for a bit
        if '?' in Variations[Var_i]:
            pass
        else:
            AddString = ''
            for char in Variations[Var_i]:
                AddString += char
            VariReturn.append(AddString)
      
    return VariReturn

def CheckAgainstReq(ListOfSprings, Req):
    ValidConfigs = 0
    RestructReq = []
    
    for j in Req.split(','):
        if j.isnumeric():
            RestructReq.append(int(j))
            
    for Spring in ListOfSprings:
        OnlyBroken = []
        Chopped = Spring.split(".")

        for Entry in Chopped:
            if Entry != '':
                OnlyBroken.append(len(Entry))
    
        if OnlyBroken == RestructReq:
            ValidConfigs += 1
    
    return ValidConfigs
        
        

            
    
Total = 0

for i in clean_data:
    AllVariations = CreateAllVariations([i[0]])
    Total += CheckAgainstReq(AllVariations, i[1])
    
    
    
print("Problem 1: ", Total)
print("End of script: ", str(datetime.now()).split(" ")[1][:-7])
    

        
