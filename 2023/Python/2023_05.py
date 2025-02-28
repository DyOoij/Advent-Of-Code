from datetime import datetime

print("Start of script: ", str(datetime.now()).split(" ")[1])

input_file = open("input.txt", "r").readlines()
intermediate_list = []
source_list_cutoff = []
clean_data = []


for j in input_file:
    if j.replace("\n", "") != '':
        intermediate_list.append(j.replace("\n", ""))
        
for item_i in range(len(intermediate_list)):
    if intermediate_list[item_i][0].isnumeric() == False:
        source_list_cutoff.append(item_i)
    
for cutoff in source_list_cutoff:
    instructions = []
    if source_list_cutoff.index(cutoff) + 1 != len(source_list_cutoff):
        cap_to = source_list_cutoff[source_list_cutoff.index(cutoff) + 1]
        for numbers in intermediate_list[cutoff + 1 :cap_to]:
            instructions.append(numbers)
    else:
        for numbers in intermediate_list[cutoff + 1 :]:
            instructions.append(numbers)
    clean_data.append([intermediate_list[cutoff], instructions])



#problem 1

All_locations = []
    
def TranslateRanges(data_input, seed):
    for collection_of_nums in data_input[1]:
        All_numbers = collection_of_nums.split(" ")
        
        Destination = int(All_numbers[0])
        Source      = int(All_numbers[1])
        Range       = int(All_numbers[2])
        

        
        if seed in range(Source, Source + Range):
            return int(seed + (Destination - Source))

            break

    return int(seed)


    
    
    
Seeds = []
for seed in clean_data[0][0].split(": ")[1].split(" "):
    Seeds.append(int(seed))



for seed in Seeds:
    for map_step in range(len(clean_data)):
        if map_step != 0:
            seed = TranslateRanges(clean_data[map_step], seed)

    All_locations.append(seed)
            
print("Problem 1: ", min(All_locations))
print()    

#problem 2
#Reverse it

#Setup ranges
SeedStart = []
SeedStop = []

list_of_seed_nums = clean_data[0][0].split(": ")[1].split(" ")
for number_i in range(len(list_of_seed_nums)):
    
    if number_i % 2 == 0:
        SeedStart.append(int(list_of_seed_nums[number_i]))
    else:
        SeedStop.append(int(list_of_seed_nums[number_i]) + SeedStart[-1])
        
"""
for i in range(len(SeedStart)):
    for j in range(SeedStart[i], SeedStop[i]):
        print(j, end = ", ")
    print()
    
"""
    



def RevTranslateRanges(data_input, seedf):
    for collection_of_numsf in data_input[1]:
        All_numbersf = collection_of_numsf.split(" ")

        Destination = int(All_numbersf[0])
        Source      = int(All_numbersf[1])
        Range       = int(All_numbersf[2])

        if seedf in range(Destination, Destination + Range):
            return int(seedf + (Source - Destination ))

    return int(seedf)




for Loc in range(0, 9999999999):
    Initial_Loc = Loc
    for map_step in range(len(clean_data)):
        if map_step != 0:
            Loc = RevTranslateRanges(clean_data[-map_step], Loc)
    
    Eventual_Seed = Loc
    
    for range_set_i in range(len(SeedStart)):
        Min = SeedStart[range_set_i]
        Max = SeedStop[range_set_i]
        
        if Eventual_Seed in range(Min, Max):
            #We have the LOWEST location possible that results in a seed which we have a range for
            print("Lowest location with seed in range: ", Initial_Loc)
            print("End of script:   ", str(datetime.now()).split(" ")[1])
            quit()
            

            

        

        

        
            






        






    






            

            
            
        
    
