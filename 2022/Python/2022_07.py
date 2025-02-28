with open("input.txt", "r") as Text:
    Clean_Data = []
    AllLines = Text.readlines()
    for Line in AllLines:
        Clean_Data.append(Line.replace("\n",""))
    
    
def BuildTree(Data):
    #Construct a tree out of the commands
    
    Dict_Of_Dirs = {}
    DirTracker = []
    ListedFiles = []
    
    
    
    for Line in Data:
        if Line[0] == "$":
            #Input command
            if len(ListedFiles) != 0:
                Dict_Of_Dirs["_".join(DirTracker)] = ListedFiles
                ListedFiles = []
            
            
            if Line.split(" ")[1] == "cd":
                #Directory Commands
                TargetDir = Line.split(" ")[2]
                
                
                if TargetDir != "..":
                    MoveToDir = Line.split(" ")[2]
                    DirTracker.append(TargetDir)

                
                elif TargetDir == "..":

                    
                    DirTracker = DirTracker[:-1]
                    
        else:
            #Now the console is just printing files
            
            DictKey = "_".join(DirTracker)
            
            if DictKey not in Dict_Of_Dirs:
                #Make sure Dict exists
                Dict_Of_Dirs[DictKey] = None
                
            
            FileType = Line.split(" ")[0]
            
            if FileType == 'dir':
                ListedFiles.append(Line.split(" ")[1])
            else:
                ListedFiles.append(int(Line.split(" ")[0]))
                
            
                
    #Final Listing        
    Dict_Of_Dirs["_".join(DirTracker)] = ListedFiles                
    
    return Dict_Of_Dirs      
                
                
def CountDirSize(Dict):
    
    SizeByDir = []
    DictOfPathDepths = {}
    AnotherFuckingIntermediate = []
    
    #This collects all the dir sizes of files in the dir itself, files of nested dirs not included
    for Key in Dict:
        Total = 0
        for Value in Dict[Key]:
            if type(Value) == int:
                Total += Value
        
        SizeByDir.append([Key, Total])


    for Entry in SizeByDir:
        #Collects all the directory depths of all paths, a_b_c would be depth 3, for example.
        #And stores the path in a dict by path size
        PathDepth = len(Entry[0].split("_"))

        
        #Make sure the depth size exists in the dict
        if PathDepth not in DictOfPathDepths:
            DictOfPathDepths[PathDepth] = []
            
        DictOfPathDepths[PathDepth].append(Entry[0])
    
    #This is the most nested folder
    MaxDepth = list(DictOfPathDepths.keys())[-1]
    
    
    #Now here comes the fucky part
    #We know the most deeply rooted dir, which is at level MaxDepth in the DictOfPathDepths dir
    #so we start with the most deeply rooted dirs, compound their file sizes and add the file sizes to their
    #Mother folder
    for Level in reversed(range(MaxDepth)):
        CompoundLevel = Level + 1
        
        for Vals in DictOfPathDepths[CompoundLevel]:
            #So, starting with the deepest dir, add the deepest dir and its total size to a list
            #So we get a list starting with the most nested dir and its filesize, all the way up to root and ITS filesize
            AnotherFuckingIntermediate.append([x for x in SizeByDir if Vals == x[0]][0])
    
    #Here we take the most nested dir and add its filesize to the filesize of its mother directory
    #Think of it as procedurally compounding the directories' filesize from the bottom up
    #Like collapsing a tree down to its stump
    for Help in AnotherFuckingIntermediate:             # for example:
        DirPath = Help[0]                               # a_b_c
        DirSize = Help[1]                               # 1234
        DirMom  = "_".join(DirPath.split("_")[:-1])     # a_b
        
        for i_CheckLines in range(len(AnotherFuckingIntermediate)):
            #Look through the lists of all dirs and their sizes, if you find a dir whose name corresponds to the mother
            #Add the size of your current dir, to the mother dir
            #This compounds the filesizes upwards towards the root folder
            if AnotherFuckingIntermediate[i_CheckLines][0] == DirMom:
                AnotherFuckingIntermediate[i_CheckLines][1] += DirSize
                
    #Now we have a list of all directories and their filesizes, child directories' file sizes included!
    print(AnotherFuckingIntermediate)
    return AnotherFuckingIntermediate
        
    
def SolveP1(DirsAndSizes):
    Limit = 100000
    Total = 0
    
    for Entry in DirsAndSizes:
        if Entry[1] <= Limit:
            Total += Entry[1]
    
    return Total

        
def SolveP2(DirsAndSizes):
    TotalDiskSpace = 70000000
    NeededSpace    = 30000000
    FreeSpace      = TotalDiskSpace - DirsAndSizes[-1][1]
    NeedToRemove   = NeededSpace - FreeSpace
    
    for Dir in DirsAndSizes:
        if Dir[1] >= NeedToRemove:
            break
    
    
    
    return Dir
    



        
                

                

                
        
    

            
DictedData = BuildTree(Clean_Data)
SortedAndSized = CountDirSize(DictedData)

print(SolveP1(SortedAndSized))
print(SolveP2(SortedAndSized))


        
    
