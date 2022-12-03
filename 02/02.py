from pathlib import Path 

mapping = {
    "X" : "A",
    "Y" : "B",
    "Z" : "C",
}
score = {
    "A" : 1,
    "B" : 2,
    "C" : 3,
}
# R -> S | A -> C
# S -> P | C -> B
# P -> R | B -> A


winning = {
    "A" : "C",
    "B" : "A",
    "C" : "B",
}
loosing = {
    "B" : "C",
    "C" : "A",
    "A" : "B",
}

lines = (Path(__file__).parent / "input.txt").read_text().strip().split("\n")

points = 0

# for line in lines:
#     o, p = line.split(" ")
#     p = mapping[p]
#     pp = score[p]
#     if p == o:
#         pp += 3
#     else:
#         if p == "A" and o == "C": # Rock beats scissors
#             pp += 6
#         elif p == "B" and o == "A": # paper beat rock
#             pp += 6
#         elif p == "C" and o == "B": # scisscors beat paper
#             pp += 6
#         else:
#             pp += 0
            
#     print(line, pp)
#     points += pp
            
# print("Task 1:" ,points)

tr = {
    "A" : "R",
    "B" : "P",
    "C" : "S",
}

points = 0
for line in lines:
    o, p = line.split(" ")
    
    round_points = 0
    # you need to lose
    if p == "X":
        round_points += 0
        p = winning[o]
        print(f"Loose \t[{tr[o]}][{tr[p]}]-> " , end="")
    # you need in draw
    elif p == "Y":
        round_points += 3
        p = o
        print(f"Draw \t[{tr[o]}][{tr[p]}]-> " , end="")
    # you need to win
    elif p == "Z":
        round_points += 6
        p = loosing[o]
        print(f"Win \t[{tr[o]}][{tr[p]}]-> " , end="")
    else:
        raise Exception("I did dump shit")
    
    round_points += score[p]
    print(line, round_points)
    points += round_points
    
print("Task 2:", points)