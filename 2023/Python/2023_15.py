from datetime import datetime
from collections import Counter


#print("Start of script: ", str(datetime.now()).split(" ")[1][:-7])

input_file = open("input.txt", "r").readlines()
clean_data = []

RunTotal = 0

for i in input_file:
    for j in i.split(','):
        clean_data.append(j)
       


def StringValue(Entry):
    #Simple calculation for part one
    ReturnTotal = 0   
    for char in Entry:
        ReturnTotal += ord(char)
        ReturnTotal = (ReturnTotal * 17) % 256
    return ReturnTotal
        

for Str in clean_data:
    RunTotal += StringValue(Str)
print("Problem 1: ", RunTotal)


Dict_Box = {}
#Set up the Dict with box number 0 > 255
for BoxNo in range(256):
    Dict_Box[BoxNo] = []
    


for Str in clean_data:
    Add = True #This controls whether or not the Str will be added at the end of the for loop
    
    if '=' in Str:
        Box = StringValue(Str.split('=')[0])
        LabelNoNum = Str.split('=')[0]
        ReplaceLabel = Str.split('=')[0] + ' ' + Str.split('=')[1] #[cm 1]
        
        for item_i in range(len(Dict_Box[Box])): # for index in ['ab 1', 'cd 2']
            IsLabelHere = Dict_Box[Box][item_i].split(' ')[0]   # 'ab'
            if IsLabelHere == LabelNoNum:
                #Matching labels, replace
                CopyList = Dict_Box[Box].copy()
                CopyList[item_i] = ReplaceLabel #Work with copies to avoid any fuckery
                Dict_Box[Box] = CopyList
                Add = False #If a value is replaced, it doesn't need to be added at the end, so Add is set to false
                break
        
        if Add == True:
            Dict_Box[Box].append(ReplaceLabel)
        

        

        
    elif '-' in Str:
        Box = StringValue(Str.split('-')[0])
        Label = Str.split('-')[0]
        
        for Dict_Label_i in range(len(Dict_Box[Box])):
            if Dict_Box[Box][Dict_Label_i].split(' ')[0] == Label:
                List_In_Dict = Dict_Box[Box].copy()
                
                for Label_i in range(len(List_In_Dict)):
                    if List_In_Dict[Label_i].split(' ')[0] == Label:
                        del List_In_Dict[Label_i]
                        Dict_Box[Box] = List_In_Dict
                        break
                break
                        
Total2 = 0

for Box in Dict_Box:
    if len(Dict_Box[Box]) > 0:
        BoxNo = Box + 1
        for Lens_i in range(len(Dict_Box[Box])):
            Total2 += ((Lens_i + 1)  *  int(Dict_Box[Box][Lens_i].split(' ')[1]) * BoxNo)
            
            
print("Problem 2: " ,Total2)
