import copy
import pathlib
import numpy as np
# values can be double
encrypted = list(map(int, pathlib.Path('input.txt').read_text().splitlines()))

original_order = copy.deepcopy(encrypted)
original_index = np.arange(len(encrypted))

len_encrypted = len(encrypted)

for idx, current_number in enumerate(original_order):
    idx_cn = original_index[idx]    
    encrypted.pop(idx_cn)
    
    # compute the new position, if it's out of bounds, wrap around
    to_idx = idx_cn + current_number
    to_idx = to_idx - int(to_idx / len(encrypted)) * len(encrypted)
    
    to_idx -= 1 if current_number < 0 else 0
    to_idx = (len_encrypted + to_idx) if to_idx < 0 else to_idx
    
    original_index[np.where(original_index <= to_idx)] -= 1
    original_index[idx] = to_idx
    
    # insert the current number at the new position
    encrypted.insert(to_idx, current_number)
    
# find the index of value 0 and then take the 1000th number, the 2000th number, and the 3000th number 
start_idx = encrypted.index(0)
idx_1000 = (start_idx + 1000) % len_encrypted
idx_2000 = (start_idx + 2000) % len_encrypted
idx_3000 = (start_idx + 3000) % len_encrypted

number_1000 = encrypted[idx_1000]
number_2000 = encrypted[idx_2000]
number_3000 = encrypted[idx_3000]

print("Task 1:", number_1000 + number_2000 + number_3000)