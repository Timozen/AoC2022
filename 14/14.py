import pathlib
import numpy as np
import cv2

def move_sand(cave: np.ndarray, condition: callable) -> int:
    sand_spawn = 500 , 0
    partiles_move = False
    sand_counter = 0
    while not partiles_move:
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
                
            if condition(sd_x, sd_y):
                can_move = False
                partiles_move = True
    return sand_counter     

def draw_stones(cave: np.ndarray, stones: list) -> np.ndarray:
    for stone in stones:
        for from_, to_ in zip(stone, stone[1:]):
            from_x, from_y = from_
            to_x, to_y = to_
            
            from_x -= border_left
            to_x -= border_left
            # i am way to lazy for that ;)
            cv2.line(cave, (from_x, from_y), (to_x, to_y), color=(1), thickness=1)
            
    return cave

# Task 1
lines = pathlib.Path("input.txt").read_text().split("\n")
stones = []
for line in lines:
    stones.append([list(map(lambda x: int(x.strip()), path.split(","))) for path in line.split("->")])

_, not_so_endless_bottom = np.max(np.vstack(stones), axis=0)

border_left  = 0
border_right = 1000
not_so_endless_bottom += 2

cave = np.zeros((not_so_endless_bottom+1, border_right), dtype=np.int32)
cave = draw_stones(cave, stones)
        
print("Task 1", move_sand(cave, lambda _, y: y==not_so_endless_bottom))

# Task 2
stones.append([[border_left,not_so_endless_bottom], [border_right, not_so_endless_bottom]])
cave = np.zeros((not_so_endless_bottom+1, border_right), dtype=np.int32)
cave = draw_stones(cave, stones)
        
print("Task 2", move_sand(cave, lambda x, y: x == 500 and y == 0))
    