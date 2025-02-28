from datetime import datetime
from collections import Counter


#print("Start of script: ", str(datetime.now()).split(" ")[1][:-7])

input_file = open("input.txt", "r").readlines()
Total = 0

def CleanBlocks(raw, separator):
    #A function written specifically to parse input files
    #This function reads the input line by line and separates it into blocks
    #Based on what divider is given through >separator (like \n or ----- or ~~~~~~)
    #Returns the block as a list of a list of lines:
    #        [['L1, L2, L3', 'L1, L2, L3'], ['L4, L5', 'L4, L5']]
    Clean_Return = []
    Dividers_i = [0]
    All_Lines = []
    
    for Line in range(len(raw)):
        if raw[Line] != separator:
            All_Lines.append(raw[Line].replace('\n', ''))
        else:
            All_Lines.append('BREAK')
            Dividers_i.append(Line + 1)
            
    for Div_i in range(len(Dividers_i)):
        if Div_i < len(Dividers_i) - 1:
            Clean_Return.append(All_Lines[Dividers_i[Div_i]:Dividers_i[Div_i + 1] - 1])
        else:
            Clean_Return.append(All_Lines[Dividers_i[Div_i]:])      
    
    return Clean_Return


def FlipBlock(Block):
    #Just flips the block so X becomes Y, easier to handle lines in X direction that way
    Rotated_Block = []
    Height = len(Block)
    
    for TopRow_i in range(len(Block[0])):
        RowDown = ''
        for LookDown in range(Height):
            RowDown += Block[LookDown][TopRow_i]
        Rotated_Block.append(RowDown)
    return Rotated_Block


def FindMirror(Block, Points):
    #Split the list and check the smaller half against the bigger half
    #If all values overlap: Mirror
    
    for PossibleMirror in range(len(Block)):
        TopHalf    = Block[:PossibleMirror]
        Toppy = TopHalf.copy()
        BottomHalf = Block[PossibleMirror:]

        
        if len(TopHalf) != 0:
        
            if len(BottomHalf) > len(TopHalf):
                Toppy.reverse()
                if Toppy == BottomHalf[:len(Toppy)]:
                    return PossibleMirror * Points
            
            elif len(BottomHalf) == len(TopHalf):
                Toppy.reverse()
                if Toppy == BottomHalf:
                    return PossibleMirror * Points
    
            elif len(BottomHalf) < len(TopHalf):
                Toppy.reverse()
                if Toppy[:len(BottomHalf)] == BottomHalf:
                    return PossibleMirror * Points
    return 0

def Diffy(Lists1, Lists2):
    Diffy = 0
    for Line_i in range(len(Lists1)):
        Compare1 = Lists1[Line_i]
        Compare2 = Lists2[Line_i]
        
        for char_i in range(len(Compare1)):
            if Compare1[char_i] != Compare2[char_i]:
                Diffy += 1
    return Diffy



def FindSmudge(Block, Points):
    #Split the list and check the smaller half against the bigger half
    #If all values overlap: Mirror
    
    for PossibleMirror in range(len(Block)):
        TopHalf    = Block[:PossibleMirror]
        Toppy = TopHalf.copy()
        BottomHalf = Block[PossibleMirror:]

        
        if len(TopHalf) != 0:
            
            if len(BottomHalf) > len(TopHalf):
                Toppy.reverse()
                if Diffy(Toppy, BottomHalf[:len(Toppy)]) == 1:
                    if FindMirror(Block, Points) != PossibleMirror * Points:
                        return PossibleMirror * Points
            
            elif len(BottomHalf) == len(TopHalf):
                Toppy.reverse()
                if Diffy(Toppy, BottomHalf) == 1:
                    if FindMirror(Block, Points) != PossibleMirror * Points:
                        return PossibleMirror * Points
    
            elif len(BottomHalf) < len(TopHalf):
                Toppy.reverse()
                if Diffy(Toppy[:len(BottomHalf)], BottomHalf) == 1:
                    if FindMirror(Block, Points) != PossibleMirror * Points:
                        return PossibleMirror * Points
    return 0
    
            

            
        


            

            

        
        
        



clean_data = CleanBlocks(input_file, '\n')
data_with_mirrors = []

Total = 0
Total2 = 0

for Block in clean_data:
    Total += FindMirror(Block, 100)
    Total += FindMirror(FlipBlock(Block), 1)
    
print("Problem 1: ", Total)

for Block in clean_data:
    Total2 += FindSmudge(Block, 100)
    Total2 += FindSmudge(FlipBlock(Block), 1)
    
print("Problem 2: ", Total2)


       










    
        
            
        
        


    
    







    



    
