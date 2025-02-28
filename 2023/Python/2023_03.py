input_file = open("input.txt", "r").readlines()


grid = []



for i in input_file:
    rows = []
    for j in i.replace("\n", ""):
        rows.append(j)
    grid.append(rows)


numsandtermini = []
numswithsymbols = []
NumLenCounter = 0
SymbolLocations = []


#problem 1
for line_i in range(len(grid)):

    for loc_i in range(len(grid[0])):       
        if NumLenCounter == 0:
            if grid[line_i][loc_i].isnumeric() and loc_i < len(grid[0]):
                #A number is found, count length
                LenCount = 0
                while grid[line_i][loc_i + LenCount].isnumeric():
                    LenCount += 1
                    NumLenCounter += 1
                    if loc_i + LenCount  == len(grid[0]):
                        break
                
                numsandtermini.append([line_i, (loc_i, loc_i + LenCount), int("".join(grid[line_i][loc_i : loc_i + LenCount]))])
                

                    
        else:
            NumLenCounter -= 1

    
    
for item in numsandtermini:
    SurroundingSymbols = []
    ExaminedLine = item[0]
    indexmin = item[1][0]
    indexmax = item[1][1]
    
    for Loc in range(indexmin, indexmax):
        
        for PosY in range(-1, 2):
            for PosX in range(-1, 2):
                if PosY + ExaminedLine >= 0 and PosY + ExaminedLine < len(grid) and PosX + Loc >= 0 and PosX + Loc < len(grid[0]):
                    #As long as yer within bounds HARRY
                    if grid[PosY + ExaminedLine][PosX + Loc] != '.' and grid[PosY + ExaminedLine][PosX + Loc].isnumeric() == False:
                        SurroundingSymbols.append(grid[PosY + ExaminedLine][PosX + Loc])
                        
    
    if len(SurroundingSymbols) != 0:
         numswithsymbols.append(item[2])
         
Runningtotal = 0
for r in numswithsymbols:
    Runningtotal += r
    
print(Runningtotal)
    
#problem 2 - only works for sets with TWO UNIQUE GEARS
GearTotal = 0
locationofgear = []

gearnumber = []

for line_i in range(len(grid)):
    for loc_i in range(len(grid[line_i])):
        if grid[line_i][loc_i] == '*':
            locationofgear.append((line_i,loc_i))
            
for geartuple in locationofgear:
    
    touchinggears = []
    
    gearX = geartuple[1]
    gearY = geartuple[0]
    
    
    for PosY in range(-1, 2):
        for PosX in range(-1, 2):
            if [PosY, PosX] != [0, 0]:
                if PosY + gearY >= 0 and PosY + gearY < len(grid) and PosX + gearX >= 0 and PosX + gearX < len(grid[0]):
                    if grid[PosY + gearY][PosX + gearX].isnumeric():
                        #we have a number
                        
                        fullnumber = [grid[PosY + gearY][PosX + gearX]] #This is the centre number
                        
                        NumberY = PosY + gearY
                        NumberX = PosX + gearX
                        
                        for creepL in range(1, len(grid[0])):
                            if NumberX - creepL >= 0:
                                if grid[PosY + gearY][PosX + gearX - creepL].isnumeric():
                                    fullnumber.insert(0, grid[PosY + gearY][PosX + gearX - creepL])
                                else:
                                    break
                                    
                        for creepR in range(1, len(grid[0])):
                            if NumberX + creepR < len(grid[0]):
                                if grid[PosY + gearY][PosX + gearX + creepR].isnumeric():
                                    fullnumber.append(grid[PosY + gearY][PosX + gearX + creepR])
                                else:
                                    break
                                
                        if fullnumber not in touchinggears:
                            touchinggears.append(fullnumber)
    
    if len(touchinggears) == 2:
        geartouchset = []
        for listofdigits in touchinggears:
            geartouchset.append(''.join(listofdigits))
        
        gearnumber.append(geartouchset)
            

for setofgears in gearnumber:
    GearTotal += (int(setofgears[0]) * int(setofgears[1]))

    
print(GearTotal)
        


                                
                            
                    
                    
                
            
        
            

            

            
            



            
