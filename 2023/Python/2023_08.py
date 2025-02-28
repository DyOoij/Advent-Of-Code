from datetime import datetime
from collections import Counter
from math import lcm


print("Start of script: ", str(datetime.now()).split(" ")[1][:-7])

input_file = open("input.txt", "r").readlines()
LR_instructions = input_file[0].replace('\n', '')

Token_Dict = {}


for i in input_file[2:]:
    LR_Pair = []
    Line = i.replace('\n', '').split(" = ")
    Token = Line[0]
    Pairs = Line[1][1:-1].split(", ")
    
    Token_Dict[Token] = Pairs


#Problem 1
Loc = 'AAA'
StepCounter = 0    

    
def UpdateLoc(Loc, Direction):
    WhereTo = Token_Dict[Loc]
    if Direction == 'L':
        return Token_Dict[Loc][0]
    else:
        return Token_Dict[Loc][1]


    


"""    
for steps in range(0, 99999):
    NewLoc = UpdateLoc(Loc, LR_instructions[steps])
    StepCounter += 1
    if NewLoc == 'ZZZ':
        print("Total steps: ", StepCounter)
        break
    else:
        Loc = NewLoc
    
    if steps + 1 == len(LR_instructions):
        LR_instructions += LR_instructions"""
    

#Problem 2
Starting_Points = []
LCM = []

for i in Token_Dict:
    if i[2] == 'A':
        Starting_Points.append(i)
        
        

for steps in range(0, 9999999999):
       
    for Sim_Pos_i in range(len(Starting_Points)):
        Sim_Pos = Starting_Points[Sim_Pos_i]
        

        NewLoc = UpdateLoc(Sim_Pos, LR_instructions[steps % len(LR_instructions)])
        

        Starting_Points[Sim_Pos_i] = NewLoc

        
    for Point in Starting_Points:
        if Point[2] == 'Z':
            LCM.append(steps + 1)
        
    if len(LCM) == 6:
                break
        
print("Problem 2: ", lcm(*LCM))



        
    
        

    
    

    






    



    

    
