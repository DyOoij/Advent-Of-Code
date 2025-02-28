input_file = open("input.txt", "r").readlines()

clean_data = []

running_game_ID_score = 0

RGB_Max = [12, 13, 14]

for i in input_file:
    clean_data.append(i.replace("\n", ""))


#problem 1
for line in clean_data:
    
    counter_of_valid_rounds = 0
    
    game_ID = line.split(":")[0].split(" ")[1]
    game_all_rounds = line.split(":")[1].split(";")
    

    for game_round in game_all_rounds:
        
        result_per_round = game_round.split(",")
        RGB_result = [0,0,0]
        for result in result_per_round:

            draw = result[1:].split(" ")  #[number, colour]
            
            if draw[1] == "red":
                RGB_result[0] = draw[0]    
            elif draw[1] == "green":
                RGB_result[1] = draw[0]  
            elif draw[1] == "blue":
                RGB_result[2] = draw[0]
        #print(len(game_all_rounds))
        #now test it lmao
        
        counter_of_valid_draws = 0
        for RGB_result_index in range(len(RGB_result)):
            if int(RGB_result[RGB_result_index]) <= RGB_Max[RGB_result_index]:
                counter_of_valid_draws += 1
        if counter_of_valid_draws == 3:
            counter_of_valid_rounds += 1
             
        if counter_of_valid_rounds == len(game_all_rounds):
            running_game_ID_score += int(game_ID)

print("Valid game IDs: ", running_game_ID_score)
    

#problem 2
total_power = 0

for line in clean_data:    
    game_ID = line.split(":")[0].split(" ")[1]
    game_all_rounds = line.split(":")[1].split(";")
    
    RGB_result = [0,0,0]
    
    for game_round in game_all_rounds:
        result_per_round = game_round.split(",")
        for result in result_per_round:
            

            draw = result[1:].split(" ")  #[number, colour]
            if draw[1] == "red" and int(draw[0]) > RGB_result[0]:
                RGB_result[0] = int(draw[0])    
            elif draw[1] == "green" and int(draw[0]) > RGB_result[1]:
                RGB_result[1] = int(draw[0])  
            elif draw[1] == "blue" and int(draw[0]) > RGB_result[2]:
                RGB_result[2] = int(draw[0])
    
    power = RGB_result[0] * RGB_result[1] * RGB_result[2]
    total_power += power
    
    
print("Power of games: ", total_power)
        
    
