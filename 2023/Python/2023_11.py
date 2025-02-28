from datetime import datetime
from collections import Counter


#print("Start of script: ", str(datetime.now()).split(" ")[1][:-7])

input_file = open("input.txt", "r").readlines()

clean_data = []

AddedY = []
AddedX = []

for i in input_file:
    clean_data.append(i.replace('\n', ''))
    



def Expand(grid):
    YLen = len(grid)
    
    ExpandY = []
    YCounter = 0
    
    ExpandX = []
    XCounter = 0
    
    #Vertical expansion first, first locate all empty rows
    #Then insert empty rows at that location
    #Update the location no. with each added row
    #Since adding a row SHIFTS all subsequent rows down by 1, each time
    for row_i in range(YLen):
        if '#' not in grid[row_i]:
            ExpandY.append(row_i)                         
    for Y in ExpandY:
        grid.insert(Y + YCounter, '_' * len(grid[0]))
        AddedY.append(Y + YCounter)
        YCounter += 1
        
    #Now do horizontal expansion, first find all empty columns
    #Then, following the same logic as the vertical expansion
    #insert a '.' at the location of the empty collumn, for each row
    #Update the row location no. to account for the rows shifting
    for column_i in range(len(grid[0])):
        DrawDown = []
        for YStep in range(YLen + YCounter):
            DrawDown.append(grid[YStep][column_i])
            
        if '#' not in DrawDown:
            ExpandX.append(column_i)    
    for X in ExpandX:
        for row in range(YLen + YCounter):
            grid[row] = grid[row][:X + XCounter] + '_' * 1 + grid[row][X + XCounter:]
        AddedX.append(X + XCounter)
        XCounter += 1
            
    return grid

def FindGalaxies(Screen):
    GalaxyTuples = []
    GalaxyNo = 0
    for index_row in range(len(Screen)):
        for index_column in range(len(Screen[index_row])):
            if Screen[index_row][index_column] == '#':
                GalaxyNo += 1
                GalaxyTuples.append([(index_row, index_column), GalaxyNo])
    return GalaxyTuples
                
    
def PathCounter(Gal_List):
    Distances = []
    
    for Gal_i in range(len(Gal_List)):
        Gal = Gal_List[Gal_i]
        Gal_Pairs = Gal_List[Gal_i + 1:]
        
        for GalP in Gal_Pairs:
            DifY = abs(Gal[0][0] - GalP[0][0])
            DifX = abs(Gal[0][1] - GalP[0][1])
            
            Distances.append(DifX + DifY)
    
    return Distances
        
def PathCounterWithMultiples(Gal_List, Multiple):
    Multiple -= 1 #To delete the space that we are replacing with the multiple
    Multiple -= 1 #To delete the extra row we added when the galaxy expanded
    
    #Essentially, since I am working on the expanded galaxy (Which I need to check galaxies against the added space)
    #I need to substract 1 from the multiple to delete the CURRENT SPACE and make room for a space with N SPACES
    #Then I need to delete the extra row from when I expanded the galaxy
    #Left undone, the actual galaxy space size for a space that needs to be updated to 10 is:
    #1 (space itself) + 1 (it's double from ExpandedGalaxy) + 10 (The updated space)
    #So the space itself and its double need to be removed
    
    DistancesMulti = []
    
    for Galaxy_i in range(len(Gal_List)):
        Eval_Gal = Gal_List[Galaxy_i]
        Pair_With = Gal_List[Galaxy_i + 1:]
        
        for Pair in Pair_With:
            AddToY = 0
            AddToX = 0
            
            OrderedY = sorted([Eval_Gal[0][0], Pair[0][0]])
            OrderedX = sorted([Eval_Gal[0][1], Pair[0][1]])
            
            for AddY in AddedY:
                if AddY in range(OrderedY[0], OrderedY[1]):
                    AddToY += Multiple
                    
            for AddX in AddedX:
                if AddX in range(OrderedX[0], OrderedX[1]):
                    AddToX += Multiple
                    
            DifY = OrderedY[1] - OrderedY[0]
            DifX = OrderedX[1] - OrderedX[0]
                   
            DistancesMulti.append(DifY + DifX + AddToY + AddToX)
    

    return DistancesMulti
                    
                    

            
            
            
    


          
ExpandedGrid = Expand(clean_data.copy())
Galaxies = FindGalaxies(ExpandedGrid)


print("Total distance between all galaxy pairs: ", sum(PathCounter(Galaxies)))

#print()
#for u in ExpandedGrid:
#    print(u)
#print()



print("Total distances with updated spaces: ", sum(PathCounterWithMultiples(Galaxies, 1000000)))




    
