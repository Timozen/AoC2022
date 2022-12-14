import pathlib
import numpy as np
import cv2

# Task 1
lines = pathlib.Path("test.txt").read_text().split("\n")
stones = []
for line in lines:
    stones.append([list(map(lambda x: int(x.strip()), path.split(","))) for path in line.split("->")])

temp_stones = np.vstack(stones)

border_left, _ = np.min(temp_stones, axis=0)
border_right, endless_bottom = np.max(temp_stones, axis=0)

border_left  -= 1
border_right += 1

cave = np.zeros((endless_bottom+1, border_right-border_left), dtype=np.int32)

for stone in stones:
    for from_, to_ in zip(stone, stone[1:]):
        from_x, from_y = from_
        to_x, to_y = to_
        
        from_x -= border_left
        to_x -= border_left
        # i am way to lazy for that ;)
        cv2.line(cave, (from_x, from_y), (to_x, to_y), color=(1), thickness=1)
        
sand_spawn = 500 - border_left, 0

has_reached_endless_bottom = False
sand_counter = 0
while not has_reached_endless_bottom:
    sd_x, sd_y = sand_spawn
    
    can_move = True
    while can_move:
        # first look down!
        if cave[sd_y + 1, sd_x] == 0:
            sd_y += 1
        # then check check down left!
        elif cave[sd_y + 1, sd_x - 1] == 0:
            sd_x -= 1
            sd_y += 1
        elif cave[sd_y + 1, sd_x + 1] == 0:
            sd_x += 1
            sd_y += 1
        else:
            can_move = False
            cave[sd_y, sd_x] = 2
            sand_counter += 1
            
        if sd_y == endless_bottom:
            can_move = False
            has_reached_endless_bottom = True

print(cave)
print(sand_counter)


# Task 2
# copy and paste task1 and just do slight modifications!
lines = pathlib.Path("input.txt").read_text().split("\n")
stones = []
for line in lines:
    stones.append([list(map(lambda x: int(x.strip()), path.split(","))) for path in line.split("->")])

temp_stones = np.vstack(stones)

_, not_so_endless_bottom = np.max(temp_stones, axis=0)

border_left  = 0
border_right = 1000
not_so_endless_bottom += 2

cave = np.zeros((not_so_endless_bottom+1, border_right), dtype=np.int32)
stones.append([[border_left,not_so_endless_bottom], [border_right, not_so_endless_bottom]])

for stone in stones:
    for from_, to_ in zip(stone, stone[1:]):
        from_x, from_y = from_
        to_x, to_y = to_
        
        from_x -= border_left
        to_x -= border_left
        # i am way to lazy for that ;)
        cv2.line(cave, (from_x, from_y), (to_x, to_y), color=(1), thickness=1)
        
sand_spawn = 500, 0

has_reached_top = False
sand_counter = 0
while not has_reached_top:
    sd_x, sd_y = sand_spawn
    
    can_move = True
    while can_move:
        # first look down!
        if cave[sd_y + 1, sd_x] == 0:
            sd_y += 1
        # then check check down left!
        elif cave[sd_y + 1, sd_x - 1] == 0:
            sd_x -= 1
            sd_y += 1
        elif cave[sd_y + 1, sd_x + 1] == 0:
            sd_x += 1
            sd_y += 1
        else:
            can_move = False
            cave[sd_y, sd_x] = 2
            sand_counter += 1
            
        if sd_x == sand_spawn[0] and sd_y == sand_spawn[1]:
            can_move = False
            has_reached_top = True

print(cave)
print(sand_counter)