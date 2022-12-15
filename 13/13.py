import pathlib
from typing import Union

def compare_elements(left: Union[list,int], right: Union[list,int]) -> int:    
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return 0
        
        if left < right:
            return 1
        
        if left > right:
            return -1
        
    elif isinstance(left, list) and isinstance(right, list):
        return compare_lists(left=left, right=right)
    
    else:
        # one of them has to be a int and the other a list!
        if isinstance(left, int):
            return compare_lists(left=[left], right=right)
        else:
            return compare_lists(left=left, right=[right])

def compare_lists(left: list, right:list) -> int:  
    for l, r in zip(left, right):
        result = compare_elements(l, r)
        # just for clearity
        if result != 0:
            return result    
    # if we end because left is smaller then this is a RIGHT case!
    if len(left) < len(right):
        return 1
    elif len(left) > len(right):
        return -1
    return 0


# task1
file_name = "input.txt"

pairs = pathlib.Path(file_name).read_text().split("\n\n")
correct_pairs = []
for idx, p in enumerate(pairs):
    left, right = p.split("\n")
    result = compare_lists(left=eval(left), right=eval(right))
    if result == 1:
        correct_pairs.append(idx + 1)
        
print("Task 1", sum(correct_pairs))

#task2
from functools import cmp_to_key
lines = pathlib.Path(file_name).read_text().split("\n")

connected_lines = [eval(line) for line in lines if line.strip()]
connected_lines.append([[2]])
connected_lines.append([[6]])
connected_lines = sorted(connected_lines, key=cmp_to_key(compare_lists), reverse=True)

pos_1 = connected_lines.index([[2]]) + 1 # fix start index of zero
pos_2 = connected_lines.index([[6]]) + 1 # fix start index of zero

print("Task 2", pos_1 * pos_2)