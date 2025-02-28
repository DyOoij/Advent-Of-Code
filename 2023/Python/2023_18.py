from datetime import datetime
from collections import Counter


#print("Start of script: ", str(datetime.now()).split(" ")[1][:-7])

input_file = open("input.txt", "r").readlines()
clean_data = []

for i in input_file:
    clean_data.append(i.replace('\n', '').split(' '))
    
CoordsByY = {}
PosX = 0
PosY = 0

def UpdatePos(Line):
    #Takes the input line by line and generates coordinates that it distributes
    #   throughout a dict
    #   The Dict is ordered by Y coordinate, essentially horizontal line by horizontal line
    
    global PosX, PosY
    Dir = Line[0]
    Dist = int(Line[1])
    
    for Steps in range(Dist):
        
        if Dir == 'L' or Dir == 'R':
            PosX += [-1, 1][['L', 'R'].index(Dir)]
        elif Dir == 'U' or Dir == 'D':
            PosY += [-1, 1][['U', 'D'].index(Dir)]
        
        #This creates a new Key if there's no PosY in the Dict
        if PosY not in CoordsByY: 
                CoordsByY[PosY] = []
                
        CoordsByY[PosY].append(PosX)

def FloodFill(Seeds, Dict):
    #Standard flood fill algo, probably adds extra unneeded entries due to looping
    #This is why it returns a set() instead of a list
    #Because I am have smol brain
    NewSeeds = []
    
    for Seed in Seeds:
        Dict[Seed[0]].append(Seed[1])
        
        #Surrounding locations
        Seed_Up    = (Seed[0] - 1, Seed[1])
        Seed_Down  = (Seed[0] + 1, Seed[1])
        Seed_Left  = (Seed[0], Seed[1] - 1)
        Seed_Right = (Seed[0], Seed[1] + 1)
        
        TempSeeds = [Seed_Up, Seed_Down, Seed_Left, Seed_Right]
    
        for TempSeed in TempSeeds:
            if TempSeed[1] not in Dict[TempSeed[0]]:
                NewSeeds.append(TempSeed)
    
    return set(NewSeeds)
        
        
    


for Entry in clean_data:
    #This creates the coordinate dictionary
    UpdatePos(Entry)

#HAS TO BE WITHIN BOUNDS
Seeds = [(-1,-1)]
    
while len(Seeds) != 0:
    #Exit condition! Lookie at you!
    Seeds = FloodFill(Seeds, CoordsByY)
    
    
TotalTiles = 0

for g in CoordsByY:
    TotalTiles += len(CoordsByY[g])
    
print("Problem 1: ", TotalTiles)

    
