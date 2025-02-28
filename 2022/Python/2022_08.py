with open("input.txt", "r") as Text:
    Clean_Data = []
    AllLines = Text.readlines()
    for Line in AllLines:
        Clean_Data.append(list(Line.replace("\n","")))
        


def FlipAxis(ListOfVals):
    #Flips the grid along the XY axis to count verticals as horizontals
    
    FlippedTable = []
    LenX = len(ListOfVals[0])
    LenY = len(ListOfVals)
    
    for X in range(LenX):
        LineX = []
        for Y in range(LenY):
            LineX.append(ListOfVals[Y][X])
        FlippedTable.append(LineX)
    
    return(FlippedTable)


def TreesInEachDirection(Normal, Flipped):
    #Creates lists to of tree tallness in either direction of the tree considered
    
    LenX = len(Normal[0])
    LenY = len(Normal)
    
    
    #This calculates the border trees amount
    TotalVisible = (2 * LenX) + (2 * LenY) - 4
    
    #Tree score
    TreeScore = 0
    
    
    for Y in range(LenY):
        LineY = Normal[Y]
        for X in range(LenX):
            LineX = Flipped[X]
            
            #We do not consider the trees at the border, so either X[0], Y[0], X[max], Y[max]
            
            if X != 0 and X != LenX - 1 and Y != 0 and Y != LenY-1:
                
                Self  = int(Normal[Y][X])
                Left  = [int(L) for L in Normal[Y][:X][::-1]]
                Right = [int(R) for R in Normal[Y][X+1:]]
                Up    = [int(U) for U in Flipped[X][:Y][::-1]]
                Down  = [int(D) for D in Flipped[X][Y+1:]]
                
                #So for problem one, we calculate whether or not a tree is visible (border trees are always visible)
                TotalVisible += DetermineVisibility(Self, Left, Right, Up, Down)
                
                #And for problem two, we calculate the highest tree score
                #If this score is higher than the current known score, overwrite it
                if DetermineScore(Self, Left, Right, Up, Down) > TreeScore:
                    TreeScore = DetermineScore(Self, Left, Right, Up, Down)
                    

                
            

                
    return [TotalVisible, TreeScore]

def DetermineVisibility(Self, Left, Right, Up, Down):
    #Check if tree is visible or not
    #As soon as a tree is visible in any direction, exit the function with return 1
    #If a tree is not at all visible, return 0
    
    for Direction in [Left, Right, Up, Down]:
        if Self > max(Direction):
            return 1

    return 0

def DetermineScore(Self, Left, Right, Up, Down):
    
    Multipliers = []
    
    for Direction in [Up, Right, Down, Left]:
        
        #See how many trees you can count before you see one at the same height or taller than yours
        #If you can't see one at the same height or taller than yours, you must be able to see to the edge
        for i_Step in range(len(Direction)):
            if Self <= Direction[i_Step]:
                Multipliers.append(i_Step + 1)
                break
        
        
        
        #If multipliers has not yet received a value for this direction
        #Add the total length of the direction (to the edge of the map)
        if len(Multipliers) == [Up, Right, Down, Left].index(Direction):
            Multipliers.append(len(Direction))
            
            

    #Calculates the product of the list
    InitMultiplier = 1
    for Value in Multipliers:
        InitMultiplier *= Value

    return InitMultiplier
        
            
            
NormalGrid  = Clean_Data
FlippedGrid = FlipAxis(Clean_Data)
Retrieve = TreesInEachDirection(NormalGrid, FlippedGrid)

print("Problem 1: ", Retrieve[0])
print("Problem 2: ", Retrieve[1])



