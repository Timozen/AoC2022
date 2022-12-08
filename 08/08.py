from pathlib import Path

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("WebAgg")


lines = (Path(__file__).parent / "input.txt").read_text().split("\n")

# 0... shortest
# 9... highest

# visible only if all tree to all edges (up, down, left, right) are shorter!
# around the edge 100% visible :)

# task 1: how many total visible!

forest = np.array([list(line) for line in lines], dtype=np.int8)
visible_trees = np.zeros_like(forest) - 1
visible_trees[:,  0] = forest[:,  0]
visible_trees[:, -1] = forest[:, -1]
visible_trees[ 0, :] = forest[ 0, :]
visible_trees[-1, :] = forest[-1, :]

# check all the outher locations
for loc_x in range(1, len(forest) - 1):
    for loc_y in range(1, len(forest) - 1):
        tree_height = forest[loc_y, loc_x]
        
        l = np.all(forest[loc_y, :loc_x]   < tree_height)
        r = np.all(forest[loc_y, loc_x+1:] < tree_height)
        t = np.all(forest[:loc_y, loc_x]   < tree_height)
        b = np.all(forest[loc_y+1:, loc_x] < tree_height)
        
        # print(f"x:{loc_x},y:{loc_y} [{tree_height}] L:{l:^1}, R:{r:^1}, T:{t:^1}, B:{b:^1}")
        cond = l or r or t or b
        visible_trees[loc_y, loc_x] = tree_height if cond else -1
        
        # if loc_x == 2 and loc_y == 2:
        #     print("L", trees_to_l)
        #     print("R", trees_to_r)
        #     print("B", trees_to_b)
        #     print("T", trees_to_t)
        
print("Task 1, total visible trees ", np.sum(visible_trees > -1))
# fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))        

# ax[0].matshow(forest, vmin=0, vmax=9)
# # for (i, j), z in np.ndenumerate(forest):
# #     ax[0].text(j, i, '{:0.1f}'.format(z), ha='center', va='center')
    
# ax[1].matshow(visible_trees, vmin=-1, vmax=9)
# plt.show()

# check all the outher locations

scenic_scores = np.zeros_like(forest, dtype=np.int32)
for loc_x in range(len(forest)):
    for loc_y in range(len(forest)):
        tree_height = forest[loc_y, loc_x]
        
        l = 0
        r = 0
        t = 0
        b = 0
        
        # going left..
        temp_idx = loc_x - 1
        while 0 <= temp_idx:
            l +=1
            if forest[loc_y, temp_idx] >= tree_height:
                break
            temp_idx -= 1
            
        # going right...
        temp_idx = loc_x + 1
        while temp_idx < len(forest):
            r += 1
            if forest[loc_y, temp_idx] >= tree_height:
                break
            temp_idx += 1
            
        # going top...
        temp_idy = loc_y - 1
        while 0 <= temp_idy:
            t += 1
            if forest[temp_idy, loc_x] >= tree_height:
                break
            temp_idy -= 1
        
        # going bottom...
        temp_idy = loc_y + 1
        while temp_idy < len(forest):
            b += 1
            if forest[temp_idy, loc_x] >= tree_height:
                break
            temp_idy += 1
        
        score = l * r * t * b
        print(f"x:{loc_x},y:{loc_y} [{tree_height}|{score}|{scenic_scores[loc_y, loc_x]}] L:{l}, R:{r}, T:{t}, B:{b}")
        scenic_scores[loc_y, loc_x] = score
        # if loc_x == 2 and loc_y == 3:            

        
        # print(f"x:{loc_x},y:{loc_y} [{tree_height}] L:{l:^1}, R:{r:^1}, T:{t:^1}, B:{b:^1}")
        # cond = l or r or t or b
        # visible_trees[loc_y, loc_x] = tree_height if cond else -1
        
        # if loc_x == 2 and loc_y == 2:
        #     print("L", trees_to_l)
        #     print("R", trees_to_r)
        #     print("B", trees_to_b)
        #     print("T", trees_to_t)
        
print(scenic_scores.max())
print(scenic_scores[43, 97])