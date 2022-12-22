import collections
import pathlib
import re

import numpy as np
import matplotlib.pyplot as plt

def print_map(map_2d: np.ndarray):
    # print the map_2d char array as a full string block
    out = ""
    for line in map_2d:
        out += "".join(line) + "\n"
    print(out)
    
def plot_map(map2d: np.ndarray):
    out = np.array(list(map( np.vectorize(ord), map2d)))
    fig, ax = plt.subplots()
    ax.imshow(out)
    plt.show()
    plt.close(fig)    

def transfer_coordinates(from_: str, to_: str, x: int, y: int, cube_dim: int):
    # coordinates are in the format (y, x)
    # i definitely lost some brain cells here...
    # but it works
    if from_ == "<":
        if to_ == "<":
            return cube_dim - 1 - y, 0
        if to_ == ">":
            return y, cube_dim-1
        if to_ == "^":
            return 0, y
        if to_ == "v":
            return cube_dim-1, cube_dim-1-y
    if from_ == ">":
        if to_ == ">":
            return cube_dim - 1 - y, cube_dim-1
        if to_ == "<":
            return y, 0
        if to_ == "^":
            return 0, cube_dim-1-y
        if to_ == "v":
            return cube_dim-1, y
    if from_ == "^":
        if to_ == "^":
            return 0, cube_dim - 1 - x
        if to_ == "v":
            return cube_dim-1, x
        if to_ == "<":
            return x, 0
        if to_ == ">":
            return cube_dim - 1 - x, cube_dim - 1
    if from_ == "v":
        if to_ == "v":
            return cube_dim-1, cube_dim - 1 - x
        if to_ == "^":
            return 0, x
        if to_ == "<":
            return cube_dim - x, 0
        if to_ == ">":
            return x, cube_dim-1
    
    raise Exception("Unknown transfer coordinates", from_, to_, x, y, cube_dim)

test = False

if test: 
    lines = pathlib.Path('test.txt').read_text()
    mapviw, path = lines.split("\n\n")
    cube_dim = 4
    # the 2d map is a unfolded 3d cube
    # so we have to check which side is connected to which side of the cube
    connections = {
        1 : {
            ">" : (6, ">"),
            "<" : (3, "^"),
            "^" : (2, "^"),
            "v" : (4, "^"),
        },
        2 : {
            ">" : (3, "<"),
            "<" : (6, "v"),
            "^" : (1, "^"),
            "v" : (5, "v"),
        },
        3 : {
            ">" : (4, "<"),
            "<" : (2, ">"),
            "^" : (1, "<"),
            "v" : (5, "<"),
        },
        4 : {
            ">" : (6, "^"),
            "<" : (3, ">"),
            "^" : (1, "v"),
            "v" : (5, "^"),
        },
        5 : {
            ">" : (6, "<"),
            "<" : (3, "v"),
            "^" : (4, "v"),
            "v" : (2, "v"),
        },
        6 : {
            ">" : (1, ">"),
            "<" : (5, ">"),
            "^" : (4, ">"),
            "v" : (2, "<"),
        },
    }
    # maps = {idx: np.full((cube_dim, cube_dim), " ") for idx in range(1, 7)}
    # get the max line map length
    max_line_length = max([len(line) for line in mapviw.split("\n")])
    map_2d = np.full((len(mapviw.split("\n")), max_line_length), " ")
    for ldx, map_line in enumerate(mapviw.split("\n")):
        for i, char in enumerate(map_line):
            map_2d[ldx, i] = char
            
    # now read the input into the maps
    # the maps looks like
    #     1
    # 2 3 4
    #     5 6
    map_cubed = {}
    # these are just references to the map_2d so plotting is easier :^)
    map_cubed[1] = map_2d[cube_dim*0:cube_dim*1, cube_dim*2:cube_dim*3]
    map_cubed[2] = map_2d[cube_dim*1:cube_dim*2, cube_dim*0:cube_dim*1]
    map_cubed[3] = map_2d[cube_dim*1:cube_dim*2, cube_dim*1:cube_dim*2]
    map_cubed[4] = map_2d[cube_dim*1:cube_dim*2, cube_dim*2:cube_dim*3]
    map_cubed[5] = map_2d[cube_dim*2:cube_dim*3, cube_dim*2:cube_dim*3]
    map_cubed[6] = map_2d[cube_dim*2:cube_dim*3, cube_dim*3:cube_dim*4]
    
else:
    lines = pathlib.Path('input.txt').read_text()
    mapviw, path = lines.split("\n\n")
    cube_dim = 50
    # the 2d map is a unfolded 3d cube
    # so we have to check which side is connected to which side of the cube
    connections = {
        1 : {
            ">" : (2, "<"),
            "<" : (4, "<"),
            "^" : (6, "<"),
            "v" : (3, "^"),
        },
        2 : {
            ">" : (5, ">"),
            "<" : (1, ">"),
            "^" : (6, "v"),
            "v" : (3, ">"),
        },
        3 : {
            ">" : (2, "v"),
            "<" : (4, "^"),
            "^" : (1, "v"),
            "v" : (5, "^"),
        },
        4 : {
            ">" : (5, "<"),
            "<" : (1, "<"),
            "^" : (3, "<"),
            "v" : (6, "^"),
        },
        5 : {
            ">" : (2, ">"),
            "<" : (4, ">"),
            "^" : (3, "v"),
            "v" : (6, ">"),
        },
        6 : {
            ">" : (5, "v"),
            "<" : (1, "^"),
            "^" : (4, "v"),
            "v" : (2, "^"),
        },
    }
    # maps = {idx: np.full((cube_dim, cube_dim), " ") for idx in range(1, 7)}
    # get the max line map length
    max_line_length = max([len(line) for line in mapviw.split("\n")])
    map_2d = np.full((len(mapviw.split("\n")), max_line_length), " ")
    for ldx, map_line in enumerate(mapviw.split("\n")):
        for i, char in enumerate(map_line):
            map_2d[ldx, i] = char
            
    # now read the input into the maps
    # the maps looks like
    #   1 2
    #   3 
    # 4 5
    # 6

    map_cubed = {}
    # these are just references to the map_2d so plotting is easier :^)
    map_cubed[1] = map_2d[cube_dim*0:cube_dim*1, cube_dim*1:cube_dim*2]
    map_cubed[2] = map_2d[cube_dim*0:cube_dim*1, cube_dim*2:cube_dim*3]
    map_cubed[3] = map_2d[cube_dim*1:cube_dim*2, cube_dim*1:cube_dim*2]
    map_cubed[4] = map_2d[cube_dim*2:cube_dim*3, cube_dim*0:cube_dim*1]
    map_cubed[5] = map_2d[cube_dim*2:cube_dim*3, cube_dim*1:cube_dim*2]
    map_cubed[6] = map_2d[cube_dim*3:cube_dim*4, cube_dim*0:cube_dim*1]
    


Dir = collections.namedtuple("Dir", "x y inverse")
dirs = {
    ">": Dir( 0,  1, "<"),
    "v": Dir( 1,  0, "^"),
    "<": Dir( 0, -1, ">"),
    "^": Dir(-1,  0, "v"),
}

orders = list(dirs.keys())

path = "R" + path
path = re.findall(r"([RL])(\d+)", path)
cx, cy = 0, 0

cur_side, cur_order = 1, "^"
for rotation, steps in path:
    idx_order = orders.index(cur_order) + (1 if rotation == "R" else -1)
    cur_order = orders[idx_order  % len(orders)]    

    for _ in range(int(steps)):
        map_cubed[cur_side][cy, cx] = cur_order
        dir_order = dirs[cur_order]
        
        ny, nx = cy + dir_order.x, cx + dir_order.y
        
        if 0 <= ny < cube_dim and 0 <= nx < cube_dim:
            # if the next step is a wall, just do nothing
            if map_cubed[cur_side][ny, nx] == "#":
                break
            # if the next step is in the current map, just do it
            cx, cy = nx, ny
        else:
            new_side, new_order = connections[cur_side][cur_order]            
            ny, nx = transfer_coordinates(cur_order, new_order, nx, ny, cube_dim)
            assert 0 <= ny < cube_dim and 0 <= nx < cube_dim, f"new nx, ny {nx}, {ny}, {cur_order}-{new_order}"       
            if map_cubed[new_side][ny, nx] == "#":
                break
            cx, cy = nx, ny
            cur_side = new_side
            cur_order = dirs[new_order].inverse
    
plot_map(map_2d)
# draw the last step with @
map_cubed[cur_side][cy, cx] = "@"
# find the position of the @
cy, cx = np.where(map_2d == "@")
print("Final position:", cx+1, cy+1, "with order", orders.index(cur_order))
print("Task 2:", (cy+1) * 1000 + (cx+1) * 4 + orders.index(cur_order))
