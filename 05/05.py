import copy
from pathlib import Path

lines = (Path(__file__).parent / "input.txt").read_text()

stack_layers, moving_orders = lines.split("\n\n")

# reverse the order of the layers for easier parsing
stack_layers = stack_layers.split("\n")[::-1]

# the the stack ids and where to find the loaded item locationszs
stack_ids = list(map(int, list(stack_layers[0].replace(" ", ""))))
stack_array_idx = {idx : stack_layers[0].index(str(idx)) for idx in stack_ids}

# create the stacks and put the laoded items into them!
stacks = {idx : [] for idx in stack_ids}
for layer in stack_layers[1:]:
    for idx_k, idx_v in stack_array_idx.items():
        loaded_item = layer[idx_v]
               
        if loaded_item == " ":
            continue
        stacks[idx_k].append(loaded_item)

print(stacks)

stacks_2 = copy.deepcopy(stacks)

# task 1
# parse the order!
moving_orders = moving_orders.strip().split("\n")
for order in moving_orders:
    move_amount, from_, to_ = map(int, filter(lambda x: x.isdecimal(), order.split(" ")))    
    for _ in range(move_amount):
        stacks[to_].append(stacks[from_].pop())
        
print(stacks)
output = "".join([stacks[idx].pop() for idx in stack_ids])
print("Task 1", output)


# task 2 
stacks = stacks_2
for order in moving_orders:
    move_amount, from_, to_ = map(int, filter(lambda x: x.isdecimal(), order.split(" ")))
    
    temp_movement = [stacks[from_].pop() for _ in range(move_amount)]
    temp_movement.reverse()
    stacks[to_].extend(temp_movement)
    
output = "".join([stacks[idx].pop() for idx in stack_ids])
print("Task 2", output)