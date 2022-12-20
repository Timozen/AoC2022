import pathlib
from collections import deque
import numpy as np

# values can be double
encrypted = list(map(int, pathlib.Path('input.txt').read_text().splitlines()))
decryption_key = 811589153

# multiply all values by the decryption key
for idx, value in enumerate(encrypted):
    encrypted[idx] = value * decryption_key
    
len_encrypted = len(encrypted)

encrypted = deque(encrypted)
original_index = deque(np.arange(len(encrypted)).tolist())

for _ in range(10):
    for idx in range(len_encrypted):
        position = original_index.index(idx)
        
        encrypted.rotate(position * -1)
        value_at_position = encrypted.popleft()
        encrypted.rotate(value_at_position * -1)      # rotate by the actual value back
        encrypted.appendleft(value_at_position)
        
        original_index.rotate(position * -1)
        index_at_position = original_index.popleft()
        original_index.rotate(value_at_position * -1) # rotate by the actual value back
        original_index.appendleft(index_at_position)
        
start_idx = encrypted.index(0)
idx_1000 = (start_idx + 1000) % len_encrypted
idx_2000 = (start_idx + 2000) % len_encrypted
idx_3000 = (start_idx + 3000) % len_encrypted

number_1000 = encrypted[idx_1000]
number_2000 = encrypted[idx_2000]
number_3000 = encrypted[idx_3000]

print("Task 2:", number_1000 + number_2000 + number_3000)