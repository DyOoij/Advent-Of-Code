import copy

with open("input.txt", "r") as Text:
    Clean_Data = []
    AllLines = Text.readlines()
    for Line in AllLines:
        Clean_Data.append(list(Line.replace("\n","").split(" ")))
        

def CreateSignalList(InstructionsSet, InitNumber):
    #Create a dict of cycle numbers, then add the changes that happen during that cycle
    
    ValuePerCycleStartEnd = [[InitNumber]]

    
    for i_Instruction in range(len(InstructionsSet)):
        
        Command = InstructionsSet[i_Instruction][0]
        ValAtStart = ValuePerCycleStartEnd[-1][-1]
        
        if Command == "noop":
            #Nothing changes, add a new pair of [Val,Val] to the list
            ValuePerCycleStartEnd.append([ValAtStart, ValAtStart])
        
        if Command == "addx":
            Change = int(InstructionsSet[i_Instruction][1])
            
            #First, nothing happens
            ValuePerCycleStartEnd.append([ValAtStart, ValAtStart])
            
            #Then, we update the value
            ValuePerCycleStartEnd.append([ValAtStart, ValAtStart + Change])
            

        
    return ValuePerCycleStartEnd 

def CreateGridLine(Signals):
    #Create a single line of characters to use as a grid
    PixelLine = ""
    CurrentPixel = 0
    
    for Line in Signals:
        CurrentPosition = Line[0]   #This is the middle of the sprite

        if (CurrentPixel) % 40 in [CurrentPosition - 1, CurrentPosition, CurrentPosition + 1]:
            #So if the sprite covers the current pixel either by the leftmost, center or rightmost pixel of the sprite
            #If Pixel == 40, then just reset the Pixel to 0 (leftmost side of the screen) through % 40
            PixelLine += "#"
        else:
            #The sprite does not cover the current pixel
            PixelLine += " "
        CurrentPixel += 1
        
    return PixelLine
    
    


def TransformPixels(PixelLine):
    
    Points = [x for x in range(241) if x % 40 == 0]
    for i_PointsAB in range(len(Points)):
        
        try:
            print(PixelLine[Points[i_PointsAB]:
                            Points[i_PointsAB + 1]])
        except:
            print(PixelLine[Points[i_PointsAB]:])
        

            
def SolveP1(SignalList, FirstSignal, ProceduralSignal):            
 
    AddProducts = []  #Stores all the (cycle * valsatstart) values
            
    for i_Cycle in range(len(SignalList)):
        
        #This catches the 20
        if i_Cycle == FirstSignal:
            AddProducts.append(SignalList[i_Cycle][0] * i_Cycle)
        
        #This catches everything beyond 20, incrementing by 40, excluding ((20-20) % 20) which would be the first line (index 0)
        if ((i_Cycle - FirstSignal) % ProceduralSignal) == 0 and i_Cycle  != FirstSignal:
            
            #SignalList lists the START and END values of the signal, so we take the START value ([0]), as that is the signal during the cycle 
            AddProducts.append(SignalList[i_Cycle][0] * i_Cycle)
            
    return sum(AddProducts)
             

            
        
            

            
    

Signals = CreateSignalList(Clean_Data, 1)
Problem1 = SolveP1(Signals, 20, 40)
print("Problem 1: ", Problem1)

Pixels = CreateGridLine(Signals[1:])
print("Problem 2: \n")
Problem2 = TransformPixels(Pixels)
