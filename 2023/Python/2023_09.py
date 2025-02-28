from datetime import datetime
from collections import Counter



#print("Start of script: ", str(datetime.now()).split(" ")[1][:-7])

input_file = open("input.txt", "r").readlines()
clean_data = []
Overall_Values = []
Second_Vals = []


for i in input_file:
    intermediate_list = i.replace('\n', '').split(' ')
    
    for j_i in range(len(intermediate_list)):
        intermediate_list[j_i] = int(intermediate_list[j_i])
    clean_data.append(intermediate_list)



def SetupDict(List_of_Values):
    Dict_With_Levels = {0 : List_of_Values}
    
    for i in range(len(Dict_With_Levels[0])):
        add_to_dict = []
    
        for j in range(len(Dict_With_Levels[i])):
            if j + 1 < len(Dict_With_Levels[i]):
                add_to_dict.append(Dict_With_Levels[i][j+1] - Dict_With_Levels[i][j])
            
            Dict_With_Levels[i+1] = add_to_dict
        
        if len(set(Dict_With_Levels[i+1])) == 1 and 0 in Dict_With_Levels[i+1]:

            break
        
    #for i in Dict_With_Levels:
     #   print(i, Dict_With_Levels[i])
        

        
    return Dict_With_Levels
    
def SummateTerminals(Level_Dict):
    Total_Sum = 0
    for i in range(len(Level_Dict)):
        Total_Sum += Level_Dict[i][-1]   
    return Total_Sum


def BuildFromBottom(Eval_Dict):
    
    Iterate_PLS = []
    Len_Dict = len(Eval_Dict)

    
    for Dict_Key in range(Len_Dict):
        Iterate_PLS.append(Eval_Dict[Dict_Key][0])
        
    Iterate_PLS.reverse()

    Return_Sum = Iterate_PLS[0]
    
    if len(Iterate_PLS) % 2 == 0:
        
    
        for number_i in range(len(Iterate_PLS)):
            if number_i != 0:
                if number_i % 2 == 0:
                    Return_Sum -= Iterate_PLS[number_i]
                
                else:
                    Return_Sum += Iterate_PLS[number_i]
                    
                    
    else:
        for number_i in range(len(Iterate_PLS)):
            if number_i != 0:
                if number_i % 2 == 0:
                    Return_Sum += Iterate_PLS[number_i]
                
                else:
                    Return_Sum -= Iterate_PLS[number_i]
        

    return Return_Sum
                
    
    
    



    
    
    
     



for i in clean_data:
    Overall_Values.append(SummateTerminals(SetupDict(i)))
    
for j in clean_data:
    Second_Vals.append(BuildFromBottom(SetupDict(j)))
    

   
print("Problem 1: ", sum(Overall_Values))
print("Problem 2: ", sum(Second_Vals))







    



    

    
