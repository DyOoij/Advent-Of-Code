from datetime import datetime
from collections import Counter


#print("Start of script: ", str(datetime.now()).split(" ")[1][:-7])

input_file = open("input.txt", "r").readlines()
clean_data = []
rotate_data = []

Total = 0
 

for i in input_file:
    clean_data.append(list(i.replace('\n', '')))
    
    
for LineDown in tuple(zip(*clean_data)):
    return_line_flip = ''
    for item in LineDown:
        return_line_flip += item
    rotate_data.append(return_line_flip)
    

def StoneLine(Line):
    Pos_Cube = [-1] #'rock' at the top
    Pos_Round = []
    PointsForLine = 0

    #We record the initial state of all rocks
    for char_i in range(len(Line)):
        if Line[char_i] == '#':
            Pos_Cube.append(char_i)
        elif Line[char_i] == 'O':
            Pos_Round.append(char_i)
            
    Pos_Cube.append(len(Line)) #'rock' at the bottom

    
            
    for Gap_i in range(len(Pos_Cube)):
        if Gap_i < len(Pos_Cube) - 1:
            Point1 = Pos_Cube[Gap_i]
            Point2 = Pos_Cube[Gap_i + 1]
            
            These_Rocks_Here = []
        
            for Round in Pos_Round:
                if Round in range(Point1, Point2):
                    #Rocks fall in these ranges
                    These_Rocks_Here.append(Round)
                    
            if len(These_Rocks_Here) != 0:            
                for i in range(len(These_Rocks_Here)):
                    PointsForLine += (len(Line) - 1 - Point1) - i

    return PointsForLine
                
            
                

        
            

        

for t in rotate_data:

    Total += StoneLine(t)


print("Problem 1: ", Total)
