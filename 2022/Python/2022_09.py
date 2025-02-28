import copy

with open("input.txt", "r") as Text:
    Clean_Data = []
    AllLines = Text.readlines()
    for Line in AllLines:
        Clean_Data.append(list(Line.replace("\n","").split(" ")))
        

def CreateGrid(Y, X):
    #Return a grid
    Grid = []
    
    for stepY in range(Y):
        LineY = []
        for stepX in range(X):
            LineY.append(".")
        Grid.append(LineY)
    return Grid


def DetermineGridInitState(Data):
    #First, let's see what size of grid we need by following the extremes of where H travels
    
    InitPos = [0,0]  #[Y,X]
    LocationsY = [0]
    LocationsX = [0]
    
    Directions  = ['U', 'D', 'L', 'R']
    DistanceMod = [-1, 1, -1, 1]
    UpdateIndex = [0, 0, 1, 1]
    Locations   = [LocationsY, LocationsY, LocationsX, LocationsX]
    
    for Line in Data:
        DirIndex = Directions.index(Line[0])
        
        MoveBy = int(Line[1]) * DistanceMod[DirIndex]
        InitPos[UpdateIndex[DirIndex]] += MoveBy
        
        if InitPos[UpdateIndex[DirIndex]] not in Locations[DirIndex]:
            Locations[DirIndex].append(InitPos[UpdateIndex[DirIndex]])
        
    MinY = int(sorted(LocationsY)[0])
    MaxY = int(sorted(LocationsY)[-1])
    MinX = int(sorted(LocationsX)[0])
    MaxX = int(sorted(LocationsX)[-1])
    
    LenY = MaxY - MinY + 1
    LenX = MaxX - MinX + 1
    StartPos = (abs(MinY), abs(MinX))
    
    return [LenY, LenX, StartPos]
    
    
def CreateKnotDict(Names, YX):
    #Create a dict based on all the knots needed and sets it to the start position
    #(They all start one atop the other)
    
    NewDict = {}
    PosList = [x for x in YX]  #Converts (a, b) into [a, b] so it is mutable
    
    for Name in Names:
        NewDict[Name] = PosList
        
    return NewDict


def MoveKnots(Instructions, KnotNames, Y, X):
    global DictOfNamesAndYX
    
    #Read instructions
    for Instruction in Instructions:
        Dir   = Instruction[0]
        Steps = int(Instruction[1])
        
        #MoveH and Update Tails
        for Step in range(Steps):
            #print(DictOfNamesAndYX)
            MoveH(Dir)
            UpdateTails(KnotNames, Dir)
        
   
            #Check unique pos of T
            if DictOfNamesAndYX['T'] not in AllLocsOfTail:
                #Save unique positions in external list
                AllLocsOfTail.append(DictOfNamesAndYX['T'])
                

def MoveH(Dir):

    global DictOfNamesAndYX
    
    CurrentHLoc = DictOfNamesAndYX['H'] #Location YX of the Head
    HY = CurrentHLoc[0]
    HX = CurrentHLoc[1]
    
    if Dir in ['U', 'D']:
        DictOfNamesAndYX['H'] = [HY + [-1, 1][['U', 'D'].index(Dir)] ,HX]
        
    if Dir in ['L', 'R']:
        DictOfNamesAndYX['H'] = [HY, HX + [-1, 1][['L', 'R'].index(Dir)]]
        
def UpdateTails(KnotNames, Dir):
    global DictOfNamesAndYX
    
    for KnotName in KnotNames:
        if KnotName != 'H':
            LeadKnotName = KnotNames[KnotNames.index(KnotName) - 1]
            
            try:
                NextKnotName = KnotNames[KnotNames.index(KnotName) + 1]
            except:
                pass
          
            #So now we have the NAME of the knot that moves, and the tail it is connected to
            #Check if the tail is still connected
            
            TailScan = []
            TailYX = DictOfNamesAndYX[KnotName]
            
            for Y in [-1, 0, 1]:
                for X in [-1, 0, 1]:
                    TailScan.append([TailYX[0] + Y, TailYX[1] + X])
            
            if DictOfNamesAndYX[LeadKnotName] not in TailScan:
                #The leading knot has left the area around the current Knot
                UpdateKnot(LeadKnotName, KnotName, Dir, KnotNames)
            
            
def UpdateKnot(Lead, Follow, Dir, KnotNames):
    global DictOfNamesAndYX
    #Lets the Follow follow the Lead
    
    LeadPos   = DictOfNamesAndYX[Lead]
    FollowPos = DictOfNamesAndYX[Follow]
    
    if LeadPos[0] == FollowPos[0]:
        #Only moved in X direction
        UpdateX = int((LeadPos[1] - FollowPos[1])/2)
        DictOfNamesAndYX[Follow] = [FollowPos[0], FollowPos[1] + UpdateX]
        
    if LeadPos[1] == FollowPos[1]:
        #Only moved in Y direction
        UpdateY = int((LeadPos[0] - FollowPos[0])/2)
        DictOfNamesAndYX[Follow] = [FollowPos[0] + UpdateY, FollowPos[1]]
        
    
    if  LeadPos[0] != FollowPos[0] and  LeadPos[1] != FollowPos[1]:
        #Both Y and X changed, moved diagonally
        #So the Follow needs to follow diagonally
        
        MovedY = LeadPos[0] - FollowPos[0]
        MovedX = LeadPos[1] - FollowPos[1]
        
        
        #Either the Y or the X for the FollowPos will be two, since there HAS to be a diagonal gap
        #The Follow moves diagonally, so only once in Y and one in X
        #Hence, reduce the value that is is a power of two, to a value that is a power of 1
        # -2>-1     2>1
        if MovedX % 2 == 0:
            MovedX = int(MovedX / 2)
        if MovedY % 2 == 0:
            MovedY = int(MovedY / 2)

       
        
        DictOfNamesAndYX[Follow] = [FollowPos[0] + MovedY, FollowPos[1] + MovedX]


GridStats = DetermineGridInitState(Clean_Data)
GridY   = GridStats[0]   #Int
GridX   = GridStats[1]   #Int
StartYX = GridStats[2]   #Tuple

LastDir = None


KnotNamesP1 = ['H', 'T']
KnotNamesP2 = ['H', '1', '2', '3', '4', '5', '6', '7', '8', 'T']


for Problem in [KnotNamesP1, KnotNamesP2]:
    
    AllLocsOfTail = [[x for x in StartYX]]
    DictOfNamesAndYX = CreateKnotDict(Problem, StartYX)
    MoveKnots(Clean_Data, Problem, GridY, GridX)

    print(["Problem 1: ", "Problem 2: "][[KnotNamesP1, KnotNamesP2].index(Problem)] + str(len(AllLocsOfTail)))

