import copy

with open("input.txt", "r") as Text:
    Clean_Data = []
    AllLines = Text.readlines()
    for Line in AllLines:
        Clean_Data.append(list(Line.replace("\n","").split(" ")))
Text.close()


def ConvertToNumberGrid(Data):
    #Convert alphabetical to numbers for easier comparison
    
    GriddedHeights = []    
    ABC = "abcdefghijklmnopqrstuvwxyz"    
    for Row in Data:
        RowNums = []
        for char in Row[0]:
            if char in ABC:
                RowNums.append(ABC.index(char))
            else:
                RowNums.append(char)
        GriddedHeights.append(RowNums)
        
    return GriddedHeights
    
    
def DetermineTermini(Grid):
    #Returns start and end positions as YX tuples
    
    iMax_Y = len(Grid) - 1
    iMax_X = len(Grid[0]) - 1
    
    
    
    for i_Row in range(len(Grid)):
        for i_Column in range(len(Grid[i_Row])):
            if Grid[i_Row][i_Column] == 'S':
                Start = [i_Row, i_Column]
            if Grid[i_Row][i_Column] == 'E':
                End = [i_Row, i_Column]
    return [Start, End, iMax_Y, iMax_X]


def SolidAlgo(Grid, GridStats, PackedLocations):
    """
    Right, a verbose, solid as fuck A-Algorithm
    
    It takes the following format of input
           [ [list of tuples to visit],     [visited tuples]]
     e.g.  [ [[Y+1, X], [Y-1, X], [Y, X+1], [Y, X-1]], [[Y,X]] ]
     
    It then cycles through each tuple to visit, and moves one step in either Y or X direction
        This gets you 4 new tuples, you make sure to exclude the ones you have already visited
        So to travel from [Y+1, X] with -1 to Y, you get back to [Y, X], which you have already visited
        
    Now you can test the remaining tuples according to the following restraints:
    -Cannot be negative (Would be outside of grid on the top, or towards the left)
    -Cannot be higher than YMax for Y or XMax for X (Would be outside of grid on the bottom or right, respectively)
    -the int value contained in the looked at tuple can only have a delta of [-1, 0, 1] (is one lower or higher) in respect to the int contained at the current tuple
    
    This creates a whole host of new tuples that you can visit in the next cycle
        Perhaps, one tuple is the exit condition, in which case you can reach the goal set for this problem and is by definiton the shortest path, since you increment the path by 1 step each cycle
    
    Package these tuples in a list
    Package the tuples you have just considered in another list
    
    return [NewTuples], [VisitedTuples]
        This is the format you started with, and you can cycle these new tuples through again
    """
    

    Goal  = GridStats[1]
    MaxY  = GridStats[2]
    MaxX  = GridStats[3]
    
    YXTuples = PackedLocations[0]
    Visited  = PackedLocations[1]
    
    NewTuples  = []
    
    #Lets cycle through the fed tuples
    for YX in YXTuples:
        #Lets add the YX to visited
        Visited.append(YX)
        
        #This is where we store the up, down, left, right tuples for this current YX we are considering
        ConsiderTuples  = []
        ScaleableTuples = []
        
        Y = YX[0]
        X = YX[1]
        
        #Move up and down
        for YRange in [-1, 1]:
            #Exclude already visited tuples
            if [Y + YRange, X] not in Visited:
                #Check if the value does not go out of bounds
                if Y + YRange >= 0 and Y + YRange <= MaxY:
                    ConsiderTuples.append([Y + YRange, X])
            
        #Move left and right
        for XRange in [-1, 1]:
            #Exclude already visited tuples
            if [Y, X + XRange] not in Visited:
                #Check if the value does not go out of bounds
                if X + XRange >= 0 and X + XRange <= MaxX:
                    ConsiderTuples.append([Y, X + XRange])
                
        #So for the current, single YX that we are considering now, we have a number of hypothetical new locations
        #We can now test whether these new YX tuple locations are scaleable
        
        ValueAtCurrent = Grid[Y][X]
        
        #Grab the int value at the considered tuple
        for ConsiderTuple in ConsiderTuples:
            ConsiderY = ConsiderTuple[0]
            ConsiderX = ConsiderTuple[1]
            ValueAtConsider = Grid[ConsiderY][ConsiderX]
            
            #This allows you to travel both up and down
            #Maybe you only need to go up
            #Ok so after getting stuck it turns out you can just jump down as much as you want, break your ankles, fuck it
            # Val in [-1, 0, 1] changed to Val <= 1
            if ValueAtConsider - ValueAtCurrent <= 1:
                ScaleableTuples.append(ConsiderTuple)
        
        #What we have now is a list of tuples that are
        #   -Not previously visited
        #   -Not out of bounds
        #   -Scaleable (descend or ascend)
        
        for Tuple in ScaleableTuples:
            
            if Tuple == Goal:
                #We have reached the exit condition
                return False
                
            
            #Sometimes different start tuples can neighbour and return the same next tuple location
            #This if statement stops those from being added multiple times
            
            if Tuple not in NewTuples:
                NewTuples.append(Tuple)
            
    
    return [NewTuples, Visited]
        

def DetermineStartingPoints(Grid):
    #Determine the YX for all tiles labelled a
    
    AllTilesA = []
    
    for Y in range(len(Grid)):
        for X in range(len(Grid[Y])):
            if Grid[Y][X] == 0:
                
                AllTilesA.append([Y, X])
                
    return AllTilesA



def BuildVisual(Grid):
    """Troubleshooting for grid flood filling visual"""
    VisualGrid = []
    
    for Line in Grid:
        Row = []
        for Column in Line:
            Row.append(".")
        VisualGrid.append(Row)
    
    return VisualGrid
                

    






Grid =  ConvertToNumberGrid(Clean_Data)


Termini = DetermineTermini(Grid)          #[[sYX], [eYX], MaxY, MaxX]
StartYX = Termini[0]
EndYX   = Termini[1]


Grid[StartYX[0]][StartYX[1]] = 0
Grid[EndYX[0]][EndYX[1]] = 25



LocPack = [[StartYX],[]]

TotalSteps = 0

#Problem 1
for Iteration in range(500):
    try:
        LocPack = SolidAlgo(Grid, Termini, LocPack)
        TotalSteps += 1
    except:
        #SolidAlgo returns "False" instead of a list as soon as the exit condition is met
        #So the loop will fuck up here, perfect, that means that right now we have our answer
        print("Problem 1: ", TotalSteps)
        break

#Problem 2
AllALocs = DetermineStartingPoints(Grid)

PathLengths = []

"""
Basically doing the same as problem one, but instead of feeding it a single starting point, feed it all the points 'a' as a list and cycle through all of those
Is it efficient? No. Does it get the job done? Oh fuck yes it does my dude

A better solution would be the run the path backwards, just start at E and iterate until you hit a tile that has value 'a'.
However, this requires a tweak in logic for checking the maximum vertical difference.
For problem 1, you can only move to a tile that is at maximum 1 higher
Inversely, for this reverse approach that means that the tile (from E to any a) can only be as low as 1 lower (it can be any number higher)

So logic <= 1 has to become >= -1

"""

for StartingPoint in AllALocs:
    LocPack = [[StartingPoint],[]]
    TotalSteps = 0
    
    for Iteration in range(500):
        try:
            LocPack = SolidAlgo(Grid, Termini, LocPack)
            TotalSteps += 1
        except:
            PathLengths.append(TotalSteps)
            break
            
print("Problem 2: ", sorted(PathLengths)[0])





