from datetime import datetime
from collections import Counter

#print("Start of script: ", str(datetime.now()).split(" ")[1])

input_file = open("input.txt", "r").readlines()

clean_data = []
dict_with_prio = {10: [], 8: [], 6: [], 5: [], 4: [], 3: [], 2: []}

#Problem 1

hex_replace = ['2', '2',
               '3', '3',
               '4', '4',
               '5', '5',
               '6', '6',
               '7', '7',
               '8', '8',
               '9', '9',
               'T', 'a',
               'J', 'b',
               'Q', 'c',
               'K', 'd',
               'A', 'e',
               ]

hex_replace2 = ['J', '1',
               '2', '2',
               '3', '3',
               '4', '4',
               '5', '5',
               '6', '6',
               '7', '7',
               '8', '8',
               '9', '9',
               'T', 'a',
               'Q', 'b',
               'K', 'c',
               'A', 'd',
               ]

ranked_points = []
Running_Total = 0


for i in input_file:
    clean_data.append(i.replace("\n", "").split(" "))
    

def PrioSets(hand):
    set_prio = len(set(hand)) * 2
    set_hand = dict(Counter(hand))

    if set_prio == 4: #Either Four of Kind OR Full house
        for h in set_hand:
            if set_hand[h] == 4: #This is FOUR of kind
                set_prio -= 1
                break
       
    if set_prio == 6: #Either Three of Kind OR Two Pair
        for h in set_hand:
            if set_hand[h] == 3: #This is THREE of kind
                set_prio -= 1
                break

    return set_prio

def PrioSets2(hand):
    set_prio = len(set(hand)) * 2
    set_hand = dict(Counter(hand))
    
    if 'J' in hand:
        
        if set_prio == 2:   #Fives of J
            set_prio = 2
        elif set_prio == 4: #Always Fives with aaaa + j
            set_prio = 2
        elif set_prio == 6: #Either Fours or FullH
             if hand.count('J') == 1: #special case for J1 with either Fours or FullH
                 
                 for h in set_hand:        
                    if set_hand[h] == 3: #Will resolve to J aaa b > Fours
                        set_prio = 3
                        return set_prio
                        break
                    
                    elif set_hand[h] == 2: #Will resolve to J aa bb > FullH
                        set_prio = 4
                        return set_prio
                        break

             if hand.count('J') == 2:
                 for h in set_hand:
                     if set_hand[h] == 2: #Will resolve to JJ aa b > FullH
                         set_prio = 3

                 
                 
             else:
                set_prio = 3
        elif set_prio == 8:
            set_prio = 5
        else:
            set_prio = 8
        

            
    
    else:

        if set_prio == 4: #Either Four of Kind OR Full house
            for h in set_hand:
                if set_hand[h] == 4: #This is FOUR of kind
                    set_prio -= 1
                    break
       
        if set_prio == 6: #Either Three of Kind OR Two Pair
            for h in set_hand:
                if set_hand[h] == 3: #This is THREE of kind
                    set_prio -= 1
                    break

    return set_prio


def ConvertToHex(HandPoint):

    init_hand = HandPoint[0]
    hex_hand = ""
    for digit in init_hand:

        hex_hand += hex_replace[hex_replace.index(digit) + 1]
            
            #the INT(x, 16) already convert the hexadecimal to a decimal number
    return [int(hex_hand, 16), HandPoint[1]]

def ConvertToHex2(HandPoint):
    init_hand = HandPoint[0]
    hex_hand = ""
    for digit in init_hand:

        hex_hand += hex_replace2[hex_replace2.index(digit) + 1]
            
            #the INT(x, 16) already convert the hexadecimal to a decimal number
    return [int(hex_hand, 16), HandPoint[1]]



for entry in clean_data:
    dict_with_prio[PrioSets(entry[0])].append(ConvertToHex(entry))
    
    
for i in dict_with_prio:
    for j in sorted(dict_with_prio[i], key=lambda x: int(x[0])):
        ranked_points.append(j[1])

for index_i in range(len(ranked_points)):
    Running_Total += (int(ranked_points[index_i]) * (index_i + 1))
    
print("Problem 1: ", Running_Total)


#Problem 2
dict_with_prio2 = {10: [], 8: [], 6: [], 5: [], 4: [], 3: [], 2: []}

ranked_points2 = []
Running_Total2 = 0



for entry in clean_data:
    dict_with_prio2[PrioSets2(entry[0])].append(ConvertToHex2(entry))

for i in dict_with_prio2:
    for j in sorted(dict_with_prio2[i], key=lambda x: int(x[0])):
        ranked_points2.append(j[1])

for index_i in range(len(ranked_points2)):
    Running_Total2 += (int(ranked_points2[index_i]) * (index_i + 1))
    
print("Problem 2: ", Running_Total2)
    

Title = 0
print()

for i in dict_with_prio2:
    types = ["None", "Two of a Kind", "Two Pairs", "Three of a Kind", "Full House", "Four of a Kind", "Five of a Kind"]
    
    print("-----------------------", types[Title], "-----------------------")
    for j in sorted(dict_with_prio2[i], key=lambda x: int(x[0])):
        for g in range(len(clean_data)):
            if clean_data[g][1] == j[1]:
                print(clean_data[g][0], end = ",")
    print()
    Title += 1
    print()
    



    

    
