import pathlib

lines = (pathlib.Path(__file__).parent / "input.txt").read_text().split("\n")
# Task 1
total_priority = 0
for line in lines:
    priority = 0
    
    length_of_rucksack = len(line) // 2
    compart_1, compart_2 = line[:length_of_rucksack], line[length_of_rucksack:]
    double_item = set(compart_1).intersection(compart_2).pop()
    
    if double_item.islower():
        priority = ord(double_item) - 96
    elif double_item.isupper():
        priority = ord(double_item) - 65 + 27
        
    # print(double_item, priority)
    total_priority += priority
print("Task 1", total_priority)
        
# Task 2
def group_by_n(iterable: list, n: int=3):
    for i in range(0, len(iterable), n):
        yield iterable[i : i+n]

total_priority = 0 
for group in group_by_n(lines, n=3):
    priority = 0
    badge_item = set.intersection(*map(set, group)).pop()
    
    if badge_item.islower():
        priority = ord(badge_item) - 96
    elif badge_item.isupper():
        priority = ord(badge_item) - 65 + 27
        
    #print(badge_item, priority)
    total_priority += priority
print("Task 2", total_priority)
    
    
    
    
