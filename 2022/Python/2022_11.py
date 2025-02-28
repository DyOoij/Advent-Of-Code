import copy
from datetime import datetime

with open("input.txt", "r") as Text:
    Clean_Data = []
    AllLines = Text.readlines()
    
    NewLineBreaks = [0]
    
    for i_Element in range(len(AllLines)):
        if AllLines[i_Element] == "\n":
            NewLineBreaks.append(i_Element + 1)
    
    for i_Point in range(len(NewLineBreaks)):
        
        MonkeChunk = []
        
        try:
            for i in AllLines[NewLineBreaks[i_Point]:NewLineBreaks[i_Point + 1]]:
                MonkeChunk.append(i.replace("\n", ""))
                
        except:
             for i in AllLines[NewLineBreaks[i_Point]:]:
                MonkeChunk.append(i.replace("\n", ""))
        
        MonkeChunkChopped = [
        int(MonkeChunk[0][-2]),                                       #Int monkey number
        MonkeChunk[1].split(":")[1].replace(" ", "").split(","),      #list of item number str
        MonkeChunk[2].split(": ")[1].split(" = ")[1],                 #str rule to determine worry
        int(MonkeChunk[3].split(" ")[-1]),                            #Int of divisible by rule
        int(MonkeChunk[4][-1]),                                       #Int throw to monkey when true
        int(MonkeChunk[5][-1]),                                       #Int throw to monkey when false
        0]                                                            #Inspection count
        
        
        Clean_Data.append(MonkeChunkChopped)
        


def CreateMonkeys(Data):
    #Create a dict of monkeys where the key is the monkey number
    #                           and the value is a list of all their attributes
    DictOfMonkeys = {}
    
    for Line in Data:
        Monkey = Line[0]
        DictOfMonkeys[Monkey] = Line[1:]
        
    return DictOfMonkeys
            

def PlayRound(Dict, Monkeys, Worry, SuperMod):
    #Simulate playing a round
    
    for Monkey in Monkeys:
        #Each monkey takes their turn
        
        Items           = Dict[Monkey][0]
        IsDivisible     = Dict[Monkey][2]
        InspectionCount = Dict[Monkey][5]
        
        for Item in Items:
            InspectionCount += 1
            
            """
            Alright, expo time. Since you are trying to see whether or not a value is divisible by IsDivisible, you don't need the WHOLE number, just a representative part
            When the number gets aboslutely fucking huge, you just need to make sure you keep a part that is divisible by all divisors, so the modulo of the value with modulo supermod
            All this shit is called Chinese Remainder Theorem, give it a google if you forgot what the fuck I am on about
            But yea, essentially, get the product of all IsDivisible values, then use that as a modulo to get a representative remainder of the item
            """
            
            if Worry == 3:
                Updated = int(UpdateWorry(int(Item), Dict[Monkey][1])/Worry)
                
            else:
                Updated = UpdateWorry(int(Item), Dict[Monkey][1])
                
            if Updated % IsDivisible == 0:
                #Trigger True
                ThrowToMonkey = Dict[Monkey][3]
                
            else:
                #Trigger False
                ThrowToMonkey = Dict[Monkey][4]
            
            #We need to throw the item out
            Dict[Monkey][0] = Dict[Monkey][0][1:]
            
            #And update the inspection count
            Dict[Monkey][5] = InspectionCount
                
            Dict[ThrowToMonkey][0].append(Updated)
   

                    
                    
                
                
                
                

                     
            

                

            
    return Dict
            
def UpdateWorry(Item, Rule):
    #Interprets the rule and returns the updated worry value
    Operation = Rule.split(" ")[1]    
    Num2      = Rule.split(" ")[2]
    
    if Num2 == 'old':
        Num2 = Item
    else:
        Num2 = int(Num2)
        
    #Just converts string to mathematical operation
    if Operation == "-":
        return Item - Num2
    if Operation == "+":
        return Item + Num2
    if Operation == "*":
        return Item * Num2
    
    
def GetSuperMod(Dict):
    
    AllDivvies = []
    ReturnProduct = 1
    
    for Key in Dict:
        AllDivvies.append(Dict[Key][2])
        
    for Divvy in AllDivvies:
        ReturnProduct *= Divvy
        
    return ReturnProduct

def SolveP1(DictOfMonkeysr):
        
    AllCounts = []    
    for Key in DictOfMonkeysr:
        AllCounts.append(DictOfMonkeysr[Key][5])
        
    Highest = sorted(AllCounts)[-1]
    Second  = sorted(AllCounts)[-2]
    
    return (Highest * Second)
    
 
    
    
DictOfMonkeys = CreateMonkeys(Clean_Data)

#This pisses me off so much, you HAD the right approach, but fucking TRACKBACKS fucked you over
#At least with the deepcopy you get the right answer
DictOfMonkeys2 = copy.deepcopy(DictOfMonkeys)

Monkeys = [Key for Key in DictOfMonkeys]
SuperMod = GetSuperMod(DictOfMonkeys)
Worry   = 3


for Round in range(20):
    DictOfMonkeys = PlayRound(DictOfMonkeys, Monkeys, Worry, SuperMod)
    
print("Problem 1: ", SolveP1(DictOfMonkeys))


#Problem 2, just run it for more range
Worry   = 1
for Round in range(10000):
    if (Round % 10) == 0 and Round != 0:
        print(datetime.now().strftime("%H:%M:%S -- "), "Rounds played thus far: ", Round)
        for Key in DictOfMonkeys2:
            print("    Monkey: ", Key, "    Items: ", DictOfMonkeys2[Key][0])

    DictOfMonkeys2 = PlayRound(DictOfMonkeys2, Monkeys, Worry, SuperMod)
    
print("Problem 2: ", SolveP1(DictOfMonkeys2))

    



