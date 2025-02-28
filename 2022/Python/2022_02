nput_file = open("input.txt", "r").readlines()

#Rock, paper, scissors



#Problem one

problem_one = []

points = ['X', 'Y', 'Z']

wins = ['X Y', 'Y Z', 'Z X']
losses = ['X Z', 'Z Y', 'Y X']

TotalScore = 0

for i in input_file:
    problem_one.append(i.replace("\n", "").replace("A", "X").replace("B", "Y").replace("C", "Z"))
    
for j in problem_one:
    #points for choosing your element
    TotalScore += points.index(j[-1])+1
    
    #points for resolving
    if j in wins:
        TotalScore += 6
    elif j in losses:
        TotalScore += 0
    else:
        TotalScore += 3
    
print(TotalScore)

problem_two = []
p2TotalScore = 0

for i in input_file:
    problem_two.append(i.replace("\n", ""))
    
p2points = ['A', 'B', 'C']
p2resolve = ['X', 'Y', 'Z']

dictresolve = {'X' : ['A C', 'B A', 'C B'],
               'Y' : ['A A', 'B B', 'C C'],
               'Z' : ['A B', 'B C', 'C A']
    }
    
for g in problem_two:
    
    #points for resolving
    p2TotalScore += p2resolve.index(g[-1]) * 3
    
    #points for element
    for possible in dictresolve[g[-1]]:
        if g[0] == possible[0]:
            p2TotalScore += (p2points.index(possible[-1]) + 1)

print(p2TotalScore)
    
