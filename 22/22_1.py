import pathlib
import numpy as np

def print_map(map_2d: np.ndarray):
    # print the map_2d char array as a full string block
    out = ""
    for line in map_2d:
        out += "".join(line) + "\n"
    print(out)


lines = pathlib.Path('input.txt').read_text()

map, path = lines.split("\n\n")

# get the max line map length
max_line_length = max([len(line) for line in map.split("\n")])

map_2d = np.full((len(map.split("\n")), max_line_length), " ")

pc_x, pc_y = None, None

for ldx, map_line in enumerate(map.split("\n")):
    for i, char in enumerate(map_line):
        if ldx == 0 and pc_x is None and char != " ":
            pc_y, pc_x = ldx, i

        map_2d[ldx, i] = char

# now we start in the top left corner of the map (symbol which is not " ")
# (y, x) is the coordinate system order
order_dirs = {
    ">": ( 0,  1),
    "<": ( 0, -1),
    "^": (-1,  0),
    "v": ( 1,  0),
}
orders = [">", "v", "<", "^"]

path = "N" + path
# split the path into rotation and steps with regex
import re

path = re.findall(r"([NRL])(\d+)", path)
print(path)
order_idx = 0

height, width = map_2d.shape

for rotation, steps in path:
    # first rotate the order, but assure wrap around
    if rotation == "R":
        order_idx = (order_idx + 1) % len(orders)
    elif rotation == "L":
        order_idx = (order_idx - 1) % len(orders)
        
    dirs = order_dirs[orders[order_idx]]
    
    # now move the steps in the direction
    # if we hit a wall ("#"), we stop
    # if we reach the end (" "), we continue on the other side of the map

    for _ in range(int(steps)):
        # check for wrapping around the map
        ny, nx = pc_y + dirs[0], pc_x + dirs[1]
        if nx == width:
            nx = 0
        if nx == -1:
            nx = width - 1
        if ny == height:
            ny = 0
        if ny == -1:
            ny = height - 1

        bnx, bny = nx, ny
        while map_2d[ny, nx] == " ":
            ny, nx = ny + dirs[0], nx + dirs[1]
            if nx == width:
                nx = 0
            if nx == -1:
                nx = width - 1

            if ny == height:
                ny = 0
            if ny == -1:
                ny = height - 1
            
                    
        if map_2d[ny, nx] == "#":
            break
        
        map_2d[pc_y, pc_x] = orders[order_idx]
        pc_x, pc_y = nx, ny            

print_map(map_2d)
print("Final position:", pc_x+1, pc_y+1, "with order", order_idx)
print("Task 1:", (pc_y+1) * 1000 + (pc_x+1) * 4 + order_idx)