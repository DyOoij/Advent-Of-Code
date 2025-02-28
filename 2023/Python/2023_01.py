nput_file = open("input.txt", "r").readlines()

digits = "123456789"
alphdigits = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", ]

all_digits_in_list = []
running_total = 0

listofvalues = []

running_total_problem_2 = 0


#PROBLEM ONE

for line in input_file:
    numbers_in_entry = ""
    for char in line.replace("\n", ""):
        if char in digits:  #character IS a number
            numbers_in_entry += char
    
    outer_digits = numbers_in_entry[0] + numbers_in_entry[-1]
    all_digits_in_list.append(int(outer_digits))

for i in all_digits_in_list:
    running_total += i
print(running_total)


#PROBLEM 2

clean_data = []
listed_digits = []


for i in input_file:
    clean_data.append(i.replace("\n", ""))


def StringChopper(string):
    stringofdigits = ""
   
    for char_index in range(len(string)):
        scan_region = string[char_index:char_index + 5]
               
        for char in scan_region:
            if char.isnumeric():               
                stringofdigits += char
                
            for alph in alphdigits:
                if alph in scan_region and not scan_region[0].isnumeric() and not scan_region[1].isnumeric():
                    stringofdigits += str(alphdigits.index(alph) + 1)
    
                
                
        
    listed_digits.append(int(stringofdigits[0] + stringofdigits[-1]))
                
            
for u in clean_data:
    StringChopper(u)
    
print(sum(listed_digits))
