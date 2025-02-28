from datetime import datetime
from collections import Counter



#print("Start of script: ", str(datetime.now()).split(" ")[1][:-7])

input_file = open("input.txt", "r").readlines()
grid = []
starting_loc = 0
Last_Loc = 0
Steps = 0
Taken_Path = []
Total_Fields = []

for i in input_file:
    grid.append(list(i.replace('\n','')))

# [NSWE]
Dict_Connect = {'|' : [1,1,0,0],
                '-' : [0,0,1,1],
                'L' : [1,0,0,1],
                'J' : [1,0,1,0],
                '7' : [0,1,1,0],
                'F' : [0,1,0,1],
                'S' : [0,0,1,0],
                '.' : [0,0,0,0]}


for y_i in range(len(grid)):
    for x_i in range(len(grid[y_i])):
        if grid[y_i][x_i] == 'S':
            starting_loc = [y_i, x_i]
            


def ListLocals(YXLoc):
    Cardinals = []

    for ystep in range(-1, 2):
        if ystep != 0:
            if YXLoc[0] + ystep >= 0:
                Cardinals.append([YXLoc[0] + ystep, YXLoc[1]])
            else:
                Cardinals.append([None, YXLoc[1]])
                
    for xstep in range(-1, 2):
        if xstep != 0:
            if YXLoc[1] + xstep >= 0:
                Cardinals.append([YXLoc[0], YXLoc[1] + xstep])
            else:
                Cardinals.append([YXLoc[0], None])
    return Cardinals            


def NextStep(Loc):
    Local_Dir = ListLocals(Loc)
    Symbol = grid[Loc[0]][Loc[1]]
    Allowed_Dir = Dict_Connect[Symbol]
    

    
    for Move in Local_Dir:

        if None not in Move:
            if Allowed_Dir[Local_Dir.index(Move)] == 1 and grid[Move[0]][Move[1]] != '.':
                if Move != Last_Loc:

                    return Move




while True:
    Move_To = NextStep(starting_loc)
    if Move_To != Last_Loc:
        Last_Loc = starting_loc
        starting_loc = Move_To
        
    Steps += 1 
    
   
    Taken_Path.append(Move_To)
    
    
    if grid[Move_To[0]][Move_To[1]] == 'S':
        print("Problem 1: ", int(Steps/2))
        #print(Taken_Path)
        break

def RayPath(Path, OGHead):
    Heading = OGHead
       
    for stepP in Path:
        
        if grid[stepP[0]][stepP[1]] == 'L':
            if Heading == 3:
                Heading = 2
            elif Heading == 4:
                Heading = 1
                
        if grid[stepP[0]][stepP[1]] == 'J':
            if Heading == 3:
                Heading = 4
            elif Heading == 2:
                Heading = 1
                
        if grid[stepP[0]][stepP[1]] == '7':
            if Heading == 2:
                Heading = 3
            elif Heading == 1:
                Heading = 4
        
        if grid[stepP[0]][stepP[1]] == 'F':
            if Heading == 1:
                Heading = 2
            elif Heading == 4:
                Heading = 3
        
        
        AddFields = []
        #print(stepP, Heading)
        
        #Look right first   
        if Heading == 3: 
            LookRight = 1
            for MaxLen in range(len(grid[0])):
                if [stepP[0], stepP[1] + LookRight] not in Path:
                    AddFields.append([stepP[0], stepP[1] + LookRight])
                    LookRight += 1   
                else:
                    break
        #Look left
        elif Heading == 1: 
            LookLeft = 1
            for MaxLen in range(len(grid[0])):
                if [stepP[0], stepP[1] - LookLeft] not in Path:
                    AddFields.append([stepP[0], stepP[1] - LookLeft])
                    LookLeft += 1   
                else:
                    break
        #Look down
        if Heading == 4: 
            LookDown = 1
            for MaxLen in range(len(grid)):
                if [stepP[0] + LookDown, stepP[1]] not in Path:
                    AddFields.append([stepP[0] + LookDown, stepP[1]])
                    LookDown += 1   
                else:
                    break
        #Look up
        if Heading == 2: 
            LookUp = 1
            for MaxLen in range(len(grid)):
                if [stepP[0] - LookUp, stepP[1]] not in Path:
                    AddFields.append([stepP[0] - LookUp, stepP[1]])
                    LookUp += 1   
                else:
                    break
        

        
        for field in AddFields:
            if field not in Total_Fields:
                Total_Fields.append(field)
        

        
    
def RayPath2(Path, OGHead):
    Heading = OGHead
       
    for stepP in Path:
        

        
        
        AddFields = []
        #print(stepP, Heading)
        
        #Look right first   
        if Heading == 3: 
            LookRight = 1
            for MaxLen in range(len(grid[0])):
                if [stepP[0], stepP[1] + LookRight] not in Path:
                    AddFields.append([stepP[0], stepP[1] + LookRight])
                    LookRight += 1   
                else:
                    break
        #Look left
        elif Heading == 1: 
            LookLeft = 1
            for MaxLen in range(len(grid[0])):
                if [stepP[0], stepP[1] - LookLeft] not in Path:
                    AddFields.append([stepP[0], stepP[1] - LookLeft])
                    LookLeft += 1   
                else:
                    break
        #Look down
        if Heading == 4: 
            LookDown = 1
            for MaxLen in range(len(grid)):
                if [stepP[0] + LookDown, stepP[1]] not in Path:
                    AddFields.append([stepP[0] + LookDown, stepP[1]])
                    LookDown += 1   
                else:
                    break
        #Look up
        if Heading == 2: 
            LookUp = 1
            for MaxLen in range(len(grid)):
                if [stepP[0] - LookUp, stepP[1]] not in Path:
                    AddFields.append([stepP[0] - LookUp, stepP[1]])
                    LookUp += 1   
                else:
                    break
        

        
        for field in AddFields:
            if field not in Total_Fields:
                Total_Fields.append(field)
                
        if grid[stepP[0]][stepP[1]] == 'L':
            if Heading == 3:
                Heading = 2
            elif Heading == 4:
                Heading = 1
                
        if grid[stepP[0]][stepP[1]] == 'J':
            if Heading == 3:
                Heading = 4
            elif Heading == 2:
                Heading = 1
                
        if grid[stepP[0]][stepP[1]] == '7':
            if Heading == 2:
                Heading = 3
            elif Heading == 1:
                Heading = 4
        
        if grid[stepP[0]][stepP[1]] == 'F':
            if Heading == 1:
                Heading = 2
            elif Heading == 4:
                Heading = 3
                        
        

            
            
#Lmao do the function twice, but swap the heading swap and void counter step LMAO            
RayPath(Taken_Path, 2)
RayPath2(Taken_Path, 2)

print("Problem 2: ", len(Total_Fields))
