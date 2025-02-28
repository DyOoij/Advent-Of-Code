input_file = open("input.txt", "r")

TotalListed = []
ShortListed = []
TotalsInList = []

Totaly = 0


print(input_file.readlines().split("\n"))


for i in input_file:
   
    if i == "\n":
        TotalListed.append(ShortListed)
        ShortListed = []
    else:
        ShortListed.append(i.replace("\n", ""))

        
for j in TotalListed:
    Total = 0
    for k in j:
        Total += int(k)
    TotalsInList.append(Total)
    

TotalsInList.sort()
TotalsInList.reverse()



for p in TotalsInList[0:3]:
    print(Totaly, p)
    Totaly += p

print(Totaly)


        
