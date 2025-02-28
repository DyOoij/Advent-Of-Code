input_file = open("input.txt", "r").readlines()

from datetime import datetime

start = str(datetime.now()).split(" ")[1]

clean_data = []

for i in input_file:
    clean_data.append(i.replace("\n", ""))

Counter = 0

RunningTotal = 0


def NumbersOfWins(data):
    winnumbers = []
    yournumbers = []
    
    
    setofwins = data.split(":")[1].split("|")[0]
    setofnums = data.split(":")[1].split("|")[1]
    
    for num_1 in setofwins.split(" "):
        if num_1.isnumeric():
            winnumbers.append(int(num_1))
    for num_2 in setofnums.split(" "):
        if num_2.isnumeric():
            yournumbers.append(int(num_2))
        
    
    return len(winnumbers + yournumbers) - len(set(winnumbers + yournumbers))   
    
for line in clean_data:
    overlap = NumbersOfWins(line)
    if overlap != 0:
        RunningTotal += (2** (overlap-1))

        
        
print("Problem 1: ", RunningTotal)
print()
    


#problem 2

Listing_Cards = [] #CardNum, Amount, Wins

for entry in clean_data:
    token = "Card " + entry.split(":")[0].replace(" ", "").split("Card")[1]
    Listing_Cards.append([token, 1, int(NumbersOfWins(entry))])
    
for card in Listing_Cards:
    print(card)
    for iterate in range(card[1]):
        if card[2] != 0:
            card_num = int(card[0].split(" ")[1])
        
            for next_card in range(1, card[2] + 1):
                update_token = "Card " + str(card_num + next_card)
                
                for iterate_over_i in range(len(Listing_Cards)):
                    if Listing_Cards[iterate_over_i][0] == update_token:
                        Listing_Cards[iterate_over_i][1] += 1
running_help = 0                       
for i in Listing_Cards:
    running_help += i[1]

end = str(datetime.now()).split(" ")[1]

print(running_help)
print("Start compiling: ", start)
print("End compiling:   ", end)
                        
                

            

      

                        
            


    

        

    

    







    






            

            
            
        
    
