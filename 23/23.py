import pathlib
import collections

DIR = collections.namedtuple('DIR', ['x', 'y'])

DIRS = {
    "N":  DIR( 0, -1),
    "S":  DIR( 0,  1),
    "E":  DIR( 1,  0),
    "W":  DIR(-1,  0),
    "NE": DIR( 1, -1),
    "NW": DIR(-1, -1),
    "SE": DIR( 1,  1),
    "SW": DIR(-1,  1),
}
DIRS_ALL = {
    "A" : list(DIRS.keys()),
    "N" : ["N", "NE", "NW"],
    "S" : ["S", "SE", "SW"],
    "E" : ["E", "NE", "SE"],
    "W" : ["W", "NW", "SW"],
}

def field_size(elves: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    return (
        min(elves, key=lambda x: x[0])[0],
        min(elves, key=lambda x: x[1])[1],
        max(elves, key=lambda x: x[0])[0],
        max(elves, key=lambda x: x[1])[1]
    )

def print_elves_location(elves: set[tuple[int,int]]) -> None:
    # the locations are in an arbitrary range, so we need to find the max x and y, and the min x and y
    min_x, min_y, max_x, max_y = field_size(elves)
    # move the min_x and min_y to 0,0
    offset_x = abs(min_x)
    offset_y = abs(min_y)
    min_x, min_y = 0, 0
    max_x, max_y = max_x + offset_x, max_y + offset_y
    
    grid = [['.' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y in elves:
        grid[y + offset_y][x + offset_x] = '#'
        
    for row in grid:
        print(''.join(row))

def has_adjacent_elves(elves: set[tuple[int,int]], elve: tuple[int,int], d:str="A") -> bool:
    for key in DIRS_ALL[d]:
        dir = DIRS[key]
        if (elve[0] + dir.x, elve[1] + dir.y) in elves:
            return True
    return False

def elve_move(elve: tuple[int,int], d: str) -> tuple[int,int]:
    dir = DIRS[d]
    return (elve[0] + dir.x, elve[1] + dir.y)

def get_or_create(d: dict, key: tuple[int, int], default: list) -> list:
    if key not in d:
        d[key] = default
    return d[key]

def diffuse(elves: set[tuple[int,int]], move_dirs: collections.deque[str]) -> bool:
    new_location = {}
    
    any_moved = False
    for elve in elves:
        # no adjacent elves, so he stays in place
        if not has_adjacent_elves(elves, elve):
            continue
        
        any_moved = True
        for d in move_dirs:
            # no adjacent elves in this direction, so he moves in this direction
            if not has_adjacent_elves(elves, elve, d):
                loc = elve_move(elve, d)
                get_or_create(new_location, loc, []).append(elve)
                break
        
    movable_elves = {}
    # second half of the round:
    # now the elves move simultaneously but if two elves want to move to the same location, they both stay in place
    for loc, elvs in new_location.items():
        if len(elvs) == 1:
            # only one elf wants to move to this location, so he moves
            movable_elves[elvs[0]] = loc

    # update the existing set!
    for elve, new_loc in movable_elves.items():
        if new_loc != elve:
            elves.remove(elve)
            elves.add(new_loc)        
    
    return any_moved

lines = pathlib.Path('input.txt').read_text().splitlines()

# # are the elves and . is empty space
elves = set((x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == '#')
move_dirs = collections.deque(["N", "S", "W", "E"])

for rdx in range(10):
    # first half of the round:
    # each elf checks if there is any elf close to him, if yes, he moves by certain rules!
    diffuse(elves, move_dirs)   
    move_dirs.rotate(-1)

min_x, min_y, max_x, max_y = field_size(elves)
# compute the field size
f_size = (max_x - min_x + 1) * (max_y - min_y + 1)
print("Task 1", f_size - len(elves))

# Task 2
# continue until no elf moves
# # are the elves and . is empty space
elves = set((x, y) for y, line in enumerate(lines) for x, c in enumerate(line) if c == '#')
move_dirs = collections.deque(["N", "S", "W", "E"])

round_cnt = 0
while diffuse(elves, move_dirs):
    round_cnt += 1
    move_dirs.rotate(-1)

print("Task 2", round_cnt)


    
    