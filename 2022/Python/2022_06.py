input_file = open("input.txt", "r").readlines()

#problem 1
for i in input_file:
    for j in range(len(i)):
        if  len(set(i[j:j+4])) == 4:
            print(j+4)
            print(i[j:j+4])
            break
#problem 2        
for u in input_file:
    for v in range(len(u)):
        if  len(set(u[v:v+14])) == 14:
            print(v+14)
            print(u[v:v+14])
            break
