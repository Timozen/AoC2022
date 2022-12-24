import collections
import pathlib

Dir = collections.namedtuple('Dir', ['x', 'y'])
Pos = collections.namedtuple('Pos', ['x', 'y'])

DIRS = [Dir(0, -1), Dir(0, 1), Dir(-1, 0), Dir(1, 0), Dir(0, 0)]

def in_field(pos: Pos, src: Pos, width: int, height: int) -> bool:
    return (0 <= pos.x < width and 0 <= pos.y < height) or pos == src

def rotate_and_check(hc, x1, x2, step):
    hc[x1].rotate(step)
    val = hc[x1][x2]
    hc[x1].rotate(-step)
    return val

def is_occupied_at_step(step: int, pos: Pos, hurricanes: dict[str, list[collections.deque[bool]]]) -> bool:
    # check for each hurricane direction if the position would be occupied at the given step
    # first theck the y axis
    if rotate_and_check(hurricanes["NS"], pos.x, pos.y,  step):
        return True
    if rotate_and_check(hurricanes["SN"], pos.x, pos.y, -step):
        return True
    if rotate_and_check(hurricanes["WE"], pos.y, pos.x,  step):
        return True
    if rotate_and_check(hurricanes["EW"], pos.y, pos.x, -step):
        return True
    return False

def path_bfs_at_step(step:int, src: Pos, dst: Pos, width:int, height: int, hurricanes: dict[str, list[collections.deque[bool]]]) -> int:
    to_visit = set([src])
    reached = False
    while not reached:
        next_visit = set()
        while not reached and to_visit:
            pos = to_visit.pop()
            if pos != src and is_occupied_at_step(step, pos, hurricanes):
                continue
            reached = pos == dst
            for dir in DIRS:
                new_pos = Pos(pos.x + dir.x, pos.y + dir.y)
                if in_field(new_pos, src, width, height):
                    next_visit.add(new_pos)
                        
        to_visit = next_visit
        step += 1
    return step
    
lines = pathlib.Path('input.txt').read_text().splitlines()
# ignore the edges of the mountain
mountain_top = [[char for char in line[1:-1]] for line in lines[1:-1]]
width, height = len(mountain_top[0]), len(mountain_top)

hurricanes: dict[str, list] = {
    "NS" : [],
    "SN" : [],
    "WE" : [],
    "EW" : [],
}

for row in range(height):
    hurricanes["WE"].append(collections.deque([True if char == '>' else False for char in mountain_top[row]]))
    hurricanes["EW"].append(collections.deque([True if char == '<' else False for char in mountain_top[row]]))

for col in range(width):
    hurricanes["NS"].append(collections.deque([True if char == 'v' else False for char in [line[col] for line in mountain_top]]))
    hurricanes["SN"].append(collections.deque([True if char == '^' else False for char in [line[col] for line in mountain_top]]))

# going from src to dst, then from dst to src, then from src to dst
src1 = Pos(0, -1)
dst1 = Pos(width - 1, height-1)

src2 = Pos(width - 1, height) # be sure to start on the other side of the mountain
dst2 = Pos(0, 0)              # and the dst is on the other side of the mountain

walk_0 = 0
walk_1 = path_bfs_at_step(walk_0, src1, dst1, width, height, hurricanes) + 1 # magic +1
walk_2 = path_bfs_at_step(walk_1, src2, dst2, width, height, hurricanes)
walk_3 = path_bfs_at_step(walk_2, src1, dst1, width, height, hurricanes)

print("Task 1", walk_1)
print("Task 2", walk_3)