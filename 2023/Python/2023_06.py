from datetime import datetime
from math import sqrt, ceil, floor

#print("Start of script: ", str(datetime.now()).split(" ")[1])

input_file = open("input.txt", "r").readlines()

Lines = []
Times = []
TimesS = []
Distances = []
DistancesS = []
Winning = []
Init = 1


for i in input_file:
    Lines.append(i.replace("\n", "").split(":")[1])
    
for Time in Lines[0].split(" "):
    if Time.isnumeric():
        Times.append(int(Time))
        TimesS.append(str(Time))
        
for Distance in Lines[1].split(" "):
    if Distance.isnumeric():
        Distances.append(int(Distance))
        DistancesS.append(str(Distance))
        



def FindBounds(time, distance):
    #x**2 - (time * x) + distance
    #Where x is time to press button
    
    x1 = (-(-time) - sqrt( (-time)**2 - 4 * distance))/2
    x2 = (-(-time) + sqrt( (-time)**2 - 4 * distance))/2
    
    if x1.is_integer():
        x1 += 1  
    else:
        x1 = ceil(x1)
    
    if x2.is_integer():
        x2 -= 1
    else:
        x2 = floor(x2)
    
    return [int(x1), int(x2)]
    
for Races_i in range(len(Times)):
    Ranges = FindBounds(Times[Races_i], Distances[Races_i])
    
    TotalWins = (Ranges[1] - Ranges[0]) + 1
    
    Winning.append(TotalWins)
    
for t in Winning:
    Init *= t
    
print(Init)

KerTime = int("".join(TimesS))
KerDistance = int("".join(DistancesS))



print(FindBounds(KerTime, KerDistance)[1] - FindBounds(KerTime, KerDistance)[0] + 1)
